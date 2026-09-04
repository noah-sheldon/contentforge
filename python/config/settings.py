"""Project-wide configuration — single source of truth for paths and settings.

DRY: Every file imports from here. No hardcoded paths anywhere.
P1: Prompt loading delegates to the versioned PromptRegistry (prompts/registry.yaml).
"""

from pathlib import Path

import yaml

from config.registry.prompts import PromptRegistry

# ─── Paths ────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYTHON_ROOT = PROJECT_ROOT / "python"
AGENTS_DIR = PYTHON_ROOT / "agents"
SERVICES_DIR = PYTHON_ROOT / "services"
SCRIPTS_DIR = PYTHON_ROOT / "scripts"
TESTS_DIR = PYTHON_ROOT / "tests"

PERSONA_PATH = PROJECT_ROOT / "config" / "persona.yaml"
PROMPTS_DIR = AGENTS_DIR / "prompts"
ENV_PATH = PYTHON_ROOT / ".env"

_prompt_registry = PromptRegistry(PROJECT_ROOT)


# ─── Persona loader ───────────────────────────────────────────────────

persona_cache: dict | None = None


def load_persona() -> dict:
    """Load persona.yaml. Cached after first read."""
    global persona_cache
    if persona_cache is None:
        with open(PERSONA_PATH) as f:
            persona_cache = yaml.safe_load(f)
    return persona_cache


# ─── Prompt loader (delegates to the versioned registry) ──────────────

prompt_cache: dict[tuple[str, str | None], str] = {}


def load_prompt(name: str, version: str | None = None, **kwargs) -> str:
    """Load and format a registered prompt template by name.

    Name format: "domain/name" e.g. "research/synthesis", "copy/copywriter",
    or a registry name such as "cp-script". Unregistered legacy paths under
    python/agents/prompts fall back to the pre-registry loader.
    """
    global prompt_cache

    key = (name, version)
    if key not in prompt_cache:
        try:
            text = _prompt_registry.load(name, version)
        except FileNotFoundError:
            # Legacy fallback: payload-only prompt yaml not yet in the registry.
            path = PROMPTS_DIR / f"{name}.yaml"
            if not path.exists():
                raise
            with open(path) as f:
                data = yaml.safe_load(f)
            text = data["prompt"]
        prompt_cache[key] = text

    return prompt_cache[key].format(**kwargs)
