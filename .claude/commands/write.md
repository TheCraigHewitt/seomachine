# Write Command

Create a complete, SEO-optimized long-form article from a topic or research brief.

## Usage
`/write [topic or research brief]`

## Pre-Writing Review
Before drafting, check:
- Research brief from `/research` (if available)
- `@context/brand-voice.md`
- `@context/writing-examples.md`
- `@context/style-guide.md`
- `@context/seo-guidelines.md`
- `@context/target-keywords.md`

## Content Structure

### 1) H1 Headline
- Include primary keyword naturally.
- Keep title within ~60 characters.
- Make value clear and specific.

### 2) Introduction (150-200 words)
The first 1-2 sentences must open with a real hook, not a generic definition.

Allowed hook styles:
- Provocative question
- Specific scenario
- Surprising statistic
- Bold or counterintuitive claim

After hook, use **APP formula**:
- **Agree**: confirm a pain point or belief the audience already has
- **Promise**: state what they will gain
- **Preview**: summarize what the article will cover

Additional intro requirements:
- Primary keyword in first 100 words
- Brief trust/credibility signal

### 3) Main Body (1800-2500+ words)
- 4-7 H2 sections, with H3 where needed
- Clear progression from basics to application
- Paragraphs 2-4 sentences max
- Primary keyword natural density around 1-2%
- Include semantic keyword variations
- Use lists/tables where they improve scanability
- Support claims with data and sources

Required engagement elements:
- **Mini-stories (2-3 total)**
  - Include a named person/team
  - Include concrete details (numbers, timeline, constraints)
  - Include clear outcome
  - Place one early, one mid-article, one near conclusion (optional)
- **Contextual CTAs (2-3 total)**
  - First CTA must appear within first 500 words
  - Match CTA strength to context (soft -> medium -> strong)
  - Avoid generic anchor text like "click here"

CTA placement pattern:
| Location | CTA Type |
|----------|----------|
| After first major value section | Soft CTA |
| After proof/comparison section | Medium CTA |
| Conclusion | Strong CTA |

### 4) Conclusion (150-200 words)
- Summarize 3-5 actionable takeaways
- Provide next steps
- End with a clear conversion-oriented CTA

## SEO Requirements

### Keyword Placement
Primary keyword should appear in:
- H1
- First 100 words
- At least 2 H2 headings
- Body copy naturally (1-2% target)
- Meta title
- Meta description
- URL slug

### Internal Linking (3-5+)
- Use `@context/internal-links-map.md`
- Include pillar + related blog + product/resource pages
- Use descriptive anchor text

### External Linking (2-3+)
- Link to authoritative sources for claims/statistics
- Prefer current, credible references

### Readability
- Average sentence length under ~25 words
- Mix short and longer sentences for rhythm
- Target grade 8-10 readability
- Prefer active voice

## Output

### 1) Publish-Ready Article
Markdown article containing:
- H1
- Intro
- H2/H3 structured body
- Conclusion + CTA

### 2) Metadata Frontmatter
```yaml
---
Meta Title: [50-60 character optimized title]
Meta Description: [150-160 character compelling description]
Primary Keyword: [main target keyword]
Secondary Keywords: [keyword1, keyword2, keyword3]
URL Slug: /blog/[optimized-slug]
Internal Links: [list of pages linked from your site]
External Links: [list of external sources]
Word Count: [actual word count]
---
```

### 3) Completion Checklist
SEO checks:
- [ ] Primary keyword in H1
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in 2+ H2 headings
- [ ] Keyword density in 1-2% range
- [ ] 3-5+ internal links
- [ ] 2-3+ external authority links
- [ ] Meta title 50-60 chars
- [ ] Meta description 150-160 chars
- [ ] Proper H2/H3 hierarchy

Engagement checks:
- [ ] Strong opening hook (not generic)
- [ ] APP formula present in intro
- [ ] 2-3 mini-stories with specifics
- [ ] 2-3 contextual CTAs
- [ ] First CTA within first 500 words
- [ ] Paragraph length <=4 sentences

## File Management
Save draft to:
`drafts/[topic-slug]-[YYYY-MM-DD].md`

Example: `drafts/content-marketing-strategies-2025-10-15.md`

## Automatic Content Scrubbing
Immediately after saving, scrub the main article file:
```bash
/scrub drafts/[article-file].md
```
Run before any further optimization or publishing.

## Automatic Quality Loop

### Step 1: Score draft
```bash
python data_sources/modules/content_scorer.py drafts/[article-file].md
```

### Step 2: Evaluate composite score (target >=70)
Scoring dimensions:
| Dimension | Weight |
|-----------|--------|
| Humanity/Voice | 30% |
| Specificity | 25% |
| Structure Balance | 20% |
| SEO Compliance | 15% |
| Readability | 10% |

### Step 3: Revise if needed
If score <70:
1. Apply top `priority_fixes`
2. Re-score
3. Repeat once more if needed

### Step 4: Route output
- Score >=70: keep in `drafts/` and continue
- Score <70 after 2 iterations: move to `review-required/` and create `[article]_REVIEW_NOTES.md`

Review-required format:
```text
review-required/
├── article-name-YYYY-MM-DD.md
└── article-name-YYYY-MM-DD_REVIEW_NOTES.md
```

## Automatic Agent Execution
After passing quality threshold, run:
- `content-analyzer` -> `drafts/content-analysis-[topic-slug]-[YYYY-MM-DD].md`
- `seo-optimizer` -> `drafts/seo-report-[topic-slug]-[YYYY-MM-DD].md`
- `meta-creator` -> `drafts/meta-options-[topic-slug]-[YYYY-MM-DD].md`
- `internal-linker` -> `drafts/link-suggestions-[topic-slug]-[YYYY-MM-DD].md`
- `keyword-mapper` -> `drafts/keyword-analysis-[topic-slug]-[YYYY-MM-DD].md`

## Audience and Voice Alignment
- Write for the audience defined in `@context/brand-voice.md`.
- Reflect real audience constraints, goals, and decision criteria.
- Mention product/features only where contextually relevant.
- Keep terminology consistent with `@context/style-guide.md`.

## Hook and Story Examples

### Hook examples
| Hook Type | Example |
|-----------|---------|
| Provocative question | "What if your lowest-cost tool is creating your highest hidden cost?" |
| Specific scenario | "On Tuesday morning, the ops team found their dashboard had been wrong for 19 days." |
| Surprising statistic | "73% of teams replacing their stack do it within 18 months for the same three reasons." |
| Counterintuitive claim | "The cheapest plan is often the most expensive choice by quarter-end." |

### Mini-story example (50-150 words)
```text
When Marcus launched in March, he chose the $5 hosting tier to cut burn. Six months later,
usage doubled and hidden bandwidth fees pushed costs to $89/month. During migration he lost
three weeks of analytics and missed a partner report deadline. The cheapest option cost him
both money and momentum.
```

## Quality Standards
Content standards:
- 2000+ words (2500-3000 preferred for competitive topics)
- Clear H1/H2/H3 hierarchy
- 3-5 internal links + 2-3 external authority links
- Actionable recommendations, not generic statements

Engagement standards:
- Hook in first 1-2 sentences
- 2-3 mini-stories with names/details/outcomes
- 2-3 contextual CTAs distributed through article
- First CTA within first 500 words
- No paragraph longer than 4 sentences

Routing standard:
- Composite quality score >=70 for draft progression
- Below threshold after two iterations -> `review-required/` with review notes

## Publish Readiness Reminder
Do not proceed to publishing until scrub, scoring, and agent outputs are complete and reviewed.
