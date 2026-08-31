# Editorial Audio Design Patterns

> Research for AI-powered automatic video editing pipeline (short-form "day in the life" / "come to work with me" vlogs).
> Style target: EDITORIAL, LUXURY, MINIMAL (Monocle, Apple commercial, high-end commercial video).
> Sources: EBU R128, ITU-R BS.1770, iZotope, BBC Sound Guidelines, YouTube Creator Academy, industry-standard post-production practices.

---

## 1. Voice Level Matching

### Normalization Targets

| Parameter | Target | Notes |
|---|---|---|
| **Integrated loudness** | **-14 LUFS** | YouTube normalization target. Mix to this. |
| **Short-term loudness** | **-14 LUFS** (±2 LU) | 3-second window. Stay consistent. |
| **True peak max** | **-2 dBTP** | Below YouTube's -1 dBTP limit for headroom. |
| **Gated loudness range** | ≤8 LU | Keep dynamic range tight for speech clarity. |
| **Sample rate / bit depth** | 48 kHz / 24-bit | Broadcast standard. |

### Compression (Voice Channel)

| Parameter | Value | Why |
|---|---|---|
| **Ratio** | **2:1** | Gentle compression. Preserves natural dynamics. |
| **Attack** | **10–20 ms** | Fast enough to catch plosives, slow enough to let consonants through. |
| **Release** | **50–100 ms** | Medium-fast. Recovers before next word but avoids pumping. |
| **Threshold** | **-18 dBFS** | Engages on louder syllables only. Leaves quiet moments natural. |
| **Gain reduction** | **3–6 dB** | Enough to even out peaks without squashing life out. |
| **Knee** | **Soft (6 dB)** | Smooth engage/disengage — no audible clamping. |

### EQ (Voice Channel)

| Frequency | Action | Q / Slope | Purpose |
|---|---|---|---|
| **80–100 Hz** | **High-pass filter** | 12 dB/oct | Remove rumble, HVAC, handling noise. |
| **200–400 Hz** | **-2 to -3 dB** | Wide (Q=1.0) | Reduce boxiness / muddiness from proximity effect. |
| **3–6 kHz** | **+1 to +2 dB** | Wide shelf | Presence bump for clarity on mobile speakers. |
| **8–12 kHz** | **+1 dB** | Shelving | Air / sparkle for luxury feel. No harshness. |

### De-essing

| Parameter | Value |
|---|---|
| **Frequency range** | 4–9 kHz |
| **Reduction** | -3 to -4 dB |
| **Detection** | Broadband or split-band |

---

## 2. Background Music Ducking

### Ducking Depth (Sidechain Compression)

| Context | Music Level | Ducking Depth |
|---|---|---|
| **Voiceover active** (no music) | — | N/A |
| **Voiceover + music** | **-24 LUFS** (relative to voice at -14 LUFS) | Music ducks **-10 dB** below its non-voice level. |
| **Music solo** (no voice) | **-20 LUFS** | Full music level. |
| **Music during pauses** | Ramp up from -24 → -20 LUFS over 500 ms | Smooth transition. |
| **Music during emphasis moments** | **-28 LUFS** (deep duck) | When voice needs full clarity for key point. |

### Sidechain Compressor Settings

| Parameter | Value | Why |
|---|---|---|
| **Ratio** | **2:1** to **4:1** | 2:1 for subtle duck (editorial), 4:1 for aggressive duck (fast vlog cuts). |
| **Attack** | **10–30 ms** | Fast enough that music drops before voice begins. 10 ms for tight vlogs, 30 ms for smoother editorial feel. |
| **Release** | **200–400 ms** | Medium-slow. Music fades back in smoothly after voice ends. 200 ms for fast-paced, 400 ms for relaxed. |
| **Threshold** | **-20 dBFS** | Engages when music exceeds background level. |
| **Knee** | **Soft (6 dB)** | Smooth duck curve — no audible clamp. |

### Volume Automation (Alternative to Sidechain)

When sidechain is not available, use volume automation:

| Event | Action | Ramp Time |
|---|---|---|
| Voice starts | Fade music from -20 LUFS → -24 LUFS | 50 ms fade |
| Voice ends | Fade music from -24 LUFS → -20 LUFS | 300 ms fade |
| Voice pause <1s | Hold at -24 LUFS | Hold |
| Voice pause >1s | Resume full music at -20 LUFS | 500 ms fade up |

### EQ on Music During Voiceover

| Filter | Setting | Purpose |
|---|---|---|
| **High-pass filter** | **200–300 Hz** | Scoop low end so voice sits above. |
| **Scoop at 1–3 kHz** | **-2 to -3 dB** | Clear space for voice presence range. |
| **Shelf dip at 4–8 kHz** | **-1 dB** | Reduce sibilance interference with voice. |

---

## 3. Ambient Sound Layering

### Layer Hierarchy

| Layer | Description | Level (relative to voice at -14 LUFS) | Notes |
|---|---|---|---|
| **1. Room Tone** | Silence of the room (recorded on location) | **-30 LUFS** (i.e. -16 dB below voice) | Foundation layer. Matches room's natural reverb/EQ. |
| **2. Office Interior** | Keyboard clicks, papers shuffling, distant conversation blur | **-32 LUFS** (-18 dB below voice) | Low-pass at 4 kHz so it doesn't mask voice. |
| **3. City Ambience** | Traffic, sirens, crowd murmur (for street scenes) | **-34 LUFS** (-20 dB below voice) | Wide stereo image. High-pass at 200 Hz to avoid mud with voice. |
| **4. Nature Ambience** | Birds, wind through trees, footsteps on gravel | **-36 LUFS** (-22 dB below voice) | For outdoor transition / coffee run scenes. |
| **5. Caf\u00e9 Ambience** | Espresso machine, chatter, cups clinking | **-34 LUFS** (-20 dB below voice) | Mid-range heavy — EQ dip at 1-3 kHz to leave room for voice. |

### Ambience Blending Rules

| Rule | Value | Purpose |
|---|---|---|
| **Crossfade between ambiences** | **500 ms** | Smooth scene transitions. No abrupt silence. |
| **Each layer** | **Mono or Mid-Side** | Room tone = mono. Interior = MS (ambient side). City = wide stereo. |
| **Ambience fade-out** | **1–2 seconds** | At end of scene. Natural tail to avoid cutoff. |
| **Ambience fade-in** | **500 ms** | Gradual entrance. Never pop in abruptly. |
| **High-pass filter per layer** | **80–200 Hz** | Each layer gets its own HPF to avoid cumulative low-end buildup. |

---

## 4. SFX for Transitions

### Whoosh (Scene Change)

| Parameter | Editorial / Luxury Style | Fast Vlog Style |
|---|---|---|
| **Duration** | **200–400 ms** | **100–200 ms** |
| **Volume** | **-20 LUFS** (-6 dB below voice) | **-22 LUFS** (-8 dB below voice) |
| **Volume envelope** | Fade in 50ms, peak, fade out 150ms | Fast attack 20ms, instant peak, decay 80ms |
| **EQ** | High-pass at 500 Hz | High-pass at 800 Hz |
| **Pitch contour** | Rising (subconscious upward movement) | Neutral or slight rise |
| **Filter sweep** | 500 Hz → 8 kHz | 800 Hz → 12 kHz |

### Hit / Stinger (Emphasis)

| Parameter | Editorial / Luxury Style | Fast Vlog Style |
|---|---|---|
| **Duration** | **100–200 ms** | **50–100 ms** |
| **Volume** | **-18 LUFS** (-4 dB below voice) | **-20 LUFS** (-6 dB below voice) |
| **Volume envelope** | Sharp attack 5ms, sustain 50ms, decay 100ms | Instant attack, fast decay 50ms |
| **EQ** | High-pass 200 Hz, boost 2–4 kHz for presence | Full range, boost 1–3 kHz |
| **Use case** | Key point emphasis, brand moment, reveal | Beat hits, energetic moments |
| **Spatial** | Center channel (mono compatible) | Stereo with slight width |

### Riser / Swell (Building Moment)

| Parameter | Editorial / Luxury Style | Fast Vlog Style |
|---|---|---|
| **Duration** | **1–3 seconds** | **500 ms – 1 second** |
| **Volume envelope** | Gradual fade in from -30 LUFS → peak at -20 LUFS over duration | Faster ramp |
| **Peak volume** | **-20 LUFS** (-6 dB below voice) | **-22 LUFS** (-8 dB below voice) |
| **Pitch contour** | Rising exponentially (pitch sweep low → high) | Rising linearly |
| **Filter** | Low-pass opens (200 Hz → 12 kHz) as riser climbs | Similar but faster |
| **Cut to** | Resolves into next scene on beat | Resolves on downbeat |

### Transition SFX Placement Rules

| Rule | Value |
|---|---|
| **Whoosh start** | **50–100 ms BEFORE** the visual cut (anticipation) |
| **Whoosh peak** | **Exactly on the cut frame** |
| **Whoosh tail** | Resolves **100–200 ms after** the cut |
| **Stinger** | **Exactly on** the visual cut or action point |
| **Riser start** | **1–3 seconds before** the climactic moment |
| **Riser resolves** | **Exactly on** the peak moment |
| **Gap between SFX** | Min **500 ms** — don't stack or overlap different transition types |

---

## 5. Audio Mixing Hierarchy

### Priority Levels (Loudness Hierarchy)

| Priority | Element | Level (relative to voice) | Rationale |
|---|---|---|---|
| **1 (LOUDEST)** | **Voice / Dialogue** | **0 dB reference** (-14 LUFS target) | Primary content. Everything serves voice clarity. |
| **2** | **SFX (Hits / Stingers)** | **-4 to -6 dB** relative to voice | Emphasis sounds should be felt, not covering voice. |
| **3** | **SFX (Whooshes)** | **-6 to -8 dB** relative to voice | Transition sounds are subconscious, not foreground. |
| **4** | **Ambient / Room Tone** | **-16 to -22 dB** relative to voice | Subconscious realism layer. Barely noticeable. |
| **5 (QUIETEST)** | **Background Music** (during voice) | **-10 dB** relative to voice (ducks to -24 LUFS) | Mood setting, not competing for attention. |
| — | **Background Music** (no voice) | **-6 dB** relative to voice (full level -20 LUFS) | Full expression between voice segments. |

### Spectral Hierarchy (EQ Allocation)

| Frequency Band | Allocated To | Notes |
|---|---|---|
| **20–80 Hz** | Music (sub-bass) | Voice doesn't live here. Music's low rumble for emotion. |
| **80–200 Hz** | Voice fundamental + low music | Voice HPF at 80 Hz. Music occupies the rest. |
| **200–500 Hz** | Voice (warmth) + ambient | Scoop music at 200–400 Hz. Keep voice warm. |
| **500 Hz – 2 kHz** | Voice (body/clarity) | **Protected band.** Minimize ambient/SFX here. |
| **2–4 kHz** | Voice (presence) + SFX hits | Presence bump for voice. SFX hits can share. |
| **4–8 kHz** | Voice (sibilance) + ambience detail | De-ess voice. Low-pass ambient here. |
| **8–20 kHz** | Music (air) + ambience sparkle | Voice HPF removes most here. Let music breathe. |

### Panning / Spatial Rules

| Element | Panning |
|---|---|
| **Voice** | **Center** (mono) — always dead center |
| **Music** | **Stereo** (full width) — use the sides |
| **Ambient** | **Stereo** (wide) — use Mid-Side, side channel prominent |
| **SFX (whoosh)** | **Left-to-right or right-to-left sweep** — directional movement matches visual |
| **SFX (hit/stinger)** | **Center** — impact should be felt equally |
| **SFX (riser)** | **Center → spread wide** — builds in width as it rises |

---

## 6. Level Metering Reference

### RMS / Peak Levels (dBFS)

| Element | Average RMS | Peak |
|---|---|---|
| **Voice** | -18 dBFS to -14 dBFS | -6 dBFS max |
| **Music (full)** | -22 dBFS to -18 dBFS | -8 dBFS max |
| **Music (under voice)** | -26 dBFS to -22 dBFS | -12 dBFS max |
| **SFX (hit)** | -16 dBFS to -12 dBFS | -6 dBFS max |
| **SFX (whoosh)** | -22 dBFS to -18 dBFS | -10 dBFS max |
| **Ambient** | -30 dBFS to -24 dBFS | -16 dBFS max |

### LUFS Reference for Different Output Platforms

| Platform | Target LUFS | Max True Peak | Notes |
|---|---|---|---|
| **YouTube** | **-14 LUFS** | -1 dBTP | Most relevant for this pipeline. |
| **Instagram / Reels** | **-14 LUFS** | -1 dBTP | Same as YouTube. |
| **LinkedIn** | **-14 LUFS** | -1 dBTP | Same standard. |
| **TikTok** | **-14 LUFS** | -1 dBTP | Same standard. |
| **Broadcast TV** | -23 LUFS | -1 dBTP | EBU R128 — much quieter. Don't use. |
| **Apple Podcasts** | -16 LUFS | -1 dBTP | Only if audio-only. |

---

## 7. Codeable Processing Pipeline (Order of Operations)

For an AI pipeline processing audio programmatically:

```
Step 1: Normalize voice to -14 LUFS (integrated)
  ├── Apply 80 Hz high-pass filter
  ├── Apply 2:1 compression (10ms attack, 70ms release, -18 dBFS threshold)
  ├── Apply de-esser (4-9 kHz, -3 dB reduction)
  └── Apply presence EQ (+1.5 dB at 4 kHz, wide Q)

Step 2: Duck music under voice
  ├── Detect voice segments (silence detection)
  ├── During voice: lower music to -24 LUFS (50 ms fade)
  ├── During pauses: raise music to -20 LUFS over 300 ms
  └── Scoop music EQ: HPF at 250 Hz, -2.5 dB at 2 kHz

Step 3: Layer ambience at scene boundaries
  ├── Room tone: -30 LUFS (mono)
  ├── Scene-specific ambience: -32 to -36 LUFS (stereo)
  ├── 500 ms crossfade between ambience layers
  └── Separate HPF per layer to prevent low-end buildup

Step 4: Place transition SFX on scene cuts
  ├── Whoosh: 200-300 ms, starts 50 ms before cut, -20 LUFS peak
  ├── Hit/stinger: on emphasis moments, 100 ms, -18 LUFS peak
  └── Riser: 1-3 seconds before climax, ramp from -30 to -20 LUFS

Step 5: Final mix loudness normalization
  ├── Verify integrated loudness = -14 LUFS
  ├── Verify true peak ≤ -2 dBTP
  └── Apply limiter at -2 dBTP if necessary (max 2 dB gain reduction)
```

---

## 8. Editorial/Luxury Style-Specific Adjustments

For Monocle / Apple / high-end commercial aesthetic, deviate from defaults:

| Parameter | Default (Vlog) | Editorial / Luxury |
|---|---|---|
| **Music ducking depth** | -10 dB | **-6 to -8 dB** (less ducking — music is more present) |
| **Music EQ scoop** | -3 dB at 2 kHz | **-1.5 dB** (gentler scoop — preserve music texture) |
| **Ambience level** | -18 dB below voice | **-22 dB below voice** (more subtle — barely perceptible) |
| **SFX level** | -6 dB below voice | **-8 to -10 dB below voice** (quieter — subconscious only) |
| **Riser duration** | 1–2 seconds | **2–4 seconds** (slower build — more patient pacing) |
| **Whoosh duration** | 100–200 ms | **300–500 ms** (slower, more graceful sweep) |
| **Voice compression** | 4:1 ratio | **2:1 ratio** (less compression — preserve natural dynamics) |
| **Voice presence boost** | +3 dB at 3 kHz | **+1.5 dB at 4 kHz** (subtler presence) |
| **Release time (ducking)** | 200 ms | **400–600 ms** (slower, smoother recovery) |
| **Ambience crossfade** | 500 ms | **1–2 seconds** (languid crossfade — editorial pacing) |

---

## References

- EBU R128: Loudness normalisation and permitted maximum level of audio signals (−23 LUFS target, ±0.5 LU deviation)
- ITU-R BS.1770-4: Algorithms to measure audio programme loudness and true-peak audio level
- YouTube: Loudness normalisation at −14 LUFS, true peak at −1 dBTP
- iZotope: Voiceover/dialogue processing guidelines (2:1 compression, 80-100 Hz high-pass, -20 dB input target)
- Industry standard post-production practices for commercial video and broadcast
- Apple / Monocle editorial video aesthetic: wider dynamic range, slower transitions, music-forward mix
