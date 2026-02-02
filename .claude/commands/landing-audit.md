# Landing Page Audit Command

Use this command to audit existing landing pages for conversion optimization opportunities.

## Usage
`/landing-audit [URL or file path] --goal [trial|demo|lead]`

**Examples:**
- `/landing-audit https://yoursite.com/private-producting-solutions/`
- `/landing-audit landing-pages/product-hosting-beginners-2025-12-11.md --goal trial`
- `/landing-audit https://yoursite.com/pricing/ --goal trial`

**Defaults:**
- `--goal trial` (if not specified)

## What This Command Does

1. Fetches or reads the landing page content
2. Runs comprehensive CRO analysis using multiple analyzers
3. Pulls GA4 performance data (if available for [YOUR COMPANY] pages)
4. Generates prioritized recommendations
5. Saves audit report for reference

## Analysis Modules Used

### 1. Landing Page Scorer
**Module**: `data_sources/modules/landing_page_scorer.py`
- Overall score (0-100) against CRO best practices
- Category scores: Above-fold, CTAs, Trust signals, Structure, SEO
- Critical issues and warnings
- Publishing readiness assessment

### 2. Above-the-Fold Analyzer
**Module**: `data_sources/modules/above_fold_analyzer.py`
- Headline quality assessment
- Value proposition clarity
- CTA visibility check
- Trust signal presence
- 5-second test evaluation

### 3. CTA Analyzer
**Module**: `data_sources/modules/cta_analyzer.py`
- CTA count and distribution
- Individual CTA quality scoring
- Goal alignment check
- Placement recommendations

### 4. Trust Signal Analyzer
**Module**: `data_sources/modules/trust_signal_analyzer.py`
- Testimonial analysis (count, quality, specificity)
- Social proof detection
- Risk reversal presence
- Authority signals

### 5. CRO Checker
**Module**: `data_sources/modules/cro_checker.py`
- Checklist-based audit (30+ checks)
- Pass/fail for each CRO best practice
- Critical failures identification
- Category-by-category breakdown

## Process

### Step 1: Content Retrieval

**For URLs:**
1. Fetch page content using WebFetch tool
2. Extract main content from HTML
3. Convert to markdown for analysis

**For Files:**
1. Read the markdown file directly
2. Parse metadata and content

### Step 2: Run All Analyzers

Run each module in sequence:
```python
# Example analysis flow
from data_sources.modules.landing_page_scorer import score_landing_page
from data_sources.modules.above_fold_analyzer import analyze_above_fold
from data_sources.modules.cta_analyzer import analyze_ctas
from data_sources.modules.trust_signal_analyzer import analyze_trust_signals
from data_sources.modules.cro_checker import check_cro

# Run all analyses
lp_score = score_landing_page(content, page_type, goal)
above_fold = analyze_above_fold(content)
ctas = analyze_ctas(content, goal)
trust = analyze_trust_signals(content)
cro = check_cro(content, page_type, goal)
```

### Step 3: Performance Data ([YOUR COMPANY] Pages Only)

For yoursite.com pages, pull GA4 data if available:
- Page views (last 30 days)
- Bounce rate
- Average time on page
- Conversion events (if tracked)
- Traffic sources

### Step 4: Generate Report

Compile all findings into a comprehensive audit report.

## Output Format

### Audit Report Structure

```markdown
# Landing Page Audit Report

**URL/File**: [source]
**Audit Date**: [date]
**Conversion Goal**: [trial|demo|lead]

---

## Executive Summary

| Metric | Score | Grade |
|--------|-------|-------|
| Overall Landing Page Score | XX/100 | [Grade] |
| Above-the-Fold | XX/100 | |
| CTA Effectiveness | XX/100 | |
| Trust Signals | XX/100 | |
| CRO Checklist | XX% passed | |

**Publishing Ready**: [Yes/No]

---

## Critical Issues (Fix Immediately)

1. [Critical issue 1]
2. [Critical issue 2]

---

## Above-the-Fold Analysis

**5-Second Test**: [Pass/Fail]

| Element | Status | Details |
|---------|--------|---------|
| Headline | [✓/✗] | [details] |
| Value Prop | [✓/✗] | [details] |
| CTA | [✓/✗] | [details] |
| Trust Signal | [✓/✗] | [details] |

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

---

## CTA Analysis

**Total CTAs**: [count]
**Distribution Quality**: [excellent/good/poor]
**Goal Alignment**: [XX%]

| CTA | Position | Quality Score | Issues |
|-----|----------|---------------|--------|
| [text] | [X%] | [score] | [issues] |

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

---

## Trust Signal Analysis

**Overall Trust Score**: [XX/100]

| Signal Type | Present | Quality |
|-------------|---------|---------|
| Testimonials | [✓/✗] | [strong/moderate/weak] |
| Customer Count | [✓/✗] | |
| Specific Results | [✓/✗] | |
| Risk Reversal | [✓/✗] | |

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

---

## CRO Checklist Summary

**Passed**: [X]/[total] checks
**Critical Failures**: [count]

### Failed Checks (by priority)

**Critical:**
- [ ] [Check name] - [details]

**Important:**
- [ ] [Check name] - [details]

**Nice-to-Have:**
- [ ] [Check name] - [details]

---

## Performance Data (if available)

| Metric | Value | Benchmark |
|--------|-------|-----------|
| Page Views (30d) | [X] | |
| Bounce Rate | [X%] | <40% ideal |
| Avg Time on Page | [Xs] | >60s ideal |
| Conversions | [X] | |

---

## Prioritized Action Items

### High Priority (Do First)
1. [Action item with specific details]
2. [Action item with specific details]

### Medium Priority
1. [Action item]
2. [Action item]

### Low Priority (Nice to Have)
1. [Action item]
2. [Action item]

---

## A/B Test Suggestions

Based on this audit, consider testing:
1. [Test idea 1]
2. [Test idea 2]
3. [Test idea 3]
```

## File Management

Save audit reports to:
- **Directory**: `audits/`
- **Filename**: `landing-audit-[slug]-[YYYY-MM-DD].md`
- **Example**: `audits/landing-audit-private-producting-solutions-2025-12-11.md`

## Audit Checklist Reference

### Above-the-Fold (Critical)
- [ ] Benefit-focused headline present
- [ ] Value proposition clear within 5 seconds
- [ ] Primary CTA visible without scrolling
- [ ] Trust signal visible (count, rating, or testimonial)

### CTAs
- [ ] CTAs use action verbs (Start, Get, Try)
- [ ] CTAs include benefit words (Free, Instant)
- [ ] CTAs aligned with conversion goal
- [ ] CTAs distributed throughout page
- [ ] CTA at end of page with risk reversal

### Trust Signals
- [ ] Customer testimonials with names
- [ ] Specific results with numbers
- [ ] Customer count or social proof
- [ ] Risk reversal present (trial, no card, cancel policy)

### Structure
- [ ] Appropriate length for page type
- [ ] Scannable format (lists, bold, headers)
- [ ] FAQ section (for SEO pages)
- [ ] Benefits before features

### SEO (SEO pages only)
- [ ] Keyword in headline
- [ ] Keyword in meta title
- [ ] Meta description with CTA
- [ ] Internal links present

## Comparison Mode

To compare against competitors:
```
/landing-audit https://yoursite.com/pricing/
/landing-competitor https://competitor.com/pricing/
```

Then compare the audit reports side-by-side.

## Integration with Other Commands

**After Audit:**
1. Use findings to create improved version: `/landing-write [topic] --type [type] --goal [goal]`
2. Or run competitor analysis: `/landing-competitor [url]`
3. Or generate new headlines: Agent `headline-generator`

**Before Publishing:**
1. Run audit on draft: `/landing-audit landing-pages/[file].md`
2. Fix critical issues
3. Re-audit until score ≥ 75
4. Publish: `/landing-publish landing-pages/[file].md`
