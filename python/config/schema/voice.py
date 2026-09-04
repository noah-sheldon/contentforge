"""Voice and caption ruleset config.

The single source of voice rules today is config/voice.md; a tenant may point
`file` at it and/or supply inline rules. Rules are plain-language strings
consumed by prompt assembly, so new rules are config, never code.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Voice(BaseModel):
    """Tenant voice identity plus caption rules."""

    model_config = ConfigDict(extra="forbid")

    grade: str = Field(default="5-6", description="Readability grade for copy.")
    rules: list[str] = Field(default_factory=list)
    file: str | None = Field(
        default=None,
        description="Optional path to a markdown voice doc relative to repo root.",
    )

    @model_validator(mode="after")
    def _at_least_one_source(self) -> "Voice":
        if not self.rules and not self.file:
            raise ValueError("voice needs at least one of: rules, file")
        if self.file and not str(self.file).endswith((".md", ".yaml", ".yml")):
            raise ValueError(f"voice file must be markdown/yaml, got {self.file!r}")
        return self

    def rule_text(self, repo_root: Path) -> str:
        """Combine file contents (when present) with inline rules."""
        parts = list(self.rules)
        if self.file:
            candidate = Path(self.file)
            path = candidate if candidate.is_absolute() else repo_root / candidate
            if not path.exists():
                raise FileNotFoundError(f"Voice rules file not found: {path}")
            parts.append(path.read_text(encoding="utf-8").strip())
        return "\n\n".join(parts)


class CaptionRules(BaseModel):
    """Overlay/caption style tokens. Reserved for P1.5 caption policy."""

    model_config = ConfigDict(extra="forbid")

    max_words_per_screen: int = 3
    em_dash_policy: str = "never"
