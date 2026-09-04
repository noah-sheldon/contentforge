"""Scene planner tests (deterministic offline strategy)."""

from pathlib import Path

from config.loader import load_tenant_by_slug
from services.scene_planner import ScenePlanner

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_scene_planner_deterministic_blocks():
    tenant = load_tenant_by_slug("sample", repo_root=REPO_ROOT)
    text = "First point. Second point. Third point. Fourth point."
    blocks = ScenePlanner(use_llm=False).plan(text, tenant)
    assert blocks
    assert all(b.type for b in blocks)
    assert all(b.duration_seconds > 0 for b in blocks)
