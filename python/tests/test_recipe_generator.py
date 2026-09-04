"""Recipe generator tests (stubbed synthesizer)."""

from pathlib import Path

import pytest

from agents.base import SynthesizerInterface
from config.schema.errors import ConfigError
from config.schema.recipe import Recipe
from services.recipe_generator import RecipeGenerator

REPO_ROOT = Path(__file__).resolve().parents[2]


class _StubSynthesizer(SynthesizerInterface):
    """Minimal SynthesizerInterface for recipe generator tests."""

    def __init__(self, response: str):
        self.response = response
        self.calls: list[str] = []

    def synthesize(self, prompt: str, temperature: float = 0.7) -> str:
        self.calls.append(prompt)
        return self.response


def test_recipe_generator_validates_llm_output():
    stub = _StubSynthesizer(
        '```json\n{"id": "json-api-demo", "name": "JSON API Demo", '
        '"description": "show endpoints", "actions": ['
        '{"type": "wait", "duration": 2000}, '
        '{"type": "highlight", "selector": "pre"}]}\n```'
    )
    recipe = RecipeGenerator(llm=stub, repo_root=REPO_ROOT).generate(
        url="https://example.com/api", direction="demo the endpoint"
    )
    assert isinstance(recipe, Recipe)
    assert recipe.actions[0].type == "wait"
    assert recipe.actions[1].type == "highlight"
    assert stub.calls  # the prompt was actually sent


def test_recipe_generator_rejects_invalid_output():
    stub = _StubSynthesizer('{"id": "x", "actions": [{"type": "teleport"}]}')
    with pytest.raises(ConfigError):
        RecipeGenerator(llm=stub, repo_root=REPO_ROOT).generate(url="https://x.dev")


def test_recipe_generator_rejects_non_json():
    stub = _StubSynthesizer("Sorry, I cannot do that.")
    with pytest.raises(ConfigError):
        RecipeGenerator(llm=stub, repo_root=REPO_ROOT).generate(url="https://x.dev")
