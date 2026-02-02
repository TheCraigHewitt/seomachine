#!/usr/bin/env python3
"""
SEO Baseline Analysis
Pulls comprehensive data from DataForSEO, GSC, and GA4 to establish
current position for high buyer-intent keywords.

Configure keywords in config/competitors.json under "bofu_keywords" and "mofu_keywords".
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('data_sources/config/.env')

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources', 'modules'))

from dataforseo import DataForSEO
from google_search_console import GoogleSearchConsole


def load_config():
    """Load keyword configuration from config file."""
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

    print("=" * 70)
    print(f"{company_name.upper()} SEO BASELINE ANALYSIS")
    print("Focus: MOFU/BOFU High Buyer-Intent Keywords")
    print("=" * 70)
    print()

    # Initialize clients
    try:
        dfs = DataForSEO()
        print("✓ DataForSEO connected")
    except Exception as e:
        print(f"✗ DataForSEO error: {e}")
        dfs = None

    try:
        gsc = GoogleSearchConsole()
        print("✓ Google Search Console connected")
    except Exception as e:
        print(f"✗ GSC error: {e}")
        gsc = None

    print()

    bofu_keywords = config.get('bofu_keywords', [])
    mofu_keywords = config.get('mofu_keywords', [])

    if not bofu_keywords and not mofu_keywords:
        print("No keywords configured. Add 'bofu_keywords' and 'mofu_keywords' to config/competitors.json")
        print("See config/competitors.example.json for format.")
        return

    # =================================================================
    # SECTION 1: DataForSEO Rankings
    # =================================================================
    ranking_on_page_1 = []
    ranking_page_2_3 = []
    not_ranking = []
    mofu_page_1 = []
    mofu_page_2_3 = []
    mofu_not_ranking = []

    if dfs:
        print("=" * 70)
        print("SECTION 1: KEYWORD RANKINGS (DataForSEO Live SERP)")
        print("=" * 70)

        if bofu_keywords:
            # Core BOFU Keywords - Bottom of Funnel (Ready to Buy)
            print("\n" + "-" * 70)
            print("BOFU KEYWORDS (Bottom of Funnel - Ready to Buy)")
            print("-" * 70)

            print("\nChecking BOFU keyword rankings (this may take a minute)...")
            try:
                bofu_rankings = dfs.get_rankings(site_domain, bofu_keywords)

                for r in bofu_rankings:
                    if r['position']:
                        if r['position'] <= 10:
                            ranking_on_page_1.append(r)
                        elif r['position'] <= 30:
                            ranking_page_2_3.append(r)
                        else:
                            not_ranking.append(r)
                    else:
                        not_ranking.append(r)

                print(f"\n  🏆 Page 1 Rankings ({len(ranking_on_page_1)})")
                for r in sorted(ranking_on_page_1, key=lambda x: x['position']):
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    #{r['position']:2d} | {r['keyword']:<45} | Vol: {vol}")

                print(f"\n  📈 Page 2-3 Quick Wins ({len(ranking_page_2_3)})")
                for r in sorted(ranking_page_2_3, key=lambda x: x['position']):
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    #{r['position']:2d} | {r['keyword']:<45} | Vol: {vol}")

                print(f"\n  ❌ Not Ranking/Beyond Page 3 ({len(not_ranking)})")
                for r in not_ranking[:15]:
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    --  | {r['keyword']:<45} | Vol: {vol}")
                if len(not_ranking) > 15:
                    print(f"    ... and {len(not_ranking) - 15} more")

            except Exception as e:
                print(f"Error fetching BOFU rankings: {e}")

        if mofu_keywords:
            # MOFU Keywords - Middle of Funnel
            print("\n" + "-" * 70)
            print("MOFU KEYWORDS (Middle of Funnel - Researching)")
            print("-" * 70)

            print("\nChecking MOFU keyword rankings (this may take a minute)...")
            try:
                mofu_rankings = dfs.get_rankings(site_domain, mofu_keywords)

                for r in mofu_rankings:
                    if r['position']:
                        if r['position'] <= 10:
                            mofu_page_1.append(r)
                        elif r['position'] <= 30:
                            mofu_page_2_3.append(r)
                        else:
                            mofu_not_ranking.append(r)
                    else:
                        mofu_not_ranking.append(r)

                print(f"\n  🏆 Page 1 Rankings ({len(mofu_page_1)})")
                for r in sorted(mofu_page_1, key=lambda x: x['position']):
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    #{r['position']:2d} | {r['keyword']:<45} | Vol: {vol}")

                print(f"\n  📈 Page 2-3 Quick Wins ({len(mofu_page_2_3)})")
                for r in sorted(mofu_page_2_3, key=lambda x: x['position']):
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    #{r['position']:2d} | {r['keyword']:<45} | Vol: {vol}")

                print(f"\n  ❌ Not Ranking/Beyond Page 3 ({len(mofu_not_ranking)})")
                for r in mofu_not_ranking[:15]:
                    vol = f"{r['search_volume']:,}" if r['search_volume'] else "N/A"
                    print(f"    --  | {r['keyword']:<45} | Vol: {vol}")
                if len(mofu_not_ranking) > 15:
                    print(f"    ... and {len(mofu_not_ranking) - 15} more")

            except Exception as e:
                print(f"Error fetching MOFU rankings: {e}")

    # =================================================================
    # SECTION 2: GSC Data - Real Performance Data
    # =================================================================
    high_intent_keywords = []
    page_1 = []
    page_2 = []
    page_3_plus = []
    total_impressions_p1 = 0
    total_impressions_p2 = 0

    if gsc:
        print("\n" + "=" * 70)
        print("SECTION 2: GOOGLE SEARCH CONSOLE DATA (Last 30 Days)")
        print("=" * 70)

        print("\nFetching keyword data from GSC...")

        try:
            all_keywords = gsc.get_keyword_positions(days=30, limit=2000)

            # Use relevant_terms from config for filtering, or accept all
            relevant_terms = config.get('relevant_terms', [])
            skip_terms = config.get('skip_terms', [
                'celebrity', 'net worth', 'wife', 'husband', 'age', 'height',
                'who is', 'biography', 'famous', 'died', 'death', 'married',
                'dating', 'girlfriend', 'boyfriend', 'kids', 'children',
                'family', 'instagram', 'twitter', 'tiktok', 'reddit'
            ])

            for kw in all_keywords:
                keyword = kw['keyword'].lower()

                if any(term in keyword for term in skip_terms):
                    continue

                # If relevant_terms configured, filter by them; otherwise include all
                if relevant_terms:
                    if any(term.lower() in keyword for term in relevant_terms):
                        high_intent_keywords.append(kw)
                else:
                    high_intent_keywords.append(kw)

            high_intent_keywords.sort(key=lambda x: x['impressions'], reverse=True)

            print(f"\nFound {len(high_intent_keywords)} high-intent keywords (filtered from {len(all_keywords)} total)\n")

            page_1 = [k for k in high_intent_keywords if k['position'] <= 10]
            page_2 = [k for k in high_intent_keywords if 10 < k['position'] <= 20]
            page_3_plus = [k for k in high_intent_keywords if k['position'] > 20]

            print(f"📊 DISTRIBUTION:")
            print(f"  Page 1 (positions 1-10): {len(page_1)} keywords")
            print(f"  Page 2 (positions 11-20): {len(page_2)} keywords")
            print(f"  Page 3+ (positions 21+): {len(page_3_plus)} keywords")

            total_impressions_p1 = sum(k['impressions'] for k in page_1)
            total_clicks_p1 = sum(k['clicks'] for k in page_1)
            total_impressions_p2 = sum(k['impressions'] for k in page_2)
            total_clicks_p2 = sum(k['clicks'] for k in page_2)

            print(f"\n  Page 1 Performance: {total_impressions_p1:,} impressions, {total_clicks_p1:,} clicks")
            print(f"  Page 2 Opportunity: {total_impressions_p2:,} impressions, {total_clicks_p2:,} clicks")

            print(f"\n🏆 TOP PAGE 1 KEYWORDS (by impressions):")
            print("-" * 70)
            for kw in page_1[:25]:
                ctr_pct = kw['ctr'] * 100
                print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:50]:<50} | {kw['impressions']:>6,} imp | {kw['clicks']:>4} clicks | {ctr_pct:.1f}% CTR")

            print(f"\n📈 TOP QUICK WIN OPPORTUNITIES (Page 2 - Position 11-20):")
            print("-" * 70)
            for kw in page_2[:25]:
                ctr_pct = kw['ctr'] * 100
                print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:50]:<50} | {kw['impressions']:>6,} imp | {kw['clicks']:>4} clicks | {ctr_pct:.1f}% CTR")

            # Get official quick wins analysis
            print("\n" + "-" * 70)
            print("COMMERCIAL INTENT ANALYSIS")
            print("-" * 70)

            quick_wins = gsc.get_quick_wins(days=30, min_impressions=30)

            filtered_wins = []
            for qw in quick_wins:
                keyword = qw['keyword'].lower()
                if not any(term in keyword for term in skip_terms):
                    filtered_wins.append(qw)

            transactional = [w for w in filtered_wins if w.get('commercial_intent_category') == 'Transactional']
            commercial_inv = [w for w in filtered_wins if w.get('commercial_intent_category') == 'Commercial Investigation']
            informational_rel = [w for w in filtered_wins if w.get('commercial_intent_category') == 'Informational (Relevant)']

            print(f"\nQuick Win Breakdown by Commercial Intent:")
            print(f"  Transactional (Ready to Buy): {len(transactional)}")
            print(f"  Commercial Investigation: {len(commercial_inv)}")
            print(f"  Informational (Relevant): {len(informational_rel)}")

            print(f"\nTop 20 TRANSACTIONAL Quick Wins:")
            for i, qw in enumerate(transactional[:20], 1):
                print(f"  {i:2d}. #{qw['position']:.1f} | {qw['keyword'][:45]:<45} | {qw['impressions']:,} imp | Score: {qw['opportunity_score']:.0f}")

            print(f"\nTop 20 COMMERCIAL INVESTIGATION Quick Wins:")
            for i, qw in enumerate(commercial_inv[:20], 1):
                print(f"  {i:2d}. #{qw['position']:.1f} | {qw['keyword'][:45]:<45} | {qw['impressions']:,} imp | Score: {qw['opportunity_score']:.0f}")

        except Exception as e:
            print(f"Error fetching GSC data: {e}")
            import traceback
            traceback.print_exc()

    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "=" * 70)
    print("BASELINE SUMMARY")
    print("=" * 70)

    if dfs and bofu_keywords:
        total_bofu = len(bofu_keywords)
        bofu_page_1_pct = (len(ranking_on_page_1) / total_bofu) * 100 if total_bofu else 0
        bofu_quick_win_pct = (len(ranking_page_2_3) / total_bofu) * 100 if total_bofu else 0

        total_mofu = len(mofu_keywords)
        mofu_page_1_pct = (len(mofu_page_1) / total_mofu) * 100 if total_mofu else 0
        mofu_quick_win_pct = (len(mofu_page_2_3) / total_mofu) * 100 if total_mofu else 0

        print(f"""
DATAFORSEO RANKINGS (Live SERP Check):
--------------------------------------
BOFU Keywords (High Buyer Intent):
  - Total Tracked: {total_bofu}
  - Page 1: {len(ranking_on_page_1)} ({bofu_page_1_pct:.0f}%)
  - Page 2-3 (Quick Wins): {len(ranking_page_2_3)} ({bofu_quick_win_pct:.0f}%)
  - Not Ranking: {len(not_ranking)} ({100 - bofu_page_1_pct - bofu_quick_win_pct:.0f}%)

MOFU Keywords (Research Phase):
  - Total Tracked: {total_mofu}
  - Page 1: {len(mofu_page_1)} ({mofu_page_1_pct:.0f}%)
  - Page 2-3 (Quick Wins): {len(mofu_page_2_3)} ({mofu_quick_win_pct:.0f}%)
  - Not Ranking: {len(mofu_not_ranking)} ({100 - mofu_page_1_pct - mofu_quick_win_pct:.0f}%)
""")

    if gsc and high_intent_keywords:
        print(f"""
GSC PERFORMANCE (Actual Traffic Data):
--------------------------------------
High-Intent Keywords:
  - Total Tracked: {len(high_intent_keywords)}
  - Page 1 Rankings: {len(page_1)}
  - Quick Win Opportunities (Page 2): {len(page_2)}
  - Page 3+ (Need Work): {len(page_3_plus)}

Traffic Potential:
  - Current Page 1 Impressions: {total_impressions_p1:,}
  - Page 2 Impressions (Quick Win Potential): {total_impressions_p2:,}
""")

    print("=" * 70)
    print("Analysis Complete - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)

if __name__ == "__main__":
    main()
