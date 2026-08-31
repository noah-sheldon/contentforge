# M1L1 · What Are AI Agents? — Build Spec

**Series:** AI Agents Zero→Hero · **Template:** `templates/courses/ai-agents-zero-to-hero/lesson-whiteboard/`
**Script:** `docs/course/m1l1-script.md` · **Post date:** 2026-08-11 · **Canvas:** 1728x3072 (9:16) · **Target:** ~58s
**Concept:** Agent ≠ chatbot. LLM + loop + tools. · **Through-line:** think → act → observe → repeat

## Brand (persona.yaml — single source of truth)

- Obsidian `#12141C` canvas · gold `#D4AF37` markers/strokes/accents · alabaster `#FAFAFA` ink
- Fonts: Playfair Display (display), Inter (body), Caveat (hand labels), JetBrains Mono (code)
- Gold surfaces: `rgba(212,175,55,0.08/0.25/0.10)` — card bg / border / glow
- Module identity via tag text only ("MODULE 1 · LESSON 1") — no per-module palettes

## Visual structure

- **Hook (0-2s):** no title card — brand flash (~0.8s: module tag + corner brand), then hook slams. Cover frame ~1.2s shows "AGENT ACTS" fully landed.
- **Persistent equation anchor (2-56s):** ONE element, dedicated overlay clip (`data-track-index` 2), three state steps at speech times:
  1. Beat 3: `AGENT = LLM + ? + ?`
  2. Beat 4: `AGENT = LLM + LOOP + ?`
  3. Beat 5: `AGENT = LLM + LOOP + TOOLS` (completes on "All three")
  Never respawned per beat.
- **Corner brand:** persistent, top-left, opacity 0.4.
- **Outro (56-58s):** full lockup + CTA "FOLLOW · AI AGENTS ZERO→HERO".

## Beat → motion budget (restrained — teaching, not spectacle)

Rule: **one gesture per beat, max two.** Elements appear when spoken (sharp fade+rise via the kit `beatIn`), strokes draw themselves (`drawOn`), marker strokes draw in gold (circle, strike). No bounce entrances, no slams, no waterfall cascades, no particles, no 3D, no glitch. The loop is the money shot — it gets the most motion, everything else stays quiet.

Kit helpers (`beatIn`/`drawOn`, `shared/reveal-engine.js`) are the course kit's compact forms; where a catalog rule exists the build uses the validated recipe: `svg-path-draw` (strokes), `discrete-text-sequence` (equation/notes state steps), `asr-keyword-glow` (keyword emphasis), `css-marker-patterns` (gold marker circle/strike), `spring-pop-entrance` (CTA, single small pop).

| Beat | Time | VO anchor | Visual | Motion |
|---|---|---|---|---|
| 1 Hook | 0-2 | "What's the difference between an agent and a chatbot?" | "AGENT vs CHATBOT" | Clean sharp reveal, question landed by ~1.2s (cover frame) |
| 2 Chatbot | 2-10 | "one call to a model, and that's it" | Chat bubble: one call in, one answer out; DONE stamp | Bubble appears; call line draws in; stamp pops |
| 3 Agent | 10-16 | "makes the call, reads the result, decides... Then it acts" | Same bubble + loop icon: call → read → decide → act | Call/read/decide/act chips appear on their spoken words |
| 4 Two parts | 16-24 | "An LLM that decides, and tools — search, code, APIs" | LLM box + TOOLS box (search · code · API chips); equation step 1 `AGENT = LLM + ? + ?` | Boxes fade+rise; chips appear; equation state step |
| 5 Pivot | 24-28 | "a chatbot can have those too. So that's not quite the difference" | Both boxes highlighted; "not the difference" scribble | Marker scribble-underline draws; no new boxes |
| 6 The loop | 28-40 | "The difference is the loop... what should I do next?... acts, calls a tool, reads the result, and repeats" | Circular loop draws: THINK → ACT → OBSERVE, arrow back REPEAT; equation step 2 `+ LOOP + ?` | Arrows **draw themselves**; words appear on speech; **gold marker-circle around LOOP** |
| 7 Feeds back | 40-46 | "result feeds back into the model... knows a little more each time" | Result line returns into the LLM box | One pass animates: result arrow draws back; "+1" chip |
| 8 Definition + flip | 46-55 | "an LLM, a loop, and tools. Take the loop away? ... chatbot with extra steps" | Equation completes `AGENT = LLM + LOOP + TOOLS`; LOOP struck through | Equation completes; **marker strike draws through LOOP**, equation collapses to chatbot stamp — the flip |
| 9 CTA | 55-60 | "Follow for the full course..." | End card "FOLLOW · AI AGENTS ZERO→HERO" | Single clean pop |

**Transitions between beats:** crossfade only (no push, no cover, no effects). The viewer's attention belongs to the teaching, not the cut.

## Sync workflow (critical)

1. Noah records VO from the beat outline (no word-for-word script).
2. Transcribe with word timestamps (faster-whisper) → map each spoken anchor to a second.
3. Build every `beatIn`/`drawOn`/state-step `at` from THAT mapping — never from the planned 58s. Planned times are estimates; the first take drifts.
4. `npm run check` → snapshot QA → render CRF 10 master → CRF 14 social re-encode.

## Fingerprint (log in docs/post-tracker.md after render)

- Module M1 (brand palette, D2 fixed) · Hook D3 (misdirection/contrarian) · CTA D4 (follow/serialization)
- Beat D5 (single deep dive) · SFX D6 (sparse: hook, loop, completion) · Length D7 (~60s)
- Trans D10 (crossfade/blur crossfade default; push at analogy→parts) · Title D11 (word slam)
- Template: lesson-whiteboard · Music: from shared audio library

## Deliverables

- `workspace/courses/2026.08.11_m1l1/` — lesson project (copy of lesson-whiteboard + spec + transcript + rendered MP4s)
- Cover frame ~1.2s; captions per platform via caption-writer (separate step)
