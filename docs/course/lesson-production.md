# Lesson Production — Operating Rules (learned on M1L1–M1L6)

Hard-won rules for building a lesson. Read before building. Applies to all course lessons.

## 1. Architecture

- **Scene-based sub-compositions:** `compositions/scenes/NN-<name>.html` (own `<template>`, `<style>` + `<script>` INSIDE the template, own `data-composition-id` + `window.__timelines` key) mounted from `index.html` host slots (`data-composition-src`, `data-start`, `data-duration`, `data-track-index`, `class="clip"`, unique `id`). Persistent overlays (corner brand) on track 2.
- **Kill the preview server before batch-editing compositions.** Studio rewrites files (injects `data-hf-id`) and races edits. `pkill -9 -f "hyperframes preview"`, edit, re-check, restart preview.
- Host slot ids required (Studio lint: `media_missing_id` style). Audio elements need ids too.

## 2. Audio pipeline (identical every lesson)

1. `python/scripts/clean_vo.py` — highpass 70 + afftdn nr=8 + agate breath-duck (threshold -38dB, attack 8ms) + loudnorm -14 LUFS. **Time-invariant** (timestamps stay valid).
2. `python/scripts/tighten_vo.py --keep 0.2 --cut 0.45` — aggressive short-form cut (pauses >0.45s → 0.2s). Keeps speech; verify with `kept N segments, Xs -> Ys`.
3. **Splice fillers** (Noah's filler rule): e.g. "basically" — find word span in transcript, `ffmpeg atrim` cut it, **shift the transcript** (t -= splice_len for t >= cut_start, drop spliced words). Never leave lead silence: trim to ~0.3s lead.
4. `python/scripts/transcribe_vo.py` (faster-whisper small.en, word timestamps) → `transcript.json`. Re-transcribe after ANY audio edit.

## 3. Sync workflow

- Scene boundaries = transcript beat boundaries; **scene sum must equal VO duration exactly.**
- Every visual anchor = a spoken word's timestamp. Local time = global − scene start. Cross-check with the OK/BAD anchor script (every anchor inside its scene window).
- Then: `check` → `snapshot --at <beats>` (frame QA: no frame >98% dark except the beyond-duration artifact) → preview → render.

## 4. Visual fit rules (checker is conservative)

- **Mono text:** the checker measures ~1em/char. Keep code lines short or panels wide (1320px panels; 40-44px mono). Shorten strings before shrinking fonts.
- **Slam/hero lines:** split into two lines (130-150px each). Single-word slams (REACT) fine at 240px. Never one long line >170px.
- **Node titles:** "OBSERVATION" (11 chars, 84px hand) overflows a 400px circle → use 74px for 10+ char titles.
- **Loop arrow endpoints:** compute in user space (screen = svg offset + user). Attach endpoints to node EDGES for the specific scene's node positions — never copy between scenes with different node layouts.
- **Intentional clipping** (code panels, chrome): `data-layout-allow-overflow` on the inner body is the sanctioned escape hatch.
- Chips/cards: content must fit inner width (measured ~0.6em hand, ~1em mono conservative).

## 5. Rotation (per lesson fingerprint)

- Music cycles tech → chillout → lo-fi, never consecutive. Wire before render.
- Hook reveal type rotates (slam / word-settle+underline / question+marker / claim); transitions rotate (hard cut / obsidian dip / blur crossfade).
- Middle-path motion: hook + payoff moments get energy (slams, pops); the rest is quiet beatIn/drawOn.

## 6. Facts

- Render: `npx hyperframes render --quality high --crf 10` → master; `ffmpeg -crf 14` for social when requested.
- The story→visual anchor verification is a required gate before preview/render.
