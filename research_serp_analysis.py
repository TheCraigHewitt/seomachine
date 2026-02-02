#!/usr/bin/env python3
"""
Research SERP Analysis

Deep analysis of what Google wants for a specific keyword.
Analyzes content patterns, lengths, types, and SERP features
to create a detailed content brief.
"""

import os
import sys
import re
import statistics
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.dataforseo import DataForSEO
from modules.search_intent_analyzer import SearchIntentAnalyzer
from modules.content_length_comparator import ContentLengthComparator


def main():
    """Main entry point for SERP analysis"""
    if len(sys.argv) < 2:
        print("Usage: python research_serp_analysis.py \"keyword phrase\"")
        print("\nExample: python research_serp_analysis.py \"your target keyword\"")
        return

    keyword = sys.argv[1]

    print("=" * 80)
    print(f"SERP ANALYSIS: {keyword}")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Understand what Google wants before creating content")
    print("=" * 80)

    # Initialize
    print("\n1. Initializing analysis tools...")
    try:
        dfs = DataForSEO()
        print("   ✓ DataForSEO connected")
    except Exception as e:
        print(f"   ✗ DataForSEO Error: {e}")
        print("   DataForSEO is required for SERP analysis")
        return

    intent_analyzer = SearchIntentAnalyzer()
    content_comparator = ContentLengthComparator()
    print("   ✓ Analysis modules loaded")

    # Get SERP data
    print(f"\n2. Fetching SERP data for '{keyword}'...")
    try:
        serp_data = dfs.get_serp_data(keyword, limit=20)

        if not serp_data or 'organic_results' not in serp_data:
            print("   ✗ No SERP data available")
            return

        organic_results = serp_data['organic_results'][:10]  # Focus on top 10
        print(f"   ✓ Retrieved top {len(organic_results)} organic results")

    except Exception as e:
        print(f"   ✗ Error fetching SERP data: {e}")
        return

    # Analyze SERP patterns
    print(f"\n3. Analyzing SERP patterns...")

    analysis = {
        'keyword': keyword,
        'analyzed_date': datetime.now().strftime('%Y-%m-%d'),
        'top_results': organic_results,
        'serp_features': serp_data.get('features', []),
        'content_types': [],
        'title_patterns': [],
        'word_counts': [],
        'domains': [],
        'domain_authority': [],
        'freshness_signals': [],
        'common_h2_topics': [],
        'competitive_difficulty': 'medium'
    }

    # Analyze each result
    for i, result in enumerate(organic_results, 1):
        title = result.get('title', '')
        url = result.get('url', '')
        description = result.get('description', '')
        domain = extract_domain(url)

        analysis['domains'].append(domain)

        # Detect content type from title
        content_type = detect_content_type(title)
        analysis['content_types'].append(content_type)

        # Detect freshness signals (year in title)
        if has_freshness_signal(title):
            analysis['freshness_signals'].append(i)

        # Get word count
        try:
            word_count = content_comparator.fetch_word_count(url)
            if word_count and word_count > 100:  # Sanity check
                analysis['word_counts'].append(word_count)
                print(f"   [{i}] {domain} - {word_count:,} words - {content_type}")
        except Exception as e:
            print(f"   [{i}] {domain} - Word count unavailable - {content_type}")

    # Calculate statistics
    print(f"\n4. Calculating content requirements...")

    # Content type analysis
    if analysis['content_types']:
        type_counts = Counter(analysis['content_types'])
        dominant_type = type_counts.most_common(1)[0][0]
        analysis['dominant_content_type'] = dominant_type
        analysis['content_type_distribution'] = dict(type_counts)
        print(f"   Dominant Content Type: {dominant_type}")
        print(f"   Distribution: {dict(type_counts)}")

    # Word count analysis
    if analysis['word_counts']:
        avg_words = statistics.mean(analysis['word_counts'])
        median_words = statistics.median(analysis['word_counts'])
        min_words = min(analysis['word_counts'])
        max_words = max(analysis['word_counts'])

        analysis['avg_word_count'] = int(avg_words)
        analysis['median_word_count'] = int(median_words)
        analysis['min_word_count'] = min_words
        analysis['max_word_count'] = max_words
        analysis['recommended_word_count'] = int(avg_words * 1.1)  # 10% more than average

        print(f"   Average Word Count: {avg_words:,.0f}")
        print(f"   Median Word Count: {median_words:,.0f}")
        print(f"   Range: {min_words:,} - {max_words:,}")
        print(f"   Recommended: {analysis['recommended_word_count']:,}+ words")

    # Freshness analysis
    freshness_ratio = len(analysis['freshness_signals']) / len(organic_results)
    analysis['freshness_important'] = freshness_ratio >= 0.6
    if analysis['freshness_important']:
        print(f"   Freshness: IMPORTANT ({len(analysis['freshness_signals'])}/{len(organic_results)} results mention year)")
    else:
        print(f"   Freshness: Normal ({len(analysis['freshness_signals'])}/{len(organic_results)} results mention year)")

    # SERP features analysis
    print(f"\n   SERP Features Present:")
    for feature in analysis['serp_features'][:5]:
        print(f"   - {feature}")

    # Search intent analysis
    print(f"\n5. Analyzing search intent...")
    intent_result = intent_analyzer.analyze(
        keyword=keyword,
        serp_features=analysis['serp_features'],
        top_results=organic_results
    )

    primary_intent = intent_result.get('primary_intent', 'unknown')
    if hasattr(primary_intent, 'value'):
        primary_intent = primary_intent.value

    analysis['search_intent'] = str(primary_intent)

    # Handle confidence - it might be a dict or a number
    confidence_data = intent_result.get('confidence', 0)
    if isinstance(confidence_data, dict):
        analysis['intent_confidence'] = confidence_data.get('overall', 0)
    else:
        analysis['intent_confidence'] = float(confidence_data) if confidence_data else 0

    analysis['intent_recommendations'] = intent_result.get('recommendations', [])

    print(f"   Primary Intent: {analysis['search_intent']}")
    print(f"   Confidence: {analysis['intent_confidence']:.0f}%")

    # Competitive difficulty
    print(f"\n6. Assessing competitive difficulty...")
    difficulty = assess_difficulty(analysis['domains'])
    analysis['competitive_difficulty'] = difficulty
    print(f"   Competitive Difficulty: {difficulty.upper()}")

    # Generate content brief
    print(f"\n7. Generating content brief...")
    content_brief = generate_content_brief(keyword, analysis)
    analysis['content_brief'] = content_brief

    # Write report
    print(f"\n8. Writing report to research/serp-analysis-{sanitize_filename(keyword)}.md...")
    write_markdown_report(keyword, analysis)

    print("\n" + "=" * 80)
    print("✅ SERP ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/serp-analysis-{sanitize_filename(keyword)}.md")
    print(f"2. Use the content brief to create your article")
    print(f"3. Ensure your content meets/exceeds the recommended word count")
    print(f"4. Match the dominant content type identified")
    print(f"5. Target the SERP features present (PAA, featured snippet, etc.)")


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.replace('www.', '')


def detect_content_type(title: str) -> str:
    """Detect content type from title"""
    title_lower = title.lower()

    patterns = {
        'Listicle': [r'\d+\s+(best|top|ways|tips|tools|ideas|examples|reasons)'],
        'How-To Guide': [r'how to', r'guide to', r'tutorial'],
        'Definition': [r'what is', r'what are', r'meaning of', r'definition'],
        'Comparison': [r'vs\.?', r'versus', r'compared', r'comparison', r'difference between'],
        'Review': [r'review', r'reviewed'],
        'Tool/Resource': [r'calculator', r'tool', r'generator', r'template', r'free'],
    }

    for content_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, title_lower):
                return content_type

    return 'General Article'


def has_freshness_signal(title: str) -> bool:
    """Check if title contains year or freshness signals"""
    current_year = datetime.now().year
    last_year = current_year - 1

    freshness_patterns = [
        str(current_year),
        str(last_year),
        'updated',
        'latest',
        'new'
    ]

    return any(pattern in title.lower() for pattern in freshness_patterns)


def assess_difficulty(domains: List[str]) -> str:
    """Assess competitive difficulty based on domains"""
    # High authority domains
    high_authority = [
        'youtube.com', 'wikipedia.org', 'forbes.com', 'nytimes.com',
        'washingtonpost.com', 'cnn.com', 'bbc.com', 'techcrunch.com',
        'wired.com', 'theverge.com', 'reddit.com', 'hubspot.com'
    ]

    # Medium authority (industry-specific) - loaded from config
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'competitors.json')
    medium_authority = []
    if os.path.exists(config_path):
        import json
        with open(config_path) as f:
            config = json.load(f)
        medium_authority = config.get('direct_competitors', []) + config.get('content_competitors', [])

    high_count = sum(1 for d in domains if any(ha in d for ha in high_authority))
    medium_count = sum(1 for d in domains if any(ma in d for ma in medium_authority))

    if high_count >= 6:
        return 'very high'
    elif high_count >= 4:
        return 'high'
    elif medium_count >= 5:
        return 'medium'
    else:
        return 'low'


def generate_content_brief(keyword: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive content brief"""

    brief = {
        'target_keyword': keyword,
        'content_type': analysis.get('dominant_content_type', 'Guide'),
        'recommended_word_count': analysis.get('recommended_word_count', 2000),
        'search_intent': analysis.get('search_intent', 'informational'),
        'tone': determine_tone(analysis.get('search_intent', 'informational')),
        'must_have_elements': [],
        'serp_features_to_target': [],
        'structure_recommendations': []
    }

    # Must-have elements based on content type
    content_type = brief['content_type']

    if 'Listicle' in content_type:
        brief['must_have_elements'] = [
            'Numbered list format',
            'Comparison table',
            'Pros and cons for each item',
            'Clear introduction explaining criteria',
            'Summary/conclusion with top recommendation'
        ]
        brief['structure_recommendations'] = [
            'Introduction (what, why, how to choose)',
            f'Item 1-{extract_number_from_titles(analysis.get("title_patterns", []))} (each with description, pros/cons)',
            'Comparison table',
            'FAQs',
            'Conclusion with top pick'
        ]

    elif 'How-To' in content_type:
        brief['must_have_elements'] = [
            'Step-by-step instructions',
            'Visual aids (screenshots, diagrams)',
            'Prerequisites section',
            'Time estimate',
            'Troubleshooting tips'
        ]
        brief['structure_recommendations'] = [
            'Introduction (what you\'ll learn)',
            'Prerequisites/Requirements',
            'Step-by-step instructions',
            'Common mistakes to avoid',
            'FAQs',
            'Conclusion/Next steps'
        ]

    elif 'Definition' in content_type:
        brief['must_have_elements'] = [
            'Clear, concise definition upfront',
            'Examples',
            'History/etymology if relevant',
            'Related concepts',
            'Practical applications'
        ]
        brief['structure_recommendations'] = [
            'Quick definition (target featured snippet)',
            'Detailed explanation',
            'Examples',
            'Related terms/concepts',
            'Practical applications',
            'FAQs'
        ]

    else:
        brief['must_have_elements'] = [
            'Comprehensive coverage',
            'Expert insights',
            'Real examples',
            'Data and statistics'
        ]
        brief['structure_recommendations'] = [
            'Introduction',
            'Main sections (3-5)',
            'Examples and case studies',
            'FAQs',
            'Conclusion'
        ]

    # SERP features to target
    serp_features = analysis.get('serp_features', [])

    if 'featured_snippet' in str(serp_features).lower():
        brief['serp_features_to_target'].append('Featured Snippet - Add concise definition/answer in first 100 words')

    if 'people_also_ask' in str(serp_features).lower():
        brief['serp_features_to_target'].append('People Also Ask - Add FAQ section answering related questions')

    if 'video' in str(serp_features).lower():
        brief['serp_features_to_target'].append('Video - Consider embedding relevant video or creating one')

    if 'images' in str(serp_features).lower():
        brief['serp_features_to_target'].append('Images - Include high-quality images with alt text')

    # Freshness requirement
    if analysis.get('freshness_important'):
        brief['must_have_elements'].append(f'Current year ({datetime.now().year}) in title and content')
        brief['must_have_elements'].append('Latest statistics and examples')

    return brief


def extract_number_from_titles(titles: List[str]) -> int:
    """Extract common number from listicle titles"""
    numbers = []
    for title in titles:
        match = re.search(r'(\d+)\s+', title)
        if match:
            numbers.append(int(match.group(1)))

    if numbers:
        return statistics.mode(numbers) if numbers else 10
    return 10


def determine_tone(intent: str) -> str:
    """Determine appropriate tone based on search intent"""
    intent_lower = str(intent).lower()

    if 'transactional' in intent_lower:
        return 'Direct and action-oriented'
    elif 'commercial' in intent_lower:
        return 'Balanced and informative, helping decision-making'
    elif 'navigational' in intent_lower:
        return 'Clear and straightforward'
    else:
        return 'Educational and helpful'


def sanitize_filename(keyword: str) -> str:
    """Convert keyword to safe filename"""
    # Remove special characters, replace spaces with hyphens
    safe = re.sub(r'[^\w\s-]', '', keyword)
    safe = re.sub(r'[\s]+', '-', safe)
    safe = safe.lower().strip('-')
    return safe[:50]  # Limit length


def write_markdown_report(keyword: str, analysis: Dict[str, Any]):
    """Write detailed markdown report"""
    safe_keyword = sanitize_filename(keyword)
    filename = f"research/serp-analysis-{safe_keyword}.md"

    with open(filename, 'w') as f:
        f.write(f"# SERP Analysis: {keyword}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Purpose:** Understand what Google wants for this keyword before creating content\n\n")
        f.write("---\n\n")

        # Overview
        f.write(f"## Overview\n\n")
        f.write(f"- **Target Keyword:** {keyword}\n")
        f.write(f"- **Search Intent:** {analysis.get('search_intent', 'unknown')}\n")
        f.write(f"- **Dominant Content Type:** {analysis.get('dominant_content_type', 'Unknown')}\n")
        f.write(f"- **Competitive Difficulty:** {analysis.get('competitive_difficulty', 'medium').upper()}\n")
        f.write(f"- **Freshness Important:** {'Yes' if analysis.get('freshness_important') else 'No'}\n\n")

        # Content requirements
        f.write(f"## Content Requirements\n\n")

        if analysis.get('avg_word_count'):
            f.write(f"### Word Count\n\n")
            f.write(f"- **Average:** {analysis['avg_word_count']:,} words\n")
            f.write(f"- **Median:** {analysis.get('median_word_count', 0):,} words\n")
            f.write(f"- **Range:** {analysis.get('min_word_count', 0):,} - {analysis.get('max_word_count', 0):,} words\n")
            f.write(f"- **Recommended:** {analysis.get('recommended_word_count', 2000):,}+ words (exceed average by 10%)\n\n")

        f.write(f"### Content Type Distribution\n\n")
        if analysis.get('content_type_distribution'):
            for ctype, count in sorted(analysis['content_type_distribution'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {ctype}: {count}/10 results\n")
            f.write(f"\n**Recommendation:** Your content should be a **{analysis.get('dominant_content_type', 'Guide')}**\n\n")

        # SERP Features
        f.write(f"## SERP Features Present\n\n")
        serp_features = analysis.get('serp_features', [])
        if serp_features:
            for feature in serp_features:
                f.write(f"- {feature}\n")
        else:
            f.write(f"- No special SERP features detected\n")
        f.write(f"\n")

        # Top 10 analysis
        f.write(f"## Top 10 Ranking Analysis\n\n")
        f.write(f"| Position | Domain | Content Type | Word Count |\n")
        f.write(f"|----------|--------|--------------|------------|\n")

        for i, result in enumerate(analysis['top_results'], 1):
            domain = extract_domain(result.get('url', ''))
            content_type = analysis['content_types'][i-1] if i <= len(analysis['content_types']) else 'Unknown'
            word_count = analysis['word_counts'][i-1] if i <= len(analysis['word_counts']) else 'N/A'
            if isinstance(word_count, int):
                word_count = f"{word_count:,}"
            f.write(f"| {i} | {domain[:30]} | {content_type} | {word_count} |\n")

        f.write(f"\n")

        # Content brief
        if analysis.get('content_brief'):
            brief = analysis['content_brief']

            f.write(f"## Content Brief\n\n")
            f.write(f"### Target Specifications\n\n")
            f.write(f"- **Primary Keyword:** {brief.get('target_keyword')}\n")
            f.write(f"- **Content Type:** {brief.get('content_type')}\n")
            f.write(f"- **Target Word Count:** {brief.get('recommended_word_count', 2000):,}+ words\n")
            f.write(f"- **Search Intent:** {brief.get('search_intent')}\n")
            f.write(f"- **Tone:** {brief.get('tone')}\n\n")

            f.write(f"### Must-Have Elements\n\n")
            for element in brief.get('must_have_elements', []):
                f.write(f"- [ ] {element}\n")
            f.write(f"\n")

            if brief.get('serp_features_to_target'):
                f.write(f"### SERP Features to Target\n\n")
                for feature in brief['serp_features_to_target']:
                    f.write(f"- [ ] {feature}\n")
                f.write(f"\n")

            f.write(f"### Recommended Structure\n\n")
            for i, section in enumerate(brief.get('structure_recommendations', []), 1):
                f.write(f"{i}. {section}\n")
            f.write(f"\n")

        # Competitive insights
        f.write(f"## Competitive Insights\n\n")
        f.write(f"### Domain Authority Mix\n\n")

        domain_counts = Counter(analysis['domains'])
        f.write(f"Top domains ranking:\n")
        for domain, count in domain_counts.most_common(5):
            f.write(f"- {domain}: {count} result(s)\n")

        f.write(f"\n### Competitive Difficulty: {analysis.get('competitive_difficulty', 'medium').upper()}\n\n")

        difficulty = analysis.get('competitive_difficulty', 'medium')
        if difficulty in ['very high', 'high']:
            f.write(f"⚠️ **High competition** - Major authority sites dominate. You'll need:\n")
            f.write(f"- Exceptional content quality\n")
            f.write(f"- Strong backlink profile\n")
            f.write(f"- Unique angle or superior depth\n")
            f.write(f"- Time to build authority (6-12 months)\n\n")
        elif difficulty == 'medium':
            f.write(f"✅ **Moderate competition** - Mix of authority and niche sites. You can rank with:\n")
            f.write(f"- Comprehensive, well-researched content\n")
            f.write(f"- Better formatting and user experience\n")
            f.write(f"- Some quality backlinks\n")
            f.write(f"- Expected timeline: 3-6 months\n\n")
        else:
            f.write(f"🎯 **Low competition** - Opportunity for quick rankings. Focus on:\n")
            f.write(f"- Quality content exceeding current results\n")
            f.write(f"- Proper on-page SEO\n")
            f.write(f"- Internal linking\n")
            f.write(f"- Expected timeline: 1-3 months\n\n")

        # Action plan
        f.write(f"## Action Plan\n\n")
        f.write(f"### Step 1: Research (1-2 hours)\n")
        f.write(f"- [ ] Read all top 10 ranking articles\n")
        f.write(f"- [ ] Identify common topics covered\n")
        f.write(f"- [ ] Find gaps they missed\n")
        f.write(f"- [ ] Collect statistics and examples\n\n")

        f.write(f"### Step 2: Outline (30 minutes)\n")
        f.write(f"- [ ] Create detailed outline following recommended structure\n")
        f.write(f"- [ ] Plan unique angles or superior depth\n")
        f.write(f"- [ ] List all H2 and H3 headings\n\n")

        f.write(f"### Step 3: Write (3-4 hours)\n")
        f.write(f"- [ ] Write {brief.get('recommended_word_count', 2000):,}+ words\n")
        f.write(f"- [ ] Include all must-have elements\n")
        f.write(f"- [ ] Target SERP features (featured snippet, PAA)\n")
        f.write(f"- [ ] Add visuals/screenshots\n\n")

        f.write(f"### Step 4: Optimize (30 minutes)\n")
        f.write(f"- [ ] Optimize title tag (include '{keyword}')\n")
        f.write(f"- [ ] Write compelling meta description\n")
        f.write(f"- [ ] Add internal links to related content\n")
        f.write(f"- [ ] Add FAQ schema markup\n")
        f.write(f"- [ ] Optimize images with alt text\n\n")

        f.write(f"### Step 5: Publish & Promote\n")
        f.write(f"- [ ] Publish on your site\n")
        f.write(f"- [ ] Share on social media\n")
        f.write(f"- [ ] Reach out for backlinks if appropriate\n")
        f.write(f"- [ ] Monitor rankings weekly\n\n")

        # Top ranking titles for reference
        f.write(f"## Top Ranking Titles (for reference)\n\n")
        for i, result in enumerate(analysis['top_results'], 1):
            f.write(f"{i}. {result.get('title', 'No title')}\n")
        f.write(f"\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
