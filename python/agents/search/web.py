"""Web search via Exa API. RSS feeds.

S: Single responsibility -- web search + RSS. Not YouTube. Not X.
O: New search provider = new function. This file never changes.
L: Swappable with any SearchInterface implementation.
"""

import os
from datetime import datetime
from typing import Any, Optional, cast

import feedparser
import requests

from agents.base import SearchInterface, SearchResult

EXA_API_KEY = os.getenv("EXA_API_KEY", "")
EXA_MAX_RESULTS = 15


def exa_search(query: str, max_results: int = EXA_MAX_RESULTS) -> list[SearchResult]:
    """Shared Exa search used by YouTube, X, and web scrapers."""
    if not EXA_API_KEY:
        return []

    resp = requests.post(
        "https://api.exa.ai/search",
        headers={
            "Authorization": f"Bearer {EXA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "query": query,
            "numResults": max_results,
            "contents": {"text": True, "highlights": True},
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    return [
        SearchResult(
            title=r.get("title", ""),
            url=r.get("url", ""),
            source="exa",
            published=r.get("publishedDate"),
            metadata={
                "snippet": (r.get("text", "") or "")[:300],
                "author": r.get("author", ""),
                "domain": r.get("domain", ""),
            },
        )
        for r in data.get("results", [])
    ]


class WebSummarizer(SearchInterface):
    """Searches via Exa. Used for IG/TT/LI/Threads trend summaries."""

    def search(self, query: str, max_results: int = EXA_MAX_RESULTS) -> list[SearchResult]:
        return exa_search(query, max_results)


class RSSReader(SearchInterface):
    """Reads RSS/Atom feeds for creator channels and tech blogs."""

    def __init__(self, feed_urls: Optional[list[str]] = None):
        self.feed_urls = feed_urls or []

    def search(self, query: str = "", max_results: int = 50) -> list[SearchResult]:
        results: list[SearchResult] = []
        for url in self.feed_urls:
            # feedparser is untyped; the typed surface is unreliable, so treat
            # the parsed feed as opaque and coerce fields defensively.
            feed = cast(Any, feedparser.parse(url))
            for entry in feed.entries[:10]:
                item = dict(entry)
                feed_meta = dict(feed.feed)
                results.append(
                    SearchResult(
                        title=str(item.get("title") or ""),
                        url=str(item.get("link") or ""),
                        source="rss",
                        published=self.parse_date(item.get("published_parsed")),
                        metadata={
                            "summary": str(item.get("summary") or "")[:300],
                            "feed_title": str(feed_meta.get("title") or ""),
                        },
                    )
                )
        return results

    def add_feed(self, url: str):
        self.feed_urls.append(url)

    @staticmethod
    def parse_date(struct_time) -> Optional[datetime]:
        if not struct_time:
            return None
        try:
            from calendar import timegm

            return datetime.utcfromtimestamp(timegm(struct_time))
        except (TypeError, ValueError):
            return None
