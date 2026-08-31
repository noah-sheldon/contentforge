"""Abstract interfaces for all agent components.

SOLID:
  - I: Segregated interfaces — SearchInterface doesn't know about publishing
  - D: Strategist depends on SearchInterface, not concrete scrapers
  - O: New platform = new class implementing SearchInterface
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ─── Models ────────────────────────────────────────────────────────────


@dataclass
class SearchResult:
    """Normalised result from any search source."""

    title: str
    url: str
    source: str  # "youtube" | "x" | "duckduckgo" | "rss"
    published: Optional[datetime] = None
    engagement: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Topic:
    """A proposed content topic with platform-fit scores."""

    title: str
    hook: str
    why_now: str
    predicted_fit: dict[str, str]  # {"linkedin": "high", "x": "med", ...}
    recommended_track: str  # "text_gen" | "short_form" | "both"


# ─── Decorators ───────────────────────────────────────────────────────


def retry_on_failure(max_retries: int = 3, backoff: float = 2.0):
    """DRY: Single retry decorator used by every scraper/publisher."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error: Optional[Exception] = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_error = e
                    wait = backoff**attempt
                    logger.warning(
                        "%s attempt %d/%d failed: %s. Retrying in %.1fs...",
                        func.__name__,
                        attempt + 1,
                        max_retries,
                        e,
                        wait,
                    )
                    time.sleep(wait)
            raise RuntimeError(
                f"{func.__name__} failed after {max_retries} retries"
            ) from last_error

        return wrapper

    return decorator


# ─── Interfaces ───────────────────────────────────────────────────────


class SearchInterface(ABC):
    """All scrapers implement this. Strategist depends on this, not concretions."""

    @abstractmethod
    def search(self, query: str, max_results: int = 20) -> list[SearchResult]:
        """Search for content matching query. Returns normalised results."""
        ...


class SynthesizerInterface(ABC):
    """LLM wrapper interface. Swap GPT-4o for Claude without touching agents."""

    @abstractmethod
    def synthesize(self, prompt: str, temperature: float = 0.7) -> str:
        """Send prompt to LLM and return response text."""
        ...


class PublisherInterface(ABC):
    """All platform publishers implement this. V1: no auto-publish, skeleton only."""

    @retry_on_failure()
    @abstractmethod
    def publish(self, content: Any) -> dict[str, Any]:
        """Publish content to platform. Returns platform response."""
        ...


class RendererInterface(ABC):
    """All renderers implement this. TextAnimation and Overlay are swappable."""

    @abstractmethod
    def render(self, script: Any, output_path: str) -> str:
        """Render script to video file. Returns path to output."""
        ...
