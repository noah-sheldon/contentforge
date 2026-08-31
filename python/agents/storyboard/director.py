"""Storyboard Director — LLM generates scene-by-scene shot list from script.

S: Single responsibility — reads script, outputs shot list. Doesn't search. Doesn't render.
D: Depends on SynthesizerInterface. Swap GPT-4o for Claude without changes.
O: New shot list format = new prompt template. Director code never changes.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona, load_prompt

# ─── Models ───────────────────────────────────────────────────────────


@dataclass
class Scene:
    scene_number: int
    description: str
    duration_seconds: float
    camera_angle: str  # "talking_head" | "overhead" | "screen" | "broll"
    assets_needed: list[str]  # ["a_roll", "screen_rec", "code_img"]
    overlay_text: str
    sfx: str  # "ambient_office" | "keyboard" | "none"


@dataclass
class Storyboard:
    scenes: list[Scene]
    total_duration: float
    estimated_shoot_time: str


# ─── Director ─────────────────────────────────────────────────────────


class StoryboardDirector:
    """Takes a script body, returns a structured storyboard.

    Usage:
        director = StoryboardDirector()
        board = director.storyboard("Today we're building a RAG pipeline...")
    """

    def __init__(self, llm: Optional[OpenAISynthesizer] = None):
        self.llm = llm or OpenAISynthesizer(thinking=True)

    def storyboard(self, script_body: str, hook: str = "") -> Storyboard:
        """Generate shot list from script text."""
        persona = load_persona()
        brand = persona.get("brand", {})

        brand_colors = {
            "primary": brand.get("colors", {}).get("obsidian", "#12141C"),
            "accent": brand.get("colors", {}).get("gold", "#D4AF37"),
            "background": brand.get("colors", {}).get("alabaster", "#FAFAFA"),
        }

        prompt = load_prompt(
            "story/storyboard",
            script_body=script_body,
            brand_colors=json.dumps(brand_colors, indent=2),
        )

        raw = self.llm.synthesize(prompt, temperature=0.5)
        return self.parse(raw)

    def parse(self, raw: str) -> Storyboard:
        """Parse LLM JSON response into Storyboard object."""
        # Extract JSON from potential markdown code blocks
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("Storyboard LLM returned no valid JSON")

        try:
            data = json.loads(match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Storyboard LLM returned invalid JSON: {e}") from e

        scenes = [
            Scene(
                scene_number=s["scene_number"],
                description=s["description"],
                duration_seconds=float(s["duration_seconds"]),
                camera_angle=s.get("camera_angle", "talking_head"),
                assets_needed=s.get("assets_needed", ["a_roll"]),
                overlay_text=s.get("overlay_text", ""),
                sfx=s.get("sfx", "none"),
            )
            for s in data.get("scenes", [])
        ]

        return Storyboard(
            scenes=scenes,
            total_duration=float(data.get("total_duration", 59)),
            estimated_shoot_time=data.get("estimated_shoot_time", "4 hours"),
        )

    def print_storyboard(self, board: Storyboard):
        """Pretty-print a storyboard to terminal."""
        print("\n" + "=" * 60)
        print("🎬  STORYBOARD")
        print(f"    Total: {board.total_duration}s | Shoot: {board.estimated_shoot_time}")
        print("=" * 60)

        for scene in board.scenes:
            icon = {
                "talking_head": "🎙️",
                "overhead": "📷",
                "screen": "🖥️",
                "broll": "🎞️",
            }.get(scene.camera_angle, "🎬")

            assets = ", ".join(scene.assets_needed)
            print(
                f"\n  {icon}  Scene {scene.scene_number}  ({scene.duration_seconds}s)  [{scene.camera_angle}]"
            )
            print(f"      {scene.description}")
            print(f"      Assets: {assets}")
            if scene.overlay_text:
                print(f'      Overlay: "{scene.overlay_text}"')
            if scene.sfx and scene.sfx != "none":
                print(f"      SFX: {scene.sfx}")

        print("\n" + "=" * 60)


# ─── Standalone test ──────────────────────────────────────────────────

if __name__ == "__main__":
    from dotenv import load_dotenv

    from config.settings import ENV_PATH

    load_dotenv(ENV_PATH)

    # Example script
    test_script = (
        "Today I'm building a RAG pipeline with LangGraph. "
        "First, I set up the vector store with ChromaDB. "
        "Then I write the retrieval chain in LangGraph. "
        "Finally, I test it with some queries and show the results."
    )

    director = StoryboardDirector()
    board = director.storyboard(test_script, hook="Building RAG at Scale")
    director.print_storyboard(board)
