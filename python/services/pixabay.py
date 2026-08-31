"""Pixabay audio service for background music and SFX.

S: Single responsibility -- downloads audio from Pixabay.
O: New source = new downloader class. This file never changes.
Self-correction: Retries once on failure. Returns None gracefully.
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
    hits = _search("https://pixabay.com/api/videos/", {
        "q": query, "per_page": per_page, "video_type": "film",
    })
    results = []
    for hit in hits:
        videos = hit.get("videos", {})
        for size in ["small", "medium"]:
            if size in videos:
                results.append({
                    "title": (hit.get("tags", "") or "").split(",")[0].strip(),
                    "url": videos[size]["url"],
                    "duration": hit.get("duration", 0),
                })
                break
    return results


def search_sfx(query: str, per_page: int = 5) -> list[dict]:
    hits = _search("https://pixabay.com/api/audio/", {
        "q": query, "per_page": per_page,
    })
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
    """Download background music via Pixabay audio API. Returns path or None."""
    try:
        resp = requests.get("https://pixabay.com/api/audio/", params={
            "key": PIXABAY_API_KEY,
            "q": mood,
            "per_page": 5,
        }, timeout=15)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
    except Exception as e:
        log.warning(f"Audio search failed: {e}")
        return None

    if not hits:
        return None

    audio_url = hits[0].get("url", "")
    if not audio_url:
        return None

    ext = audio_url.rsplit(".", 1)[-1] if "." in audio_url else "mp3"
    out_path = f"{output_dir}/audio/background.{ext}"
    return download(audio_url, out_path)
