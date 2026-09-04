"""TenantConfig — the validated blob that defines one tenant.

A tenant is pure data: brand, voice, persona reference, LLM, and registry
refs. New tenant = new YAML blob; no code changes. YAML authors may write
registry refs as plain strings ("short-form/vox") or objects
({name: ..., version: ...}) and prompts as a name->version mapping; the
model normalizes both forms.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from config.schema.brand import Brand
from config.schema.enums import FormatDirection
from config.schema.llm import LLMConfig
from config.schema.persona import PersonaRef
from config.schema.refs import PromptRef, RecipeRef, TemplateRef
from config.schema.voice import Voice

DEFAULT_VOICE_FILE = "config/voice.md"
DEFAULT_PERSONA_FILE = "config/persona.yaml"


def _as_ref_item(value: Any) -> dict[str, Any]:
    """Coerce a plain string registry ref into {'name': <value>}."""
    if isinstance(value, str):
        return {"name": value}
    if isinstance(value, dict):
        return value
    raise TypeError(f"Registry ref must be a string or object, got {type(value).__name__}")


class TenantConfig(BaseModel):
    """Validated configuration blob for a single tenant."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1, description="Tenant id, e.g. t_01.")
    slug: str = Field(
        ...,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="URL-safe tenant slug, e.g. acme-corp.",
    )
    name: str = Field("", description="Human-readable tenant name.")
    brand: Brand = Field(default_factory=Brand)
    voice: Voice = Field(default_factory=lambda: Voice(file=DEFAULT_VOICE_FILE))
    persona: PersonaRef = Field(default_factory=lambda: PersonaRef(file=DEFAULT_PERSONA_FILE))
    llm: LLMConfig = Field(default_factory=LLMConfig)
    prompts: list[PromptRef] = Field(default_factory=list)
    templates: list[TemplateRef] = Field(default_factory=list)
    recipes: list[RecipeRef] = Field(default_factory=list)
    formats: list[FormatDirection] = Field(
        default_factory=lambda: list(FormatDirection),
        description="Format directions this tenant may request.",
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_refs(cls, data: Any) -> Any:
        """Accept plain-string refs and prompt dicts as YAML convenience forms."""
        if not isinstance(data, dict):
            return data
        raw = dict(data)
        for key in ("templates", "recipes"):
            if isinstance(raw.get(key), list):
                raw[key] = [_as_ref_item(item) for item in raw[key]]
        prompts = raw.get("prompts")
        if prompts is not None:
            if isinstance(prompts, dict):
                raw["prompts"] = [
                    {"name": name, "version": version} for name, version in prompts.items()
                ]
            elif isinstance(prompts, list):
                raw["prompts"] = [_as_ref_item(item) for item in prompts]
        if isinstance(raw.get("voice"), str):
            raw["voice"] = {"rules": [raw["voice"]]}
        if isinstance(raw.get("persona"), str):
            raw["persona"] = {"file": raw["persona"]}
        return raw
