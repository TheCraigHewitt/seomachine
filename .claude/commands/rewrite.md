# Rewrite Command

Use this command to update and improve existing your company blog posts based on analysis findings.

## Usage
`/rewrite [topic or analysis file]`

## What This Command Does
1. Takes existing blog post content and improvement recommendations
2. Rewrites content with updated information and SEO optimization
3. Maintains original article structure where effective
4. Adds new sections to fill content gaps
5. Updates outdated statistics, examples, and references

## Process

### Pre-Rewrite Review
- **Original Content**: Read the existing article thoroughly
- **Analysis Report**: Review findings from `/analyze-existing` if available
- **Research Brief**: Check if new research brief exists for updated angles
- **Brand Voice**: Verify alignment with current @context/brand-voice.md
- **SEO Guidelines**: Apply latest requirements from @context/seo-guidelines.md
- **Competitive Context**: Understand what's changed in SERP since original publication

### Rewrite Strategy

#### Determine Scope
Based on analysis, classify the rewrite level:
- **Light Update (20-30% changes)**: Fix stats, add keywords, improve meta
- **Moderate Refresh (40-60% changes)**: Restructure sections, expand content, update examples
- **Major Rewrite (70-90% changes)**: New outline, significant expansion, fresh angle
- **Complete Overhaul (90%+ changes)**: Essentially new article on same topic

#### What to Keep
- Sections that are still accurate and comprehensive
- Unique insights or perspectives that remain valuable
- Well-performing structure or formatting
- Examples or case studies that are still relevant
- Internal links that remain appropriate

#### What to Update
- Outdated statistics with current data (note date/source)
- Old screenshots or examples with current versions
- Deprecated terminology or processes
- Missing keywords in headings and body
- Weak or missing meta title/description
- Insufficient internal links

#### What to Add
- New sections to fill competitive content gaps
- Recent industry trends or developments
- Additional examples or use cases
- Better introduction hook if current one is weak
- Stronger conclusion and CTA
- Missing SEO elements (keywords, links, structure)

#### What to Remove
- Deprecated information that's no longer accurate
- Redundant or repetitive sections
- Overly promotional language (if inconsistent with current brand)
- Outdated examples or references
- Fluff or filler that doesn't add value

### Content Structure
Follow same structure as `/write` command:

#### 1. Updated Headline (H1)
- Optimize with primary keyword if not already present
- Refresh if original title is dated or weak
- Maintain original if it's strong and still optimized

#### 2. Refreshed Introduction
- Update hook with current statistics or trends
- Clarify value proposition if needed
- Ensure primary keyword appears in first 100 words
- Make it compelling for today's reader

#### 3. Improved Body
- **Maintain**: Keep effective sections that are still accurate
- **Expand**: Deepen shallow sections with more detail
- **Add**: Insert new sections to cover content gaps
- **Update**: Refresh stats, examples, and references throughout
- **Restructure**: Reorganize if flow can be improved
- **Optimize**: Integrate keywords more naturally if needed

#### 4. Strengthened Conclusion
- Update takeaways to reflect new/expanded content
- Refresh CTA to align with current your company priorities
- End with forward-looking perspective

### SEO Enhancement

#### Keyword Optimization
- **Primary Keyword**: Ensure 1-2% density throughout
- **Keyword Placement**: Add to H2s if missing
- **Semantic Variations**: Use related keywords naturally
- **First 100 Words**: Confirm primary keyword appears early
- **Natural Integration**: Never force keywords unnaturally

#### Internal Linking
- **Review Existing**: Ensure all internal links still work and are relevant
- **Add New Links**: Reference newer your company content published since original
- **Strategic Placement**: Link to pillar content and related articles
- **Anchor Text**: Use keyword-rich, descriptive anchor text
- **Quantity**: Aim for 3-5+ quality internal links

#### External Linking
- **Update Broken Links**: Replace any dead external links
- **Fresher Sources**: Replace old statistics with recent data
- **Authority**: Ensure external links are to credible sources
- **Relevance**: Remove outdated external references

#### Meta Elements
- **Meta Title**: Rewrite if not optimized or compelling
- **Meta Description**: Refresh to highlight updated content
- **URL Slug**: Generally keep original to preserve any rankings
- **Featured Snippet**: Optimize for snippet opportunity if identified

### Quality Assurance

#### Content Accuracy
- Verify all updated statistics and data points
- Ensure technical information is current
- Confirm examples reflect current podcast landscape
- Check that your company product references are up-to-date

#### Brand Alignment
- Maintain your company voice from @context/brand-voice.md
- Follow formatting from @context/style-guide.md
- Ensure messaging aligns with current positioning
- Keep focus on target audience needs

#### Readability
- Improve sentence structure if needed
- Break up long paragraphs
- Add subheadings for better scannability
- Use formatting (bold, lists) to enhance clarity

## Output
Provides updated article with change tracking:

### 1. Rewritten Article
Complete markdown article with all improvements:
- Updated headline if changed
- Refreshed introduction
- Improved and expanded body sections
- Strengthened conclusion
- All new meta elements

### 2. Change Summary
```
---
Original Publication Date: [if known]
Rewrite Date: [YYYY-MM-DD]
Rewrite Scope: Light / Moderate / Major / Complete
Word Count Change: [original count] → [new count]
Primary Keyword: [keyword]
SEO Score Improvement: [estimated improvement]

Major Changes:
- [Summary of significant updates]
- [New sections added]
- [Content removed/consolidated]

SEO Improvements:
- [Keyword optimization details]
- [Internal links added]
- [Meta element updates]

Content Updates:
- [Statistics refreshed]
- [Examples updated]
- [New industry trends added]
---
```

### 3. Before/After Comparison
For major changes, note key differences:
- Original headline vs. new headline
- Original intro vs. new intro
- Sections added or removed
- Word count expansion
- SEO element improvements

## File Management
After completing the rewrite, save to:
- **File Location**: `rewrites/[topic-slug]-rewrite-[YYYY-MM-DD].md`
- **File Format**: Markdown with change summary frontmatter
- **Naming Convention**: Use original slug + "rewrite" + current date

Example: `rewrites/podcast-hosting-guide-rewrite-2025-10-15.md`

Also save the change summary separately:
- **File Location**: `rewrites/changes-[topic-slug]-[YYYY-MM-DD].md`

## Automatic Content Scrubbing
**IMPORTANT**: Immediately after saving the rewritten article file, automatically scrub the content to remove AI watermarks:

1. Run the content scrubber on the saved file:
```python
import sys
sys.path.append('data_sources/modules')
from content_scrubber import scrub_file

# Scrub the file (overwrites with cleaned version)
scrub_file('rewrites/[topic-slug]-rewrite-[YYYY-MM-DD].md', verbose=True)
```

2. This removes:
   - All invisible Unicode watermarks (zero-width spaces, format-control characters, etc.)
   - Em-dashes, replaced with contextually appropriate punctuation

3. The scrubbing happens silently and automatically - no user action required

**Result**: Rewritten content is clean of AI watermarks before agents analyze it.

## Automatic Agent Execution
After saving the rewritten article, run optimization agents:

### 1. SEO Optimizer Agent
- Review rewritten content for SEO improvements
- Compare against original SEO metrics
- Provide optimization score

### 2. Meta Creator Agent
- Generate fresh meta title/description options
- Test multiple variations for click-through optimization

### 3. Internal Linker Agent
- Ensure all internal links are current and relevant
- Suggest additional linking opportunities from newer content

### 4. Keyword Mapper Agent
- Verify keyword integration improvements
- Confirm optimal keyword placement and density

## Next Steps
After rewrite completion:
1. Review change summary and ensure all updates are intentional
2. Compare to original to verify improvements
3. Run `/optimize` for final polish if needed
4. Move to `/published` when ready
5. Note original URL to ensure proper redirect/replacement

This ensures every rewritten article is significantly improved while maintaining what worked in the original version.
