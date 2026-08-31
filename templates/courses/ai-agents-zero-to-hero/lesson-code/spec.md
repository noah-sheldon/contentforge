# lesson-code — Code/Build Template (Modules 2 & 4)

Code-first lessons: build scenes show real code revealing line-by-line as the VO explains, then the output. **Owner:** M2 (2 lessons) + M4 build lessons (L2, L3, L6-L8). Faceless — code cards are the content, with proper margins (never a full-bleed editor).

## Primitives

- `.code-panel` — bordered card, chrome bar (traffic dots + file name), generous padding. Code stays inside `--pad` margins.
- `.code-line` — one line per `<p>`, mono font, `white-space: pre`, syntax spans: `.kw` (keywords), `.str` (strings), `.fn` (functions). Reveal each line when spoken.
- `.cursor` — block cursor; blink with finite `tl.to` steps, never `repeat: -1`.
- `.output-panel` — second card below: `>>>` prompt + result lines. Appears after the code is read.

## Scene structure (30-90s lessons)

| Scene | Time | Content |
|---|---|---|
| Hook | 0-4s | Title lockup + module tag |
| Code | 4 → | Panel → lines reveal as read → cursor → output panel → caption |
| Takeaway | last ~7s | Formula + 2-3 bullets |
| Outro | last ~5s | Lockup + rotating CTA |

## Build a lesson

1. Copy this template to `workspace/courses/<date>_m#l#/`.
2. Beat-outline script (what/how/show/when), never word-for-word. Decide how many code lines each beat reveals.
3. Noah records VO → transcribe with word timestamps → map beats to seconds → set every `at`.
4. Replace demo snippet with the lesson's real code. Keep lockup, corner brand, outro.
5. `npm run check` → snapshot QA → render (CRF 10 master → CRF 14 social).

## Kit sync

Tokens, brand, reveal engine inlined from `../shared/` — regenerate inline blocks from canonical, never edit inline copies.

## Before render

- Bundle `Playfair Display`, `Inter`, `JetBrains Mono` as local `fonts/*.woff2`.
- Log the fingerprint in `docs/post-tracker.md` (format in `../shared/rotation.md`).
