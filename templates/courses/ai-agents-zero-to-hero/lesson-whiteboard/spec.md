# lesson-whiteboard — Teaching Template (Module 1)

Hand-drawn whiteboard explainer for conceptual lessons. **Owner:** Module 1 (all 7 lessons). Faceless — full-screen animated cards are the content; VO drives every reveal.

## Primitives

- `.wcard` — hand-drawn card (rough border-radius, slight baked rotation on `.wcard-inner`). Use for concepts, comparisons, definitions.
- `.big-symbol` — display-font symbol (≠, +, →, =) for comparisons.
- `svg path` + `drawOn` — self-sketching strokes (underlines, arrows, loops).
- `.bullet` — speech-timed bullet rows (takeaway scenes).
- `.formula` — one-line takeaway formula.
- `.takeaway-card` — closing card for the lesson's core statement.

## Scene structure (30-90s lessons)

| Scene | Time | Content |
|---|---|---|
| Hook | 0-4s | Title lockup + module tag (cover frame ~1.2s — hook fully landed) |
| Beat 1..n | 4 → | One idea per beat. Diagram-first: card/stroke appears at the exact second the VO says it |
| Takeaway | last ~11s | Formula + 2-3 speech-timed bullets |
| Outro | last ~5s | Lockup + rotating CTA |

## Build a lesson

1. Copy this template to `workspace/courses/<date>_m#l#/`.
2. Write the script as a **beat outline** — what/how/show/when per beat, never word-for-word. One idea per segment, define every term before use.
3. Noah records VO from the outline. Transcribe with word timestamps (whisper).
4. Map each beat's spoken time to a second → set every `beatIn`/`drawOn` `at` value from that mapping.
5. Replace demo scenes with the lesson's cards/diagrams. Keep hook lockup, corner brand, outro.
6. `npm run check` → snapshot QA → render (CRF 10 master → CRF 14 social).

## Production rules

Read `docs/course/lesson-production.md` before building — scene architecture, audio pipeline, sync workflow, visual-fit rules, rotation, and QA gates (hard-won on M1L1-M1L6).

## Kit sync

Tokens, brand blocks, and the reveal engine are inlined from `../shared/`. When the kit changes, regenerate the inline blocks — do not edit inline copies directly.

## Through-line anchor (M1L1 pattern)

Lessons that build a formula across beats (M1L1: `AGENT = LLM + ? + ?` → `+ LOOP + ?` → `+ LOOP + TOOLS`) keep **one persistent element** in a dedicated overlay clip (its own `data-track-index`) spanning all the beats, stepping states via text replacement at speech times. Never respawn the equation per beat — the build-up story dies if the anchor resets.

## Before render

- Bundle `Playfair Display`, `Caveat`, `Inter` as local `fonts/*.woff2` (registry rule — no remote font loading).
- Log the fingerprint in `docs/post-tracker.md` (format in `../shared/rotation.md`).
