"""Opt-in web research through Parallel Unified MCP, without an SDK or API key."""

import json
import os
from typing import Any, Dict, Optional

import requests


class ParallelSearchError(RuntimeError):
    """Parallel transport, protocol, or tool failure. No provider fallback is made."""


class ParallelSearch:
    """Return Exa-style title/url/content results from MCP web_search excerpts.

    Constructing a client does not contact the network. Only search() does.
    Exa-specific filters and content modes are intentionally not emulated.
    """

    ENDPOINT = "https://mcp.parallel.ai/mcp"
    USER_AGENT = "seomachine/parallel-search"
    PROTOCOL_VERSION = "2025-03-26"

    def __init__(self, api_key: Optional[str] = None, *, enabled: bool = True,
                 offline: bool = False, timeout: float = 60):
        # None means use the environment; an explicitly empty key is an error.
        self.api_key = os.getenv("PARALLEL_API_KEY") if api_key is None else api_key
        if self.api_key is not None and not self.api_key.strip():
            raise ValueError("PARALLEL_API_KEY must be nonempty when supplied")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.enabled = enabled
        self.offline = offline
        self.timeout = timeout

    def search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Search for one research objective, returning URLs and excerpt passages.

        num_results is a local cap (1..10), not a promise of that many matches.
        Anonymous MCP uses the server's default Fast mode and result count.
        HTTP failures, including auth and rate limits, are raised without retry.
        """
        if (not self.enabled or self.offline or
                os.getenv("PARALLEL_SEARCH_ENABLED", "true").lower() == "false"):
            raise ParallelSearchError("Parallel search is disabled or offline")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a nonempty string")
        if type(num_results) is not int or not 1 <= num_results <= 10:
            raise ValueError("num_results must be an integer from 1 to 10")

        with requests.Session() as session:
            session.headers.update({
                "User-Agent": self.USER_AGENT,
                "Accept": "application/json, text/event-stream",
            })
            if self.api_key is not None:
                session.headers["Authorization"] = "Bearer " + self.api_key
            try:
                initialized = self._rpc(session, "initialize", 1, {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "seomachine", "version": "1.0"},
                })
                if initialized.get("protocolVersion") != self.PROTOCOL_VERSION:
                    raise ParallelSearchError("Unsupported MCP protocol version")
                session.headers["MCP-Protocol-Version"] = self.PROTOCOL_VERSION
                self._rpc(session, "notifications/initialized")
                tools = self._rpc(session, "tools/list", 2, {})
                if not any(t.get("name") == "web_search" for t in tools.get("tools", [])):
                    raise ParallelSearchError("Parallel web_search is unavailable")
                result = self._rpc(session, "tools/call", 3, {
                    "name": "web_search",
                    "arguments": {"objective": query, "search_queries": [query]},
                })
                return self._process_results(result, num_results)
            finally:
                if "Mcp-Session-Id" in session.headers:
                    # Teardown must not hide the original search/auth failure.
                    try:
                        with session.delete(self.ENDPOINT, timeout=self.timeout,
                                            allow_redirects=False):
                            pass
                    except requests.RequestException:
                        pass

    def _rpc(self, session, method, request_id=None, params=None):
        payload = {"jsonrpc": "2.0", "method": method}
        if request_id is not None:
            payload["id"] = request_id
        if params is not None:
            payload["params"] = params
        with session.post(self.ENDPOINT, json=payload, timeout=self.timeout,
                          allow_redirects=False) as response:
            # Do not follow redirects or forward credentials to another origin.
            if 300 <= response.status_code < 400:
                raise ParallelSearchError("Parallel MCP redirect refused")
            response.raise_for_status()
            if response.headers.get("Mcp-Session-Id"):
                session.headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
            if request_id is None:
                return None
            try:
                if "text/event-stream" in response.headers.get("Content-Type", ""):
                    messages = []
                    for event in response.content.decode("utf-8").replace("\r\n", "\n").split("\n\n"):
                        data = "\n".join(line[5:].lstrip(" ") for line in event.splitlines()
                                         if line.startswith("data:"))
                        if data:
                            messages.append(json.loads(data))
                else:
                    messages = [response.json()]
                for message in messages:
                    if message.get("id") == request_id:
                        if "error" in message:
                            raise ParallelSearchError("Parallel MCP RPC error")
                        if isinstance(message.get("result"), dict):
                            return message["result"]
            except (ValueError, AttributeError) as exc:
                raise ParallelSearchError("Malformed Parallel MCP response") from exc
            raise ParallelSearchError("Missing Parallel MCP response")

    @staticmethod
    def _process_results(result, limit):
        if result.get("isError"):
            raise ParallelSearchError("Parallel web_search failed")
        data = result.get("structuredContent")
        if data is None:
            # MCP also allows structured JSON serialized in text content blocks.
            try:
                data = json.loads("\n".join(block["text"] for block in result.get("content", [])
                                            if block.get("type") == "text"))
            except (ValueError, KeyError) as exc:
                raise ParallelSearchError("Malformed Parallel search content") from exc
        if not isinstance(data, dict) or not isinstance(data.get("results"), list):
            raise ParallelSearchError("Missing Parallel search results")
        processed = []
        for item in data["results"][:limit]:
            if (not isinstance(item, dict) or not isinstance(item.get("url"), str)
                    or not isinstance(item.get("excerpts"), list)
                    or not all(isinstance(text, str) for text in item["excerpts"])):
                raise ParallelSearchError("Malformed Parallel search result")
            entry = {"title": item.get("title") or "No Title", "url": item["url"],
                     "content": "\n".join(item["excerpts"])}
            if item.get("publish_date"):
                entry["published_date"] = item["publish_date"]
            processed.append(entry)
        return {"results": processed, "total_results": len(processed)}


if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv

    parser = argparse.ArgumentParser(description="Opt-in Parallel web research")
    parser.add_argument("query")
    parser.add_argument("--num-results", type=int, default=5)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    load_dotenv("data_sources/config/.env")
    print(json.dumps(ParallelSearch(offline=args.offline).search(
        args.query, num_results=args.num_results), indent=2, ensure_ascii=False))
