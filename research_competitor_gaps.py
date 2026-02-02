#!/usr/bin/env python3
"""
Research Competitor Content Gaps

Identifies keywords where competitors rank in top 20 but you don't rank at all.
These are proven demand areas with zero cannibalization - highest ROI opportunities.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.dataforseo import DataForSEO
from modules.opportunity_scorer import OpportunityScorer, OpportunityType
from modules.search_intent_analyzer import SearchIntentAnalyzer


def load_competitors():
    """Load competitor lists from config file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'competitors.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        return config.get('direct_competitors', []), config.get('content_competitors', [])
    print("WARNING: config/competitors.json not found. See config/competitors.example.json")
    return [], []


DIRECT_COMPETITORS, CONTENT_COMPETITORS = load_competitors()


def main():
    print("=" * 80)
    print("COMPETITOR CONTENT GAP ANALYSIS")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Find keywords competitors rank for that we don't")
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
        print(f"   ✗ DataForSEO Error: {e}")
        print("   DataForSEO is required for competitor analysis")
        return

    # Initialize scoring modules
    scorer = OpportunityScorer()
    intent_analyzer = SearchIntentAnalyzer()
    print("   ✓ Analysis modules loaded")

    # Get our current ranking keywords
    print("\n2. Fetching your current rankings from GSC...")
    our_keywords = gsc.get_keyword_positions(days=90)
    # Filter by minimum impressions
    our_keywords = [kw for kw in our_keywords if kw.get('impressions', 0) >= 10]
    our_keyword_set = {kw['keyword'].lower().strip() for kw in our_keywords}
    print(f"   ✓ Found {len(our_keyword_set)} keywords you're ranking for")

    # Analyze competitors
    all_competitors = DIRECT_COMPETITORS + CONTENT_COMPETITORS
    print(f"\n3. Analyzing {len(all_competitors)} competitors...")

    competitor_gaps = []
    seen_keywords = set()  # To deduplicate

    for i, competitor in enumerate(all_competitors, 1):
        comp_type = "Direct" if competitor in DIRECT_COMPETITORS else "Content"
        print(f"\n   [{i}/{len(all_competitors)}] Analyzing {competitor} ({comp_type})...")

        try:
            # Get competitor's top ranking keywords
            comp_keywords = dfs.get_domain_keywords(
                domain=competitor,
                position_max=20,  # Top 20 only
                limit=300  # Reasonable limit to manage API costs
            )

            if not comp_keywords:
                print(f"      No data available for {competitor}")
                continue

            print(f"      Found {len(comp_keywords)} keywords they rank for (top 20)")

            # Find gaps
            gaps_found = 0
            for kw_data in comp_keywords:
                keyword = kw_data['keyword'].lower().strip()

                # Skip if:
                # - We already rank for it
                # - Already seen from another competitor
                # - Too branded/specific to them
                if (keyword in our_keyword_set or
                    keyword in seen_keywords or
                    is_branded_keyword(keyword, competitor)):
                    continue

                # Filter for relevant keywords
                if not is_relevant_keyword(keyword):
                    continue

                seen_keywords.add(keyword)
                gaps_found += 1

                # Enrich with analysis
                gap_data = {
                    'keyword': kw_data['keyword'],  # Original case
                    'competitor': competitor,
                    'competitor_type': comp_type,
                    'competitor_position': kw_data.get('position', 99),
                    'search_volume': kw_data.get('search_volume', 0),
                    'cpc': kw_data.get('cpc', 0),
                    'difficulty': kw_data.get('difficulty', 50),
                    'your_position': None  # Not ranking
                }

                competitor_gaps.append(gap_data)

            print(f"      Identified {gaps_found} gap opportunities")

        except Exception as e:
            print(f"      Error analyzing {competitor}: {e}")
            continue

    if not competitor_gaps:
        print("\n   No competitor gaps found!")
        return

    print(f"\n4. Analyzing {len(competitor_gaps)} total gap opportunities...")

    # Enrich gap data with intent analysis and scoring
    enriched_gaps = []
    for i, gap in enumerate(competitor_gaps):
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i+1}/{len(competitor_gaps)}...")

        try:
            # Get SERP data for intent analysis
            serp_features = []
            try:
                serp_data = dfs.get_serp_data(gap['keyword'], limit=10)
                if serp_data and 'features' in serp_data:
                    serp_features = serp_data.get('features', [])
                    gap['serp_features'] = serp_features
            except:
                pass

            # Analyze search intent
            intent_result = intent_analyzer.analyze(
                keyword=gap['keyword'],
                serp_features=serp_features
            )

            primary_intent = intent_result.get('primary_intent', 'unknown')
            if hasattr(primary_intent, 'value'):
                primary_intent = primary_intent.value

            gap['search_intent'] = str(primary_intent)
            gap['intent_confidence'] = float(intent_result.get('confidence', {}).get('overall', 0)) if isinstance(intent_result.get('confidence'), dict) else 0

            # Determine content type needed
            gap['content_type'] = determine_content_type(gap['keyword'], serp_features)

            # Calculate opportunity score
            # For new content, we create a pseudo keyword_data dict
            keyword_data = {
                'keyword': gap['keyword'],
                'position': 100,  # Not ranking
                'impressions': gap.get('search_volume', 0),
                'clicks': 0,
                'ctr': 0,
                'commercial_intent': calculate_commercial_intent_from_serp(intent_result)
            }

            score_result = scorer.calculate_score(
                keyword_data=keyword_data,
                opportunity_type=OpportunityType.NEW_CONTENT,
                search_volume=gap.get('search_volume'),
                difficulty=gap.get('difficulty'),
                serp_features=serp_features,
                cluster_value=50  # Default
            )

            gap['opportunity_score'] = score_result['final_score']
            gap['priority'] = score_result['priority']
            gap['score_breakdown'] = score_result['score_breakdown']

            enriched_gaps.append(gap)

        except Exception as e:
            print(f"   Error enriching '{gap['keyword']}': {e}")
            continue

    # Sort by opportunity score
    enriched_gaps.sort(key=lambda x: x['opportunity_score'], reverse=True)

    # Filter to top opportunities (skip low priority)
    top_gaps = [g for g in enriched_gaps if g['priority'] not in ['SKIP', 'LOW']]

    print(f"\n   ✓ Analysis complete")
    print(f"   Total gaps found: {len(competitor_gaps)}")
    print(f"   High-value opportunities: {len(top_gaps)}")

    # Display summary
    print("\n" + "=" * 80)
    print("TOP 10 COMPETITOR GAP OPPORTUNITIES")
    print("=" * 80)

    for i, gap in enumerate(top_gaps[:10], 1):
        print(f"\n#{i} KEYWORD: {gap['keyword']}")
        print("-" * 80)
        print(f"Competitor: {gap['competitor']} (position {gap['competitor_position']})")
        print(f"Search Volume: {gap.get('search_volume', 'Unknown')}/month")
        print(f"Difficulty: {gap.get('difficulty', 'Unknown')}/100")
        print(f"Search Intent: {gap.get('search_intent', 'unknown')}")
        print(f"Content Type Needed: {gap.get('content_type', 'Guide')}")
        print(f"Opportunity Score: {gap['opportunity_score']:.2f}/100")
        print(f"Priority: {gap['priority']}")

    # Write report
    print(f"\n5. Writing report to research/competitor-gaps-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(top_gaps, len(competitor_gaps))

    print("\n" + "=" * 80)
    print("✅ COMPETITOR GAP ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/competitor-gaps-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Prioritize top 5-10 gaps based on your content strategy")
    print(f"3. Create comprehensive content for each gap")
    print(f"4. Use /write [keyword] command to generate content briefs")


def is_branded_keyword(keyword: str, domain: str) -> bool:
    """Check if keyword is branded/specific to the competitor"""
    # Extract brand name from domain
    brand = domain.split('.')[0]

    # Check if brand name is in keyword
    if brand.lower() in keyword.lower():
        return True

    # Known branded terms (derived from competitor domains)
    branded_terms = {}
    for comp in DIRECT_COMPETITORS + CONTENT_COMPETITORS:
        domain_part = comp.split('.')[0]
        branded_terms[domain_part] = [domain_part]

    for domain_part, terms in branded_terms.items():
        if domain_part in domain.lower():
            for term in terms:
                if term in keyword.lower():
                    return True

    return False


def is_relevant_keyword(keyword: str) -> bool:
    """Filter for relevant industry keywords. Override relevant_terms for your niche."""
    keyword_lower = keyword.lower()

    # Minimum keyword length
    if len(keyword) < 4:
        return False

    # Industry-relevant terms - customize for your niche
    # Load from config if available, otherwise accept all keywords
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'competitors.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        relevant_terms = config.get('relevant_terms', [])
        if not relevant_terms:
            return True  # No filter configured, accept all
    else:
        return True  # No config, accept all

    relevant_terms = [t.lower() for t in relevant_terms]

    # Check if keyword contains any relevant terms
    if not any(term in keyword_lower for term in relevant_terms):
        return False

    # Exclude obvious spam/irrelevant
    spam_terms = [
        'porn', 'xxx', 'casino', 'pills', 'viagra',
        'weight loss', 'crypto', 'forex', 'loan'
    ]

    if any(term in keyword_lower for term in spam_terms):
        return False

    return True


def determine_content_type(keyword: str, serp_features: List[str]) -> str:
    """Determine what type of content is needed based on keyword and SERP"""
    keyword_lower = keyword.lower()

    # Listicle signals
    if any(word in keyword_lower for word in ['best', 'top', 'list of']):
        return 'Listicle/Comparison'

    # How-to signals
    if any(word in keyword_lower for word in ['how to', 'how do', 'guide', 'tutorial']):
        return 'How-To Guide'

    # What is signals
    if any(word in keyword_lower for word in ['what is', 'what are', 'meaning', 'definition']):
        return 'Definitional Guide'

    # Comparison signals
    if any(word in keyword_lower for word in ['vs', 'versus', 'compared', 'comparison', 'difference between']):
        return 'Comparison Article'

    # Tool/calculator signals
    if any(word in keyword_lower for word in ['calculator', 'tool', 'generator', 'template']):
        return 'Tool/Resource Page'

    # Default based on SERP features
    if 'people_also_ask' in str(serp_features).lower():
        return 'Comprehensive Guide'

    return 'Guide/Article'


def calculate_commercial_intent_from_serp(intent_result: Dict[str, Any]) -> float:
    """Convert search intent to commercial intent score (0.1-3.0)"""
    primary_intent = intent_result.get('primary_intent', 'informational')

    if hasattr(primary_intent, 'value'):
        primary_intent = primary_intent.value

    intent_map = {
        'transactional': 3.0,
        'commercial_investigation': 2.0,
        'commercial': 2.0,
        'informational': 1.0,
        'navigational': 0.5
    }

    return intent_map.get(str(primary_intent).lower(), 1.0)


def write_markdown_report(gaps: List[Dict[str, Any]], total_found: int):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/competitor-gaps-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Competitor Content Gap Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Strategy:** Identify proven demand areas where competitors rank but we don't\n\n")
        f.write(f"**Total Gaps Found:** {total_found}\n")
        f.write(f"**High-Value Opportunities:** {len(gaps)}\n\n")
        f.write("---\n\n")

        # Group by priority
        critical = [g for g in gaps if g['priority'] == 'CRITICAL']
        high = [g for g in gaps if g['priority'] == 'HIGH']
        medium = [g for g in gaps if g['priority'] == 'MEDIUM']

        f.write(f"## Summary by Priority\n\n")
        f.write(f"- **CRITICAL:** {len(critical)} opportunities\n")
        f.write(f"- **HIGH:** {len(high)} opportunities\n")
        f.write(f"- **MEDIUM:** {len(medium)} opportunities\n\n")
        f.write("---\n\n")

        # Top 20 opportunities
        f.write(f"## Top 20 Content Gap Opportunities\n\n")

        for i, gap in enumerate(gaps[:20], 1):
            f.write(f"### {i}. {gap['keyword']}\n\n")

            f.write(f"**Priority:** {gap['priority']}  \n")
            f.write(f"**Opportunity Score:** {gap['opportunity_score']:.2f}/100\n\n")

            f.write(f"#### Competitor Intel\n\n")
            f.write(f"- **Ranking Competitor:** {gap['competitor']} ({gap['competitor_type']})\n")
            f.write(f"- **Their Position:** {gap['competitor_position']}\n")
            f.write(f"- **Your Position:** Not ranking (top 100)\n\n")

            f.write(f"#### Keyword Metrics\n\n")
            f.write(f"- **Search Volume:** {gap.get('search_volume', 'Unknown')}/month\n")
            f.write(f"- **SEO Difficulty:** {gap.get('difficulty', 'Unknown')}/100\n")
            if gap.get('cpc'):
                f.write(f"- **CPC:** ${gap['cpc']:.2f}\n")
            f.write(f"- **Search Intent:** {gap.get('search_intent', 'unknown')}\n")
            f.write(f"- **Content Type Needed:** {gap.get('content_type', 'Guide')}\n\n")

            if gap.get('score_breakdown'):
                f.write(f"#### Opportunity Analysis\n\n")
                breakdown = gap['score_breakdown']
                f.write(f"- Volume Score: {breakdown.get('volume_score', 0):.0f}/100\n")
                f.write(f"- Competition Score: {breakdown.get('competition_score', 0):.0f}/100\n")
                f.write(f"- Intent Score: {breakdown.get('intent_score', 0):.0f}/100\n\n")

            f.write(f"#### Recommended Action\n\n")
            f.write(f"Create comprehensive {gap.get('content_type', 'guide').lower()} targeting this keyword.\n\n")

            f.write(f"**Next Steps:**\n")
            f.write(f"1. Analyze top 10 ranking content for '{gap['keyword']}'\n")
            f.write(f"2. Identify content gaps and unique angles\n")
            f.write(f"3. Create detailed content outline\n")
            f.write(f"4. Write comprehensive, 2000+ word {gap.get('content_type', 'article').lower()}\n")
            f.write(f"5. Optimize for target keyword and related terms\n")
            f.write(f"6. Build internal linking strategy\n\n")

            if gap.get('serp_features'):
                f.write(f"**SERP Features Present:** {', '.join(gap['serp_features'][:5])}\n\n")

            f.write("---\n\n")

        # Summary recommendations
        f.write(f"## Implementation Strategy\n\n")
        f.write(f"### Phase 1: Quick Wins (Weeks 1-2)\n")
        f.write(f"Focus on CRITICAL priority gaps with lower difficulty:\n\n")

        quick_wins = [g for g in critical if g.get('difficulty', 100) < 50][:5]
        for i, gap in enumerate(quick_wins, 1):
            f.write(f"{i}. **{gap['keyword']}** - Difficulty: {gap.get('difficulty', 'Unknown')}, Volume: {gap.get('search_volume', 'Unknown')}\n")

        f.write(f"\n### Phase 2: High-Value Targets (Weeks 3-6)\n")
        f.write(f"Target HIGH priority gaps with strong search volume:\n\n")

        high_value = [g for g in high if g.get('search_volume', 0) > 500][:5]
        for i, gap in enumerate(high_value, 1):
            f.write(f"{i}. **{gap['keyword']}** - Volume: {gap.get('search_volume', 'Unknown')}, Difficulty: {gap.get('difficulty', 'Unknown')}\n")

        f.write(f"\n### Phase 3: Content Clusters (Weeks 7+)\n")
        f.write(f"Build topical authority by creating content clusters around related gaps.\n\n")

        f.write(f"## Key Insights\n\n")

        # Analyze patterns
        total_volume = sum(g.get('search_volume', 0) for g in gaps if g.get('search_volume'))
        avg_difficulty = sum(g.get('difficulty', 0) for g in gaps if g.get('difficulty')) / len([g for g in gaps if g.get('difficulty')])

        f.write(f"- **Total Potential Search Volume:** {total_volume:,}/month\n")
        f.write(f"- **Average SEO Difficulty:** {avg_difficulty:.1f}/100\n")

        # Content type breakdown
        content_types = {}
        for gap in gaps:
            ct = gap.get('content_type', 'Unknown')
            content_types[ct] = content_types.get(ct, 0) + 1

        f.write(f"\n**Content Types Needed:**\n")
        for ct, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {ct}: {count} articles\n")

        # Competitor breakdown
        competitor_counts = {}
        for gap in gaps:
            comp = gap['competitor']
            competitor_counts[comp] = competitor_counts.get(comp, 0) + 1

        f.write(f"\n**Top Competitors to Learn From:**\n")
        for comp, count in sorted(competitor_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            f.write(f"- {comp}: {count} gap opportunities\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
