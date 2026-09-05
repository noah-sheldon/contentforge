#!/usr/bin/env python3
"""Web asset capture engine for video production.

Deterministic glue for the ASSETS stage (skills/planner/agents/assets.md).
Captures every page a script references as a LIVE-scroll webm (usable b-roll)
plus top/mid/full-page PNG screenshots (storyboard/reference only — house rule:
static screenshots never appear in-frame) and writes a manifest.

Usage:
  uv run --project python python python/scripts/capture_assets.py sites.json --out <dir> [--workers 3] [--seconds 9]

sites.json: [{"slug": str, "url": str, "note": str}]
Output per site: <out>/<slug>/<slug>.webm, <slug>-top.png, <slug>-mid.png, <slug>-full.png
Manifest:       <out>/manifest.json (captured / failed, with reason)

Env to pass bot walls: PLAYWRIGHT_CHANNEL=chrome, PLAYWRIGHT_UA="<desktop UA>".
Pages that still wall (Cloudflare "Just a moment", empty app shells) fail fast and
are flagged for manual capture in the ASSETS agent.
"""

import argparse
import json
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from playwright.sync_api import sync_playwright

GOLD_CSS = """
.opencode-spotlight-highlight { outline: 3px solid #D4AF37 !important; outline-offset: 4px !important; }
"""

BOT_WALL_MARKERS = ("just a moment", "attention required", "verify you are human")


def capture_one(site: dict, out_dir: Path, record_seconds: int, headed: bool = False) -> dict:
    """Record + screenshot one URL. Raises RuntimeError on walls/empty shells."""
    slug = site["slug"]
    url = site["url"]
    out = out_dir / slug
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not headed,
            channel=os.environ.get("PLAYWRIGHT_CHANNEL") or None,
            args=["--disable-blink-features=AutomationControlled", "--hide-scrollbars"],
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(out),
            record_video_size={"width": 1920, "height": 1080},
            color_scheme="dark",
            locale="en-US",
            user_agent=os.environ.get("PLAYWRIGHT_UA"),
        )
        page = ctx.new_page()
        page.add_init_script(
            "const s=document.createElement('style');"
            f"s.textContent=`{GOLD_CSS}`;document.head.appendChild(s);"
        )
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            try:
                page.goto(url, wait_until="load", timeout=45000)
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError(f"load failed: {exc}") from exc
        page.wait_for_timeout(2500)

        body = page.inner_text("body")
        low = body.lower()
        if any(m in low for m in BOT_WALL_MARKERS) or len(body.strip()) < 80:
            raise RuntimeError("bot wall or empty app shell — flag for manual capture")

        page.screenshot(path=str(out / f"{slug}-top.png"))
        total = page.evaluate("document.documentElement.scrollHeight")
        mid = max(0, int(total * 0.45) - 400)
        page.evaluate(f"window.scrollTo(0, {mid})")
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / f"{slug}-mid.png"))
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        page.screenshot(path=str(out / f"{slug}-full.png"), full_page=True)

        steps = 90
        for _ in range(steps):
            page.mouse.wheel(0, 140)
            page.wait_for_timeout(int(record_seconds * 1000 / steps))
        page.wait_for_timeout(800)

        vpath = page.video.path() if page.video else None
        page.close()
        ctx.close()
        browser.close()

        if vpath:
            shutil.move(vpath, out / f"{slug}.webm")
        else:
            raise RuntimeError("no video recorded")

    return {
        "slug": slug,
        "url": url,
        "files": [f"{slug}.webm", f"{slug}-top.png", f"{slug}-mid.png", f"{slug}-full.png"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sites_json", help="Path to sites.json [{slug,url,note}]")
    parser.add_argument("slugs", nargs="*", help="Optional: capture only these slugs")
    parser.add_argument("--out", default="outputs/assets", help="Output dir (video assets/web)")
    parser.add_argument("--workers", type=int, default=3, help="Parallel page captures")
    parser.add_argument("--seconds", type=int, default=9, help="Recording length per site")
    parser.add_argument("--headed", action="store_true", help="Visible browser (passes bot walls real Chrome clears)")
    args = parser.parse_args()

    sites = json.loads(Path(args.sites_json).read_text(encoding="utf-8"))
    if args.slugs:
        sites = [s for s in sites if s["slug"] in args.slugs]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"captured": [], "failed": []}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(capture_one, s, out_dir, args.seconds, args.headed): s for s in sites}
        for fut in as_completed(futures):
            site = futures[fut]
            try:
                result = fut.result()
                manifest["captured"].append(result)
                print(f"[ok]   {site['slug']}", flush=True)
            except Exception as exc:  # noqa: BLE001
                manifest["failed"].append({"slug": site["slug"], "url": site["url"], "error": str(exc)})
                print(f"[FAIL] {site['slug']}: {exc}", flush=True)

    (out_dir.parent / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest -> {out_dir.parent / 'manifest.json'}")


if __name__ == "__main__":
    sys.exit(main())
