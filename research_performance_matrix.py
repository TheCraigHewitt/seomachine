#!/usr/bin/env python3
"""
Research Content Performance Matrix

Categorizes all content into performance quadrants:
- Stars: High traffic + High rankings (maintain and expand)
- Overperformers: High traffic + Low rankings (understand why)
- Underperformers: Low traffic + High rankings (CTR problem)
- Declining: Low traffic + Low rankings (refresh or redirect)
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.google_analytics import GoogleAnalytics


# Performance thresholds
TRAFFIC_THRESHOLD_HIGH = 500  # monthly pageviews
POSITION_THRESHOLD_GOOD = 15  # average position


def main():
    print("=" * 80)
    print("CONTENT PERFORMANCE MATRIX ANALYSIS")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Categorize content by traffic and rankings to prioritize actions")
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
        ga = GoogleAnalytics()
        print("   ✓ Google Analytics 4 connected")
    except Exception as e:
        print(f"   ✗ GA4 Error: {e}")
        print("   GA4 is required for performance matrix analysis")
        return

    # Get all pages from GA4
    print("\n2. Fetching page traffic data from GA4 (last 90 days)...")
    try:
        ga_pages = ga.get_top_pages(days=90, limit=500)
        print(f"   ✓ Found {len(ga_pages)} pages with traffic")
    except Exception as e:
        print(f"   ✗ Error fetching GA4 data: {e}")
        return

    # Filter to blog/content pages only
    content_pages = [p for p in ga_pages if is_content_page(p.get('path', ''))]
    print(f"   ✓ Filtered to {len(content_pages)} content pages")

    # Enrich with GSC data
    print("\n3. Enriching with Search Console ranking data...")
    performance_matrix = []

    for i, page in enumerate(content_pages):
        if (i + 1) % 50 == 0:
            print(f"   Progress: {i+1}/{len(content_pages)}...")

        path = page.get('path', '')

        try:
            # Get GSC performance for this page
            gsc_data = gsc.get_page_performance(path, days=90)

            if not gsc_data or 'avg_position' not in gsc_data:
                # Page exists in GA but not ranking in GSC
                avg_position = 100
                impressions = 0
                clicks = 0
                ctr = 0
            else:
                avg_position = gsc_data['avg_position']
                impressions = gsc_data.get('impressions', 0)
                clicks = gsc_data.get('clicks', 0)
                ctr = gsc_data.get('ctr', 0)

            # Get traffic trend
            try:
                trend = ga.get_page_trends(path, days=180)
                trend_direction = trend.get('trend_direction', 'stable')
                trend_percent = trend.get('trend_percent', 0)
            except:
                trend_direction = 'stable'
                trend_percent = 0

            # Normalize to monthly pageviews
            monthly_pageviews = int(page.get('pageviews', 0) * (30/90))

            # Categorize performance
            category, action, priority = categorize_page(
                monthly_pageviews,
                avg_position,
                trend_direction,
                trend_percent
            )

            performance_data = {
                'path': path,
                'title': page.get('title', path),
                'monthly_pageviews': monthly_pageviews,
                'pageviews_90d': page.get('pageviews', 0),
                'avg_position': round(avg_position, 1),
                'impressions': impressions,
                'clicks': clicks,
                'ctr': ctr,
                'trend_direction': trend_direction,
                'trend_percent': trend_percent,
                'category': category,
                'action': action,
                'priority': priority,
                'engagement_time': page.get('avg_engagement_time', 0),
                'bounce_rate': page.get('bounce_rate', 0)
            }

            performance_matrix.append(performance_data)

        except Exception as e:
            print(f"   Error processing {path}: {e}")
            continue

    print(f"   ✓ Performance matrix created for {len(performance_matrix)} pages")

    # Group by category
    stars = [p for p in performance_matrix if p['category'] == 'Star']
    overperformers = [p for p in performance_matrix if p['category'] == 'Overperformer']
    underperformers = [p for p in performance_matrix if p['category'] == 'Underperformer']
    declining = [p for p in performance_matrix if p['category'] == 'Declining']

    # Display summary
    print("\n" + "=" * 80)
    print("PERFORMANCE MATRIX SUMMARY")
    print("=" * 80)
    print(f"\n📊 Content Distribution:")
    print(f"   ⭐ Stars (High Traffic + High Rankings): {len(stars)}")
    print(f"   🚀 Overperformers (High Traffic + Low Rankings): {len(overperformers)}")
    print(f"   ⚠️  Underperformers (Low Traffic + High Rankings): {len(underperformers)}")
    print(f"   📉 Declining (Low Traffic + Low Rankings): {len(declining)}")

    print(f"\n🎯 Priority Actions:")
    critical = [p for p in performance_matrix if p['priority'] == 'CRITICAL']
    high = [p for p in performance_matrix if p['priority'] == 'HIGH']
    medium = [p for p in performance_matrix if p['priority'] == 'MEDIUM']
    print(f"   CRITICAL: {len(critical)}")
    print(f"   HIGH: {len(high)}")
    print(f"   MEDIUM: {len(medium)}")

    # Show top items from each category
    print(f"\n" + "=" * 80)
    print("TOP PRIORITIES BY CATEGORY")
    print("=" * 80)

    print(f"\n⭐ STARS - Top Performers (Maintain & Expand)")
    print("-" * 80)
    for p in sorted(stars, key=lambda x: x['monthly_pageviews'], reverse=True)[:5]:
        print(f"\n{p['title'][:60]}")
        print(f"   Traffic: {p['monthly_pageviews']:,}/mo | Position: {p['avg_position']}")
        print(f"   Trend: {p['trend_direction']} ({p['trend_percent']:+.1f}%)")
        print(f"   Action: {p['action']}")

    print(f"\n\n⚠️  UNDERPERFORMERS - Fix CTR Issues")
    print("-" * 80)
    for p in sorted(underperformers, key=lambda x: x['avg_position'])[:5]:
        expected_traffic = estimate_expected_traffic(p['avg_position'], p['impressions'])
        gap = expected_traffic - p['monthly_pageviews']
        print(f"\n{p['title'][:60]}")
        print(f"   Position: {p['avg_position']} | Traffic: {p['monthly_pageviews']:,}/mo (Expected: {expected_traffic:,})")
        print(f"   Missing: {gap:,} pageviews/mo")
        print(f"   Action: {p['action']}")

    print(f"\n\n📉 DECLINING - Needs Refresh")
    print("-" * 80)
    for p in sorted(declining, key=lambda x: x['trend_percent'])[:5]:
        print(f"\n{p['title'][:60]}")
        print(f"   Traffic: {p['monthly_pageviews']:,}/mo ({p['trend_percent']:+.1f}% trend)")
        print(f"   Position: {p['avg_position']}")
        print(f"   Action: {p['action']}")

    print(f"\n\n🚀 OVERPERFORMERS - Learn Why")
    print("-" * 80)
    for p in sorted(overperformers, key=lambda x: x['monthly_pageviews'], reverse=True)[:5]:
        print(f"\n{p['title'][:60]}")
        print(f"   Traffic: {p['monthly_pageviews']:,}/mo despite position {p['avg_position']}")
        print(f"   Action: {p['action']}")

    # Write report
    print(f"\n\n4. Writing report to research/performance-matrix-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(performance_matrix, stars, overperformers, underperformers, declining)

    print("\n" + "=" * 80)
    print("✅ PERFORMANCE MATRIX ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/performance-matrix-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Start with CRITICAL priority items")
    print(f"3. Fix underperformer titles/meta descriptions first (quick wins)")
    print(f"4. Refresh declining content or redirect")
    print(f"5. Expand star content with related topics")


def is_content_page(path: str) -> bool:
    """Determine if path is a content page (blog post/article)"""
    # Exclude non-content pages
    excluded_patterns = [
        '/tag/', '/category/', '/author/', '/search/', '/api/',
        '/login/', '/signup/', '/account/', '/dashboard/',
        '/checkout/', '/cart/', '/thank-you/', '/404/',
        '.xml', '.json', '.jpg', '.png', '.gif', '.pdf'
    ]

    for pattern in excluded_patterns:
        if pattern in path.lower():
            return False

    # Include pages that look like content
    # Typically blog posts have patterns like: /article-title/ or /blog/article-title/
    if path.count('/') >= 2 and len(path) > 10:
        return True

    return False


def categorize_page(
    monthly_pageviews: int,
    avg_position: float,
    trend_direction: str,
    trend_percent: float
) -> tuple:
    """
    Categorize page into performance quadrant.

    Returns:
        (category, action, priority)
    """

    high_traffic = monthly_pageviews >= TRAFFIC_THRESHOLD_HIGH
    good_rankings = avg_position <= POSITION_THRESHOLD_GOOD
    declining_trend = trend_direction == 'declining' and trend_percent < -20
    strong_growth = trend_direction == 'rising' and trend_percent > 30

    # Stars: High traffic + Good rankings
    if high_traffic and good_rankings:
        if declining_trend:
            return ('Star', 'Monitor closely - declining star, investigate cause', 'CRITICAL')
        elif strong_growth:
            return ('Star', 'Riding high - expand with related content', 'HIGH')
        else:
            return ('Star', 'Maintain excellence - keep content fresh and updated', 'MEDIUM')

    # Overperformers: High traffic despite poor rankings
    elif high_traffic and not good_rankings:
        return ('Overperformer', 'Analyze traffic sources - strong referral/social? Improve SEO to capture organic too', 'HIGH')

    # Underperformers: Good rankings but low traffic
    elif not high_traffic and good_rankings:
        if declining_trend:
            return ('Underperformer', 'URGENT: Rankings dropping AND low CTR - major title/meta refresh needed', 'CRITICAL')
        else:
            return ('Underperformer', 'CTR problem - rewrite title and meta description for better click-through', 'HIGH')

    # Declining: Low traffic + Poor rankings
    else:
        if monthly_pageviews < 100 and avg_position > 50:
            return ('Declining', 'Consider 301 redirect to related content or complete rewrite', 'MEDIUM')
        elif declining_trend:
            return ('Declining', 'Major content refresh needed - update stats, examples, add depth', 'HIGH')
        else:
            return ('Declining', 'Needs significant optimization or consolidation with better content', 'MEDIUM')


def estimate_expected_traffic(avg_position: float, impressions: int) -> int:
    """Estimate expected monthly traffic based on position and impressions"""
    # Expected CTR by position
    position_ctr = {
        range(1, 2): 0.316,
        range(2, 3): 0.157,
        range(3, 4): 0.105,
        range(4, 6): 0.067,
        range(6, 11): 0.040,
        range(11, 16): 0.015,
        range(16, 21): 0.010,
    }

    pos_int = int(round(avg_position))
    expected_ctr = 0.005  # Default

    for pos_range, ctr in position_ctr.items():
        if pos_int in pos_range:
            expected_ctr = ctr
            break

    # Convert 90-day impressions to monthly
    monthly_impressions = impressions * (30/90)

    return int(monthly_impressions * expected_ctr)


def write_markdown_report(
    all_pages: List[Dict],
    stars: List[Dict],
    overperformers: List[Dict],
    underperformers: List[Dict],
    declining: List[Dict]
):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/performance-matrix-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Content Performance Matrix\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Strategy:** Categorize content by traffic and rankings to prioritize optimization efforts\n\n")
        f.write(f"**Total Pages Analyzed:** {len(all_pages)}\n\n")
        f.write("---\n\n")

        # Summary
        f.write(f"## Performance Distribution\n\n")
        f.write(f"| Category | Count | Description |\n")
        f.write(f"|----------|-------|-------------|\n")
        f.write(f"| ⭐ Stars | {len(stars)} | High traffic + High rankings |\n")
        f.write(f"| 🚀 Overperformers | {len(overperformers)} | High traffic + Low rankings |\n")
        f.write(f"| ⚠️ Underperformers | {len(underperformers)} | Low traffic + High rankings |\n")
        f.write(f"| 📉 Declining | {len(declining)} | Low traffic + Low rankings |\n\n")

        # Stars
        f.write(f"## ⭐ STARS ({len(stars)} pages)\n\n")
        f.write(f"**Strategy:** Maintain excellence and expand with related content\n\n")

        for i, page in enumerate(sorted(stars, key=lambda x: x['monthly_pageviews'], reverse=True)[:20], 1):
            f.write(f"### {i}. {page['title']}\n\n")
            f.write(f"- **URL:** {page['path']}\n")
            f.write(f"- **Monthly Traffic:** {page['monthly_pageviews']:,} pageviews\n")
            f.write(f"- **Average Position:** {page['avg_position']}\n")
            f.write(f"- **Trend:** {page['trend_direction']} ({page['trend_percent']:+.1f}%)\n")
            f.write(f"- **Priority:** {page['priority']}\n\n")
            f.write(f"**Action:** {page['action']}\n\n")
            f.write(f"**Specific Steps:**\n")
            f.write(f"- Keep content updated with latest information\n")
            f.write(f"- Add new sections addressing related questions\n")
            f.write(f"- Create supporting cluster content linking to this page\n")
            f.write(f"- Monitor for ranking changes weekly\n\n")
            f.write("---\n\n")

        # Underperformers
        f.write(f"## ⚠️ UNDERPERFORMERS ({len(underperformers)} pages)\n\n")
        f.write(f"**Strategy:** Fix CTR issues - rewrite titles and meta descriptions\n\n")

        for i, page in enumerate(sorted(underperformers, key=lambda x: x['avg_position'])[:20], 1):
            expected = estimate_expected_traffic(page['avg_position'], page['impressions'])
            gap = expected - page['monthly_pageviews']

            f.write(f"### {i}. {page['title']}\n\n")
            f.write(f"- **URL:** {page['path']}\n")
            f.write(f"- **Average Position:** {page['avg_position']} (GOOD!)\n")
            f.write(f"- **Monthly Traffic:** {page['monthly_pageviews']:,} pageviews\n")
            f.write(f"- **Expected Traffic:** {expected:,} pageviews\n")
            f.write(f"- **Traffic Gap:** {gap:,} pageviews/month missing\n")
            f.write(f"- **Current CTR:** {page['ctr']*100:.2f}%\n")
            f.write(f"- **Priority:** {page['priority']}\n\n")
            f.write(f"**Action:** {page['action']}\n\n")
            f.write(f"**Specific Steps:**\n")
            f.write(f"1. Rewrite title tag to be more compelling\n")
            f.write(f"2. Add year/numbers/power words to title\n")
            f.write(f"3. Rewrite meta description with clear value proposition\n")
            f.write(f"4. Add FAQ schema if relevant\n")
            f.write(f"5. Test different title variations\n\n")
            f.write("---\n\n")

        # Declining
        f.write(f"## 📉 DECLINING ({len(declining)} pages)\n\n")
        f.write(f"**Strategy:** Major refresh or strategic redirect\n\n")

        for i, page in enumerate(sorted(declining, key=lambda x: x['trend_percent'])[:20], 1):
            f.write(f"### {i}. {page['title']}\n\n")
            f.write(f"- **URL:** {page['path']}\n")
            f.write(f"- **Monthly Traffic:** {page['monthly_pageviews']:,} pageviews\n")
            f.write(f"- **Average Position:** {page['avg_position']}\n")
            f.write(f"- **Trend:** {page['trend_direction']} ({page['trend_percent']:+.1f}%)\n")
            f.write(f"- **Priority:** {page['priority']}\n\n")
            f.write(f"**Action:** {page['action']}\n\n")
            f.write(f"**Specific Steps:**\n")

            if page['monthly_pageviews'] < 50:
                f.write(f"- Consider 301 redirect to related high-performing content\n")
                f.write(f"- OR complete rewrite if topic is still valuable\n")
            else:
                f.write(f"- Update all statistics and examples to current year\n")
                f.write(f"- Add 500+ words of new content\n")
                f.write(f"- Refresh images and add new visuals\n")
                f.write(f"- Improve keyword targeting\n")
                f.write(f"- Strengthen internal linking\n")

            f.write("\n---\n\n")

        # Overperformers
        f.write(f"## 🚀 OVERPERFORMERS ({len(overperformers)} pages)\n\n")
        f.write(f"**Strategy:** Analyze why and improve SEO to capture more organic traffic\n\n")

        for i, page in enumerate(sorted(overperformers, key=lambda x: x['monthly_pageviews'], reverse=True)[:20], 1):
            f.write(f"### {i}. {page['title']}\n\n")
            f.write(f"- **URL:** {page['path']}\n")
            f.write(f"- **Monthly Traffic:** {page['monthly_pageviews']:,} pageviews (HIGH!)\n")
            f.write(f"- **Average Position:** {page['avg_position']} (Could be better)\n")
            f.write(f"- **Impressions:** {page['impressions']:,}\n")
            f.write(f"- **Priority:** {page['priority']}\n\n")
            f.write(f"**Action:** {page['action']}\n\n")
            f.write(f"**Investigation Needed:**\n")
            f.write(f"- Check Google Analytics for traffic sources (likely referral/social)\n")
            f.write(f"- Analyze which external sites link to this page\n")
            f.write(f"- Improve SEO to also capture organic search traffic\n")
            f.write(f"- Optimize for keywords it's almost ranking for\n\n")
            f.write("---\n\n")

        # Summary stats
        f.write(f"## Key Metrics\n\n")
        total_traffic = sum(p['monthly_pageviews'] for p in all_pages)
        star_traffic = sum(p['monthly_pageviews'] for p in stars)
        star_percent = (star_traffic / total_traffic * 100) if total_traffic > 0 else 0

        f.write(f"- **Total Monthly Traffic:** {total_traffic:,} pageviews\n")
        f.write(f"- **Star Content Traffic:** {star_traffic:,} ({star_percent:.1f}% of total)\n")
        f.write(f"- **Pages Needing Attention:** {len(underperformers) + len(declining)}\n\n")

        f.write(f"## Recommended Workflow\n\n")
        f.write(f"### Week 1: Fix Underperformers\n")
        f.write(f"Focus on rewriting titles and meta descriptions for underperformers. Quick wins!\n\n")

        critical_under = [p for p in underperformers if p['priority'] == 'CRITICAL'][:5]
        for p in critical_under:
            f.write(f"- {p['title'][:60]} (Position {p['avg_position']}, missing {estimate_expected_traffic(p['avg_position'], p['impressions']) - p['monthly_pageviews']:,} clicks)\n")

        f.write(f"\n### Week 2-3: Refresh Declining Content\n")
        f.write(f"Update declining content with fresh information and examples.\n\n")

        high_decline = [p for p in declining if p['priority'] == 'HIGH'][:5]
        for p in high_decline:
            f.write(f"- {p['title'][:60]} ({p['trend_percent']:+.1f}% trend)\n")

        f.write(f"\n### Week 4+: Expand Stars\n")
        f.write(f"Create related content clustering around your top performers.\n\n")

        top_stars = sorted(stars, key=lambda x: x['monthly_pageviews'], reverse=True)[:3]
        for p in top_stars:
            f.write(f"- Build cluster around: {p['title'][:60]}\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
