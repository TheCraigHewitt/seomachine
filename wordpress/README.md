# WordPress Integration Files

These files enable the SEO Machine tool to set Yoast SEO meta fields (Focus Keyphrase, SEO Title, Meta Description) via the REST API and optionally add a front-end day/night mode toggle.

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

## Option C: Theme Day/Night Toggle

**File:** `theme-mode-toggle.php`

**What it adds:**
- Floating toggle button in the bottom-right corner
- Day mode / night mode switching on the front-end
- Preference persistence via browser local storage
- Auto-detect fallback from `prefers-color-scheme` when no explicit choice exists

**Installation (MU-plugin):**
1. Upload to: `wp-content/mu-plugins/theme-mode-toggle.php`
2. Done - it auto-activates

**Alternative installation:**
1. Open `theme-mode-toggle.php`
2. Copy function contents into your active theme's `functions.php`

**Verification checklist:**
1. Open your site in a browser and hard refresh (`Ctrl+F5`)
2. Confirm the toggle appears at the bottom-right
3. Click `Night mode` and verify site colors change to dark
4. Reload the page and confirm your selected mode persists
5. Click `Day mode` to switch back

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
