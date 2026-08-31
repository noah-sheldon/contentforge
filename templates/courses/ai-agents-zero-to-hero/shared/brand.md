# Course Brand — Obsidian + Gold

The whole course uses ONE palette — the persona brand (`persona.yaml`), which is the single source of truth. No per-module palettes.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#12141C` obsidian | canvas |
| `--ink` | `#FAFAFA` alabaster | text |
| `--accent` | `#D4AF37` gold | marker strokes, chalk, accents, display line "ZERO → HERO" |
| `--secondary` | `#E9D8A6` pale gold | edge labels, soft highlights |
| `--surface` | `rgba(212,175,55,0.08)` | card backgrounds |
| `--border` | `rgba(212,175,55,0.25)` | card borders |
| `--glow` | `rgba(212,175,55,0.10)` | radial glows |

## Usage rules

- The hand-drawn layer (marker highlights, hand-circles, scribbles, self-sketching strokes) is **always gold** — it is the series signature across all 24 lessons.
- Accent gold is for large text/decoratives and strokes; small text uses alabaster ink or `--muted` (contrast).
- Modules are differentiated by **tag text only** ("MODULE 1 · LESSON 1" → "MODULE 3 · LESSON 5"), never by palette.
- Background: obsidian + a soft gold radial glow behind content (`--glow`).
- Rotation registry: **D2 palette does not rotate** — the brand palette is fixed. Surface rotation happens on hooks, transitions, title animation, CTA (see `rotation.md`).
