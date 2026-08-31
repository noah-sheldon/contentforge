"""Research orchestrator — runs scrapers, filters, topic engine, review loop.

S: Single responsibility — coordinates research pipeline. Doesn't scrape directly.
O: New research step = new module. Orchestrator never changes.
"""

from agents.research.filter import format_filter, niche_filter
from agents.research.review_agent import ResearchReview
from agents.research.topic_engine import run_topic_engine
from agents.search.duck_duckgo import DuckDuckGoSummarizer
from agents.search.x import XScraper
from agents.search.youtube import YouTubeScraper
from agents.synthesis.openai import OpenAISynthesizer
from config.settings import load_persona, load_prompt


def run_all_scrapers() -> dict:
    """Run YouTube API + X API + DuckDuckGo. Returns raw results."""
    print("Research phase -- scraping sources...")

    youtube = YouTubeScraper()
    x = XScraper()
    web = DuckDuckGoSummarizer()

    print("  YouTube...", end=" ", flush=True)
    yt = youtube.search("AI engineering machine learning production")

    print("  X...", end=" ", flush=True)
    xr = x.search("AI ML engineering langgraph RAG")

    print("  DuckDuckGo (LinkedIn, Threads)...", end=" ", flush=True)
    ddg = web.search("trending AI engineering topics this week")

    print("done")
    return {"youtube": yt, "x": xr, "web": ddg}


def run_research():
    """Full research pipeline: scrape -> filter -> synthesise -> topic engine -> review.

    Returns:
        dict with 'synthesis' (str) and 'topics' (list[dict])
    """
    from agents.research.filter import complexity_score

    # Phase 1: Scrape
    raw = run_all_scrapers()

    # Phase 2: Filter by niche
    filtered = niche_filter(raw)
    filtered = format_filter(filtered)

    # Phase 3: LLM synthesis
    persona = load_persona()
    content = persona["content"]

    yt_block = (
        "\n".join(
            f"- [{r.engagement.get('views', 0):>6} views] {r.title} ({r.metadata.get('channel', '?')})"
            for r in filtered["youtube"][:8]
        )
        or "No YouTube results."
    )

    x_block = (
        "\n".join(
            f"- [{r.engagement.get('likes', 0):>4} likes] {r.title[:100]}"
            for r in filtered["x"][:10]
        )
        or "No X results."
    )

    web_block = "\n".join(f"- {r.title}" for r in filtered["web"][:8]) or "No web summaries."

    print("  Synthesising trends...", end=" ", flush=True)
    llm = OpenAISynthesizer()
    raw = llm.synthesize(
        load_prompt(
            "research/synthesis",
            youtube_data=yt_block,
            x_data=x_block,
            web_data=web_block,
        ),
        system=f"You are a content strategist for {persona['creator']['name']}, {persona['creator']['title']}. "
               f"Niche: {content['niche']}. Audience: {content['audience']}. Tone: {content['tone']}. "
               f"Output JSON only. No explanation.",
        temperature=0.5,
    )
    # Parse JSON synthesis
    import json
    import re
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    synthesis = json.loads(match.group()) if match else []
    print("done")

    # Phase 4: Topic engine (novelty + complexity)
    print("  Generating topics...", end=" ", flush=True)
    research_for_engine = {
        "youtube": filtered["youtube"],
        "x": filtered["x"],
        "web": filtered["web"],
        "synthesis": synthesis,
    }
    topics = run_topic_engine(research_for_engine)
    print(f"{len(topics)} generated")

    # Phase 5: Review loop
    print("  Reviewing topics...", end=" ", flush=True)
    reviewer = ResearchReview()
    approved = reviewer.run(topics)
    print(f"{len(approved)} approved")

    # Score each for output
    for t in approved:
        t["complexity_score"] = complexity_score(t.get("topic", ""))

    return {
        "synthesis": synthesis,
        "topics": approved[:3],
        "raw_count": {
            "youtube": len(raw.get("youtube", [])),
            "x": len(raw.get("x", [])),
            "web": len(raw.get("web", [])),
        },
    }
