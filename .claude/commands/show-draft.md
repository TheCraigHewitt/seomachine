# Show Draft Command

Renders a clean, formatted preview of a draft article and saves it to `data/` as a standalone `.md` file — ready to share, review, or copy-paste.

## Usage
`/show-draft [filename]`

### Examples

```
/show-draft drafts/finland-digital-nomad-visa-2026-03-15.md
```

```
/show-draft
```
*(with no argument: lists all files in `drafts/` and asks which to show)*

---

## What This Command Does

1. **Reads the draft file** from `drafts/` (or any path you provide)
2. **Strips away all tooling metadata** — no SEO reports, no agent output blocks, no frontmatter key-value lines
3. **Renders a clean formatted version** with a compact info header followed by the full article
4. **Saves to `data/[slug].md`** — a clean standalone file with no clutter
5. **Displays the article** in the conversation so you can read and review it immediately

---

## Process

### Step 1: Locate the File

If a file path is given, read it directly.

If no argument is provided:
- List all `.md` files in `drafts/`
- Ask the user which one to show

### Step 2: Parse the Draft

Extract from the file:
- **Title** — from the H1 heading or `**Title**:` frontmatter field
- **Meta Title** — from `**Meta Title**:` field
- **Meta Description** — from `**Meta Description**:` field
- **Target Keyword** — from `**Target Keyword**:` field
- **Author** — from `**Author**:` field
- **Category** — from `**Category**:` field
- **URL Slug** — from `**URL Slug**:` field
- **Word count** — count words in the article body

Strip out all frontmatter lines (the `**Field**: value` lines), leaving only the article body (H1 + content).

### Step 3: Build the Formatted Output

Assemble a clean `.md` file in this format:

```markdown
---
title: [Title]
meta_title: [Meta Title]
meta_description: [Meta Description]
keyword: [Target Keyword]
author: [Author]
category: [Category]
slug: [URL Slug]
word_count: [N words]
source: [original file path]
---

[Full article content, exactly as written, starting from H1]
```

The article content block should be:
- The H1 heading
- Every section, paragraph, list, table exactly as in the draft
- No truncation, no summarization
- No added commentary or agent notes

### Step 4: Save to `data/`

Create the `data/` folder if it doesn't exist.

Save the file as:
```
data/[slug].md
```

Where `[slug]` is taken from the `**URL Slug**:` frontmatter field, or derived from the H1 title if no slug is set (lowercase, hyphenated).

If a file with that name already exists in `data/`, overwrite it (the draft is the source of truth).

### Step 5: Display in Conversation

After saving, render the full article directly in the conversation so the user can read it immediately. Show:

1. A brief one-line confirmation: `Saved to data/[slug].md ([N] words)`
2. The full formatted article, rendered as markdown

---

## Output File Format

The `data/[slug].md` file is the clean, shareable version of the article. It contains:

- A YAML frontmatter block with all meta fields (for reference / CMS import)
- The complete article body in clean Markdown
- Nothing else — no agent notes, no SEO checklist, no optimization reports

This file is safe to share with editors, send to contributors for review, or paste into a CMS manually.

---

## Notes

- The `data/` folder is for clean formatted outputs only — do not store drafts, reports, or research there
- If the draft has multiple agent output files (e.g. `seo-report-*.md`, `meta-options-*.md`), ignore them — only process the main article file
- Word count in the header is article body only (not frontmatter)
- This command does not modify the original draft file in any way
