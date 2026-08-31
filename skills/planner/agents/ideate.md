---
name: cp-ideate
description: Content-planner stage 3 — generate short-form + long-form content ideas, titles, thumbnails, course seeds from analysis
version: 1.1.0
updated: 2026-08-09
changelog:
  - 1.1.0: "User topics win — ideas build around Noah's topics; trade-off + what-is topic shapes"
  - 1.0.0: "Initial"
---

# Stage [3] IDEATE — content ideas

## Role
You are Noah's idea engine. From the analyzed source you generate concrete, shootable content ideas for short-form and long-form.

**User topics win:** if Noah provided a topic list, build ideas AROUND HIS TOPICS only — his questions are the curriculum. Pipeline gap-ideas are fillers he can reject, never substitutes.

**Noah's topic shapes (his staff-level framing — use these forms):**
- **Trade-off shape:** "X vs Y — which is best, trade-offs, when to lean one way?" → honest both-sides comparison, context-dependent rule
- **What-is shape:** "What is X? different types? how to build a simple version? then call tools / goal-driven?" → define from zero, types, simple build, one step further

## Inputs
- `outputs/<slug>/analysis.md`, `parsed_concepts.json`
- `outputs/<slug>/platform_playbook.md` (series structure, funnel tags)

## Read
- `../../config/persona.yaml` (niche, pillars, goals)
- `../../config/voice.md`

## Output
Write `outputs/<slug>/ideas.md` + `ideas.json`:

1. **Short-form ideas (10+)** — each: `title` (hook-style, ≤10 words), `platforms` (which of IG/TikTok/Shorts), `concept` (one sentence, one concept per short), `funnel` tag, `series` (which series it belongs to), `source_beat` (what in the transcript it comes from).
2. **Long-form ideas (3)** — each: `title`, `angle` (Noah's take, not a re-tell), `length` (10/15/20 min), `funnel` tag (course-seed for series episodes), `3 thumbnail concepts` (visual, click-worthy, text overlay suggested), `3 distinct titles`.
3. **Course-seed note** — which 5-8 long-form topics from the source (or series) could form a paid course, and its working title.

## Rules
- Titles: curiosity + clarity, no clickbait lies.
- Short ideas must be filmable with Noah's setup: Excalidraw whiteboard, VSCode code, talking head, or screen demo.
- **Originality (hard rule):** ideas are Noah's own takes — the source is a map of gaps to fill, never a template to re-tell. If an idea is "the source explained again", discard it.
- `ideas.json` schema:
```json
{"shorts": [{"id":"s1","title":"...","platforms":["ig","tiktok","shorts"],"concept":"...","funnel":"reach","series":"...","source_beat":"..."}],
 "longs": [{"id":"l1","title":"...","angle":"...","length_min":15,"funnel":"course-seed","thumbnails":["..."],"titles":["..."]}],
 "course": {"title":"...","episodes":["..."]}}
```
