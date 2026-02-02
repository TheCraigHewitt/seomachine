# Publish Draft to WordPress

Publishes a draft article from this project to WordPress as a Draft, with all SEO metadata auto-populated.

## Usage
`/publish-draft [filename] [--type post|page|custom]`

### Examples

**Create a blog post (default):**
```
/publish-draft drafts/content-marketing-guide-2025-12-10.md
```

**Create a page:**
```
/publish-draft drafts/pricing-comparison.md --type page
```

**Create a custom post type:**
```
/publish-draft drafts/product-comparison.md --type compare
```

### Post Types
- `post` - Standard blog post (default) - supports categories and tags
- `page` - WordPress page - no categories/tags
- Custom types (e.g., `compare`) - must be registered in WordPress with REST API support

## What This Command Does

1. **Parses the draft file** - Extracts all metadata from frontmatter
2. **Converts Markdown to HTML** - Formats content for WordPress
3. **Creates WordPress draft** - Posts via REST API with status "draft"
4. **Sets Yoast SEO fields**:
   - SEO Title (from Meta Title)
   - Meta Description
   - Focus Keyphrase (from Target Keyword)
5. **Assigns taxonomy** - Categories and Tags if specified
6. **Returns edit URL** - Direct link to edit the post in WordPress

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

These must be set in `.env`:
```
WORDPRESS_URL=https://yoursite.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

### Getting an Application Password
1. Log into WordPress Admin
2. Go to Users > Your Profile
3. Scroll to "Application Passwords"
4. Enter a name (e.g., "SEO Machine")
5. Click "Add New Application Password"
6. Copy the generated password to your `.env` file

## Process

When you run this command:

### Step 1: Validate File
- Confirm the draft file exists
- Parse metadata and content
- Display extracted fields for confirmation

### Step 2: Publish to WordPress
Run the WordPress publisher:
```bash
cd /path/to/seomachine
python data_sources/modules/wordpress_publisher.py "$FILE_PATH" --type "$POST_TYPE"
```

Where `$POST_TYPE` is `post`, `page`, or a custom post type.

### Step 3: Confirm Success
Display the WordPress edit URL so the user can review and publish.

## Optional: Add Categories/Tags

To assign categories or tags, add these fields to your draft frontmatter:

```markdown
**Category**: [Your Category]
**Tags**: [your topic], beginner, getting started
```

Multiple categories/tags are comma-separated.

## Troubleshooting

### "WORDPRESS_URL must be set"
Add credentials to `.env` file. See Required Environment Variables above.

### "401 Unauthorized"
- Verify username is correct
- Regenerate Application Password
- Ensure user has permission to create posts

### "Could not find category"
The category will be created automatically if it doesn't exist.

## Notes

- Posts are always created as **drafts** (never published automatically)
- The H1 heading from the article becomes the WordPress post title
- Images/media are not uploaded - only text content is transferred
- You can run this command multiple times on the same file (creates new drafts each time)
