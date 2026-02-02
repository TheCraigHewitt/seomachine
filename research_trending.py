#!/usr/bin/env python3
"""
Research Trending Opportunities

Identifies topics gaining search interest NOW using GSC trend data.
These are time-sensitive opportunities - strike while the trend is hot!
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.dataforseo import DataForSEO
from modules.search_intent_analyzer import SearchIntentAnalyzer


def main():
    print("=" * 80)
    print("TRENDING TOPIC OPPORTUNITIES")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Identify rising search trends for time-sensitive content")
    print("=" * 80)

    # Initialize
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
        has_dfs = True
    except Exception as e:
        print(f"   ⚠ DataForSEO not available: {e}")
        has_dfs = False

    intent_analyzer = SearchIntentAnalyzer()

    # Get trending queries from GSC
    print("\n2. Identifying trending queries...")
    try:
        trending_queries = gsc.get_trending_queries(
            days_recent=7,          # Last week
            days_comparison=30,     # vs previous 30 days
            min_impressions=20      # At least 20 impressions to avoid noise
        )

        if not trending_queries:
            print("   No trending queries found")
            return

        print(f"   ✓ Found {len(trending_queries)} trending queries")

    except Exception as e:
        print(f"   ✗ Error identifying trends: {e}")
        return

    # Enrich with additional data
    print(f"\n3. Enriching trend data...")
    enriched_trends = []

    for i, trend in enumerate(trending_queries[:30], 1):  # Top 30
        if i % 10 == 0:
            print(f"   Progress: {i}/30...")

        query = trend['query']

        # Get additional data from DataForSEO
        search_volume = None
        difficulty = None
        cpc = None

        if has_dfs:
            try:
                # Get keyword metrics
                keyword_data = dfs.get_keyword_ideas(query, limit=1)
                if keyword_data and len(keyword_data) > 0:
                    search_volume = keyword_data[0].get('search_volume')
                    difficulty = keyword_data[0].get('difficulty')
                    cpc = keyword_data[0].get('cpc')
            except:
                pass

        # Analyze intent
        try:
            intent_result = intent_analyzer.analyze(keyword=query)
            primary_intent = intent_result.get('primary_intent', 'unknown')
            if hasattr(primary_intent, 'value'):
                primary_intent = primary_intent.value
            search_intent = str(primary_intent)
        except:
            search_intent = 'unknown'

        # Calculate opportunity score
        opportunity_score = calculate_trend_opportunity_score(
            growth_percent=trend['growth_percent'],
            recent_impressions=trend['recent_impressions'],
            current_position=trend['position'],
            search_volume=search_volume
        )

        enriched_trend = {
            **trend,
            'search_volume': search_volume,
            'difficulty': difficulty,
            'cpc': cpc,
            'search_intent': search_intent,
            'opportunity_score': opportunity_score,
            'priority': determine_trend_priority(opportunity_score, trend['growth_percent']),
            'urgency': calculate_urgency(trend['growth_percent'])
        }

        enriched_trends.append(enriched_trend)

    # Sort by opportunity score
    enriched_trends.sort(key=lambda x: x['opportunity_score'], reverse=True)

    # Display summary
    print("\n" + "=" * 80)
    print("TOP 10 TRENDING OPPORTUNITIES")
    print("=" * 80)

    for i, trend in enumerate(enriched_trends[:10], 1):
        print(f"\n#{i} QUERY: {trend['query']}")
        print("-" * 80)
        print(f"Growth: +{trend['growth_percent']:.0f}% ({trend['comparison_impressions']} → {trend['recent_impressions']})")
        print(f"Your Position: {trend['position']:.1f}")

        if trend['search_volume']:
            print(f"Search Volume: {trend['search_volume']:,}/month")

        print(f"Search Intent: {trend['search_intent']}")
        print(f"Opportunity Score: {trend['opportunity_score']:.2f}/100")
        print(f"Priority: {trend['priority']}")
        print(f"Urgency: {trend['urgency']}")

    # Write report
    print(f"\n\n4. Writing report to research/trending-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(enriched_trends)

    print("\n" + "=" * 80)
    print("✅ TRENDING ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/trending-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Act quickly on CRITICAL urgency trends (within 1 week)")
    print(f"3. Create time-sensitive content for top trends")
    print(f"4. Monitor trend continuation over next few weeks")


def calculate_trend_opportunity_score(
    growth_percent: float,
    recent_impressions: int,
    current_position: float,
    search_volume: int = None
) -> float:
    """Calculate opportunity score for trending topic (0-100)"""

    # Growth score (40% weight)
    if growth_percent >= 200:
        growth_score = 100
    elif growth_percent >= 100:
        growth_score = 85
    elif growth_percent >= 50:
        growth_score = 70
    elif growth_percent >= 25:
        growth_score = 50
    else:
        growth_score = 30

    # Volume score (30% weight)
    volume = search_volume if search_volume else recent_impressions
    if volume >= 5000:
        volume_score = 100
    elif volume >= 2000:
        volume_score = 85
    elif volume >= 1000:
        volume_score = 70
    elif volume >= 500:
        volume_score = 55
    elif volume >= 100:
        volume_score = 40
    else:
        volume_score = 20

    # Position advantage (30% weight)
    # If you already have some visibility, easier to capitalize
    if current_position <= 20:
        position_score = 100  # Already visible
    elif current_position <= 50:
        position_score = 70   # Some visibility
    elif current_position <= 100:
        position_score = 40   # Minimal visibility
    else:
        position_score = 20   # Not visible

    # Weighted total
    final_score = (
        growth_score * 0.40 +
        volume_score * 0.30 +
        position_score * 0.30
    )

    return round(final_score, 2)


def determine_trend_priority(opportunity_score: float, growth_percent: float) -> str:
    """Determine priority level"""
    if opportunity_score >= 80 or growth_percent >= 150:
        return 'CRITICAL'
    elif opportunity_score >= 65:
        return 'HIGH'
    elif opportunity_score >= 45:
        return 'MEDIUM'
    else:
        return 'LOW'


def calculate_urgency(growth_percent: float) -> str:
    """Calculate how urgently to act on this trend"""
    if growth_percent >= 150:
        return 'CRITICAL - Act within 1 week'
    elif growth_percent >= 75:
        return 'HIGH - Act within 2 weeks'
    elif growth_percent >= 30:
        return 'MODERATE - Act within 1 month'
    else:
        return 'LOW - Monitor trend'


def write_markdown_report(trends: List[Dict]):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/trending-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Trending Topic Opportunities\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Strategy:** Capitalize on rising search trends with time-sensitive content\n\n")
        f.write(f"**Trends Identified:** {len(trends)}\n\n")
        f.write(f"⏰ **TIME-SENSITIVE:** These trends are hot NOW. Act quickly before they cool or competition increases.\n\n")
        f.write("---\n\n")

        # Group by urgency
        critical = [t for t in trends if 'CRITICAL' in t['urgency']]
        high = [t for t in trends if 'HIGH' in t['urgency']]
        moderate = [t for t in trends if 'MODERATE' in t['urgency']]

        f.write(f"## Urgency Distribution\n\n")
        f.write(f"- 🔥 CRITICAL (Act within 1 week): {len(critical)}\n")
        f.write(f"- ⚡ HIGH (Act within 2 weeks): {len(high)}\n")
        f.write(f"- ⏳ MODERATE (Act within 1 month): {len(moderate)}\n\n")
        f.write("---\n\n")

        # Critical urgency trends
        if critical:
            f.write(f"## 🔥 CRITICAL URGENCY TRENDS\n\n")
            f.write(f"**These topics are exploding NOW. Create content immediately!**\n\n")

            for i, trend in enumerate(critical[:10], 1):
                f.write(f"### {i}. {trend['query']}\n\n")
                f.write(f"- **Growth:** +{trend['growth_percent']:.0f}% ({trend['comparison_impressions']} → {trend['recent_impressions']} impressions)\n")
                f.write(f"- **Your Position:** {trend['position']:.1f}\n")

                if trend.get('search_volume'):
                    f.write(f"- **Search Volume:** {trend['search_volume']:,}/month\n")

                if trend.get('difficulty'):
                    f.write(f"- **SEO Difficulty:** {trend['difficulty']}/100\n")

                f.write(f"- **Search Intent:** {trend['search_intent']}\n")
                f.write(f"- **Opportunity Score:** {trend['opportunity_score']:.2f}/100\n")
                f.write(f"- **Urgency:** {trend['urgency']}\n\n")

                f.write(f"**Why It's Hot:**\n")
                if trend['growth_percent'] >= 200:
                    f.write(f"- Massive growth spike (3x+ increase)\n")
                elif trend['growth_percent'] >= 100:
                    f.write(f"- Strong growth (2x+ increase)\n")

                if trend['position'] <= 20:
                    f.write(f"- You already have visibility (position {trend['position']:.0f})\n")
                    f.write(f"- Small optimization could drive significant traffic\n")

                if trend['recent_impressions'] > 500:
                    f.write(f"- High immediate demand ({trend['recent_impressions']} impressions last week)\n")

                f.write(f"\n**Recommended Action:**\n")

                if trend['position'] <= 30:
                    f.write(f"1. Update existing ranking content immediately\n")
                    f.write(f"2. Add trending angle/section\n")
                    f.write(f"3. Update title to include current year\n")
                    f.write(f"4. Optimize for this trending query\n")
                else:
                    f.write(f"1. Create comprehensive content targeting this query\n")
                    f.write(f"2. Publish within 3-5 days (trend is hot!)\n")
                    f.write(f"3. Promote on social media immediately\n")
                    f.write(f"4. Consider paid promotion to accelerate visibility\n")

                f.write(f"\n**Timeline:** Complete within 7 days\n\n")
                f.write("---\n\n")

        # High urgency trends
        if high:
            f.write(f"## ⚡ HIGH URGENCY TRENDS\n\n")
            f.write(f"**Strong upward trends. Act within 2 weeks.**\n\n")

            for i, trend in enumerate(high[:10], 1):
                f.write(f"### {i}. {trend['query']}\n\n")
                f.write(f"- Growth: +{trend['growth_percent']:.0f}%\n")
                f.write(f"- Position: {trend['position']:.1f}\n")

                if trend.get('search_volume'):
                    f.write(f"- Volume: {trend['search_volume']:,}/month\n")

                f.write(f"- Opportunity Score: {trend['opportunity_score']:.2f}/100\n")
                f.write(f"- Urgency: {trend['urgency']}\n\n")

                f.write(f"**Action:** ")
                if trend['position'] <= 30:
                    f.write(f"Update existing content within 2 weeks\n")
                else:
                    f.write(f"Create new comprehensive content within 2 weeks\n")

                f.write(f"\n---\n\n")

        # Moderate urgency trends
        if moderate:
            f.write(f"## ⏳ MODERATE URGENCY TRENDS\n\n")
            f.write(f"**Steady growth. Monitor and act within 1 month.**\n\n")

            for i, trend in enumerate(moderate[:15], 1):
                f.write(f"### {i}. {trend['query']}\n")
                f.write(f"- Growth: +{trend['growth_percent']:.0f}%\n")
                f.write(f"- Position: {trend['position']:.1f}\n")

                if trend.get('search_volume'):
                    f.write(f"- Volume: {trend['search_volume']:,}/month\n")

                f.write(f"- Score: {trend['opportunity_score']:.2f}/100\n\n")

        # Strategy recommendations
        f.write(f"## Implementation Strategy\n\n")

        f.write(f"### Week 1: Critical Trends\n")
        f.write(f"Focus all resources on critical urgency trends:\n\n")

        for i, trend in enumerate(critical[:3], 1):
            f.write(f"{i}. **{trend['query']}** - +{trend['growth_percent']:.0f}% growth\n")
            if trend['position'] <= 30:
                f.write(f"   - Quick win: Update existing content (position {trend['position']:.0f})\n")
            else:
                f.write(f"   - New content needed: 2000+ word comprehensive guide\n")
            f.write(f"\n")

        f.write(f"### Week 2-3: High Urgency Trends\n")
        f.write(f"Build on critical work with high urgency items:\n\n")

        for i, trend in enumerate(high[:3], 1):
            f.write(f"{i}. **{trend['query']}**\n")

        f.write(f"\n### Week 4: Monitor & Moderate Trends\n")
        f.write(f"- Review if critical trends maintained momentum\n")
        f.write(f"- Begin work on moderate urgency items\n")
        f.write(f"- Track which trends are continuing vs fading\n\n")

        # Insights
        f.write(f"## Key Insights\n\n")

        avg_growth = sum(t['growth_percent'] for t in trends) / len(trends) if trends else 0
        highest_growth = max(trends, key=lambda x: x['growth_percent']) if trends else None

        f.write(f"- **Average Growth:** +{avg_growth:.0f}%\n")

        if highest_growth:
            f.write(f"- **Hottest Trend:** {highest_growth['query']} (+{highest_growth['growth_percent']:.0f}%)\n")

        already_ranking = [t for t in trends if t['position'] <= 30]
        f.write(f"- **Already Ranking (Position ≤30):** {len(already_ranking)} trends\n")
        f.write(f"- **Quick Win Potential:** {len([t for t in already_ranking if t['priority'] in ['CRITICAL', 'HIGH']])} high-priority items where you already rank\n\n")

        f.write(f"## Trend Monitoring\n\n")
        f.write(f"- **Run this analysis weekly** to catch new trends early\n")
        f.write(f"- **Track trend continuation** - Some spikes are temporary, others sustain\n")
        f.write(f"- **Monitor your position changes** for trending queries you target\n")
        f.write(f"- **Analyze traffic impact** 2-4 weeks after publishing trend content\n\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
