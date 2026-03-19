# Publish Draft to Payload CMS

Publishes a draft article from this project to Freaking Nomads' Payload CMS as a draft, with all SEO metadata auto-populated.

## Usage
`/publish-draft [filename]`

### Examples

**Publish a blog post:**
```
/publish-draft drafts/finland-digital-nomad-visa-2026-03-15.md
```

**Publish a landing page:**
```
/publish-draft landing-pages/digital-nomad-visa-comparison.md
```

## What This Command Does

1. **Parses the draft file** — Extracts all metadata from frontmatter
2. **Converts Markdown to Lexical format** — Formats content for Payload CMS's rich text editor
3. **Creates a Payload CMS draft** — Posts via REST API with status "draft"
4. **Sets SEO metadata**:
   - Title (from H1)
   - Meta title (from frontmatter Meta Title)
   - Meta description (from frontmatter Meta Description)
   - Focus keyword (from frontmatter Target Keyword)
5. **Sets taxonomy** — Categories and tags if specified in frontmatter
6. **Returns the Payload admin edit URL** — Direct link to review the draft

## Metadata Mapping

| Draft Frontmatter Field | Payload CMS Field |
|---|---|
| H1 Title | `title` |
| Meta Title | `meta.title` |
| Meta Description | `meta.description` |
| Target Keyword | `meta.keywords` (or equivalent SEO field) |
| URL Slug | `slug` |
| Category | `categories` (relation) |
| Tags | `tags` (relation or array) |
| Author | `author` (relation — Irene, Luca, or contributor) |
| Content | `content` (Lexical rich text) |

## Required Environment Variables

Set these in `data_sources/config/.env`:
```
PAYLOAD_API_URL=https://freakingnomads.com/api
PAYLOAD_API_TOKEN=your_payload_api_token_here
PAYLOAD_COLLECTION=posts
```

### Getting a Payload API Token
1. Log into the Payload admin panel at your site's admin URL
2. Navigate to Settings or your user profile
3. Generate an API key with access to the posts collection
4. Add it to your `.env` file as `PAYLOAD_API_TOKEN`

> **Note**: The exact path for API key generation depends on your Payload CMS configuration. Check with Luca or Irene for the current setup.

## Process

When you run this command:

### Step 1: Validate File
- Confirm the draft file exists
- Parse frontmatter metadata and content
- Display extracted fields for confirmation
- Check that all mandatory fields are present (title, meta description, target keyword)

### Step 2: Pre-publish Check
Verify mandatory Freaking Nomads requirements are met:
- [ ] Author field set (Irene, Luca, or named contributor)
- [ ] Meta description ≤155 characters
- [ ] At least 3 internal links present in content
- [ ] FAQ section present
- [ ] AI detection has been run (flag if not confirmed)

### Step 3: Publish to Payload CMS
Run the Payload publisher:
```bash
python payload/payload_publisher.py "$FILE_PATH"
```

The publisher converts Markdown to Payload Lexical format and creates the draft via REST API.

### Step 4: Confirm Success
Display the Payload admin edit URL so the editor can review and publish.

## Draft Frontmatter Format

Your draft should include this frontmatter block:

```markdown
**Title**: Finland Digital Nomad Visa: Requirements, Costs & How to Apply
**Meta Title**: Finland Digital Nomad Visa: Complete 2026 Guide
**Meta Description**: Finland has no dedicated digital nomad visa — but its Self-Employment Visa works. Requirements, €400 cost, and 4-month timeline explained.
**Target Keyword**: Finland digital nomad visa
**URL Slug**: finland-digital-nomad-visa
**Author**: [Irene Wang | Luca Mussari | Contributor Name]
**Category**: Visas
**Tags**: Finland, Europe, Self-Employment Visa, Schengen
```

## Categories (FN Taxonomy)

Standard categories aligned with freakingnomads.com:
- `Digital Nomad Guides`
- `Destinations`
- `Visas`
- `Remote Work`
- `Gear & Tech`
- `Insurance`
- `Finance & Banking`
- `Lifestyle`
- `Community`
- `Legal & Taxes`
- `Online Income`

## Troubleshooting

### "PAYLOAD_API_URL must be set"
Add credentials to `data_sources/config/.env`. See Required Environment Variables above.

### "401 Unauthorized"
- Verify the API token is correct
- Check that the token has write access to the posts collection
- Regenerate the token in Payload admin if needed

### "Collection not found"
- Verify `PAYLOAD_COLLECTION` matches your Payload schema collection name exactly
- Common values: `posts`, `articles`, `blog-posts`

### "Lexical conversion error"
The Markdown-to-Lexical converter handles standard Markdown. If you have custom elements, simplify them before publishing and add them manually in the Payload editor.

## Notes

- Posts are always created as **drafts** (never published automatically)
- The H1 heading becomes the Payload post title
- Images referenced in Markdown are not uploaded — add them manually in Payload admin after publishing the draft
- You can run this command multiple times on the same file (creates new drafts each time)
- After publishing, always review in Payload admin before setting to "published"

## Legacy WordPress Integration

The `wordpress/` directory contains the original WordPress MU-plugin and publisher. It is no longer used for Freaking Nomads (which runs on Payload CMS / Next.js). See `wordpress/DEPRECATED.md` for details.
