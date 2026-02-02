#!/usr/bin/env python3
"""
Competitor SEO Analysis
Compares your site vs configured competitors on key keywords.

Configure competitors in config/competitors.json.
"""

import os
import sys
import json
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()
load_dotenv('data_sources/config/.env')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources', 'modules'))

from dataforseo import DataForSEO


def load_config():
    """Load configuration from config file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'competitors.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    print("WARNING: config/competitors.json not found. See config/competitors.example.json")
    return {}


def main():
    config = load_config()
    site_domain = os.getenv('GSC_SITE_URL', 'yoursite.com').replace('https://', '').replace('http://', '').rstrip('/')
    company_name = os.getenv('COMPANY_NAME', 'Your Company')

    # Build competitors dict: our site + configured competitors
    competitors = {site_domain: company_name}
    for domain in config.get('direct_competitors', []):
        name = domain.split('.')[0].capitalize()
        competitors[domain] = name

    comp_names = list(competitors.values())

    print("=" * 90)
    print(f"COMPETITOR SEO ANALYSIS: {company_name.upper()} VS COMPETITORS")
    print("=" * 90)

    dfs = DataForSEO()

    bofu_keywords = config.get('bofu_keywords', [])
    mofu_keywords = config.get('mofu_keywords', [])
    relevant_terms = config.get('relevant_terms', [])

    if not bofu_keywords:
        print("\nNo bofu_keywords configured in config/competitors.json")
        return

    # =========================================================================
    # SECTION 1: HEAD-TO-HEAD ON BOFU KEYWORDS
    # =========================================================================
    print("\n" + "=" * 90)
    print("SECTION 1: HEAD-TO-HEAD BOFU KEYWORD RANKINGS")
    print("=" * 90)

    all_rankings = defaultdict(dict)

    for keyword in bofu_keywords:
        print(f"\n>>> Checking: '{keyword}'")
        try:
            serp = dfs.get_serp_data(keyword, limit=100)

            volume = serp.get('search_volume')
            print(f"    Search Volume: {volume:,}" if volume else "    Search Volume: N/A")

            for result in serp.get('organic_results', []):
                domain = result.get('domain', '')
                for comp_domain, comp_name in competitors.items():
                    if comp_domain in domain:
                        pos = result.get('position')
                        all_rankings[keyword][comp_name] = pos
                        break

            print(f"    Rankings:")
            for comp_name in comp_names:
                pos = all_rankings[keyword].get(comp_name, '-')
                if pos != '-':
                    status = "✅" if pos <= 10 else "📈" if pos <= 20 else "❌"
                    print(f"      {status} {comp_name:12s}: #{pos}")
                else:
                    print(f"      ⚫ {comp_name:12s}: Not in top 100")

        except Exception as e:
            print(f"    Error: {e}")

    # =========================================================================
    # SECTION 2: RANKING COMPARISON TABLE
    # =========================================================================
    print("\n" + "=" * 90)
    print("SECTION 2: COMPLETE RANKING COMPARISON TABLE")
    print("=" * 90)

    # Build header
    header = f"{'Keyword':<40}"
    for name in comp_names:
        header += f" | {name:>{max(8, len(name))}}"
    print(f"\n{header}")
    print("-" * len(header))

    for keyword in bofu_keywords:
        row = f"{keyword:<40}"
        for name in comp_names:
            pos = all_rankings[keyword].get(name, '-')
            pos_str = f"#{pos}" if pos != '-' else '-'
            row += f" | {pos_str:>{max(8, len(name))}}"
        print(row)

    # =========================================================================
    # SECTION 3: COMPETITOR KEYWORD ANALYSIS
    # =========================================================================
    print("\n" + "=" * 90)
    print("SECTION 3: COMPETITOR RANKED KEYWORDS (Top 300)")
    print("=" * 90)

    competitor_keywords = {}

    for domain, name in competitors.items():
        if domain == site_domain:
            continue

        print(f"\n>>> Fetching top keywords for {name} ({domain})...")
        try:
            keywords = dfs.get_domain_keywords(domain, position_max=20, limit=300)
            competitor_keywords[name] = keywords

            # Filter for relevant keywords if terms configured
            if relevant_terms:
                filtered = [k for k in keywords if any(term.lower() in k['keyword'].lower()
                    for term in relevant_terms)]
            else:
                filtered = keywords

            print(f"    Total ranked keywords (top 20): {len(keywords)}")
            if relevant_terms:
                print(f"    Industry-relevant keywords: {len(filtered)}")

            if filtered:
                print(f"\n    Top 20 Keywords for {name}:")
                for i, kw in enumerate(sorted(filtered, key=lambda x: x['search_volume'] or 0, reverse=True)[:20], 1):
                    vol = f"{kw['search_volume']:,}" if kw['search_volume'] else "N/A"
                    print(f"      {i:2d}. #{kw['position']:2d} | {kw['keyword'][:50]:<50} | Vol: {vol}")

        except Exception as e:
            print(f"    Error fetching keywords: {e}")
            competitor_keywords[name] = []

    # =========================================================================
    # SECTION 4: KEYWORD GAP ANALYSIS
    # =========================================================================
    print("\n" + "=" * 90)
    print("SECTION 4: KEYWORD GAP ANALYSIS")
    print(f"Where competitors rank but {company_name} doesn't")
    print("=" * 90)

    print(f"\n>>> Fetching {company_name} ranked keywords...")
    try:
        our_keywords = dfs.get_domain_keywords(site_domain, position_max=50, limit=500)
        our_kw_set = set(k['keyword'].lower() for k in our_keywords)
        print(f"    {company_name} ranked keywords (top 50): {len(our_keywords)}")
    except Exception as e:
        print(f"    Error: {e}")
        our_keywords = []
        our_kw_set = set()

    for name, keywords in competitor_keywords.items():
        gaps = []
        for kw in keywords:
            keyword_lower = kw['keyword'].lower()
            if relevant_terms:
                if any(term.lower() in keyword_lower for term in relevant_terms):
                    if keyword_lower not in our_kw_set:
                        gaps.append(kw)
            else:
                if keyword_lower not in our_kw_set:
                    gaps.append(kw)

        if gaps:
            print(f"\n>>> {name} ranks for these keywords where {company_name} doesn't:")
            gaps_sorted = sorted(gaps, key=lambda x: x['search_volume'] or 0, reverse=True)
            for kw in gaps_sorted[:15]:
                vol = f"{kw['search_volume']:,}" if kw['search_volume'] else "N/A"
                print(f"    #{kw['position']:2d} | {kw['keyword'][:55]:<55} | Vol: {vol}")

    # =========================================================================
    # SECTION 5: WIN/LOSS ANALYSIS
    # =========================================================================
    print("\n" + "=" * 90)
    print("SECTION 5: HEAD-TO-HEAD WIN/LOSS ANALYSIS")
    print("=" * 90)

    for comp_name in [n for n in comp_names if n != company_name]:
        wins = 0
        losses = 0
        ties = 0
        win_keywords = []
        loss_keywords = []

        for keyword, rankings in all_rankings.items():
            our_pos = rankings.get(company_name)
            comp_pos = rankings.get(comp_name)

            if our_pos and comp_pos:
                if our_pos < comp_pos:
                    wins += 1
                    win_keywords.append((keyword, our_pos, comp_pos))
                elif our_pos > comp_pos:
                    losses += 1
                    loss_keywords.append((keyword, our_pos, comp_pos))
                else:
                    ties += 1
            elif our_pos and not comp_pos:
                wins += 1
                win_keywords.append((keyword, our_pos, '-'))
            elif comp_pos and not our_pos:
                losses += 1
                loss_keywords.append((keyword, '-', comp_pos))

        print(f"\n>>> {company_name} vs {comp_name}:")
        print(f"    Wins: {wins} | Losses: {losses} | Ties: {ties}")

        if win_keywords:
            print(f"\n    Keywords where {company_name} WINS:")
            for kw, c_pos, comp_pos in sorted(win_keywords, key=lambda x: x[1] if x[1] != '-' else 999)[:5]:
                print(f"      {kw}: {company_name} #{c_pos} vs {comp_name} #{comp_pos}")

        if loss_keywords:
            print(f"\n    Keywords where {company_name} LOSES:")
            for kw, c_pos, comp_pos in sorted(loss_keywords, key=lambda x: x[2] if x[2] != '-' else 999)[:5]:
                print(f"      {kw}: {company_name} #{c_pos} vs {comp_name} #{comp_pos}")

    # =========================================================================
    # SECTION 6: MOFU KEYWORDS COMPARISON
    # =========================================================================
    if mofu_keywords:
        print("\n" + "=" * 90)
        print("SECTION 6: MOFU KEYWORDS COMPARISON")
        print("=" * 90)

        mofu_rankings = defaultdict(dict)

        for keyword in mofu_keywords:
            print(f"\n>>> Checking: '{keyword}'")
            try:
                serp = dfs.get_serp_data(keyword, limit=50)

                for result in serp.get('organic_results', []):
                    domain = result.get('domain', '')
                    for comp_domain, comp_name in competitors.items():
                        if comp_domain in domain:
                            mofu_rankings[keyword][comp_name] = result.get('position')
                            break

                for comp_name in comp_names:
                    pos = mofu_rankings[keyword].get(comp_name)
                    if pos:
                        print(f"    {comp_name:12s}: #{pos}")

            except Exception as e:
                print(f"    Error: {e}")

        # Print MOFU comparison table
        header = f"{'MOFU Keyword':<35}"
        for name in comp_names:
            header += f" | {name:>{max(8, len(name))}}"
        print(f"\n{header}")
        print("-" * len(header))

        for keyword in mofu_keywords:
            row = f"{keyword:<35}"
            for name in comp_names:
                pos = mofu_rankings[keyword].get(name, '-')
                pos_str = f"#{pos}" if pos != '-' else '-'
                row += f" | {pos_str:>{max(8, len(name))}}"
            print(row)

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 90)
    print("COMPETITIVE ANALYSIS SUMMARY")
    print("=" * 90)

    print("\n>>> Page 1 Rankings Count (BOFU Keywords):")
    for comp_name in comp_names:
        page_1_count = sum(1 for kw in all_rankings.values()
                          if kw.get(comp_name) and kw.get(comp_name) <= 10)
        page_2_count = sum(1 for kw in all_rankings.values()
                          if kw.get(comp_name) and 10 < kw.get(comp_name) <= 20)
        not_ranking_count = sum(1 for kw in all_rankings.values()
                          if not kw.get(comp_name))
        print(f"    {comp_name:12s}: Page 1: {page_1_count} | Page 2: {page_2_count} | Not ranking: {not_ranking_count}")

    print("\n" + "=" * 90)
    print("ANALYSIS COMPLETE")
    print("=" * 90)

if __name__ == "__main__":
    main()
