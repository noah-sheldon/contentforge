"""Filter Agent -- persona-aware filtering + complexity scoring.

S: Single responsibility -- filters research data. Does not generate topics.
O: New guardrail = new function. Topic engine never changes.
"""

import re

from config.settings import load_persona


def niche_filter(data: dict) -> dict:
    """Filter research results to only AI/ML engineering niche topics."""
    persona = load_persona()
    niche = persona["content"]["niche"].lower()
    keywords = niche.replace(",", "").split()

    filtered = {}
    for source, results in data.items():
        if not results:
            filtered[source] = []
            continue
        kept = []
        for r in results:
            title_lower = r.title.lower()
            # Keep if any niche keyword matches
            if any(k in title_lower for k in keywords):
                kept.append(r)
        filtered[source] = kept

    return filtered


def complexity_score(text: str) -> int:
    """Score content complexity from 1-10. Lower = simpler.

    Rules:
    - Count technical terms (RAG, LangGraph, vectorstore, etc.)
    - Count long words (>3 syllables)
    - Rate 1-10
    """
    tech_terms = [
        "rag",
        "llm",
        "langgraph",
        "vectorstore",
        "embedding",
        "retrieval",
        "pipeline",
        "architecture",
        "deployment",
        "infrastructure",
        "kubernetes",
        "docker",
        "api",
        "fine.tune",
        "token",
        "latency",
        "throughput",
        "orchestration",
        "agent",
        "workflow",
    ]

    text_lower = text.lower()
    term_count = sum(1 for t in tech_terms if re.search(t, text_lower))

    # Estimate grade level from word length
    words = text_lower.split()
    long_words = sum(1 for w in words if len(w) > 8)

    score = min(10, max(1, term_count + long_words // 3))
    return score


def complexity_check(topics: list[dict], max_score: int = 4) -> list[dict]:
    """Remove topics above max complexity score."""
    return [t for t in topics if t.get("complexity_score", 10) <= max_score]


def format_filter(data: dict) -> dict:
    """Filter research to only text-friendly formats."""
    # Currently no format filter -- all research is text-based
    return data
