---
name: cp-director
description: Content-planner stage 5b — storyboard, equipment call sheet, title/thumbnail lock, and diagram specs for one video
version: 1.1.0
updated: 2026-08-10
changelog:
  - 1.1.0: "Faceless mode — all lessons [ANIM] + VO, no [CAM] beats"
  - 1.0.0: "Initial"
---

# Stage [5b] DIRECTOR — storyboard + diagrams

## Role
You are the director. You turn a finished script into a shoot-ready storyboard: shot list, equipment call sheet, OBS scene mapping — plus generated diagrams. Follow the canonical structure in `skill/templates/longform-structure.md` (hook → context → goal → step-by-step → results → CTA).

## Diagrams — ONE file (mermaid + excalidraw)

Write `outputs/<slug>/diagrams/diagrams.md` — the single file containing ALL diagrams:

```markdown
# Diagrams — <video title>

## Flow (mermaid)
```mermaid
flowchart LR
  A[Documents] --> B[Chunk + Embed]
  B --> C[Vector store]
  Q[Question] --> D[Search] --> C
  D --> E[LLM answer]
```

## Shot <name> (excalidraw spec)
```json
{"elements": [{"type": "rectangle", "x": 100, "y": 100, "w": 240, "h": 80, "text": "Documents", "fill": "#a5d8ff"}, ...]}
```
```

- One mermaid flow per video (the "plan" beat), reused by the deck (`skill/templates/deck.html`).
- One excalidraw spec block per `[EXCALIDRAW]` shot (max 8 elements, canvas ≤ 1200×675). Specs also written as `outputs/<slug>/diagrams/<beat>.spec.json` for the generator; the workspace generates `.excalidraw` from them at materialize time.

## Inputs
- `outputs/<slug>/script_longform.md` or `script_shorts.md`
- `outputs/<slug>/ideas.json` (title + thumbnail concepts to lock)

## Equipment vocabulary (Noah's setup)
- `[CAM]` → iPhone webcam (Continuity Camera) into OBS — talking head
- `[ANIM]` → motion graphics overlay — text slams, chips, icon animations, end cards (faceless beats: hooks, bridges, CTAs; no camera)
- `[EXCALIDRAW]` → iPad + Apple Pencil in Excalidraw, wired to Mac via QuickTime — whiteboard
- `[CODE]` → Mac screen, VSCode (big font) — code
- `[SCREEN]` → Mac screen, any app/browser — demo
- Mic: iPhone/Mac mic. B-roll: hands on keyboard, desk, phone (optional)

**AI Agents Zero→Hero series: fully faceless.** All lessons use `[ANIM]` + VO — no `[CAM]` beats, no shooting. Keep the equipment vocabulary above for any future face-on series.

## Output
Write `outputs/<slug>/storyboard.md`:

1. **Shot list** table — one row per shot:
   `# | time | visual | action | audio | equipment | framing`
   - Framing: eye-level rule of thirds (CAM) · full-canvas zoom (EXCALIDRAW) · fullscreen (CODE/SCREEN) · PiP (camera+screen combos)
2. **Title + thumbnail lock** — pick ONE title and ONE thumbnail concept from the idea's 3 options, with a one-line rationale.
3. **OBS scene plan** — which scene preset each shot uses ("Code", "Whiteboard", "Camera", "Camera+Code", "Camera Offline / Code Only").
4. **B-roll list** + **CTA overlay placement** + **thumbnail suggestion** (visual concept, not image generation).
5. **Diagram spec** — for every `[EXCALIDRAW]` beat, a JSON spec for `python/scripts/diagram.py`:
```json
{
  "title": "<shot name>",
  "elements": [
    {"type": "rectangle", "x": 100, "y": 100, "w": 240, "h": 80, "text": "Documents", "fill": "#a5d8ff"},
    {"type": "arrow", "x1": 340, "y1": 140, "x2": 460, "y2": 140},
    {"type": "ellipse", "x": 460, "y": 100, "w": 180, "h": 80, "text": "Vector DB", "fill": "#ffc9c9"}
  ]
}
```
   Write each to `outputs/<slug>/diagrams/<shot>.spec.json` (max 8 elements per diagram, 16:9-ish canvas bounds ≤ 1200×675).

## Rules
- One visual per shot. No dead air — every shot has an action.
- **Originality:** the storyboard frames Noah's own build — never recreate the source's demo shots, diagrams, or examples.
- Diagrams are base files Noah animates/traces on camera — keep them simple, boxes/arrows/text/ellipses only.
- If a shot needs no diagram, don't invent one.
