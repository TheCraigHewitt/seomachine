# Landing Page Research Command

Use this command to research a landing page opportunity before creating it. Analyzes competitors, keywords, and provides strategic recommendations.

## Usage
`/landing-research [topic or keyword] --type [seo|ppc]`

**Examples:**
- `/landing-research "product hosting for beginners" --type seo`
- `/landing-research "product free trial" --type ppc`
- `/landing-research "private producting solutions"`

**Defaults:**
- `--type seo` (if not specified)

## What This Command Does

1. Researches the target keyword and search intent
2. Analyzes top competitor landing pages (5-10)
3. Identifies gaps and opportunities
4. Recommends headlines, CTAs, and trust signals
5. Creates a research brief for `/landing-write`

## Research Process

### Step 1: Keyword & Intent Analysis

**For SEO Pages:**
- Analyze search volume and difficulty (via DataForSEO if available)
- Classify search intent (informational, commercial, transactional)
- Identify related keywords and questions
- Check SERP features (featured snippets, PAA, ads)

**For PPC Pages:**
- Focus on commercial/transactional intent
- Identify ad copy patterns from competitors
- Note CPC and competition level
- Analyze landing page message match requirements

### Step 2: Competitor Analysis

Analyze top 5-10 competitors for the keyword:

**Content Analysis:**
- Page length (word count)
- Structure (sections, H2s)
- Content focus (features vs benefits)

**CRO Elements:**
- Headline patterns (what works)
- CTA copy and placement
- Trust signals used
- Risk reversal approaches
- Unique value propositions

**Gaps to Exploit:**
- What are competitors NOT saying?
- What objections are unaddressed?
- What social proof is missing?
- Where is messaging weak?

### Step 3: Strategic Recommendations

Based on research, recommend:

**Positioning:**
- Primary angle to differentiate
- Key benefit to emphasize
- Target audience segment

**Headlines:**
- 5+ headline options based on competitor analysis
- Headline formulas that work in this space

**CTAs:**
- Recommended CTA copy
- Optimal placement strategy

**Trust Signals:**
- Which trust signals are most important
- Specific proof points to include

## Output Format

### Research Brief Structure

```markdown
# Landing Page Research Brief

**Topic**: [topic/keyword]
**Page Type**: [SEO/PPC]
**Research Date**: [date]

---

## Keyword Analysis

**Primary Keyword**: [keyword]
**Search Intent**: [informational/commercial/transactional]
**Competition Level**: [low/medium/high]

**Related Keywords:**
- [keyword 1]
- [keyword 2]
- [keyword 3]

**Questions People Ask:**
- [question 1]
- [question 2]
- [question 3]

---

## SERP Analysis

**Current SERP Features:**
- [ ] Featured snippet
- [ ] People Also Ask
- [ ] Ads present
- [ ] Video results
- [ ] Local pack

**Top Results:**
| Position | URL | Type | Word Count |
|----------|-----|------|------------|
| 1 | [url] | [page/post] | [count] |
| 2 | [url] | [page/post] | [count] |
| 3 | [url] | [page/post] | [count] |

---

## Competitor Analysis

### Competitor 1: [name/url]

**Headline**: [their headline]
**Primary CTA**: [their CTA]
**Trust Signals**: [what they use]
**Strengths**: [what works]
**Weaknesses**: [gaps to exploit]

### Competitor 2: [name/url]
[Same structure]

### Competitor 3: [name/url]
[Same structure]

---

## Competitive Patterns

**Common Headline Approaches:**
1. [Pattern] - Example: "[example]"
2. [Pattern] - Example: "[example]"
3. [Pattern] - Example: "[example]"

**Common CTA Patterns:**
- [Pattern 1]
- [Pattern 2]

**Trust Signals Used:**
| Signal | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|--------------|--------------|--------------|
| Testimonials | [✓/✗] | [✓/✗] | [✓/✗] |
| Customer Count | [✓/✗] | [✓/✗] | [✓/✗] |
| Free Trial | [✓/✗] | [✓/✗] | [✓/✗] |
| Results/Numbers | [✓/✗] | [✓/✗] | [✓/✗] |

---

## Gaps & Opportunities

### What Competitors Are Missing

1. **[Gap 1]**
   - None/few competitors mention [X]
   - [YOUR COMPANY] opportunity: [how to exploit]

2. **[Gap 2]**
   - Competitors weak on [X]
   - [YOUR COMPANY] opportunity: [how to exploit]

3. **[Gap 3]**
   - No competitor addresses [objection/concern]
   - [YOUR COMPANY] opportunity: [how to address]

### Differentiation Opportunities

1. [Differentiation angle 1]
2. [Differentiation angle 2]
3. [Differentiation angle 3]

---

## Strategic Recommendations

### Positioning

**Primary Angle**: [recommended angle]
**Key Benefit to Emphasize**: [benefit]
**Target Audience**: [specific audience]
**Tone**: [recommended tone]

### Recommended Headlines

Based on competitive analysis and gaps:

1. **[Headline option 1]**
   - Formula: [formula used]
   - Why: [rationale]

2. **[Headline option 2]**
   - Formula: [formula used]
   - Why: [rationale]

3. **[Headline option 3]**
   - Formula: [formula used]
   - Why: [rationale]

4. **[Headline option 4]**
   - Formula: [formula used]
   - Why: [rationale]

5. **[Headline option 5]**
   - Formula: [formula used]
   - Why: [rationale]

### Recommended CTAs

**Primary CTA**: "[recommended text]"
**Secondary CTA**: "[recommended text]"
**Closing CTA**: "[recommended text]"

### Trust Signals to Include

**Must Have:**
- [Trust signal 1] - [why]
- [Trust signal 2] - [why]

**Should Have:**
- [Trust signal 3]
- [Trust signal 4]

**Nice to Have:**
- [Trust signal 5]

### Key Objections to Address

1. **[Objection]** → Address with: [approach]
2. **[Objection]** → Address with: [approach]
3. **[Objection]** → Address with: [approach]

---

## Content Recommendations

**Recommended Word Count**: [range] words
**Recommended Sections**: [X] H2 sections
**FAQ Questions to Include**:
1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]

---

## Internal Linking

Based on this topic, link to:
- [[YOUR COMPANY] page 1] - Anchor: "[suggested anchor]"
- [[YOUR COMPANY] page 2] - Anchor: "[suggested anchor]"
- [[YOUR COMPANY] page 3] - Anchor: "[suggested anchor]"

---

## Next Steps

Ready to create the landing page:
```
/landing-write research/landing-brief-[slug].md --type [seo|ppc] --goal [trial|demo|lead]
```
```

## File Management

Save research briefs to:
- **Directory**: `research/`
- **Filename**: `landing-brief-[topic-slug]-[YYYY-MM-DD].md`
- **Example**: `research/landing-brief-product-hosting-beginners-2025-12-11.md`

## Tools Used

**Web Research:**
- WebSearch for competitor discovery
- WebFetch for competitor page analysis

**Data Sources (if available):**
- DataForSEO for keyword data
- Google Search Console for existing performance

## Research Guidelines

### For SEO Landing Pages

Focus on:
- Search intent alignment
- Keyword optimization opportunities
- Content gaps vs competitors
- Featured snippet opportunities
- Long-form content requirements

### For PPC Landing Pages

Focus on:
- Message match with ad copy
- Quick value proposition delivery
- Single conversion focus
- Minimal distractions
- Trust signals that overcome ad skepticism

## Integration with Other Commands

**After Research:**
```
/landing-write research/landing-brief-[slug].md --type [type] --goal [goal]
```

**For Competitor Deep Dive:**
```
/landing-competitor [specific-competitor-url]
```

**For Existing Page Updates:**
```
/landing-audit [existing-page-url]
```
