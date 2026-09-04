"""Run-level config: how a run starts and what it produces.

Every run declares its input mode (idea/url/script/assets) and format
direction. The schema validates that the payload matches the declared mode,
so a run cannot silently start from a half-empty request.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from config.schema.enums import FormatDirection, InputKind, ScriptSource


class ScriptInput(BaseModel):
    """User-supplied or generated script text plus optional direction."""

    model_config = ConfigDict(extra="forbid")

    source: ScriptSource = ScriptSource.user
    text: str | None = Field(default=None, description="Full script text when provided.")
    direction: str | None = Field(
        default=None,
        description="High-level direction when no final script is given.",
    )

    @model_validator(mode="after")
    def _text_or_direction(self) -> "ScriptInput":
        if not self.text and not self.direction:
            raise ValueError("script input needs at least one of text, direction")
        return self


class RunInput(BaseModel):
    """The input half of a run request; kind selects the entry stage."""

    model_config = ConfigDict(extra="forbid")

    kind: InputKind
    idea: str | None = Field(default=None, description="Topic text for idea mode.")
    url: str | None = Field(default=None, description="Source URL for url mode.")
    script: ScriptInput | None = Field(default=None, description="For script mode.")
    assets: list[str] = Field(
        default_factory=list,
        description="Local file refs for assets mode (OBJ keys from P2).",
    )

    @model_validator(mode="after")
    def _kind_payload(self) -> "RunInput":
        if self.kind == InputKind.idea and not self.idea:
            raise ValueError("kind=idea requires a non-empty 'idea' topic.")
        if self.kind == InputKind.url and not self.url:
            raise ValueError("kind=url requires a non-empty 'url'.")
        if self.kind == InputKind.script and self.script is None:
            raise ValueError("kind=script requires a 'script' object.")
        if self.kind == InputKind.assets and not self.assets:
            raise ValueError("kind=assets requires at least one asset path.")
        return self


class RunConfig(BaseModel):
    """Everything needed to start one pipeline run."""

    model_config = ConfigDict(extra="forbid")

    tenant: str = Field(..., description="Tenant slug the run belongs to.")
    project_title: str = Field("", description="Optional human-readable project title.")
    format_direction: FormatDirection = FormatDirection.short
    input: RunInput
