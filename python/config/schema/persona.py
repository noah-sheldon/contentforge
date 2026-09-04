"""Persona configuration.

The persona (creator identity, voice, brand) lives in a YAML file. A tenant
config references it by path; the loader resolves it relative to the repo
root and validates that the referenced file exists and parses as YAML.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class PersonaRef(BaseModel):
    """File reference to a persona YAML blob."""

    model_config = ConfigDict(extra="forbid")

    file: str = Field(..., description="Persona YAML path relative to the repo root.")

    def resolve(self, repo_root: Path) -> Path:
        """Return the absolute persona path, validating it exists."""
        path = Path(self.file)
        resolved = path if path.is_absolute() else repo_root / path
        if not resolved.is_file():
            raise FileNotFoundError(f"Persona file not found: {resolved}")
        if resolved.suffix not in (".yaml", ".yml"):
            raise ValueError(f"Persona file must be YAML, got {resolved}")
        return resolved
