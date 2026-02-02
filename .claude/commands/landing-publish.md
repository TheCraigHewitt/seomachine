# Landing Page Publish Command

Use this command to publish landing pages to WordPress as pages (not blog posts).

## Usage
`/landing-publish [file path] [options]`

**Options:**
- `--noindex`: Set noindex meta (for PPC pages)
- `--template [slug]`: Use specific WordPress page template

**Examples:**
- `/landing-publish landing-pages/product-hosting-beginners-2025-12-11.md`
- `/landing-publish landing-pages/free-trial-ppc-2025-12-11.md --noindex`
- `/landing-publish landing-pages/pricing-comparison-2025-12-11.md --template landing-page`

## What This Command Does

1. Validates the landing page file
2. Checks landing page score (must be ≥75)
3. Parses markdown and metadata
4. Creates WordPress page via REST API
5. Sets Yoast SEO fields
6. Returns edit URL for review

## Prerequisites

Before publishing, ensure:
1. Landing page score is ≥75 (run `/landing-audit` first)
2. No critical issues remain
3. All required metadata is present
4. Content has been scrubbed for AI watermarks

## File Format Requirements

Landing page files must include this metadata:

```markdown
# [H1 Headline]

**Meta Title**: [50-60 characters]
**Meta Description**: [150-160 characters]
**Target Keyword**: [primary keyword]
**Page Type**: seo | ppc
**Conversion Goal**: trial | demo | lead
**URL Slug**: /[page-slug]/

---

[Content...]
```

## Publishing Process

### Step 1: Validation

Check file exists and contains required fields:
- Meta Title (required)
- Meta Description (required)
- Target Keyword (required for SEO pages)
- Page Type
- Conversion Goal
- URL Slug

### Step 2: Score Check

Run landing page scorer:
```python
from data_sources.modules.landing_page_scorer import score_landing_page

score = score_landing_page(content, page_type, goal, meta_title, meta_description, keyword)

if score['overall_score'] < 75:
    print("Score too low. Fix issues before publishing.")
    print(f"Current score: {score['overall_score']}")
    print(f"Critical issues: {score['critical_issues']}")
    # Abort publishing
```

### Step 3: Content Preparation

1. Parse metadata from file header
2. Extract main content (markdown)
3. Convert markdown to HTML
4. Prepare Yoast SEO fields

### Step 4: WordPress API Call

Uses existing `wordpress_publisher.py` module:

```python
from data_sources.modules.wordpress_publisher import WordPressPublisher

publisher = WordPressPublisher()

result = publisher.create_page(
    title=headline,
    content=html_content,
    slug=url_slug,
    status='draft',  # Always create as draft first
    meta={
        'yoast_wpseo_title': meta_title,
        'yoast_wpseo_metadesc': meta_description,
        'yoast_wpseo_focuskw': target_keyword,
    }
)
```

### Step 5: Additional Settings

**For PPC Pages (--noindex):**
```python
# Set noindex via Yoast
meta['yoast_wpseo_meta-robots-noindex'] = '1'
```

**For Page Templates:**
```python
# Set page template
result = publisher.update_page(
    page_id=page_id,
    template=template_slug
)
```

## Output

### Successful Publish
```
=== Landing Page Published ===

Status: Draft created
Page ID: [ID]
Edit URL: https://yoursite.com/wp-admin/post.php?post=[ID]&action=edit

Next Steps:
1. Review the page in WordPress
2. Check formatting and images
3. Set featured image if needed
4. Publish when ready

Landing Page Score: [X]/100
```

### Failed Publish
```
=== Publishing Failed ===

Reason: [Error message]

If score too low:
- Current Score: [X]/100
- Required Score: 75/100
- Critical Issues:
  1. [Issue 1]
  2. [Issue 2]

Run `/landing-audit landing-pages/[file].md` for full analysis.
```

## Differences from /publish-draft

| Aspect | /publish-draft (Blog) | /landing-publish (Pages) |
|--------|----------------------|--------------------------|
| WordPress Type | Post | Page |
| Categories/Tags | Yes | No |
| Score Required | Content score ≥70 | Landing page score ≥75 |
| noindex Option | No | Yes (for PPC) |
| Template Option | No | Yes |
| Output Directory | drafts/ | landing-pages/ |

## Pre-Publish Checklist

Before running this command, verify:

### Content
- [ ] Headline is benefit-focused
- [ ] Value proposition is clear
- [ ] CTAs use action verbs
- [ ] Trust signals present
- [ ] Risk reversal near CTAs
- [ ] FAQ section (for SEO pages)

### Meta
- [ ] Meta title 50-60 characters
- [ ] Meta title includes keyword
- [ ] Meta description 150-160 characters
- [ ] Meta description includes CTA
- [ ] URL slug is clean and short

### Technical
- [ ] Content scrubbed for AI watermarks
- [ ] Landing page score ≥75
- [ ] No critical issues
- [ ] Proper markdown formatting

## Post-Publish Tasks

After publishing to WordPress:

1. **Review in WordPress**
   - Check formatting displays correctly
   - Verify all links work
   - Ensure CTAs are prominent

2. **Add Visuals**
   - Set featured image
   - Add any hero images
   - Add trust badges/logos

3. **Final SEO Check**
   - Verify Yoast green lights
   - Check mobile preview
   - Validate schema if applicable

4. **Publish Live**
   - Change status from Draft to Published
   - Clear any caches
   - Verify live page loads correctly

## Rollback

If issues are found after publishing:

1. In WordPress, revert to draft status
2. Fix issues in the markdown file
3. Re-run `/landing-audit` to verify score
4. Re-publish with `/landing-publish`

## Integration with Other Commands

**Typical Workflow:**
```bash
# 1. Research (optional)
/landing-research "product hosting" --type seo

# 2. Create landing page
/landing-write "product hosting" --type seo --goal trial

# 3. Audit the draft
/landing-audit landing-pages/product-hosting-2025-12-11.md

# 4. Fix any issues (if needed)
# Edit the file manually

# 5. Re-audit until score ≥75
/landing-audit landing-pages/product-hosting-2025-12-11.md

# 6. Publish
/landing-publish landing-pages/product-hosting-2025-12-11.md
```
