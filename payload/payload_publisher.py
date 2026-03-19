"""
Payload CMS Publisher for Freaking Nomads
=========================================
Publishes SEO Machine draft articles to the Freaking Nomads Payload CMS
via the REST API. Converts Markdown content to Payload Lexical rich text format.

TODO: Configure these environment variables in data_sources/config/.env:
    PAYLOAD_API_URL    - e.g. https://freakingnomads.com/api
    PAYLOAD_API_TOKEN  - API key from Payload admin panel
    PAYLOAD_COLLECTION - Collection name for posts (e.g. "posts")

Usage:
    python payload/payload_publisher.py drafts/my-article.md
    python payload/payload_publisher.py drafts/my-article.md --dry-run
    python payload/payload_publisher.py --test
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install requests python-dotenv")
    sys.exit(1)

# Load environment variables
env_path = Path(__file__).parent.parent / "data_sources" / "config" / ".env"
load_dotenv(dotenv_path=env_path)

PAYLOAD_API_URL = os.getenv("PAYLOAD_API_URL", "").rstrip("/")
PAYLOAD_API_TOKEN = os.getenv("PAYLOAD_API_TOKEN", "")
PAYLOAD_COLLECTION = os.getenv("PAYLOAD_COLLECTION", "posts")


# ---------------------------------------------------------------------------
# Markdown → Payload Lexical converter
# ---------------------------------------------------------------------------

def md_to_lexical(markdown: str) -> dict:
    """
    Converts Markdown text to Payload CMS Lexical rich text format.

    Lexical stores content as a tree of nodes. This converter handles:
    - Headings (H1–H4)
    - Paragraphs
    - Bold (**text**) and italic (*text*) inline formatting
    - Ordered and unordered lists
    - Horizontal rules
    - Plain text fallback for unsupported elements

    Returns a Lexical root node dict compatible with Payload CMS.
    """
    lines = markdown.split("\n")
    children = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines between blocks
        if not line.strip():
            i += 1
            continue

        # Headings
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            tag = f"h{level}"
            children.append({
                "type": "heading",
                "tag": tag,
                "children": _parse_inline(text),
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "version": 1,
            })
            i += 1
            continue

        # Unordered list
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                item_text = re.sub(r"^[-*]\s+", "", lines[i])
                items.append({
                    "type": "listitem",
                    "children": _parse_inline(item_text),
                    "direction": "ltr",
                    "format": "",
                    "indent": 0,
                    "value": len(items) + 1,
                    "version": 1,
                })
                i += 1
            children.append({
                "type": "list",
                "listType": "bullet",
                "start": 1,
                "tag": "ul",
                "children": items,
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "version": 1,
            })
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                item_text = re.sub(r"^\d+\.\s+", "", lines[i])
                items.append({
                    "type": "listitem",
                    "children": _parse_inline(item_text),
                    "direction": "ltr",
                    "format": "",
                    "indent": 0,
                    "value": len(items) + 1,
                    "version": 1,
                })
                i += 1
            children.append({
                "type": "list",
                "listType": "number",
                "start": 1,
                "tag": "ol",
                "children": items,
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "version": 1,
            })
            continue

        # Horizontal rule
        if re.match(r"^---+$", line.strip()):
            children.append({
                "type": "horizontalrule",
                "version": 1,
            })
            i += 1
            continue

        # Paragraph (default)
        # Collect consecutive non-empty, non-special lines
        para_lines = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^#{1,4}\s", lines[i]) and not re.match(r"^[-*\d]", lines[i]) and not re.match(r"^---+$", lines[i].strip()):
            para_lines.append(lines[i])
            i += 1

        if para_lines:
            text = " ".join(para_lines)
            children.append({
                "type": "paragraph",
                "children": _parse_inline(text),
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "version": 1,
            })

    return {
        "root": {
            "type": "root",
            "children": children,
            "direction": "ltr",
            "format": "",
            "indent": 0,
            "version": 1,
        }
    }


def _parse_inline(text: str) -> list:
    """
    Parses inline Markdown formatting into Lexical text nodes.
    Handles: **bold**, *italic*, ***bold+italic***, plain text.
    """
    nodes = []
    # Pattern: captures bold+italic, bold, italic, and plain text
    pattern = re.compile(r"(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|([^*]+))")

    for match in pattern.finditer(text):
        if match.group(2):  # bold + italic
            nodes.append(_text_node(match.group(2), bold=True, italic=True))
        elif match.group(3):  # bold
            nodes.append(_text_node(match.group(3), bold=True))
        elif match.group(4):  # italic
            nodes.append(_text_node(match.group(4), italic=True))
        elif match.group(5):  # plain
            plain = match.group(5)
            if plain:
                nodes.append(_text_node(plain))

    if not nodes:
        nodes.append(_text_node(text))

    return nodes


def _text_node(text: str, bold: bool = False, italic: bool = False) -> dict:
    """Creates a Lexical text node."""
    # Lexical format bitmask: 1=bold, 2=italic, 3=bold+italic
    fmt = 0
    if bold:
        fmt |= 1
    if italic:
        fmt |= 2
    return {
        "type": "text",
        "text": text,
        "format": fmt,
        "detail": 0,
        "mode": "normal",
        "style": "",
        "version": 1,
    }


# ---------------------------------------------------------------------------
# Draft parser
# ---------------------------------------------------------------------------

def parse_draft(file_path: str) -> dict:
    """
    Parses a Freaking Nomads draft Markdown file.

    Extracts frontmatter fields (Title, Meta Title, Meta Description,
    Target Keyword, URL Slug, Author, Category, Tags) and body content.

    Returns a dict with all extracted fields.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Draft file not found: {file_path}")

    raw = path.read_text(encoding="utf-8")

    # Extract frontmatter fields (bold **Field**: value format used by FN)
    def extract_field(field_name: str) -> Optional[str]:
        pattern = re.compile(rf"^\*\*{field_name}\*\*:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
        match = pattern.search(raw)
        return match.group(1).strip() if match else None

    # Extract H1 as title fallback
    h1_match = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
    h1_title = h1_match.group(1).strip() if h1_match else None

    title = extract_field("Title") or h1_title or path.stem
    meta_title = extract_field("Meta Title") or title
    meta_description = extract_field("Meta Description") or ""
    target_keyword = extract_field("Target Keyword") or ""
    slug = extract_field("URL Slug") or _title_to_slug(title)
    author = extract_field("Author") or "Freaking Nomads"
    category = extract_field("Category") or ""
    tags_raw = extract_field("Tags") or ""
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    # Strip frontmatter lines and H1 from body content
    body = raw
    # Remove **Field**: value lines
    body = re.sub(r"^\*\*[^*]+\*\*:.+\n?", "", body, flags=re.MULTILINE)
    # Remove H1
    body = re.sub(r"^#\s+.+\n?", "", body, flags=re.MULTILINE)
    body = body.strip()

    return {
        "title": title,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "target_keyword": target_keyword,
        "slug": slug,
        "author": author,
        "category": category,
        "tags": tags,
        "content": body,
        "source_file": str(path),
    }


def _title_to_slug(title: str) -> str:
    """Converts a title to a URL slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug


# ---------------------------------------------------------------------------
# Payload CMS API client
# ---------------------------------------------------------------------------

def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {PAYLOAD_API_TOKEN}",
        "Content-Type": "application/json",
    }


def create_draft(draft: dict, dry_run: bool = False) -> dict:
    """
    Creates a draft post in Payload CMS via REST API.

    TODO: Adjust the payload structure to match your Payload CMS schema.
    Field names like 'meta', 'content', 'categories', 'tags' may differ.
    Check your Payload collection config for exact field names.
    """
    lexical_content = md_to_lexical(draft["content"])

    payload_data = {
        "title": draft["title"],
        "slug": draft["slug"],
        "status": "draft",
        "content": lexical_content,  # TODO: verify field name in your Payload schema
        "meta": {                     # TODO: verify 'meta' group field name
            "title": draft["meta_title"],
            "description": draft["meta_description"],
        },
        # TODO: Author may need to be a relation (ID) rather than a string
        # "author": draft["author"],
    }

    if draft["category"]:
        # TODO: Categories are typically relations in Payload — you may need to
        # look up the category ID first or create it if it doesn't exist
        payload_data["categories"] = [{"name": draft["category"]}]

    if draft["tags"]:
        # TODO: Tags structure depends on your Payload schema
        payload_data["tags"] = draft["tags"]

    if dry_run:
        print("\n[DRY RUN] Would POST to Payload CMS:")
        print(json.dumps(payload_data, indent=2, ensure_ascii=False))
        return {"dry_run": True, "data": payload_data}

    url = f"{PAYLOAD_API_URL}/{PAYLOAD_COLLECTION}"
    response = requests.post(url, headers=get_headers(), json=payload_data, timeout=30)

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Payload API error {response.status_code}: {response.text}"
        )

    return response.json()


def test_connection() -> bool:
    """Tests the Payload CMS API connection."""
    if not PAYLOAD_API_URL:
        print("ERROR: PAYLOAD_API_URL not set in .env")
        return False
    if not PAYLOAD_API_TOKEN:
        print("ERROR: PAYLOAD_API_TOKEN not set in .env")
        return False

    url = f"{PAYLOAD_API_URL}/{PAYLOAD_COLLECTION}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        if response.status_code == 200:
            print(f"✓ Connected to Payload CMS at {PAYLOAD_API_URL}")
            print(f"✓ Collection '{PAYLOAD_COLLECTION}' accessible")
            return True
        else:
            print(f"✗ Connection failed: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Publish a Freaking Nomads draft to Payload CMS"
    )
    parser.add_argument("file", nargs="?", help="Path to the draft Markdown file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    parser.add_argument("--test", action="store_true", help="Test API connection and exit")
    args = parser.parse_args()

    if args.test:
        success = test_connection()
        sys.exit(0 if success else 1)

    if not args.file:
        parser.print_help()
        sys.exit(1)

    # Validate config
    if not PAYLOAD_API_URL:
        print("ERROR: PAYLOAD_API_URL not set. Add it to data_sources/config/.env")
        print("  PAYLOAD_API_URL=https://freakingnomads.com/api")
        sys.exit(1)

    if not PAYLOAD_API_TOKEN and not args.dry_run:
        print("ERROR: PAYLOAD_API_TOKEN not set. Add it to data_sources/config/.env")
        sys.exit(1)

    # Parse draft
    try:
        draft = parse_draft(args.file)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Display extracted metadata
    print("\n── Draft Metadata ──────────────────────────────")
    print(f"  Title:       {draft['title']}")
    print(f"  Meta Title:  {draft['meta_title']}")
    print(f"  Meta Desc:   {draft['meta_description'][:80]}{'...' if len(draft['meta_description']) > 80 else ''}")
    print(f"  Keyword:     {draft['target_keyword']}")
    print(f"  Slug:        {draft['slug']}")
    print(f"  Author:      {draft['author']}")
    print(f"  Category:    {draft['category']}")
    print(f"  Tags:        {', '.join(draft['tags'])}")
    print(f"  Content:     {len(draft['content'].split())} words")
    print("────────────────────────────────────────────────\n")

    # Pre-publish checks
    warnings = []
    if len(draft["meta_description"]) > 155:
        warnings.append(f"Meta description is {len(draft['meta_description'])} chars (max 155)")
    if not draft["target_keyword"]:
        warnings.append("No target keyword set")
    if draft["content"].count("freakingnomads.com") < 3:
        warnings.append("Fewer than 3 internal links detected — check minimum requirement")

    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")
        print()

    # Publish
    try:
        result = create_draft(draft, dry_run=args.dry_run)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if not args.dry_run:
        doc_id = result.get("id") or result.get("doc", {}).get("id", "unknown")
        admin_url = f"{PAYLOAD_API_URL.replace('/api', '')}/admin/collections/{PAYLOAD_COLLECTION}/{doc_id}"
        print(f"✓ Draft created successfully!")
        print(f"  Edit URL: {admin_url}")
        print("\nNext steps:")
        print("  1. Review the draft in Payload admin")
        print("  2. Add any images (not uploaded automatically)")
        print("  3. Verify all internal links resolve correctly")
        print("  4. Set status to 'Published' when ready")


if __name__ == "__main__":
    main()
