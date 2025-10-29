"""
Search Intent Analyzer

Determines the search intent of a query by analyzing SERP features and content patterns.
Classifies queries as: Informational, Navigational, Transactional, or Commercial Investigation.
"""

import re
from typing import Dict, List, Optional, Any
from enum import Enum


class SearchIntent(Enum):
    """Search intent types"""
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial_investigation"


class SearchIntentAnalyzer:
    """Analyzes search intent from keywords and SERP data"""

    # Intent signal keywords
    INFORMATIONAL_SIGNALS = [
        'what', 'why', 'how', 'when', 'where', 'who', 'guide', 'tutorial',
        'learn', 'tips', 'best practices', 'explained', 'definition', 'meaning'
    ]

    NAVIGATIONAL_SIGNALS = [
        'login', 'sign in', 'website', 'official', 'home page', 'account',
        'dashboard', 'portal', 'app'
    ]

    TRANSACTIONAL_SIGNALS = [
        'buy', 'purchase', 'order', 'download', 'get', 'pricing', 'cost',
        'free trial', 'sign up', 'subscribe', 'install', 'coupon', 'deal',
        'discount', 'cheap', 'affordable'
    ]

    COMMERCIAL_SIGNALS = [
        'best', 'top', 'review', 'vs', 'versus', 'compare', 'comparison',
        'alternative', 'alternatives', 'like', 'similar', 'better than',
        'instead of', 'or', 'option', 'choice'
    ]

    # SERP features that indicate intent
    SERP_INTENT_MAPPING = {
        'featured_snippet': SearchIntent.INFORMATIONAL,
        'knowledge_graph': SearchIntent.INFORMATIONAL,
        'people_also_ask': SearchIntent.INFORMATIONAL,
        'shopping_results': SearchIntent.TRANSACTIONAL,
        'local_pack': SearchIntent.TRANSACTIONAL,
        'ads': SearchIntent.TRANSACTIONAL,
        'video': SearchIntent.INFORMATIONAL,
        'images': SearchIntent.INFORMATIONAL,
        'top_stories': SearchIntent.INFORMATIONAL,
        'carousel': SearchIntent.COMMERCIAL,
    }

    def analyze(
        self,
        keyword: str,
        serp_features: Optional[List[str]] = None,
        top_results: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze search intent of a keyword

        Args:
            keyword: The search query to analyze
            serp_features: List of SERP features present (from DataForSEO)
            top_results: Top ranking pages with titles/descriptions

        Returns:
            Dict with intent classification and confidence scores
        """
        keyword_lower = keyword.lower()

        # Calculate intent scores
        scores = {
            SearchIntent.INFORMATIONAL: 0,
            SearchIntent.NAVIGATIONAL: 0,
            SearchIntent.TRANSACTIONAL: 0,
            SearchIntent.COMMERCIAL: 0
        }

        # Score from keyword patterns
        keyword_scores = self._analyze_keyword_patterns(keyword_lower)
        for intent, score in keyword_scores.items():
            scores[intent] += score

        # Score from SERP features
        if serp_features:
            serp_scores = self._analyze_serp_features(serp_features)
            for intent, score in serp_scores.items():
                scores[intent] += score

        # Score from top results content
        if top_results:
            content_scores = self._analyze_content_patterns(top_results)
            for intent, score in content_scores.items():
                scores[intent] += score

        # Normalize scores to percentages
        total = sum(scores.values())
        if total > 0:
            confidence = {intent.value: (score / total * 100) for intent, score in scores.items()}
        else:
            confidence = {intent.value: 25 for intent in SearchIntent}

        # Primary intent is highest scoring
        primary_intent = max(scores.items(), key=lambda x: x[1])[0]

        # Secondary intent if within 15% of primary
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        secondary_intent = None
        if len(sorted_scores) > 1:
            primary_pct = confidence[sorted_scores[0][0].value]
            secondary_pct = confidence[sorted_scores[1][0].value]
            if primary_pct - secondary_pct < 15:
                secondary_intent = sorted_scores[1][0]

        return {
            'keyword': keyword,
            'primary_intent': primary_intent.value,
            'secondary_intent': secondary_intent.value if secondary_intent else None,
            'confidence': confidence,
            'signals_detected': self._get_detected_signals(keyword_lower, serp_features),
            'recommendations': self._get_recommendations(primary_intent, secondary_intent)
        }

    def _analyze_keyword_patterns(self, keyword: str) -> Dict[SearchIntent, float]:
        """Score keyword based on pattern matching"""
        scores = {intent: 0 for intent in SearchIntent}

        # Check for signal words
        for signal in self.INFORMATIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.INFORMATIONAL] += 2

        for signal in self.NAVIGATIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.NAVIGATIONAL] += 3

        for signal in self.TRANSACTIONAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.TRANSACTIONAL] += 2

        for signal in self.COMMERCIAL_SIGNALS:
            if signal in keyword:
                scores[SearchIntent.COMMERCIAL] += 2

        # Pattern-based scoring
        # Questions are typically informational
        if re.match(r'^(what|why|how|when|where|who|can|should|is|are|does)', keyword):
            scores[SearchIntent.INFORMATIONAL] += 3

        # Brand + generic term = navigational
        if len(keyword.split()) == 2:
            scores[SearchIntent.NAVIGATIONAL] += 1

        # Lists and comparisons = commercial
        if re.search(r'\d+\s+(best|top)', keyword):
            scores[SearchIntent.COMMERCIAL] += 3

        return scores

    def _analyze_serp_features(self, features: List[str]) -> Dict[SearchIntent, float]:
        """Score based on SERP features present"""
        scores = {intent: 0 for intent in SearchIntent}

        for feature in features:
            feature_lower = feature.lower()

            # Map SERP features to intents
            if 'snippet' in feature_lower or 'featured' in feature_lower:
                scores[SearchIntent.INFORMATIONAL] += 2

            if 'knowledge' in feature_lower or 'people_also_ask' in feature_lower:
                scores[SearchIntent.INFORMATIONAL] += 2

            if 'shopping' in feature_lower or 'product' in feature_lower:
                scores[SearchIntent.TRANSACTIONAL] += 3

            if 'ad' in feature_lower:
                scores[SearchIntent.TRANSACTIONAL] += 1

            if 'local' in feature_lower or 'map' in feature_lower:
                scores[SearchIntent.TRANSACTIONAL] += 2

            if 'video' in feature_lower:
                scores[SearchIntent.INFORMATIONAL] += 1

            if 'carousel' in feature_lower:
                scores[SearchIntent.COMMERCIAL] += 1

        return scores

    def _analyze_content_patterns(self, results: List[Dict[str, str]]) -> Dict[SearchIntent, float]:
        """Score based on top ranking content patterns"""
        scores = {intent: 0 for intent in SearchIntent}

        for result in results[:10]:  # Analyze top 10
            title = result.get('title', '').lower()
            description = result.get('description', '').lower()
            url = result.get('url', '').lower()

            combined = f"{title} {description}"

            # Informational indicators
            if any(word in combined for word in ['guide', 'how to', 'what is', 'tutorial', 'tips']):
                scores[SearchIntent.INFORMATIONAL] += 0.5

            # Commercial indicators
            if any(word in combined for word in ['best', 'top', 'review', 'vs', 'compare']):
                scores[SearchIntent.COMMERCIAL] += 0.5

            # Transactional indicators
            if any(word in combined for word in ['buy', 'price', 'shop', 'order', 'get']):
                scores[SearchIntent.TRANSACTIONAL] += 0.5

            # Product/checkout pages in URLs
            if any(word in url for word in ['/product/', '/pricing', '/buy', '/shop', '/checkout']):
                scores[SearchIntent.TRANSACTIONAL] += 0.5

        return scores

    def _get_detected_signals(
        self,
        keyword: str,
        serp_features: Optional[List[str]]
    ) -> Dict[str, List[str]]:
        """Get list of signals detected for each intent"""
        signals = {
            'informational': [],
            'navigational': [],
            'transactional': [],
            'commercial': []
        }

        # Keyword signals
        for signal in self.INFORMATIONAL_SIGNALS:
            if signal in keyword:
                signals['informational'].append(f"Keyword contains '{signal}'")

        for signal in self.NAVIGATIONAL_SIGNALS:
            if signal in keyword:
                signals['navigational'].append(f"Keyword contains '{signal}'")

        for signal in self.TRANSACTIONAL_SIGNALS:
            if signal in keyword:
                signals['transactional'].append(f"Keyword contains '{signal}'")

        for signal in self.COMMERCIAL_SIGNALS:
            if signal in keyword:
                signals['commercial'].append(f"Keyword contains '{signal}'")

        # SERP feature signals
        if serp_features:
            for feature in serp_features:
                if 'snippet' in feature.lower() or 'knowledge' in feature.lower():
                    signals['informational'].append(f"SERP has {feature}")
                if 'shopping' in feature.lower() or 'ad' in feature.lower():
                    signals['transactional'].append(f"SERP has {feature}")

        return {k: v for k, v in signals.items() if v}  # Remove empty lists

    def _get_recommendations(
        self,
        primary: SearchIntent,
        secondary: Optional[SearchIntent]
    ) -> List[str]:
        """Get content recommendations based on intent"""
        recommendations = []

        if primary == SearchIntent.INFORMATIONAL:
            recommendations.extend([
                "Create comprehensive, educational content",
                "Include step-by-step instructions or explanations",
                "Answer common questions (People Also Ask)",
                "Use FAQ sections and definition boxes",
                "Target featured snippet optimization",
                "Include videos, images, and visual aids"
            ])

        elif primary == SearchIntent.NAVIGATIONAL:
            recommendations.extend([
                "Optimize for brand-related searches",
                "Ensure homepage/key pages rank well",
                "Include site navigation and clear CTAs",
                "Strengthen brand presence and awareness",
                "May not need traditional content marketing"
            ])

        elif primary == SearchIntent.TRANSACTIONAL:
            recommendations.extend([
                "Focus on product/service pages",
                "Include clear pricing and purchase options",
                "Add trust signals (reviews, testimonials)",
                "Optimize for conversion, not just traffic",
                "Include strong, action-oriented CTAs",
                "Consider local SEO if applicable"
            ])

        elif primary == SearchIntent.COMMERCIAL:
            recommendations.extend([
                "Create comparison and review content",
                "Include pros/cons and alternatives",
                "Add detailed feature breakdowns",
                "Include data tables and comparisons",
                "Show 'best for' categories",
                "Help users make informed decisions"
            ])

        if secondary:
            recommendations.append(f"\nNote: Secondary intent is {secondary.value} - consider blending content approaches")

        return recommendations


# Convenience function
def analyze_intent(
    keyword: str,
    serp_features: Optional[List[str]] = None,
    top_results: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Analyze search intent for a keyword

    Args:
        keyword: Search query
        serp_features: SERP features from DataForSEO
        top_results: Top ranking pages

    Returns:
        Intent analysis with recommendations
    """
    analyzer = SearchIntentAnalyzer()
    return analyzer.analyze(keyword, serp_features, top_results)


# Example usage
if __name__ == "__main__":
    # Example 1: Informational query
    result1 = analyze_intent("how to start a podcast")
    print("Query:", result1['keyword'])
    print("Primary Intent:", result1['primary_intent'])
    print("Confidence:", result1['confidence'])
    print()

    # Example 2: Commercial query with SERP data
    result2 = analyze_intent(
        "best podcast hosting platforms",
        serp_features=['carousel', 'people_also_ask', 'video'],
        top_results=[
            {'title': 'Top 10 Podcast Hosting Platforms in 2024', 'description': 'Compare the best...'},
            {'title': 'Best Podcast Hosting Services: Review', 'description': 'Our expert review...'}
        ]
    )
    print("Query:", result2['keyword'])
    print("Primary Intent:", result2['primary_intent'])
    print("Confidence:", result2['confidence'])
    print("Recommendations:", result2['recommendations'][:3])
    print()

    # Example 3: Transactional query
    result3 = analyze_intent(
        "buy podcast microphone",
        serp_features=['shopping_results', 'ads', 'local_pack']
    )
    print("Query:", result3['keyword'])
    print("Primary Intent:", result3['primary_intent'])
    print("Confidence:", result3['confidence'])
