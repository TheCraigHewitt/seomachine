"""
Trust Signal Analyzer

Analyzes trust signals in landing page content:
- Testimonials (quotes with attribution)
- Social proof (customer counts, results)
- Authority signals (media mentions, certifications)
- Risk reversals (guarantees, free trials)
- Security indicators (privacy, data protection)
"""

import re
from typing import Dict, List, Any


class TrustSignalAnalyzer:
    """Analyzes trust signals in landing pages"""

    # Testimonial patterns
    TESTIMONIAL_PATTERNS = {
        'quoted_text': [
            r'"([^"]{20,300})"',           # Double-quoted testimonial
            r'"([^"]{20,300})"',           # Curly double quotes
            r"'([^']{20,300})'",           # Single quotes
        ],
        'attribution': [
            r'—\s*\*?\*?([A-Z][a-z]+(?:\s+[A-Z]\.?)?)',  # — Name or — Name L.
            r'[-–]\s*\*?\*?([A-Z][a-z]+(?:\s+[A-Z]\.?)?)',  # - Name
            r'\*\*([A-Z][a-z]+\s+[A-Z]\.?)\*\*',  # **Name L.**
        ],
        'with_company': [
            r'([A-Z][a-z]+(?:\s+[A-Z]\.?)?),\s*([A-Za-z\s]+(?:Podcast|Show|Co\.|Inc\.|LLC|Agency|Studio))',
        ]
    }

    # Customer count / social proof patterns
    SOCIAL_PROOF_PATTERNS = {
        'customer_count': [
            r'(\d{1,3}(?:,\d{3})*\+?)\s*(?:podcasters?|customers?|users?|creators?|businesses?|shows?)',
            r'(?:trusted|used|loved)\s+by\s+(\d{1,3}(?:,\d{3})*\+?)',
            r'(?:join|over)\s+(\d{1,3}(?:,\d{3})*\+?)\s*(?:podcasters?|customers?)',
            r'(\d+(?:\.\d+)?[KMBkmb])\+?\s*(?:podcasters?|downloads?|users?)',
        ],
        'specific_results': [
            r'(\d+%)\s+(?:increase|decrease|growth|improvement|more|less|higher|lower)',
            r'(?:increased?|grew?|improved?|boosted?|saved?)\s+(?:by\s+)?(\d+%)',
            r'(\d+x)\s+(?:more|growth|increase|improvement)',
            r'(?:\$|€|£)(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # Dollar amounts
            r'(\d{1,3}(?:,\d{3})*)\s+(?:downloads?|listens?|subscribers?|plays?)',
        ],
        'time_results': [
            r'in\s+(?:just\s+)?(\d+)\s*(?:minutes?|hours?|days?)',
            r'(\d+)\s*(?:minutes?|hours?)\s+(?:or\s+less|to\s+set\s+up)',
            r'(?:launched?|started?|set\s+up)\s+in\s+(\d+)',
        ]
    }

    # Risk reversal patterns
    RISK_REVERSAL_PATTERNS = {
        'free_trial': [
            r'free\s+(?:for\s+)?(\d+)[- ]?days?\s+trial',
            r'(\d+)[- ]?days?\s+free\s+trial',
            r'free\s+trial',
            r'try\s+(?:it\s+)?(?:for\s+)?free',
            r'start\s+free',
        ],
        'no_card': [
            r'no\s+credit\s+card\s+(?:required|needed)',
            r'(?:without|no)\s+(?:a\s+)?credit\s+card',
            r'credit\s+card\s+not\s+required',
        ],
        'cancel_anytime': [
            r'cancel\s+(?:any\s*time|whenever)',
            r'no\s+(?:commitment|contract|obligation)',
            r'(?:cancel|quit)\s+(?:any\s*time)',
            r'month[- ]to[- ]month',
        ],
        'guarantee': [
            r'(?:money[- ]?back|satisfaction)\s+guarantee',
            r'(\d+)[- ]?day\s+(?:money[- ]?back\s+)?guarantee',
            r'risk[- ]?free',
            r'full\s+refund',
            r'no\s+(?:risk|questions\s+asked)',
        ]
    }

    # Authority signals
    AUTHORITY_PATTERNS = {
        'media_mentions': [
            r'(?:as\s+)?(?:seen|featured|mentioned)\s+(?:in|on)\s+([A-Za-z\s,]+)',
            r'featured\s+(?:in|on)',
            r'as\s+seen\s+(?:in|on)',
        ],
        'awards': [
            r'(?:award|prize)[- ]?(?:winning|winner)',
            r'(?:best|top|leading)\s+(?:podcast|hosting|software|platform|tool)',
            r'(\d{4})\s+(?:award|winner)',
            r'rated\s+(?:#?\d|best)',
        ],
        'certifications': [
            r'(?:certified|accredited)\s+(?:by\s+)?([A-Za-z]+)',
            r'(?:IAB|SOC|GDPR|ISO)[- ]?\d*\s+(?:certified|compliant)',
        ],
        'partnerships': [
            r'(?:official|authorized)\s+(?:partner|integration)',
            r'(?:partner|integrated)\s+with\s+([A-Za-z\s,]+)',
            r'(?:Apple|Spotify|Google)\s+(?:partner|certified)',
        ],
        'experience': [
            r'(?:since|founded\s+in)\s+(\d{4})',
            r'(\d+)\+?\s+years?\s+(?:of\s+)?(?:experience|in\s+business)',
            r'(?:trusted\s+)?since\s+(\d{4})',
        ]
    }

    # Security patterns (for pages collecting data)
    SECURITY_PATTERNS = {
        'privacy': [
            r'privacy\s+(?:policy|protected|first)',
            r'(?:your\s+)?data\s+(?:is\s+)?(?:safe|secure|protected)',
            r'we\s+(?:never|don\'t)\s+(?:sell|share)\s+your',
        ],
        'encryption': [
            r'(?:SSL|TLS|256[- ]?bit)\s+(?:encryption|encrypted|secure)',
            r'(?:secure|encrypted)\s+(?:connection|checkout|payment)',
        ],
        'compliance': [
            r'(?:GDPR|CCPA|SOC\s*2?|HIPAA)\s*(?:compliant|certified)?',
        ]
    }

    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze trust signals in landing page content

        Args:
            content: Landing page content (markdown)

        Returns:
            Dict with trust signal analysis
        """
        results = {
            'testimonials': self._analyze_testimonials(content),
            'social_proof': self._analyze_social_proof(content),
            'risk_reversals': self._analyze_risk_reversals(content),
            'authority': self._analyze_authority(content),
            'security': self._analyze_security(content),
        }

        # Calculate overall score
        score = self._calculate_score(results)

        # Generate recommendations
        recommendations = self._generate_recommendations(results)

        return {
            'overall_score': score,
            'grade': self._get_grade(score),
            'summary': {
                'testimonials_found': results['testimonials']['count'],
                'has_social_proof': results['social_proof']['has_any'],
                'has_risk_reversal': results['risk_reversals']['has_any'],
                'authority_signals': results['authority']['count'],
                'security_present': results['security']['has_any']
            },
            'details': results,
            'recommendations': recommendations,
            'strengths': self._identify_strengths(results),
            'weaknesses': self._identify_weaknesses(results)
        }

    def _analyze_testimonials(self, content: str) -> Dict[str, Any]:
        """Analyze testimonials"""
        testimonials = []
        seen_quotes = set()

        for pattern in self.TESTIMONIAL_PATTERNS['quoted_text']:
            matches = re.finditer(pattern, content)
            for match in matches:
                quote = match.group(1)
                if quote not in seen_quotes and len(quote) >= 20:
                    seen_quotes.add(quote)

                    # Check for specificity (numbers, results)
                    has_specifics = bool(re.search(r'\d+%?|\$\d+|\d+x', quote))

                    # Look for attribution nearby
                    context_after = content[match.end():match.end() + 100]
                    attribution = None
                    for attr_pattern in self.TESTIMONIAL_PATTERNS['attribution']:
                        attr_match = re.search(attr_pattern, context_after)
                        if attr_match:
                            attribution = attr_match.group(1)
                            break

                    testimonials.append({
                        'quote': quote[:100] + ('...' if len(quote) > 100 else ''),
                        'attribution': attribution,
                        'has_specifics': has_specifics,
                        'quality': 'strong' if has_specifics and attribution else 'moderate' if attribution else 'weak'
                    })

        return {
            'count': len(testimonials),
            'testimonials': testimonials[:5],  # Limit to 5 for output
            'has_strong': any(t['quality'] == 'strong' for t in testimonials),
            'has_attributed': any(t['attribution'] for t in testimonials),
            'has_specifics': any(t['has_specifics'] for t in testimonials)
        }

    def _analyze_social_proof(self, content: str) -> Dict[str, Any]:
        """Analyze social proof signals"""
        results = {
            'customer_counts': [],
            'specific_results': [],
            'time_results': []
        }

        # Customer counts
        for pattern in self.SOCIAL_PROOF_PATTERNS['customer_count']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                count = match.group(1)
                if count not in [c['value'] for c in results['customer_counts']]:
                    results['customer_counts'].append({
                        'value': count,
                        'context': content[max(0, match.start() - 20):match.end() + 30].strip()
                    })

        # Specific results
        for pattern in self.SOCIAL_PROOF_PATTERNS['specific_results']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                value = match.group(1)
                results['specific_results'].append({
                    'value': value,
                    'context': content[max(0, match.start() - 30):match.end() + 30].strip()
                })

        # Time results
        for pattern in self.SOCIAL_PROOF_PATTERNS['time_results']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                results['time_results'].append({
                    'value': match.group(1) if match.groups() else match.group(),
                    'context': content[max(0, match.start() - 20):match.end() + 20].strip()
                })

        return {
            'customer_counts': results['customer_counts'][:3],
            'specific_results': results['specific_results'][:5],
            'time_results': results['time_results'][:3],
            'has_any': bool(results['customer_counts'] or results['specific_results']),
            'has_customer_count': bool(results['customer_counts']),
            'has_specific_results': bool(results['specific_results']),
            'total_count': len(results['customer_counts']) + len(results['specific_results'])
        }

    def _analyze_risk_reversals(self, content: str) -> Dict[str, Any]:
        """Analyze risk reversal signals"""
        results = {}

        for category, patterns in self.RISK_REVERSAL_PATTERNS.items():
            matches = []
            for pattern in patterns:
                found = re.finditer(pattern, content, re.IGNORECASE)
                for match in found:
                    matches.append({
                        'text': match.group(),
                        'position_pct': round(match.start() / len(content) * 100, 1)
                    })
            results[category] = {
                'found': bool(matches),
                'count': len(matches),
                'matches': matches[:2]  # Limit output
            }

        has_any = any(r['found'] for r in results.values())
        categories_present = sum(1 for r in results.values() if r['found'])

        return {
            'has_any': has_any,
            'categories_present': categories_present,
            'free_trial': results.get('free_trial', {}),
            'no_card': results.get('no_card', {}),
            'cancel_anytime': results.get('cancel_anytime', {}),
            'guarantee': results.get('guarantee', {}),
            'is_strong': categories_present >= 3
        }

    def _analyze_authority(self, content: str) -> Dict[str, Any]:
        """Analyze authority signals"""
        results = {}

        for category, patterns in self.AUTHORITY_PATTERNS.items():
            matches = []
            for pattern in patterns:
                found = re.finditer(pattern, content, re.IGNORECASE)
                for match in found:
                    matches.append(match.group())
            results[category] = {
                'found': bool(matches),
                'matches': list(set(matches))[:3]
            }

        count = sum(1 for r in results.values() if r['found'])

        return {
            'count': count,
            'has_media_mentions': results.get('media_mentions', {}).get('found', False),
            'has_awards': results.get('awards', {}).get('found', False),
            'has_certifications': results.get('certifications', {}).get('found', False),
            'has_partnerships': results.get('partnerships', {}).get('found', False),
            'has_experience': results.get('experience', {}).get('found', False),
            'details': results
        }

    def _analyze_security(self, content: str) -> Dict[str, Any]:
        """Analyze security signals"""
        results = {}

        for category, patterns in self.SECURITY_PATTERNS.items():
            matches = []
            for pattern in patterns:
                found = re.finditer(pattern, content, re.IGNORECASE)
                for match in found:
                    matches.append(match.group())
            results[category] = {
                'found': bool(matches),
                'matches': list(set(matches))[:2]
            }

        has_any = any(r['found'] for r in results.values())

        return {
            'has_any': has_any,
            'has_privacy': results.get('privacy', {}).get('found', False),
            'has_encryption': results.get('encryption', {}).get('found', False),
            'has_compliance': results.get('compliance', {}).get('found', False),
            'details': results
        }

    def _calculate_score(self, results: Dict[str, Any]) -> int:
        """Calculate overall trust signal score"""
        score = 0

        # Testimonials (up to 35 points)
        testimonials = results['testimonials']
        if testimonials['count'] >= 3:
            score += 25
        elif testimonials['count'] >= 2:
            score += 20
        elif testimonials['count'] >= 1:
            score += 10

        if testimonials['has_strong']:
            score += 10
        elif testimonials['has_attributed']:
            score += 5

        # Social proof (up to 30 points)
        social = results['social_proof']
        if social['has_customer_count']:
            score += 15
        if social['has_specific_results']:
            score += 15
        elif social['has_any']:
            score += 10

        # Risk reversals (up to 25 points)
        risk = results['risk_reversals']
        if risk['is_strong']:
            score += 25
        elif risk['categories_present'] >= 2:
            score += 20
        elif risk['has_any']:
            score += 10

        # Authority (up to 10 points)
        authority = results['authority']
        if authority['count'] >= 3:
            score += 10
        elif authority['count'] >= 1:
            score += 5

        return min(100, score)

    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Average)"
        elif score >= 60:
            return "D (Needs Work)"
        else:
            return "F (Poor)"

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Testimonials
        if results['testimonials']['count'] == 0:
            recommendations.append({
                'priority': 'high',
                'category': 'testimonials',
                'issue': 'No testimonials found',
                'recommendation': 'Add 2-3 customer testimonials with names and specific results.'
            })
        elif not results['testimonials']['has_specifics']:
            recommendations.append({
                'priority': 'medium',
                'category': 'testimonials',
                'issue': 'Testimonials lack specifics',
                'recommendation': 'Update testimonials to include specific numbers (e.g., "grew by 300%", "10,000 downloads").'
            })
        elif not results['testimonials']['has_attributed']:
            recommendations.append({
                'priority': 'medium',
                'category': 'testimonials',
                'issue': 'Testimonials missing attribution',
                'recommendation': 'Add names and titles to testimonials (e.g., "Sarah M., The Creative Hour").'
            })

        # Social proof
        if not results['social_proof']['has_customer_count']:
            recommendations.append({
                'priority': 'high',
                'category': 'social_proof',
                'issue': 'No customer count',
                'recommendation': 'Add customer count (e.g., "Join 50,000+ customers" or "Trusted by thousands").'
            })

        if not results['social_proof']['has_specific_results']:
            recommendations.append({
                'priority': 'medium',
                'category': 'social_proof',
                'issue': 'No specific results',
                'recommendation': 'Include specific customer results with numbers (e.g., "grew audience by 300%").'
            })

        # Risk reversals
        if not results['risk_reversals']['has_any']:
            recommendations.append({
                'priority': 'high',
                'category': 'risk_reversal',
                'issue': 'No risk reversal',
                'recommendation': 'Add risk reversal near CTAs: free trial length, no credit card, or guarantee.'
            })
        elif not results['risk_reversals']['is_strong']:
            recommendations.append({
                'priority': 'medium',
                'category': 'risk_reversal',
                'issue': 'Weak risk reversal',
                'recommendation': 'Strengthen risk reversal by adding: trial length, no credit card required, AND cancel anytime.'
            })

        # Authority
        if results['authority']['count'] == 0:
            recommendations.append({
                'priority': 'low',
                'category': 'authority',
                'issue': 'No authority signals',
                'recommendation': 'Consider adding: years in business, media mentions, awards, or partnerships.'
            })

        return sorted(recommendations, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])

    def _identify_strengths(self, results: Dict[str, Any]) -> List[str]:
        """Identify trust signal strengths"""
        strengths = []

        if results['testimonials']['has_strong']:
            strengths.append("Strong testimonials with specific results")
        if results['social_proof']['has_customer_count']:
            strengths.append(f"Customer count displayed")
        if results['risk_reversals']['is_strong']:
            strengths.append("Strong risk reversal (multiple elements)")
        if results['authority']['count'] >= 2:
            strengths.append(f"Multiple authority signals ({results['authority']['count']})")

        return strengths

    def _identify_weaknesses(self, results: Dict[str, Any]) -> List[str]:
        """Identify trust signal weaknesses"""
        weaknesses = []

        if results['testimonials']['count'] == 0:
            weaknesses.append("No testimonials")
        elif not results['testimonials']['has_attributed']:
            weaknesses.append("Testimonials lack attribution")

        if not results['social_proof']['has_any']:
            weaknesses.append("No social proof")
        if not results['risk_reversals']['has_any']:
            weaknesses.append("No risk reversal")

        return weaknesses


# Convenience function
def analyze_trust_signals(content: str) -> Dict[str, Any]:
    """
    Analyze trust signals in landing page content

    Args:
        content: Landing page content (markdown)

    Returns:
        Trust signal analysis results
    """
    analyzer = TrustSignalAnalyzer()
    return analyzer.analyze(content)


# Example usage
if __name__ == "__main__":
    sample_content = """
# Start Your Free Trial Today

Join 50,000+ customers who trust [YOUR COMPANY].

"[YOUR COMPANY] helped me grow my audience by 300% in the first year. The analytics alone are worth it."
— **Sarah M., The Creative Hour**

"I launched in one afternoon and had 10,000 users within 3 months."
— **Marcus T.**

## Why Customers Choose Us

- Unlimited storage
- Easy distribution

**[Start Your Free Trial →]**

14-day free trial. No credit card required. Cancel anytime.

As featured in Industry Business Journal.

Since 2017, we've helped creators launch successfully.
    """

    result = analyze_trust_signals(sample_content)

    print("=== Trust Signal Analysis ===")
    print(f"\nOverall Score: {result['overall_score']}/100")
    print(f"Grade: {result['grade']}")

    print(f"\nSummary:")
    for key, value in result['summary'].items():
        print(f"  {key}: {value}")

    print(f"\nStrengths:")
    for s in result['strengths']:
        print(f"  ✓ {s}")

    print(f"\nWeaknesses:")
    for w in result['weaknesses']:
        print(f"  ✗ {w}")

    if result['recommendations']:
        print(f"\nRecommendations:")
        for rec in result['recommendations'][:3]:
            print(f"  [{rec['priority'].upper()}] {rec['recommendation']}")
