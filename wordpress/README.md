# WordPress Integration Files

These files enable the SEO Machine tool to set Yoast SEO meta fields (Focus Keyphrase, SEO Title, Meta Description) via the REST API.

**Choose ONE option** - either the mu-plugin OR the functions.php snippet. They do the same thing.

---

## Option A: MU-Plugin (Recommended)

**File:** `seo-machine-yoast-rest.php`

**Installation:**
1. Upload to: `wp-content/mu-plugins/seo-machine-yoast-rest.php`
2. Create the `mu-plugins` folder if it doesn't exist
3. Done - mu-plugins auto-activate, no enabling required

**Pros:**
- Won't be lost during theme updates
- Can't be accidentally deactivated
- Clean separation from theme code

---

## Option B: Functions.php Snippet

**File:** `functions-snippet.php`

**Installation:**
1. Copy the contents of this file
2. Paste at the end of your theme's `functions.php`
3. Or use a code snippets plugin (WPCode, Code Snippets, etc.)

**Pros:**
- No new files to manage
- Works with code snippet plugins

**Cons:**
- Lost if theme is changed/updated (unless using child theme)

---

## What This Code Does

Registers a custom REST API field called `yoast_seo` on posts that allows reading and writing:

- `focus_keyphrase` → `_yoast_wpseo_focuskw`
- `seo_title` → `_yoast_wpseo_title`
- `meta_description` → `_yoast_wpseo_metadesc`

**API Usage:**
```json
POST /wp-json/wp/v2/posts/{id}
{
  "yoast_seo": {
    "focus_keyphrase": "your target keyword",
    "seo_title": "Your SEO Title | Brand",
    "meta_description": "Your meta description here."
  }
}
```

---

## Security

- Requires authentication (Application Password)
- User must have `edit_post` capability
- All inputs are sanitized with `sanitize_text_field()`
