# Landing Page Research Command

Research a landing page opportunity before creating it.

## Usage
`/landing-research [topic or keyword] --type [seo|ppc]`

**Examples:**
- `/landing-research "product hosting for beginners" --type seo`
- `/landing-research "product free trial" --type ppc`

**Default:** `--type seo`

## Research Process

### Step 1: Keyword & Intent Analysis

**SEO Pages:** Search volume + difficulty (DataForSEO), intent classification, related keywords/questions, SERP features.

**PPC Pages:** Commercial/transactional intent focus, ad copy patterns, CPC + competition level, message match requirements.

### Step 2: Competitor Analysis (top 5-10)

**Content:** Page length, structure, features vs benefits focus.

**CRO Elements:** Headline patterns, CTA copy + placement, trust signals, risk reversals, unique value props.

**Gaps:** What competitors are NOT saying, unaddressed objections, missing social proof, weak messaging.

### Step 3: Strategic Recommendations

- **Positioning:** Primary angle, key benefit, target audience
- **Headlines:** 5+ options based on competitor analysis
- **CTAs:** Recommended copy + placement strategy
- **Trust Signals:** Priority-ranked proof points to include

## Output

Save to: `research/landing-brief-[topic-slug]-[YYYY-MM-DD].md`

Brief includes: keyword analysis, SERP analysis (features + top results), per-competitor breakdown (headline, CTA, trust, strengths, weaknesses), competitive patterns, gaps & differentiation opportunities, strategic recommendations (positioning, headlines, CTAs, trust signals, objections to address), content recommendations (word count, sections, FAQ questions), internal linking suggestions.

## Tools Used

- WebSearch + WebFetch for competitor discovery and analysis
- DataForSEO for keyword data (if available)
- Google Search Console for existing performance

## SEO vs PPC Focus

**SEO:** Intent alignment, keyword optimization, content gaps, featured snippet opportunities, long-form requirements.

**PPC:** Ad message match, quick value delivery, single conversion focus, minimal distractions, trust signals for ad skepticism.

## Next Steps

```
/landing-write research/landing-brief-[slug].md --type [seo|ppc] --goal [trial|demo|lead]
```

For competitor deep dive: `/landing-competitor [url]`
For existing page updates: `/landing-audit [url]`
