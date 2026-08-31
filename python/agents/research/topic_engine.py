"""Topic Engine -- generates topics from research, checks history for novelty.

S: Single responsibility -- topic generation + novelty checking.
D: Depends on SynthesizerInterface.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona

HISTORY_PATH = Path(__file__).resolve().parent.parent.parent / "state" / "topic_history.json"


def load_history() -> list[dict]:
    """Load topic history from JSON."""
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH) as f:
        data = json.load(f)
        return data.get("topics", [])


def save_history(topics: list[dict]):
    """Append new topics to history."""
    existing = load_history()
    existing.extend(topics)
    with open(HISTORY_PATH, "w") as f:
        json.dump({"topics": existing}, f, indent=2)


def is_novel(topic: str, history: list[dict], days: int = 90) -> bool:
    """Check if topic is novel. False if similar topic used within days."""
    cutoff = datetime.now() - timedelta(days=days)
    topic_lower = topic.lower()

    for entry in history:
        entry_date = datetime.fromisoformat(entry["date"])
        if entry_date < cutoff:
            continue
        entry_topic = entry["topic"].lower()
        # Simple overlap check -- if 50%+ word overlap, reject
        topic_words = set(topic_lower.split())
        entry_words = set(entry_topic.split())
        if len(topic_words) == 0:
            continue
        overlap = len(topic_words & entry_words) / len(topic_words)
        if overlap > 0.5:
            return False
    return True


def generate_topics(research_data: dict, count: int = 5) -> list[dict]:
    """Generate topic ideas from research. Returns list with scores.

    Each topic: {"topic": str, "complexity_score": int, "source": str}
    """
    persona = load_persona()
    history = load_history()

    summary_lines = []
    for source, items in research_data.items():
        if isinstance(items, list):
            for item in items[:5]:
                title = getattr(item, "title", str(item))[:100]
                summary_lines.append(f"  [{source}] {title}")
        elif isinstance(items, str):
            summary_lines.append(f"  [{source}] {items[:100]}")

    summary = "\n".join(summary_lines) or "No research data available."

    prompt = (
        f"You are a content strategist for {persona['creator']['name']}, "
        f"{persona['creator']['title']}.\n\n"
        f"CONTENT PILLARS:\n"
        f"- Technical deep-dives: RAG, agents, LLMOps, production AI\n"
        f"- Engineering leadership: managing teams, hiring, career\n"
        f"- AI applications: building in public, demos, product thinking\n"
        f"- Career / hiring: AI job market, skills, team building\n\n"
        f"Audience: {persona['content']['audience']}\n"
        f"Tone: {persona['content']['tone']}\n\n"
        f"Research data from this week:\n{summary}\n\n"
        f"Propose {count} topics spanning MULTIPLE pillars. "
        f"Each must be simple (Grade 6), max 2 technical terms.\n\n"
        f"Previous topics (do not repeat):\n"
        + "\n".join(f"  - {h['topic']} ({h['date']})" for h in history[-10:])
        + "\n\n"
        "Output JSON only:\n"
        '{"topics": [{"topic": "string", "hook": "string", '
        '"complexity_score": 1-10, '
        '"pillar": "technical|leadership|applications|career|vlog", '
        '"format": "short_text|thread|article|video", '
        '"best_platform": "linkedin|x|threads|instagram|any", '
        '"reason": "why this topic in one sentence"}]}'
    )

    llm = OpenAISynthesizer(thinking=True)
    import json as j
    import re

    raw = llm.synthesize(prompt, temperature=0.7)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return []

    try:
        parsed = j.loads(match.group())
    except json.JSONDecodeError:
        return []

    topics = parsed.get("topics", [])
    for t in topics:
        t["source"] = "topic_engine"

    return topics


def run_topic_engine(research_data: dict) -> list[dict]:
    """Full pipeline: generate, check novelty, filter by complexity."""
    from agents.research.filter import complexity_check

    history = load_history()

    # Generate
    topics = generate_topics(research_data)

    # Novelty filter
    novel = [t for t in topics if is_novel(t["topic"], history)]

    # Complexity filter
    simple = complexity_check(novel, max_score=4)

    return simple[:3]  # Return max 3 topics
