"""
Content Length Comparator

Fetches top SERP results for a keyword and analyzes their content length
to determine optimal word count for ranking competitively.
"""

import re
import requests
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
import statistics


class ContentLengthComparator:
    """Compares content length against top SERP competitors"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def analyze(
        self,
        keyword: str,
        your_word_count: Optional[int] = None,
        serp_results: Optional[List[Dict[str, str]]] = None,
        fetch_content: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze content length compared to SERP competitors

        Args:
            keyword: Search keyword to analyze
            your_word_count: Your content's word count
            serp_results: SERP results from DataForSEO (list of {'url', 'title', 'domain'})
            fetch_content: Whether to fetch and analyze competitor content

        Returns:
            Dict with length comparison, recommendations, and statistics
        """
        if not serp_results:
            return {
                'error': 'No SERP results provided',
                'recommendation': 'Use DataForSEO to get SERP data first'
            }

        # Analyze competitor content lengths
        competitor_lengths = []

        if fetch_content:
            for i, result in enumerate(serp_results[:10]):  # Top 10 only
                url = result.get('url')
                if url:
                    word_count = self._fetch_word_count(url)
                    if word_count:
                        competitor_lengths.append({
                            'position': i + 1,
                            'url': url,
                            'domain': result.get('domain', ''),
                            'title': result.get('title', '')[:100],
                            'word_count': word_count
                        })

        if not competitor_lengths:
            return {
                'error': 'Could not fetch competitor content',
                'recommendation': 'Manually check top ranking pages for word count'
            }

        # Calculate statistics
        counts = [comp['word_count'] for comp in competitor_lengths]
        stats = self._calculate_statistics(counts)

        # Determine recommended length
        recommendation = self._get_recommendation(
            stats,
            your_word_count
        )

        # Position your content
        your_position = self._get_position_in_range(
            your_word_count,
            competitor_lengths
        ) if your_word_count else None

        return {
            'keyword': keyword,
            'competitors_analyzed': len(competitor_lengths),
            'your_word_count': your_word_count,
            'statistics': stats,
            'competitor_lengths': competitor_lengths,
            'your_position': your_position,
            'recommendation': recommendation,
            'competitive_analysis': self._analyze_competition(
                your_word_count,
                competitor_lengths,
                stats
            )
        }

    def _fetch_word_count(self, url: str) -> Optional[int]:
        """Fetch and count words from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script, style, nav, footer, header elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            # Try to find main content area
            main_content = None
            for selector in ['article', 'main', '[role="main"]', '.content', '#content', '.post', '.entry-content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If no main content found, use body
            if not main_content:
                main_content = soup.find('body')

            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                # Clean and count words
                words = re.findall(r'\b[a-zA-Z]{2,}\b', text)
                return len(words)

        except Exception as e:
            # Silently fail for individual URLs
            pass

        return None

    def _calculate_statistics(self, counts: List[int]) -> Dict[str, Any]:
        """Calculate statistical measures"""
        if not counts:
            return {}

        return {
            'min': min(counts),
            'max': max(counts),
            'mean': round(statistics.mean(counts)),
            'median': round(statistics.median(counts)),
            'mode': round(statistics.mode(counts)) if len(counts) > 1 else counts[0],
            'std_dev': round(statistics.stdev(counts)) if len(counts) > 1 else 0,
            'percentile_25': round(statistics.quantiles(counts, n=4)[0]) if len(counts) > 3 else min(counts),
            'percentile_75': round(statistics.quantiles(counts, n=4)[2]) if len(counts) > 3 else max(counts)
        }

    def _get_recommendation(
        self,
        stats: Dict[str, Any],
        your_count: Optional[int]
    ) -> Dict[str, Any]:
        """Generate content length recommendation"""
        if not stats:
            return {'error': 'Insufficient data'}

        # Target: 75th percentile or median + 20%, whichever is higher
        target_median = stats['median']
        target_75th = stats['percentile_75']

        # Recommended range
        recommended_min = target_median
        recommended_optimal = max(target_75th, int(target_median * 1.2))
        recommended_max = int(recommended_optimal * 1.2)

        status = None
        message = None

        if your_count:
            if your_count < recommended_min * 0.8:
                status = "too_short"
                message = f"Your content is significantly shorter than competitors. Add {recommended_optimal - your_count} more words."
            elif your_count < recommended_min:
                status = "short"
                message = f"Your content is shorter than most competitors. Consider adding {recommended_optimal - your_count} more words."
            elif your_count < recommended_optimal:
                status = "good"
                message = f"Your content length is competitive. Add {recommended_optimal - your_count} more words to match top performers."
            elif your_count <= recommended_max:
                status = "optimal"
                message = "Your content length is optimal - matches or exceeds top competitors."
            else:
                status = "long"
                message = "Your content is longer than competitors. Ensure all content adds value."

        return {
            'recommended_min': recommended_min,
            'recommended_optimal': recommended_optimal,
            'recommended_max': recommended_max,
            'your_status': status,
            'message': message,
            'reasoning': f"Based on median ({target_median}) and 75th percentile ({target_75th}) of top 10 results"
        }

    def _get_position_in_range(
        self,
        your_count: int,
        competitors: List[Dict[str, Any]]
    ) -> str:
        """Determine where your content falls in the competitor range"""
        counts = [c['word_count'] for c in competitors]
        counts.sort()

        if your_count < counts[0]:
            return f"Below all competitors (shortest is {counts[0]})"
        elif your_count > counts[-1]:
            return f"Above all competitors (longest is {counts[-1]})"
        else:
            # Find position
            for i, count in enumerate(counts):
                if your_count <= count:
                    return f"Between position {i} and {i+1} competitors"

        return "Within competitive range"

    def _analyze_competition(
        self,
        your_count: Optional[int],
        competitors: List[Dict[str, Any]],
        stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Provide competitive analysis"""
        analysis = {
            'total_competitors': len(competitors),
            'length_distribution': self._categorize_lengths(competitors),
        }

        if your_count and stats:
            # How many competitors you're longer than
            shorter_than_you = len([c for c in competitors if c['word_count'] < your_count])
            longer_than_you = len([c for c in competitors if c['word_count'] > your_count])

            analysis['comparison'] = {
                'shorter_than_you': shorter_than_you,
                'longer_than_you': longer_than_you,
                'percentile': round((shorter_than_you / len(competitors)) * 100) if competitors else 0
            }

            # Gap analysis
            if your_count < stats['median']:
                gap = stats['median'] - your_count
                analysis['gap_to_median'] = {
                    'words': gap,
                    'percentage': round((gap / your_count) * 100)
                }

            if your_count < stats['percentile_75']:
                gap = stats['percentile_75'] - your_count
                analysis['gap_to_75th_percentile'] = {
                    'words': gap,
                    'percentage': round((gap / your_count) * 100) if your_count > 0 else 0
                }

        return analysis

    def _categorize_lengths(self, competitors: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize competitor content by length ranges"""
        categories = {
            'under_1000': 0,
            '1000_1500': 0,
            '1500_2000': 0,
            '2000_2500': 0,
            '2500_3000': 0,
            '3000_plus': 0
        }

        for comp in competitors:
            count = comp['word_count']
            if count < 1000:
                categories['under_1000'] += 1
            elif count < 1500:
                categories['1000_1500'] += 1
            elif count < 2000:
                categories['1500_2000'] += 1
            elif count < 2500:
                categories['2000_2500'] += 1
            elif count < 3000:
                categories['2500_3000'] += 1
            else:
                categories['3000_plus'] += 1

        return categories


# Convenience function
def compare_content_length(
    keyword: str,
    your_word_count: Optional[int] = None,
    serp_results: Optional[List[Dict[str, str]]] = None,
    fetch_content: bool = True
) -> Dict[str, Any]:
    """
    Compare content length against SERP competitors

    Args:
        keyword: Target keyword
        your_word_count: Your content's word count
        serp_results: SERP results from DataForSEO
        fetch_content: Whether to fetch competitor content

    Returns:
        Content length comparison and recommendations
    """
    comparator = ContentLengthComparator()
    return comparator.analyze(keyword, your_word_count, serp_results, fetch_content)


# Example usage
if __name__ == "__main__":
    # Example with mock SERP data
    mock_serp = [
        {'url': 'https://example1.com/podcast-guide', 'domain': 'example1.com', 'title': 'How to Start a Podcast'},
        {'url': 'https://example2.com/podcast-tutorial', 'domain': 'example2.com', 'title': 'Podcast Tutorial'},
        {'url': 'https://example3.com/podcasting-101', 'domain': 'example3.com', 'title': 'Podcasting 101'},
    ]

    # Note: In real usage, this would fetch actual content
    # For demo, we'll create mock data
    print("=== Content Length Comparison ===")
    print("\nNote: In production, this would fetch real competitor content.")
    print("Example output structure:")

    example_output = {
        'keyword': 'how to start a podcast',
        'competitors_analyzed': 10,
        'your_word_count': 2200,
        'statistics': {
            'min': 1800,
            'max': 4500,
            'mean': 2650,
            'median': 2500,
            'percentile_75': 3200
        },
        'recommendation': {
            'recommended_min': 2500,
            'recommended_optimal': 3200,
            'recommended_max': 3840,
            'your_status': 'short',
            'message': 'Consider adding 1000 more words to match top performers.',
            'reasoning': 'Based on median (2500) and 75th percentile (3200) of top 10 results'
        },
        'competitive_analysis': {
            'total_competitors': 10,
            'comparison': {
                'shorter_than_you': 3,
                'longer_than_you': 7,
                'percentile': 30
            },
            'gap_to_median': {
                'words': 300,
                'percentage': 14
            }
        }
    }

    import json
    print(json.dumps(example_output, indent=2))
