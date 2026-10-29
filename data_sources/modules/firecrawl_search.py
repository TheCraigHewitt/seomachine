"""
Firecrawl Search Integration

Web search and content retrieval for SEO research via the Firecrawl API.
Complements DataForSEO SERP data with live search results that can include
the full page content (as markdown) of each result, for competitor content
analysis and content discovery.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class FirecrawlSearch:
    """Firecrawl web search client for content research and discovery"""

    # Integration tag sent with every Firecrawl request
    INTEGRATION = "_seomachine"

    # Valid content modes
    CONTENT_MODES = ["description", "markdown", "none"]

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Firecrawl search client

        Args:
            api_key: Firecrawl API key (defaults to FIRECRAWL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")

        if not self.api_key:
            raise ValueError(
                "FIRECRAWL_API_KEY must be set. Get your key from https://firecrawl.dev"
            )

        self.client = self._get_client()

    def _get_client(self):
        """Create and return a configured Firecrawl client"""
        from firecrawl import Firecrawl

        return Firecrawl(api_key=self.api_key)

    def search(
        self,
        query: str,
        num_results: int = 10,
        content_mode: str = "description",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        include_news: bool = False,
        time_filter: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search the web using Firecrawl

        Args:
            query: Search query
            num_results: Number of results to return (max 100)
            content_mode: 'description' (search snippet, default), 'markdown'
                (full page content of each result), or 'none'
            include_domains: Only include results from these domains
            exclude_domains: Exclude results from these domains
            include_news: Also search news sources
            time_filter: Time filter, e.g. 'qdr:w' (past week) or
                'cdr:1,cd_min:1/1/2025,cd_max:1/31/2025'
            location: Location for localized results (e.g. 'Germany')

        Returns:
            Dict with search results and metadata
        """
        search_kwargs = {
            "limit": min(num_results, 100),
            "integration": self.INTEGRATION,
        }

        if content_mode == "markdown":
            search_kwargs["scrape_options"] = {
                "formats": ["markdown"],
                "only_main_content": True,
            }

        # Add optional filters
        if include_domains:
            search_kwargs["include_domains"] = include_domains
        if exclude_domains:
            search_kwargs["exclude_domains"] = exclude_domains
        if include_news:
            search_kwargs["sources"] = ["web", "news"]
        if time_filter:
            search_kwargs["tbs"] = time_filter
        if location:
            search_kwargs["location"] = location

        response = self.client.search(query, **search_kwargs)
        return self._process_results(response, content_mode)

    def find_competitor_content(
        self,
        topic: str,
        competitor_domains: List[str],
        num_results: int = 10,
    ) -> Dict[str, Any]:
        """
        Find competitor content on a specific topic

        Args:
            topic: Topic or keyword to search for
            competitor_domains: List of competitor domains to search within
            num_results: Number of results to return

        Returns:
            Dict with competitor content analysis
        """
        results = self.search(
            query=topic,
            num_results=num_results,
            content_mode="description",
            include_domains=competitor_domains,
        )

        # Group by domain
        by_domain = {}
        for item in results.get("results", []):
            domain = self._extract_domain(item.get("url", ""))
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(item)

        return {
            "topic": topic,
            "competitor_domains": competitor_domains,
            "results_by_domain": by_domain,
            "total_results": len(results.get("results", [])),
        }

    def discover_content_ideas(
        self,
        seed_topic: str,
        num_results: int = 20,
        exclude_domains: Optional[List[str]] = None,
        days_back: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Discover content ideas and trending articles on a topic

        Args:
            seed_topic: Topic to explore
            num_results: Number of results to return
            exclude_domains: Domains to exclude (e.g. your own)
            days_back: Only include content published within this many days

        Returns:
            Dict with discovered content and ideas
        """
        time_filter = None
        if days_back:
            from datetime import timedelta
            start = datetime.now() - timedelta(days=days_back)
            time_filter = f"cdr:1,cd_min:{start.month}/{start.day}/{start.year}"

        results = self.search(
            query=seed_topic,
            num_results=num_results,
            content_mode="description",
            exclude_domains=exclude_domains,
            time_filter=time_filter,
        )

        return {
            "topic": seed_topic,
            "articles_found": len(results.get("results", [])),
            "results": results.get("results", []),
        }

    def _process_results(
        self, response, content_mode: str
    ) -> Dict[str, Any]:
        """Process Firecrawl search response into a standard dict format"""
        processed = []

        items = list(getattr(response, "web", None) or [])
        items += list(getattr(response, "news", None) or [])

        for result in items:
            # Results with scraped content are Documents: url/title live in metadata
            metadata = getattr(result, "metadata", None)
            url = getattr(result, "url", None) or (
                getattr(metadata, "url", None)
                or getattr(metadata, "source_url", None)
                if metadata else None
            )
            if not url:
                continue

            title = getattr(result, "title", None) or (
                getattr(metadata, "title", None) if metadata else None
            )
            entry = {
                "title": title or "No Title",
                "url": url,
            }

            # Extract content based on mode
            if content_mode == "markdown":
                entry["content"] = getattr(result, "markdown", "") or ""
            elif content_mode == "description":
                content = getattr(result, "description", None) or getattr(
                    result, "snippet", None
                )
                if content:
                    entry["content"] = content

            # Add metadata when available
            published_date = getattr(result, "date", None) or (
                getattr(metadata, "published_time", None) if metadata else None
            )
            if published_date:
                entry["published_date"] = published_date

            processed.append(entry)

        return {
            "results": processed,
            "total_results": len(processed),
        }

    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain from URL"""
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc.replace("www.", "")


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("data_sources/config/.env")

    firecrawl = FirecrawlSearch()

    print("Searching for podcast hosting content...")
    results = firecrawl.search(
        query="best podcast hosting platforms for beginners",
        num_results=5,
    )

    for result in results["results"]:
        print(f"\n{result['title']}")
        print(f"  {result['url']}")
        if result.get("content"):
            print(f"  {result['content'][:200]}...")

    print("\n\nDiscovering recent content ideas...")
    ideas = firecrawl.discover_content_ideas(
        seed_topic="podcast monetization strategies",
        num_results=5,
        days_back=30,
    )

    print(f"Found {ideas['articles_found']} recent articles")
    for article in ideas["results"]:
        print(f"  - {article['title']}")
