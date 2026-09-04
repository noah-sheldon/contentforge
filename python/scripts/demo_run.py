"""Demo run — sample tenant renders a short video end-to-end from config alone.

Reads a run config blob (config/runs/*.yaml), loads + validates the tenant it
references, plans scenes from the run's script text, and renders an MP4 using
the tenant's brand tokens. No per-video code is involved.

Usage:
    python -m scripts.demo_run --run config/runs/sample-demo.yaml [--output out.mp4]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from config.loader import load_tenant_by_slug
from config.run_loader import load_run_config
from config.schema.errors import ConfigError, ConfigIssue
from config.settings import PROJECT_ROOT
from services.scene_planner import ScenePlanner
from services.text_animator import render_blocks


def run_demo(run_path: str | Path, output: str | Path | None = None) -> str:
    """Execute a config-driven demo run; returns the rendered MP4 path."""
    run = load_run_config(run_path)
    tenant = load_tenant_by_slug(run.tenant)

    if run.format_direction not in tenant.formats:
        raise ConfigError(
            f"Run format '{run.format_direction.value}' not enabled for tenant '{run.tenant}'.",
            [ConfigIssue("formats", f"tenant allows: {[f.value for f in tenant.formats]}")],
        )

    script_text = run.input.script.text if run.input.script else run.input.idea
    if not script_text:
        raise ConfigError(
            f"Run '{run.tenant}' has no script text to render.",
            [ConfigIssue("input", "script-mode runs need input.script.text.")],
        )
    planner = ScenePlanner()
    blocks = planner.plan(script_text, tenant)

    brand = {"colors": dict(tenant.brand.colors)}
    fonts = dict(tenant.brand.fonts)

    if output is None:
        output = PROJECT_ROOT / "outputs" / tenant.slug / f"{run.project_title or 'demo'}.mp4"
    output_path = Path(output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Tenant: {tenant.slug} ({tenant.name or 'no name'})")
    print(f"Format: {run.format_direction.value} | scenes: {len(blocks)}")
    print(f"Template registry refs: {[t.name for t in tenant.templates]}")
    return render_blocks(blocks, str(output_path), brand=brand, fonts=fonts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, help="Run config blob under config/runs/")
    parser.add_argument("--output", default=None, help="Output MP4 path.")
    args = parser.parse_args()
    run_demo(args.run, args.output)


if __name__ == "__main__":
    main()
