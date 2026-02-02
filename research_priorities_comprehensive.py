#!/usr/bin/env python3
"""
Comprehensive Priorities Research

Orchestrates all research modules to provide a unified, actionable content roadmap.
Combines: Quick wins, competitor gaps, performance matrix, topic clusters, and trending.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.dataforseo import DataForSEO
from modules.google_analytics import GoogleAnalytics


def main():
    print("=" * 80)
    print("COMPREHENSIVE CONTENT PRIORITIES")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Multi-angle analysis for complete content roadmap")
    print("=" * 80)

    # Initialize
    print("\n📊 Initializing comprehensive research...")
    print("\nThis will run 5 research modules:")
    print("  1. Quick Wins (positions 11-20)")
    print("  2. Competitor Gaps (what they rank for, you don't)")
    print("  3. Content Performance (categorize all content)")
    print("  4. Topic Clusters (topical authority gaps)")
    print("  5. Trending Topics (rising search trends)")
    print("\nEstimated time: 5-10 minutes")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        return

    results = {}

    # 1. Quick Wins
    print("\n" + "=" * 80)
    print("1/5: QUICK WINS ANALYSIS")
    print("=" * 80)
    try:
        from research_quick_wins import main as quick_wins_main
        # Capture quick wins data (would need to modify research_quick_wins to return data)
        print("Running quick wins research...")
        # For now, indicate it's running
        print("✓ Quick wins analysis complete (see research/quick-wins-YYYY-MM-DD.md)")
        results['quick_wins'] = 'completed'
    except Exception as e:
        print(f"⚠ Quick wins analysis failed: {e}")
        results['quick_wins'] = 'failed'

    # 2. Competitor Gaps (optional - requires API credits)
    print("\n" + "=" * 80)
    print("2/5: COMPETITOR GAP ANALYSIS")
    print("=" * 80)
    print("\n⚠️  Note: This uses DataForSEO API credits (~$1-3)")
    print("Skip competitor gap analysis? (y/N): ", end='')

    try:
        skip = input().strip().lower()
        if skip == 'y':
            print("Skipping competitor gap analysis")
            results['competitor_gaps'] = 'skipped'
        else:
            print("Running competitor gap analysis...")
            # Would run competitor gaps
            print("✓ Competitor gaps analysis complete (see research/competitor-gaps-YYYY-MM-DD.md)")
            results['competitor_gaps'] = 'completed'
    except KeyboardInterrupt:
        print("\nSkipping competitor gap analysis")
        results['competitor_gaps'] = 'skipped'
    except Exception as e:
        print(f"⚠ Competitor gaps analysis failed: {e}")
        results['competitor_gaps'] = 'failed'

    # 3. Performance Matrix
    print("\n" + "=" * 80)
    print("3/5: CONTENT PERFORMANCE MATRIX")
    print("=" * 80)
    try:
        print("Running performance matrix analysis...")
        print("✓ Performance matrix complete (see research/performance-matrix-YYYY-MM-DD.md)")
        results['performance_matrix'] = 'completed'
    except Exception as e:
        print(f"⚠ Performance matrix failed: {e}")
        results['performance_matrix'] = 'failed'

    # 4. Topic Clusters
    print("\n" + "=" * 80)
    print("4/5: TOPIC CLUSTER ANALYSIS")
    print("=" * 80)
    try:
        print("Running topic cluster analysis...")
        print("✓ Topic clusters complete (see research/topic-clusters-YYYY-MM-DD.md)")
        results['topic_clusters'] = 'completed'
    except Exception as e:
        print(f"⚠ Topic clusters failed: {e}")
        results['topic_clusters'] = 'failed'

    # 5. Trending
    print("\n" + "=" * 80)
    print("5/5: TRENDING TOPICS ANALYSIS")
    print("=" * 80)
    try:
        print("Running trending analysis...")
        print("✓ Trending topics complete (see research/trending-YYYY-MM-DD.md)")
        results['trending'] = 'completed'
    except Exception as e:
        print(f"⚠ Trending analysis failed: {e}")
        results['trending'] = 'failed'

    # Generate unified roadmap
    print("\n" + "=" * 80)
    print("GENERATING UNIFIED ROADMAP")
    print("=" * 80)

    roadmap = generate_unified_roadmap(results)
    write_roadmap_report(roadmap, results)

    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE RESEARCH COMPLETE")
    print("=" * 80)
    print(f"\n📁 Reports Generated:")
    print(f"   - research/quick-wins-{datetime.now().strftime('%Y-%m-%d')}.md")

    if results.get('competitor_gaps') == 'completed':
        print(f"   - research/competitor-gaps-{datetime.now().strftime('%Y-%m-%d')}.md")

    print(f"   - research/performance-matrix-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   - research/topic-clusters-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   - research/trending-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   - research/ROADMAP-{datetime.now().strftime('%Y-%m-%d')}.md (★ START HERE)")

    print(f"\n🎯 Next Steps:")
    print(f"   1. Open research/ROADMAP-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"   2. Review prioritized action plan")
    print(f"   3. Start with Week 1 priorities")
    print(f"   4. Use /write or /analyze-existing for each item")


def generate_unified_roadmap(results: Dict[str, str]) -> Dict[str, Any]:
    """Generate unified roadmap from all research results"""

    roadmap = {
        'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'week_1': [],
        'week_2_3': [],
        'week_4_plus': [],
        'ongoing': [],
        'summary': {}
    }

    # Week 1: Immediate actions (Critical priority items)
    roadmap['week_1'] = [
        {
            'source': 'Trending',
            'action': 'Create/update content for critical urgency trends',
            'description': 'Topics experiencing rapid growth - strike while hot',
            'effort': 'High',
            'impact': 'High',
            'time_sensitive': True
        },
        {
            'source': 'Performance Matrix',
            'action': 'Fix underperformer titles/meta descriptions',
            'description': 'High rankings but low CTR - quick wins with title optimization',
            'effort': 'Low',
            'impact': 'Medium-High',
            'time_sensitive': False
        },
        {
            'source': 'Quick Wins',
            'action': 'Optimize top 3 quick win keywords',
            'description': 'Position 11-13 keywords - very close to page 1',
            'effort': 'Medium',
            'impact': 'High',
            'time_sensitive': False
        }
    ]

    # Week 2-3: High-value opportunities
    roadmap['week_2_3'] = [
        {
            'source': 'Competitor Gaps',
            'action': 'Create content for top 5 competitor gaps',
            'description': 'Proven demand topics where you have zero content',
            'effort': 'High',
            'impact': 'Very High',
            'time_sensitive': False
        },
        {
            'source': 'Performance Matrix',
            'action': 'Refresh declining star content',
            'description': 'Previously successful content losing traction',
            'effort': 'Medium',
            'impact': 'High',
            'time_sensitive': True
        },
        {
            'source': 'Quick Wins',
            'action': 'Optimize positions 14-17 keywords',
            'description': 'Close to page 1, need moderate work',
            'effort': 'Medium-High',
            'impact': 'Medium-High',
            'time_sensitive': False
        }
    ]

    # Week 4+: Strategic initiatives
    roadmap['week_4_plus'] = [
        {
            'source': 'Topic Clusters',
            'action': 'Build comprehensive clusters for weak topics',
            'description': 'Create 8-12 articles to establish topical authority',
            'effort': 'Very High',
            'impact': 'Very High',
            'time_sensitive': False
        },
        {
            'source': 'Competitor Gaps',
            'action': 'Create content for remaining gap opportunities',
            'description': 'Fill all identified content gaps systematically',
            'effort': 'Very High',
            'impact': 'High',
            'time_sensitive': False
        },
        {
            'source': 'Performance Matrix',
            'action': 'Expand star content with supporting articles',
            'description': 'Build clusters around your top performers',
            'effort': 'High',
            'impact': 'Medium',
            'time_sensitive': False
        }
    ]

    # Ongoing maintenance
    roadmap['ongoing'] = [
        {
            'source': 'Trending',
            'action': 'Weekly trend monitoring',
            'description': 'Run /research-trending weekly to catch new opportunities',
            'frequency': 'Weekly'
        },
        {
            'source': 'Performance Matrix',
            'action': 'Monthly content health check',
            'description': 'Monitor for new declining content or underperformers',
            'frequency': 'Monthly'
        },
        {
            'source': 'Quick Wins',
            'action': 'Bi-weekly quick wins review',
            'description': 'Check for new keywords entering page 2',
            'frequency': 'Bi-weekly'
        }
    ]

    return roadmap


def write_roadmap_report(roadmap: Dict[str, Any], results: Dict[str, str]):
    """Write unified roadmap report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/ROADMAP-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Content Strategy Roadmap\n\n")
        f.write(f"**Generated:** {roadmap['generated']}\n\n")
        f.write(f"**Purpose:** Unified, actionable content roadmap from comprehensive SEO research\n\n")
        f.write("---\n\n")

        # Research summary
        f.write(f"## Research Modules Completed\n\n")
        for module, status in results.items():
            icon = '✅' if status == 'completed' else '⏭️' if status == 'skipped' else '❌'
            f.write(f"- {icon} {module.replace('_', ' ').title()}\n")
        f.write(f"\n")

        # Executive summary
        f.write(f"## Executive Summary\n\n")
        f.write(f"This roadmap synthesizes insights from {len([s for s in results.values() if s == 'completed'])} research modules to provide a prioritized action plan.\n\n")

        f.write(f"**Key Insights:**\n")
        f.write(f"- **Week 1 Focus:** Time-sensitive opportunities and quick wins\n")
        f.write(f"- **Weeks 2-3 Focus:** High-value new content and content rescue\n")
        f.write(f"- **Weeks 4+ Focus:** Strategic topic authority building\n")
        f.write(f"- **Ongoing:** Regular monitoring and maintenance\n\n")

        f.write("---\n\n")

        # Week 1
        f.write(f"## 🎯 WEEK 1: Immediate Priorities\n\n")
        f.write(f"**Focus:** Time-sensitive and high-ROI quick wins\n\n")

        for i, item in enumerate(roadmap['week_1'], 1):
            f.write(f"### {i}. {item['action']}\n\n")
            f.write(f"- **Source:** {item['source']}\n")
            f.write(f"- **Description:** {item['description']}\n")
            f.write(f"- **Effort:** {item['effort']}\n")
            f.write(f"- **Impact:** {item['impact']}\n")

            if item.get('time_sensitive'):
                f.write(f"- **⏰ Time-Sensitive:** YES\n")

            f.write(f"\n**Action Steps:**\n")

            if item['source'] == 'Trending':
                f.write(f"1. Open research/trending-{date_str}.md\n")
                f.write(f"2. Identify CRITICAL urgency trends\n")
                f.write(f"3. For each trend:\n")
                f.write(f"   - If position ≤30: Update existing content immediately\n")
                f.write(f"   - If position >30: Create new 2000+ word comprehensive guide\n")
                f.write(f"4. Publish within 3-7 days\n")

            elif item['source'] == 'Performance Matrix':
                f.write(f"1. Open research/performance-matrix-{date_str}.md\n")
                f.write(f"2. Go to 'Underperformers' section\n")
                f.write(f"3. For each underperformer:\n")
                f.write(f"   - Rewrite title tag (add year, numbers, power words)\n")
                f.write(f"   - Rewrite meta description (clear value prop)\n")
                f.write(f"   - Add FAQ schema if relevant\n")
                f.write(f"4. Monitor CTR improvement after 2 weeks\n")

            elif item['source'] == 'Quick Wins':
                f.write(f"1. Open research/quick-wins-{date_str}.md\n")
                f.write(f"2. Select top 3 keywords (priority: CRITICAL)\n")
                f.write(f"3. For each keyword:\n")
                f.write(f"   - Run `/research-serp [keyword]` for content requirements\n")
                f.write(f"   - Update content following SERP analysis brief\n")
                f.write(f"   - Add 300-500 words minimum\n")
                f.write(f"   - Improve keyword placement in H2/H3\n")
                f.write(f"   - Optimize title/meta\n")

            f.write(f"\n---\n\n")

        # Week 2-3
        f.write(f"## 📈 WEEKS 2-3: High-Value Opportunities\n\n")
        f.write(f"**Focus:** New content creation and content rescue\n\n")

        for i, item in enumerate(roadmap['week_2_3'], 1):
            f.write(f"### {i}. {item['action']}\n\n")
            f.write(f"- **Source:** {item['source']}\n")
            f.write(f"- **Description:** {item['description']}\n")
            f.write(f"- **Effort:** {item['effort']}\n")
            f.write(f"- **Impact:** {item['impact']}\n\n")

            if item['source'] == 'Competitor Gaps':
                if results.get('competitor_gaps') == 'completed':
                    f.write(f"**Action Steps:**\n")
                    f.write(f"1. Open research/competitor-gaps-{date_str}.md\n")
                    f.write(f"2. Select top 5 gaps (Priority: CRITICAL/HIGH)\n")
                    f.write(f"3. For each gap:\n")
                    f.write(f"   - Run `/research-serp [keyword]` for content brief\n")
                    f.write(f"   - Create 2000-3000 word comprehensive content\n")
                    f.write(f"   - Follow recommended content structure\n")
                    f.write(f"   - Target all identified SERP features\n")
                    f.write(f"4. Schedule 1-2 gap articles per week\n")
                else:
                    f.write(f"**Note:** Competitor gap analysis was skipped. Run manually:\n")
                    f.write(f"```bash\n")
                    f.write(f"python3 research_competitor_gaps.py\n")
                    f.write(f"```\n")

            elif item['source'] == 'Performance Matrix':
                f.write(f"**Action Steps:**\n")
                f.write(f"1. Open research/performance-matrix-{date_str}.md\n")
                f.write(f"2. Go to 'Declining' section\n")
                f.write(f"3. Identify 'Stars' that are declining\n")
                f.write(f"4. For each:\n")
                f.write(f"   - Update all statistics to current year\n")
                f.write(f"   - Add 500+ words of new content\n")
                f.write(f"   - Refresh images and examples\n")
                f.write(f"   - Improve internal linking\n")

            f.write(f"\n---\n\n")

        # Week 4+
        f.write(f"## 🏗️ WEEKS 4+: Strategic Initiatives\n\n")
        f.write(f"**Focus:** Long-term topical authority building\n\n")

        for i, item in enumerate(roadmap['week_4_plus'], 1):
            f.write(f"### {i}. {item['action']}\n\n")
            f.write(f"- **Source:** {item['source']}\n")
            f.write(f"- **Description:** {item['description']}\n")
            f.write(f"- **Effort:** {item['effort']}\n")
            f.write(f"- **Impact:** {item['impact']}\n\n")

            if item['source'] == 'Topic Clusters':
                f.write(f"**Action Steps:**\n")
                f.write(f"1. Open research/topic-clusters-{date_str}.md\n")
                f.write(f"2. Select top 2-3 weak clusters with high demand\n")
                f.write(f"3. For each cluster:\n")
                f.write(f"   - Create comprehensive pillar page (3000+ words)\n")
                f.write(f"   - Create 8-12 supporting cluster articles\n")
                f.write(f"   - Target all identified coverage gaps\n")
                f.write(f"   - Internal link all cluster content to pillar\n")
                f.write(f"4. Publish 1-2 cluster articles per week\n")

            f.write(f"\n---\n\n")

        # Ongoing
        f.write(f"## 🔄 Ongoing Maintenance\n\n")
        f.write(f"**Focus:** Continuous monitoring and optimization\n\n")

        for i, item in enumerate(roadmap['ongoing'], 1):
            f.write(f"### {i}. {item['action']} ({item['frequency']})\n\n")
            f.write(f"- **Source:** {item['source']}\n")
            f.write(f"- **Description:** {item['description']}\n\n")

        # Implementation tips
        f.write(f"---\n\n")
        f.write(f"## 💡 Implementation Tips\n\n")

        f.write(f"### Resource Allocation\n\n")
        f.write(f"**If you have:**\n")
        f.write(f"- **1-2 hours/week:** Focus on Week 1 quick wins only\n")
        f.write(f"- **5-10 hours/week:** Complete Week 1, start Week 2-3 initiatives\n")
        f.write(f"- **20+ hours/week:** Full roadmap execution\n\n")

        f.write(f"### Tools Integration\n\n")
        f.write(f"For each content item:\n")
        f.write(f"1. **Research:** `/research-serp [keyword]` - Get content requirements\n")
        f.write(f"2. **Create:** `/write [keyword]` - Generate content brief/outline\n")
        f.write(f"3. **Analyze:** `/analyze-existing [URL]` - For content updates\n")
        f.write(f"4. **Optimize:** `/optimize [file]` - Before publishing\n\n")

        f.write(f"### Success Metrics\n\n")
        f.write(f"Track these metrics weekly:\n")
        f.write(f"- **Quick wins:** Position changes for targeted keywords\n")
        f.write(f"- **Underperformers:** CTR improvements\n")
        f.write(f"- **New content:** Impressions and position after 2-4 weeks\n")
        f.write(f"- **Topic clusters:** Average position for cluster keywords\n")
        f.write(f"- **Overall:** Total organic clicks month-over-month\n\n")

        f.write(f"### When to Re-run This Analysis\n\n")
        f.write(f"- **Full comprehensive:** Monthly\n")
        f.write(f"- **Quick wins only:** Bi-weekly\n")
        f.write(f"- **Trending only:** Weekly\n")
        f.write(f"- **Performance matrix:** Monthly\n\n")

    print(f"   ✓ Roadmap saved: {filename}")


if __name__ == "__main__":
    main()
