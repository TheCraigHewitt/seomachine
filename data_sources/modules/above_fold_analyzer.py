"""
Above-the-Fold Analyzer

Analyzes the critical above-the-fold section of landing pages.
The first 500-700 characters are crucial for conversion - visitors
decide within 5 seconds whether to stay or leave.

Checks for:
- Headline presence and quality
- Value proposition clarity
- CTA visibility
- Trust signal presence
"""

import re
from typing import Dict, List, Any, Optional


class AboveFoldAnalyzer:
    """Analyzes above-the-fold content effectiveness"""

    # Approximate character count for above-the-fold (varies by design)
    ABOVE_FOLD_CHARS = 700

    # Strong headline indicators
    STRONG_HEADLINE_PATTERNS = [
        r'^\d+',                    # Opens with number
        r'\?$',                     # Ends with question
        r'(?:without|no\s+more)',   # Pain point removal
        r'(?:finally|at\s+last)',   # Solution arrival
        r'(?:save|grow|increase|boost|launch|start)', # Action/benefit verbs
        r'(?:free|instant|easy|fast|simple)', # Benefit words
    ]

    # Weak headline patterns to flag
    WEAK_HEADLINE_PATTERNS = [
        r'^Welcome\s+to',
        r'^The\s+(?:best|ultimate|complete)\s+',
        r'^(?:Everything|All)\s+you\s+need',
        r'^Introducing\s+',
        r'^We\s+(?:help|offer|provide)',
        r'^Our\s+(?:product|service|solution)',
        r'^[A-Z][a-z]+\s+is\s+a\s+',  # "X is a..."
    ]

    # Value proposition patterns
    VALUE_PROP_PATTERNS = [
        r'(?:help|helps)\s+(?:you\s+)?(?:to\s+)?',
        r'(?:grow|launch|start|create|build)\s+your',
        r'(?:save|reduce|eliminate)\s+',
        r'(?:the\s+)?(?:easiest|fastest|best|only|simplest)\s+way',
        r'(?:without|no)\s+(?:the\s+)?(?:hassle|complexity|confusion)',
        r'in\s+(?:just\s+)?\d+\s+(?:minutes?|seconds?|days?)',
    ]

    # CTA patterns
    CTA_PATTERNS = [
        r'\[.{5,60}→?\]',                        # [Text →] or [Text]
        r'\*\*\[.{5,60}\]\*\*',                  # **[Text]**
        r'(?:start|try|get|begin)\s+(?:your\s+)?(?:free\s+)?(?:trial|now|today)',
        r'(?:book|schedule|request)\s+(?:a\s+)?demo',
        r'(?:download|get)\s+(?:the\s+)?(?:free\s+)?(?:guide|ebook)',
    ]

    # Trust signal patterns
    TRUST_PATTERNS = [
        r'\d{1,3}(?:,\d{3})*\+?\s*(?:podcasters?|customers?|users?)',
        r'trusted\s+by',
        r'"[^"]{10,100}"',  # Short testimonial
        r'(?:\d(?:\.\d)?|\d\d?)/(?:5|10)\s*(?:stars?|rating)?',
        r'(?:as\s+)?(?:seen|featured)\s+(?:in|on)',
    ]

    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze above-the-fold content

        Args:
            content: Full landing page content (markdown)

        Returns:
            Dict with above-fold analysis results
        """
        # Extract above-the-fold content
        above_fold = content[:self.ABOVE_FOLD_CHARS]

        # Parse the content
        lines = content.split('\n')

        # Find headline (H1)
        headline_analysis = self._analyze_headline(lines)

        # Find value proposition
        value_prop_analysis = self._analyze_value_proposition(above_fold)

        # Find CTA
        cta_analysis = self._analyze_cta(above_fold)

        # Find trust signal
        trust_analysis = self._analyze_trust_signal(above_fold)

        # Calculate scores
        element_scores = {
            'headline': headline_analysis['score'],
            'value_prop': value_prop_analysis['score'],
            'cta': cta_analysis['score'],
            'trust': trust_analysis['score']
        }

        # Overall score (weighted)
        overall_score = (
            element_scores['headline'] * 0.35 +
            element_scores['value_prop'] * 0.25 +
            element_scores['cta'] * 0.25 +
            element_scores['trust'] * 0.15
        )

        # Generate issues and recommendations
        issues = self._identify_issues(
            headline_analysis, value_prop_analysis, cta_analysis, trust_analysis
        )

        return {
            'overall_score': round(overall_score, 1),
            'grade': self._get_grade(overall_score),
            'element_scores': element_scores,
            'passes_5_second_test': overall_score >= 70,
            'headline': headline_analysis,
            'value_proposition': value_prop_analysis,
            'cta': cta_analysis,
            'trust_signal': trust_analysis,
            'issues': issues,
            'recommendations': self._generate_recommendations(issues),
            'above_fold_preview': above_fold[:300] + '...'
        }

    def _analyze_headline(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze the headline (H1)"""
        h1_text = None
        h1_line_index = None

        for i, line in enumerate(lines):
            h1_match = re.match(r'^#\s+(.+)$', line)
            if h1_match:
                h1_text = h1_match.group(1).strip()
                h1_line_index = i
                break

        if not h1_text:
            return {
                'present': False,
                'text': None,
                'score': 0,
                'issues': ['No H1 headline found'],
                'quality': 'missing'
            }

        score = 60  # Base score for having a headline
        issues = []

        # Check for weak patterns
        for pattern in self.WEAK_HEADLINE_PATTERNS:
            if re.search(pattern, h1_text, re.IGNORECASE):
                score -= 30
                issues.append(f'Weak headline pattern detected')
                break

        # Check for strong patterns
        strong_count = 0
        for pattern in self.STRONG_HEADLINE_PATTERNS:
            if re.search(pattern, h1_text, re.IGNORECASE):
                strong_count += 1

        if strong_count >= 2:
            score += 30
        elif strong_count == 1:
            score += 15

        # Check length
        if len(h1_text) > 80:
            score -= 10
            issues.append(f'Headline too long ({len(h1_text)} chars)')
        elif len(h1_text) < 20:
            score -= 10
            issues.append(f'Headline too short ({len(h1_text)} chars)')

        # Check if it appears early (within first few lines)
        if h1_line_index and h1_line_index > 10:
            score -= 10
            issues.append('Headline appears too late in content')

        # Determine quality
        if score >= 80:
            quality = 'strong'
        elif score >= 60:
            quality = 'moderate'
        else:
            quality = 'weak'

        return {
            'present': True,
            'text': h1_text,
            'length': len(h1_text),
            'score': max(0, min(100, score)),
            'issues': issues,
            'quality': quality,
            'strong_elements': strong_count
        }

    def _analyze_value_proposition(self, above_fold: str) -> Dict[str, Any]:
        """Analyze value proposition presence and clarity"""
        score = 0
        found_patterns = []

        for pattern in self.VALUE_PROP_PATTERNS:
            if re.search(pattern, above_fold, re.IGNORECASE):
                score += 20
                found_patterns.append(pattern)

        # Cap the score
        score = min(100, score)

        # Adjust based on pattern quality
        if len(found_patterns) >= 3:
            score = 100  # Multiple value signals is excellent
        elif len(found_patterns) == 2:
            score = max(score, 80)
        elif len(found_patterns) == 1:
            score = max(score, 60)

        # Check for specificity (numbers make value props stronger)
        has_specifics = bool(re.search(r'\d+%?|\$\d+|#?\d+', above_fold))
        if has_specifics:
            score = min(100, score + 10)

        issues = []
        if score < 60:
            issues.append('Value proposition not clear above the fold')
        if not has_specifics and score > 0:
            issues.append('Value proposition lacks specifics (numbers, results)')

        return {
            'present': score > 0,
            'score': score,
            'patterns_found': len(found_patterns),
            'has_specifics': has_specifics,
            'issues': issues,
            'clarity': 'clear' if score >= 70 else 'unclear' if score < 40 else 'moderate'
        }

    def _analyze_cta(self, above_fold: str) -> Dict[str, Any]:
        """Analyze CTA presence above the fold"""
        ctas_found = []

        for pattern in self.CTA_PATTERNS:
            matches = re.finditer(pattern, above_fold, re.IGNORECASE)
            for match in matches:
                ctas_found.append({
                    'text': match.group()[:50],
                    'position': match.start()
                })

        if not ctas_found:
            return {
                'present': False,
                'count': 0,
                'score': 0,
                'issues': ['No CTA visible above the fold'],
                'first_cta_position': None
            }

        # Score based on presence and position
        score = 70  # Base score for having a CTA

        # Bonus for early placement
        first_position = ctas_found[0]['position']
        if first_position < 300:
            score += 20
        elif first_position < 500:
            score += 10

        # Check CTA quality (action verb)
        first_cta = ctas_found[0]['text'].lower()
        action_verbs = ['start', 'get', 'try', 'begin', 'launch', 'download', 'book', 'schedule']
        has_action_verb = any(verb in first_cta for verb in action_verbs)
        if has_action_verb:
            score += 10

        return {
            'present': True,
            'count': len(ctas_found),
            'score': min(100, score),
            'first_cta': ctas_found[0]['text'],
            'first_cta_position': first_position,
            'has_action_verb': has_action_verb,
            'issues': [] if score >= 70 else ['CTA could be more prominent']
        }

    def _analyze_trust_signal(self, above_fold: str) -> Dict[str, Any]:
        """Analyze trust signal presence above the fold"""
        signals_found = []

        for pattern in self.TRUST_PATTERNS:
            matches = re.finditer(pattern, above_fold, re.IGNORECASE)
            for match in matches:
                signals_found.append({
                    'text': match.group()[:60],
                    'position': match.start()
                })

        if not signals_found:
            return {
                'present': False,
                'count': 0,
                'score': 30,  # Not critical, but recommended
                'issues': ['No trust signal above the fold'],
                'signals': []
            }

        # Score based on presence
        score = 80
        if len(signals_found) >= 2:
            score = 100

        return {
            'present': True,
            'count': len(signals_found),
            'score': score,
            'signals': [s['text'] for s in signals_found[:3]],
            'issues': []
        }

    def _identify_issues(
        self,
        headline: Dict,
        value_prop: Dict,
        cta: Dict,
        trust: Dict
    ) -> List[Dict[str, Any]]:
        """Compile all issues"""
        issues = []

        # Critical issues
        if not headline['present']:
            issues.append({
                'severity': 'critical',
                'element': 'headline',
                'issue': 'Missing headline (H1)'
            })

        if not cta['present']:
            issues.append({
                'severity': 'critical',
                'element': 'cta',
                'issue': 'No CTA visible above the fold'
            })

        # Warnings
        if headline['present'] and headline['quality'] == 'weak':
            issues.append({
                'severity': 'warning',
                'element': 'headline',
                'issue': 'Headline is weak or generic'
            })

        if not value_prop['present'] or value_prop['clarity'] == 'unclear':
            issues.append({
                'severity': 'warning',
                'element': 'value_prop',
                'issue': 'Value proposition not clear'
            })

        # Suggestions
        if not trust['present']:
            issues.append({
                'severity': 'suggestion',
                'element': 'trust',
                'issue': 'Consider adding trust signal above the fold'
            })

        if cta['present'] and not cta.get('has_action_verb', True):
            issues.append({
                'severity': 'suggestion',
                'element': 'cta',
                'issue': 'CTA could use stronger action verb'
            })

        return issues

    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        for issue in issues:
            if issue['element'] == 'headline':
                if issue['severity'] == 'critical':
                    recommendations.append(
                        'Add a benefit-focused H1 headline immediately.'
                    )
                else:
                    recommendations.append(
                        'Strengthen headline: use numbers, questions, or benefit verbs.'
                    )

            elif issue['element'] == 'cta':
                if issue['severity'] == 'critical':
                    recommendations.append(
                        'Add a prominent CTA button above the fold.'
                    )
                else:
                    recommendations.append(
                        'Start CTA with action verb (Start, Get, Try).'
                    )

            elif issue['element'] == 'value_prop':
                recommendations.append(
                    'Clarify value proposition: state what visitor gets and how quickly.'
                )

            elif issue['element'] == 'trust':
                recommendations.append(
                    'Add trust signal: customer count, rating, or short testimonial.'
                )

        return recommendations

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Acceptable)"
        elif score >= 60:
            return "D (Needs Work)"
        else:
            return "F (Poor)"


# Convenience function
def analyze_above_fold(content: str) -> Dict[str, Any]:
    """
    Analyze above-the-fold content of a landing page

    Args:
        content: Full landing page content (markdown)

    Returns:
        Above-fold analysis results
    """
    analyzer = AboveFoldAnalyzer()
    return analyzer.analyze(content)


# Example usage
if __name__ == "__main__":
    sample_content = """
# Launch Your Product in 5 Minutes

The easiest way to start and grow your business. No technical skills needed.

Join 50,000+ customers who trust us.

**[Start Your Free Trial →]**

## Why Customers Love Our Product

Our platform makes everything simple...

[Rest of content...]
    """

    result = analyze_above_fold(sample_content)

    print("=== Above-the-Fold Analysis ===")
    print(f"\nOverall Score: {result['overall_score']}/100")
    print(f"Grade: {result['grade']}")
    print(f"Passes 5-Second Test: {result['passes_5_second_test']}")

    print(f"\nElement Scores:")
    for element, score in result['element_scores'].items():
        print(f"  {element}: {score}/100")

    print(f"\nHeadline: {result['headline']['text']}")
    print(f"  Quality: {result['headline']['quality']}")

    print(f"\nValue Proposition:")
    print(f"  Clarity: {result['value_proposition']['clarity']}")

    print(f"\nCTA:")
    if result['cta']['present']:
        print(f"  Text: {result['cta']['first_cta']}")
    else:
        print(f"  NOT FOUND")

    print(f"\nTrust Signal:")
    if result['trust_signal']['present']:
        print(f"  Found: {result['trust_signal']['signals']}")
    else:
        print(f"  NOT FOUND")

    if result['issues']:
        print(f"\nIssues:")
        for issue in result['issues']:
            severity = {'critical': '❌', 'warning': '⚠️', 'suggestion': '💡'}
            print(f"  {severity[issue['severity']]} {issue['issue']}")

    if result['recommendations']:
        print(f"\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  → {rec}")
