"""
WordPress Publisher Module

Publishes draft articles to WordPress as draft posts via the REST API.
Supports Yoast SEO meta fields (title, description, focus keyphrase).
"""

import os
import re
import requests
from typing import Dict, Optional, List, Tuple
from pathlib import Path


class WordPressPublisher:
    """WordPress REST API client for publishing drafts"""

    def __init__(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        app_password: Optional[str] = None
    ):
        """
        Initialize WordPress publisher

        Args:
            url: WordPress site URL (defaults to env var WORDPRESS_URL)
            username: WordPress username (defaults to env var WORDPRESS_USERNAME)
            app_password: Application password (defaults to env var WORDPRESS_APP_PASSWORD)
        """
        self.url = (url or os.getenv('WORDPRESS_URL', '')).rstrip('/')
        self.username = username or os.getenv('WORDPRESS_USERNAME')
        self.app_password = app_password or os.getenv('WORDPRESS_APP_PASSWORD')

        if not self.url:
            raise ValueError("WORDPRESS_URL must be set")
        if not self.username or not self.app_password:
            raise ValueError("WORDPRESS_USERNAME and WORDPRESS_APP_PASSWORD must be set")

        self.api_base = f"{self.url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.auth = (self.username, self.app_password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'SEOMachine/1.0 (WordPress Content Publisher)'
        })

        # Cache for categories and tags
        self._categories_cache: Optional[Dict[str, int]] = None
        self._tags_cache: Optional[Dict[str, int]] = None

    def parse_draft_file(self, file_path: str) -> Dict:
        """
        Parse a markdown draft file and extract metadata and content

        Args:
            file_path: Path to the markdown file

        Returns:
            Dict with keys: title, meta_title, meta_description, target_keyword,
                           secondary_keywords, slug, category, tags, content
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Draft file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract H1 title
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = h1_match.group(1).strip() if h1_match else ''

        # Extract metadata fields (format: **Field Name**: Value)
        def extract_field(field_name: str) -> str:
            pattern = rf'\*\*{field_name}\*\*:\s*(.+?)(?:\n|$)'
            match = re.search(pattern, content, re.IGNORECASE)
            return match.group(1).strip() if match else ''

        meta_title = extract_field('Meta Title')
        meta_description = extract_field('Meta Description')
        target_keyword = extract_field('Target Keyword')
        secondary_keywords = extract_field('Secondary Keywords')
        category = extract_field('Category')
        tags = extract_field('Tags')

        # Extract URL slug - handle both formats
        slug = ''
        slug_match = re.search(r'\*\*URL Slug\*\*:\s*/?(?:blog/)?([^\s/]+)/?', content, re.IGNORECASE)
        if slug_match:
            slug = slug_match.group(1).strip()
        else:
            # Generate from title if not specified
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[\s_]+', '-', slug)

        # Remove metadata section from content for body
        # Content starts after the metadata block (after the first ---)
        body_content = content

        # Remove the H1 title
        body_content = re.sub(r'^#\s+.+\n', '', body_content, count=1)

        # Remove metadata lines
        metadata_patterns = [
            r'\*\*Meta Title\*\*:.+\n?',
            r'\*\*Meta Description\*\*:.+\n?',
            r'\*\*Target Keyword\*\*:.+\n?',
            r'\*\*Secondary Keywords\*\*:.+\n?',
            r'\*\*URL Slug\*\*:.+\n?',
            r'\*\*Category\*\*:.+\n?',
            r'\*\*Tags\*\*:.+\n?',
            r'\*\*Internal Links\*\*:.+\n?',
            r'\*\*External Links\*\*:.+\n?',
            r'\*\*Word Count\*\*:.+\n?',
        ]
        for pattern in metadata_patterns:
            body_content = re.sub(pattern, '', body_content, flags=re.IGNORECASE)

        # Remove leading/trailing horizontal rules and whitespace
        body_content = re.sub(r'^[\s\-]*\n', '', body_content)
        body_content = body_content.strip()

        return {
            'title': title,
            'meta_title': meta_title or title,
            'meta_description': meta_description,
            'target_keyword': target_keyword,
            'secondary_keywords': secondary_keywords,
            'slug': slug,
            'category': category,
            'tags': tags,
            'content': body_content
        }

    def markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown to HTML for WordPress

        Args:
            markdown_content: Markdown formatted content

        Returns:
            HTML formatted content
        """
        try:
            import markdown
            md = markdown.Markdown(extensions=['extra', 'nl2br', 'sane_lists'])
            return md.convert(markdown_content)
        except ImportError:
            # Fallback: basic markdown conversion
            html = markdown_content

            # Convert headers
            html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
            html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
            html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

            # Convert bold and italic
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

            # Convert links
            html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

            # Convert unordered lists
            html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

            # Wrap paragraphs
            paragraphs = html.split('\n\n')
            wrapped = []
            for p in paragraphs:
                p = p.strip()
                if p and not p.startswith('<'):
                    wrapped.append(f'<p>{p}</p>')
                else:
                    wrapped.append(p)
            html = '\n\n'.join(wrapped)

            return html

    def get_categories(self) -> Dict[str, int]:
        """Get all categories as name->ID mapping"""
        if self._categories_cache is not None:
            return self._categories_cache

        categories = {}
        page = 1
        while True:
            response = self.session.get(
                f"{self.api_base}/categories",
                params={'per_page': 100, 'page': page}
            )
            response.raise_for_status()
            items = response.json()
            if not items:
                break
            for cat in items:
                categories[cat['name'].lower()] = cat['id']
            page += 1

        self._categories_cache = categories
        return categories

    def get_tags(self) -> Dict[str, int]:
        """Get all tags as name->ID mapping"""
        if self._tags_cache is not None:
            return self._tags_cache

        tags = {}
        page = 1
        while True:
            response = self.session.get(
                f"{self.api_base}/tags",
                params={'per_page': 100, 'page': page}
            )
            response.raise_for_status()
            items = response.json()
            if not items:
                break
            for tag in items:
                tags[tag['name'].lower()] = tag['id']
            page += 1

        self._tags_cache = tags
        return tags

    def get_or_create_category(self, name: str) -> int:
        """Get category ID, creating if it doesn't exist"""
        categories = self.get_categories()
        name_lower = name.lower().strip()

        if name_lower in categories:
            return categories[name_lower]

        # Create new category
        response = self.session.post(
            f"{self.api_base}/categories",
            json={'name': name.strip()}
        )
        response.raise_for_status()
        new_cat = response.json()
        self._categories_cache[name_lower] = new_cat['id']
        return new_cat['id']

    def get_or_create_tag(self, name: str) -> int:
        """Get tag ID, creating if it doesn't exist"""
        tags = self.get_tags()
        name_lower = name.lower().strip()

        if name_lower in tags:
            return tags[name_lower]

        # Create new tag
        response = self.session.post(
            f"{self.api_base}/tags",
            json={'name': name.strip()}
        )
        response.raise_for_status()
        new_tag = response.json()
        self._tags_cache[name_lower] = new_tag['id']
        return new_tag['id']

    def create_draft(
        self,
        title: str,
        content: str,
        slug: str,
        excerpt: str = '',
        category_ids: Optional[List[int]] = None,
        tag_ids: Optional[List[int]] = None,
        post_type: str = 'posts'
    ) -> Dict:
        """
        Create a WordPress draft post, page, or custom post type

        Args:
            title: Post title
            content: HTML content
            slug: URL slug
            excerpt: Post excerpt
            category_ids: List of category IDs (posts only)
            tag_ids: List of tag IDs (posts only)
            post_type: WordPress post type endpoint ('posts', 'pages', or custom type)

        Returns:
            WordPress post response with id, link, etc.
        """
        post_data = {
            'title': title,
            'content': content,
            'slug': slug,
            'status': 'draft',
            'excerpt': excerpt
        }

        # Categories and tags only apply to posts
        if post_type == 'posts':
            if category_ids:
                post_data['categories'] = category_ids
            if tag_ids:
                post_data['tags'] = tag_ids

        response = self.session.post(
            f"{self.api_base}/{post_type}",
            json=post_data
        )
        response.raise_for_status()
        return response.json()

    def set_yoast_meta(
        self,
        post_id: int,
        meta_title: str,
        meta_description: str,
        focus_keyphrase: str,
        post_type: str = 'posts'
    ) -> Dict:
        """
        Set Yoast SEO meta fields on a post, page, or custom post type

        Requires the SEO Machine Yoast REST plugin to be installed:
        wp-content/mu-plugins/seo-machine-yoast-rest.php

        Args:
            post_id: WordPress post ID
            meta_title: SEO title
            meta_description: Meta description
            focus_keyphrase: Focus keyphrase (target keyword)
            post_type: WordPress post type endpoint ('posts', 'pages', or custom type)

        Returns:
            Updated post response
        """
        # Use the yoast_seo field provided by our mu-plugin
        yoast_data = {
            'yoast_seo': {
                'seo_title': meta_title,
                'meta_description': meta_description,
                'focus_keyphrase': focus_keyphrase
            }
        }

        response = self.session.post(
            f"{self.api_base}/{post_type}/{post_id}",
            json=yoast_data
        )
        response.raise_for_status()
        return response.json()

    def publish_draft(self, file_path: str, post_type: str = 'post') -> Dict:
        """
        Publish a draft file to WordPress as a post, page, or custom post type

        Args:
            file_path: Path to the markdown draft file
            post_type: Content type - 'post', 'page', or custom post type (e.g., 'compare')

        Returns:
            Dict with post_id, edit_url, view_url, and status information
        """
        # Map friendly names to REST API endpoints
        type_endpoints = {
            'post': 'posts',
            'posts': 'posts',
            'page': 'pages',
            'pages': 'pages',
        }
        # Use the mapping, or assume custom post types use plural form
        api_endpoint = type_endpoints.get(post_type.lower(), post_type.lower())

        # Parse the draft file
        draft = self.parse_draft_file(file_path)

        # Convert content to HTML
        html_content = self.markdown_to_html(draft['content'])
        word_count = len(draft['content'].split())

        # Process categories (only for posts)
        category_ids = []
        if api_endpoint == 'posts' and draft['category']:
            cat_names = [c.strip() for c in draft['category'].split(',')]
            for cat_name in cat_names:
                if cat_name:
                    category_ids.append(self.get_or_create_category(cat_name))

        # Process tags (only for posts)
        tag_ids = []
        if api_endpoint == 'posts' and draft['tags']:
            tag_names = [t.strip() for t in draft['tags'].split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag_ids.append(self.get_or_create_tag(tag_name))

        # Create the draft
        post = self.create_draft(
            title=draft['title'],
            content=html_content,
            slug=draft['slug'],
            excerpt=draft['meta_description'],
            category_ids=category_ids if category_ids else None,
            tag_ids=tag_ids if tag_ids else None,
            post_type=api_endpoint
        )

        post_id = post['id']

        # Set Yoast meta
        if draft['meta_title'] or draft['meta_description'] or draft['target_keyword']:
            self.set_yoast_meta(
                post_id=post_id,
                meta_title=draft['meta_title'],
                meta_description=draft['meta_description'],
                focus_keyphrase=draft['target_keyword'],
                post_type=api_endpoint
            )

        # Build edit URL
        edit_url = f"{self.url}/wp-admin/post.php?post={post_id}&action=edit"

        return {
            'post_id': post_id,
            'post_type': post_type,
            'edit_url': edit_url,
            'view_url': post.get('link', ''),
            'title': draft['title'],
            'slug': draft['slug'],
            'word_count': word_count,
            'categories': [c.strip() for c in draft['category'].split(',')] if draft['category'] else [],
            'tags': [t.strip() for t in draft['tags'].split(',')] if draft['tags'] else [],
            'meta': {
                'title': draft['meta_title'],
                'description': draft['meta_description'],
                'focus_keyphrase': draft['target_keyword']
            }
        }


def main():
    """CLI entry point for testing"""
    import sys
    import argparse
    from dotenv import load_dotenv

    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)

    parser = argparse.ArgumentParser(description='Publish a draft to WordPress')
    parser.add_argument('file_path', help='Path to the markdown draft file')
    parser.add_argument(
        '--type', '-t',
        default='post',
        help='Content type: post, page, or custom post type (default: post)'
    )
    args = parser.parse_args()

    try:
        publisher = WordPressPublisher()
        result = publisher.publish_draft(args.file_path, post_type=args.type)

        type_label = result['post_type'].title()
        print(f"\n✓ Parsed draft file")
        print(f"✓ Converted {result['word_count']:,} words to HTML")
        print(f"✓ Created WordPress {type_label} draft (ID: {result['post_id']})")
        print(f"✓ Set Yoast meta (title, description, focus keyphrase)")

        if result['categories']:
            print(f"✓ Assigned categories: {', '.join(result['categories'])}")
        if result['tags']:
            print(f"✓ Assigned tags: {', '.join(result['tags'])}")

        print(f"\nDraft published to WordPress!")
        print(f"Edit URL: {result['edit_url']}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"WordPress API Error: {e}")
        print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
