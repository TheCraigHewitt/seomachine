# Scrub Command

Use this command to remove AI-generated content watermarks and telltale signs from markdown files.

## Usage
`/scrub [file path]`

## What This Command Does
Removes invisible Unicode watermarks and replaces em-dashes with contextually appropriate punctuation to make content appear naturally human-written.

## What Gets Removed/Replaced

### Invisible Unicode Watermarks Removed:
- **Zero-width spaces (U+200B)**: Often used for word-breaking and watermarking
- **Byte Order Mark (U+FEFF)**: Text encoding indicator, sometimes inserted as watermark
- **Zero-width non-joiners (U+200C)**: Prevents character joining, used for watermarking
- **Word joiner (U+2060)**: Invisible character that prevents line breaks
- **Soft hyphen (U+00AD)**: Invisible hyphen used for watermarking
- **Narrow no-break space (U+202F)**: Special space character
- **All Unicode Category Cf characters**: Format-control codepoints

### Em-Dash Replacement (U+2014):
Em-dashes are replaced with contextually appropriate punctuation:
- **Comma**: For simple separation, parenthetical phrases, or lists
- **Semicolon**: For independent clauses that are closely related
- **Period**: For strong breaks or when the em-dash separates complete thoughts
- **Space**: When em-dash is used for attribution

The scrubber analyzes sentence structure and context to determine the most natural replacement.

## Process

### 1. Read the File
Load the specified markdown file from the file path provided.

### 2. Run Content Scrubber
Execute the Python content scrubber module:

```python
import sys
sys.path.append('data_sources/modules')
from content_scrubber import scrub_file

# Scrub the file (overwrites original with cleaned version)
scrub_file('[file_path]', verbose=True)
```

### 3. Report Results
Show statistics about what was cleaned:
- Number of invisible Unicode characters removed
- Number of format-control characters removed
- Number of em-dashes replaced
- File location of cleaned content

### 4. Verify Clean Content
Read a sample of the cleaned content to verify it looks natural and all watermarks are removed.

## Output Format

```
Content Scrubbing Complete:
  - Unicode watermarks removed: [count]
  - Format-control chars removed: [count]
  - Em-dashes replaced: [count]

Scrubbed content saved to: [file_path]

Sample of cleaned content:
[First 300 characters of cleaned content]

✓ Content successfully scrubbed of AI watermarks
```

## Example Usage

```
/scrub drafts/content-marketing-guide-2025-10-31.md
```

This will:
1. Read the file
2. Remove all invisible watermarks
3. Replace em-dashes with appropriate punctuation
4. Save the cleaned version (overwrites original)
5. Show statistics and sample

## File Requirements
- File must be a markdown (.md) file
- File must exist in the workspace
- File will be overwritten with cleaned version (original is replaced)

## Best Practices
- Run `/scrub` after generating content with `/write` or `/rewrite` (though this should happen automatically)
- Useful for cleaning files before publishing
- Can be run on any markdown file in the workspace
- Safe to run multiple times (idempotent - won't change already-clean content)

## Technical Details

The scrubber uses intelligent context analysis to replace em-dashes:

**Example transformations**:
- "This is great—you'll love it" → "This is great, you'll love it" (comma for simple separation)
- "I tried everything—nothing worked" → "I tried everything; nothing worked" (semicolon for independent clauses)
- "Here's the thing—AI content is detectable" → "Here's the thing: AI content is detectable" (natural separation)

The goal is to make the content indistinguishable from naturally human-written text while maintaining readability and proper grammar.

## Integration Note

This command is automatically triggered after `/write` and `/rewrite` commands, so you typically don't need to run it manually. Use this command when:
- Testing the scrubber
- Cleaning older content that wasn't auto-scrubbed
- Verifying scrubbing was successful
- Cleaning content from external sources

---

**Result**: Content that is clean of AI watermarks and appears naturally human-written.
