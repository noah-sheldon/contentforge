"""Enums shared across the config schema.

All run-level and registry-level vocabulary lives here so schema models,
registry loaders, and pipeline code agree on spellings without string drift.
"""

from enum import Enum


class FormatDirection(str, Enum):
    """The four run-level transformation modes a pipeline run may request."""

    short = "short"
    long = "long"
    long_to_short = "long_to_short"
    short_to_long = "short_to_long"


class InputKind(str, Enum):
    """Entry mode for a run; selects which pipeline stage the run enters at."""

    idea = "idea"
    url = "url"
    script = "script"
    assets = "assets"


class ScriptSource(str, Enum):
    """Origin of the script text for script/hybrid input modes."""

    generated = "generated"
    user = "user"
    hybrid = "hybrid"


class LlmMode(str, Enum):
    """How a tenant's LLM access is provided."""

    hosted = "hosted"
    byok = "byok"


class RegistryStatus(str, Enum):
    """Lifecycle state of a registry entry (prompt/template/recipe)."""

    active = "active"
    deprecated = "deprecated"


class BrandToken(str, Enum):
    """Canonical brand color tokens; single source shared with the web theme."""

    obsidian = "obsidian"
    alabaster = "alabaster"
    gold = "gold"
    silent_gray = "silent_gray"
