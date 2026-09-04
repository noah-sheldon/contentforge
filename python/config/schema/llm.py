"""LLM provider configuration for a tenant.

Hosted mode uses the platform's LiteLLM virtual key; byok mode carries a
key reference the pipeline resolves at runtime. Model naming follows the
LiteLLM aliases used by the pipeline (default deepseek-v4-flash).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from config.schema.enums import LlmMode


class LLMConfig(BaseModel):
    """Which LLM a tenant's runs use and how credentials are provided."""

    model_config = ConfigDict(extra="forbid")

    mode: LlmMode = LlmMode.hosted
    provider: str = Field(default="deepseek", min_length=1)
    model: str = Field(default="deepseek-v4-flash", min_length=1)
    key_ref: str | None = Field(
        default=None,
        description="Encrypted key reference when mode=byok.",
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
