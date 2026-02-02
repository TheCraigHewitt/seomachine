#!/usr/bin/env python3
"""
Research Topic Clusters

Analyzes topical authority by clustering keywords into related topics.
Identifies which topics you dominate and where you have gaps.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Set
from collections import Counter, defaultdict
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.google_search_console import GoogleSearchConsole
from modules.dataforseo import DataForSEO

# Try to import sklearn for clustering (optional)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Note: sklearn not available. Using simple keyword grouping instead.")


def main():
    print("=" * 80)
    print("TOPIC CLUSTER ANALYSIS")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Identify topical authority gaps and cluster building opportunities")
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

    # Get all ranking keywords
    print("\n2. Fetching all ranking keywords from GSC...")
    try:
        all_keywords = gsc.get_keyword_positions(days=90, min_impressions=5)
        print(f"   ✓ Found {len(all_keywords)} ranking keywords")
    except Exception as e:
        print(f"   ✗ Error fetching keywords: {e}")
        return

    if len(all_keywords) < 10:
        print("   Not enough keywords for clustering analysis")
        return

    # Cluster keywords
    print(f"\n3. Clustering keywords into topics...")

    if SKLEARN_AVAILABLE and len(all_keywords) >= 20:
        clusters = cluster_keywords_ml(all_keywords)
        print(f"   ✓ Created {len(clusters)} topic clusters using ML")
    else:
        clusters = cluster_keywords_simple(all_keywords)
        print(f"   ✓ Created {len(clusters)} topic clusters using keyword matching")

    # Analyze each cluster
    print(f"\n4. Analyzing topic authority for each cluster...")
    cluster_analysis = []

    for cluster_id, cluster_data in clusters.items():
        keywords_in_cluster = cluster_data['keywords']

        # Calculate cluster metrics
        total_impressions = sum(kw['impressions'] for kw in keywords_in_cluster)
        total_clicks = sum(kw['clicks'] for kw in keywords_in_cluster)
        avg_position = sum(kw['position'] for kw in keywords_in_cluster) / len(keywords_in_cluster)

        # Calculate authority score (0-100)
        authority_score = calculate_authority_score(
            keyword_count=len(keywords_in_cluster),
            avg_position=avg_position,
            total_impressions=total_impressions
        )

        # Identify cluster topic name
        topic_name = cluster_data['topic']

        # Find coverage gaps
        coverage_gaps = []
        if has_dfs:
            try:
                # Get related keywords we might be missing
                seed_keyword = keywords_in_cluster[0]['keyword']
                coverage_gaps = find_cluster_gaps(seed_keyword, keywords_in_cluster, dfs)
            except:
                pass

        cluster_analysis.append({
            'topic': topic_name,
            'keyword_count': len(keywords_in_cluster),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'avg_position': round(avg_position, 1),
            'authority_score': authority_score,
            'authority_level': get_authority_level(authority_score),
            'coverage_gaps': coverage_gaps[:10],  # Top 10 gaps
            'top_keywords': sorted(keywords_in_cluster, key=lambda x: x['impressions'], reverse=True)[:5]
        })

    # Sort by authority score (lowest first = biggest opportunity)
    cluster_analysis.sort(key=lambda x: x['authority_score'])

    # Display summary
    print("\n" + "=" * 80)
    print("TOPIC AUTHORITY SUMMARY")
    print("=" * 80)

    print(f"\n📊 Cluster Distribution:")
    print(f"   Total Topics: {len(cluster_analysis)}")

    authority_levels = Counter(c['authority_level'] for c in cluster_analysis)
    print(f"   Strong Authority: {authority_levels.get('Strong', 0)}")
    print(f"   Moderate Authority: {authority_levels.get('Moderate', 0)}")
    print(f"   Weak Authority: {authority_levels.get('Weak', 0)}")
    print(f"   Minimal Authority: {authority_levels.get('Minimal', 0)}")

    # Show top opportunities (weakest clusters with demand)
    print(f"\n🎯 TOP 5 TOPIC CLUSTER OPPORTUNITIES (Build These!)")
    print("-" * 80)

    weak_clusters = [c for c in cluster_analysis if c['authority_level'] in ['Weak', 'Minimal']]
    # Sort by impressions (demand)
    weak_with_demand = sorted(weak_clusters, key=lambda x: x['total_impressions'], reverse=True)[:5]

    for i, cluster in enumerate(weak_with_demand, 1):
        print(f"\n{i}. {cluster['topic'].upper()}")
        print(f"   Keywords Ranking: {cluster['keyword_count']}")
        print(f"   Authority Score: {cluster['authority_score']}/100 ({cluster['authority_level']})")
        print(f"   Avg Position: {cluster['avg_position']}")
        print(f"   Total Impressions: {cluster['total_impressions']:,}/month")

        if cluster['coverage_gaps']:
            print(f"   Coverage Gaps Found: {len(cluster['coverage_gaps'])}")
            print(f"   Top Gaps:")
            for gap in cluster['coverage_gaps'][:3]:
                vol = gap.get('search_volume', 'Unknown')
                print(f"     - {gap['keyword']} ({vol} searches/mo)")

    # Show strong clusters
    print(f"\n\n⭐ TOP 5 STRONG TOPIC CLUSTERS (Maintain These!)")
    print("-" * 80)

    strong_clusters = [c for c in cluster_analysis if c['authority_level'] == 'Strong']
    strong_sorted = sorted(strong_clusters, key=lambda x: x['authority_score'], reverse=True)[:5]

    for i, cluster in enumerate(strong_sorted, 1):
        print(f"\n{i}. {cluster['topic'].upper()}")
        print(f"   Keywords Ranking: {cluster['keyword_count']}")
        print(f"   Authority Score: {cluster['authority_score']}/100 ({cluster['authority_level']})")
        print(f"   Avg Position: {cluster['avg_position']}")
        print(f"   Total Clicks: {cluster['total_clicks']:,}/month")

    # Write report
    print(f"\n\n5. Writing report to research/topic-clusters-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(cluster_analysis)

    print("\n" + "=" * 80)
    print("✅ TOPIC CLUSTER ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/topic-clusters-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Focus on weak clusters with high demand")
    print(f"3. Create content for identified coverage gaps")
    print(f"4. Build comprehensive topic clusters around weak areas")
    print(f"5. Maintain and expand strong clusters")


def cluster_keywords_ml(keywords: List[Dict]) -> Dict[int, Dict]:
    """Cluster keywords using TF-IDF and K-means"""
    keyword_texts = [kw['keyword'] for kw in keywords]

    # Determine optimal number of clusters (roughly 1 cluster per 15-20 keywords)
    n_clusters = max(5, min(20, len(keywords) // 15))

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        max_features=100,
        ngram_range=(1, 2),
        stop_words='english'
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(keyword_texts)

        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)

        # Organize into clusters
        clusters = defaultdict(lambda: {'keywords': [], 'topic': ''})

        for i, kw in enumerate(keywords):
            cluster_id = cluster_labels[i]
            clusters[cluster_id]['keywords'].append(kw)

        # Determine topic name for each cluster
        for cluster_id, data in clusters.items():
            cluster_keywords = [kw['keyword'] for kw in data['keywords']]
            topic_name = extract_topic_name(cluster_keywords)
            data['topic'] = topic_name

        return dict(clusters)

    except Exception as e:
        print(f"   ML clustering failed: {e}, falling back to simple clustering")
        return cluster_keywords_simple(keywords)


def cluster_keywords_simple(keywords: List[Dict]) -> Dict[int, Dict]:
    """Simple keyword clustering based on common terms"""

    # Define topic patterns - customize these for your industry
    # Load from config if available
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'competitors.json')
    if os.path.exists(config_path):
        import json
        with open(config_path) as f:
            config = json.load(f)
        topic_patterns = config.get('topic_patterns', {})
    else:
        # Default generic patterns - customize for your niche
        topic_patterns = {
            'Product Features': ['feature', 'tool', 'platform', 'service', 'software'],
            'Pricing': ['price', 'pricing', 'cost', 'plan', 'free', 'trial'],
            'Tutorials': ['how to', 'guide', 'tutorial', 'step', 'setup'],
            'Comparisons': ['vs', 'versus', 'compare', 'comparison', 'alternative', 'best'],
            'Marketing': ['market', 'marketing', 'promote', 'promotion', 'grow', 'audience'],
            'Analytics': ['analytics', 'stats', 'statistics', 'metrics', 'data', 'report'],
            'Integration': ['integration', 'connect', 'api', 'webhook', 'automate'],
            'Getting Started': ['start', 'starting', 'beginner', 'guide', 'onboard'],
        }

    clusters = defaultdict(lambda: {'keywords': [], 'topic': ''})
    uncategorized = []

    # Assign keywords to topics
    for kw in keywords:
        keyword_lower = kw['keyword'].lower()
        matched = False

        for topic, patterns in topic_patterns.items():
            if any(pattern in keyword_lower for pattern in patterns):
                clusters[topic]['keywords'].append(kw)
                clusters[topic]['topic'] = topic
                matched = True
                break

        if not matched:
            uncategorized.append(kw)

    # Group uncategorized by common words
    if uncategorized:
        clusters['Other/General']['keywords'] = uncategorized
        clusters['Other/General']['topic'] = 'Other/General'

    # Convert to indexed dict
    return {i: data for i, data in enumerate(clusters.values())}


def extract_topic_name(keywords: List[str]) -> str:
    """Extract topic name from list of keywords"""
    # Get most common words (excluding stop words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'how', 'what', 'best', 'top', 'is', 'are', 'of', 'with'}

    words = []
    for keyword in keywords:
        for word in keyword.lower().split():
            if word not in stop_words and len(word) > 3:
                words.append(word)

    # Get most common words
    if words:
        common_words = Counter(words).most_common(3)
        topic_words = [word for word, count in common_words if count > 1]
        if topic_words:
            return ' '.join(topic_words[:2]).title()

    # Fallback: use first keyword
    return keywords[0] if keywords else 'Unknown Topic'


def calculate_authority_score(
    keyword_count: int,
    avg_position: float,
    total_impressions: int
) -> int:
    """Calculate topical authority score (0-100)"""

    # Score components
    # 1. Coverage (50%): How many keywords you rank for
    if keyword_count >= 50:
        coverage_score = 100
    elif keyword_count >= 30:
        coverage_score = 80
    elif keyword_count >= 15:
        coverage_score = 60
    elif keyword_count >= 8:
        coverage_score = 40
    elif keyword_count >= 4:
        coverage_score = 20
    else:
        coverage_score = 10

    # 2. Position Quality (30%): How well you rank
    if avg_position <= 5:
        position_score = 100
    elif avg_position <= 10:
        position_score = 80
    elif avg_position <= 20:
        position_score = 60
    elif avg_position <= 30:
        position_score = 40
    elif avg_position <= 50:
        position_score = 20
    else:
        position_score = 10

    # 3. Demand (20%): Total search demand
    if total_impressions >= 10000:
        demand_score = 100
    elif total_impressions >= 5000:
        demand_score = 80
    elif total_impressions >= 2000:
        demand_score = 60
    elif total_impressions >= 1000:
        demand_score = 40
    elif total_impressions >= 500:
        demand_score = 20
    else:
        demand_score = 10

    # Weighted total
    final_score = (
        coverage_score * 0.50 +
        position_score * 0.30 +
        demand_score * 0.20
    )

    return int(final_score)


def get_authority_level(score: int) -> str:
    """Convert authority score to level"""
    if score >= 75:
        return 'Strong'
    elif score >= 50:
        return 'Moderate'
    elif score >= 25:
        return 'Weak'
    else:
        return 'Minimal'


def find_cluster_gaps(
    seed_keyword: str,
    cluster_keywords: List[Dict],
    dfs: DataForSEO,
    limit: int = 20
) -> List[Dict]:
    """Find related keywords in this topic that we don't rank for"""

    try:
        # Get related keywords
        related = dfs.get_keyword_ideas(seed_keyword, limit=100)

        if not related:
            return []

        # Get set of keywords we already rank for in this cluster
        ranking_keywords = {kw['keyword'].lower().strip() for kw in cluster_keywords}

        # Find gaps
        gaps = []
        for related_kw in related:
            kw_lower = related_kw['keyword'].lower().strip()

            if kw_lower not in ranking_keywords:
                gaps.append({
                    'keyword': related_kw['keyword'],
                    'search_volume': related_kw.get('search_volume', 0),
                    'difficulty': related_kw.get('difficulty', 50)
                })

        # Sort by search volume
        gaps.sort(key=lambda x: x.get('search_volume', 0), reverse=True)

        return gaps[:limit]

    except Exception as e:
        return []


def write_markdown_report(clusters: List[Dict]):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/topic-clusters-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Topic Cluster Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Strategy:** Build topical authority by identifying and filling cluster gaps\n\n")
        f.write(f"**Total Topics:** {len(clusters)}\n\n")
        f.write("---\n\n")

        # Summary by authority level
        strong = [c for c in clusters if c['authority_level'] == 'Strong']
        moderate = [c for c in clusters if c['authority_level'] == 'Moderate']
        weak = [c for c in clusters if c['authority_level'] == 'Weak']
        minimal = [c for c in clusters if c['authority_level'] == 'Minimal']

        f.write(f"## Authority Distribution\n\n")
        f.write(f"| Level | Count | Strategy |\n")
        f.write(f"|-------|-------|----------|\n")
        f.write(f"| ⭐ Strong | {len(strong)} | Maintain and expand |\n")
        f.write(f"| ✅ Moderate | {len(moderate)} | Strengthen coverage |\n")
        f.write(f"| ⚠️ Weak | {len(weak)} | Build comprehensive cluster |\n")
        f.write(f"| 🔴 Minimal | {len(minimal)} | Major opportunity or ignore |\n\n")

        # Weak clusters (opportunities)
        f.write(f"## 🎯 WEAK AUTHORITY TOPICS (Build These!)\n\n")
        f.write(f"These topics have demand but you lack comprehensive coverage. Build topic clusters here.\n\n")

        weak_and_minimal = weak + minimal
        # Sort by total impressions (demand)
        weak_sorted = sorted(weak_and_minimal, key=lambda x: x['total_impressions'], reverse=True)

        for i, cluster in enumerate(weak_sorted[:15], 1):
            f.write(f"### {i}. {cluster['topic']}\n\n")
            f.write(f"- **Authority Score:** {cluster['authority_score']}/100 ({cluster['authority_level']})\n")
            f.write(f"- **Keywords Ranking:** {cluster['keyword_count']}\n")
            f.write(f"- **Average Position:** {cluster['avg_position']}\n")
            f.write(f"- **Total Impressions:** {cluster['total_impressions']:,}/month\n")
            f.write(f"- **Total Clicks:** {cluster['total_clicks']}/month\n\n")

            f.write(f"**Current Top Keywords:**\n")
            for kw in cluster['top_keywords'][:5]:
                f.write(f"- {kw['keyword']} (position {kw['position']:.1f}, {kw['impressions']:,} impressions)\n")
            f.write(f"\n")

            if cluster['coverage_gaps']:
                f.write(f"**Coverage Gaps** ({len(cluster['coverage_gaps'])} opportunities):\n")
                for gap in cluster['coverage_gaps'][:8]:
                    vol = gap.get('search_volume', 'Unknown')
                    diff = gap.get('difficulty', 'Unknown')
                    f.write(f"- {gap['keyword']} - Volume: {vol}, Difficulty: {diff}\n")
                f.write(f"\n")

            f.write(f"**Recommended Action:**\n")
            if cluster['keyword_count'] < 5:
                f.write(f"- Create 8-12 comprehensive articles covering this topic cluster\n")
                f.write(f"- Build pillar page linking to all cluster content\n")
                f.write(f"- Target the coverage gaps identified above\n")
            else:
                f.write(f"- Expand existing content to cover identified gaps\n")
                f.write(f"- Improve rankings for current keywords (avg position {cluster['avg_position']})\n")
                f.write(f"- Create pillar page if you don't have one\n")

            f.write(f"\n---\n\n")

        # Strong clusters
        f.write(f"## ⭐ STRONG AUTHORITY TOPICS (Maintain These!)\n\n")
        f.write(f"These topics are your strengths. Keep content updated and expand strategically.\n\n")

        strong_sorted = sorted(strong, key=lambda x: x['authority_score'], reverse=True)

        for i, cluster in enumerate(strong_sorted[:10], 1):
            f.write(f"### {i}. {cluster['topic']}\n\n")
            f.write(f"- **Authority Score:** {cluster['authority_score']}/100 ({cluster['authority_level']})\n")
            f.write(f"- **Keywords Ranking:** {cluster['keyword_count']}\n")
            f.write(f"- **Average Position:** {cluster['avg_position']}\n")
            f.write(f"- **Total Clicks:** {cluster['total_clicks']:,}/month\n\n")

            f.write(f"**Top Performing Keywords:**\n")
            for kw in cluster['top_keywords'][:5]:
                f.write(f"- {kw['keyword']} (position {kw['position']:.1f}, {kw['clicks']} clicks/mo)\n")
            f.write(f"\n")

            if cluster['coverage_gaps']:
                f.write(f"**Expansion Opportunities:**\n")
                for gap in cluster['coverage_gaps'][:5]:
                    vol = gap.get('search_volume', 'Unknown')
                    f.write(f"- {gap['keyword']} ({vol} searches/mo)\n")
                f.write(f"\n")

            f.write(f"**Recommended Action:**\n")
            f.write(f"- Keep content fresh with regular updates\n")
            f.write(f"- Expand to cover expansion opportunities\n")
            f.write(f"- Build supporting cluster content\n")
            f.write(f"- Consider creating advanced/niche content in this area\n\n")

            f.write(f"---\n\n")

        # Moderate clusters
        if moderate:
            f.write(f"## ✅ MODERATE AUTHORITY TOPICS\n\n")

            moderate_sorted = sorted(moderate, key=lambda x: x['total_impressions'], reverse=True)

            for cluster in moderate_sorted[:10]:
                f.write(f"### {cluster['topic']}\n\n")
                f.write(f"- Authority Score: {cluster['authority_score']}/100\n")
                f.write(f"- Keywords: {cluster['keyword_count']} | Avg Position: {cluster['avg_position']} | Clicks: {cluster['total_clicks']}/mo\n")
                f.write(f"- **Action:** Strengthen with 3-5 more articles to build strong authority\n\n")

        # Strategy recommendations
        f.write(f"## Strategy Recommendations\n\n")

        f.write(f"### Priority 1: Build Weak Clusters\n\n")
        f.write(f"Focus on weak clusters with high demand (impressions):\n\n")

        top_weak = sorted(weak_sorted, key=lambda x: x['total_impressions'], reverse=True)[:5]
        for i, cluster in enumerate(top_weak, 1):
            f.write(f"{i}. **{cluster['topic']}** - {cluster['total_impressions']:,} impressions/mo, {cluster['keyword_count']} keywords\n")
            f.write(f"   - Create {max(8, 15 - cluster['keyword_count'])} new articles\n")
            f.write(f"   - Target identified coverage gaps\n\n")

        f.write(f"### Priority 2: Maintain Strong Clusters\n\n")
        f.write(f"Keep your strong topics fresh and expand:\n\n")

        for i, cluster in enumerate(strong_sorted[:3], 1):
            f.write(f"{i}. **{cluster['topic']}** - {cluster['total_clicks']:,} clicks/mo\n")
            f.write(f"   - Regular content updates\n")
            f.write(f"   - Expand with advanced topics\n\n")

        f.write(f"### Priority 3: Improve Moderate Clusters\n\n")
        f.write(f"Strengthen moderate topics to strong authority:\n\n")

        for i, cluster in enumerate(moderate_sorted[:3], 1):
            f.write(f"{i}. **{cluster['topic']}**\n")
            f.write(f"   - Add 3-5 comprehensive articles\n")
            f.write(f"   - Improve rankings for existing content\n\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()
