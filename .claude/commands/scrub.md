# Scrub Command

Remove invisible watermark characters and normalize AI-typical punctuation artifacts in markdown files.

## Usage
`/scrub [file path]`

## What This Command Does
1. Removes invisible Unicode watermark characters.
2. Replaces em-dashes (`—`) with context-appropriate punctuation.
3. Normalizes spacing/formatting artifacts.
4. Reports exact counts of changes.

## Character Classes Removed
The scrubber removes:
- Zero-width spaces (`U+200B`)
- Byte Order Marks (`U+FEFF`)
- Zero-width non-joiners (`U+200C`)
- Word joiners (`U+2060`)
- Soft hyphens (`U+00AD`)
- Narrow no-break spaces (`U+202F`)
- Any Unicode format-control character (`Cf` category)

## Em-Dash Normalization Rules
When replacing `—`, use context:
- Attribution style -> comma
  - `"Quote — Author"` -> `"Quote, Author"`
- Independent clauses -> semicolon
  - `"A — B"` -> `"A; B"`
- Strong sentence break -> period
  - `"Sentence one — Sentence two"` -> `"Sentence one. Sentence two"`
- Simple separator -> comma
- Before conjunctive adverbs (`however`, `therefore`, `moreover`) -> semicolon

## Whitespace Normalization
- Collapse repeated spaces to single spaces
- Remove spaces before punctuation
- Ensure single space after punctuation
- Reduce 3+ blank lines to 2

## Output Format
```text
Content Scrubbing Complete:
  - Unicode watermarks removed: [count]
  - Format-control chars removed: [count]
  - Em-dashes replaced: [count]
```

## File Behavior and Safety
- Updates file in place.
- Preserves markdown structure and visible meaning.
- Idempotent: re-running on clean content produces no further changes.
- Safe for automated workflows.

## Workflow Integration
Run immediately after `/write` or `/rewrite` and before optimization/publishing.

## Implementation
- Module: `data_sources/modules/content_scrubber.py`
- Main function: `scrub_file(file_path, output_path, verbose)`
- Class: `ContentScrubber`

## Example
```text
/scrub drafts/content-marketing-strategies-2025-10-31.md
```

Before:
```text
Content​ marketing​ is​ a​ powerful​ strategy—businesses can reach global audiences—and convert more customers.
```

After:
```text
Content marketing is a powerful strategy; businesses can reach global audiences, and convert more customers.
```

## Why This Matters
Generated content can include invisible markers and punctuation patterns that are easy to detect and often reduce editorial quality. Scrubbing standardizes output before optimization and publishing.

## Best Practices
1. Run scrub immediately after file generation.
2. Review scrub statistics for unexpected spikes in removals.
3. Keep scrub as a required step in automated writing/rewrite pipelines.
4. Re-run safely after major edits if content was regenerated.

## Verification
After scrubbing, spot-check at least one previously problematic section to confirm punctuation reads naturally and markdown formatting remains intact.
