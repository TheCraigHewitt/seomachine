"""
CTA Analyzer

Analyzes Call-to-Action elements in landing pages:
- Detects CTAs (buttons, links, forms)
- Scores CTA quality (action verbs, benefit-oriented, urgency)
- Analyzes placement distribution
- Checks goal alignment (trial vs demo vs lead)
"""

import re
from typing import Dict, List, Optional, Any


class CTAAnalyzer:
    """Analyzes CTA effectiveness in landing pages"""

    # Button-style CTA patterns
    BUTTON_PATTERNS = [
        r'\[([^\]]{5,60})→\]',           # [Text →]
        r'\*\*\[([^\]]{5,60})\]\*\*',    # **[Text]**
        r'\[([^\]]{5,60})\]\([^)]+\)',   # [Text](link)
    ]

    # Goal-specific CTA phrases
    GOAL_PATTERNS = {
        'trial': {
            'primary': [
                r'start\s+(?:your\s+)?(?:free\s+)?trial',
                r'try\s+(?:it\s+)?(?:for\s+)?free',
                r'get\s+started\s+(?:for\s+)?free',
                r'start\s+(?:for\s+)?free',
                r'begin\s+(?:your\s+)?(?:free\s+)?trial',
            ],
            'secondary': [
                r'sign\s+up\s+(?:for\s+)?free',
                r'create\s+(?:your\s+)?(?:free\s+)?account',
                r'launch\s+your',
                r'start\s+(?:your\s+)?(?:free\s+)?trial',
            ]
        },
        'demo': {
            'primary': [
                r'(?:book|schedule|request)\s+(?:a\s+)?demo',
                r'get\s+(?:a\s+)?demo',
                r'see\s+(?:it\s+)?in\s+action',
                r'(?:watch|view)\s+demo',
            ],
            'secondary': [
                r'(?:schedule|book)\s+(?:a\s+)?call',
                r'(?:talk|speak)\s+to\s+(?:sales|us|an?\s+expert)',
                r'contact\s+(?:sales|us)',
                r'get\s+(?:a\s+)?(?:personalized|custom)\s+',
            ]
        },
        'lead': {
            'primary': [
                r'(?:download|get)\s+(?:the\s+)?(?:free\s+)?(?:guide|ebook|checklist|template|pdf)',
                r'get\s+(?:instant\s+)?access',
                r'(?:download|get)\s+(?:your\s+)?(?:free\s+)?(?:copy)',
                r'claim\s+(?:your\s+)?(?:free\s+)?',
            ],
            'secondary': [
                r'(?:subscribe|sign\s+up)\s+(?:for|to)',
                r'join\s+(?:our\s+)?(?:newsletter|list|community)',
                r'get\s+(?:weekly|daily|monthly)\s+',
                r'stay\s+(?:updated|informed)',
            ]
        }
    }

    # Strong action verbs (good for CTAs)
    ACTION_VERBS = {
        'strongest': ['start', 'get', 'claim', 'unlock', 'discover'],
        'strong': ['try', 'begin', 'launch', 'create', 'download', 'book', 'schedule'],
        'moderate': ['learn', 'see', 'find', 'explore', 'read', 'watch'],
        'weak': ['submit', 'click', 'enter', 'continue', 'next']
    }

    # Benefit words that strengthen CTAs
    BENEFIT_WORDS = [
        'free', 'instant', 'immediate', 'today', 'now',
        'unlimited', 'exclusive', 'premium', 'full',
        'easy', 'fast', 'quick', 'simple'
    ]

    # Urgency words
    URGENCY_WORDS = [
        'now', 'today', 'immediately', 'instant',
        'limited', 'hurry', 'soon', 'before',
        'don\'t miss', 'last chance', 'expires', 'only'
    ]

    # Specificity indicators (make CTAs more concrete)
    SPECIFICITY_PATTERNS = [
        r'\d+[- ]?day',           # 14-day, 30-day
        r'\d+%',                  # percentages
        r'\$\d+',                 # dollar amounts
        r'(?:free|no)\s+(?:credit\s+card|payment)',
        r'in\s+\d+\s+(?:minutes?|seconds?)',
    ]

    def __init__(self, conversion_goal: str = 'trial'):
        """
        Initialize CTA Analyzer

        Args:
            conversion_goal: 'trial', 'demo', or 'lead'
        """
        self.conversion_goal = conversion_goal

    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze CTAs in landing page content

        Args:
            content: Landing page content (markdown)

        Returns:
            Dict with CTA analysis results
        """
        # Find all CTAs
        ctas = self._find_ctas(content)

        # Analyze distribution
        distribution = self._analyze_distribution(ctas, len(content))

        # Score each CTA
        scored_ctas = [self._score_cta(cta) for cta in ctas]

        # Check goal alignment
        goal_alignment = self._check_goal_alignment(content)

        # Calculate overall metrics
        avg_quality = sum(c['quality_score'] for c in scored_ctas) / len(scored_ctas) if scored_ctas else 0

        return {
            'summary': {
                'total_ctas': len(ctas),
                'average_quality_score': round(avg_quality, 1),
                'distribution_score': distribution['score'],
                'goal_alignment_score': goal_alignment['score'],
                'overall_effectiveness': round(
                    (avg_quality * 0.4 + distribution['score'] * 0.3 + goal_alignment['score'] * 0.3),
                    1
                )
            },
            'ctas': scored_ctas,
            'distribution': distribution,
            'goal_alignment': goal_alignment,
            'recommendations': self._generate_recommendations(scored_ctas, distribution, goal_alignment)
        }

    def _find_ctas(self, content: str) -> List[Dict[str, Any]]:
        """Find all CTAs in content"""
        ctas = []
        seen_texts = set()

        # Find button-style CTAs
        for pattern in self.BUTTON_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                text = match.group(1) if match.groups() else match.group()
                text_lower = text.lower().strip()

                if text_lower not in seen_texts:
                    seen_texts.add(text_lower)
                    ctas.append({
                        'text': text.strip(),
                        'position': match.start(),
                        'position_pct': round(match.start() / len(content) * 100, 1),
                        'type': 'button',
                        'full_match': match.group()
                    })

        # Find text CTAs matching goal patterns
        goal_patterns = self.GOAL_PATTERNS.get(self.conversion_goal, {})
        all_patterns = goal_patterns.get('primary', []) + goal_patterns.get('secondary', [])

        for pattern in all_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                text = match.group()
                text_lower = text.lower().strip()

                if text_lower not in seen_texts:
                    seen_texts.add(text_lower)
                    ctas.append({
                        'text': text.strip(),
                        'position': match.start(),
                        'position_pct': round(match.start() / len(content) * 100, 1),
                        'type': 'text',
                        'full_match': match.group()
                    })

        # Sort by position
        ctas.sort(key=lambda x: x['position'])
        return ctas

    def _score_cta(self, cta: Dict[str, Any]) -> Dict[str, Any]:
        """Score an individual CTA"""
        text = cta['text'].lower()
        score = 50  # Base score
        factors = []

        # 1. Action verb strength (up to +30)
        for strength, verbs in self.ACTION_VERBS.items():
            if any(verb in text for verb in verbs):
                if strength == 'strongest':
                    score += 30
                    factors.append(f"+30: Strong action verb")
                elif strength == 'strong':
                    score += 25
                    factors.append(f"+25: Good action verb")
                elif strength == 'moderate':
                    score += 15
                    factors.append(f"+15: Moderate action verb")
                else:
                    score += 5
                    factors.append(f"+5: Weak action verb")
                break
        else:
            factors.append("-10: No clear action verb")
            score -= 10

        # 2. Benefit words (up to +15)
        benefit_count = sum(1 for word in self.BENEFIT_WORDS if word in text)
        if benefit_count >= 2:
            score += 15
            factors.append(f"+15: Multiple benefit words ({benefit_count})")
        elif benefit_count == 1:
            score += 10
            factors.append("+10: Has benefit word")

        # 3. Urgency (up to +10)
        if any(word in text for word in self.URGENCY_WORDS):
            score += 10
            factors.append("+10: Creates urgency")

        # 4. Specificity (up to +10)
        for pattern in self.SPECIFICITY_PATTERNS:
            if re.search(pattern, cta['text'], re.IGNORECASE):
                score += 10
                factors.append("+10: Specific details")
                break

        # 5. Length optimization
        word_count = len(text.split())
        if 2 <= word_count <= 5:
            score += 5
            factors.append("+5: Optimal length")
        elif word_count > 8:
            score -= 10
            factors.append("-10: Too long")

        # 6. Button type bonus
        if cta['type'] == 'button':
            score += 5
            factors.append("+5: Button format")

        return {
            **cta,
            'quality_score': max(0, min(100, score)),
            'scoring_factors': factors
        }

    def _analyze_distribution(self, ctas: List[Dict], content_length: int) -> Dict[str, Any]:
        """Analyze CTA distribution throughout the page"""
        if not ctas:
            return {
                'score': 0,
                'first_cta_position': None,
                'last_cta_position': None,
                'has_above_fold': False,
                'has_mid_page': False,
                'has_closing': False,
                'distribution_quality': 'none',
                'issues': ['No CTAs found']
            }

        positions = [c['position_pct'] for c in ctas]
        issues = []

        # Calculate distribution metrics
        first_pos = positions[0]
        last_pos = positions[-1]

        has_above_fold = any(p < 20 for p in positions)
        has_mid_page = any(30 < p < 70 for p in positions)
        has_closing = any(p > 80 for p in positions)

        # Score distribution
        score = 40  # Base score for having at least one CTA

        if has_above_fold:
            score += 20
        else:
            issues.append("No CTA above the fold (first 20%)")

        if has_mid_page:
            score += 20
        else:
            issues.append("No CTA in middle of page (30-70%)")

        if has_closing:
            score += 20
        else:
            issues.append("No closing CTA (last 20%)")

        # Bonus for good first CTA placement
        if first_pos < 15:
            score += 10
        elif first_pos > 40:
            score -= 10
            issues.append(f"First CTA appears late ({first_pos:.0f}% into page)")

        # Determine distribution quality
        coverage = sum([has_above_fold, has_mid_page, has_closing])
        if coverage == 3:
            quality = 'excellent'
        elif coverage == 2:
            quality = 'good'
        elif coverage == 1:
            quality = 'poor'
        else:
            quality = 'none'

        return {
            'score': max(0, min(100, score)),
            'first_cta_position': round(first_pos, 1),
            'last_cta_position': round(last_pos, 1),
            'has_above_fold': has_above_fold,
            'has_mid_page': has_mid_page,
            'has_closing': has_closing,
            'distribution_quality': quality,
            'cta_count': len(ctas),
            'issues': issues
        }

    def _check_goal_alignment(self, content: str) -> Dict[str, Any]:
        """Check if CTAs align with conversion goal"""
        goal_patterns = self.GOAL_PATTERNS.get(self.conversion_goal, {})
        primary_patterns = goal_patterns.get('primary', [])
        secondary_patterns = goal_patterns.get('secondary', [])

        # Count matches
        primary_matches = 0
        secondary_matches = 0

        for pattern in primary_patterns:
            primary_matches += len(re.findall(pattern, content, re.IGNORECASE))

        for pattern in secondary_patterns:
            secondary_matches += len(re.findall(pattern, content, re.IGNORECASE))

        # Calculate score
        score = 0
        issues = []
        strengths = []

        if primary_matches >= 2:
            score = 100
            strengths.append(f"Strong primary goal alignment ({primary_matches} matches)")
        elif primary_matches == 1:
            score = 80
            strengths.append(f"Good primary goal alignment")
            issues.append("Consider adding more goal-aligned CTAs")
        elif secondary_matches >= 2:
            score = 60
            strengths.append(f"Secondary goal alignment ({secondary_matches} matches)")
            issues.append("Add primary goal CTAs for stronger conversion")
        elif secondary_matches == 1:
            score = 40
            issues.append("Weak goal alignment - add more targeted CTAs")
        else:
            score = 20
            issues.append(f"CTAs don't align with '{self.conversion_goal}' goal")

        # Check for conflicting goals
        other_goals = [g for g in self.GOAL_PATTERNS.keys() if g != self.conversion_goal]
        conflicting = 0
        for other_goal in other_goals:
            for pattern in self.GOAL_PATTERNS[other_goal].get('primary', []):
                conflicting += len(re.findall(pattern, content, re.IGNORECASE))

        if conflicting > primary_matches + secondary_matches:
            score -= 20
            issues.append("More CTAs for other goals than the target goal - confusing focus")

        return {
            'score': max(0, min(100, score)),
            'goal': self.conversion_goal,
            'primary_matches': primary_matches,
            'secondary_matches': secondary_matches,
            'conflicting_matches': conflicting,
            'issues': issues,
            'strengths': strengths
        }

    def _generate_recommendations(
        self,
        scored_ctas: List[Dict],
        distribution: Dict,
        goal_alignment: Dict
    ) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Distribution recommendations
        if not distribution['has_above_fold']:
            recommendations.append({
                'priority': 'high',
                'category': 'distribution',
                'issue': 'No CTA above the fold',
                'recommendation': 'Add a prominent CTA in the first 20% of the page, ideally right after the headline.'
            })

        if not distribution['has_closing']:
            recommendations.append({
                'priority': 'high',
                'category': 'distribution',
                'issue': 'No closing CTA',
                'recommendation': 'Add a strong CTA at the end of the page to capture visitors who read through.'
            })

        if distribution['cta_count'] < 3:
            recommendations.append({
                'priority': 'medium',
                'category': 'distribution',
                'issue': f'Only {distribution["cta_count"]} CTA(s) found',
                'recommendation': 'Add CTAs throughout the page. Aim for 3-5 CTAs distributed across sections.'
            })

        # Goal alignment recommendations
        if goal_alignment['score'] < 60:
            goal_examples = {
                'trial': 'Start Your Free Trial, Try Free for 14 Days',
                'demo': 'Book a Demo, See It in Action',
                'lead': 'Download the Free Guide, Get Instant Access'
            }
            recommendations.append({
                'priority': 'high',
                'category': 'goal_alignment',
                'issue': f'CTAs not aligned with {self.conversion_goal} goal',
                'recommendation': f'Use goal-specific CTA text. Examples: {goal_examples.get(self.conversion_goal, "")}'
            })

        # Quality recommendations
        low_quality_ctas = [c for c in scored_ctas if c['quality_score'] < 60]
        if low_quality_ctas:
            recommendations.append({
                'priority': 'medium',
                'category': 'quality',
                'issue': f'{len(low_quality_ctas)} CTA(s) have low quality scores',
                'recommendation': 'Improve CTAs by: (1) Starting with action verbs (Start, Get, Try), (2) Adding benefit words (free, instant), (3) Creating urgency (today, now).'
            })

        # Check for action verbs
        weak_verb_ctas = [
            c for c in scored_ctas
            if not any(
                verb in c['text'].lower()
                for verbs in [self.ACTION_VERBS['strongest'], self.ACTION_VERBS['strong']]
                for verb in verbs
            )
        ]
        if weak_verb_ctas:
            recommendations.append({
                'priority': 'medium',
                'category': 'quality',
                'issue': 'Some CTAs lack strong action verbs',
                'recommendation': 'Replace weak verbs with strong ones: Start (not Begin), Get (not Receive), Try (not Test).'
            })

        return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])


# Convenience function
def analyze_ctas(
    content: str,
    conversion_goal: str = 'trial'
) -> Dict[str, Any]:
    """
    Analyze CTAs in landing page content

    Args:
        content: Landing page content (markdown)
        conversion_goal: 'trial', 'demo', or 'lead'

    Returns:
        CTA analysis results
    """
    analyzer = CTAAnalyzer(conversion_goal)
    return analyzer.analyze(content)


# Example usage
if __name__ == "__main__":
    sample_content = """
# Start Your Journey Today

Launch your product in minutes.

**[Start Your Free Trial →]**

## Why Choose Us?

- Unlimited storage
- Easy setup
- Great analytics

Over 50,000 customers trust us.

Learn more about our features.

## Ready to Begin?

**[Try Free for 14 Days →]**

No credit card required. Cancel anytime.

Questions? [Book a demo](/demo) with our team.
    """

    result = analyze_ctas(sample_content, conversion_goal='trial')

    print("=== CTA Analysis Report ===")
    print(f"\nSummary:")
    print(f"  Total CTAs: {result['summary']['total_ctas']}")
    print(f"  Average Quality: {result['summary']['average_quality_score']}/100")
    print(f"  Distribution Score: {result['summary']['distribution_score']}/100")
    print(f"  Goal Alignment: {result['summary']['goal_alignment_score']}/100")
    print(f"  Overall Effectiveness: {result['summary']['overall_effectiveness']}/100")

    print(f"\nCTAs Found:")
    for cta in result['ctas']:
        print(f"  [{cta['position_pct']:.0f}%] \"{cta['text']}\" (Score: {cta['quality_score']})")

    print(f"\nDistribution: {result['distribution']['distribution_quality']}")
    for issue in result['distribution']['issues']:
        print(f"  ⚠️  {issue}")

    print(f"\nGoal Alignment ({result['goal_alignment']['goal']}):")
    print(f"  Primary matches: {result['goal_alignment']['primary_matches']}")
    print(f"  Secondary matches: {result['goal_alignment']['secondary_matches']}")

    if result['recommendations']:
        print(f"\nTop Recommendations:")
        for rec in result['recommendations'][:3]:
            print(f"  [{rec['priority'].upper()}] {rec['recommendation']}")
