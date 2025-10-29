"""
Keyword Analyzer

Calculates keyword density, analyzes distribution, and performs semantic clustering
to identify keyword usage patterns and topic clusters within content.
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class KeywordAnalyzer:
    """Analyzes keyword density, distribution, and clustering in content"""

    def __init__(self):
        self.stop_words = set([
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'you', 'your', 'this', 'their', 'but',
            'or', 'not', 'can', 'have', 'all', 'when', 'there', 'been', 'if',
            'more', 'so', 'about', 'what', 'which', 'who', 'would', 'could'
        ])

    def analyze(
        self,
        content: str,
        primary_keyword: str,
        secondary_keywords: Optional[List[str]] = None,
        target_density: float = 1.5
    ) -> Dict[str, Any]:
        """
        Comprehensive keyword analysis

        Args:
            content: Article content to analyze
            primary_keyword: Main target keyword
            secondary_keywords: List of secondary keywords
            target_density: Target keyword density percentage (default 1.5%)

        Returns:
            Dict with density metrics, distribution map, and recommendations
        """
        secondary_keywords = secondary_keywords or []

        # Clean and prepare content
        word_count = len(content.split())
        sections = self._extract_sections(content)

        # Analyze primary keyword
        primary_analysis = self._analyze_keyword(
            content,
            primary_keyword,
            word_count,
            sections,
            target_density
        )

        # Analyze secondary keywords
        secondary_analysis = []
        for keyword in secondary_keywords:
            analysis = self._analyze_keyword(
                content,
                keyword,
                word_count,
                sections,
                target_density * 0.5  # Lower target for secondary
            )
            secondary_analysis.append(analysis)

        # Detect keyword stuffing
        stuffing_risk = self._detect_keyword_stuffing(
            content,
            primary_keyword,
            primary_analysis['density']
        )

        # Perform topic clustering
        clusters = self._perform_clustering(content, sections)

        # Distribution heatmap
        heatmap = self._create_distribution_heatmap(
            primary_keyword,
            sections
        )

        # LSI/semantic keyword suggestions
        lsi_keywords = self._find_lsi_keywords(content, primary_keyword)

        return {
            'word_count': word_count,
            'primary_keyword': {
                'keyword': primary_keyword,
                **primary_analysis
            },
            'secondary_keywords': secondary_analysis,
            'keyword_stuffing': stuffing_risk,
            'topic_clusters': clusters,
            'distribution_heatmap': heatmap,
            'lsi_keywords': lsi_keywords,
            'recommendations': self._generate_recommendations(
                primary_analysis,
                secondary_analysis,
                stuffing_risk,
                target_density
            )
        }

    def _analyze_keyword(
        self,
        content: str,
        keyword: str,
        word_count: int,
        sections: List[Dict],
        target_density: float
    ) -> Dict[str, Any]:
        """Analyze a single keyword"""
        content_lower = content.lower()
        keyword_lower = keyword.lower()

        # Count exact matches
        exact_count = content_lower.count(keyword_lower)

        # Count variations (word order doesn't matter for multi-word keywords)
        variation_count = 0
        keyword_words = keyword_lower.split()
        if len(keyword_words) > 1:
            # Look for variations like "podcast hosting" -> "hosting podcast" or "hosting your podcast"
            variation_pattern = r'\b(?:' + '|'.join(keyword_words) + r')\b'
            matches = re.finditer(variation_pattern, content_lower)
            variation_count = len(list(matches)) - (exact_count * len(keyword_words))

        total_count = exact_count + (variation_count // len(keyword_words) if len(keyword_words) > 1 else 0)

        # Calculate density
        density = (total_count / word_count * 100) if word_count > 0 else 0

        # Find positions
        positions = self._find_keyword_positions(content, keyword)

        # Check critical placements
        critical_placements = self._check_critical_placements(
            content,
            sections,
            keyword
        )

        # Distribution across sections
        section_distribution = self._analyze_section_distribution(
            sections,
            keyword
        )

        return {
            'exact_matches': exact_count,
            'total_occurrences': total_count,
            'density': round(density, 2),
            'target_density': target_density,
            'density_status': self._get_density_status(density, target_density),
            'positions': positions,
            'critical_placements': critical_placements,
            'section_distribution': section_distribution
        }

    def _extract_sections(self, content: str) -> List[Dict]:
        """Extract sections with headers from content"""
        sections = []

        # Split by headers (H1, H2, H3)
        lines = content.split('\n')
        current_section = {'type': 'intro', 'header': '', 'content': '', 'start_pos': 0}
        current_pos = 0

        for line in lines:
            # Check for markdown headers
            h1_match = re.match(r'^#\s+(.+)$', line)
            h2_match = re.match(r'^##\s+(.+)$', line)
            h3_match = re.match(r'^###\s+(.+)$', line)

            if h1_match or h2_match or h3_match:
                # Save previous section
                if current_section['content']:
                    current_section['end_pos'] = current_pos
                    sections.append(current_section.copy())

                # Start new section
                if h1_match:
                    header = h1_match.group(1)
                    header_type = 'h1'
                elif h2_match:
                    header = h2_match.group(1)
                    header_type = 'h2'
                else:
                    header = h3_match.group(1)
                    header_type = 'h3'

                current_section = {
                    'type': header_type,
                    'header': header,
                    'content': '',
                    'start_pos': current_pos
                }
            else:
                current_section['content'] += line + '\n'

            current_pos += len(line) + 1

        # Add last section
        if current_section['content']:
            current_section['end_pos'] = current_pos
            sections.append(current_section)

        return sections

    def _find_keyword_positions(self, content: str, keyword: str) -> List[int]:
        """Find all positions where keyword appears"""
        positions = []
        content_lower = content.lower()
        keyword_lower = keyword.lower()

        start = 0
        while True:
            pos = content_lower.find(keyword_lower, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        return positions

    def _check_critical_placements(
        self,
        content: str,
        sections: List[Dict],
        keyword: str
    ) -> Dict[str, bool]:
        """Check if keyword appears in critical locations"""
        content_lower = content.lower()
        keyword_lower = keyword.lower()

        # First 100 words
        first_100 = ' '.join(content.split()[:100]).lower()
        in_first_100 = keyword_lower in first_100

        # Last paragraph (conclusion)
        last_para = content.split('\n\n')[-1].lower() if '\n\n' in content else content[-500:].lower()
        in_conclusion = keyword_lower in last_para

        # H1 (first heading)
        in_h1 = False
        if sections and sections[0].get('header'):
            in_h1 = keyword_lower in sections[0]['header'].lower()

        # H2 headings
        h2_count = 0
        h2_with_keyword = 0
        for section in sections:
            if section['type'] == 'h2':
                h2_count += 1
                if keyword_lower in section['header'].lower():
                    h2_with_keyword += 1

        return {
            'in_first_100_words': in_first_100,
            'in_conclusion': in_conclusion,
            'in_h1': in_h1,
            'in_h2_headings': f"{h2_with_keyword}/{h2_count}" if h2_count > 0 else "0/0",
            'h2_keyword_ratio': (h2_with_keyword / h2_count) if h2_count > 0 else 0
        }

    def _analyze_section_distribution(
        self,
        sections: List[Dict],
        keyword: str
    ) -> List[Dict]:
        """Analyze how keyword is distributed across sections"""
        keyword_lower = keyword.lower()
        distribution = []

        for i, section in enumerate(sections):
            section_text = (section['header'] + ' ' + section['content']).lower()
            count = section_text.count(keyword_lower)
            word_count = len(section_text.split())

            distribution.append({
                'section_index': i,
                'section_type': section['type'],
                'header': section['header'][:50],  # Truncate long headers
                'keyword_count': count,
                'word_count': word_count,
                'density': round((count / word_count * 100) if word_count > 0 else 0, 2)
            })

        return distribution

    def _get_density_status(self, actual: float, target: float) -> str:
        """Determine if density is appropriate"""
        if actual < target * 0.5:
            return "too_low"
        elif actual < target * 0.8:
            return "slightly_low"
        elif actual <= target * 1.2:
            return "optimal"
        elif actual <= target * 1.5:
            return "slightly_high"
        else:
            return "too_high"

    def _detect_keyword_stuffing(
        self,
        content: str,
        keyword: str,
        density: float
    ) -> Dict[str, Any]:
        """Detect potential keyword stuffing"""
        keyword_lower = keyword.lower()
        risk_level = "none"
        warnings = []

        # High density check
        if density > 3.0:
            risk_level = "high"
            warnings.append(f"Keyword density {density}% is very high (over 3%)")
        elif density > 2.5:
            risk_level = "medium"
            warnings.append(f"Keyword density {density}% is high (over 2.5%)")

        # Check for keyword clustering (multiple instances in same paragraph)
        paragraphs = content.split('\n\n')
        for i, para in enumerate(paragraphs):
            count = para.lower().count(keyword_lower)
            words = len(para.split())
            if words > 0:
                para_density = (count / words * 100)
                if para_density > 5:
                    risk_level = "high" if risk_level == "medium" else risk_level
                    warnings.append(f"Paragraph {i+1} has very high keyword density ({para_density:.1f}%)")

        # Check for unnatural repetition (keyword appears in consecutive sentences)
        sentences = re.split(r'[.!?]+', content)
        consecutive = 0
        max_consecutive = 0
        for sentence in sentences:
            if keyword_lower in sentence.lower():
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        if max_consecutive >= 5:
            risk_level = "high"
            warnings.append(f"Keyword appears in {max_consecutive} consecutive sentences")
        elif max_consecutive >= 3:
            if risk_level == "none":
                risk_level = "low"
            warnings.append(f"Keyword appears in {max_consecutive} consecutive sentences")

        return {
            'risk_level': risk_level,
            'warnings': warnings,
            'safe': risk_level in ["none", "low"]
        }

    def _perform_clustering(self, content: str, sections: List[Dict]) -> Dict[str, Any]:
        """Perform topic clustering to identify content themes"""
        try:
            # Prepare section texts
            section_texts = []
            for section in sections:
                text = section['header'] + ' ' + section['content']
                if len(text.split()) > 10:  # Only include substantial sections
                    section_texts.append(text)

            if len(section_texts) < 3:
                return {
                    'clusters_found': 0,
                    'note': 'Insufficient sections for clustering'
                }

            # Use TF-IDF to vectorize
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = vectorizer.fit_transform(section_texts)

            # Determine optimal number of clusters (max 5 or len/2)
            n_clusters = min(5, max(2, len(section_texts) // 2))

            # Perform k-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)

            # Get top terms per cluster
            feature_names = vectorizer.get_feature_names_out()
            clusters = []

            for i in range(n_clusters):
                cluster_center = kmeans.cluster_centers_[i]
                top_indices = cluster_center.argsort()[-5:][::-1]
                top_terms = [feature_names[idx] for idx in top_indices]

                sections_in_cluster = [j for j, label in enumerate(cluster_labels) if label == i]

                clusters.append({
                    'cluster_id': i,
                    'top_terms': top_terms,
                    'section_count': len(sections_in_cluster),
                    'sections': sections_in_cluster
                })

            return {
                'clusters_found': n_clusters,
                'clusters': clusters
            }
        except Exception as e:
            return {
                'clusters_found': 0,
                'error': str(e)
            }

    def _create_distribution_heatmap(
        self,
        keyword: str,
        sections: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Create a visual representation of keyword distribution"""
        keyword_lower = keyword.lower()
        heatmap = []

        for i, section in enumerate(sections):
            section_text = (section['header'] + ' ' + section['content']).lower()
            count = section_text.count(keyword_lower)
            word_count = len(section_text.split())

            # Calculate heat level (0-5)
            density = (count / word_count * 100) if word_count > 0 else 0
            if density == 0:
                heat = 0
            elif density < 0.5:
                heat = 1
            elif density < 1.0:
                heat = 2
            elif density < 2.0:
                heat = 3
            elif density < 3.0:
                heat = 4
            else:
                heat = 5

            heatmap.append({
                'section': section['header'][:40] or f"Section {i+1}",
                'keyword_count': count,
                'heat_level': heat,
                'density': round(density, 2)
            })

        return heatmap

    def _find_lsi_keywords(self, content: str, primary_keyword: str) -> List[str]:
        """Find LSI (Latent Semantic Indexing) keywords - semantically related terms"""
        try:
            # Extract common phrases and terms
            words = re.findall(r'\b[a-z]{4,}\b', content.lower())
            word_freq = Counter(words)

            # Remove stop words
            filtered_words = {
                word: freq for word, freq in word_freq.items()
                if word not in self.stop_words and word not in primary_keyword.lower().split()
            }

            # Get top terms
            top_terms = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20]

            # Extract bigrams and trigrams
            content_lower = content.lower()
            sentences = re.split(r'[.!?]+', content_lower)

            phrases = []
            for sentence in sentences:
                words = sentence.split()
                # Bigrams
                for i in range(len(words) - 1):
                    phrase = f"{words[i]} {words[i+1]}"
                    if len(phrase) > 8 and not any(sw in phrase.split() for sw in self.stop_words):
                        phrases.append(phrase)
                # Trigrams
                for i in range(len(words) - 2):
                    phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                    if len(phrase) > 12 and not any(sw in phrase.split() for sw in self.stop_words):
                        phrases.append(phrase)

            phrase_freq = Counter(phrases)
            top_phrases = sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)[:10]

            # Combine and return
            lsi_keywords = []
            lsi_keywords.extend([word for word, _ in top_terms[:10]])
            lsi_keywords.extend([phrase for phrase, _ in top_phrases[:5]])

            return lsi_keywords[:15]

        except Exception as e:
            return []

    def _generate_recommendations(
        self,
        primary_analysis: Dict,
        secondary_analysis: List[Dict],
        stuffing_risk: Dict,
        target_density: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Primary keyword density
        status = primary_analysis['density_status']
        if status == "too_low":
            recommendations.append(
                f"⚠️ Primary keyword density is too low ({primary_analysis['density']}%). "
                f"Target is {target_density}%. Add {primary_analysis['keyword']} naturally in more paragraphs."
            )
        elif status == "slightly_low":
            recommendations.append(
                f"ℹ️ Primary keyword density is slightly low ({primary_analysis['density']}%). "
                f"Consider adding a few more mentions of '{primary_analysis['keyword']}'."
            )
        elif status == "too_high":
            recommendations.append(
                f"⚠️ Primary keyword density is too high ({primary_analysis['density']}%). "
                f"This may trigger keyword stuffing penalties. Remove some instances or replace with variations."
            )
        elif status == "slightly_high":
            recommendations.append(
                f"ℹ️ Primary keyword density is slightly high ({primary_analysis['density']}%). "
                f"Consider using more keyword variations or synonyms."
            )

        # Critical placements
        placements = primary_analysis['critical_placements']
        if not placements['in_first_100_words']:
            recommendations.append("⚠️ Primary keyword missing from first 100 words - add it to the introduction")

        if not placements['in_h1']:
            recommendations.append("⚠️ Primary keyword missing from H1 headline - include it in the title")

        if placements['h2_keyword_ratio'] < 0.33:  # Less than 1/3 of H2s
            recommendations.append(
                f"ℹ️ Primary keyword appears in only {placements['in_h2_headings']} H2 headings. "
                "Aim for 2-3 H2s with keyword variations."
            )

        if not placements['in_conclusion']:
            recommendations.append("ℹ️ Consider mentioning primary keyword in the conclusion for better optimization")

        # Keyword stuffing
        if not stuffing_risk['safe']:
            recommendations.append(
                f"⚠️ KEYWORD STUFFING RISK: {stuffing_risk['risk_level'].upper()} - "
                + '; '.join(stuffing_risk['warnings'])
            )

        # Secondary keywords
        for analysis in secondary_analysis:
            if analysis['total_occurrences'] == 0:
                recommendations.append(
                    f"ℹ️ Secondary keyword '{analysis['keyword']}' not found in content - consider adding it"
                )

        return recommendations


# Convenience function
def analyze_keywords(
    content: str,
    primary_keyword: str,
    secondary_keywords: Optional[List[str]] = None,
    target_density: float = 1.5
) -> Dict[str, Any]:
    """
    Analyze keyword usage in content

    Args:
        content: Article text
        primary_keyword: Main target keyword
        secondary_keywords: List of secondary keywords
        target_density: Target density percentage

    Returns:
        Comprehensive keyword analysis
    """
    analyzer = KeywordAnalyzer()
    return analyzer.analyze(content, primary_keyword, secondary_keywords, target_density)


# Example usage
if __name__ == "__main__":
    sample_content = """
# How to Start a Podcast: Complete Guide

Starting a podcast has never been easier. In this guide, you'll learn how to start a podcast from scratch.

## Choosing Your Podcast Topic

When you start a podcast, the first step is choosing your topic. Your podcast topic should be something you're passionate about.

## Getting Podcast Equipment

To start a podcast, you need basic equipment. A good microphone is essential for podcast recording.

## Podcast Hosting Platforms

Podcast hosting is crucial. Choose a reliable podcast hosting platform for your show.
    """

    result = analyze_keywords(
        sample_content,
        "start a podcast",
        ["podcast hosting", "podcast equipment", "podcast recording"],
        target_density=1.5
    )

    print("=== Keyword Analysis ===")
    print(f"\nWord Count: {result['word_count']}")
    print(f"\nPrimary Keyword: {result['primary_keyword']['keyword']}")
    print(f"Density: {result['primary_keyword']['density']}%")
    print(f"Status: {result['primary_keyword']['density_status']}")
    print(f"\nCritical Placements:")
    for key, value in result['primary_keyword']['critical_placements'].items():
        print(f"  {key}: {value}")

    print(f"\nKeyword Stuffing Risk: {result['keyword_stuffing']['risk_level']}")
    if result['keyword_stuffing']['warnings']:
        print("Warnings:")
        for warning in result['keyword_stuffing']['warnings']:
            print(f"  - {warning}")

    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
