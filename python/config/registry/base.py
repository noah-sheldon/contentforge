"""Shared helpers for registry loaders: YAML IO and markdown frontmatter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    """Load a YAML file, raising FileNotFoundError with a clear message."""
    if not path.is_file():
        raise FileNotFoundError(f"Registry data file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split markdown frontmatter (--- yaml ---) from body.

    Returns (frontmatter_dict, body). Body excludes the delimiters.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines(keepends=True)
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}, text
    header = "".join(lines[1:end])
    body = "".join(lines[end + 1 :])
    try:
        meta = yaml.safe_load(header) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Malformed frontmatter: {exc}") from exc
    if not isinstance(meta, dict):
        raise ValueError("Frontmatter must be a YAML mapping.")
    return meta, body
