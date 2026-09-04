"""Animation Director — LLM reads script, chooses visual block types.

S: Single responsibility — analyzes content, outputs block structure.
D: Depends on SynthesizerInterface. Swappable.
O: New block type = add to prompt + create HyperFrames block template. Director code never changes.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona, load_prompt

# ─── Models ───────────────────────────────────────────────────────────


@dataclass
class Block:
    """A visual block in the animation. Type determines which HyperFrames template renders it."""

    type: str  # "text_card" | "code_block" | "diagram" | "comparison" | "metric" | "quote"
    duration_seconds: float
    data: dict  # Type-specific payload (heading, body, code, nodes, etc.)


# ─── Director ─────────────────────────────────────────────────────────


class AnimationDirector:
    """Reads a script body, returns a structured block sequence.

    Usage:
        director = AnimationDirector()
        blocks = director.direct(hook="Building RAG", body="...")
    """

    def __init__(self, llm: Optional[OpenAISynthesizer] = None):
        self.llm = llm or OpenAISynthesizer(thinking=True)

    def direct(
        self,
        hook: str,
        body: str,
        total_duration: float = 15.0,
        brand_colors: Optional[dict] = None,
    ) -> list[Block]:
        """Analyze script and return optimal block sequence.

        brand_colors: optional token -> hex mapping. Defaults to persona.yaml.
        """
        if brand_colors is None:
            persona = load_persona()
            brand = persona.get("brand", {})
            brand_colors = {
                "obsidian": brand.get("colors", {}).get("obsidian", "#12141C"),
                "alabaster": brand.get("colors", {}).get("alabaster", "#FAFAFA"),
                "gold": brand.get("colors", {}).get("gold", "#D4AF37"),
                "silentGray": brand.get("colors", {}).get("silent_gray", "#6B7280"),
            }

        prompt = load_prompt(
            "story/animation_director",
            hook=hook,
            body=body,
            brand_colors=json.dumps(brand_colors, indent=2),
        )

        raw = self.llm.synthesize(prompt, temperature=0.4)
        return self.parse(raw, total_duration)

    def parse(self, raw: str, total_duration: float) -> list[Block]:
        """Parse LLM JSON response into Block list. Normalizes durations to fit total."""
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            print("Animation director returned no valid JSON")
            return self.fallback(raw, total_duration)

        try:
            data = json.loads(match.group())
        except json.JSONDecodeError as e:
            print(f"Animation director JSON parse failed: {e}")
            return self.fallback(raw, total_duration)

        raw_blocks = data.get("blocks", [])
        if not raw_blocks:
            return self.fallback(raw, total_duration)

        # Parse blocks
        blocks = [
            Block(
                type=b["type"],
                duration_seconds=float(b.get("duration_seconds", 4)),
                data=b.get("data", {}),
            )
            for b in raw_blocks
        ]

        # Normalize durations to fit total_duration
        raw_total = sum(b.duration_seconds for b in blocks)
        if raw_total > 0:
            scale = total_duration / raw_total
            for b in blocks:
                b.duration_seconds = round(b.duration_seconds * scale, 1)

        return blocks

    def fallback(self, raw: str, total_duration: float) -> list[Block]:
        """Fallback: treat entire body as a single text_card block."""
        lines = raw.strip().split("\n")
        hook = lines[0][:60] if lines else "Content"
        body = " ".join(lines[1:])[:120] if len(lines) > 1 else raw[:120]
        return [
            Block(
                type="text_card",
                duration_seconds=total_duration,
                data={
                    "heading": hook,
                    "body": body,
                },
            )
        ]

    def print_blocks(self, blocks: list[Block]):
        """Pretty-print block sequence to terminal."""
        print("\n" + "=" * 50)
        print("🎬  ANIMATION BLOCKS")
        print("=" * 50)
        total = sum(b.duration_seconds for b in blocks)
        for i, b in enumerate(blocks, 1):
            icon = {
                "text_card": "📝",
                "code_block": "💻",
                "diagram": "🔷",
                "comparison": "⚖️",
                "metric": "📊",
                "quote": "💬",
            }.get(b.type, "📦")
            print(f"\n  {icon}  Block {i}  ({b.duration_seconds}s)  [{b.type}]")
            for key, val in b.data.items():
                if isinstance(val, str) and len(val) > 80:
                    val = val[:80] + "..."
                print(f"      {key}: {val}")
        print(f"\n{'─' * 50}")
        print(f"  Total: {total:.1f}s / {len(blocks)} blocks")
        print("=" * 50)


# ─── Standalone test ──────────────────────────────────────────────────

if __name__ == "__main__":
    from dotenv import load_dotenv

    from config.settings import ENV_PATH

    load_dotenv(ENV_PATH)

    director = AnimationDirector()
    blocks = director.direct(
        hook="Building RAG at Scale",
        body="I've spent 6 months building production RAG pipelines.\n"
        "The biggest lesson: chunking strategy matters more than the model.\n"
        "Semantic chunking with overlapping windows gave us a 40% lift in retrieval accuracy.\n"
        "Here's the code: vectorstore.similarity_search(query, k=5)",
    )
    director.print_blocks(blocks)
