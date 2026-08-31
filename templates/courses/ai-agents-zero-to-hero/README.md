# AI Agents Zero→Hero — Course Template Family

Template family for the "AI Agents Zero→Hero" short-form teaching course (LangGraph series, 4 modules, 24 lessons). All three templates share one kit so every lesson reads as one course.

## The family

| Template | Covers | Primitives |
|---|---|---|
| `lesson-whiteboard/` | M1 — conceptual (7 lessons) | Hand-drawn cards, self-sketching strokes, comparisons, the agent loop |
| `lesson-graph/` | M3 + M4L9 — LangGraph (6 lessons) | Nodes, edges, state pill, animated graph construction |
| `lesson-code/` | M2 + M4 build (8 lessons) | Code cards, line-by-line reveal, terminal chrome, output panels |

## Shared kit (`shared/`)

| File | What it is |
|---|---|
| `tokens.css` | Canonical design tokens — brand fonts, obsidian/gold palette (persona.yaml), FONT_SCALE, spacing. Inlined into each template's `<style>`. |
| `brand.html` | Canonical title lockup (AI AGENTS / ZERO → HERO / using LangGraph), corner brand, outro. Inlined into each template. |
| `reveal-engine.js` | Speech-timed beat helpers (`beatIn`, `drawOn`). Inlined into each template's `<script>`. |
| `rotation.md` | Course-mode rotation policy — fixed vs rotated dimensions, through-line anchor pattern, fingerprint log format. |
| `brand.md` | The single course palette — obsidian + gold, usage rules, module-via-tag-text rule. |

**Sync rule:** the kit is inlined into each `index.html`. When the kit changes, regenerate the inline blocks from the canonical source in `shared/` (do not edit inline copies directly).

## How a lesson is built

1. Copy the owning template into a per-lesson project (e.g. `workspace/courses/2026.08.11_m1l1/`). The copy carries the inlined kit.
2. Write the script as a **beat outline** (first-principles style — what/how/show/when), never word-for-word. See `spec.md` of the template.
3. Noah records the VO from the outline; transcribe with word timestamps.
4. Map each beat to a second in the composition; drive every reveal from those times (`beatIn`).
5. Replace demo scenes with lesson content. Keep the hook lockup, corner brand, and outro structure.
6. `npm run check`, snapshot QA, `npm run render` (CRF 10 master → CRF 14 social).

## Build order

1. `lesson-whiteboard` — validated by building M1L1 (in progress at scaffold time).
2. `lesson-graph` — build when M3L1 arrives; swap in node/edge primitives.
3. `lesson-code` — build when M2L1 arrives; swap in code primitives.

Never render with un-bundled fonts: the registry rule requires local `fonts/*.woff2` before render. The demo stacks fall back to system fonts; bundle `Playfair Display`, `Caveat`, `JetBrains Mono` before shipping a lesson.
