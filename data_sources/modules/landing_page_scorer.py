"""
Landing Page Scorer

Scores landing pages (0-100) against CRO best practices.
Supports both SEO landing pages and PPC landing pages with different scoring criteria.

Categories (weights):
- Above-the-fold (25%): Headline, value prop, CTA visibility, trust signal
- CTAs (25%): Quality, distribution, goal alignment
- Trust signals (20%): Testimonials, social proof, risk reversals
- Structure (15%): Benefit-focused, scannable, appropriate length
- SEO (15%): Meta, keywords, links (for SEO pages only)
"""

import re
from typing import Dict, List, Optional, Any


class LandingPageScorer:
    """Scores landing pages against CRO best practices"""

    # Page type configurations
    PAGE_CONFIGS = {
        'seo': {
            'min_word_count': 1500,
            'optimal_word_count': 2000,
            'max_word_count': 2500,
            'min_ctas': 3,
            'optimal_ctas': 5,
            'internal_links': 2,  # Allow some internal links
        },
        'ppc': {
            'min_word_count': 400,
            'optimal_word_count': 600,
            'max_word_count': 800,
            'min_ctas': 2,
            'optimal_ctas': 3,
            'internal_links': 0,  # Minimize distractions
        }
    }

    # Goal-specific CTA patterns
    GOAL_CTA_PATTERNS = {
        'trial': [
            r'(?:start|begin|try|get)\s+(?:your\s+)?free\s+trial',
            r'try\s+(?:it\s+)?free',
            r'start\s+(?:for\s+)?free',
            r'free\s+for\s+\d+\s+days',
            r'no\s+credit\s+card',
        ],
        'demo': [
            r'(?:book|schedule|request|get)\s+(?:a\s+)?demo',
            r'(?:talk|speak)\s+to\s+(?:sales|an?\s+expert)',
            r'see\s+(?:it\s+)?in\s+action',
            r'(?:schedule|book)\s+(?:a\s+)?call',
        ],
        'lead': [
            r'(?:download|get)\s+(?:the\s+)?(?:free\s+)?(?:guide|ebook|checklist|template)',
            r'get\s+(?:your\s+)?(?:free\s+)?(?:copy|access)',
            r'(?:subscribe|sign\s+up)\s+(?:for\s+)?(?:our\s+)?(?:newsletter|updates)',
            r'join\s+(?:\d+[,\d]*\+?\s+)?(?:podcasters?|creators?|people)',
        ]
    }

    # Strong action verbs for CTAs
    CTA_ACTION_VERBS = [
        'start', 'get', 'try', 'begin', 'launch', 'create', 'download',
        'book', 'schedule', 'claim', 'unlock', 'discover', 'join'
    ]

    # Benefit-oriented CTA words
    CTA_BENEFIT_WORDS = [
        'free', 'instant', 'today', 'now', 'easy', 'fast', 'quick',
        'unlimited', 'exclusive', 'premium'
    ]

    # Urgency words
    CTA_URGENCY_WORDS = [
        'now', 'today', 'limited', 'hurry', 'don\'t miss', 'last chance',
        'expires', 'only', 'before'
    ]

    # Trust signal patterns
    TRUST_PATTERNS = {
        'testimonial': [
            r'"[^"]{20,200}"',  # Quoted text
            r'—\s*[A-Z][a-z]+',  # Attribution dash
            r'\*\*[A-Z][a-z]+\s+[A-Z]\.\*\*',  # **Name L.**
        ],
        'customer_count': [
            r'\d{1,3}(?:,\d{3})*\+?\s+(?:podcasters?|customers?|users?|creators?|businesses?)',
            r'(?:thousands|millions)\s+of\s+(?:podcasters?|customers?|users?)',
            r'trusted\s+by\s+\d+',
        ],
        'specific_results': [
            r'\d+%\s+(?:increase|decrease|growth|improvement)',
            r'(?:saved?|grew?|increased?)\s+(?:by\s+)?\$?\d+',
            r'\d+x\s+(?:more|growth|increase)',
        ],
        'risk_reversal': [
            r'no\s+credit\s+card',
            r'(?:money[- ]?back|satisfaction)\s+guarantee',
            r'cancel\s+(?:any\s*time|whenever)',
            r'risk[- ]?free',
            r'free\s+(?:for\s+)?\d+[- ]?days?',
        ],
        'authority': [
            r'(?:as\s+)?(?:seen|featured)\s+(?:in|on)',
            r'(?:award|certified|recognized)',
            r'(?:partner|integrated)\s+with',
        ]
    }

    # Generic/weak headline patterns (to penalize)
    WEAK_HEADLINE_PATTERNS = [
        r'^Welcome\s+to',
        r'^The\s+(?:best|ultimate|complete)',
        r'^(?:Everything|All)\s+you\s+need',
        r'^Introducing\s+',
        r'^We\s+(?:help|offer|provide)',
        r'^Our\s+(?:product|service|solution)',
    ]

    # Strong headline patterns (to reward)
    STRONG_HEADLINE_PATTERNS = [
        r'^\d+',  # Opens with number
        r'\?$',  # Ends with question
        r'(?:without|no\s+more)\s+',  # Pain point removal
        r'(?:finally|at\s+last)',  # Solution arrival
        r'(?:save|grow|increase|boost)',  # Benefit verb
    ]

    def __init__(
        self,
        page_type: str = 'seo',
        conversion_goal: str = 'trial'
    ):
        """
        Initialize Landing Page Scorer

        Args:
            page_type: 'seo' or 'ppc'
            conversion_goal: 'trial', 'demo', or 'lead'
        """
        self.page_type = page_type
        self.conversion_goal = conversion_goal
        self.config = self.PAGE_CONFIGS.get(page_type, self.PAGE_CONFIGS['seo'])

    def score(
        self,
        content: str,
        meta_title: Optional[str] = None,
        meta_description: Optional[str] = None,
        primary_keyword: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Score landing page against CRO best practices

        Args:
            content: Landing page content (markdown)
            meta_title: Meta title tag
            meta_description: Meta description tag
            primary_keyword: Target keyword (for SEO pages)

        Returns:
            Dict with overall score, category scores, and recommendations
        """
        # Analyze structure
        structure = self._analyze_structure(content)

        # Score each category
        above_fold_score = self._score_above_fold(content, structure)
        cta_score = self._score_ctas(content, structure)
        trust_score = self._score_trust_signals(content)
        structure_score = self._score_structure(content, structure)

        # SEO score only for SEO pages
        if self.page_type == 'seo':
            seo_score = self._score_seo(
                content, structure, meta_title, meta_description, primary_keyword
            )
        else:
            # PPC pages don't need SEO scoring
            seo_score = {'score': 100, 'critical': [], 'warnings': [], 'suggestions': []}

        # Calculate overall score (weighted average)
        if self.page_type == 'seo':
            weights = {
                'above_fold': 0.25,
                'ctas': 0.25,
                'trust': 0.20,
                'structure': 0.15,
                'seo': 0.15
            }
        else:
            # PPC pages: redistribute SEO weight
            weights = {
                'above_fold': 0.30,
                'ctas': 0.30,
                'trust': 0.25,
                'structure': 0.15,
                'seo': 0.00
            }

        overall_score = (
            above_fold_score['score'] * weights['above_fold'] +
            cta_score['score'] * weights['ctas'] +
            trust_score['score'] * weights['trust'] +
            structure_score['score'] * weights['structure'] +
            seo_score['score'] * weights['seo']
        )

        # Compile all issues
        critical_issues = []
        warnings = []
        suggestions = []

        for category in [above_fold_score, cta_score, trust_score, structure_score, seo_score]:
            critical_issues.extend(category.get('critical', []))
            warnings.extend(category.get('warnings', []))
            suggestions.extend(category.get('suggestions', []))

        return {
            'overall_score': round(overall_score, 1),
            'grade': self._get_grade(overall_score),
            'page_type': self.page_type,
            'conversion_goal': self.conversion_goal,
            'category_scores': {
                'above_fold': above_fold_score['score'],
                'ctas': cta_score['score'],
                'trust_signals': trust_score['score'],
                'structure': structure_score['score'],
                'seo': seo_score['score'] if self.page_type == 'seo' else 'N/A'
            },
            'critical_issues': critical_issues,
            'warnings': warnings,
            'suggestions': suggestions,
            'publishing_ready': overall_score >= 75 and len(critical_issues) == 0,
            'details': {
                'word_count': structure['word_count'],
                'cta_count': structure['cta_count'],
                'headline': structure.get('h1_text', '')[:60],
                'has_value_prop': structure.get('has_value_prop', False),
                'trust_signal_count': structure.get('trust_signal_count', 0)
            }
        }

    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze landing page structure"""
        lines = content.split('\n')

        # Extract headings
        h1_text = ""
        h2_texts = []
        h2_count = 0

        for line in lines:
            h1_match = re.match(r'^#\s+(.+)$', line)
            h2_match = re.match(r'^##\s+(.+)$', line)

            if h1_match and not h1_text:
                h1_text = h1_match.group(1)
            elif h2_match:
                h2_count += 1
                h2_texts.append(h2_match.group(1))

        # Word count
        word_count = len(content.split())

        # CTA detection
        cta_count = 0
        cta_positions = []

        # Check for button-style CTAs
        button_ctas = re.findall(r'\[.{5,60}→?\]|\*\*\[.{5,60}\]', content)
        cta_count += len(button_ctas)

        # Check for goal-specific CTAs
        goal_patterns = self.GOAL_CTA_PATTERNS.get(self.conversion_goal, [])
        for pattern in goal_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            cta_count += len(matches)
            for match in matches:
                pos_pct = match.start() / len(content) * 100
                cta_positions.append(pos_pct)

        # Above-the-fold content (first 500-700 characters)
        above_fold = content[:700]

        # Value proposition detection
        value_prop_patterns = [
            r'help\s+(?:you\s+)?(?:to\s+)?(?:\w+\s+){0,3}',
            r'(?:grow|launch|start|create|build)\s+your',
            r'(?:save|reduce|eliminate)\s+',
            r'(?:the\s+)?(?:easiest|fastest|best|only)\s+way',
        ]
        has_value_prop = any(
            re.search(p, above_fold, re.IGNORECASE)
            for p in value_prop_patterns
        )

        # Trust signal count
        trust_count = 0
        for signal_type, patterns in self.TRUST_PATTERNS.items():
            for pattern in patterns:
                trust_count += len(re.findall(pattern, content, re.IGNORECASE))

        return {
            'word_count': word_count,
            'h1_text': h1_text,
            'h2_count': h2_count,
            'h2_texts': h2_texts,
            'cta_count': cta_count,
            'cta_positions': cta_positions,
            'above_fold': above_fold,
            'has_value_prop': has_value_prop,
            'trust_signal_count': trust_count
        }

    def _score_above_fold(self, content: str, structure: Dict) -> Dict[str, Any]:
        """Score above-the-fold elements"""
        score = 100
        critical = []
        warnings = []
        suggestions = []

        above_fold = structure['above_fold']
        h1_text = structure['h1_text']

        # 1. Headline presence and quality (40 points)
        if not h1_text:
            score -= 40
            critical.append("Missing headline (H1)")
        else:
            # Check for weak headlines
            for pattern in self.WEAK_HEADLINE_PATTERNS:
                if re.search(pattern, h1_text, re.IGNORECASE):
                    score -= 15
                    warnings.append(f"Headline may be too generic: '{h1_text[:50]}...'")
                    break

            # Check for strong headlines
            has_strong = any(
                re.search(p, h1_text, re.IGNORECASE)
                for p in self.STRONG_HEADLINE_PATTERNS
            )
            if not has_strong:
                score -= 5
                suggestions.append("Headline could be stronger. Consider adding a number, benefit, or question.")

            # Headline length
            if len(h1_text) > 70:
                score -= 5
                suggestions.append(f"Headline is long ({len(h1_text)} chars). Consider shortening to <70 chars.")

        # 2. Value proposition (25 points)
        if not structure['has_value_prop']:
            score -= 25
            warnings.append("No clear value proposition found above the fold")

        # 3. CTA visibility above fold (25 points)
        cta_in_above_fold = any(
            re.search(pattern, above_fold, re.IGNORECASE)
            for patterns in self.GOAL_CTA_PATTERNS.values()
            for pattern in patterns
        ) or re.search(r'\[.{5,60}→?\]', above_fold)

        if not cta_in_above_fold:
            score -= 25
            critical.append("No CTA visible above the fold")

        # 4. Trust signal above fold (10 points)
        trust_above_fold = False
        for patterns in self.TRUST_PATTERNS.values():
            for pattern in patterns:
                if re.search(pattern, above_fold, re.IGNORECASE):
                    trust_above_fold = True
                    break

        if not trust_above_fold:
            score -= 10
            suggestions.append("Consider adding a trust signal above the fold (customer count, testimonial, logo)")

        return {
            'score': max(0, score),
            'critical': critical,
            'warnings': warnings,
            'suggestions': suggestions
        }

    def _score_ctas(self, content: str, structure: Dict) -> Dict[str, Any]:
        """Score CTA effectiveness"""
        score = 100
        critical = []
        warnings = []
        suggestions = []

        cta_count = structure['cta_count']
        cta_positions = structure['cta_positions']
        min_ctas = self.config['min_ctas']
        optimal_ctas = self.config['optimal_ctas']

        # 1. CTA count (30 points)
        if cta_count == 0:
            score -= 40
            critical.append("No CTAs found on page")
        elif cta_count < min_ctas:
            score -= 20
            warnings.append(f"Too few CTAs ({cta_count}). Target is {min_ctas}-{optimal_ctas} CTAs.")
        elif cta_count > optimal_ctas + 2:
            score -= 10
            suggestions.append(f"Many CTAs ({cta_count}). Consider consolidating to avoid overwhelming visitors.")

        # 2. CTA distribution (25 points)
        if len(cta_positions) >= 2:
            has_early = any(p < 40 for p in cta_positions)
            has_late = any(p > 70 for p in cta_positions)

            if not has_early:
                score -= 15
                warnings.append("No CTA in first 40% of page. Add an early CTA.")
            if not has_late:
                score -= 10
                suggestions.append("No CTA in final section. Add a closing CTA.")
        elif cta_count == 1:
            score -= 15
            warnings.append("Only one CTA found. Add CTAs throughout the page.")

        # 3. Goal alignment (25 points)
        goal_patterns = self.GOAL_CTA_PATTERNS.get(self.conversion_goal, [])
        goal_aligned = any(
            re.search(pattern, content, re.IGNORECASE)
            for pattern in goal_patterns
        )

        if not goal_aligned:
            score -= 25
            critical.append(
                f"CTAs don't align with '{self.conversion_goal}' goal. "
                f"Use goal-specific language."
            )

        # 4. CTA quality (20 points)
        cta_text_samples = re.findall(r'\[([^\]]{5,60})\]', content)
        if cta_text_samples:
            has_action_verb = any(
                any(verb in cta.lower() for verb in self.CTA_ACTION_VERBS)
                for cta in cta_text_samples
            )
            has_benefit = any(
                any(word in cta.lower() for word in self.CTA_BENEFIT_WORDS)
                for cta in cta_text_samples
            )

            if not has_action_verb:
                score -= 10
                warnings.append("CTAs missing action verbs (Start, Get, Try, etc.)")
            if not has_benefit:
                score -= 10
                suggestions.append("CTAs could include benefit words (free, instant, today)")

        return {
            'score': max(0, score),
            'critical': critical,
            'warnings': warnings,
            'suggestions': suggestions
        }

    def _score_trust_signals(self, content: str) -> Dict[str, Any]:
        """Score trust signals"""
        score = 100
        critical = []
        warnings = []
        suggestions = []

        # Count each type of trust signal
        trust_counts = {}
        for signal_type, patterns in self.TRUST_PATTERNS.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, content, re.IGNORECASE))
            trust_counts[signal_type] = count

        # 1. Testimonials (30 points)
        if trust_counts.get('testimonial', 0) == 0:
            score -= 30
            warnings.append("No testimonials found. Add customer quotes with names.")
        elif trust_counts.get('testimonial', 0) < 2:
            score -= 10
            suggestions.append("Only 1 testimonial. Consider adding 2-3 for stronger proof.")

        # 2. Social proof (25 points)
        has_social_proof = (
            trust_counts.get('customer_count', 0) > 0 or
            trust_counts.get('specific_results', 0) > 0
        )
        if not has_social_proof:
            score -= 25
            warnings.append("No social proof (customer count, results). Add specific numbers.")

        # 3. Risk reversal (25 points)
        if trust_counts.get('risk_reversal', 0) == 0:
            score -= 25
            warnings.append(
                "No risk reversal found. Add 'no credit card', 'guarantee', or 'cancel anytime'."
            )

        # 4. Authority signals (20 points)
        if trust_counts.get('authority', 0) == 0:
            score -= 10
            suggestions.append("Consider adding authority signals (as seen in, awards, partners).")

        # Bonus for specific results
        if trust_counts.get('specific_results', 0) >= 2:
            score = min(100, score + 5)  # Bonus for multiple specific results

        return {
            'score': max(0, score),
            'critical': critical,
            'warnings': warnings,
            'suggestions': suggestions
        }

    def _score_structure(self, content: str, structure: Dict) -> Dict[str, Any]:
        """Score content structure"""
        score = 100
        critical = []
        warnings = []
        suggestions = []

        word_count = structure['word_count']
        min_words = self.config['min_word_count']
        optimal_words = self.config['optimal_word_count']
        max_words = self.config['max_word_count']

        # 1. Word count (40 points)
        if word_count < min_words * 0.7:
            score -= 40
            critical.append(
                f"Content too short ({word_count} words). "
                f"Minimum for {self.page_type.upper()} page is {min_words} words."
            )
        elif word_count < min_words:
            score -= 20
            warnings.append(
                f"Content slightly short ({word_count} words). "
                f"Target is {optimal_words} words."
            )
        elif word_count > max_words * 1.3:
            score -= 15
            warnings.append(
                f"Content may be too long for {self.page_type.upper()} page ({word_count} words). "
                f"Target is {min_words}-{max_words} words."
            )

        # 2. Scannability (30 points)
        h2_count = structure['h2_count']
        bullet_lists = len(re.findall(r'^\s*[-*]\s', content, re.MULTILINE))
        bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))

        if self.page_type == 'seo' and h2_count < 4:
            score -= 15
            warnings.append(f"Too few sections ({h2_count} H2s). Add more headings for scannability.")
        elif self.page_type == 'ppc' and h2_count < 2:
            score -= 15
            warnings.append("Add at least 2 section headings for structure.")

        if bullet_lists == 0:
            score -= 10
            suggestions.append("No bullet lists found. Use lists for benefits/features.")

        if bold_count < 3:
            score -= 5
            suggestions.append("Add bold text to highlight key points.")

        # 3. Benefit vs feature focus (30 points)
        benefit_words = ['save', 'grow', 'increase', 'improve', 'reduce', 'eliminate', 'easy', 'fast', 'simple']
        feature_words = ['feature', 'function', 'capability', 'specification', 'technology']

        benefit_count = sum(len(re.findall(rf'\b{word}\b', content, re.IGNORECASE)) for word in benefit_words)
        feature_count = sum(len(re.findall(rf'\b{word}\b', content, re.IGNORECASE)) for word in feature_words)

        if feature_count > benefit_count:
            score -= 15
            warnings.append("Content may be too feature-focused. Lead with benefits, not features.")

        return {
            'score': max(0, score),
            'critical': critical,
            'warnings': warnings,
            'suggestions': suggestions
        }

    def _score_seo(
        self,
        content: str,
        structure: Dict,
        meta_title: Optional[str],
        meta_description: Optional[str],
        primary_keyword: Optional[str]
    ) -> Dict[str, Any]:
        """Score SEO elements (for SEO pages only)"""
        score = 100
        critical = []
        warnings = []
        suggestions = []

        # 1. Meta title (35 points)
        if not meta_title:
            score -= 35
            critical.append("Meta title is missing")
        else:
            if len(meta_title) < 50:
                score -= 10
                warnings.append(f"Meta title too short ({len(meta_title)} chars). Target is 50-60.")
            elif len(meta_title) > 65:
                score -= 5
                suggestions.append(f"Meta title may be truncated ({len(meta_title)} chars).")

            if primary_keyword and primary_keyword.lower() not in meta_title.lower():
                score -= 10
                warnings.append(f"Keyword '{primary_keyword}' not in meta title")

        # 2. Meta description (35 points)
        if not meta_description:
            score -= 35
            critical.append("Meta description is missing")
        else:
            if len(meta_description) < 150:
                score -= 10
                warnings.append(f"Meta description too short ({len(meta_description)} chars). Target is 150-160.")
            elif len(meta_description) > 165:
                score -= 5
                suggestions.append(f"Meta description may be truncated ({len(meta_description)} chars).")

        # 3. Keyword in headline (15 points)
        if primary_keyword and structure['h1_text']:
            if primary_keyword.lower() not in structure['h1_text'].lower():
                score -= 15
                warnings.append(f"Keyword '{primary_keyword}' not in headline")

        # 4. Internal links (15 points)
        internal_links = len(re.findall(r'\[([^\]]+)\]\((?!/|http)', content))
        if internal_links < self.config['internal_links']:
            score -= 15
            suggestions.append(
                f"Add {self.config['internal_links'] - internal_links} internal links "
                f"to related pages."
            )

        return {
            'score': max(0, score),
            'critical': critical,
            'warnings': warnings,
            'suggestions': suggestions
        }

    def _get_grade(self, score: float) -> str:
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


# Convenience function
def score_landing_page(
    content: str,
    page_type: str = 'seo',
    conversion_goal: str = 'trial',
    meta_title: Optional[str] = None,
    meta_description: Optional[str] = None,
    primary_keyword: Optional[str] = None
) -> Dict[str, Any]:
    """
    Score a landing page against CRO best practices

    Args:
        content: Landing page content (markdown)
        page_type: 'seo' or 'ppc'
        conversion_goal: 'trial', 'demo', or 'lead'
        meta_title: Meta title tag
        meta_description: Meta description tag
        primary_keyword: Target keyword (for SEO pages)

    Returns:
        Landing page score with recommendations
    """
    scorer = LandingPageScorer(page_type, conversion_goal)
    return scorer.score(content, meta_title, meta_description, primary_keyword)


# Example usage
if __name__ == "__main__":
    sample_content = """
# Launch Your Product in Minutes, Not Months

**Meta Title**: Easy Product Hosting | Start Free Today - [YOUR COMPANY]
**Meta Description**: Get started in minutes with [YOUR COMPANY]. No technical skills needed. Free 14-day trial, no credit card required. Join 50,000+ customers today.
**Target Keyword**: product hosting
**Conversion Goal**: trial

---

Ready to get started? [YOUR COMPANY] makes it ridiculously simple.

50,000+ customers trust us. Here's why:

## Start Building Today, Not "Someday"

Most platforms make you jump through hoops. Complex dashboards. Confusing settings. Technical jargon.

[YOUR COMPANY] is different. Upload your content, configure your settings, and hit publish. That's it.

**[Start Your Free Trial →]**

## What You Get

- **Unlimited storage** - No caps, no surprises
- **Automatic distribution** - Everywhere your audience is
- **Built-in analytics** - See what's working
- **24/7 support** - Real humans, real help

## Real Results from Real Customers

"I launched in one afternoon. Six months later, I have 10,000 users."
— **Sarah M., The Creative Hour**

"[YOUR COMPANY] helped me grow my audience by 300% in year one. The analytics alone are worth it."
— **Marcus T., Tech Talk Daily**

## No Risk, All Reward

- Free 14-day trial
- No credit card required
- Cancel anytime

**[Start Your Free Trial →]**

Still have questions? [Book a quick demo](/demo) with our team.
    """

    result = score_landing_page(
        content=sample_content,
        page_type='seo',
        conversion_goal='trial',
        meta_title="Easy Product Hosting | Start Free Today - [YOUR COMPANY]",
        meta_description="Get started in minutes with [YOUR COMPANY]. No technical skills needed. Free 14-day trial, no credit card required. Join 50,000+ customers today.",
        primary_keyword="product hosting"
    )

    print("=== Landing Page Score Report ===")
    print(f"\nPage Type: {result['page_type'].upper()}")
    print(f"Conversion Goal: {result['conversion_goal']}")
    print(f"\nOverall Score: {result['overall_score']}/100")
    print(f"Grade: {result['grade']}")
    print(f"Publishing Ready: {result['publishing_ready']}")

    print(f"\nCategory Scores:")
    for category, score in result['category_scores'].items():
        print(f"  {category}: {score}")

    if result['critical_issues']:
        print(f"\nCritical Issues:")
        for issue in result['critical_issues']:
            print(f"  ❌ {issue}")

    if result['warnings']:
        print(f"\nWarnings:")
        for warning in result['warnings']:
            print(f"  ⚠️  {warning}")

    if result['suggestions']:
        print(f"\nSuggestions:")
        for suggestion in result['suggestions'][:3]:
            print(f"  💡 {suggestion}")
