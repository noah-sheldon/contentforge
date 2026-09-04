"""Scene planning — script text to typed visual blocks.

Two strategies:
- llm: AnimationDirector reads the script and picks block types (prompt from
  the prompt registry, brand colors from tenant config).
- deterministic: offline fallback that chunks the script into text_card
  blocks. Used when no LLM key is available so the demo still renders.

P1 rule: scenes come from config + a generator, never hand-authored markup.
"""

from __future__ import annotations

import os

from agents.storyboard.animation_director import AnimationDirector, Block
from config.schema.tenant import TenantConfig

_TOTAL_DURATION_S = 16.0


class ScenePlanner:
    """Plans the visual scene list for one run's script text."""

    def __init__(self, use_llm: bool | None = None):
        self.use_llm = use_llm
        if self.use_llm is None:
            self.use_llm = bool(
                os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
            )

    def plan(self, script_text: str, tenant: TenantConfig) -> list[Block]:
        """Return the block sequence for a script in a tenant's brand."""
        script_text = script_text.strip()
        if not script_text:
            raise ValueError("Scene planning requires non-empty script text.")
        if self.use_llm:
            return self._plan_with_llm(script_text, tenant)
        return self._plan_deterministic(script_text)

    def _plan_with_llm(self, script_text: str, tenant: TenantConfig) -> list[Block]:
        director = AnimationDirector()
        hook = _first_sentence(script_text, limit=90)
        brand_colors = {
            "obsidian": tenant.brand.colors.get("obsidian", "#12141C"),
            "alabaster": tenant.brand.colors.get("alabaster", "#FAFAFA"),
            "gold": tenant.brand.colors.get("gold", "#D4AF37"),
            "silentGray": tenant.brand.colors.get("silent_gray", "#6B7280"),
        }
        blocks = director.direct(
            hook=hook,
            body=script_text,
            total_duration=_TOTAL_DURATION_S,
            brand_colors=brand_colors,
        )
        if not blocks:
            return self._plan_deterministic(script_text)
        return blocks

    def _plan_deterministic(self, script_text: str) -> list[Block]:
        sentences = [s.strip() for s in script_text.replace("\n", " ").split(".") if s.strip()]
        if not sentences:
            sentences = [script_text.strip()]
        per_block = 2
        groups = [sentences[i : i + per_block] for i in range(0, len(sentences), per_block)]
        duration = round(_TOTAL_DURATION_S / len(groups), 2)
        blocks: list[Block] = []
        for group in groups:
            first = group[0]
            rest = " ".join(group[1:])
            blocks.append(
                Block(
                    type="text_card",
                    duration_seconds=duration,
                    data={
                        "heading": first[:64] if len(first) > 48 else first,
                        "body": rest if rest else first,
                    },
                )
            )
        return blocks


def _first_sentence(text: str, limit: int) -> str:
    head = text.replace("\n", " ").strip()
    if "." in head:
        head = head.split(".", 1)[0]
    return head[:limit]
