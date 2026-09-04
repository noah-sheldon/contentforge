"""Config package: settings loader, Pydantic schema, registries, loaders.

Public convenience exports mirror config.schema; deep imports stay available.
Tenant blobs load via config.loader; run blobs via config.run_loader.
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
