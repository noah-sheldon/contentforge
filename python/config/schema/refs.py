"""Typed references into the prompt/template/recipe registries.

A registry ref is name + optional pinned version. Versions use loose semver
(major.minor.patch) so prompt files can bump majors without breaking code.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


class RegistryRef(BaseModel):
    """Base for any registry reference: name plus optional version."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    version: str | None = Field(
        default=None,
        description="Optional semver pin; latest is used when omitted.",
    )

    @field_validator("version")
    @classmethod
    def _version_is_semver(cls, value: str | None) -> str | None:
        if value is not None and not _SEMVER_RE.match(value):
            raise ValueError(f"version must be semver (major.minor.patch), got {value!r}")
        return value


class PromptRef(RegistryRef):
    """Reference to a registered prompt by name."""


class TemplateRef(RegistryRef):
    """Reference to a registered HyperFrames template by name."""


class RecipeRef(RegistryRef):
    """Reference to a registered capture recipe by name."""
