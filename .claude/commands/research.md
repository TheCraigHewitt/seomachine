# Research Command

Run SEO keyword research and competitive analysis before drafting new content.

## Usage
`/research [topic]`

## Process

### 1) Keyword Research
- Pick one primary keyword aligned to the topic.
- Capture estimated monthly volume and keyword difficulty.
- Identify 3-5 related keywords (semantic variants and long-tail terms).
- Pull related questions from People Also Ask, forums, and Reddit.
- Classify intent: informational, navigational, commercial, or transactional.
- Map topic fit to your cluster priorities in `@context/target-keywords.md`.

### 2) Competitive Analysis
- Review top 10 SERP results for the target keyword.
- Record article length benchmarks and common H2/H3 patterns.
- Note sections that appear in most top pages (must-cover topics).
- Identify content gaps, weak sections, outdated data, and missing angles.
- Check featured snippet opportunities (paragraph/list/table).
- Note domain patterns (indie blogs, SaaS docs, major publications).

### 3) Context Integration
- Align findings with `@context/brand-voice.md`.
- Confirm SEO constraints from `@context/seo-guidelines.md`.
- Pull internal link targets from `@context/internal-links-map.md`.
- Cross-check keyword priority in `@context/target-keywords.md`.

### 4) Audience and Industry Focus
- Define audience pain points this topic should solve.
- Add concrete use cases and real scenarios to include.
- Capture industry-specific technical constraints or terminology.
- Note trends that should be reflected in the angle.

### 5) Content Planning
- Recommend H2/H3 outline and target depth.
- Set word-count target (typically 2000-3000+ for competitive topics).
- List evidence needs: stats, studies, quotes, examples.
- Suggest visuals (screenshots/charts/diagrams).
- Map 3-5 internal links and 2-3 external authority links.
- Define introduction angle, value proposition, and story hooks.

## Output

### 1. SEO Foundation
- Primary keyword + volume/difficulty
- 3-5 secondary keywords
- Target word count
- Featured snippet opportunity (Yes/No + format)

### 2. Competitive Landscape
- Top 3 competitor articles (URL + key takeaway)
- Must-cover sections from SERP patterns
- Content gaps and under-served angles
- Differentiation strategy for your company perspective

### 3. Recommended Outline
```markdown
H1: [Optimized headline with primary keyword]

Introduction
- Hook
- Problem statement
- Value proposition

H2: [Main section 1]
H3: [Subsection]
H3: [Subsection]

H2: [Main section 2]
...

Conclusion
- Key takeaways
- Call to action
```

### 4. Supporting Elements
- 5-7 statistics with sources
- Expert quote candidates
- Case study/story opportunities
- Visual suggestions

### 5. Internal Linking Strategy
- Pillar page target
- 2-4 related article links
- Product/feature pages to reference
- Supporting resource/tool pages

### 6. Meta Preview
- Meta title draft (50-60 characters)
- Meta description draft (150-160 characters)
- Recommended URL slug

## File Management
Save research brief to:
`research/brief-[topic-slug]-[YYYY-MM-DD].md`

Example: `research/brief-podcast-editing-software-2025-10-15.md`

## Next Steps
Use the brief with `/write [topic]` (or `/article [topic]` for full end-to-end pipeline).
