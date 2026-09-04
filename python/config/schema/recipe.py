"""Capture recipe schema.

A capture recipe is a sequence of typed Playwright actions that the capture
script executes against a page. Actions use a discriminated union on `type`
so an unknown action or a malformed payload fails validation immediately.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

# ─── Actions ──────────────────────────────────────────────────────────


class WaitAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["wait"] = "wait"
    duration: int = Field(default=2000, gt=0)
    wait: int = Field(default=0, ge=0)


class ScrollAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["scroll"] = "scroll"
    y: int = Field(default=400, ge=0)
    steps: int = Field(default=10, gt=0)
    step_delay: int = Field(default=50, ge=0)
    wait: int = Field(default=0, ge=0)


class ClickAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["click"] = "click"
    selector: str = Field(..., min_length=1)
    wait: int = Field(default=0, ge=0)


class TypeAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["type"] = "type"
    selector: str = Field(..., min_length=1)
    text: str = ""
    delay: int = Field(default=80, ge=0)
    wait: int = Field(default=0, ge=0)


class HighlightAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["highlight"] = "highlight"
    selector: str = Field(..., min_length=1)
    wait: int = Field(default=0, ge=0)


class UnhighlightAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["unhighlight"] = "unhighlight"
    selector: str | None = Field(default=None)
    wait: int = Field(default=0, ge=0)


CaptureAction = Annotated[
    WaitAction | ScrollAction | ClickAction | TypeAction | HighlightAction | UnhighlightAction,
    Field(discriminator="type"),
]


# ─── Recipe ───────────────────────────────────────────────────────────


class Recipe(BaseModel):
    """One named capture recipe: a sequence of typed actions."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    version: str = Field(default="1.0.0")
    name: str = Field(..., min_length=1)
    description: str = ""
    actions: list[CaptureAction] = Field(..., min_length=1)
