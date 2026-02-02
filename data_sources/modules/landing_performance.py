"""
Landing Page Performance Tracker

Tracks landing page performance metrics via GA4 and GSC.
Extends existing google_analytics.py module for landing-page-specific analysis.

Metrics tracked:
- Traffic (page views, sessions, users)
- Engagement (bounce rate, time on page)
- Conversions (by goal type, by traffic source)
- SEO (for SEO landing pages via GSC)
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Try to import GA4 module (may not be available in all environments)
try:
    from .google_analytics import GoogleAnalytics
    GA4_AVAILABLE = True
except ImportError:
    GA4_AVAILABLE = False

try:
    from .google_search_console import GoogleSearchConsole
    GSC_AVAILABLE = True
except ImportError:
    GSC_AVAILABLE = False


class LandingPagePerformance:
    """Track and analyze landing page performance"""

    # Conversion event mappings (adjust to match your GA4 setup)
    CONVERSION_EVENTS = {
        'trial': ['trial_started', 'signup_complete', 'start_trial'],
        'demo': ['demo_requested', 'demo_booked', 'schedule_demo'],
        'lead': ['lead_captured', 'download_complete', 'form_submit']
    }

    # Industry benchmarks for landing pages
    BENCHMARKS = {
        'bounce_rate': {
            'excellent': 30,
            'good': 40,
            'average': 50,
            'poor': 60
        },
        'avg_time_on_page': {
            'excellent': 180,  # 3 minutes
            'good': 120,       # 2 minutes
            'average': 60,     # 1 minute
            'poor': 30         # 30 seconds
        },
        'conversion_rate': {
            'trial': {'excellent': 15, 'good': 10, 'average': 5, 'poor': 2},
            'demo': {'excellent': 10, 'good': 5, 'average': 3, 'poor': 1},
            'lead': {'excellent': 30, 'good': 20, 'average': 10, 'poor': 5}
        }
    }

    def __init__(self):
        """Initialize performance tracker"""
        self.ga4 = GoogleAnalytics() if GA4_AVAILABLE else None
        self.gsc = GoogleSearchConsole() if GSC_AVAILABLE else None

    def get_landing_page_performance(
        self,
        url: str,
        days: int = 30,
        conversion_goal: str = 'trial'
    ) -> Dict[str, Any]:
        """
        Get comprehensive performance data for a landing page

        Args:
            url: Landing page URL (full URL or path)
            days: Lookback period in days
            conversion_goal: 'trial', 'demo', or 'lead'

        Returns:
            Dict with traffic, engagement, conversion, and SEO metrics
        """
        results = {
            'url': url,
            'period_days': days,
            'conversion_goal': conversion_goal,
            'data_available': False,
            'traffic': {},
            'engagement': {},
            'conversions': {},
            'seo': {},
            'recommendations': []
        }

        # Get traffic metrics from GA4
        if self.ga4:
            traffic_data = self._get_traffic_metrics(url, days)
            results['traffic'] = traffic_data
            results['data_available'] = traffic_data.get('sessions', 0) > 0

            # Get engagement metrics
            engagement_data = self._get_engagement_metrics(url, days)
            results['engagement'] = engagement_data

            # Get conversion metrics
            conversion_data = self._get_conversion_metrics(url, days, conversion_goal)
            results['conversions'] = conversion_data

        # Get SEO metrics from GSC
        if self.gsc:
            seo_data = self._get_seo_metrics(url, days)
            results['seo'] = seo_data

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)

        # Add performance grades
        results['grades'] = self._calculate_grades(results)

        return results

    def _get_traffic_metrics(self, url: str, days: int) -> Dict[str, Any]:
        """Get traffic metrics from GA4"""
        if not self.ga4:
            return {'error': 'GA4 not configured'}

        try:
            # This would use the GA4 API to get page-specific metrics
            # Placeholder implementation - adjust to your GA4 setup
            return {
                'page_views': 0,
                'sessions': 0,
                'users': 0,
                'new_users': 0,
                'by_source': {
                    'organic': 0,
                    'paid': 0,
                    'direct': 0,
                    'referral': 0,
                    'social': 0
                }
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_engagement_metrics(self, url: str, days: int) -> Dict[str, Any]:
        """Get engagement metrics from GA4"""
        if not self.ga4:
            return {'error': 'GA4 not configured'}

        try:
            return {
                'bounce_rate': 0.0,
                'avg_time_on_page': 0,
                'engagement_rate': 0.0,
                'scroll_depth': {
                    '25%': 0,
                    '50%': 0,
                    '75%': 0,
                    '100%': 0
                },
                'exit_rate': 0.0
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_conversion_metrics(
        self,
        url: str,
        days: int,
        goal: str
    ) -> Dict[str, Any]:
        """Get conversion metrics from GA4"""
        if not self.ga4:
            return {'error': 'GA4 not configured'}

        events = self.CONVERSION_EVENTS.get(goal, [])

        try:
            return {
                'total_conversions': 0,
                'conversion_rate': 0.0,
                'by_event': {event: 0 for event in events},
                'by_source': {
                    'organic': {'conversions': 0, 'rate': 0.0},
                    'paid': {'conversions': 0, 'rate': 0.0},
                    'direct': {'conversions': 0, 'rate': 0.0}
                }
            }
        except Exception as e:
            return {'error': str(e)}

    def _get_seo_metrics(self, url: str, days: int) -> Dict[str, Any]:
        """Get SEO metrics from Google Search Console"""
        if not self.gsc:
            return {'error': 'GSC not configured'}

        try:
            return {
                'impressions': 0,
                'clicks': 0,
                'ctr': 0.0,
                'avg_position': 0.0,
                'top_queries': []
            }
        except Exception as e:
            return {'error': str(e)}

    def _generate_recommendations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on performance data"""
        recommendations = []

        # Check bounce rate
        engagement = data.get('engagement', {})
        bounce_rate = engagement.get('bounce_rate', 0)

        if bounce_rate > self.BENCHMARKS['bounce_rate']['poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'bounce_rate',
                'issue': f'High bounce rate ({bounce_rate:.1f}%)',
                'recommendation': 'Review above-the-fold content. Ensure value proposition is clear within 5 seconds.'
            })
        elif bounce_rate > self.BENCHMARKS['bounce_rate']['average']:
            recommendations.append({
                'priority': 'medium',
                'metric': 'bounce_rate',
                'issue': f'Above-average bounce rate ({bounce_rate:.1f}%)',
                'recommendation': 'Consider improving headline or adding trust signals above fold.'
            })

        # Check time on page
        time_on_page = engagement.get('avg_time_on_page', 0)

        if time_on_page < self.BENCHMARKS['avg_time_on_page']['poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'time_on_page',
                'issue': f'Very low time on page ({time_on_page}s)',
                'recommendation': 'Content may not be engaging. Add compelling visuals, improve copy, or reconsider targeting.'
            })

        # Check conversion rate
        conversions = data.get('conversions', {})
        conv_rate = conversions.get('conversion_rate', 0)
        goal = data.get('conversion_goal', 'trial')
        benchmarks = self.BENCHMARKS['conversion_rate'].get(goal, {})

        if conv_rate < benchmarks.get('poor', 2):
            recommendations.append({
                'priority': 'high',
                'metric': 'conversion_rate',
                'issue': f'Low conversion rate ({conv_rate:.1f}%)',
                'recommendation': 'Review CTA placement, copy, and trust signals. Consider A/B testing headline and CTA.'
            })
        elif conv_rate < benchmarks.get('average', 5):
            recommendations.append({
                'priority': 'medium',
                'metric': 'conversion_rate',
                'issue': f'Below-average conversion rate ({conv_rate:.1f}%)',
                'recommendation': 'Test different CTAs, add social proof, or improve risk reversal messaging.'
            })

        # Check traffic source mix
        traffic = data.get('traffic', {})
        by_source = traffic.get('by_source', {})
        total = sum(by_source.values())

        if total > 0:
            paid_pct = by_source.get('paid', 0) / total * 100 if total else 0
            organic_pct = by_source.get('organic', 0) / total * 100 if total else 0

            if paid_pct > 80:
                recommendations.append({
                    'priority': 'low',
                    'metric': 'traffic_source',
                    'issue': 'Heavily reliant on paid traffic',
                    'recommendation': 'Consider optimizing for organic search to reduce customer acquisition costs.'
                })

        return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])

    def _calculate_grades(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Calculate letter grades for each metric category"""
        grades = {}

        # Engagement grade
        engagement = data.get('engagement', {})
        bounce = engagement.get('bounce_rate', 100)

        if bounce <= self.BENCHMARKS['bounce_rate']['excellent']:
            grades['engagement'] = 'A'
        elif bounce <= self.BENCHMARKS['bounce_rate']['good']:
            grades['engagement'] = 'B'
        elif bounce <= self.BENCHMARKS['bounce_rate']['average']:
            grades['engagement'] = 'C'
        elif bounce <= self.BENCHMARKS['bounce_rate']['poor']:
            grades['engagement'] = 'D'
        else:
            grades['engagement'] = 'F'

        # Conversion grade
        conversions = data.get('conversions', {})
        conv_rate = conversions.get('conversion_rate', 0)
        goal = data.get('conversion_goal', 'trial')
        benchmarks = self.BENCHMARKS['conversion_rate'].get(goal, {})

        if conv_rate >= benchmarks.get('excellent', 15):
            grades['conversions'] = 'A'
        elif conv_rate >= benchmarks.get('good', 10):
            grades['conversions'] = 'B'
        elif conv_rate >= benchmarks.get('average', 5):
            grades['conversions'] = 'C'
        elif conv_rate >= benchmarks.get('poor', 2):
            grades['conversions'] = 'D'
        else:
            grades['conversions'] = 'F'

        return grades

    def compare_landing_pages(
        self,
        urls: List[str],
        days: int = 30,
        conversion_goal: str = 'trial'
    ) -> Dict[str, Any]:
        """
        Compare multiple landing pages

        Args:
            urls: List of landing page URLs
            days: Lookback period
            conversion_goal: Conversion goal for all pages

        Returns:
            Comparison data for all pages
        """
        comparison = {
            'period_days': days,
            'conversion_goal': conversion_goal,
            'pages': []
        }

        for url in urls:
            page_data = self.get_landing_page_performance(url, days, conversion_goal)
            comparison['pages'].append({
                'url': url,
                'traffic': page_data.get('traffic', {}).get('sessions', 0),
                'bounce_rate': page_data.get('engagement', {}).get('bounce_rate', 0),
                'conversions': page_data.get('conversions', {}).get('total_conversions', 0),
                'conversion_rate': page_data.get('conversions', {}).get('conversion_rate', 0),
                'grades': page_data.get('grades', {})
            })

        # Sort by conversion rate descending
        comparison['pages'].sort(
            key=lambda x: x.get('conversion_rate', 0),
            reverse=True
        )

        # Add winner/loser tags
        if len(comparison['pages']) > 1:
            comparison['pages'][0]['tag'] = 'best_performer'
            comparison['pages'][-1]['tag'] = 'needs_improvement'

        return comparison

    def get_ppc_performance(
        self,
        url: str,
        days: int = 30,
        campaign: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get PPC-specific landing page performance

        Args:
            url: Landing page URL
            days: Lookback period
            campaign: Optional campaign filter

        Returns:
            PPC-specific metrics
        """
        if not self.ga4:
            return {'error': 'GA4 not configured'}

        try:
            return {
                'url': url,
                'campaign': campaign,
                'period_days': days,
                'ppc_traffic': {
                    'sessions': 0,
                    'users': 0,
                    'by_campaign': {}
                },
                'ppc_engagement': {
                    'bounce_rate': 0.0,
                    'avg_time_on_page': 0
                },
                'ppc_conversions': {
                    'total': 0,
                    'rate': 0.0,
                    'by_campaign': {}
                },
                'recommendations': []
            }
        except Exception as e:
            return {'error': str(e)}


# Convenience functions
def get_landing_page_performance(
    url: str,
    days: int = 30,
    conversion_goal: str = 'trial'
) -> Dict[str, Any]:
    """
    Get landing page performance data

    Args:
        url: Landing page URL
        days: Lookback period
        conversion_goal: 'trial', 'demo', or 'lead'

    Returns:
        Performance metrics and recommendations
    """
    tracker = LandingPagePerformance()
    return tracker.get_landing_page_performance(url, days, conversion_goal)


def compare_landing_pages(
    urls: List[str],
    days: int = 30,
    conversion_goal: str = 'trial'
) -> Dict[str, Any]:
    """
    Compare multiple landing pages

    Args:
        urls: List of landing page URLs
        days: Lookback period
        conversion_goal: Conversion goal

    Returns:
        Comparison data
    """
    tracker = LandingPagePerformance()
    return tracker.compare_landing_pages(urls, days, conversion_goal)


# Example usage
if __name__ == "__main__":
    # Example usage (requires GA4 credentials)
    print("Landing Page Performance Tracker")
    print("=" * 40)

    # Check if modules are available
    print(f"GA4 Available: {GA4_AVAILABLE}")
    print(f"GSC Available: {GSC_AVAILABLE}")

    # Example (would need real credentials)
    if GA4_AVAILABLE or GSC_AVAILABLE:
        result = get_landing_page_performance(
            url="https://yoursite.com/pricing/",
            days=30,
            conversion_goal='trial'
        )

        print(f"\nURL: {result['url']}")
        print(f"Data Available: {result['data_available']}")

        if result.get('grades'):
            print(f"\nGrades:")
            for category, grade in result['grades'].items():
                print(f"  {category}: {grade}")

        if result.get('recommendations'):
            print(f"\nRecommendations:")
            for rec in result['recommendations'][:3]:
                print(f"  [{rec['priority'].upper()}] {rec['recommendation']}")
    else:
        print("\nNote: GA4 and GSC modules not available.")
        print("This module requires google_analytics.py and google_search_console.py")
