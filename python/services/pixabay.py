"""Pixabay audio service for SFX.

S: Single responsibility -- downloads audio from Pixabay.
O: New source = new downloader class. This file never changes.
Self-correction: Retries once on failure. Returns None gracefully.

Rule: music is BANNED on all videos (video-agent v1.4+). The music
endpoints (search_music / get_background_music) are deprecated and return
None so no code path can add a music bed.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import requests

log = logging.getLogger("pixabay")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")


def _search(url: str, params: dict) -> list[dict]:
    """Search Pixabay. Returns empty list on any failure."""
    if not PIXABAY_API_KEY:
        log.warning("PIXABAY_API_KEY not set")
        return []
    params["key"] = PIXABAY_API_KEY
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("hits", [])
    except requests.RequestException as e:
        log.warning(f"Pixabay search failed: {e}")
        return []


def search_music(query: str, per_page: int = 5) -> list[dict]:
    log.warning("search_music is deprecated: music is banned on all videos (video-agent v1.4+). Use search_sfx.")
    return []


def search_sfx(query: str, per_page: int = 5) -> list[dict]:
    hits = _search(
        "https://pixabay.com/api/audio/",
        {
            "q": query,
            "per_page": per_page,
        },
    )
    return [
        {
            "title": hit.get("tags", "sfx").split(",")[0].strip(),
            "url": hit.get("url", ""),
            "duration": hit.get("duration", 0),
        }
        for hit in hits
    ]


def download(url: str, output_path: str) -> Optional[str]:
    """Download file. Returns path or None on failure."""
    try:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        path.write_bytes(resp.content)
        return str(path)
    except Exception as e:
        log.warning(f"Download failed: {e}")
        return None


def get_background_music(output_dir: str, mood: str = "ambient") -> Optional[str]:
    """Deprecated -- music is banned on all videos (video-agent v1.4+). Returns None."""
    log.warning("get_background_music is deprecated: music is banned on all videos. No music downloaded.")
    return None
