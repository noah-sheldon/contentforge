"""P1 tests: tenant config schema, registries, overrides, run input."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from config.loader import load_tenant_config
from config.registry.prompts import PromptRegistry
from config.registry.recipes import RecipeLibrary
from config.registry.templates import TemplateRegistry
from config.schema import (
    InputKind,
    PromptRef,
    RunInput,
    ScriptInput,
    ScriptSource,
)
from config.schema.errors import ConfigError

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_sample_tenant_loads():
    tenant = load_tenant_config(REPO_ROOT / "config/tenants/sample.yaml")
    assert tenant.slug == "sample"
    assert tenant.brand.colors["obsidian"] == "#12141C"
    assert tenant.brand.fonts["mono"] == "JetBrains Mono"
    assert tenant.persona.file == "config/persona.yaml"
    assert tenant.voice.file == "config/voice.md"
    assert tenant.llm.model == "deepseek-v4-flash"
    assert {f.value for f in tenant.formats} == {
        "short",
        "long",
        "long_to_short",
        "short_to_long",
    }
    assert any(p.name == "copy/copywriter" and p.version == "1.0.0" for p in tenant.prompts)
    assert any(t.name == "short-form/desk-setup" for t in tenant.templates)
    assert any(r.name == "table-walkthrough" for r in tenant.recipes)


def test_invalid_color_rejected_with_path():
    payload = {
        "id": "t_bad",
        "slug": "bad-color",
        "brand": {"colors": {"obsidian": "not-a-color"}},
    }
    with pytest.raises(ConfigError) as exc:
        _validate_payload(payload)
    issues = exc.value.issues
    assert any(i.path.startswith("brand.colors") for i in issues)


def _validate_payload(payload: dict):
    from config.schema.errors import config_error_from_pydantic
    from config.schema.tenant import TenantConfig

    try:
        return TenantConfig.model_validate(payload)
    except ValidationError as err:
        raise config_error_from_pydantic(err, "Tenant config") from err


def test_unknown_field_rejected():
    with pytest.raises(ConfigError) as exc:
        _validate_payload({"id": "t_x", "slug": "x", "not_a_field": True})
    assert any("not_a_field" in i.message or "not_a_field" in i.path for i in exc.value.issues)


def test_extra_formats_rejected():
    with pytest.raises(ConfigError):
        _validate_payload({"id": "t_x", "slug": "x", "formats": ["short", "remix_into_4d"]})


def test_overrides_merge_and_validate():
    tenant = load_tenant_config(
        REPO_ROOT / "config/tenants/sample.yaml",
        overrides={"brand": {"colors": {"gold": "#FFD700"}}},
    )
    assert tenant.brand.colors["gold"] == "#FFD700"
    # Unrelated tokens survive the deep merge.
    assert tenant.brand.colors["obsidian"] == "#12141C"


def test_overrides_invalid_fail_fast():
    with pytest.raises(ConfigError):
        load_tenant_config(
            REPO_ROOT / "config/tenants/sample.yaml",
            overrides={"brand": {"colors": {"gold": "nope"}}},
        )


def test_prompt_registry_loads_by_name_and_version():
    reg = PromptRegistry(REPO_ROOT)
    text = reg.load("story/animation_director", "1.0.0")
    assert "{hook}" in text
    with pytest.raises(ConfigError):
        reg.load("story/animation_director", "9.9.9")
    with pytest.raises(ConfigError):
        reg.load("no/such-prompt")


def test_prompt_refs_are_semver_validated():
    with pytest.raises(ValidationError):
        PromptRef(name="copy/copywriter", version="not-semver")


def test_template_registry_discovers_and_resolves():
    reg = TemplateRegistry(REPO_ROOT)
    names = reg.list_names()
    assert "short-form/desk-setup" in names
    tpl = reg.get("short-form/desk-setup")
    assert tpl.index_html.is_file()
    assert tpl.spec
    with pytest.raises(ConfigError):
        reg.get("does/not-exist")


def test_recipe_library_loads_and_resolves():
    lib = RecipeLibrary(REPO_ROOT)
    ids = lib.list_ids()
    assert "table-walkthrough" in ids
    recipe = lib.get("table-walkthrough")
    assert recipe.actions[0].type == "wait"
    with pytest.raises(ConfigError):
        lib.get("missing-recipe")


def test_run_input_requires_url_for_url_kind():
    with pytest.raises(ValidationError):
        RunInput(kind=InputKind.url)


def test_run_input_script_mode_ok():
    run = RunInput(
        kind=InputKind.script,
        script=ScriptInput(source=ScriptSource.user, text="Hello world"),
    )
    assert run.kind == InputKind.script
