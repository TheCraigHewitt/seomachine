# Article Command

Unified article workflow: mandatory research, structured planning, section-by-section drafting, and quality-gated output.

## Usage
`/article [topic]`

Examples:
- `/article "Best Project Management Tools for Small Teams"`
- `/article "Content Marketing Strategy Guide 2025"`
- `/article "How to Migrate from Competitor to Your Product"`

## When to Use `/article` vs `/write`
| Scenario | Command |
|----------|---------|
| New competitive topic | `/article` |
| Topic where you must beat existing SERP content | `/article` |
| Existing high-quality research already available | `/write` |
| Light update to an existing draft | `/write` |

## Required 4-Step Pipeline
1. SERP Analysis
2. Social Research
3. Article Planning
4. Section-by-Section Writing

Research is mandatory in this command flow.

## Step 1: SERP Analysis (Mandatory)

### Process
1. Use `WebSearch` for current ranking landscape.
2. Use `WebFetch` on top 5 ranking pages.
3. For each page, capture:
- URL/domain
- Approximate word count
- Heading structure (H2/H3 flow)
- Strengths to match
- Gaps and thin sections
- Unsupported claims
- Outdated stats/tools

4. Build competitor gap blueprint:
- must-fill gaps appearing across multiple competitors
- differentiation angles competitors are missing
- data needs (statistics/quotes/case evidence)
- outdated industry points to refresh

### Output File
`research/serp-analysis-[topic-slug]-[YYYY-MM-DD].md`

Suggested structure:
- Top ranking pages summary
- Google-validated common sections
- Gap blueprint
- Data required
- Outdated claims to replace

## Step 2: Social Research (Mandatory)

### Process
#### Reddit
- Use `WebSearch` with `site:reddit.com` queries.
- Visit 5 real threads using `WebFetch`.
- Extract:
  - original question/problem
  - top-voted solutions
  - recurring pain points
  - debates/opposing opinions
  - success/failure stories
  - phrases users actually use

#### YouTube
- Use `WebSearch` with `site:youtube.com` queries.
- Review 5 relevant video pages with `WebFetch`.
- Extract:
  - title/description angle
  - view count signal
  - topics covered
  - missing topics
  - comment themes/questions

### Output File
`research/social-research-[topic-slug]-[YYYY-MM-DD].md`

Required sections:
- Reddit insight summaries (5 threads)
- YouTube insight summaries (5 videos)
- pain-point synthesis
- real-user language list
- questions to answer in article
- story seeds for mini-stories

## Step 3: Article Planning

### Process
Combine:
- SERP structure signals
- competitor gap blueprint
- social insights
- context files (`@context/brand-voice.md`, `@context/features.md`, `@context/seo-guidelines.md`)

For each planned section define:
- section type (`intro`, `body-how-to`, `body-comparison`, `body-explanation`, `faq`, `conclusion`)
- word target
- strategic angle
- competitor gap addressed
- social insight/data to include
- internal link target
- CTA type (soft/medium/strong)
- mini-story placement

### Output File
`research/article-plan-[topic-slug]-[YYYY-MM-DD].md`

Plan must include:
- title options + meta description + slug
- section-by-section blueprint
- engagement map (story + CTA distribution)
- gap-to-section mapping
- social-insight-to-section mapping

## Step 4: Section-by-Section Writing
Write each section separately, then assemble.

### Section requirements
#### Introduction
- strong hook (question/scenario/stat/bold claim)
- APP formula (Agree, Promise, Preview)
- primary keyword in first 100 words
- 150-250 words

Avoid generic openers such as:
- "[Category] is..."
- "When it comes to..."
- "In today's world..."

#### Body sections
- Use appropriate type (how-to/comparison/explanation)
- Keep each section specific and actionable
- Use concrete examples and data
- 250-400 words per section (typical)

#### FAQ
- 4-6 real user questions from research
- direct answers first, then brief context
- target snippet-friendly formatting

#### Conclusion
- 3-5 actionable takeaways
- practical next steps
- strong final CTA

### Editing pass per section
- Remove AI boilerplate phrasing
- Replace vague terms with specifics
- Keep paragraphs <=4 sentences
- Vary sentence rhythm
- Preserve active voice

### Assembly
After all sections are drafted:
1. Combine in planned order.
2. Improve transitions.
3. Verify planned CTA and story placement.
4. Add metadata frontmatter.
5. Run final checks.

Output file:
`drafts/[topic-slug]-[YYYY-MM-DD].md`

## Post-Writing Quality Loop
1. Scrub AI artifacts:
```bash
/scrub drafts/[filename].md
```
2. Score quality:
```bash
python data_sources/modules/content_scorer.py drafts/[filename].md
```

Scoring threshold: **>=70**.

If score <70:
1. Apply top `priority_fixes`
2. Re-score
3. Repeat once
4. If still <70, route to `review-required/` with `[filename]_REVIEW_NOTES.md`

## Agent Outputs (after score threshold passes)
- `drafts/content-analysis-[topic]-[date].md` (`content-analyzer`)
- `drafts/seo-report-[topic]-[date].md` (`seo-optimizer`)
- `drafts/meta-options-[topic]-[date].md` (`meta-creator`)
- `drafts/link-suggestions-[topic]-[date].md` (`internal-linker`)
- `drafts/keyword-analysis-[topic]-[date].md` (`keyword-mapper`)

## Output Tree
```text
research/
├── serp-analysis-[topic]-[date].md
├── social-research-[topic]-[date].md
└── article-plan-[topic]-[date].md

drafts/
├── [topic]-[date].md
├── content-analysis-[topic]-[date].md
├── seo-report-[topic]-[date].md
├── meta-options-[topic]-[date].md
├── link-suggestions-[topic]-[date].md
└── keyword-analysis-[topic]-[date].md
```

## Required Context Files
- `@context/brand-voice.md`
- `@context/style-guide.md`
- `@context/seo-guidelines.md`
- `@context/internal-links-map.md`
- `@context/features.md`
- `@context/writing-examples.md`

## Minimum Quality Standards
- Top 5 SERP pages analyzed
- 5 Reddit threads + 5 YouTube pages reviewed
- 2000+ word article with proper H1/H2/H3 hierarchy
- 3-5 internal links + 2-3 external authority links
- 2-3 mini-stories + 2-3 contextual CTAs
- Composite quality score >=70

## Step Output Templates

### A) SERP Analysis Template
```markdown
# SERP Analysis: [Topic]
Date: [YYYY-MM-DD]
Target Keyword: [keyword]
Search Intent: [intent]

## Top Pages (5)
### 1) [Title] - [Domain]
- URL: [url]
- Word Count: ~[count]
- Structure: [key headings]
- Strengths: [what works]
- Gaps: [what's missing]
- Outdated Items: [what to replace]

## Common Sections Across SERP
1. [section]
2. [section]

## Gap Blueprint
- Must-fill gaps: [list]
- Differentiation angles: [list]
- Data needed: [list]
```

### B) Social Research Template
```markdown
# Social Research: [Topic]
Date: [YYYY-MM-DD]

## Reddit Threads (5)
### Thread 1: [Title]
- URL: [url]
- Core Question: [summary]
- Key Insight: [summary]
- Quotable Language: "[phrase]"

## YouTube Pages (5)
### Video 1: [Title]
- URL: [url]
- Topics Covered: [list]
- Viewer Gaps/Questions: [list]

## Synthesis
- Recurring pain points: [list]
- Questions to answer: [list]
- Story seeds: [list]
- Preferred user language: [list]
```

### C) Article Plan Template
```markdown
# Article Plan: [Topic]
Date: [YYYY-MM-DD]
Word Target: [count]
Primary Keyword: [keyword]
Secondary Keywords: [list]

## Meta Draft
- Title options: [1], [2], [3]
- Meta Description: [150-160 chars]
- URL Slug: /blog/[slug]

## Section Plan
### 1) Introduction
- Type: intro
- Word Target: 200
- Hook Strategy: [type]
- APP Elements: [Agree, Promise, Preview]
- Story/CTA Placement: [details]

### 2) [H2]
- Type: [section type]
- Word Target: [count]
- Gap Addressed: [gap]
- Social Insight Used: [insight]
- Internal Link: [target]

## Mapping
- Gap -> Section
- Social Insight -> Section
```

## Section-Type Guidance
- `body-how-to`: use ordered steps, practical actions, and common pitfalls.
- `body-comparison`: use balanced evaluation and concrete criteria.
- `body-explanation`: progress from simple to advanced concepts.
- `faq`: direct answers first, then concise context.

## Final Assembly Checks
Before moving to post-writing loop, verify:
- Planned sections are all present and in the intended order.
- Gap-to-section and social-insight mappings are represented in the draft.
- CTA placement follows planned soft/medium/strong progression.
- Mini-stories are distributed across intro/mid/end.
- Metadata and links are complete.

## Review-Required Routing
If score stays below threshold after two revision cycles:
- Move article to `review-required/[topic]-[date].md`
- Create `review-required/[topic]-[date]_REVIEW_NOTES.md`
- Include final score breakdown, unresolved issues, and recommended human edits.

## Minimum Research Coverage Gate
Do not start section writing until the research files explicitly contain competitor gaps, real user questions, and mapped section usage. If this gate fails, continue research first instead of drafting placeholder sections.

## Handoff Note
When delivering outputs, include a short summary of what changed from research to draft so reviewers can validate that planned differentiation was actually implemented.
