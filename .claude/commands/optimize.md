# Optimize Command

Perform a final SEO optimization pass before publishing.

## Usage
`/optimize [article file]`

## Process

### 1) Keyword Audit
- Measure primary keyword density (target 1-2%).
- Confirm keyword placement in:
  - H1
  - First 100 words
  - At least 2-3 H2 headings
  - Meta title
  - Meta description
  - URL slug
- Validate semantic keyword coverage.
- Flag over-optimization/keyword stuffing.

### 2) Heading and Structure Audit
- Ensure one H1 only.
- Validate clean H2/H3 hierarchy (no skipped levels).
- Confirm headings are descriptive and support search intent.

### 3) Content Quality Audit
- Word count target: 2000+ (2500-3000 preferred).
- Paragraph length: generally 2-4 sentences.
- Sentence mix: short + medium for readability.
- Reading level target: grade 8-10.
- Prefer active voice and clear transitions.
- Verify formatting supports scanability (lists, emphasis, spacing).

### 4) Link Optimization

#### Internal Links (3-5+)
- Validate quantity, relevance, and anchor quality.
- Ensure links cover pillar, related blog, and product/resource pages.
- Check for broken links.
- Cross-check opportunities in `@context/internal-links-map.md`.

#### External Links (2-3+)
- Validate source authority and relevance.
- Replace outdated or broken references.
- Ensure claims/statistics are properly sourced.

### 5) Meta Element Optimization

#### Meta Title
- 50-60 characters
- Includes primary keyword naturally
- Compelling and specific

#### Meta Description
- 150-160 characters
- Includes primary keyword
- Clear value proposition + action language

#### URL Slug
- Concise, lowercase, hyphenated
- Keyword-aligned, minimal filler words

Provide current-state analysis plus improved alternatives.

### 6) Technical/UX Checks
- Flag images missing alt text.
- Suggest featured snippet opportunities (definition/list/table/FAQ).
- Recommend schema where relevant (Article/FAQ/How-To).
- Validate brand and style alignment with `@context/brand-voice.md` and `@context/style-guide.md`.
- Check intro strength, CTA quality, and promise fulfillment.

## Output

### 1) SEO Score (0-100)
- Keyword Optimization: /25
- Technical SEO: /25
- Content Quality: /25
- User Experience: /25
- Overall: /100

### 2) Priority Fixes
List issues as:
- High priority (must fix before publish)
- Medium priority (recommended before publish)
- Low priority (optional improvements)

### 3) Recommendations by Effort
**Quick Wins (5-10 min):**
- Keyword placement tweaks
- Metadata improvements
- Internal link additions

**Strategic Improvements (longer):**
- Structural reorganization
- Content expansion
- Additional sourcing/research

### 4) Optimized Metadata Options
- 3-5 title options (with character counts)
- 3-5 description options (with character counts)
- Recommended final selection

### 5) Link Enhancement
- Internal links to add/update with suggested anchor text and section placement
- External sources to add/replace for unsupported claims

### 6) Keyword Distribution Map
Report where primary keyword appears (H1, intro, H2s, body, conclusion, metadata).

### 7) Publishing Readiness
- Status: `Ready` / `Needs Minor Fixes` / `Needs Revision`
- Estimated time to publish
- Ordered next steps

## File Management
Save report to:
`drafts/optimization-report-[topic-slug]-[YYYY-MM-DD].md`

Example: `drafts/optimization-report-podcast-analytics-2025-10-15.md`

## Agent Integration
Run final review with:
- `content-analyzer`
- `seo-optimizer`
- `meta-creator`
- `internal-linker`
- `keyword-mapper`

## Publishing Decision Bands
- 90-100: publish now
- 80-89: publish with minor tweaks
- 70-79: fix priority issues first
- <70: major revision needed

## Final Validation Checklist
- [ ] Primary keyword present in required fields/sections
- [ ] Density is natural (no stuffing)
- [ ] Heading hierarchy is clean and complete
- [ ] Internal/external link targets met
- [ ] No broken links
- [ ] Metadata within length limits
- [ ] Readability and scanability targets met
- [ ] CTA is clear and relevant
- [ ] Brand voice and style are consistent

## Content Analyzer Signals
When `content-analyzer` output is available, incorporate:
- Search intent match confidence
- Section-level keyword density and clustering
- Content length position vs SERP competitors
- Readability diagnostics
- SEO quality sub-scores with fix recommendations

Every issue in the report must include location and fix recommendation. Link recommendations must specify section placement and anchor text.
