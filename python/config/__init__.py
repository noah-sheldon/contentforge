"""Config package: settings loader, Pydantic schema, registries, tenant loader.

Public convenience exports mirror config.schema; deep imports stay available.
"""

from config.schema import (
    Brand,
    BrandToken,
    CaptionRules,
    ConfigError,
    ConfigIssue,
    FormatDirection,
    InputKind,
    LLMConfig,
    LlmMode,
    PersonaRef,
    PromptRef,
    RecipeRef,
    RegistryStatus,
    RunConfig,
    RunInput,
    ScriptInput,
    ScriptSource,
    TemplateRef,
    TenantConfig,
    VideoSpec,
    Voice,
)

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
