"""YouTube scraper -- Exa search. No API key needed beyond Exa.

S: Single responsibility -- searches YouTube. That's it.
O: New source = new scraper class. This file never changes.
L: Swappable with any SearchInterface implementation.
"""

import logging

from agents.base import SearchInterface, SearchResult
from agents.search.web import exa_search

logger = logging.getLogger("search.youtube")
YOUTUBE_MAX_RESULTS = 15


class YouTubeScraper(SearchInterface):
    """Searches YouTube via Exa."""

    def search(self, query: str, max_results: int = YOUTUBE_MAX_RESULTS) -> list[SearchResult]:
        try:
            results = exa_search(f"site:youtube.com {query}", max_results)
            for r in results:
                r.source = "youtube"
                if " - YouTube" in r.title:
                    r.title = r.title.split(" - YouTube")[0].strip()
            return results
        except Exception as e:
            logger.warning(f"YouTube search failed: {e}")
            return []
