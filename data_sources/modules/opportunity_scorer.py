"""
Opportunity Scorer

Multi-factor scoring system for prioritizing SEO opportunities.
Considers: volume, position, intent, competition, cluster value, CTR, and freshness.
"""

from typing import Dict, Any, Optional
from enum import Enum


class OpportunityType(Enum):
    """Types of SEO opportunities"""
    QUICK_WIN = "quick_win"           # Position 11-20, close to page 1
    IMPROVEMENT = "improvement"        # Position 1-10, can reach #1-3
    MEDIUM_TERM = "medium_term"        # Position 21-50, needs significant work
    NEW_CONTENT = "new_content"        # Not ranking, competitor gap
    DECLINING = "declining"            # Was good, now dropping
    UNDERPERFORMER = "underperformer"  # High ranking, low CTR


class OpportunityScorer:
    """
    Calculate comprehensive opportunity scores for keywords/pages.

    Scoring Methodology:
    - Volume Score (25%): Search demand/impressions
    - Position Score (20%): Proximity to target position
    - Intent Score (20%): Commercial value
    - Competition Score (15%): Ranking difficulty
    - Cluster Score (10%): Strategic topic value
    - CTR Score (5%): Improvement potential
    - Freshness Score (5%): Content update requirements
    - Trend Score (5%): Rising/declining interest
    """

    # Expected CTR by position (industry averages)
    EXPECTED_CTR = {
        1: 0.316,   # 31.6%
        2: 0.157,   # 15.7%
        3: 0.105,   # 10.5%
        4: 0.075,   # 7.5%
        5: 0.059,   # 5.9%
        6: 0.048,   # 4.8%
        7: 0.041,   # 4.1%
        8: 0.035,   # 3.5%
        9: 0.031,   # 3.1%
        10: 0.027,  # 2.7%
        11: 0.018,  # 1.8%
        12: 0.015,  # 1.5%
        13: 0.013,  # 1.3%
        14: 0.012,  # 1.2%
        15: 0.011,  # 1.1%
        16: 0.010,  # 1.0%
        17: 0.009,  # 0.9%
        18: 0.008,  # 0.8%
        19: 0.008,  # 0.8%
        20: 0.007,  # 0.7%
    }

    def calculate_score(
        self,
        keyword_data: Dict[str, Any],
        opportunity_type: OpportunityType = OpportunityType.QUICK_WIN,
        search_volume: Optional[int] = None,
        difficulty: Optional[int] = None,
        serp_features: Optional[list] = None,
        cluster_value: Optional[int] = None,
        trend_direction: Optional[str] = None,
        trend_percent: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive opportunity score.

        Args:
            keyword_data: GSC data with position, impressions, clicks, ctr
            opportunity_type: Type of opportunity being scored
            search_volume: Monthly search volume (from DataForSEO)
            difficulty: SEO difficulty 0-100 (from DataForSEO)
            serp_features: SERP features present
            cluster_value: Strategic value of topic cluster (0-100)
            trend_direction: 'rising', 'stable', or 'declining'
            trend_percent: Percent change in search volume

        Returns:
            Dict with final score and breakdown
        """
        scores = {
            'volume_score': 0,
            'position_score': 0,
            'intent_score': 0,
            'competition_score': 0,
            'cluster_score': 0,
            'ctr_score': 0,
            'freshness_score': 0,
            'trend_score': 0
        }

        # 1. Volume Score (25% weight)
        scores['volume_score'] = self._calculate_volume_score(
            keyword_data.get('impressions', 0),
            search_volume
        )

        # 2. Position Score (20% weight)
        scores['position_score'] = self._calculate_position_score(
            keyword_data.get('position', 100),
            opportunity_type
        )

        # 3. Intent Score (20% weight)
        scores['intent_score'] = self._calculate_intent_score(
            keyword_data.get('commercial_intent', 1.0)
        )

        # 4. Competition Score (15% weight)
        scores['competition_score'] = self._calculate_competition_score(
            difficulty
        )

        # 5. Cluster Score (10% weight)
        scores['cluster_score'] = cluster_value or 50  # Default mid-value

        # 6. CTR Score (5% weight)
        scores['ctr_score'] = self._calculate_ctr_score(
            keyword_data.get('position', 100),
            keyword_data.get('ctr', 0),
            keyword_data.get('impressions', 0),
            keyword_data.get('clicks', 0)
        )

        # 7. Freshness Score (5% weight)
        scores['freshness_score'] = self._calculate_freshness_score(
            serp_features
        )

        # 8. Trend Score (5% weight)
        scores['trend_score'] = self._calculate_trend_score(
            trend_direction,
            trend_percent
        )

        # Calculate weighted total
        final_score = (
            scores['volume_score'] * 0.25 +
            scores['position_score'] * 0.20 +
            scores['intent_score'] * 0.20 +
            scores['competition_score'] * 0.15 +
            scores['cluster_score'] * 0.10 +
            scores['ctr_score'] * 0.05 +
            scores['freshness_score'] * 0.05 +
            scores['trend_score'] * 0.05
        )

        # Determine priority level
        priority = self._determine_priority(final_score, opportunity_type, scores)

        # Identify primary factor driving the score
        primary_factor = max(
            {k: v for k, v in scores.items() if v > 0}.items(),
            key=lambda x: x[1],
            default=('volume_score', 0)
        )[0].replace('_score', '')

        return {
            'final_score': round(final_score, 2),
            'score_breakdown': {k: round(v, 1) for k, v in scores.items()},
            'priority': priority,
            'primary_factor': primary_factor,
            'score_explanation': self._explain_score(scores, priority)
        }

    def _calculate_volume_score(
        self,
        impressions: int,
        search_volume: Optional[int] = None
    ) -> float:
        """Score based on search demand (0-100)"""
        # Prefer search volume if available, fall back to impressions
        volume = search_volume or impressions

        if volume >= 5000:
            return 100
        elif volume >= 2000:
            return 90
        elif volume >= 1000:
            return 80
        elif volume >= 500:
            return 65
        elif volume >= 250:
            return 50
        elif volume >= 100:
            return 35
        elif volume >= 50:
            return 20
        else:
            return 10

    def _calculate_position_score(
        self,
        position: float,
        opportunity_type: OpportunityType
    ) -> float:
        """Score based on proximity to target position (0-100)"""
        if opportunity_type == OpportunityType.QUICK_WIN:
            # Target: Move from 11-20 to page 1
            if position <= 12:
                return 100  # Very close to page 1
            elif position <= 15:
                return 85   # Close to page 1
            elif position <= 18:
                return 70   # Middle of page 2
            elif position <= 20:
                return 55   # Bottom of page 2
            else:
                return 30   # Beyond page 2

        elif opportunity_type == OpportunityType.IMPROVEMENT:
            # Target: Move from page 1 to top 3
            if position <= 5 and position >= 4:
                return 100  # Very close to top 3
            elif position <= 7:
                return 85   # Close to top 3
            elif position <= 10:
                return 70   # Bottom of page 1
            else:
                return 40

        elif opportunity_type == OpportunityType.MEDIUM_TERM:
            # Target: Move from 21-50 to page 1
            if position <= 30:
                return 70   # Page 3
            elif position <= 40:
                return 50   # Page 4
            elif position <= 50:
                return 30   # Page 5
            else:
                return 10

        elif opportunity_type == OpportunityType.NEW_CONTENT:
            # Not ranking yet - score based on competitor difficulty
            return 60  # Default moderate score for new opportunities

        else:
            return 50  # Default mid-score

    def _calculate_intent_score(self, commercial_intent: float) -> float:
        """Score based on commercial value (0-100)"""
        # commercial_intent is 0.1-3.0 from GSC module
        return (commercial_intent / 3.0) * 100

    def _calculate_competition_score(
        self,
        difficulty: Optional[int]
    ) -> float:
        """Score based on ranking difficulty (0-100)"""
        if difficulty is None:
            return 50  # Default mid-score if unknown

        # Invert difficulty - lower difficulty = higher score
        if difficulty <= 20:
            return 100  # Very easy
        elif difficulty <= 35:
            return 85   # Easy
        elif difficulty <= 50:
            return 70   # Moderate
        elif difficulty <= 65:
            return 50   # Difficult
        elif difficulty <= 80:
            return 30   # Very difficult
        else:
            return 10   # Extremely difficult

    def _calculate_ctr_score(
        self,
        position: float,
        ctr: float,
        impressions: int,
        clicks: int
    ) -> float:
        """Score based on CTR improvement potential (0-100)"""
        if position > 20 or position < 1:
            return 50  # Default if position out of range

        # Get expected CTR for this position
        pos_int = int(round(position))
        expected_ctr = self.EXPECTED_CTR.get(pos_int, 0.005)

        # Calculate actual CTR if not provided
        if ctr == 0 and impressions > 0 and clicks > 0:
            ctr = clicks / impressions

        # Score based on how far below expected we are
        if ctr < expected_ctr * 0.3:
            return 100  # WAY below expected - huge opportunity
        elif ctr < expected_ctr * 0.5:
            return 85   # Significantly below expected
        elif ctr < expected_ctr * 0.7:
            return 70   # Below expected
        elif ctr < expected_ctr * 0.9:
            return 50   # Slightly below expected
        else:
            return 30   # At or above expected - less opportunity

    def _calculate_freshness_score(
        self,
        serp_features: Optional[list]
    ) -> float:
        """Score based on SERP freshness requirements (0-100)"""
        if not serp_features:
            return 50  # Default if unknown

        # SERP features that indicate freshness is important
        freshness_indicators = [
            'top_stories',
            'news_results',
            'video',  # Videos often dated
        ]

        # Check for freshness signals
        has_freshness_signals = any(
            feature in str(serp_features).lower()
            for feature in freshness_indicators
        )

        if has_freshness_signals:
            return 90  # High score - fresh content has advantage
        else:
            return 50  # Normal - freshness less critical

    def _calculate_trend_score(
        self,
        trend_direction: Optional[str],
        trend_percent: Optional[float]
    ) -> float:
        """Score based on search trend (0-100)"""
        if not trend_direction:
            return 50  # Default if unknown

        if trend_direction == 'rising':
            # Higher score for faster growth
            if trend_percent and trend_percent >= 100:
                return 100  # Doubling or more
            elif trend_percent and trend_percent >= 50:
                return 85   # Strong growth
            elif trend_percent and trend_percent >= 20:
                return 70   # Good growth
            else:
                return 60   # Rising

        elif trend_direction == 'stable':
            return 50  # Neutral

        elif trend_direction == 'declining':
            # Lower score for declining topics
            if trend_percent and trend_percent <= -50:
                return 10   # Major decline
            elif trend_percent and trend_percent <= -20:
                return 25   # Significant decline
            else:
                return 35   # Declining

        return 50  # Default

    def _determine_priority(
        self,
        final_score: float,
        opportunity_type: OpportunityType,
        scores: Dict[str, float]
    ) -> str:
        """Determine priority level based on score and type"""
        # Critical: Very high score OR high commercial intent + good position
        if final_score >= 80:
            return 'CRITICAL'

        if (opportunity_type == OpportunityType.QUICK_WIN and
            scores['intent_score'] >= 66 and  # High commercial intent
            scores['position_score'] >= 85):   # Very close to page 1
            return 'CRITICAL'

        # High: Good score and opportunity
        if final_score >= 65:
            return 'HIGH'

        # Medium: Moderate score
        if final_score >= 45:
            return 'MEDIUM'

        # Low: Lower score
        if final_score >= 25:
            return 'LOW'

        # Skip: Very low score, not worth pursuing
        return 'SKIP'

    def _explain_score(
        self,
        scores: Dict[str, float],
        priority: str
    ) -> str:
        """Generate human-readable explanation of the score"""
        explanations = []

        # Identify strengths (scores > 70)
        strengths = [k.replace('_score', '') for k, v in scores.items() if v >= 70]
        if strengths:
            strength_text = ', '.join(strengths)
            explanations.append(f"Strong {strength_text}")

        # Identify weaknesses (scores < 40)
        weaknesses = [k.replace('_score', '') for k, v in scores.items() if v < 40 and v > 0]
        if weaknesses:
            weakness_text = ', '.join(weaknesses)
            explanations.append(f"Weak {weakness_text}")

        # Priority-specific explanations
        if priority == 'CRITICAL':
            explanations.append("IMMEDIATE ACTION RECOMMENDED")
        elif priority == 'SKIP':
            explanations.append("Not recommended - focus on higher priorities")

        return ". ".join(explanations) if explanations else "Balanced opportunity"


    def calculate_potential_traffic(
        self,
        current_position: float,
        target_position: int,
        impressions: int,
        current_clicks: int
    ) -> Dict[str, Any]:
        """
        Calculate potential traffic increase from ranking improvement.

        Args:
            current_position: Current average position
            target_position: Target position to reach
            impressions: Monthly impressions
            current_clicks: Current monthly clicks

        Returns:
            Dict with traffic projections
        """
        # Get current and target CTRs
        current_pos_int = int(round(current_position))
        current_expected_ctr = self.EXPECTED_CTR.get(current_pos_int, 0.005)
        target_expected_ctr = self.EXPECTED_CTR.get(target_position, 0.055)

        # Calculate potential clicks
        potential_clicks = int(impressions * target_expected_ctr)
        additional_clicks = potential_clicks - current_clicks
        percent_increase = ((additional_clicks / current_clicks * 100)
                          if current_clicks > 0 else 0)

        return {
            'current_clicks': current_clicks,
            'current_position': current_position,
            'current_ctr': round(current_clicks / impressions * 100, 2) if impressions > 0 else 0,
            'current_expected_ctr': round(current_expected_ctr * 100, 2),
            'target_position': target_position,
            'target_expected_ctr': round(target_expected_ctr * 100, 2),
            'potential_clicks': potential_clicks,
            'additional_clicks': additional_clicks,
            'percent_increase': round(percent_increase, 1)
        }


if __name__ == "__main__":
    # Example usage
    scorer = OpportunityScorer()

    # Example: Quick win opportunity
    keyword_data = {
        'keyword': 'project management software',
        'position': 12.3,
        'impressions': 1500,
        'clicks': 15,
        'ctr': 0.01,
        'commercial_intent': 2.5  # High commercial intent
    }

    result = scorer.calculate_score(
        keyword_data=keyword_data,
        opportunity_type=OpportunityType.QUICK_WIN,
        search_volume=2000,
        difficulty=45,
        serp_features=['featured_snippet', 'people_also_ask'],
        cluster_value=75,
        trend_direction='rising',
        trend_percent=25
    )

    print("Opportunity Score Analysis")
    print("=" * 60)
    print(f"Keyword: {keyword_data['keyword']}")
    print(f"Final Score: {result['final_score']}/100")
    print(f"Priority: {result['priority']}")
    print(f"Primary Factor: {result['primary_factor']}")
    print(f"\nScore Breakdown:")
    for factor, score in result['score_breakdown'].items():
        print(f"  {factor}: {score}/100")
    print(f"\nExplanation: {result['score_explanation']}")

    # Calculate traffic potential
    traffic = scorer.calculate_potential_traffic(
        current_position=keyword_data['position'],
        target_position=7,
        impressions=keyword_data['impressions'],
        current_clicks=keyword_data['clicks']
    )

    print(f"\nTraffic Potential:")
    print(f"  Current: {traffic['current_clicks']} clicks/month (position {traffic['current_position']})")
    print(f"  Potential: {traffic['potential_clicks']} clicks/month (position {traffic['target_position']})")
    print(f"  Gain: +{traffic['additional_clicks']} clicks (+{traffic['percent_increase']}%)")
