# M1L2 · Why Do We Need AI Agents? — Build Spec

**Series:** AI Agents Zero→Hero · **Template:** `templates/courses/ai-agents-zero-to-hero/lesson-whiteboard/`
**Script:** `docs/course/m1l2-script.md` · **Post date:** 2026-08-12 · **Canvas:** 1728x3072 (9:16) · **Target:** ~60s
**Concept:** LLM tells you how; the agent does it. · **Through-line:** TELLS HOW → DOES IT

## Brand (persona.yaml — single source of truth)

Same as M1L1: obsidian `#12141C` + gold `#D4AF37` markers, Playfair/Inter/Caveat/JetBrains Mono. Gold surfaces for cards. Module identity via tag text ("MODULE 1 · LESSON 2"). No per-module palettes.

## Visual structure

- **Hook (0-3s):** "WHY AGENTS?" question — no title card, corner brand visible.
- **Through-line anchor:** the TELLS HOW → DOES IT contrast — plan card that stops at a wall, then the loop that finishes the job.
- **Series echo:** the loop motif returns (same drawing language as M1L1) but from the execution angle — "Same loop. Call. Read. Decide. Repeat." explicitly references M1L1's loop.
- **Corner brand:** persistent, top-left, opacity 0.4.
- **Outro:** end card + M1L3 tease ("Next up — where agents already work").

## Beat → motion budget (restrained — same vocabulary as M1L1)

One gesture per beat, max two. `beatIn` (fade+rise on spoken word), `drawOn` (self-sketching strokes), gold marker strokes (X, strike, underline). Crossfades only. No slams, no particles, no 3D, no glitch.

| Beat | Time | VO anchor | Visual | Motion |
|---|---|---|---|---|
| 1 Hook | 0-3 | "So why do we even need agents? Well — here's the thing." | "WHY AGENTS?" | Clean sharp reveal (~1.2s cover) |
| 2 The stop | 3-12 | "plan your week... a perfect plan. And then? It just stops." | Plan card appears; arrow stops at a wall; "STOPS" stamp | Card rises; wall line draws; stamp pops |
| 3 Three can'ts | 12-18 | "can't check your calendar. Can't make the call. The email simply doesn't get sent." | Three chips: calendar ✗, call ✗, email ✗ | Each chip appears on its spoken word; gold **X draws** through each |
| 4 Close the gap | 18-23 | "That's where agents come in. They close the gap." | The wall gap; agent icon bridges it | Bridge arrow draws across |
| 5 The parts | 23-32 | "LLM does the planning. Agent does the doing. Tools make it real — search, code, APIs." | LLM (plans) → AGENT (does) → TOOLS chips | Three cards fade+rise in order; chips appear |
| 6 The loop | 32-45 | "one call is never enough... Same loop. Call. Read. Decide. Repeat. Until the job's done." | Loop draws (echo of M1L1): CALL → READ → DECIDE → REPEAT, "until done" | Arrows **draw themselves**; chant words settle on speech |
| 7 Finishes the job | 45-50 | "It doesn't stop at an answer. It actually finishes the job." | "ANSWER" vs "JOB DONE" — loop completes; DONE stamp | Stamp pops; answer card fades |
| 8 Payoff | 50-57 | "knowing isn't doing. An LLM hands you a map. An agent walks the road... comes back and tells you." | Map card vs road — path draws, agent walks it, returns with a report chip | Road **draws itself**; report chip appears — the payoff |
| 9 CTA | 57-60 | "Next up — where agents already work. Follow..." | End card "FOLLOW · AI AGENTS ZERO→HERO" | Single clean pop |

**Transitions between beats:** crossfade only.

## Sync workflow (critical)

1. Noah's recorded VO → clean (fillers/dead air out, natural rhythm in) → transcribe with word timestamps (faster-whisper).
2. Map every VO anchor to a second from the transcript — never from the planned times.
3. Build every `beatIn`/`drawOn`/marker-stroke `at` from that mapping.
4. `npm run check` → `snapshot` contact sheet at beat midpoints → `keyframes --shot` for draw-on proof → Studio preview → user approval.
5. Render high → CRF 10 master → CRF 14 social re-encode.

## Fingerprint (log in docs/post-tracker.md after render)

- Module M1 (brand palette, D2 fixed) · Hook D3 (question) · CTA D4 (serialization → M1L3)
- Beat D5 (single deep dive) · SFX D6 (sparse: hook, stamps, loop) · Length D7 (~60s)
- Trans D10 (crossfade) · Title D11 (clean reveal) · Template: lesson-whiteboard
- Music: shared audio library (same bed family as M1L1 — series consistency)

## Deliverables

- `workspace/courses/2026.08.12_m1l2/` — lesson project (copy of lesson-whiteboard + transcript + rendered MP4s)
- Cover frame ~1.2s; captions per platform via caption-writer (separate step)
