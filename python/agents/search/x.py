"""X (Twitter) scraper -- Exa search. No API key needed beyond Exa.

S: Single responsibility -- searches X. That's it.
O: New source = new scraper class. This file never changes.
L: Swappable with any SearchInterface implementation.
"""

import logging

from agents.base import SearchInterface, SearchResult
from agents.search.web import exa_search

logger = logging.getLogger("search.x")
X_MAX_RESULTS = 15


class XScraper(SearchInterface):
    """Searches X via Exa."""

    def search(self, query: str, max_results: int = X_MAX_RESULTS) -> list[SearchResult]:
        try:
            results = exa_search(f"(site:x.com OR site:twitter.com) {query}", max_results)
            for r in results:
                r.source = "x"
            return results
        except Exception as e:
            logger.warning(f"X search failed: {e}")
            return []
