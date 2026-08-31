# Long-Form Video Structure (canonical template)

Noah teaches from first principles: high-level goal first, then build up slowly.
Scripts are BEAT OUTLINES — what to explain, how to explain it simply, what to
show, when. Noah speaks naturally from the outline; never word-for-word.

## The arc (Noah's flow, mandatory order)

1. **HOOK + HIGH-LEVEL GOAL (0:00-0:40)** — what we build, where we're going, why it matters. One simple sentence on the destination. No unexplained terms.
2. **SETUP + DEPENDENCIES (0:40-1:30)** — project folder, Python env, what we install and why. Show real commands `[CODE]`.
3. **ARCHITECTURE VISUAL (1:30-3:00)** — the whole system as a diagram BEFORE any code: components, what fits where. Mermaid flow + Excalidraw `[EXCALIDRAW]`. Point at each component, say what it does in one simple line.
4. **PLAN + REVIEW PLAN (3:00-3:45)** — state the build order, review it out loud ("step 1, then 2, then 3 — because X"). Show the plan on screen or whiteboard.
5. **CODE (3:45 → ~85% of video)** — build piece by piece, in the planned order. Every term defined before use. Concept segments: ~40-50s each, diagram-first. `[CODE]` / `[SCREEN]`.
6. **TEST (last ~90s before demo)** — run it. Show real output. If it fails, that's content: explain the failure, fix, re-run.
7. **ITERATE** — if something can be better (or A/B test), do it on camera. Show before/after.
8. **FINAL DEMO + RESULTS (last ~60s)** — the completed thing, live, with numbers captured on screen. Never fake.
9. **RECAP + CTA** — one-line summary, series nudge, subscribe/comment ask.

## Video modes

**Deep Build** — the arc above (setup → code → demo). For lessons and builds.

**High-Level Overview** — for module overview videos (the default for course
modules): explain the topic, not the code. Arc:
1. **HOOK (0:00-0:15)** — the pain this module solves, one punchy line
2. **WHAT + WHY (0:15-0:60)** — what this module is, why it matters, who it's for
3. **KEY CONCEPTS (0:60 → ~85%)** — one concept per segment, ~40-50s each,
   diagram-first, defined from zero (e.g. Module 03: "what is BM25", "why
   keyword search first", "precision vs recall")
4. **DEMO GLIMPSE (last ~60s before CTA)** — 20-30s of the real thing, no deep
   dive ("this is what you'll build in the course")
5. **COURSE CTA** — "this is module 3 of 7 — production agentic RAG from
   scratch, free, link below", subscribe/comment ask

## Rules

- **Build-up rule:** never use a term before explaining it. New concept → 40-50s segment with a diagram.
- **Diagram before code.** The architecture visual (step 3) always precedes the build.
- **Beat outline format** in every script:
  ```
  ## Beat <N> — <concept name>
  [time] [VISUAL] [CAM|CODE|SCREEN|EXCALIDRAW]
  WHAT: one-line concept, grade-5 words
  HOW: build-up steps (define terms first), analogy if useful
  SHOW: what appears on screen (code snippet, diagram element, terminal output)
  WHEN: trigger for this beat (after previous beat's result)
  ```
- **Results are captured live** during filming — never script fake numbers.
- One concept per segment. If a segment needs two concepts, split it.

## Mermaid + Excalidraw (all diagrams in one file)

- Director writes ONE `diagrams.md` per video: mermaid flow (architecture, plan)
  + one excalidraw spec per `[EXCALIDRAW]` beat. Reused by the deck
  (`skill/templates/deck.html`) and attached to the GitHub repo with the code.
- Diagrams live with the code: `outputs/<slug>/diagrams/` + `05_code/` — the
  GitHub repo for the video carries markdown flow + mermaid + excalidraw.
