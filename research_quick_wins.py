#!/usr/bin/env python3
"""
Research Quick Win Opportunities

Identifies keywords ranking 11-20 (page 2) that can be pushed to page 1.
Combines data from Google Search Console, DataForSEO, and Google Analytics.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.dataforseo import DataForSEO
from modules.google_analytics import GoogleAnalytics
from modules.opportunity_scorer import OpportunityScorer, OpportunityType
from modules.search_intent_analyzer import SearchIntentAnalyzer

def main():
    print("=" * 80)
    print("QUICK WIN OPPORTUNITIES RESEARCH")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: Keywords ranking positions 11-20 (page 2 of Google)")
    print("=" * 80)

    # Initialize clients
    print("\n1. Initializing data sources...")
    try:
        gsc = GoogleSearchConsole()
        print("   ✓ Google Search Console connected")
    except Exception as e:
        print(f"   ✗ GSC Error: {e}")
        return

    try:
        dfs = DataForSEO()
        print("   ✓ DataForSEO connected")
    except Exception as e:
        print(f"   ⚠ DataForSEO Error: {e}")
        dfs = None

    try:
        ga = GoogleAnalytics()
        print("   ✓ Google Analytics 4 connected")
    except Exception as e:
        print(f"   ⚠ GA4 Error: {e}")
        ga = None

    # Initialize scoring and analysis modules
    scorer = OpportunityScorer()
    intent_analyzer = SearchIntentAnalyzer()
    print("   ✓ Enhanced scoring enabled")

    # Get quick wins from GSC
    print("\n2. Fetching keywords ranking positions 11-20...")
    quick_wins = gsc.get_quick_wins(
        days=30,
        position_min=11,
        position_max=20,
        min_impressions=50
    )

    if not quick_wins:
        print("   No quick win opportunities found.")
        return

    print(f"   ✓ Found {len(quick_wins)} quick win opportunities")

    # Analyze top opportunities
    print(f"\n3. Analyzing top {min(10, len(quick_wins))} opportunities...")
    print("\n" + "=" * 80)

    detailed_opportunities = []

    for i, kw in enumerate(quick_wins[:10], 1):
        keyword = kw['keyword']
        position = kw['position']
        impressions = kw['impressions']
        clicks = kw['clicks']
        ctr = kw['ctr'] * 100

        print(f"\n#{i} KEYWORD: {keyword}")
        print("-" * 80)
        print(f"Current Position: {position}")
        print(f"Impressions (30d): {impressions:,}")
        print(f"Clicks (30d): {clicks}")
        print(f"CTR: {ctr:.2f}%")
        print(f"Commercial Intent: {kw['commercial_intent_category']} ({kw['commercial_intent']}/3.0)")
        print(f"Opportunity Score: {kw['opportunity_score']:.2f}")
        print(f"Priority: {kw['priority'].upper()}")

        # Get current ranking URL and SERP data from DataForSEO
        serp_features = []
        difficulty = None
        if dfs:
            try:
                print(f"\nVerifying with DataForSEO...")
                rankings = dfs.get_rankings(
                    domain=os.getenv('GSC_SITE_URL', 'yoursite.com').replace('https://', '').replace('http://', '').rstrip('/'),
                    keywords=[keyword]
                )

                if rankings and rankings[0]['position']:
                    dfs_position = rankings[0]['position']
                    dfs_url = rankings[0]['url']
                    search_volume = rankings[0]['search_volume']
                    difficulty = rankings[0].get('difficulty')

                    print(f"  DataForSEO Position: {dfs_position}")
                    print(f"  Ranking URL: {dfs_url}")
                    if search_volume:
                        print(f"  Search Volume: {search_volume:,}/month")
                    if difficulty:
                        print(f"  SEO Difficulty: {difficulty}/100")

                    kw['dfs_position'] = dfs_position
                    kw['ranking_url'] = dfs_url
                    kw['search_volume'] = search_volume
                    kw['difficulty'] = difficulty
                else:
                    print(f"  Not found in top 100 (DataForSEO)")

                # Get SERP features for intent analysis
                try:
                    serp_data = dfs.get_serp_data(keyword, limit=10)
                    if serp_data and 'features' in serp_data:
                        serp_features = serp_data.get('features', [])
                        kw['serp_features'] = serp_features
                        if serp_features:
                            print(f"  SERP Features: {', '.join(serp_features[:3])}")
                except:
                    pass
            except Exception as e:
                print(f"  DataForSEO error: {e}")

        # Get page performance from GA4 (if we have the URL)
        if ga and kw.get('ranking_url'):
            try:
                # Extract path from URL
                from urllib.parse import urlparse
                path = urlparse(kw['ranking_url']).path

                print(f"\nChecking GA4 performance for {path}...")
                page_data = ga.get_page_performance(path, days=30)

                if page_data and 'pageviews' in page_data:
                    print(f"  Pageviews: {page_data['pageviews']:,}")
                    print(f"  Avg. Engagement: {page_data.get('avg_engagement_time', 0):.0f}s")
                    print(f"  Bounce Rate: {page_data.get('bounce_rate', 0):.1%}")

                    kw['pageviews'] = page_data['pageviews']
                    kw['engagement'] = page_data.get('avg_engagement_time', 0)
            except Exception as e:
                print(f"  GA4 error: {e}")

        # Calculate enhanced opportunity score
        print(f"\nEnhanced Scoring Analysis...")
        enhanced_score_result = scorer.calculate_score(
            keyword_data=kw,
            opportunity_type=OpportunityType.QUICK_WIN,
            search_volume=kw.get('search_volume'),
            difficulty=kw.get('difficulty'),
            serp_features=serp_features,
            cluster_value=50,  # Default - will be enhanced with topic clustering later
            trend_direction=None,  # Will be added with trend detection
            trend_percent=None
        )

        kw['enhanced_score'] = enhanced_score_result['final_score']
        kw['enhanced_priority'] = enhanced_score_result['priority']
        kw['score_breakdown'] = enhanced_score_result['score_breakdown']
        kw['primary_factor'] = enhanced_score_result['primary_factor']

        print(f"  Enhanced Score: {enhanced_score_result['final_score']}/100")
        print(f"  Priority: {enhanced_score_result['priority']}")
        print(f"  Key Factor: {enhanced_score_result['primary_factor']}")

        # Calculate traffic potential
        if kw.get('position') and kw.get('impressions'):
            traffic_potential = scorer.calculate_potential_traffic(
                current_position=kw['position'],
                target_position=7,  # Target middle of page 1
                impressions=kw['impressions'],
                current_clicks=kw['clicks']
            )
            kw['traffic_potential'] = traffic_potential
            print(f"  Potential: +{traffic_potential['additional_clicks']} clicks/month (+{traffic_potential['percent_increase']:.0f}%)")

        # Analyze search intent
        if serp_features:
            try:
                intent_result = intent_analyzer.analyze(
                    keyword=keyword,
                    serp_features=serp_features
                )
                # Handle SearchIntent enum or string
                primary_intent = intent_result.get('primary_intent', 'unknown')
                if hasattr(primary_intent, 'value'):
                    primary_intent = primary_intent.value
                kw['search_intent'] = str(primary_intent)
                kw['intent_confidence'] = float(intent_result.get('confidence', 0))
                print(f"  Search Intent: {kw['search_intent']} (confidence: {kw['intent_confidence']:.0f}%)")
            except Exception as e:
                print(f"  Intent analysis error: {e}")

        print("\nRECOMMENDATION:")
        recommendation = generate_recommendation(kw)
        print(f"  {recommendation}")

        kw['recommendation'] = recommendation
        detailed_opportunities.append(kw)

    # Re-sort by enhanced score
    detailed_opportunities.sort(
        key=lambda x: x.get('enhanced_score', x.get('opportunity_score', 0)),
        reverse=True
    )

    # Generate summary report
    print("\n\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)

    total_impressions = sum(k['impressions'] for k in detailed_opportunities)
    total_clicks = sum(k['clicks'] for k in detailed_opportunities)
    avg_position = sum(k['position'] for k in detailed_opportunities) / len(detailed_opportunities)

    print(f"\nQuick Wins Identified: {len(detailed_opportunities)}")
    print(f"Total Impressions: {total_impressions:,}")
    print(f"Total Current Clicks: {total_clicks}")
    print(f"Average Position: {avg_position:.1f}")

    # Estimate potential if moved to page 1
    # Position 5-7 typically has 5-7% CTR vs 1-2% on page 2
    estimated_new_ctr = 0.055  # 5.5%
    current_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    potential_clicks = int(total_impressions * estimated_new_ctr)
    additional_clicks = potential_clicks - total_clicks

    print(f"\nPOTENTIAL IMPACT:")
    print(f"Current CTR: {current_ctr:.2%}")
    print(f"Target CTR (positions 5-7): {estimated_new_ctr:.2%}")
    print(f"Potential Additional Clicks/Month: +{additional_clicks}")
    print(f"Total Potential Clicks: {potential_clicks}")

    # Top priorities
    print(f"\nTOP 3 PRIORITIES:")
    for i, kw in enumerate(detailed_opportunities[:3], 1):
        print(f"\n{i}. {kw['keyword']}")
        print(f"   Position {kw['position']} → Target: 5-7")
        print(f"   Current: {kw['clicks']} clicks → Potential: {int(kw['impressions'] * 0.055)} clicks")
        if kw.get('ranking_url'):
            print(f"   URL: {kw['ranking_url']}")

    # Write to markdown file
    print(f"\n\n4. Writing report to research/quick-wins-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(detailed_opportunities)

    print("\n" + "=" * 80)
    print("✅ RESEARCH COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/quick-wins-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Prioritize top 3-5 keywords to target first")
    print(f"3. Update content-priorities.md with findings")
    print(f"4. Start content optimization with top priority")


def generate_recommendation(kw):
    """Generate action recommendation based on keyword data"""
    position = kw['position']
    impressions = kw['impressions']
    clicks = kw['clicks']
    ctr = (clicks / impressions * 100) if impressions > 0 else 0

    recommendations = []

    # Position-based
    if position <= 13:
        recommendations.append("Strong candidate - very close to page 1")
    elif position <= 16:
        recommendations.append("Good opportunity - needs moderate optimization")
    else:
        recommendations.append("Requires more significant content improvements")

    # CTR-based
    if ctr < 1.5:
        recommendations.append("Also optimize title/meta for better CTR")

    # Impression volume
    if impressions > 1000:
        recommendations.append("HIGH VOLUME - prioritize this!")
    elif impressions > 500:
        recommendations.append("Good search volume")

    # Content actions
    if position > 15:
        recommendations.append("Consider: Add 500+ words, update examples, add visuals")
    else:
        recommendations.append("Consider: Refresh intro, update stats, improve formatting")

    return " | ".join(recommendations)


def write_markdown_report(opportunities):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/quick-wins-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Quick Win Opportunities\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Strategy:** Target keywords ranking positions 11-20 (page 2) to push to page 1\n\n")
        f.write(f"**Opportunities Found:** {len(opportunities)}\n\n")
        f.write("---\n\n")

        for i, kw in enumerate(opportunities, 1):
            f.write(f"## {i}. {kw['keyword']}\n\n")

            f.write(f"### Current Performance\n\n")
            f.write(f"- **Position:** {kw['position']}\n")
            f.write(f"- **Impressions (30d):** {kw['impressions']:,}\n")
            f.write(f"- **Clicks (30d):** {kw['clicks']}\n")
            f.write(f"- **CTR:** {kw['ctr'] * 100:.2f}%\n")
            f.write(f"- **Commercial Intent:** {kw['commercial_intent_category']} ({kw['commercial_intent']}/3.0)\n")
            if kw.get('search_intent'):
                f.write(f"- **Search Intent:** {kw['search_intent']} ({kw.get('intent_confidence', 0):.0f}% confidence)\n")
            f.write(f"\n### Enhanced Opportunity Analysis\n\n")
            f.write(f"- **Enhanced Score:** {kw.get('enhanced_score', kw['opportunity_score']):.2f}/100\n")
            f.write(f"- **Priority:** {kw.get('enhanced_priority', kw['priority']).upper()}\n")
            f.write(f"- **Key Factor:** {kw.get('primary_factor', 'volume')}\n\n")

            if kw.get('score_breakdown'):
                f.write(f"**Score Breakdown:**\n")
                breakdown = kw['score_breakdown']
                f.write(f"- Volume: {breakdown.get('volume_score', 0):.0f}/100\n")
                f.write(f"- Position: {breakdown.get('position_score', 0):.0f}/100\n")
                f.write(f"- Intent: {breakdown.get('intent_score', 0):.0f}/100\n")
                f.write(f"- Competition: {breakdown.get('competition_score', 0):.0f}/100\n")
                f.write(f"- CTR Opportunity: {breakdown.get('ctr_score', 0):.0f}/100\n")
                f.write(f"\n")

            if kw.get('traffic_potential'):
                tp = kw['traffic_potential']
                f.write(f"### Traffic Potential\n\n")
                f.write(f"- **Current:** {tp['current_clicks']} clicks/month at position {tp['current_position']:.1f}\n")
                f.write(f"- **Target:** Position {tp['target_position']} (page 1)\n")
                f.write(f"- **Potential:** {tp['potential_clicks']} clicks/month\n")
                f.write(f"- **Gain:** +{tp['additional_clicks']} clicks (+{tp['percent_increase']:.0f}%)\n\n")

            if kw.get('ranking_url'):
                f.write(f"### Ranking Page\n\n")
                f.write(f"- **URL:** {kw['ranking_url']}\n")
                if kw.get('dfs_position'):
                    f.write(f"- **DataForSEO Position:** {kw['dfs_position']}\n")
                if kw.get('search_volume'):
                    f.write(f"- **Search Volume:** {kw['search_volume']:,}/month\n")
                if kw.get('pageviews'):
                    f.write(f"- **Pageviews (30d):** {kw['pageviews']:,}\n")
                    f.write(f"- **Avg. Engagement:** {kw['engagement']:.0f}s\n")
                f.write("\n")

            f.write(f"### Recommendation\n\n")
            f.write(f"{kw['recommendation']}\n\n")

            f.write(f"### Action Items\n\n")
            f.write(f"- [ ] Analyze current content on ranking page\n")
            f.write(f"- [ ] Review top 5 ranking competitors for this keyword\n")
            f.write(f"- [ ] Identify content gaps to fill\n")
            f.write(f"- [ ] Optimize for keyword density and semantic relevance\n")
            f.write(f"- [ ] Improve internal linking to this page\n")
            f.write(f"- [ ] Update title tag and meta description\n")
            f.write(f"- [ ] Add/update visuals (images, videos, infographics)\n")
            f.write(f"- [ ] Refresh with current data and examples\n\n")

            f.write("---\n\n")

        # Summary section
        total_impressions = sum(k['impressions'] for k in opportunities)
        total_clicks = sum(k['clicks'] for k in opportunities)
        estimated_potential = int(total_impressions * 0.055)

        f.write(f"## Summary\n\n")
        f.write(f"**Total Opportunities:** {len(opportunities)}\n\n")
        f.write(f"**Combined Metrics:**\n")
        f.write(f"- Total Impressions: {total_impressions:,}\n")
        f.write(f"- Total Current Clicks: {total_clicks}\n")
        f.write(f"- Current CTR: {(total_clicks/total_impressions*100):.2f}%\n\n")
        f.write(f"**Potential Impact:**\n")
        f.write(f"- Target CTR (page 1): 5.5%\n")
        f.write(f"- Potential Total Clicks: {estimated_potential}\n")
        f.write(f"- Additional Clicks: +{estimated_potential - total_clicks}\n\n")

        f.write(f"## Next Steps\n\n")
        f.write(f"1. **Prioritize:** Start with top 3-5 keywords (highest opportunity score)\n")
        f.write(f"2. **Research:** Analyze top-ranking competitor content for each keyword\n")
        f.write(f"3. **Optimize:** Update existing content or create comprehensive new content\n")
        f.write(f"4. **Monitor:** Track position changes weekly\n")
        f.write(f"5. **Iterate:** Continue with next set of opportunities\n\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
