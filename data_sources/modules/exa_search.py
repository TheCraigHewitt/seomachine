"""
Exa AI Search Integration

AI-powered web search and content retrieval for SEO research.
Complements DataForSEO SERP data with semantic search, content discovery,
and competitor content analysis via the Exa API.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class ExaSearch:
    """Exa AI-powered search client for content research and discovery"""

    # Valid search types
    SEARCH_TYPES = ["auto", "neural", "fast", "instant"]

    # Valid content categories
    CATEGORIES = [
        "company",
        "research paper",
        "news",
        "personal site",
        "financial report",
        "people",
    ]

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Exa search client

        Args:
            api_key: Exa API key (defaults to EXA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("EXA_API_KEY")

        if not self.api_key:
            raise ValueError(
                "EXA_API_KEY must be set. Get your key from https://exa.ai"
            )

        self.client = self._get_client()

    def _get_client(self):
        """Create and return a configured Exa client"""
        from exa_py import Exa

        client = Exa(api_key=self.api_key)
        client.headers["x-exa-integration"] = "seomachine"
        return client

    def search(
        self,
        query: str,
        num_results: int = 10,
        search_type: str = "auto",
        content_mode: str = "highlights",
        category: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        include_text: Optional[List[str]] = None,
        exclude_text: Optional[List[str]] = None,
        start_published_date: Optional[str] = None,
        end_published_date: Optional[str] = None,
        user_location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search the web using Exa's AI-powered search

        Args:
            query: Search query (works best as a natural-language statement)
            num_results: Number of results to return (max 100)
            search_type: 'auto' (default), 'neural', 'fast', or 'instant'
            content_mode: 'highlights', 'text', 'summary', or 'none'
            category: Filter by category (e.g. 'news', 'company', 'research paper')
            include_domains: Only include results from these domains
            exclude_domains: Exclude results from these domains
            include_text: Strings that must appear in page text
            exclude_text: Strings to exclude from results
            start_published_date: ISO 8601 date; results published after this
            end_published_date: ISO 8601 date; results published before this
            user_location: Two-letter ISO country code for localized results

        Returns:
            Dict with search results and metadata
        """
        search_kwargs = {
            "query": query,
            "num_results": min(num_results, 100),
            "type": search_type,
        }

        # Add content retrieval
        contents = self._build_contents(content_mode)
        if contents is not None:
            search_kwargs["contents"] = contents

        # Add optional filters
        if category:
            search_kwargs["category"] = category
        if include_domains:
            search_kwargs["include_domains"] = include_domains
        if exclude_domains:
            search_kwargs["exclude_domains"] = exclude_domains
        if include_text:
            search_kwargs["include_text"] = include_text
        if exclude_text:
            search_kwargs["exclude_text"] = exclude_text
        if start_published_date:
            search_kwargs["start_published_date"] = start_published_date
        if end_published_date:
            search_kwargs["end_published_date"] = end_published_date
        if user_location:
            search_kwargs["user_location"] = user_location

        response = self.client.search(**search_kwargs)
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
            num_results: Number of results per competitor

        Returns:
            Dict with competitor content analysis
        """
        results = self.search(
            query=topic,
            num_results=num_results,
            content_mode="highlights",
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
        start_date = None
        if days_back:
            from datetime import timedelta
            start_date = (datetime.now() - timedelta(days=days_back)).strftime(
                "%Y-%m-%dT00:00:00.000Z"
            )

        results = self.search(
            query=seed_topic,
            num_results=num_results,
            content_mode="highlights",
            exclude_domains=exclude_domains,
            start_published_date=start_date,
        )

        return {
            "topic": seed_topic,
            "articles_found": len(results.get("results", [])),
            "results": results.get("results", []),
        }

    def find_similar_content(
        self,
        url: str,
        num_results: int = 10,
        exclude_domains: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Find content similar to a given URL

        Args:
            url: URL to find similar content for
            num_results: Number of similar results to return
            exclude_domains: Domains to exclude from results

        Returns:
            Dict with similar content results
        """
        find_kwargs = {
            "url": url,
            "num_results": min(num_results, 100),
            "contents": {"highlights": {"max_characters": 4000}},
        }

        if exclude_domains:
            find_kwargs["exclude_domains"] = exclude_domains

        response = self.client.find_similar(**find_kwargs)
        return self._process_results(response, "highlights")

    def research_topic(
        self,
        topic: str,
        num_results: int = 10,
        include_news: bool = True,
        include_research: bool = False,
    ) -> Dict[str, Any]:
        """
        Comprehensive topic research combining multiple searches

        Args:
            topic: Topic to research
            num_results: Results per search
            include_news: Include recent news articles
            include_research: Include research papers

        Returns:
            Dict with categorized research results
        """
        research = {
            "topic": topic,
            "researched_at": datetime.now().isoformat(),
            "general": [],
            "news": [],
            "research_papers": [],
        }

        # General search
        general = self.search(
            query=topic,
            num_results=num_results,
            content_mode="highlights",
        )
        research["general"] = general.get("results", [])

        # News search
        if include_news:
            news = self.search(
                query=topic,
                num_results=num_results,
                content_mode="highlights",
                category="news",
            )
            research["news"] = news.get("results", [])

        # Research papers
        if include_research:
            papers = self.search(
                query=topic,
                num_results=num_results,
                content_mode="summary",
                category="research paper",
            )
            research["research_papers"] = papers.get("results", [])

        return research

    def _build_contents(self, content_mode: str) -> Optional[Dict[str, Any]]:
        """Build the contents parameter for the Exa API"""
        if content_mode == "highlights":
            return {"highlights": {"max_characters": 4000}}
        elif content_mode == "text":
            return {"text": {"max_characters": 10000}}
        elif content_mode == "summary":
            return {"summary": True}
        elif content_mode == "none":
            return None
        # Default to highlights
        return {"highlights": {"max_characters": 4000}}

    def _process_results(
        self, response, content_mode: str
    ) -> Dict[str, Any]:
        """Process Exa API response into a standard dict format"""
        processed = []

        for result in response.results:
            entry = {
                "title": getattr(result, "title", "No Title") or "No Title",
                "url": getattr(result, "url", "") or "",
            }

            # Extract content based on mode
            if content_mode == "highlights":
                highlights = getattr(result, "highlights", None)
                if highlights:
                    entry["content"] = "\n".join(highlights)
            elif content_mode == "text":
                entry["content"] = getattr(result, "text", "") or ""
            elif content_mode == "summary":
                entry["content"] = getattr(result, "summary", "") or ""

            # Add metadata when available
            published_date = getattr(result, "published_date", None)
            if published_date:
                entry["published_date"] = published_date

            author = getattr(result, "author", None)
            if author:
                entry["author"] = author

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

    exa = ExaSearch()

    print("Searching for podcast hosting content...")
    results = exa.search(
        query="best podcast hosting platforms for beginners",
        num_results=5,
        content_mode="highlights",
    )

    for result in results["results"]:
        print(f"\n{result['title']}")
        print(f"  {result['url']}")
        if result.get("content"):
            print(f"  {result['content'][:200]}...")

    print("\n\nDiscovering recent content ideas...")
    ideas = exa.discover_content_ideas(
        seed_topic="podcast monetization strategies",
        num_results=5,
        days_back=30,
    )

    print(f"Found {ideas['articles_found']} recent articles")
    for article in ideas["results"]:
        print(f"  - {article['title']}")
