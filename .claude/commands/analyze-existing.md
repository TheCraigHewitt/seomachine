# Analyze Existing Command

Analyze an existing post (URL or local file) for SEO quality, freshness, and rewrite priority.

## Usage
`/analyze-existing [URL or file path]`

## Process

### 1) Extract and Baseline Content
- Load full article content, structure, and metadata.
- Record publication date (if available).
- Flag stale claims, outdated statistics, and deprecated references.
- Assess coverage completeness for the core topic.

### 2) SEO Audit
- **Search intent analysis**: informational/commercial/transactional/navigational match.
- **Keyword analysis**:
  - identify primary keyword and variations
  - check density, distribution, and clustering
  - detect stuffing risks
- **Placement checks**:
  - H1, H2s, first 100 words
  - meta title and meta description
- **Length benchmarking**:
  - compare against top 10-20 SERP competitors
  - estimate required expansion/reduction
- **Link checks**:
  - internal link count/quality (target 3-5+)
  - external authority links and freshness
- **Readability checks**:
  - Flesch Reading Ease
  - Flesch-Kincaid grade
  - passive voice ratio and sentence complexity
- **SEO quality rating**: overall 0-100 + category breakdowns

### 3) Competitive Context
- Identify top competing pages for target keyword(s).
- Compare structure and depth.
- Document gaps competitors cover that this article misses.
- Note opportunities for a differentiated angle.

### 4) UX and Conversion Review
- Intro hook quality and clarity.
- Flow and scanability of sections.
- Actionability of advice.
- CTA alignment with intent.
- Missing visuals/media opportunities.

## Output

### 1) Content Health Score (0-100)
Include:
- SEO quality rating
- Search intent alignment score
- Keyword optimization score
- Length competitiveness score
- Readability score
- Freshness/relevance score
- UX score

### 2) Quick Wins (Top 3-5)
Immediate improvements such as:
- metadata fixes
- heading/keyword placement fixes
- stale data updates
- internal link additions
- readability cleanups

### 3) Strategic Improvements
Higher-effort recommendations:
- expansion targets from SERP benchmarks
- intent realignment
- missing topic cluster coverage
- structural rewrites for better performance

### 4) Detailed Analysis Artifacts
- intent classification with confidence
- keyword density heatmap by section
- topic cluster notes
- competitor length percentiles (min/median/75th)
- readability diagnostics

### 5) Rewrite Recommendation
- **Priority Level**: Low / Medium / High / Critical
- **Estimated Effort**: Light / Moderate / Major / Complete refresh
- **Expected Impact**: traffic/ranking/engagement estimate
- **Specific Targets**: word count, keyword, and readability deltas

### 6) Research Brief (if rewrite recommended)
Include updated keywords, competitor targets, missing data to source, and internal linking opportunities.

## File Management
Save report to:
`research/analysis-[post-slug]-[YYYY-MM-DD].md`

Example: `research/analysis-podcast-hosting-guide-2025-10-15.md`

## Next Steps
- Use `/rewrite [topic]` for medium/major recommendations.
- Use `/optimize [file]` when changes are mostly metadata/link polish.
