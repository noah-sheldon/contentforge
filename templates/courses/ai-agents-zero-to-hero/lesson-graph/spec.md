# lesson-graph — Graph/Architecture Template (Modules 3 & 4)

Node/edge/state diagrams for LangGraph lessons. **Owner:** M3 (all 5 lessons) + M4L9 (subgraphs, parallel, time travel). Faceless — the graph IS the content; it builds live as the VO explains.

## Primitives

- `.state-pill` — the shared state (pill + hand-font value). Pulses/updates as state is discussed.
- `.gnode` — a node card (rounded rect, accent border). `gnode-title` + `gnode-note`.
- `svg path` + `drawOn` — directed edges with arrow markers; self-sketch on speech. Add more `<path>`s for loops/branching.
- `.edge-label` — hand-font label beside an edge ("decides", "observes", "repeats").
- Finite node pulse (`yoyo: true, repeat: 1`) to show the active node — never `repeat: -1`.

## Scene structure (30-90s lessons)

| Scene | Time | Content |
|---|---|---|
| Hook | 0-4s | Title lockup + module tag |
| Build | 4 → | State pill → nodes appear as named → edges draw as explained → labels |
| Takeaway | last ~7s | "State · nodes · edges" formula + bullets |
| Outro | last ~5s | Lockup + rotating CTA |

## Build a lesson

1. Copy this template to `workspace/courses/<date>_m#l#/`.
2. Beat-outline script (what/how/show/when), never word-for-word.
3. Noah records VO → transcribe with word timestamps → map beats to seconds → set every `at`.
4. Replace demo graph with the lesson's real graph (nodes/edges/state). Keep lockup, corner brand, outro.
5. `npm run check` → snapshot QA → render (CRF 10 master → CRF 14 social).

## Kit sync

Tokens, brand, reveal engine inlined from `../shared/` — regenerate inline blocks from canonical, never edit inline copies.

## Before render

- Bundle `Playfair Display`, `Caveat`, `Inter` as local `fonts/*.woff2`.
- Log the fingerprint in `docs/post-tracker.md` (format in `../shared/rotation.md`).
