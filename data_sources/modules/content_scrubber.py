"""
Content Scrubber

Removes AI-generated content watermarks and telltale signs including:
- Invisible Unicode characters (zero-width spaces, format-control characters, etc.)
- Em-dashes replaced with contextually appropriate punctuation

This module ensures content appears naturally human-written.
"""

import re
import unicodedata
from typing import Dict, List, Tuple


class ContentScrubber:
    """
    Scrubs AI-generated content to remove watermarks and telltale patterns.
    """

    # Specific Unicode characters to remove
    WATERMARK_CHARS = [
        '\u200B',  # Zero-width space
        '\uFEFF',  # Byte Order Mark (BOM)
        '\u200C',  # Zero-width non-joiner
        '\u2060',  # Word joiner
        '\u00AD',  # Soft hyphen
        '\u202F',  # Narrow no-break space
    ]

    def __init__(self):
        self.stats = {
            'unicode_removed': 0,
            'emdashes_replaced': 0,
            'format_control_removed': 0,
        }

    def scrub(self, content: str) -> Tuple[str, Dict]:
        """
        Scrub content of all AI watermarks and telltale signs.

        Args:
            content: The text content to scrub

        Returns:
            Tuple of (cleaned_content, statistics_dict)
        """
        # Reset stats
        self.stats = {
            'unicode_removed': 0,
            'emdashes_replaced': 0,
            'format_control_removed': 0,
        }

        # Step 1: Remove specific watermark characters
        content = self._remove_watermark_chars(content)

        # Step 2: Remove all Unicode format-control characters (Category Cf)
        content = self._remove_format_control_chars(content)

        # Step 3: Replace em-dashes with contextually appropriate punctuation
        content = self._replace_emdashes(content)

        # Step 4: Clean up any double spaces created by removals
        content = self._clean_whitespace(content)

        return content, self.stats

    def _remove_watermark_chars(self, content: str) -> str:
        """Remove specific invisible Unicode watermark characters."""
        original_len = len(content)

        for char in self.WATERMARK_CHARS:
            # Replace zero-width space with regular space if between word characters
            if char == '\u200B':
                # Replace zero-width space between alphanumeric chars with regular space
                content = re.sub(r'(\w)\u200B(\w)', r'\1 \2', content)
                # Remove any remaining zero-width spaces
                content = content.replace(char, '')
            else:
                content = content.replace(char, '')

        self.stats['unicode_removed'] = original_len - len(content)
        return content

    def _remove_format_control_chars(self, content: str) -> str:
        """Remove all Unicode Category Cf (format-control) characters."""
        cleaned = []
        removed = 0

        for char in content:
            if unicodedata.category(char) == 'Cf':
                removed += 1
                continue
            cleaned.append(char)

        self.stats['format_control_removed'] = removed
        return ''.join(cleaned)

    def _replace_emdashes(self, content: str) -> str:
        """
        Replace em-dashes with contextually appropriate punctuation.

        Analyzes the context around each em-dash to determine the best replacement:
        - Comma: For simple separation, parenthetical phrases, or lists
        - Semicolon: For independent clauses that are closely related
        - Period: For strong breaks or when near sentence end
        - Space: When em-dash is used for attribution or breaking phrases
        """
        # Find all em-dashes with surrounding context
        emdash_pattern = r'([^—]{0,100})—([^—]{0,100})'

        def replace_emdash(match):
            before = match.group(1)
            after = match.group(2)

            replacement = self._determine_emdash_replacement(before, after)
            self.stats['emdashes_replaced'] += 1

            return before + replacement + after

        content = re.sub(emdash_pattern, replace_emdash, content)

        return content

    def _determine_emdash_replacement(self, before: str, after: str) -> str:
        """
        Determine the best punctuation to replace an em-dash.

        Args:
            before: Text before the em-dash
            after: Text after the em-dash

        Returns:
            Replacement punctuation string
        """
        # Get the last 50 chars before and first 50 chars after
        before_context = before[-50:].strip() if before else ""
        after_context = after[:50].strip() if after else ""

        # Check if at the end of a sentence (em-dash before end punctuation)
        if after_context and after_context[0] in '.!?':
            return ''  # Remove em-dash, keep the end punctuation

        # Check if it's an attribution or citation (often at end)
        attribution_patterns = [
            r'\b(said|wrote|noted|according to|via)\s*$',
            r'^[A-Z][a-z]+ [A-Z]',  # Looks like "John Smith" after
        ]
        for pattern in attribution_patterns:
            if re.search(pattern, before_context, re.IGNORECASE) or \
               re.match(pattern, after_context):
                return ', '

        # Check if before text ends with a complete clause
        # Indicators: ends with noun/verb pattern, has subject
        has_verb_before = bool(re.search(r'\b(is|are|was|were|has|have|had|do|does|did|can|could|will|would|should|may|might)\b', before_context[-30:], re.IGNORECASE))
        has_verb_after = bool(re.search(r'\b(is|are|was|were|has|have|had|do|does|did|can|could|will|would|should|may|might)\b', after_context[:30], re.IGNORECASE))

        # If both sides have verbs, they might be independent clauses
        if has_verb_before and has_verb_after:
            # Check if after starts with capital (stronger break)
            if after_context and after_context[0].isupper():
                # Could be a new sentence
                return '. '
            # Check for conjunctive adverbs that suggest semicolon
            conjunctive_adverbs = ['however', 'therefore', 'moreover', 'furthermore',
                                   'nevertheless', 'consequently', 'thus', 'hence']
            after_lower = after_context.lower()
            if any(after_lower.startswith(adv) for adv in conjunctive_adverbs):
                return '; '
            # Otherwise semicolon for independent clauses
            return '; '

        # Check if it's a list or series
        if ',' in before_context[-20:] or ',' in after_context[:20]:
            return ', '

        # Check for parenthetical or explanatory content
        # Usually lowercase after em-dash for parenthetical
        if after_context and after_context[0].islower():
            return ', '

        # Check if after content is short (might be an aside)
        if len(after_context) < 30:
            return ', '

        # Default: Use comma for general separation
        return ', '

    def _clean_whitespace(self, content: str) -> str:
        """Clean up multiple spaces and normalize whitespace."""
        # Replace multiple spaces with single space
        content = re.sub(r' {2,}', ' ', content)

        # Fix spacing around punctuation
        content = re.sub(r'\s+([.,;:!?])', r'\1', content)  # Remove space before punctuation
        content = re.sub(r'([.,;:!?])([A-Za-z])', r'\1 \2', content)  # Add space after punctuation if missing

        # Clean up line breaks
        content = re.sub(r'\n{3,}', '\n\n', content)  # Max 2 consecutive newlines

        return content


def scrub_content(content: str, verbose: bool = False) -> str:
    """
    Convenience function to scrub content.

    Args:
        content: The text to scrub
        verbose: If True, print statistics

    Returns:
        Cleaned content
    """
    scrubber = ContentScrubber()
    cleaned_content, stats = scrubber.scrub(content)

    if verbose:
        print(f"Content Scrubbing Complete:")
        print(f"  - Unicode watermarks removed: {stats['unicode_removed']}")
        print(f"  - Format-control chars removed: {stats['format_control_removed']}")
        print(f"  - Em-dashes replaced: {stats['emdashes_replaced']}")

    return cleaned_content


def scrub_file(file_path: str, output_path: str = None, verbose: bool = False) -> None:
    """
    Scrub a file and optionally save to a new location.

    Args:
        file_path: Path to file to scrub
        output_path: Path to save cleaned content (if None, overwrites original)
        verbose: If True, print statistics
    """
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Scrub content
    cleaned_content = scrub_content(content, verbose=verbose)

    # Write file
    output = output_path or file_path
    with open(output, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    if verbose:
        print(f"Scrubbed content saved to: {output}")


if __name__ == '__main__':
    # Test the scrubber
    test_content = """
    This is a test\u200Bcontent with invisible\uFEFF characters.

    Here's a sentence with an em-dash—it should be replaced appropriately.

    And another one—this time with\u200C more context—to test the logic.

    Final test: some content\u2060 with word\u00AD joiners and soft\u202F hyphens.
    """

    print("Original content (with invisible chars):")
    print(repr(test_content))
    print("\n" + "="*60 + "\n")

    cleaned = scrub_content(test_content, verbose=True)

    print("\n" + "="*60 + "\n")
    print("Cleaned content:")
    print(cleaned)
