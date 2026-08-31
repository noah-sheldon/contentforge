"""Research Review Agent -- self-review loop for topic quality.

S: Single responsibility -- validates topics. Does not generate.
O: New validation = new check function. Agent code never changes.
"""

import json
import re
from typing import Optional

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona


class ResearchReview:
    """Self-review loop for proposed topics. Max 3 cycles.

    Usage:
        review = ResearchReview()
        passed, notes = review.check(topic_data)
        if not passed:
            revised = review.regenerate(topic_data, notes)
    """

    def __init__(self, llm: Optional[OpenAISynthesizer] = None):
        self.llm = llm or OpenAISynthesizer(thinking=True)
        self.max_cycles = 1

    def check(self, topic: dict) -> tuple[bool, str]:
        """Evaluate a single topic. Returns (passed, notes)."""
        persona = load_persona()
        content = persona["content"]

        prompt = (
            f"Review this content topic for Noah Sheldon, "
            f"{persona['creator']['title']}.\n\n"
            f"TOPIC: {topic.get('topic', '')}\n"
            f"COMPLEXITY SCORE: {topic.get('complexity_score', 5)}/10\n\n"
            f"PERSONA:\n"
            f"- Niche: {content['niche']}\n"
            f"- Audience: {content['audience']}\n"
            f"- Tone: {content['tone']}\n\n"
            f"CHECKLIST:\n"
            f"1. Is this topic within AI/ML engineering? (yes/no)\n"
            f"2. Is the complexity appropriate for junior engineers? (max 2 technical terms)\n"
            f"3. Does the topic have a personal take or story angle? (not just generic news)\n"
            f"4. Can this topic be explained in under 30 seconds? (short attention span)\n\n"
            f"Output JSON only:\n"
            f'{{"passed": true/false, "notes": "specific fix instructions"}}'
        )

        raw = self.llm.synthesize(prompt, temperature=0.3)
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return True, ""

        try:
            result = json.loads(match.group())
        except json.JSONDecodeError:
            return True, ""

        return result.get("passed", True), result.get("notes", "")

    def regenerate(self, topic: dict, notes: str) -> dict:
        """Rewrite a topic based on review feedback."""
        prompt = (
            f"Rewrite this content topic based on the feedback below.\n\n"
            f"ORIGINAL TOPIC: {topic.get('topic', '')}\n"
            f"FEEDBACK: {notes}\n\n"
            f"Make it simpler, more specific, and more personal. "
            f"Output JSON only:\n"
            f'{{"topic": "string", "complexity_score": 1-10}}'
        )

        raw = self.llm.synthesize(prompt, temperature=0.6)
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return topic

        try:
            revised = json.loads(match.group())
            revised["source"] = "review_rewrite"
            return revised
        except json.JSONDecodeError:
            return topic

    def run(self, topics: list[dict]) -> list[dict]:
        """Run review loop on all topics. Returns only approved ones."""
        approved = []
        for topic in topics:
            current = topic
            for cycle in range(self.max_cycles):
                passed, notes = self.check(current)
                if passed:
                    approved.append(current)
                    break
                elif cycle < self.max_cycles - 1:
                    current = self.regenerate(current, notes)
                # else: max cycles reached, drop the topic

        return approved
