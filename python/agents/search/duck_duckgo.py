"""DuckDuckGo search provider.

S: Single responsibility -- DuckDuckGo search.
O: New provider = new file. This file never changes.
L: Swappable with any SearchInterface implementation.
"""

import logging

from ddgs import DDGS

from agents.base import SearchInterface, SearchResult

logger = logging.getLogger("search.ddg")
DDG_MAX_RESULTS = 20

client = None


def get_client():
    global client
    if client is None:
        client = DDGS()
    return client


def ddg_search(query: str, max_results: int = DDG_MAX_RESULTS) -> list[SearchResult]:
    """DuckDuckGo search. Free, no API key needed."""
    try:
        c = get_client()
        raw = list(c.text(query, max_results=max_results))
        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("href", ""),
                source="duckduckgo",
                metadata={"snippet": item.get("body", "")[:300]},
            )
            for item in raw
        ]
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed: {e}")
        return []


class DuckDuckGoSummarizer(SearchInterface):
    """DuckDuckGo search. Used for trend summaries."""

    def search(self, query: str, max_results: int = DDG_MAX_RESULTS) -> list[SearchResult]:
        return ddg_search(query, max_results)
