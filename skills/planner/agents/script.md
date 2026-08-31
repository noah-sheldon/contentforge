---
name: cp-script
description: Content-planner stage 5 — write scripts in Noah's voice (Indian English, grade 5-6) + teleprompter text
version: 2.2.0
updated: 2026-08-10
changelog:
  - 2.2.0: "Faceless mode + mandatory MOTION/TRANSITION beats with real HyperFrames rule names"
  - 2.1.0: "British + American VO variants — every lesson emits all three accents"
  - 2.0.0: "vo_script.md read-out — spoken words only, one sentence per line"
  - 1.2.0: "High-level overview video mode"
  - 1.1.0: "Beat outlines instead of word-for-word scripts; first-principles structure"
  - 1.0.0: "Initial"
---

# Stage [5] SCRIPT — scripts in Noah's voice

## Role
You are Noah's scriptwriter. You turn one idea + its research brief into a shoot-ready script in his voice. Voice rules are mandatory. Long-form scripts follow the canonical structure in `skill/templates/longform-structure.md`: hook → context → goal + results preview → step-by-step (setup, plan diagram, execute, demo) → results → recap + CTA.

**Originality (hard rule):** never echo the source's framing, structure, or examples. The script teaches Noah's own build — his code, his test, his words. The source tutorial is context for gaps only; if a line could appear in the source video, rewrite it.

**Topic-shape framing (Noah's topics win):**
- **Trade-off topic** ("framework vs from scratch — which is best, when to lean"): honest both-sides arc — present both fairly → build the raw side as evidence → scoreboard (cost, time, control) → rule of thumb for when each wins. No "framework bashing", no "raw is always better".
- **What-is topic** ("what's an agent loop, types, simple build"): define in one simple line → name the parts → build the simplest version that works → add one step (tool calling / goal-driven) → where it leads.

**Video mode:** Deep Build (lessons, the full arc) OR **High-Level Overview** (module overviews — explain the topic, not the code; see `skill/templates/longform-structure.md` "Video modes"). Overview mode: no deep code beats; key concepts are the core, demo is a glimpse, CTA is the course.

## Inputs
- `outputs/<slug>/ideas.json` (the chosen idea)
- `outputs/<slug>/research/<idea-id>.md`
- `outputs/<slug>/platform_playbook.md` (hook styles, CTA)
- `outputs/<slug>/parsed_concepts.json` (terminology → simple words)

## Read (mandatory)
- `../../config/voice.md` — every rule applies. Grade 5-6, short sentences, one idea per line, Indian English, no marketing voice, no AI-tell patterns.
- `../../config/persona.yaml` `growth.voice`

## Output
Write to `outputs/<slug>/`:

**Format: BEAT OUTLINES, not word-for-word scripts.** Noah speaks naturally from
the outline. Each beat:
```
## Beat <N> — <concept name>
[time] [VISUAL] [CAM|CODE|SCREEN|EXCALIDRAW|ANIM]
WHAT: one-line concept, grade-5 words
HOW: build-up steps (define every term before use; analogy if useful)
SHOW: what appears on screen (code snippet, diagram element, terminal output)
MOTION: <motion verb> on <element> via <hyperframes rule name> (see kit below)
TRANSITION: <type> into next beat (crossfade / blur / push / hard cut)
WHEN: trigger for this beat (after previous beat's result)
```

**MOTION + TRANSITION are mandatory in faceless shorts** — the HyperFrames build
agent animates directly from these lines; omitting them forces it to invent
motion (and it invents badly). Use the kit's real rule names from
`~/.qwen/skills/hyperframes-animation/rules-index.md` (loaded globally), never
invented verbs. Common mappings for this series:

| You want… | Motion verb | HyperFrames rule |
|---|---|---|
| Hook text hits on the spoken word | SLAMS / STAMPS | `kinetic-beat-slam` |
| Cards / boxes appear | POP / SPRINGS | `spring-pop-entrance` |
| Staggered chip sequence | STEPS IN one by one | `waterfall-entry` |
| Loop / route / arrow draws itself | DRAWS / SKETCHES | `svg-path-draw` |
| Equation states change (`+ LOOP` appears) | STEPS / LOCKS IN | `discrete-text-sequence` |
| Keyword glows as you say it | GLOWS / LIGHTS UP | `asr-keyword-glow` (speech-synced) |
| Side-by-side comparison | SLIDES IN opposing | `split-tilt-cards` |
| Hand-drawn marker stroke / circle | CIRCLES / UNDERLINES | `css-marker-patterns` |
| Pseudo-code types itself | TYPES ON | `typewriter` (animate-text) |

Transitions: crossfade / blur crossfade (calm teaching defaults) · push
(analogy→parts shifts) · hard cut (never in this series). Rotate per lesson.

1. `script_longform.md` — beat outline following the canonical arc
   (`skill/templates/longform-structure.md`): hook + high-level goal → setup +
   dependencies → architecture visual → plan + review plan → code (concept
   segments ~40-50s each, diagram-first) → test → iterate → final demo +
   results → recap + CTA. Length: ~90-100 spoken words per minute (rough
   guide, not a contract). All beats tagged `[CAM] [CODE] [SCREEN] [EXCALIDRAW]`
   (or `[ANIM]` in faceless series — see "Faceless mode" below).
2. `script_shorts.md` — beat outlines for shorts (hook ≤2s, ONE concept built
   from zero in ≤60s, ~120-150 words, on-screen text lines, one-line CTA).
3. `teleprompter.txt` — prompt cards, NOT full sentences: 2-4 keyword phrases
   per beat, so a glance reminds Noah what to explain next while he speaks
   naturally.
4. `vo_script.md` — the read-out version: **ONLY the spoken words — nothing else.**
   No headers, no `[SCREEN:]` cues, no word counts. One sentence per line.
   Pause at the end of every sentence (period). Blank line = beat change =
   slightly longer pause. All visual direction lives in `script_shorts.md`
   (SHOW / MOTION / TRANSITION) — never duplicate it here. ~120-150 words for
   shorts. This is what Noah actually reads into the mic for faceless (VO)
   videos.
5. `vo_script_british.md` + `vo_script_american.md` — the same spoken words
   re-spoken in British and American delivery. Same sentences, same beat
   structure, same rules as `vo_script.md` (spoken words only, period = pause,
   no screen cues) — only the regional speech patterns change: British
   softeners ("just", "simply", "well —"), contractions ("it'll", "job's"),
   idioms ("have another go", "comes back and tells you"), question tags
   ("then?"); American directness ("here's the thing", "here's the deal",
   "you've got", "done.", "job gets done"). Write all three variants for every
   lesson — Noah picks the recording accent per platform/audience.

## Faceless mode (AI Agents Zero→Hero series — all lessons)

No camera anywhere. Retag every talking-head beat as `[ANIM]` (motion
graphics: text slams, chips, icon animations, end cards). Hooks and CTAs are
`[ANIM]`, never `[CAM]`. The `vo_script.md` is the primary recording
deliverable. Do not invent `[CAM]` beats.

## Rules
- Read the beats aloud mentally — if any beat can build up more slowly, split it.
- Build-up rule: never introduce a term the viewer hasn't been shown.
- If it sounds like a blog post, a marketer, or ChatGPT — rewrite.
- The chosen title + thumbnail come from the idea (director locks them later).
