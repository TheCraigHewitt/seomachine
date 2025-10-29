"""
Google Analytics 4 Data Integration

Fetches traffic, engagement, and conversion data from GA4 properties.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter,
)
from google.oauth2 import service_account

class GoogleAnalytics:
    """Google Analytics 4 data fetcher"""

    def __init__(self, property_id: Optional[str] = None, credentials_path: Optional[str] = None):
        """
        Initialize GA4 client

        Args:
            property_id: GA4 property ID (defaults to env var GA4_PROPERTY_ID)
            credentials_path: Path to credentials JSON (defaults to env var)
        """
        self.property_id = property_id or os.getenv('GA4_PROPERTY_ID')
        credentials_path = credentials_path or os.getenv('GA4_CREDENTIALS_PATH')

        if not self.property_id:
            raise ValueError("GA4_PROPERTY_ID must be provided or set in environment")

        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError(f"Credentials file not found: {credentials_path}")

        # Initialize client with service account
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )

        self.client = BetaAnalyticsDataClient(credentials=credentials)

    def get_top_pages(
        self,
        days: int = 30,
        limit: int = 20,
        path_filter: Optional[str] = "/blog/"
    ) -> List[Dict[str, Any]]:
        """
        Get top performing pages by pageviews

        Args:
            days: Number of days to look back
            limit: Number of results to return
            path_filter: Filter pages by path (e.g., "/blog/")

        Returns:
            List of dicts with page data
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )],
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="pageTitle"),
            ],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="sessions"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
                Metric(name="engagementRate"),
            ],
            limit=limit,
            order_bys=[{
                "metric": {"metric_name": "screenPageViews"},
                "desc": True
            }]
        )

        # Add path filter if provided
        if path_filter:
            request.dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value=path_filter
                    )
                )
            )

        response = self.client.run_report(request)

        results = []
        for row in response.rows:
            results.append({
                'path': row.dimension_values[0].value,
                'title': row.dimension_values[1].value,
                'pageviews': int(row.metric_values[0].value),
                'sessions': int(row.metric_values[1].value),
                'avg_session_duration': float(row.metric_values[2].value),
                'bounce_rate': float(row.metric_values[3].value),
                'engagement_rate': float(row.metric_values[4].value),
            })

        return results

    def get_page_trends(
        self,
        url: str,
        days: int = 90,
        granularity: str = "week"
    ) -> Dict[str, Any]:
        """
        Get traffic trends for a specific page

        Args:
            url: Page path (e.g., "/blog/podcast-monetization")
            days: Number of days to analyze
            granularity: "day" or "week"

        Returns:
            Dict with trend data
        """
        dimension_name = "date" if granularity == "day" else "week"

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )],
            dimensions=[Dimension(name=dimension_name)],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="sessions"),
                Metric(name="averageSessionDuration"),
            ],
            dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.EXACT,
                        value=url
                    )
                )
            ),
            order_bys=[{
                "dimension": {"dimension_name": dimension_name},
                "desc": False
            }]
        )

        response = self.client.run_report(request)

        timeline = []
        for row in response.rows:
            timeline.append({
                'period': row.dimension_values[0].value,
                'pageviews': int(row.metric_values[0].value),
                'sessions': int(row.metric_values[1].value),
                'avg_duration': float(row.metric_values[2].value),
            })

        # Calculate trend direction
        if len(timeline) >= 2:
            recent_views = sum(t['pageviews'] for t in timeline[-4:])  # Last 4 periods
            older_views = sum(t['pageviews'] for t in timeline[:4])     # First 4 periods

            if older_views > 0:
                trend_percent = ((recent_views - older_views) / older_views) * 100
            else:
                trend_percent = 0

            trend_direction = "rising" if trend_percent > 10 else "declining" if trend_percent < -10 else "stable"
        else:
            trend_percent = 0
            trend_direction = "unknown"

        return {
            'url': url,
            'timeline': timeline,
            'trend_direction': trend_direction,
            'trend_percent': round(trend_percent, 2),
            'total_pageviews': sum(t['pageviews'] for t in timeline),
        }

    def get_conversions(
        self,
        days: int = 30,
        path_filter: Optional[str] = "/blog/"
    ) -> List[Dict[str, Any]]:
        """
        Get conversion data by page

        Args:
            days: Number of days to look back
            path_filter: Filter pages by path

        Returns:
            List of pages with conversion data
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )],
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="pageTitle"),
            ],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="conversions"),
                Metric(name="totalRevenue"),
            ],
            order_bys=[{
                "metric": {"metric_name": "conversions"},
                "desc": True
            }]
        )

        if path_filter:
            request.dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value=path_filter
                    )
                )
            )

        response = self.client.run_report(request)

        results = []
        for row in response.rows:
            pageviews = int(row.metric_values[0].value)
            conversions = float(row.metric_values[1].value)

            results.append({
                'path': row.dimension_values[0].value,
                'title': row.dimension_values[1].value,
                'pageviews': pageviews,
                'conversions': conversions,
                'conversion_rate': (conversions / pageviews * 100) if pageviews > 0 else 0,
                'revenue': float(row.metric_values[2].value),
            })

        return results

    def get_traffic_sources(
        self,
        url: Optional[str] = None,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get traffic source breakdown for a page or entire site

        Args:
            url: Specific page path (optional, None = all pages)
            days: Number of days to analyze

        Returns:
            List of traffic sources with metrics
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )],
            dimensions=[
                Dimension(name="sessionDefaultChannelGroup"),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="engagementRate"),
            ],
            order_bys=[{
                "metric": {"metric_name": "sessions"},
                "desc": True
            }]
        )

        if url:
            request.dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.EXACT,
                        value=url
                    )
                )
            )

        response = self.client.run_report(request)

        results = []
        for row in response.rows:
            results.append({
                'source': row.dimension_values[0].value,
                'sessions': int(row.metric_values[0].value),
                'pageviews': int(row.metric_values[1].value),
                'engagement_rate': float(row.metric_values[2].value),
            })

        return results

    def get_declining_pages(
        self,
        comparison_days: int = 30,
        threshold_percent: float = -20.0,
        path_filter: str = "/blog/"
    ) -> List[Dict[str, Any]]:
        """
        Identify pages with declining traffic

        Args:
            comparison_days: Compare this many recent days vs previous period
            threshold_percent: Consider declining if drop exceeds this %
            path_filter: Filter pages by path

        Returns:
            List of declining pages with metrics
        """
        # Get recent period data
        recent_pages = self.get_top_pages(
            days=comparison_days,
            limit=100,
            path_filter=path_filter
        )

        # Get previous period data
        previous_pages = self.get_top_pages(
            days=comparison_days * 2,
            limit=100,
            path_filter=path_filter
        )

        # Create lookup for previous data
        previous_lookup = {p['path']: p['pageviews'] for p in previous_pages}

        declining = []
        for page in recent_pages:
            path = page['path']
            recent_views = page['pageviews']
            previous_views = previous_lookup.get(path, 0)

            if previous_views > 0:
                change_percent = ((recent_views - previous_views) / previous_views) * 100

                if change_percent < threshold_percent:
                    declining.append({
                        **page,
                        'previous_pageviews': previous_views,
                        'change_percent': round(change_percent, 2),
                        'priority': 'high' if change_percent < -40 else 'medium'
                    })

        # Sort by worst decline
        declining.sort(key=lambda x: x['change_percent'])

        return declining


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    ga = GoogleAnalytics()

    print("Top 10 blog articles:")
    top_pages = ga.get_top_pages(days=30, limit=10)
    for i, page in enumerate(top_pages, 1):
        print(f"{i}. {page['title']}")
        print(f"   {page['path']}")
        print(f"   {page['pageviews']:,} pageviews | {page['engagement_rate']:.1%} engagement")
        print()

    print("\nDeclining articles:")
    declining = ga.get_declining_pages(comparison_days=30)
    for page in declining[:5]:
        print(f"- {page['title']}")
        print(f"  {page['path']}")
        print(f"  {page['change_percent']:.1f}% change ({page['previous_pageviews']} → {page['pageviews']})")
        print()
