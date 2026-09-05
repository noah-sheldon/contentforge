---
name: content-planner
description: Turn ANY input — YouTube video/playlist, blog, website, audio file, or pasted text — into short-form + long-form content ideas, researched briefs, scripts in Noah's voice, storyboards with equipment call sheets, teleprompter text, and 7/14-day publishing plans synced to GitHub Projects boards (7=short, 8=long).
version: 2.2.0
updated: 2026-09-05
changelog:
  - 2.2.0: "ASSETS stage (5b) — parallel web capture of every page a script references + per-video asset_manifest.md the video agent stages from (long + short form)"
  - 2.1.0: "Course-builder workflow + course.yaml template (no hardcoding)"
  - 2.0.0: "High-level overview video mode + course-module source (skip INGEST)"
  - 1.1.0: "Agentic RAG series pipeline; quickstart + workspace auto-README"
  - 1.0.0: "Initial — ingest-to-boards content pipeline"
---

# Content Planner

Orchestrates the full pipeline. Every stage reads/writes from this repo (`content-planner/`); `../../config/persona.yaml` is the single source of truth for voice, goals, and platform strategy.

## When used

User pastes a URL, file path, or text and asks to plan content from it. Or asks to continue/produce a stage for an existing `library/<slug>/` source. Or asks for content from a course module: the source is a module README (e.g. `../production-agentic-rag-from-scratch/modules/03-keyword-search-bm25/README.md`) — **skip INGEST**, the module README IS the source; ANALYZE reads it directly.

## Pipeline

```
[1] INGEST     python/scripts/ingest.py <input>        -> library/<slug>/raw_transcript.md + metadata.json
[2] ANALYZE    agent  (agents/analyze.md)      -> outputs/<slug>/analysis.md + parsed_concepts.json
[2b] MARKETING agent  (agents/marketing.md)    -> outputs/<slug>/platform_playbook.md
[3] IDEATE     agent  (agents/ideate.md)       -> outputs/<slug>/ideas.md + ideas.json
[4] RESEARCH   agents in parallel (agents/research.md) -> outputs/<slug>/research/<idea>.md
[5] SCRIPT     agent  (agents/script.md)       -> outputs/<slug>/script_longform.md,
                                                   script_shorts.md, teleprompter.txt
[5a] REVIEW    agent  (agents/review.md)       -> outputs/<slug>/fact_check.md
                (gate: must PASS before 5b)
[5b] ASSETS    agent  (agents/assets.md)       -> outputs/<slug>/assets/asset_manifest.md
                + python/scripts/capture_assets.py outputs/<slug>/assets/sites.json \
                    --out outputs/<slug>/assets/web --workers 3
                (pages captured in parallel -> web/<slug>/{webm,pngs}; walled pages first
                 retried headed real Chrome (--headed), else queued to Noah's own browser
                 — manual drop)
[5c] DIRECTOR  agent  (agents/director.md)     -> outputs/<slug>/storyboard.md + diagram specs
                (generated into the video's workspace/03_diagrams/ at materialize time)
[6] PLAN       agent  (agents/plan.md)         -> calendar/<Wxx>_plan.md + calendar/items.json
                then: python3 python/scripts/board.py --project 7|8 --owner noah-sheldon calendar/items.json
```

## Rules

1. **Voice is mandatory** — every script/caption must follow `../../config/voice.md`: spoken-flow register (multi-clause, or-chains, rhetorical questions), Indian English, no jargon, no marketing voice, must read human-written. ICP = AI engineers (junior/beginner, 0-3 yrs) — explainer content (benchmarks, evals, AGI, autonomy) uses define-from-zero mode from voice.md (state what something does before quoting any result). No "short sentences, one idea per line" — that rule was removed from voice.md (short lines are the caption register only).
2. **No fabrication** — research briefs cite sources; when facts can't be verified, say so.
3. **One card per video** on the boards (shorts → project 7, long-form → project 8); update card status as stages complete.
4. **Platform profiles, not separate pipelines** — one asset, per-platform variants (caption/hashtags/CTA/aspect).
5. **Batch filming** — plans group shorts + long-form into batch filming days, not daily filming.
6. **Visual tags** in every script beat: `[EXCALIDRAW] [CODE] [SCREEN] [CAM]` — the director maps them to OBS scenes.
7. **Code only for deterministic, stable mechanics** — `python/scripts/` holds just the glue (ingest, diagram, board, workspace) that never changes per-run. Everything creative is an agent (`skill/agents/*.md`); everything configurable lives in `config.yaml` / `../../config/persona.yaml`. If a script's logic would change per run, it belongs in an agent instead.
8. **Originality — never re-tell the source.** Ingested material is raw material for gaps, angles, and verified facts ONLY. No copied framing, structure, code, or examples from the source — in scripts, storyboards, demos, or demo code. Every build is Noah's own, written from scratch, tested by him, said in his words. If an idea is "the source explained again", kill it.
9. **User topics win — Noah's topics are the curriculum.** When he provides topics (e.g. "framework vs from scratch — trade-offs", "what's an agent loop"), build research/scripts/storyboards around HIS topics. Skip IDEATE when topics are given; gap-ideas are fillers he can reject, never substitutes.
10. **Assets are a stage, not an afterthought** — every beat that shows a real page/post/browser view needs an asset: WEB (live webm — footage) / POST (replica card or real capture) / MOTION (built by the video agent). The ASSETS stage (5b) derives its list from the script + fact base, captures pages in parallel, and queues bot-walled pages for Noah's own browser (manual drop). Chapters without a WEB/POST capture must carry an explicit MOTION note — the video agent never improvises a static screenshot.

## Stage prompts

Load the prompt from `skill/agents/<stage>.md`, spawn a sub-agent with it (parallel where independent: ANALYZE + MARKETING can run together; RESEARCH agents run in parallel per idea; ASSETS runs after REVIEW passes and captures its pages in parallel). Pass the agent exact file paths and tell it to read `../../config/persona.yaml` + `../../config/voice.md` as needed. Agents write output files; the orchestrator (you) runs the Python scripts.

**Course building (separate workflow):** `agents/course-builder.md` generates/updates the course repo from `templates/course.yaml` — no hardcoding, Six Beats pattern, same build-first rules. Used when writing future courses, not for video content.

## Outputs of a full run

- `outputs/<slug>/analysis.md`, `parsed_concepts.json`
- `outputs/<slug>/platform_playbook.md`
- `outputs/<slug>/ideas.md`, `ideas.json`
- `outputs/<slug>/research/<idea>.md`
- `outputs/<slug>/script_longform.md`, `script_shorts.md`, `teleprompter.txt`
- `outputs/<slug>/storyboard.md`
- `outputs/<slug>/assets/asset_manifest.md` + `assets/sites.json` + `assets/web/<slug>/*.{webm,png}`
- `workspace/.../03_diagrams/*.excalidraw` (generated per video)
- `calendar/<Wxx>_plan.md` + board cards created
