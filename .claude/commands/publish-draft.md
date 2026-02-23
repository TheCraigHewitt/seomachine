# Publish Draft to WordPress

Publish a local markdown draft to WordPress as a **draft** with SEO metadata mapped automatically.

## Usage
`/publish-draft [filename] [--type post|page|custom]`

Examples:
```text
/publish-draft drafts/content-marketing-guide-2025-12-10.md
/publish-draft drafts/pricing-comparison.md --type page
/publish-draft drafts/product-comparison.md --type compare
```

## Post Types
- `post` (default): supports categories/tags
- `page`: no categories/tags
- custom type (for example `compare`): must be registered and REST-enabled in WordPress

## Metadata Mapping

| Draft Field | WordPress/Yoast Field |
|-------------|----------------------|
| H1 Title | Post Title |
| Meta Title | Yoast SEO Title |
| Meta Description | Yoast Meta Description + Excerpt |
| Target Keyword | Yoast Focus Keyphrase |
| URL Slug | Post Slug |
| Category | Post Categories |
| Tags | Post Tags |
| Content | Post Content (HTML) |

## Required Environment Variables
Set in `.env`:
```bash
WORDPRESS_URL=https://yoursite.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## Process
1. Validate draft file and parse frontmatter/content.
2. Convert markdown to HTML.
3. Publish via:
```bash
cd /path/to/seomachine
python data_sources/modules/wordpress_publisher.py "$FILE_PATH" --type "$POST_TYPE"
```
4. Return WordPress edit URL.

## Optional Taxonomy Fields
```markdown
**Category**: [Your Category]
**Tags**: [tag1], [tag2], [tag3]
```

## Troubleshooting
- `WORDPRESS_URL must be set`: add required env vars.
- `401 Unauthorized`: verify username, regenerate app password, confirm permissions.
- Missing category: created automatically.

## Notes
- Command always creates **drafts** (never auto-publishes).
- H1 becomes WordPress post title.
- Text content is uploaded; media files are not.
- Re-running on same file creates additional draft entries.

## Getting an Application Password (WordPress)
1. Go to WordPress Admin -> Users -> Your Profile.
2. Find **Application Passwords**.
3. Create a new password (for example: `SEO Machine`).
4. Copy it into `WORDPRESS_APP_PASSWORD` in `.env`.
