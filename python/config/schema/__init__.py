"""Config schema package: Pydantic models for tenants, runs, and registries.

Public surface — import these names from config.schema:
    TenantConfig, RunConfig, RunInput, ScriptInput, Voice, Brand, VideoSpec,
    LLMConfig, PersonaRef, PromptRef, TemplateRef, RecipeRef, ConfigError
"""

from config.schema.brand import Brand, VideoSpec
from config.schema.enums import (
    BrandToken,
    FormatDirection,
    InputKind,
    LlmMode,
    RegistryStatus,
    ScriptSource,
)
from config.schema.errors import ConfigError, ConfigIssue
from config.schema.llm import LLMConfig
from config.schema.persona import PersonaRef
from config.schema.refs import PromptRef, RecipeRef, TemplateRef
from config.schema.run import RunConfig, RunInput, ScriptInput
from config.schema.tenant import TenantConfig
from config.schema.voice import CaptionRules, Voice

__all__ = [
    "Brand",
    "BrandToken",
    "CaptionRules",
    "ConfigError",
    "ConfigIssue",
    "FormatDirection",
    "InputKind",
    "LLMConfig",
    "LlmMode",
    "PersonaRef",
    "PromptRef",
    "RecipeRef",
    "RegistryStatus",
    "RunConfig",
    "RunInput",
    "ScriptInput",
    "ScriptSource",
    "TemplateRef",
    "TenantConfig",
    "VideoSpec",
    "Voice",
]
