"""
CRO Checker

Checklist-based conversion rate optimization audit for landing pages.
Evaluates content against CRO best practices with pass/fail criteria.

Categories:
- Headline best practices
- Value proposition
- Social proof
- CTAs
- Objection handling
- Risk reversal
- Urgency/scarcity
- Page structure
"""

import re
from typing import Dict, List, Any, Optional


class CROChecker:
    """Checklist-based CRO audit for landing pages"""

    def __init__(self, page_type: str = 'seo', conversion_goal: str = 'trial'):
        """
        Initialize CRO Checker

        Args:
            page_type: 'seo' or 'ppc'
            conversion_goal: 'trial', 'demo', or 'lead'
        """
        self.page_type = page_type
        self.conversion_goal = conversion_goal

    def check(self, content: str) -> Dict[str, Any]:
        """
        Run CRO checklist against landing page content

        Args:
            content: Landing page content (markdown)

        Returns:
            Dict with checklist results and score
        """
        # Run all category checks
        categories = {
            'headline': self._check_headline(content),
            'value_proposition': self._check_value_proposition(content),
            'social_proof': self._check_social_proof(content),
            'ctas': self._check_ctas(content),
            'objection_handling': self._check_objection_handling(content),
            'risk_reversal': self._check_risk_reversal(content),
            'urgency': self._check_urgency(content),
            'structure': self._check_structure(content)
        }

        # Calculate scores
        total_checks = 0
        passed_checks = 0
        critical_failures = []
        warnings = []

        for category, results in categories.items():
            for check in results['checks']:
                total_checks += 1
                if check['passed']:
                    passed_checks += 1
                elif check['importance'] == 'critical':
                    critical_failures.append(f"{category}: {check['name']}")
                elif check['importance'] == 'important':
                    warnings.append(f"{category}: {check['name']}")

        # Overall score
        score = round((passed_checks / total_checks) * 100) if total_checks > 0 else 0

        # Determine if page passes CRO audit
        passes_audit = score >= 70 and len(critical_failures) == 0

        return {
            'score': score,
            'grade': self._get_grade(score),
            'passes_audit': passes_audit,
            'summary': {
                'total_checks': total_checks,
                'passed': passed_checks,
                'failed': total_checks - passed_checks,
                'critical_failures': len(critical_failures),
                'warnings': len(warnings)
            },
            'critical_failures': critical_failures,
            'warnings': warnings,
            'categories': categories,
            'checklist': self._generate_checklist(categories),
            'recommendations': self._generate_recommendations(categories)
        }

    def _check_headline(self, content: str) -> Dict[str, Any]:
        """Check headline best practices"""
        checks = []

        # Extract H1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        h1_text = h1_match.group(1) if h1_match else ""

        # Check: Headline present
        checks.append({
            'name': 'Headline present',
            'passed': bool(h1_text),
            'importance': 'critical',
            'detail': h1_text[:60] if h1_text else 'No H1 found'
        })

        # Check: Headline contains benefit
        benefit_words = ['save', 'grow', 'increase', 'improve', 'boost', 'launch', 'start',
                         'easy', 'fast', 'simple', 'free', 'without']
        has_benefit = any(word in h1_text.lower() for word in benefit_words) if h1_text else False
        checks.append({
            'name': 'Headline contains benefit',
            'passed': has_benefit,
            'importance': 'important',
            'detail': 'Benefit word found' if has_benefit else 'No clear benefit in headline'
        })

        # Check: Headline length
        good_length = 20 <= len(h1_text) <= 70 if h1_text else False
        checks.append({
            'name': 'Headline optimal length (20-70 chars)',
            'passed': good_length,
            'importance': 'nice_to_have',
            'detail': f'{len(h1_text)} characters' if h1_text else 'N/A'
        })

        # Check: Headline not generic
        generic_patterns = [r'^Welcome', r'^The\s+best', r'^Introducing', r'^We\s+']
        is_generic = any(re.search(p, h1_text, re.IGNORECASE) for p in generic_patterns) if h1_text else True
        checks.append({
            'name': 'Headline not generic',
            'passed': not is_generic,
            'importance': 'important',
            'detail': 'Appears unique' if not is_generic else 'Generic pattern detected'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_value_proposition(self, content: str) -> Dict[str, Any]:
        """Check value proposition clarity"""
        checks = []

        above_fold = content[:700]

        # Check: Value proposition present
        vp_patterns = [
            r'(?:help|helps)\s+(?:you\s+)?',
            r'(?:grow|launch|start|create)\s+your',
            r'(?:the\s+)?(?:easiest|fastest|best|only)\s+way',
            r'in\s+(?:just\s+)?\d+\s+(?:minutes?|seconds?)',
        ]
        has_vp = any(re.search(p, above_fold, re.IGNORECASE) for p in vp_patterns)
        checks.append({
            'name': 'Value proposition present',
            'passed': has_vp,
            'importance': 'critical',
            'detail': 'Value proposition found above fold' if has_vp else 'No clear value proposition'
        })

        # Check: Specificity (numbers/results)
        has_specifics = bool(re.search(r'\d+%?|\$\d+|\d+\s+(?:minutes?|days?)', above_fold))
        checks.append({
            'name': 'Value proposition has specifics',
            'passed': has_specifics,
            'importance': 'important',
            'detail': 'Specific numbers found' if has_specifics else 'Add specific numbers/results'
        })

        # Check: Target audience clear
        audience_patterns = [r'podcasters?', r'creators?', r'you(?:r)?', r'businesses?']
        addresses_audience = any(re.search(p, above_fold, re.IGNORECASE) for p in audience_patterns)
        checks.append({
            'name': 'Addresses target audience',
            'passed': addresses_audience,
            'importance': 'nice_to_have',
            'detail': 'Audience addressed' if addresses_audience else 'Make audience clearer'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_social_proof(self, content: str) -> Dict[str, Any]:
        """Check social proof elements"""
        checks = []

        # Check: Customer count
        has_count = bool(re.search(
            r'\d{1,3}(?:,\d{3})*\+?\s*(?:podcasters?|customers?|users?)',
            content, re.IGNORECASE
        ))
        checks.append({
            'name': 'Customer count displayed',
            'passed': has_count,
            'importance': 'important',
            'detail': 'Customer count found' if has_count else 'Add customer count'
        })

        # Check: Testimonials
        testimonial_count = len(re.findall(r'"[^"]{20,200}"', content))
        has_testimonials = testimonial_count >= 1
        checks.append({
            'name': 'Has testimonial(s)',
            'passed': has_testimonials,
            'importance': 'critical' if self.page_type == 'seo' else 'important',
            'detail': f'{testimonial_count} testimonial(s) found' if has_testimonials else 'Add testimonials'
        })

        # Check: Testimonials have attribution
        has_attribution = bool(re.search(r'—\s*\*?\*?[A-Z][a-z]+', content))
        checks.append({
            'name': 'Testimonials have names',
            'passed': has_attribution or not has_testimonials,  # Pass if no testimonials to attribute
            'importance': 'important',
            'detail': 'Attribution found' if has_attribution else 'Add names to testimonials'
        })

        # Check: Specific results in testimonials
        has_specific_results = bool(re.search(
            r'"[^"]*(?:\d+%|\d+x|\$\d+|\d{1,3}(?:,\d{3})*\s*(?:downloads?|subscribers?))[^"]*"',
            content
        ))
        checks.append({
            'name': 'Testimonials include specific results',
            'passed': has_specific_results,
            'importance': 'nice_to_have',
            'detail': 'Specific results found' if has_specific_results else 'Add numbers to testimonials'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_ctas(self, content: str) -> Dict[str, Any]:
        """Check CTA effectiveness"""
        checks = []

        # Find all CTAs
        cta_pattern = r'\[([^\]]{5,60})→?\]|\*\*\[([^\]]{5,60})\]\*\*'
        ctas = re.findall(cta_pattern, content)
        cta_count = len(ctas)

        # Check: CTA present
        checks.append({
            'name': 'Has CTA(s)',
            'passed': cta_count >= 1,
            'importance': 'critical',
            'detail': f'{cta_count} CTA(s) found' if cta_count else 'No CTAs found'
        })

        # Check: CTA count appropriate
        if self.page_type == 'seo':
            good_count = 3 <= cta_count <= 6
        else:
            good_count = 2 <= cta_count <= 4

        checks.append({
            'name': 'Appropriate CTA count',
            'passed': good_count,
            'importance': 'important',
            'detail': f'{cta_count} CTAs (target: {"3-6" if self.page_type == "seo" else "2-4"})'
        })

        # Check: CTA has action verb
        action_verbs = ['start', 'get', 'try', 'begin', 'launch', 'download', 'book', 'schedule', 'claim']
        cta_texts = [c[0] or c[1] for c in ctas] if ctas else []
        has_action = any(
            any(verb in cta.lower() for verb in action_verbs)
            for cta in cta_texts
        )
        checks.append({
            'name': 'CTA has action verb',
            'passed': has_action or cta_count == 0,
            'importance': 'important',
            'detail': 'Action verb found' if has_action else 'Add action verb to CTA'
        })

        # Check: CTA above fold
        above_fold = content[:700]
        cta_above = bool(re.search(cta_pattern, above_fold))
        checks.append({
            'name': 'CTA visible above fold',
            'passed': cta_above,
            'importance': 'critical',
            'detail': 'CTA above fold' if cta_above else 'Add CTA above the fold'
        })

        # Check: Goal-aligned CTA
        goal_patterns = {
            'trial': [r'free\s+trial', r'try\s+free', r'start\s+free'],
            'demo': [r'demo', r'schedule', r'book\s+a?\s*call'],
            'lead': [r'download', r'get\s+(?:the\s+)?(?:free\s+)?guide', r'access']
        }
        patterns = goal_patterns.get(self.conversion_goal, [])
        goal_aligned = any(
            any(re.search(p, cta, re.IGNORECASE) for p in patterns)
            for cta in cta_texts
        ) if patterns else True

        checks.append({
            'name': f'CTA aligned with {self.conversion_goal} goal',
            'passed': goal_aligned or cta_count == 0,
            'importance': 'important',
            'detail': 'Goal-aligned' if goal_aligned else f'Use {self.conversion_goal}-focused CTA text'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_objection_handling(self, content: str) -> Dict[str, Any]:
        """Check objection handling"""
        checks = []

        # Check: FAQ section
        has_faq = bool(re.search(r'(?:FAQ|Frequently\s+Asked|Questions?)', content, re.IGNORECASE))
        # Also check for Q&A pattern
        qa_pattern = r'\*\*[^*]+\?\*\*'
        has_qa = len(re.findall(qa_pattern, content)) >= 2

        checks.append({
            'name': 'FAQ or Q&A section',
            'passed': has_faq or has_qa,
            'importance': 'important' if self.page_type == 'seo' else 'nice_to_have',
            'detail': 'FAQ section found' if has_faq or has_qa else 'Add FAQ section'
        })

        # Check: Addresses common objections
        objection_patterns = [
            r'(?:easy|simple|no\s+(?:technical|coding))',  # Complexity objection
            r'(?:affordable|pricing|free|cost)',           # Price objection
            r'(?:support|help|24/7)',                       # Support objection
            r'(?:migrate|switch|transfer)',                 # Switching objection
        ]
        objections_addressed = sum(
            1 for p in objection_patterns
            if re.search(p, content, re.IGNORECASE)
        )
        checks.append({
            'name': 'Addresses potential objections',
            'passed': objections_addressed >= 2,
            'importance': 'nice_to_have',
            'detail': f'{objections_addressed} objection areas addressed'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_risk_reversal(self, content: str) -> Dict[str, Any]:
        """Check risk reversal elements"""
        checks = []

        # Check: Free trial mentioned
        has_trial = bool(re.search(
            r'free\s+(?:for\s+)?\d*\s*(?:day)?\s*trial|try\s+(?:for\s+)?free',
            content, re.IGNORECASE
        ))
        checks.append({
            'name': 'Free trial mentioned',
            'passed': has_trial,
            'importance': 'critical' if self.conversion_goal == 'trial' else 'important',
            'detail': 'Free trial mentioned' if has_trial else 'Add free trial offer'
        })

        # Check: No credit card
        has_no_card = bool(re.search(r'no\s+credit\s+card', content, re.IGNORECASE))
        checks.append({
            'name': 'No credit card required',
            'passed': has_no_card,
            'importance': 'important',
            'detail': 'No card required mentioned' if has_no_card else 'Add "no credit card required"'
        })

        # Check: Cancel anytime
        has_cancel = bool(re.search(r'cancel\s+(?:any\s*time|whenever)', content, re.IGNORECASE))
        checks.append({
            'name': 'Cancel anytime mentioned',
            'passed': has_cancel,
            'importance': 'nice_to_have',
            'detail': 'Cancel policy mentioned' if has_cancel else 'Add cancel policy'
        })

        # Check: Risk reversal near CTA
        # Look for risk reversal text within 200 chars of CTA
        cta_positions = [m.start() for m in re.finditer(r'\[.{5,60}→?\]', content)]
        risk_patterns = r'(?:no\s+credit\s+card|cancel\s+any|free\s+trial|guarantee|risk[- ]?free)'

        risk_near_cta = False
        for pos in cta_positions:
            nearby = content[max(0, pos-200):pos+200]
            if re.search(risk_patterns, nearby, re.IGNORECASE):
                risk_near_cta = True
                break

        checks.append({
            'name': 'Risk reversal near CTA',
            'passed': risk_near_cta,
            'importance': 'important',
            'detail': 'Risk reversal near CTA' if risk_near_cta else 'Add risk reversal near CTA buttons'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_urgency(self, content: str) -> Dict[str, Any]:
        """Check urgency/scarcity elements (use sparingly)"""
        checks = []

        urgency_patterns = [
            r'(?:today|now|immediately)',
            r'(?:limited|exclusive|only)',
            r'(?:don\'t\s+miss|last\s+chance)',
        ]

        urgency_count = sum(
            1 for p in urgency_patterns
            if re.search(p, content, re.IGNORECASE)
        )

        # Check: Has some urgency (but not required)
        checks.append({
            'name': 'Uses urgency appropriately',
            'passed': urgency_count >= 1,
            'importance': 'nice_to_have',
            'detail': f'{urgency_count} urgency elements' if urgency_count else 'Consider adding mild urgency'
        })

        # Check: Not over-using urgency
        checks.append({
            'name': 'Urgency not excessive',
            'passed': urgency_count <= 5,
            'importance': 'important',
            'detail': 'Appropriate urgency level' if urgency_count <= 5 else 'Reduce urgency - may seem pushy'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _check_structure(self, content: str) -> Dict[str, Any]:
        """Check page structure"""
        checks = []

        # Check: Has multiple sections
        h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
        if self.page_type == 'seo':
            good_sections = h2_count >= 4
        else:
            good_sections = h2_count >= 2

        checks.append({
            'name': 'Has adequate sections',
            'passed': good_sections,
            'importance': 'important',
            'detail': f'{h2_count} sections (H2s)'
        })

        # Check: Uses bullet lists
        has_lists = bool(re.search(r'^\s*[-*]\s+', content, re.MULTILINE))
        checks.append({
            'name': 'Uses bullet lists',
            'passed': has_lists,
            'importance': 'nice_to_have',
            'detail': 'Bullet lists found' if has_lists else 'Add bullet lists for scannability'
        })

        # Check: Uses bold for emphasis
        bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))
        checks.append({
            'name': 'Uses bold for emphasis',
            'passed': bold_count >= 3,
            'importance': 'nice_to_have',
            'detail': f'{bold_count} bold elements'
        })

        # Check: Word count appropriate
        word_count = len(content.split())
        if self.page_type == 'seo':
            good_length = 1500 <= word_count <= 2500
        else:
            good_length = 400 <= word_count <= 800

        checks.append({
            'name': 'Appropriate content length',
            'passed': good_length,
            'importance': 'important',
            'detail': f'{word_count} words (target: {"1500-2500" if self.page_type == "seo" else "400-800"})'
        })

        passed = sum(1 for c in checks if c['passed'])
        return {
            'score': round((passed / len(checks)) * 100),
            'checks': checks
        }

    def _generate_checklist(self, categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate flat checklist from all categories"""
        checklist = []
        for category, data in categories.items():
            for check in data['checks']:
                checklist.append({
                    'category': category,
                    'check': check['name'],
                    'passed': check['passed'],
                    'importance': check['importance'],
                    'detail': check['detail']
                })
        return checklist

    def _generate_recommendations(self, categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations from failed checks"""
        recommendations = []

        priority_map = {'critical': 0, 'important': 1, 'nice_to_have': 2}

        for category, data in categories.items():
            for check in data['checks']:
                if not check['passed']:
                    recommendations.append({
                        'priority': check['importance'],
                        'category': category,
                        'check': check['name'],
                        'recommendation': check['detail']
                    })

        # Sort by priority
        recommendations.sort(key=lambda x: priority_map.get(x['priority'], 3))
        return recommendations

    def _get_grade(self, score: int) -> str:
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
def check_cro(
    content: str,
    page_type: str = 'seo',
    conversion_goal: str = 'trial'
) -> Dict[str, Any]:
    """
    Run CRO checklist on landing page content

    Args:
        content: Landing page content (markdown)
        page_type: 'seo' or 'ppc'
        conversion_goal: 'trial', 'demo', or 'lead'

    Returns:
        CRO checklist results
    """
    checker = CROChecker(page_type, conversion_goal)
    return checker.check(content)


# Example usage
if __name__ == "__main__":
    sample_content = """
# Launch Your Product in 5 Minutes

The easiest way to get started. Join 50,000+ customers who trust us.

**[Start Your Free Trial →]**

## Why Customers Choose Us

- **Unlimited storage** - No caps, ever
- **Easy setup** - One click to get started
- **Great analytics** - Know your audience

"This product helped me grow my audience by 300% in year one."
— **Sarah M., Acme Corp**

## How It Works

1. Sign up (takes 2 minutes)
2. Upload your first episode
3. Publish everywhere

**[Try Free for 14 Days →]**

## FAQ

**Do I need a credit card?**
No credit card required. Cancel anytime.

**How long is the free trial?**
14 days of full access.

## Ready to Start?

**[Start Your Free Trial →]**

No credit card required. Cancel anytime. Set up in under 5 minutes.
    """

    result = check_cro(sample_content, page_type='seo', conversion_goal='trial')

    print("=== CRO Checklist Results ===")
    print(f"\nScore: {result['score']}/100")
    print(f"Grade: {result['grade']}")
    print(f"Passes Audit: {result['passes_audit']}")

    print(f"\nSummary:")
    print(f"  Passed: {result['summary']['passed']}/{result['summary']['total_checks']}")
    print(f"  Critical Failures: {result['summary']['critical_failures']}")
    print(f"  Warnings: {result['summary']['warnings']}")

    if result['critical_failures']:
        print(f"\n❌ Critical Failures:")
        for failure in result['critical_failures']:
            print(f"  - {failure}")

    print(f"\nCategory Scores:")
    for category, data in result['categories'].items():
        print(f"  {category}: {data['score']}%")

    if result['recommendations'][:5]:
        print(f"\nTop Recommendations:")
        for rec in result['recommendations'][:5]:
            print(f"  [{rec['priority'].upper()}] {rec['category']}: {rec['recommendation']}")
