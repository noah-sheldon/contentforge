"""Project-wide configuration — single source of truth for paths and settings.

DRY: Every file imports from here. No hardcoded paths anywhere.
"""

from pathlib import Path

import yaml

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


# ─── Persona loader ───────────────────────────────────────────────────

persona_cache: dict | None = None


def load_persona() -> dict:
    """Load persona.yaml. Cached after first read."""
    global persona_cache
    if persona_cache is None:
        with open(PERSONA_PATH) as f:
            persona_cache = yaml.safe_load(f)
    return persona_cache


# ─── Prompt loader ────────────────────────────────────────────────────

prompt_cache: dict[str, str] = {}


def load_prompt(name: str, **kwargs) -> str:
    """Load and format a prompt template from prompts/{domain}/{name}.yaml.

    Name format: "domain/name" e.g. "research/synthesis", "copy/copywriter"
    """
    global prompt_cache

    if name not in prompt_cache:
        path = PROMPTS_DIR / f"{name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Prompt '{name}' not found at {path}")
        with open(path) as f:
            data = yaml.safe_load(f)
        prompt_cache[name] = data["prompt"]

    return prompt_cache[name].format(**kwargs)
