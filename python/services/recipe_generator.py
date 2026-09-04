"""Capture recipe generator — LLM turns a URL/script into a validated Recipe.

The generator formats the registered video/capture_recipe prompt, calls the
LLM, and validates its JSON against the Recipe schema. Invalid output raises
ConfigError with the validation issues (fail fast, never hand the pipeline a
malformed action list).
"""

from __future__ import annotations

import json
import re
from typing import Optional

from pydantic import ValidationError

from agents.base import SynthesizerInterface
from agents.synthesis.openai import OpenAISynthesizer
from config.registry.prompts import PromptRegistry
from config.schema.errors import ConfigError, config_error_from_pydantic
from config.schema.recipe import Recipe
from config.settings import PROJECT_ROOT


class RecipeGenerator:
    """Generates capture recipes from a URL and/or script via the LLM."""

    def __init__(self, llm: Optional[SynthesizerInterface] = None, repo_root=None):
        self.llm = llm or OpenAISynthesizer(thinking=True)
        self.repo_root = repo_root or PROJECT_ROOT

    def generate(self, url: str = "", direction: str = "") -> Recipe:
        """Return a validated Recipe for the given target."""
        if not url and not direction:
            raise ValueError("Recipe generation needs a URL and/or script/direction.")
        prompt_registry = PromptRegistry(self.repo_root)
        prompt = prompt_registry.load("video/capture_recipe").format(
            url=url or "(none)",
            direction=direction or "(none)",
        )
        raw = self.llm.synthesize(prompt, temperature=0.2)
        payload = _extract_json(raw)
        try:
            return Recipe.model_validate(payload)
        except ValidationError as exc:
            raise config_error_from_pydantic(exc, "Generated recipe") from exc
        except ValueError as exc:
            raise ConfigError(f"Generated recipe is invalid: {exc}") from exc


def _extract_json(raw: str) -> dict:
    """Parse the JSON object from an LLM response, tolerating prose fences."""
    stripped = raw.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    match = re.search(r"\{.*\}", stripped, re.DOTALL)
    if not match:
        raise ConfigError("Recipe generator returned no JSON object.")
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Recipe generator returned malformed JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError("Recipe generator JSON must be an object.")
    return data
