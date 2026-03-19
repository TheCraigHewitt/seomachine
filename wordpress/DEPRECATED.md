# WordPress Integration — DEPRECATED

The files in this directory (`seo-machine-yoast-rest.php`, `functions-snippet.php`, `README.md`) are the original WordPress REST API integration for SEO Machine.

**Freaking Nomads does not use WordPress.** The site runs on Next.js with Payload CMS.

These files are kept for reference only — in case you need to adapt SEO Machine for a WordPress-based project in the future.

## Current Publishing Integration

Publishing for Freaking Nomads uses **Payload CMS**:

- **Publisher script**: `payload/payload_publisher.py`
- **Command**: `/publish-draft` (see `.claude/commands/publish-draft.md`)
- **Environment variables**: `PAYLOAD_API_URL`, `PAYLOAD_API_TOKEN`, `PAYLOAD_COLLECTION`

## What the WordPress integration did

- Connected to WordPress via REST API with Application Passwords
- Published posts with Yoast SEO metadata (focus keyphrase, SEO title, meta description)
- Converted Markdown to WordPress block format (Gutenberg HTML)

## If you need to re-enable WordPress support

1. Copy `data_sources/modules/wordpress_publisher.py` back into the active pipeline
2. Add WordPress env vars to `.env.example`: `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD`
3. Install the MU-plugin (`seo-machine-yoast-rest.php`) on your WordPress site
4. Update `.claude/commands/publish-draft.md` to reference the WordPress publisher
