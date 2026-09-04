"""P1 tests: run configs, scene planner, recipe generator."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from agents.base import SynthesizerInterface
from config.loader import load_run_config
from config.schema.enums import InputKind
from config.schema.errors import ConfigError
from config.schema.recipe import Recipe
from config.schema.run import RunInput

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_sample_demo_run_loads():
    run = load_run_config(REPO_ROOT / "config/runs/sample-demo.yaml")
    script_input = run.input.script
    assert run.tenant == "sample"
    assert run.format_direction.value == "short"
    assert run.input.kind == InputKind.script
    assert script_input is not None
    assert script_input.text is not None
    assert "ContentForge" in script_input.text


def test_run_input_url_kind_requires_url():
    with pytest.raises(ValidationError):
        RunInput(kind=InputKind.url)


def test_run_input_script_kind_requires_script():
    with pytest.raises(ValidationError):
        RunInput(kind=InputKind.script)


def test_scene_planner_deterministic_blocks():
    from config.loader import load_tenant_by_slug
    from services.scene_planner import ScenePlanner

    tenant = load_tenant_by_slug("sample", repo_root=REPO_ROOT)
    text = "First point.\nSecond point.\nThird point.\nFourth point."
    blocks = ScenePlanner(use_llm=False).plan(text, tenant)
    assert blocks
    assert all(b.type for b in blocks)
    assert all(b.duration_seconds > 0 for b in blocks)


class _StubSynthesizer(SynthesizerInterface):
    """Minimal SynthesizerInterface for recipe generator tests."""

    def __init__(self, response: str):
        self.response = response
        self.calls: list[str] = []

    def synthesize(self, prompt: str, temperature: float = 0.7) -> str:
        self.calls.append(prompt)
        return self.response


def test_recipe_generator_validates_llm_output():
    from services.recipe_generator import RecipeGenerator

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
    from services.recipe_generator import RecipeGenerator

    stub = _StubSynthesizer('{"id": "x", "actions": [{"type": "teleport"}]}')
    with pytest.raises(ConfigError):
        RecipeGenerator(llm=stub, repo_root=REPO_ROOT).generate(url="https://x.dev")


def test_recipe_generator_rejects_non_json():
    from services.recipe_generator import RecipeGenerator

    stub = _StubSynthesizer("Sorry, I cannot do that.")
    with pytest.raises(ConfigError):
        RecipeGenerator(llm=stub, repo_root=REPO_ROOT).generate(url="https://x.dev")
