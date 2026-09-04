"""Brand config: color tokens, surfaces, fonts, video defaults.

A tenant's brand is an arbitrary token map (token -> color value) plus an
optional surface map. The canonical tokens from persona.yaml
(obsidian/alabaster/gold/silent_gray) are supplied as convenient defaults
but are not required; tenants may define their own palette.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def _is_rgba(value: str) -> bool:
    """Return True for rgb()/rgba() literals with 3-4 numeric components."""
    body = value.strip()
    if not (body.startswith("rgb(") and body.endswith(")")) and not (
        body.startswith("rgba(") and body.endswith(")")
    ):
        return False
    inner = body[body.index("(") + 1 : -1]
    parts = [p.strip() for p in inner.split(",")]
    if len(parts) not in (3, 4):
        return False
    try:
        return all(float(p) >= 0 for p in parts)
    except ValueError:
        return False


def is_valid_color(value: str) -> bool:
    """Return True when value is a hex or rgb()/rgba() color literal."""
    return bool(_HEX_RE.match(value) or _is_rgba(value))


class Brand(BaseModel):
    """Visual identity tokens for a tenant."""

    model_config = ConfigDict(extra="forbid")

    colors: dict[str, str] = Field(
        default_factory=dict,
        description="Brand color tokens; values are hex or rgba() literals.",
    )
    surfaces: dict[str, str] = Field(
        default_factory=dict,
        description="Surface treatments such as gold_border or glass_bg.",
    )
    fonts: dict[str, str] = Field(
        default_factory=dict,
        description="Font role -> family, e.g. {primary: Inter, mono: JetBrains Mono}.",
    )
    video: VideoSpec = Field(default_factory=lambda: VideoSpec())

    @field_validator("colors", "surfaces")
    @classmethod
    def _colors_are_literals(cls, value: dict[str, str]) -> dict[str, str]:
        for token, color in value.items():
            if not is_valid_color(color):
                raise ValueError(
                    f"'{token}' value {color!r} is not a color; use hex (#RRGGBB) or rgba(...)."
                )
        return value

    def color(self, token: str, default: str | None = None) -> str | None:
        """Look up a color token, returning default when absent."""
        return self.colors.get(token, default)


class VideoSpec(BaseModel):
    """Render defaults for brand video output."""

    model_config = ConfigDict(extra="forbid")

    aspect_ratio: str = "9:16"
    resolution: str = "1080x1920"
    fps: int = 30
