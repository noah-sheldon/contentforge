"""Run config blob loading + run input validation tests."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from config.run_loader import load_run_config
from config.schema.enums import InputKind
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
