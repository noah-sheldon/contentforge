"""Run config loading: YAML blob -> validated RunConfig.

Runs describe a single pipeline execution (tenant, format direction, input
kind + payload). This module owns reading and validating those blobs;
RunConfig model + validation live in config.schema.run.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from config.schema.errors import ConfigError, config_error_from_pydantic
from config.schema.run import RunConfig


def normalize_run_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the run mapping, accepting a bare blob or a 'run:' wrapper."""
    return payload.get("run", payload) if isinstance(payload, dict) else payload


def load_run_config(
    path: str | Path,
    repo_root: Path | None = None,
) -> RunConfig:
    """Load and validate a run config blob (config/runs/*.yaml)."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    run_path = Path(path)
    if not run_path.is_absolute():
        run_path = root / run_path
    if not run_path.is_file():
        raise ConfigError(f"Run config file not found: {run_path}")
    with open(run_path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    payload = normalize_run_payload(raw)
    if not isinstance(payload, dict):
        raise ConfigError(f"Run config {run_path} must be a YAML mapping.")
    try:
        return RunConfig.model_validate(payload)
    except ValidationError as exc:
        raise config_error_from_pydantic(exc, f"Run config {run_path}") from exc
