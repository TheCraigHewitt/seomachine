# Rewrite Command

Refresh an existing article using analysis findings, current SERP context, and updated SEO requirements.

## Usage
`/rewrite [topic or analysis file]`

## Pre-Rewrite Review
- Read the original article fully.
- Review `/analyze-existing` output if available.
- Pull fresh research brief if the topic angle changed.
- Align with `@context/brand-voice.md` and `@context/seo-guidelines.md`.
- Check current SERP changes since original publication.

## Rewrite Strategy

### Scope Tiers
- **Light Update (20-30%)**: update stats, keywords, links, metadata
- **Moderate Refresh (40-60%)**: restructure sections, expand weak areas, refresh examples
- **Major Rewrite (70-90%)**: new structure + significantly expanded content
- **Complete Overhaul (90%+)**: effectively new article on same topic

### Keep / Update / Add / Remove

**Keep**
- Accurate sections with lasting value
- Effective structure and formatting
- Useful examples still relevant today
- Internal links that still serve intent

**Update**
- Outdated statistics and references
- Deprecated terminology/processes
- Weak keyword placement
- Meta title/description
- Broken or stale links

**Add**
- Missing sections identified by competitor gap analysis
- Current trends and use cases
- Stronger intro hook and clearer CTA path
- Missing SEO elements (keyword placement, links, snippet-ready answers)

**Remove**
- Deprecated claims
- Redundant/fluff sections
- Outdated references that no longer help the reader

## Rewrite Structure

### 1) H1 and Intro
- Keep original title if strong; update if weak/outdated.
- Ensure intro hook is timely and specific.
- Include primary keyword in first 100 words.

### 2) Body Improvements
- Maintain effective sections.
- Expand shallow sections.
- Add missing sections for uncovered intent and SERP gaps.
- Update data/examples throughout.
- Reorder sections if flow is weak.

### 3) Conclusion
- Refresh takeaways to reflect new content.
- Align CTA with current business priorities.

## SEO Enhancement

### Keyword and Intent
- Primary keyword density target: 1-2% (natural usage).
- Ensure keyword appears in H1, early intro, and key H2s.
- Add semantic variants where relevant.

### Internal Linking (3-5+)
- Keep only relevant working links.
- Add newer related content published since original.
- Use descriptive anchors.

### External Linking (2-3+)
- Replace broken links.
- Refresh old sources with current data.
- Favor authoritative references.

### Metadata
- Rework meta title (50-60 chars) and description (150-160 chars).
- Keep URL slug unless there is a strong reason to change.

## Quality Assurance
- Verify technical/data accuracy in all updated sections.
- Maintain voice/style alignment (`@context/style-guide.md`, `@context/brand-voice.md`).
- Improve readability: tighter sentences, cleaner subheadings, fewer wall-of-text paragraphs.

## Output

### 1) Rewritten Article
Complete markdown article with updated content and metadata.

### 2) Change Summary
```yaml
---
Original Publication Date: [if known]
Rewrite Date: [YYYY-MM-DD]
Rewrite Scope: Light / Moderate / Major / Complete
Word Count Change: [original] -> [new]
Primary Keyword: [keyword]
SEO Score Improvement: [estimated improvement]

Major Changes:
- [significant updates]
- [new sections added]
- [content removed/consolidated]

SEO Improvements:
- [keyword placement updates]
- [internal links added/updated]
- [meta updates]

Content Updates:
- [statistics refreshed]
- [examples replaced]
- [new trends added]
---
```

### 3) Before/After Comparison
For major rewrites, capture:
- headline change
- intro change
- sections added/removed
- word count delta
- key SEO improvements

## File Management
Save:
- Rewritten article: `rewrites/[topic-slug]-rewrite-[YYYY-MM-DD].md`
- Change summary: `rewrites/changes-[topic-slug]-[YYYY-MM-DD].md`

Example: `rewrites/content-marketing-guide-rewrite-2025-10-15.md`

## Automatic Scrubbing
Immediately scrub rewritten article:
```bash
/scrub rewrites/[topic-slug]-rewrite-[YYYY-MM-DD].md
```

## Post-Rewrite Agents
Run:
- `seo-optimizer`
- `meta-creator`
- `internal-linker`
- `keyword-mapper`

## Next Steps
1. Compare old vs new intro, heading map, and CTA path.
2. Verify refreshed stats have current sources, links resolve, and technical details are accurate.
3. Run `/optimize [rewritten file]` for final SEO score and publish readiness.
