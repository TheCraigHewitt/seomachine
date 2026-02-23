# Landing Page Publish Command

Publish landing pages to WordPress as pages (not blog posts).

## Usage
`/landing-publish [file path] [options]`

**Options:**
- `--noindex` -- Set noindex meta (for PPC pages)
- `--template [slug]` -- Use specific WordPress page template

**Examples:**
- `/landing-publish landing-pages/product-hosting-beginners-2025-12-11.md`
- `/landing-publish landing-pages/free-trial-ppc-2025-12-11.md --noindex`

## Required File Format

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

1. **Validate** required fields: Meta Title, Meta Description, Target Keyword (SEO), Page Type, Conversion Goal, URL Slug
2. **Score check** -- must be >= 75:
```python
from data_sources.modules.landing_page_scorer import score_landing_page
score = score_landing_page(content, page_type, goal, meta_title, meta_description, keyword)
# Aborts if score['overall_score'] < 75
```
3. **Prepare** -- Parse metadata, convert markdown to HTML, prepare Yoast fields
4. **Publish** via WordPress REST API:
```python
from data_sources.modules.wordpress_publisher import WordPressPublisher
publisher = WordPressPublisher()
result = publisher.create_page(
    title=headline, content=html_content, slug=url_slug,
    status='draft',
    meta={
        'yoast_wpseo_title': meta_title,
        'yoast_wpseo_metadesc': meta_description,
        'yoast_wpseo_focuskw': target_keyword,
    }
)
```
5. **Additional settings:** `--noindex` sets `yoast_wpseo_meta-robots-noindex: '1'`; `--template` sets page template

Output: Draft page ID + WordPress edit URL.

## Differences from /publish-draft

| Aspect | /publish-draft (Blog) | /landing-publish (Pages) |
|--------|----------------------|--------------------------|
| WordPress Type | Post | Page |
| Categories/Tags | Yes | No |
| Score Required | Content >= 70 | Landing page >= 75 |
| noindex Option | No | Yes (PPC) |
| Template Option | No | Yes |
| Source Directory | drafts/ | landing-pages/ |

## Prerequisites

- Landing page score >= 75 (`/landing-audit` first)
- No critical issues
- Content scrubbed for AI watermarks

## Post-Publish

1. Review in WordPress (formatting, links, CTAs)
2. Set featured image and trust badges
3. Verify Yoast green lights + mobile preview
4. Change draft to Published, clear caches

**Rollback:** Revert to draft in WordPress, fix markdown, re-audit, re-publish.
