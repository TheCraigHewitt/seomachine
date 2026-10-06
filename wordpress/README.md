# WordPress Integration Files

These files enable the SEO Machine tool to set SEO meta fields (Focus Keyphrase, SEO Title, Meta Description) via the REST API for either **Yoast SEO** or **RankMath**.

**Choose ONE option** - either the mu-plugin OR the functions.php snippet. They do the same thing.

---

## Option A: MU-Plugin (Recommended)

**Files:** `seo-machine-yoast-rest.php` and/or `seo-machine-rankmath-rest.php`

**Installation:**
1. Upload the relevant file(s) for the SEO plugin(s) you use to: `wp-content/mu-plugins/`
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

Registers custom REST API fields called `yoast_seo` and/or `rankmath_seo` on posts that allows reading and writing:

**Yoast SEO:**
- `focus_keyphrase` → `_yoast_wpseo_focuskw`
- `seo_title` → `_yoast_wpseo_title`
- `meta_description` → `_yoast_wpseo_metadesc`

**RankMath:**
- `focus_keyphrase` → `rank_math_focus_keyword`
- `seo_title` → `rank_math_title`
- `meta_description` → `rank_math_description`

**API Usage (Yoast):**
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

**API Usage (RankMath):**
```json
POST /wp-json/wp/v2/posts/{id}
{
  "rankmath_seo": {
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
