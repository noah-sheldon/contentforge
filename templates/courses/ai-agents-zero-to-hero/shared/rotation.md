# Course-Mode Rotation Policy

The course family inherits the 12-dimension rotation registry (`docs/font-color-rotation.md`), but **course identity beats variety**. Two tiers:

## Fixed — never rotates (course DNA)

| Dimension | Setting |
|---|---|
| D1 Font pair | Display `Playfair Display` + body `Inter` + hand `Caveat` + mono `JetBrains Mono` (persona.yaml) |
| D2 Palette | **Brand only** — obsidian `#12141C` + gold `#D4AF37` (persona.yaml). Never rotates. Modules differ by tag text only. |
| D9 Text layout | Full-screen cards (infographic/explainer) |
| D12 Aspect | 9:16 @ 1728x3072 |

## Rotates — surface only

| Dimension | Policy |
|---|---|
| D3 Hook style | Rotate per lesson (never same in consecutive lessons) |
| D4 CTA type | Rotate per lesson |
| D5 Beat structure | Rotate per lesson |
| D6 SFX pattern | Rotate per lesson |
| D7 Length | 30-90s by content; varies naturally |
| D10 Transition | Rotate per lesson (from the HyperFrames transition catalog) |
| D11 Title animation | Rotate per lesson |

## Through-line anchors (fixed pattern)

Lessons that build a formula/equation across beats (e.g. M1L1: `AGENT = LLM + ? + ?` → `+ LOOP + ?` → `+ LOOP + TOOLS`) use **one persistent element** in a dedicated overlay clip spanning the beats, with state steps — never a respawned box per beat. The build-up story dies if the anchor resets.

## Fingerprint log

Every lesson logs its fingerprint in `docs/post-tracker.md` after render:

```markdown
## YYYY-MM-DD — M#L# <lesson name>
- Module: M# (brand palette, D2 fixed) · Hook: D3#N · CTA: D4#N
- Beat: D5#N · SFX: D6#N · Length: D7#N · Trans: D10#N · Title: D11#N
- Template: lesson-whiteboard | lesson-graph | lesson-code
- Music: none (banned, all videos) · VO: <recording file>
```

Constraint: within a module, no two consecutive lessons share the same option number in D3/D4/D5/D6/D10/D11.
