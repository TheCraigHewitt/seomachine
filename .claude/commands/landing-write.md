# Landing Page Write Command

Use this command to create high-converting landing pages optimized for either organic SEO traffic or paid PPC traffic.

## Usage
`/landing-write [topic or research brief] --type [seo|ppc] --goal [trial|demo|lead]`

**Examples:**
- `/landing-write "product hosting for beginners" --type seo --goal trial`
- `/landing-write "research/landing-brief-private-producting.md" --type ppc --goal demo`
- `/landing-write "product monetization guide" --type seo --goal lead`

**Defaults:**
- `--type seo` (if not specified)
- `--goal trial` (if not specified)

## What This Command Does

1. Creates conversion-optimized landing pages (not blog articles)
2. Tailors content length and structure to page type (SEO vs PPC)
3. Optimizes CTAs for the specified conversion goal
4. Includes all CRO best practices (trust signals, risk reversal, etc.)
5. Scores the page against landing page best practices

## Pre-Writing Review

**Required Context:**
- **Landing Page Templates**: @context/landing-page-templates.md for structure
- **CRO Best Practices**: @context/cro-best-practices.md for conversion guidelines
- **Brand Voice**: @context/brand-voice.md for tone and messaging

**If Research Brief Available:**
- Review competitor analysis
- Use recommended headlines
- Reference identified pain points
- Integrate suggested trust signals

---

## SEO Landing Page Structure (--type seo)

**Word Count:** 1500-2500 words
**CTAs:** 3-5 distributed throughout
**Internal Links:** 2-3 strategic links

### Content Structure

```markdown
# [Benefit-Focused Headline with Keyword]

**Meta Title**: [50-60 chars, keyword + benefit]
**Meta Description**: [150-160 chars, includes CTA]
**Target Keyword**: [primary keyword]
**Page Type**: seo
**Conversion Goal**: [trial|demo|lead]

---

[HOOK: 2-3 sentences. Start with pain point, surprising stat, or question]

[Trust signal: "Join 50,000+ customers" or customer results]

**[Primary CTA Button →]**

## [H2: Problem/Pain Point Section]

[2-3 paragraphs acknowledging the reader's struggle]

[Mini-story with specific person and outcome]

## [H2: Solution Overview]

[Introduce how [YOUR COMPANY] solves this problem]

**Key Benefits:**
- **[Benefit 1]** - [One sentence]
- **[Benefit 2]** - [One sentence]
- **[Benefit 3]** - [One sentence]

**[Secondary CTA →]**

## [H2: Features That Deliver]

[3-5 features, each tied to a benefit]

### [Feature 1]
[2-3 sentences: what it is, why it matters]

### [Feature 2]
[Continue...]

## [H2: Social Proof]

"[Testimonial with specific results]"
— **[Name], [Product/Company]**

"[Second testimonial]"
— **[Name], [Product/Company]**

**Results our customers see:**
- [Specific result with number]
- [Specific result with number]

**[CTA Button →]**

## [H2: How It Works]

1. **[Step 1]** - [Brief description]
2. **[Step 2]** - [Brief description]
3. **[Step 3]** - [Brief description]

## [H2: FAQ Section]

**[Question addressing objection]?**
[Answer - 2-3 sentences]

**[Question addressing objection]?**
[Answer - 2-3 sentences]

[4-6 FAQs total]

## [H2: Ready to [Achieve Outcome]?]

[1-2 sentences summarizing the value]

**[Strong CTA Button →]**

[Risk reversal: "Free trial • No credit card • Cancel anytime"]
```

---

## PPC Landing Page Structure (--type ppc)

**Word Count:** 400-800 words
**CTAs:** 2-3 (same goal, prominent)
**Internal Links:** 0-1 (minimize distractions)

### Content Structure

```markdown
# [Headline Matching Ad Copy]

**Meta Title**: [Match ad headline]
**Meta Description**: [Match ad description]
**Target Keyword**: [ad keyword]
**Page Type**: ppc
**Conversion Goal**: [trial|demo|lead]

---

[One-sentence value proposition matching the ad]

[Trust signal: "Trusted by 50,000+ customers"]

**[Primary CTA Button - Large and Prominent →]**

## [H2: Why [Audience] Choose [YOUR COMPANY]]

- **[Benefit 1]** - [One sentence max]
- **[Benefit 2]** - [One sentence max]
- **[Benefit 3]** - [One sentence max]

## [H2: Proof It Works]

"[Short testimonial with specific result]"
— **[Name]**

**[Primary CTA Button →]**

## [H2: What You Get]

- [Included item/benefit]
- [Included item/benefit]
- [Included item/benefit]

[Risk Reversal Section]
- Free [X]-day trial
- No credit card required
- Cancel anytime

**[Final CTA Button →]**
```

---

## Goal-Specific Guidelines

### Trial Goal (--goal trial)

**Primary CTAs:**
- "Start Your Free Trial →"
- "Try Free for 14 Days →"
- "Get Started Free →"

**Supporting Copy Required:**
- "No credit card required"
- Trial length mentioned
- "Cancel anytime"
- "Set up in minutes"

**Trust Signals to Include:**
- Producter count
- Ease of setup
- No commitment messaging

### Demo Goal (--goal demo)

**Primary CTAs:**
- "Book Your Demo →"
- "Schedule a Call →"
- "See It in Action →"

**Supporting Copy Required:**
- Demo length ("15-minute walkthrough")
- What demo covers
- "No pressure, no hard sell"
- Personalization promise

**Trust Signals to Include:**
- Enterprise customer logos
- Custom solutions mention
- Expert guidance

### Lead Goal (--goal lead)

**Primary CTAs:**
- "Download the Free Guide →"
- "Get Instant Access →"
- "Claim Your Copy →"

**Supporting Copy Required:**
- What they're getting
- "Instant download"
- "No spam, ever"
- Content preview/teaser

**Trust Signals to Include:**
- Community/subscriber size
- Author credibility
- Content preview

---

## Required Elements Checklist

### Above the Fold (Critical)
- [ ] Benefit-focused headline (H1)
- [ ] Clear value proposition (1-2 sentences)
- [ ] Primary CTA button (prominent, contrasting)
- [ ] Trust signal (customer count, rating, or result)

### Trust Signals
- [ ] At least 2 testimonials with names (SEO pages)
- [ ] At least 1 testimonial (PPC pages)
- [ ] Specific results with numbers
- [ ] Risk reversal near CTAs

### CTAs
- [ ] Action verb in CTA text (Start, Get, Try, Book)
- [ ] Benefit word in CTA (Free, Instant, Today)
- [ ] Goal-aligned CTA copy
- [ ] First CTA within 20% of page
- [ ] CTA at end of page

### SEO (SEO pages only)
- [ ] Keyword in headline
- [ ] Keyword in meta title
- [ ] Keyword in first 100 words
- [ ] 2-3 internal links

---

## Headline Requirements

### Formula Options

**Benefit-Focused:**
- "[Achieve Outcome] Without [Pain Point]"
- "The [Adjective] Way to [Achieve Outcome]"
- "Finally, [Solution] for [Audience]"

**Number-Based:**
- "[Number] [Audience] Trust [Product] to [Benefit]"
- "Launch Your Product in [Number] Minutes"

**Question-Based:**
- "Ready to [Achieve Outcome]?"
- "What if You Could [Desired Outcome]?"

### Headline Don'ts
- NO "Welcome to..."
- NO "The Best..." without proof
- NO generic "Everything You Need"
- NO starting with "Our" or "We"
- NO longer than 70 characters

---

## File Output

Save completed landing page to:
- **Directory**: `landing-pages/`
- **Filename**: `[topic-slug]-[YYYY-MM-DD].md`
- **Example**: `landing-pages/product-hosting-beginners-2025-12-11.md`

---

## Automatic Scrubbing

After saving, immediately run the content scrubber:
```
/scrub landing-pages/[filename].md
```

This removes AI watermarks and characteristic patterns.

---

## Automatic Scoring

After scrubbing, score the landing page using:

```bash
python data_sources/modules/landing_page_scorer.py landing-pages/[filename].md --type [seo|ppc] --goal [trial|demo|lead]
```

Or run via the landing-page-optimizer agent.

### Score Requirements
- **Minimum Score**: 75/100 to be publish-ready
- **No Critical Issues**: Must resolve any critical issues before publishing

### If Score < 75:
1. Review critical issues and warnings
2. Apply top 3 fixes
3. Re-score
4. If still below threshold, save to `review-required/landing-pages/` with notes

---

## Automatic Agent Execution

After saving and scrubbing, run these agents:

### 1. Landing Page Optimizer Agent
- **Agent**: `landing-page-optimizer`
- **Input**: Full landing page content
- **Output**: CRO optimization report
- **Analyzes**: Above-fold, CTAs, trust signals, structure

### 2. Headline Generator Agent
- **Agent**: `headline-generator`
- **Input**: Page content and keyword
- **Output**: 10+ headline variations for A/B testing

### 3. CRO Analyst Agent
- **Agent**: `cro-analyst`
- **Input**: Page content and goal
- **Output**: Psychology and persuasion analysis

---

## Quality Standards

### SEO Landing Pages Must Have:
- 1500-2500 words
- 3-5 CTAs distributed throughout
- 2+ testimonials with specific results
- 4-6 FAQ questions (featured snippet opportunity)
- 2-3 internal links
- Risk reversal statement
- Proper H2/H3 structure

### PPC Landing Pages Must Have:
- 400-800 words maximum
- 2-3 prominent CTAs (same goal)
- Headline matching ad copy
- At least 1 testimonial
- Risk reversal statement
- Minimal navigation/distractions
- Fast-loading (minimal images)

### Both Page Types Need:
- Score ≥ 75 on landing page scorer
- No critical issues
- All required above-fold elements
- Goal-aligned CTA copy
- Trust signals present
- Clear value proposition

---

## Differences from /write Command

| Aspect | /write (Blog) | /landing-write |
|--------|---------------|----------------|
| **Goal** | Educate & inform | Convert visitors |
| **Length** | 2000-3000+ words | 400-2500 words |
| **CTAs** | 2-3 contextual | 3-5 prominent (SEO) |
| **Structure** | Educational flow | Conversion flow |
| **SEO Focus** | High (rankings) | Varies (SEO vs PPC) |
| **Internal Links** | 3-5 | 0-3 |
| **Output** | drafts/ | landing-pages/ |
| **Scoring** | content_scorer | landing_page_scorer |

---

## Example Workflow

```bash
# 1. Research the opportunity (optional but recommended)
/landing-research "product hosting for wordpress" --type seo

# 2. Create the landing page
/landing-write "research/landing-brief-product-hosting-wordpress.md" --type seo --goal trial

# 3. Review score and recommendations
# (automatic scoring runs after save)

# 4. Make revisions if needed
# (edit the file in landing-pages/)

# 5. Publish when ready
/landing-publish landing-pages/product-hosting-wordpress-2025-12-11.md
```
