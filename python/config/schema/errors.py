"""Actionable configuration errors.

Single error type for every config failure so callers can catch one thing
and present one clear message. Pydantic's ValidationError is flattened into
ConfigError entries with the failing field path and a human reason.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import ValidationError


@dataclass
class ConfigIssue:
    """A single validation failure with a field path and reason."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}" if self.path else self.message


class ConfigError(Exception):
    """Raised when a config blob fails schema or registry validation."""

    def __init__(self, message: str, issues: list[ConfigIssue] | None = None):
        super().__init__(message)
        self.message = message
        self.issues: list[ConfigIssue] = issues or []
        if self.issues:
            detail = "\n".join(f"  - {i}" for i in self.issues)
            self.message = f"{message}\n{detail}"
            self.args = (self.message,)


def _field_path(loc: tuple[str | int, ...]) -> str:
    """Render a pydantic loc tuple as a dotted field path."""
    out: list[str] = []
    for part in loc:
        if isinstance(part, int):
            out.append(f"[{part}]")
        elif not out:
            out.append(str(part))
        else:
            out.append(f".{part}")
    return "".join(out) if out else "(root)"


def issues_from_pydantic(error: ValidationError) -> list[ConfigIssue]:
    """Flatten a pydantic ValidationError into ConfigIssue list."""
    return [
        ConfigIssue(
            path=_field_path(e.get("loc", ())),
            message=str(e.get("msg", "invalid value")).replace("\n", " "),
        )
        for e in error.errors()
    ]


def config_error_from_pydantic(error: ValidationError, label: str = "Config") -> ConfigError:
    """Build an actionable ConfigError from a pydantic ValidationError."""
    return ConfigError(f"{label} is invalid.", issues_from_pydantic(error))
