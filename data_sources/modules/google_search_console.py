"""
Google Search Console Data Integration

Fetches search performance, keyword rankings, and SERP data.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSearchConsole:
    """Google Search Console data fetcher"""

    def __init__(self, site_url: Optional[str] = None, credentials_path: Optional[str] = None):
        """
        Initialize GSC client

        Args:
            site_url: Site URL (e.g., "https://castos.com")
            credentials_path: Path to credentials JSON
        """
        self.site_url = site_url or os.getenv('GSC_SITE_URL')
        credentials_path = credentials_path or os.getenv('GSC_CREDENTIALS_PATH')

        if not self.site_url:
            raise ValueError("GSC_SITE_URL must be provided or set in environment")

        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError(f"Credentials file not found: {credentials_path}")

        # Initialize client
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )

        self.service = build('searchconsole', 'v1', credentials=credentials)

    def get_keyword_positions(
        self,
        days: int = 30,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get keyword rankings and performance

        Args:
            days: Number of days to analyze
            limit: Max number of keywords to return

        Returns:
            List of keywords with position, clicks, impressions
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'rowLimit': limit,
            'dimensionFilterGroups': []
        }

        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()

        results = []
        for row in response.get('rows', []):
            query = row['keys'][0]
            results.append({
                'keyword': query,
                'clicks': row['clicks'],
                'impressions': row['impressions'],
                'ctr': row['ctr'],
                'position': round(row['position'], 1)
            })

        # Sort by impressions (potential)
        results.sort(key=lambda x: x['impressions'], reverse=True)

        return results

    def get_quick_wins(
        self,
        days: int = 30,
        position_min: int = 11,
        position_max: int = 20,
        min_impressions: int = 50,
        prioritize_commercial: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find "quick win" opportunities - keywords ranking 11-20

        These are closest to page 1 and easiest to improve.

        Args:
            days: Number of days to analyze
            position_min: Minimum position (default 11)
            position_max: Maximum position (default 20)
            min_impressions: Minimum impressions threshold
            prioritize_commercial: Weight score by commercial intent (default True)

        Returns:
            List of quick win opportunities
        """
        all_keywords = self.get_keyword_positions(days=days)

        quick_wins = []
        for kw in all_keywords:
            if (position_min <= kw['position'] <= position_max and
                kw['impressions'] >= min_impressions):

                keyword = kw['keyword'].lower()

                # Calculate commercial intent score (0.1 to 3.0)
                commercial_intent = self._calculate_commercial_intent(keyword)

                # Calculate opportunity score
                # Factors: impressions, proximity to page 1, commercial intent
                distance_from_10 = kw['position'] - 10
                base_score = kw['impressions'] / (distance_from_10 + 1)

                if prioritize_commercial:
                    opportunity_score = base_score * commercial_intent
                else:
                    opportunity_score = base_score

                quick_wins.append({
                    **kw,
                    'commercial_intent': commercial_intent,
                    'commercial_intent_category': self._get_intent_category(commercial_intent),
                    'opportunity_score': round(opportunity_score, 2),
                    'priority': 'high' if kw['position'] <= 15 else 'medium'
                })

        # Sort by opportunity score
        quick_wins.sort(key=lambda x: x['opportunity_score'], reverse=True)

        return quick_wins

    def _calculate_commercial_intent(self, keyword: str) -> float:
        """
        Calculate commercial intent score for a keyword

        Returns:
            Float between 0.1 (informational) and 3.0 (transactional)
        """
        keyword = keyword.lower()

        # HIGH INTENT (3.0): Transactional - ready to buy
        high_intent_terms = [
            'pricing', 'price', 'cost', 'buy', 'purchase', 'vs', 'versus',
            'alternative', 'alternatives', 'best', 'top', 'review', 'reviews',
            'comparison', 'compare', 'plan', 'plans', 'trial', 'free trial',
            'discount', 'coupon', 'deal', 'hosting', 'service', 'services',
            'platform', 'software', 'tool', 'tools', 'solution', 'solutions',
            'provider', 'providers'
        ]

        # MEDIUM-HIGH INTENT (2.0): Commercial investigation
        medium_high_intent = [
            'how to', 'guide', 'tutorial', 'tips', 'strategies', 'examples',
            'ideas', 'ways to', 'for business', 'for companies', 'professional',
            'analytics', 'monetization', 'monetize', 'grow', 'increase',
            'improve', 'optimize', 'setup', 'set up'
        ]

        # MEDIUM INTENT (1.0): Informational with potential
        medium_intent = [
            'what is', 'how does', 'why', 'benefits', 'features',
            'podcast', 'podcasting', 'audio', 'video', 'rss', 'marketing'
        ]

        # LOW INTENT (0.1): Pure informational/celebrity/news
        low_intent_terms = [
            'who is', 'biography', 'age', 'net worth', 'height', 'wife',
            'husband', 'dating', 'married', 'death', 'died', 'born',
            'pewdiepie', 'youtube stars', 'celebrity', 'famous'
        ]

        # Check for low intent first (these override everything)
        for term in low_intent_terms:
            if term in keyword:
                return 0.1

        # Check for high intent
        for term in high_intent_terms:
            if term in keyword:
                return 3.0

        # Check for medium-high intent
        for term in medium_high_intent:
            if term in keyword:
                return 2.0

        # Check for medium intent
        for term in medium_intent:
            if term in keyword:
                return 1.0

        # Default: low-medium intent
        return 0.5

    def _get_intent_category(self, score: float) -> str:
        """Get human-readable intent category"""
        if score >= 2.5:
            return 'Transactional'
        elif score >= 1.5:
            return 'Commercial Investigation'
        elif score >= 0.8:
            return 'Informational (Relevant)'
        else:
            return 'Informational (Low Value)'

    def get_page_performance(
        self,
        url: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get search performance for a specific page

        Args:
            url: Page URL or path
            days: Number of days to analyze

        Returns:
            Dict with page performance data
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        # Get page-level data
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'page',
                    'operator': 'equals' if url.startswith('http') else 'contains',
                    'expression': url
                }]
            }]
        }

        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()

        if not response.get('rows'):
            return {'url': url, 'error': 'No data found'}

        row = response['rows'][0]

        page_data = {
            'url': row['keys'][0],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': round(row['ctr'] * 100, 2),
            'avg_position': round(row['position'], 1)
        }

        # Get keywords for this page
        keywords_request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'page',
                    'operator': 'equals' if url.startswith('http') else 'contains',
                    'expression': url
                }]
            }],
            'rowLimit': 50
        }

        keywords_response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=keywords_request
        ).execute()

        keywords = []
        for kw_row in keywords_response.get('rows', []):
            keywords.append({
                'keyword': kw_row['keys'][0],
                'clicks': kw_row['clicks'],
                'impressions': kw_row['impressions'],
                'position': round(kw_row['position'], 1)
            })

        keywords.sort(key=lambda x: x['clicks'], reverse=True)
        page_data['top_keywords'] = keywords[:10]

        return page_data

    def get_low_ctr_pages(
        self,
        days: int = 30,
        ctr_threshold: float = 0.03,  # 3%
        min_impressions: int = 100,
        path_filter: Optional[str] = "/blog/"
    ) -> List[Dict[str, Any]]:
        """
        Find pages with high impressions but low CTR

        These need better titles/descriptions.

        Args:
            days: Number of days to analyze
            ctr_threshold: CTR below this is considered low
            min_impressions: Minimum impressions to consider
            path_filter: Filter by path

        Returns:
            List of pages with low CTR
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'rowLimit': 1000
        }

        if path_filter:
            request['dimensionFilterGroups'] = [{
                'filters': [{
                    'dimension': 'page',
                    'operator': 'contains',
                    'expression': path_filter
                }]
            }]

        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()

        low_ctr = []
        for row in response.get('rows', []):
            impressions = row['impressions']
            ctr = row['ctr']

            if impressions >= min_impressions and ctr < ctr_threshold:
                # Calculate potential clicks if CTR improved
                target_ctr = 0.05  # 5% target
                potential_clicks = int(impressions * target_ctr)
                missed_clicks = potential_clicks - row['clicks']

                low_ctr.append({
                    'url': row['keys'][0],
                    'impressions': impressions,
                    'clicks': row['clicks'],
                    'ctr': round(ctr * 100, 2),
                    'avg_position': round(row['position'], 1),
                    'potential_clicks': potential_clicks,
                    'missed_clicks': missed_clicks,
                    'priority': 'high' if missed_clicks > 50 else 'medium'
                })

        # Sort by missed opportunity
        low_ctr.sort(key=lambda x: x['missed_clicks'], reverse=True)

        return low_ctr

    def get_trending_queries(
        self,
        days_recent: int = 7,
        days_comparison: int = 30,
        min_impressions: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Find queries gaining traction (rising impressions)

        Args:
            days_recent: Recent period to analyze
            days_comparison: Previous period to compare against
            min_impressions: Minimum impressions in recent period

        Returns:
            List of trending queries
        """
        # Get recent data
        recent_end = datetime.now().strftime('%Y-%m-%d')
        recent_start = (datetime.now() - timedelta(days=days_recent)).strftime('%Y-%m-%d')

        recent_request = {
            'startDate': recent_start,
            'endDate': recent_end,
            'dimensions': ['query'],
            'rowLimit': 1000
        }

        recent_response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=recent_request
        ).execute()

        # Get comparison data
        comparison_end = (datetime.now() - timedelta(days=days_recent)).strftime('%Y-%m-%d')
        comparison_start = (datetime.now() - timedelta(days=days_comparison)).strftime('%Y-%m-%d')

        comparison_request = {
            'startDate': comparison_start,
            'endDate': comparison_end,
            'dimensions': ['query'],
            'rowLimit': 1000
        }

        comparison_response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=comparison_request
        ).execute()

        # Create lookup for comparison data
        comparison_lookup = {
            row['keys'][0]: row['impressions']
            for row in comparison_response.get('rows', [])
        }

        trending = []
        for row in recent_response.get('rows', []):
            query = row['keys'][0]
            recent_impressions = row['impressions']

            if recent_impressions < min_impressions:
                continue

            previous_impressions = comparison_lookup.get(query, 0)

            if previous_impressions > 0:
                change_percent = ((recent_impressions - previous_impressions) / previous_impressions) * 100
            else:
                change_percent = 100  # New query

            # Only include queries showing growth
            if change_percent > 20:
                trending.append({
                    'query': query,
                    'recent_impressions': recent_impressions,
                    'previous_impressions': previous_impressions,
                    'change_percent': round(change_percent, 1),
                    'clicks': row['clicks'],
                    'position': round(row['position'], 1)
                })

        # Sort by growth percentage
        trending.sort(key=lambda x: x['change_percent'], reverse=True)

        return trending

    def get_position_changes(
        self,
        days_recent: int = 7,
        days_comparison: int = 30
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Track keyword position changes

        Args:
            days_recent: Recent period
            days_comparison: Previous period to compare

        Returns:
            Dict with 'improved', 'declined', and 'stable' lists
        """
        # Get recent positions
        recent_data = self.get_keyword_positions(days=days_recent)

        # Get comparison positions
        comparison_data = self.get_keyword_positions(days=days_comparison)

        # Create lookup
        comparison_lookup = {
            kw['keyword']: kw['position']
            for kw in comparison_data
        }

        improved = []
        declined = []
        stable = []

        for kw in recent_data:
            keyword = kw['keyword']
            current_pos = kw['position']
            previous_pos = comparison_lookup.get(keyword)

            if not previous_pos:
                continue  # New keyword

            position_change = previous_pos - current_pos  # Positive = improved

            result = {
                **kw,
                'previous_position': previous_pos,
                'position_change': round(position_change, 1)
            }

            if position_change >= 2:  # Improved by 2+ positions
                improved.append(result)
            elif position_change <= -2:  # Declined by 2+ positions
                declined.append(result)
            else:
                stable.append(result)

        # Sort by magnitude of change
        improved.sort(key=lambda x: x['position_change'], reverse=True)
        declined.sort(key=lambda x: x['position_change'])

        return {
            'improved': improved,
            'declined': declined,
            'stable': stable
        }


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    gsc = GoogleSearchConsole()

    print("Quick Win Opportunities (Position 11-20):")
    quick_wins = gsc.get_quick_wins()
    for i, kw in enumerate(quick_wins[:10], 1):
        print(f"{i}. {kw['keyword']}")
        print(f"   Position: {kw['position']} | Impressions: {kw['impressions']:,}")
        print(f"   Opportunity Score: {kw['opportunity_score']:.1f}")
        print()

    print("\nLow CTR Pages (Need Better Meta):")
    low_ctr = gsc.get_low_ctr_pages()
    for page in low_ctr[:5]:
        print(f"- {page['url']}")
        print(f"  {page['impressions']:,} impressions | {page['ctr']:.2f}% CTR")
        print(f"  Missing {page['missed_clicks']} potential clicks")
        print()

    print("\nTrending Queries:")
    trending = gsc.get_trending_queries()
    for query in trending[:5]:
        print(f"- {query['query']}")
        print(f"  +{query['change_percent']:.1f}% impressions")
        print()
