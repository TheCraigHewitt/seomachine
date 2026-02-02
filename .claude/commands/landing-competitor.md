# Landing Page Competitor Analysis Command

Use this command to analyze a specific competitor's landing page in depth.

## Usage
`/landing-competitor [URL]`

**Examples:**
- `/landing-competitor https://competitor1.com/pricing/`
- `/landing-competitor https://competitor2.com/features/`
- `/landing-competitor https://competitor3.com/product/`

## What This Command Does

1. Fetches and analyzes the competitor's landing page
2. Extracts key CRO elements and patterns
3. Identifies their strengths and weaknesses
4. Provides actionable insights for [YOUR COMPANY] pages
5. Saves analysis for reference

## Analysis Framework

### 1. Page Overview
- URL and page type (homepage, pricing, feature, etc.)
- Estimated word count
- Page structure (sections, headers)
- Primary conversion goal

### 2. Above-the-Fold Analysis
- Headline (exact text and approach)
- Subheadline/value proposition
- CTA (text, visibility, design description)
- Trust signals visible
- Overall first impression

### 3. Content Strategy
- Key messages and themes
- Benefit vs feature balance
- Pain points addressed
- Unique value propositions
- Content organization

### 4. CTA Strategy
- All CTAs found (text and placement)
- CTA frequency and distribution
- CTA text patterns
- Goal alignment

### 5. Trust Signals
- Testimonials (count, quality, specificity)
- Social proof (customer counts, logos)
- Risk reversals (trials, guarantees)
- Authority signals (awards, media)

### 6. Objection Handling
- FAQ presence and quality
- Objections addressed in copy
- Comparison content
- Pricing transparency

### 7. Technical/UX Elements
- Page load speed (estimated)
- Mobile considerations visible
- Form complexity (if present)
- Navigation strategy

## Output Format

### Competitor Analysis Report

```markdown
# Competitor Landing Page Analysis

**Competitor**: [Company Name]
**URL**: [URL]
**Analysis Date**: [date]
**Page Type**: [pricing/feature/homepage/etc.]

---

## Quick Summary

| Aspect | Rating | Notes |
|--------|--------|-------|
| Headline | [Strong/Moderate/Weak] | [brief note] |
| Value Prop | [Clear/Moderate/Unclear] | [brief note] |
| CTAs | [Strong/Moderate/Weak] | [brief note] |
| Trust Signals | [Strong/Moderate/Weak] | [brief note] |
| Overall CRO | [Strong/Moderate/Weak] | [brief note] |

---

## Above-the-Fold Breakdown

### Headline
**Text**: "[exact headline]"
**Approach**: [number/question/benefit/etc.]
**Strengths**: [what works]
**Weaknesses**: [what could be better]

### Subheadline/Value Prop
**Text**: "[exact text]"
**Clarity**: [clear/unclear]
**Specificity**: [specific/vague]

### Primary CTA
**Text**: "[exact CTA text]"
**Visibility**: [prominent/visible/hidden]
**Action Verb**: [yes/no - which verb]
**Benefit Word**: [yes/no - which word]

### Trust Signal Above Fold
**Present**: [yes/no]
**Type**: [customer count/rating/testimonial/logo/etc.]
**Text**: "[exact text if applicable]"

---

## Full CTA Analysis

| CTA Text | Position | Type | Strength |
|----------|----------|------|----------|
| "[text]" | [above fold/mid/bottom] | [primary/secondary] | [score] |
| "[text]" | [position] | [type] | [score] |

**Patterns Observed:**
- [Pattern 1]
- [Pattern 2]

---

## Trust Signals Inventory

### Testimonials
| Quote | Attribution | Specificity |
|-------|-------------|-------------|
| "[quote excerpt]" | [name, title] | [specific/vague] |

### Social Proof
- **Customer Count**: [if present]
- **Results/Numbers**: [if present]
- **Customer Logos**: [if present]

### Risk Reversals
- [ ] Free trial - Duration: [X days]
- [ ] No credit card
- [ ] Money-back guarantee
- [ ] Cancel anytime

### Authority Signals
- [Authority signal if present]

---

## Content Structure

**Estimated Word Count**: [X] words
**Number of Sections**: [X]

### Section Breakdown
1. **[Section title]** - [purpose/content summary]
2. **[Section title]** - [purpose/content summary]
3. **[Section title]** - [purpose/content summary]

### Content Focus
- **Benefits emphasized**: [list]
- **Features mentioned**: [list]
- **Pain points addressed**: [list]

---

## Strengths to Learn From

1. **[Strength 1]**
   - What they do: [description]
   - Why it works: [explanation]
   - How [YOUR COMPANY] can use: [application]

2. **[Strength 2]**
   - What they do: [description]
   - Why it works: [explanation]
   - How [YOUR COMPANY] can use: [application]

3. **[Strength 3]**
   - What they do: [description]
   - Why it works: [explanation]
   - How [YOUR COMPANY] can use: [application]

---

## Weaknesses to Exploit

1. **[Weakness 1]**
   - What's missing/weak: [description]
   - Impact: [why it matters]
   - [YOUR COMPANY] advantage: [how to capitalize]

2. **[Weakness 2]**
   - What's missing/weak: [description]
   - Impact: [why it matters]
   - [YOUR COMPANY] advantage: [how to capitalize]

3. **[Weakness 3]**
   - What's missing/weak: [description]
   - Impact: [why it matters]
   - [YOUR COMPANY] advantage: [how to capitalize]

---

## Key Takeaways for [YOUR COMPANY]

### Must Do (Critical Lessons)
1. [Takeaway 1]
2. [Takeaway 2]

### Should Do (Important Lessons)
1. [Takeaway 1]
2. [Takeaway 2]

### Could Do (Nice Ideas)
1. [Takeaway 1]
2. [Takeaway 2]

### Avoid (What Not to Copy)
1. [Anti-pattern 1]
2. [Anti-pattern 2]

---

## Recommended Differentiation

Based on this analysis, [YOUR COMPANY] should differentiate by:

1. **[Differentiation angle 1]**
   - They say: [competitor approach]
   - We should say: [[YOUR COMPANY] approach]

2. **[Differentiation angle 2]**
   - They say: [competitor approach]
   - We should say: [[YOUR COMPANY] approach]

---

## Headlines to Beat Theirs

Their headline: "[competitor headline]"

Better alternatives for [YOUR COMPANY]:
1. "[[YOUR COMPANY] headline option 1]"
2. "[[YOUR COMPANY] headline option 2]"
3. "[[YOUR COMPANY] headline option 3]"

---

## CTAs to Beat Theirs

Their primary CTA: "[competitor CTA]"

Stronger alternatives for [YOUR COMPANY]:
1. "[[YOUR COMPANY] CTA option 1]"
2. "[[YOUR COMPANY] CTA option 2]"
```

## File Management

Save competitor analyses to:
- **Directory**: `research/`
- **Filename**: `competitor-landing-[domain]-[YYYY-MM-DD].md`
- **Example**: `research/competitor-landing-example-com-2025-12-11.md`

## Analysis Guidelines

### What to Focus On

1. **Patterns That Convert**
   - What CTA text do they use repeatedly?
   - Where do they place trust signals?
   - How do they structure their argument?

2. **Gaps and Weaknesses**
   - What objections don't they address?
   - What trust signals are missing?
   - Where is their copy vague or generic?

3. **Differentiation Opportunities**
   - What unique angle could [YOUR COMPANY] take?
   - What can [YOUR COMPANY] claim that they can't?
   - Where is their positioning vulnerable?

### What NOT to Do

- Don't copy their copy directly
- Don't assume their approach is optimal
- Don't ignore their weaknesses
- Don't forget [YOUR COMPANY]'s unique strengths

## Integration with Other Commands

**After Competitor Analysis:**
```
# Create a landing page that beats the competitor
/landing-write "[topic]" --type seo --goal trial
```

**Compare Multiple Competitors:**
```
/landing-competitor [url1]
/landing-competitor [url2]
/landing-competitor [url3]
# Then synthesize findings
```

**Audit [YOUR COMPANY] vs Competitor:**
```
/landing-audit https://yoursite.com/[page]/
/landing-competitor https://competitor.com/[page]/
# Compare reports side-by-side
```

## Competitors to Consider

Refer to your `config/competitors.json` for your configured competitor list.

For specific features:
- Analyze competitors who excel in each feature area
- Compare pricing pages, feature pages, and landing pages
