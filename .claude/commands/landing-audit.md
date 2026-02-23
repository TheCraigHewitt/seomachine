# Landing Page Audit Command

Audit existing landing pages for conversion optimization opportunities.

## Usage
`/landing-audit [URL or file path] --goal [trial|demo|lead]`

**Examples:**
- `/landing-audit https://yoursite.com/pricing/ --goal trial`
- `/landing-audit landing-pages/product-hosting-beginners-2025-12-11.md --goal trial`

**Default:** `--goal trial`

## Analysis Modules

| Module | Path | Analyzes |
|--------|------|----------|
| Landing Page Scorer | `data_sources/modules/landing_page_scorer.py` | Overall 0-100 score, category scores, critical issues, publish readiness |
| Above-the-Fold | `data_sources/modules/above_fold_analyzer.py` | Headline quality, value prop clarity, CTA visibility, 5-second test |
| CTA Analyzer | `data_sources/modules/cta_analyzer.py` | CTA count, distribution, quality scoring, goal alignment |
| Trust Signal | `data_sources/modules/trust_signal_analyzer.py` | Testimonials, social proof, risk reversal, authority signals |
| CRO Checker | `data_sources/modules/cro_checker.py` | 30+ checklist items, pass/fail per best practice, critical failures |

## Process

1. **Retrieve content:** WebFetch for URLs, direct read for files
2. **Run all analyzers:**
```python
from data_sources.modules.landing_page_scorer import score_landing_page
from data_sources.modules.above_fold_analyzer import analyze_above_fold
from data_sources.modules.cta_analyzer import analyze_ctas
from data_sources.modules.trust_signal_analyzer import analyze_trust_signals
from data_sources.modules.cro_checker import check_cro

lp_score = score_landing_page(content, page_type, goal)
above_fold = analyze_above_fold(content)
ctas = analyze_ctas(content, goal)
trust = analyze_trust_signals(content)
cro = check_cro(content, page_type, goal)
```
3. **Pull GA4 data** (yoursite.com pages only): page views, bounce rate (<40% ideal), avg time (>60s ideal), conversions
4. **Generate report**

## Output

Save to: `audits/landing-audit-[slug]-[YYYY-MM-DD].md`

Report includes: executive summary table (scores + grades), critical issues, above-fold analysis, CTA analysis, trust signal analysis, CRO checklist summary, performance data, prioritized action items, A/B test suggestions.

## Audit Checklist

**Above-the-Fold:** Benefit-focused headline, clear value prop within 5 seconds, visible primary CTA, trust signal visible.

**CTAs:** Action verbs (Start, Get, Try), benefit words (Free, Instant), goal-aligned, distributed throughout, end-of-page CTA with risk reversal.

**Trust Signals:** Named testimonials, specific results with numbers, customer count/social proof, risk reversal (trial, no card, cancel policy).

**Structure:** Appropriate length, scannable format, FAQ section (SEO pages), benefits before features.

**SEO (SEO pages only):** Keyword in headline + meta title, meta description with CTA, internal links present.

## Next Steps

- Fix critical issues, then: `/landing-write [topic] --type [type] --goal [goal]`
- Compare vs competitor: `/landing-competitor [url]`
- Re-audit until score >= 75, then: `/landing-publish landing-pages/[file].md`
