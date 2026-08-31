#!/usr/bin/env python3
"""Automated screen capture engine using Playwright for tech demo videos.

Captures pixel-perfect browser walkthroughs for YouTube (16:9) and Shorts/X (9:16).
Supports action recipes (scrolling, clicking, typing, highlighting, waiting).
"""
import argparse
import json
import os
from pathlib import Path

from common import ROOT

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

GOLD_ACCENT_CSS = """
.opencode-spotlight-highlight {
    outline: 3px solid #D4AF37 !important;
    outline-offset: 4px !important;
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
}
"""


def execute_action_recipe(page, recipe_actions):
    """Executes a list of step-by-step actions on the page."""
    for action in recipe_actions:
        action_type = action.get("type", "").lower()
        delay_after = action.get("wait", 1000)

        if action_type == "scroll":
            delta_y = action.get("y", 400)
            steps = action.get("steps", 10)
            step_delay = action.get("step_delay", 50)
            for _ in range(steps):
                page.mouse.wheel(0, delta_y / steps)
                page.wait_for_timeout(step_delay)

        elif action_type == "click":
            selector = action.get("selector")
            if selector:
                page.wait_for_selector(selector, timeout=5000)
                page.click(selector)

        elif action_type == "type":
            selector = action.get("selector")
            text = action.get("text", "")
            delay = action.get("delay", 80)
            if selector:
                page.wait_for_selector(selector, timeout=5000)
                page.type(selector, text, delay=delay)

        elif action_type == "highlight":
            selector = action.get("selector")
            if selector:
                page.evaluate(
                    """(sel) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        el.classList.add('opencode-spotlight-highlight');
                        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }""",
                    selector,
                )

        elif action_type == "unhighlight":
            selector = action.get("selector")
            if selector:
                page.evaluate(
                    """(sel) => {
                    const el = document.querySelector(sel);
                    if (el) el.classList.remove('opencode-spotlight-highlight');
                }""",
                    selector,
                )
            else:
                page.evaluate(
                    """() => {
                    document.querySelectorAll('.opencode-spotlight-highlight')
                        .forEach(el => el.classList.remove('opencode-spotlight-highlight'));
                }"""
                )

        elif action_type == "wait":
            duration = action.get("duration", 2000)
            page.wait_for_timeout(duration)

        if delay_after > 0:
            page.wait_for_timeout(delay_after)


def record_screen(
    url: str,
    output_dir: Path,
    aspect_ratio: str = "16:9",
    recipe_path: Path = None,
    duration_seconds: int = 10,
    headless: bool = True,
    color_scheme: str = "dark",
) -> Path:
    """Records a browser session using Playwright and saves the video artifact."""
    if sync_playwright is None:
        raise RuntimeError(
            "playwright is not installed in the environment. Run: pip install playwright && playwright install chromium"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    if aspect_ratio == "9:16":
        viewport = {"width": 1080, "height": 1920}
        record_size = {"width": 1080, "height": 1920}
    else:  # 16:9 default
        viewport = {"width": 1920, "height": 1080}
        record_size = {"width": 1920, "height": 1080}

    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--hide-scrollbars",
            ],
        )

        context = browser.new_context(
            viewport=viewport,
            record_video_dir=str(output_dir),
            record_video_size=record_size,
            color_scheme=color_scheme,
        )

        page = context.new_page()

        # Inject styling for custom element spotlights
        page.add_init_script(
            f"""
            const style = document.createElement('style');
            style.textContent = `{GOLD_ACCENT_CSS}`;
            document.head.appendChild(style);
        """
        )

        print(f"Navigating to {url} ({aspect_ratio})...")
        if url.startswith("http://") or url.startswith("https://"):
            page.goto(url, wait_until="networkidle", timeout=30000)
        else:
            page.goto(f"file://{Path(url).resolve()}", wait_until="load")

        # Initial stabilize wait
        page.wait_for_timeout(1500)

        if recipe_path and recipe_path.exists():
            recipe_data = json.loads(recipe_path.read_text(encoding="utf-8"))
            recipe_actions = recipe_data.get("actions", [])
            print(f"Running {len(recipe_actions)} recipe actions...")
            execute_action_recipe(page, recipe_actions)
        else:
            # Default fallback walkthrough: smooth downward scroll and pause
            print(f"Recording default {duration_seconds}s scroll session...")
            total_steps = max(1, int(duration_seconds * 2))
            for _ in range(total_steps):
                page.mouse.wheel(0, 150)
                page.wait_for_timeout(500)

        # Final buffer
        page.wait_for_timeout(1000)

        # Close page to flush video
        video_obj = page.video
        video_path_raw = video_obj.path() if video_obj else None

        page.close()
        context.close()
        browser.close()

        if video_path_raw and os.path.exists(video_path_raw):
            final_path = Path(video_path_raw)
            print(f"Screen capture recorded successfully: {final_path}")
            return final_path
        else:
            print("Video recorded in output directory.")
            return output_dir


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Automated screen capture engine using Playwright"
    )
    parser.add_argument("url", help="URL or local HTML file path to capture")
    parser.add_argument(
        "--output-dir",
        default="workspace/captures",
        help="Directory to save video captures (default: workspace/captures)",
    )
    parser.add_argument(
        "--format",
        choices=["16:9", "9:16"],
        default="16:9",
        help="Aspect ratio (default: 16:9 for YT Longs, 9:16 for Shorts/X)",
    )
    parser.add_argument(
        "--recipe",
        default=None,
        help="Path to JSON action recipe file with step-by-step actions",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Duration in seconds if no recipe provided (default: 10)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in visible mode (default is headless)",
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help="Preferred browser color scheme (default: dark)",
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    target_output = ROOT / args.output_dir
    recipe_file = (ROOT / args.recipe) if args.recipe else None

    record_screen(
        url=args.url,
        output_dir=target_output,
        aspect_ratio=args.format,
        recipe_path=recipe_file,
        duration_seconds=args.duration,
        headless=not args.headed,
        color_scheme=args.theme,
    )


if __name__ == "__main__":
    main()
