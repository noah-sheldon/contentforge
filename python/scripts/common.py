#!/usr/bin/env python3
"""Shared paths + config for the content-planner pipeline.

Rule: scripts contain ONLY deterministic, stable logic. Anything that can
change (paths, model names, board numbers, lifecycle options) lives in
config.yaml / skill/persona.yaml.
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _load_config():
    p = ROOT / "config.yaml"
    if not p.exists():
        return {}
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}


CONFIG = _load_config()
_paths = CONFIG.get("paths", {})

LIBRARY = ROOT / _paths.get("library", "library")
OUTPUTS = ROOT / _paths.get("outputs", "outputs")
CALENDAR = ROOT / _paths.get("calendar", "calendar")


def ensure_dirs():
    for d in (LIBRARY, OUTPUTS, CALENDAR):
        d.mkdir(parents=True, exist_ok=True)


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s[:max_len] or "untitled"


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
