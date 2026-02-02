#!/usr/bin/env python3
"""
Detailed BOFU Keyword Rankings Analysis
Checks specific high-value buyer-intent keywords.

Configure keywords in config/competitors.json under "bofu_keywords" and "alternative_keywords".
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
load_dotenv('data_sources/config/.env')

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

    print("=" * 80)
    print(f"DETAILED BOFU KEYWORD ANALYSIS FOR {company_name.upper()}")
    print("=" * 80)

    # Initialize
    dfs = DataForSEO()
    gsc = GoogleSearchConsole()

    # CRITICAL BOFU Keywords from config
    critical_keywords = config.get('bofu_keywords', [])
    if not critical_keywords:
        print("\nNo bofu_keywords configured in config/competitors.json")
        return

    print("\n" + "=" * 80)
    print("PART 1: LIVE SERP CHECK (DataForSEO)")
    print("=" * 80)

    for keyword in critical_keywords[:20]:  # Limit to top 20 to control API costs
        print(f"\n>>> Checking: '{keyword}'")
        try:
            serp = dfs.get_serp_data(keyword, limit=50)

            print(f"    Search Volume: {serp.get('search_volume', 'N/A'):,}" if serp.get('search_volume') else "    Search Volume: N/A")
            print(f"    CPC: ${serp.get('cpc', 0):.2f}" if serp.get('cpc') else "    CPC: N/A")
            print(f"    Competition: {serp.get('competition', 'N/A')}")

            # Find our site in results
            our_pos = None
            our_url = None
            for result in serp.get('organic_results', []):
                if site_domain in result.get('domain', ''):
                    our_pos = result.get('position')
                    our_url = result.get('url')
                    break

            if our_pos:
                print(f"    ✓ RANKING: #{our_pos}")
                print(f"      URL: {our_url}")
            else:
                print(f"    ✗ NOT IN TOP 50")

            # Show top 5 results
            print(f"    Top 5 Results:")
            for result in serp.get('organic_results', [])[:5]:
                print(f"      #{result['position']:2d}. {result['domain']}")

        except Exception as e:
            print(f"    Error: {e}")

    # Competitor alternative keywords
    alternative_keywords = config.get('alternative_keywords', [])
    if alternative_keywords:
        print("\n" + "=" * 80)
        print("PART 2: COMPETITOR ALTERNATIVE KEYWORDS")
        print("=" * 80)

        for keyword in alternative_keywords:
            print(f"\n>>> Checking: '{keyword}'")
            try:
                serp = dfs.get_serp_data(keyword, limit=30)

                print(f"    Search Volume: {serp.get('search_volume', 'N/A'):,}" if serp.get('search_volume') else "    Search Volume: N/A")

                our_pos = None
                for result in serp.get('organic_results', []):
                    if site_domain in result.get('domain', ''):
                        our_pos = result.get('position')
                        break

                if our_pos:
                    print(f"    ✓ RANKING: #{our_pos}")
                else:
                    print(f"    ✗ NOT IN TOP 30")

                print(f"    Top 3 Results:")
                for result in serp.get('organic_results', [])[:3]:
                    print(f"      #{result['position']:2d}. {result['domain']}")

            except Exception as e:
                print(f"    Error: {e}")

    # GSC Data for relevant keywords
    print("\n" + "=" * 80)
    print("PART 3: GSC DATA - HIGH-INTENT KEYWORDS")
    print("=" * 80)

    all_keywords = gsc.get_keyword_positions(days=30, limit=2000)

    # Filter using relevant_terms from config
    relevant_terms = config.get('relevant_terms', [])
    skip_terms = config.get('skip_terms', [])

    hosting_keywords = []
    for kw in all_keywords:
        keyword = kw['keyword'].lower()
        if skip_terms and any(skip in keyword for skip in skip_terms):
            continue
        if relevant_terms:
            if any(term.lower() in keyword for term in relevant_terms):
                hosting_keywords.append(kw)
        else:
            hosting_keywords.append(kw)

    hosting_keywords.sort(key=lambda x: x['impressions'], reverse=True)

    print(f"\nFound {len(hosting_keywords)} high-intent keywords")
    print("-" * 80)

    page_1 = [k for k in hosting_keywords if k['position'] <= 10]
    page_2 = [k for k in hosting_keywords if 10 < k['position'] <= 20]
    page_3_plus = [k for k in hosting_keywords if k['position'] > 20]

    print(f"Page 1: {len(page_1)} | Page 2: {len(page_2)} | Page 3+: {len(page_3_plus)}")

    print(f"\n🏆 PAGE 1 KEYWORDS:")
    for kw in page_1[:30]:
        ctr = kw['ctr'] * 100
        print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

    print(f"\n📈 PAGE 2 QUICK WINS:")
    for kw in page_2[:20]:
        ctr = kw['ctr'] * 100
        print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

    print(f"\n❌ PAGE 3+ (Need Work):")
    for kw in page_3_plus[:15]:
        ctr = kw['ctr'] * 100
        print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

    # Check specific important queries from config
    key_queries = config.get('key_queries', critical_keywords[:10])
    if key_queries:
        print("\n" + "=" * 80)
        print("PART 4: KEY QUERY PERFORMANCE (GSC)")
        print("=" * 80)

        for query in key_queries:
            matches = [k for k in all_keywords if query.lower() in k['keyword'].lower()]
            if matches:
                best = min(matches, key=lambda x: x['position'])
                total_imp = sum(m['impressions'] for m in matches)
                total_clicks = sum(m['clicks'] for m in matches)
                print(f"\n'{query}':")
                print(f"  Best Position: #{best['position']:.1f} for '{best['keyword']}'")
                print(f"  Total Related Impressions: {total_imp:,}")
                print(f"  Total Related Clicks: {total_clicks}")
            else:
                print(f"\n'{query}': No data in GSC")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
