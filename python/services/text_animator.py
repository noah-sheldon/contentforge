"""Text Animation Pipeline — AnimationDirector blocks → HyperFrames → MP4.

S: Single responsibility — renders text animations via HyperFrames.
O: New block type = add template clause here + register in animation_director prompt.
KISS: render_blocks() for dynamic blocks. render_linkedin_post() for legacy text.
DRY: Brand config from persona.yaml. Block logic from AnimationDirector.
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from agents.storyboard.animation_director import AnimationDirector, Block
from config.settings import PYTHON_ROOT, load_persona

OUTPUT_DIR = PYTHON_ROOT.parent / "output"

FPS = 30

# Block type → (heading tag, body renderer)
BLOCK_STYLES = {
    "text_card": ("block-title", "block-body"),
    "quote": ("block-quote", "block-body"),
    "code_block": ("block-code-title", "block-code"),
    "metric": ("block-metric", "block-metric-sub"),
    "comparison": ("block-compare-title", "block-compare-body"),
    "diagram": ("block-diagram-title", "block-diagram-body"),
}


def _build_composition(blocks: list[Block], brand: dict, fonts: dict) -> str:
    """Generate a standalone HyperFrames composition HTML from blocks."""
    colors = brand.get("colors", {})
    obsidian = colors.get("obsidian", "#12141C")
    alabaster = colors.get("alabaster", "#FAFAFA")
    gold = colors.get("gold", "#D4AF37")
    silent_gray = colors.get("silent_gray", "#6B7280")
    primary_font = fonts.get("primary", "Inter")
    mono_font = fonts.get("mono", "JetBrains Mono")

    total_duration = sum(b.duration_seconds for b in blocks)

    clips = []
    timeline = []
    t = 0.0
    for i, b in enumerate(blocks):
        dur = b.duration_seconds
        style = BLOCK_STYLES.get(b.type, BLOCK_STYLES["text_card"])
        data = b.data
        heading = data.get("heading", data.get("title", ""))
        body = data.get("body", data.get("text", ""))

        inner = ""
        if b.type == "code_block":
            code = data.get("code", body).replace("\n", "<br>")
            inner = f"""
        <div id="c{i}-h" class="block-code-title">{heading}</div>
        <pre id="c{i}-b" class="block-code">{code}</pre>"""
        elif b.type == "metric":
            value = data.get("value", heading)
            sub = data.get("subtitle", body)
            inner = f"""
        <div id="c{i}-h" class="block-metric">{value}</div>
        <div id="c{i}-b" class="block-metric-sub">{sub}</div>"""
        else:
            inner = f"""
        <div id="c{i}-h" class="{style[0]}">{heading}</div>
        <div id="c{i}-b" class="{style[1]}">{body}</div>"""

        clips.append(
            f"""
    <section id="clip{i}" class="clip" data-start="{t:.1f}" data-duration="{dur:.1f}" data-track-index="1">
      {inner}
    </section>"""
        )
        timeline.append(
            f"""
      tl.fromTo("#c{i}-h", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {t + 0.15:.2f});
      tl.fromTo("#c{i}-b", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {t + 0.5:.2f});"""
        )
        t += dur

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {obsidian}; }}
      body {{ font-family: "{primary_font}", sans-serif; color: {alabaster}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {obsidian}; }}
      .clip {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 0 80px; }}
      .block-title {{ font-size: 96px; font-weight: 800; line-height: 1.1; margin-bottom: 48px; }}
      .block-quote {{ font-size: 96px; font-weight: 700; line-height: 1.15; margin-bottom: 48px; color: {gold}; font-style: italic; }}
      .block-body {{ font-size: 48px; font-weight: 500; line-height: 1.45; color: {alabaster}; max-width: 900px; }}
      .block-code-title {{ font-size: 44px; font-weight: 700; color: {gold}; margin-bottom: 40px; }}
      .block-code {{ font-family: "{mono_font}", monospace; font-size: 40px; line-height: 1.5; background: rgba(255,255,255,0.06); border-radius: 16px; padding: 48px; color: {alabaster}; white-space: pre-wrap; }}
      .block-metric {{ font-family: "{mono_font}", monospace; font-size: 160px; font-weight: 800; color: {gold}; margin-bottom: 32px; }}
      .block-metric-sub {{ font-size: 44px; color: {silent_gray}; }}
      .block-compare-title {{ font-size: 72px; font-weight: 800; margin-bottom: 40px; }}
      .block-compare-body {{ font-size: 44px; line-height: 1.5; color: {alabaster}; }}
      .block-diagram-title {{ font-size: 72px; font-weight: 800; margin-bottom: 40px; }}
      .block-diagram-body {{ font-size: 44px; line-height: 1.5; color: {alabaster}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total_duration:.1f}" data-width="1080" data-height="1920">
      {''.join(clips)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {''.join(timeline)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def build_props(blocks: list[Block]) -> str:
    """Build block props (kept for API compatibility)."""
    persona = load_persona()
    brand = persona.get("brand", {})
    fonts = brand.get("fonts", {})
    return _build_composition(blocks, brand, fonts)


def render_blocks(blocks: list[Block], output_path: Optional[str] = None) -> str:
    """Render blocks from AnimationDirector as a 9:16 MP4 via HyperFrames.

    Args:
        blocks: List of Block objects from AnimationDirector.direct()
        output_path: Full path for output MP4. Auto-generated if None.

    Returns:
        Path to rendered MP4 file.
    """
    persona = load_persona()
    brand = persona.get("brand", {})
    fonts = brand.get("fonts", {})
    total_duration = sum(b.duration_seconds for b in blocks)

    html = _build_composition(blocks, brand, fonts)

    # Determine output path
    if output_path is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        existing = len(list(OUTPUT_DIR.glob("*.mp4")))
        output_path = str(OUTPUT_DIR / f"animation_{existing + 1}.mp4")

    print(f"  Rendering {len(blocks)} blocks, {total_duration:.1f}s → {total_duration:.1f}s @ {FPS}fps")
    print(f"  Output: {output_path}")

    with tempfile.TemporaryDirectory(prefix="hf_text_") as tmp:
        project = Path(tmp)
        (project / "index.html").write_text(html, encoding="utf-8")
        (project / "hyperframes.json").write_text(
            json.dumps({
                "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
                "authoringSkill": "general-video",
            }),
            encoding="utf-8",
        )
        (project / "meta.json").write_text(
            json.dumps({"id": "text-animation", "name": "text-animation"}),
            encoding="utf-8",
        )

        result = subprocess.run(
            ["npx", "hyperframes", "render", "--output", output_path],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise RuntimeError(f"HyperFrames render failed:\n{error_msg[:500]}")

    print(f"  Rendered: {output_path}")
    return output_path


def render_linkedin_post(
    hook: str,
    body: str,
    output_path: Optional[str] = None,
) -> str:
    """Render a LinkedIn-style post as a 15s animation.

    Uses AnimationDirector to dynamically select block types
    (text_card, code_block, diagram, comparison, metric, quote).
    """
    director = AnimationDirector()
    blocks = director.direct(hook=hook, body=body)
    return render_blocks(blocks, output_path)


# ─── Standalone test ──────────────────────────────────────────────────

if __name__ == "__main__":
    from dotenv import load_dotenv

    from config.settings import ENV_PATH

    load_dotenv(ENV_PATH)

    path = render_linkedin_post(
        hook="Building RAG at Scale",
        body=(
            "I've spent 6 months building production RAG pipelines at Fitch Ratings.\n\n"
            "The biggest lesson: chunking strategy matters more than the model.\n"
            "Semantic chunking with overlapping windows gave 40% lift in retrieval accuracy.\n\n"
            "Here's the code pattern:\n"
            "vectorstore = ChromaDB()\n"
            "retriever = vectorstore.as_retriever(search_kwargs={'k': 5})\n\n"
            "Result: 99.7% retrieval accuracy, 3x faster than baseline."
        ),
    )
    print(f"\n  Animation saved to: {path}")
