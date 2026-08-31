# Professional Video Editing Patterns — Short-Form Vlog Pipeline

**Style target:** Editorial / luxury / high-end commercial (Monocle, Apple, Vogue)
**Format:** "Day in the life" / "Come to work with me" vlogs
**Pipeline:** AI-powered automatic video editing (59s short-form primary)

---

## Table of Contents

1. [Editing Rhythm & Pacing](#1-editing-rhythm--pacing)
2. [Transition Types](#2-transition-types)
3. [Audio Design](#3-audio-design)
4. [Motion Graphics](#4-motion-graphics)
5. [Color Grading](#5-color-grading)
6. [Subtitle & Caption Style](#6-subtitle--caption-style)
7. [Intro & Hook Structure](#7-intro--hook-structure)
8. [Outro Patterns](#8-outro-patterns)

---

## 1. Editing Rhythm & Pacing

### 1.1 Shot Duration by Type (59s Editorial Vlog)

| Shot Type | Duration | Purpose |
|---|---|---|
| Hook / opener | 2–4s | Fast attention grab |
| Establishing (location, time context) | 6–8s | Orient viewer |
| Action / B-roll (walking, typing, coffee) | 3–5s | Visual variety |
| Talking head / monologue | 5–8s | Max before cutaway needed |
| Detail shot (hands, screen, objects) | 2–4s | Proximity variety |
| Montage sequence | 1–3s per clip | Time compression |
| Transition wipe to next scene | 0.5–1s | Brief bridge clip |
| Slow / reflective moment | up to 12s | Max luxury duration |
| Close / outro | 4–6s | Sign-off, CTA |

**Rule:** Mix wide (6–8s), medium (4–6s), and close-up (2–4s) in sequence — never two same-length clips consecutively.

### 1.2 Three-Phase Pacing Structure for 59s

| Phase | Position | Duration | Pace Multiplier | Cuts/Min | Purpose |
|---|---|---|---|---|---|
| Hook | 0:00–0:08 | 8s (13%) | 2–3× baseline | 40–60 | Best moment first, no slow establishing |
| Main content | 0:08–0:52 | 44s (75%) | 1× baseline | 20–30 | Vary shot length, inject energy every 12–15s |
| Close | 0:52–0:59 | 7s (12%) | 1.5–2× baseline | 30–40 | Accelerate toward CTA, don't fade out slowly |

### 1.3 Core Pacing Rules

| Rule | Value |
|---|---|
| Max consecutive same shot type | 2 clips |
| Visual shift frequency | Every 3–7s |
| Energy injection frequency | Every 8–15s |
| Max slow segment before cut needed | 10s |
| Minimum clip duration | 1.0s |
| Optimal clip density | 25–40 cuts/min |
| Max silence gap before cut | 1.5s |
| Jump cut min angle change | 30° OR 2× scale change |

### 1.4 Fibonacci-ish Pacing Pattern

Vary clip durations to avoid metronome pacing:

```
PACING_PATTERN = [2, 3, 5, 3, 2, 4, 6, 2, 5, 3, 4, 2, 3, 7, 2, 5, 3, 2, 4, 3, 2, 6, 3, 2, 5, 3, 2, 4, 3, 2]
```

Rule: Never 3 consecutive clips of same duration. Interleave short (1–2s), medium (3–5s), long (6–8s).

### 1.5 J-Cut / L-Cut Timing

| Type | Offset | Use Case |
|---|---|---|
| J-Cut (audio leads) | 0.8–1.5s (24–45 frames) | Entering new location, starting a section, anticipation moment |
| L-Cut (video leads) | 0.4–1.5s (12–45 frames) | Monologue over B-roll, music tail, reaction linger, dialogue interruption |

J-cuts for: entering office → building ambience starts while still showing commute.
L-cuts for: monologue continues over B-roll of typing/working.

### 1.6 Retention Curve (59s Format)

| Time | Viewer Behavior | Pipeline Rule |
|---|---|---|
| 0–3s | Decide to stay or leave | Must deliver visual interest + promise within 3s |
| 0–8s | Algorithm evaluates 60%+ retention | First 8s = strongest content, apply 2–3× hook pacing |
| 15–20s | Peak engagement zone | Keep energy high |
| 45–50s | Fatigue zone | Accelerate toward close, no new concepts |

---

## 2. Transition Types

### 2.1 Transition Palette (Editorial Only)

| Transition | Duration | Use Case | Frequency |
|---|---|---|---|
| **Hard cut** | Instant | Default for everything | 90%+ of transitions |
| **Dip to black** | 0.5–1s (12–24 frames) | Scene end, time passage | As needed |
| **Dip to white** | 0.33–0.66s (8–16 frames) | Aspirational/memory moments | Max 2/video |
| **Micro-dissolve** | 4–6 frames | Barely perceptible softening | Occasional |
| **Short dissolve** | 8–12 frames | Within-scene continuity | Rare |
| **Standard dissolve** | 1–2s (24–48 frames) | Major scene change | Rare |

### 2.2 Prohibited Transitions (Editorial Style)

All of the following are FORBIDDEN in editorial/luxury content:
- Wipe, slide, push, glitch, flash, zoom, shutter, page peel, 3D transitions
- Any transition that draws attention to itself

**Hard cut or nothing.** The occasional subtle dissolve is the only acceptable non-hard-cut.

### 2.3 Cut Decision Priority Matrix

```python
# Priority logic - evaluate in order:
1. Dialogue speech → hard cut (never dissolve during speech)
2. Scene end → dip to black (0.5-1s)
3. Aspirational moment → dip to white (0.33-0.66s)
4. Visual match found → match cut (hard cut)
5. Audio crossover possible → J-cut or L-cut
6. B-roll transition → hard cut
7. Last resort → cross dissolve
```

### 2.4 Good Hard Cut Rules

- Cut during motion (movement masks the cut)
- Match eye-trace position between shots
- Trim dead space (breaths, pauses, hesitations)
- Beat-match to music (cut on downbeat or half-beat)
- 30-degree rule: change angle ≥30° between shots of same subject

### 2.5 Match Cuts (Detection Logic)

Trigger match cut when any single similarity score >0.85:
1. **Positional** — X/Y of subject center
2. **Graphic/shape** — HOG descriptors or contour similarity
3. **Motion vector** — Optical flow cosine similarity
4. **Audio match** — MFCC feature vector comparison
5. **Color palette** — Histogram intersection

All match cuts are hard cuts (no dissolve).

---

## 3. Audio Design

### 3.1 Audio Mixing Hierarchy

| Element | Relative Level | Frequency Notes |
|---|---|---|
| Voice (0 dB reference) | 0 dB | 80 Hz – 8 kHz (HPF at 80–100 Hz) |
| SFX hits/stingers | –4 to –6 dB | Full spectrum, transient shapes |
| Whooshes | –6 to –8 dB | 200 Hz – 8 kHz |
| Ambient sound | –16 to –22 dB | HPF varies by layer |
| Background music | –10 dB (–24 LUFS) | Scooped at 250 Hz, –2.5 dB at 2 kHz |

### 3.2 Voice Level Matching

| Parameter | Value |
|---|---|
| Normalization target | –14 LUFS (YouTube/IG standard) |
| Compression ratio | 2:1 |
| Attack time | 10–20 ms |
| Release time | 50–100 ms |
| Threshold | –18 dBFS |
| Max gain reduction | 3–6 dB |
| HPF | 80–100 Hz |
| Presence boost | +1.5 dB at 4 kHz |

### 3.3 Background Music Ducking

| Parameter | Value |
|---|---|
| Voice-active music level | –24 LUFS (10 dB below voice) |
| Music level in pauses | –20 LUFS |
| Duck ratio | 2:1 to 4:1 |
| Duck attack | 10–30 ms |
| Duck release | 200–400 ms |
| Duck fade (start) | 50 ms |
| Recovery time | 300 ms |
| Music HPF | 250 Hz |
| Music scoop at 2 kHz | –2.5 dB |

### 3.4 Ambient Sound Layering

| Layer | Level | HPF |
|---|---|---|
| Room tone | –30 LUFS | None |
| Office interior | –32 LUFS | 100 Hz |
| City ambience | –34 LUFS | 150 Hz |
| Nature | –36 LUFS | 80 Hz |
| Café | –32 LUFS | 120 Hz |

- 500 ms crossfade between ambient layers
- 16–22 dB below voice level

### 3.5 Transition SFX

| SFX | Duration | Level | Timing |
|---|---|---|---|
| Whoosh | 200–400 ms | –20 LUFS | Starts 50 ms before cut, peaks at cut |
| Hit / stinger | 100–200 ms | –18 LUFS | Exactly on beat or action |
| Riser | 1–3s | –30 to –20 LUFS (ramp) | Leads into key moment |

### 3.6 Editorial/Luxury Audio Adjustments

| Parameter | Standard | Editorial |
|---|---|---|
| Music ducking | –10 dB | –6 dB (gentler) |
| Whoosh duration | 200–300 ms | 300–500 ms (slower) |
| Compression ratio | 4:1 | 2:1 (lighter) |
| Release time | 200–300 ms | 400–600 ms (slower) |
| Ambience crossfade | 500 ms | 1–2s |

---

## 4. Motion Graphics

### 4.1 Lower Third Animation

| Parameter | Value |
|---|---|
| Position | Bottom-left, 5% from left, 8% from bottom |
| Entry duration | 0.40s cubic-bezier(0, 0, 0.2, 1) — slide from left (-48px) + fade + blur dissolve (8px→0) |
| Hold duration | 4.0s |
| Exit duration | 0.30s cubic-bezier(0.4, 0, 1, 1) |
| Total duration | ~4.7s |
| Accent bar | Gold, 40px wide × 3px, precedes text |
| Name typography | Inter Semi-Bold 32px, 0.04em tracking |
| Descriptor typography | Inter Regular 22px, 0.08em tracking |

### 4.2 Kinetic Typography / Text Reveals

| Style | Parameters | Use |
|---|---|---|
| Per-word fade + slide up | 0.10s stagger between words, 0.20s per word, 24px upward | Primary style |
| Full-line fade up | 0.35s for entire line | Secondary, simpler moments |
| Hero typography | Inter Bold 56px, –0.02em tracking | Key statements |
| Kicker | Gold uppercase 18px, 0.12em tracking | Section labels |
| Hold duration | 3–5s per block | Readability |
| Exit | 0.30s cubic-bezier(0.4, 0, 1, 1) | Quick out |

### 4.3 HUD Overlay Positioning

| Position | Inset | Width | Usage |
|---|---|---|---|
| Top-left info stamp | 4% from top/left | 30% frame width | Time, date, location data |
| Bottom-left metric card | 5% from bottom, 18% from left | 30% frame | Stats, counters |
| Top-right data cluster | 4% from top, 4% from right | 30% frame | Rare — secondary data |

**Visual treatment:**
- Background: rgba(18, 20, 28, 0.55) with 12px backdrop blur
- Border: 1px hairline at 8% white
- Max opacity: 80%
- Typography: JetBrains Mono 32px for primary data, Inter 16px for labels, –0.02em tracking

### 4.4 Data Visualization Overlays

| Type | Dimensions | Animation |
|---|---|---|
| Progress bar | 70% frame width × 6px | Fill over 0.8s deceleration |
| Timeline indicator | 65% width × 3px rail | Slide along rail |
| Ring gauge | 90px diameter | Fill over 0.8s |
| Stat counter | Variable | Count-up over 1.0–1.5s |
| Bar chart | Variable | 0.08s stagger between bars |

Colors: Single accent = gold (#D4AF37). Background tracks at rgba(250, 250, 250, 0.10). Green/red only for performance deltas.

### 4.5 Brand Bug / Logo

| Parameter | Value |
|---|---|
| Position | Bottom-right, 3% from right, 4% from bottom |
| Size | 5% of frame width |
| Intro animation | Fade in to 65% over 0.50s → hold 2.0s → fade to persistent 30% |
| Rule | Appears once at intro. Never on title or end cards. Not persistent. |

---

## 5. Color Grading

### 5.1 Teal/Orange Split (Editorial Look)

| Element | Hue Angle | Target |
|---|---|---|
| Shadows/midtones | 170°–210° (cyan/teal) | Shift toward teal |
| Highlights/skin | 15°–40° (orange) | Shift toward warm orange |

**Implementation:** Applied relatively (not absolute). Saturate based on source footage. Keep skin tones natural — protect H: 0°–40° zone.

### 5.2 Exposure Targets

| Element | IRE Target | 8-bit Y' |
|---|---|---|
| Skin (fair) | 65–75 IRE | ~159–180 |
| Skin (olive/medium) | 55–68 IRE | ~137–165 |
| Skin (dark/deep) | 45–62 IRE | ~115–152 |
| Highlights | 80–90 IRE | ~191–213 |
| Shadows | 10–20 IRE | ~38–60 |

Reference: Rec.709 — Black at 16, White at 235 (8-bit).

### 5.3 S-Curve Contrast

| Zone | Input (IRE%) | Output (IRE%) |
|---|---|---|
| Shadow | 0% | 4–6% (lift slightly) |
| Quarter | 25% | 29–31% |
| Midtone (locked) | 50% | 50% |
| Three-quarter | 75% | 70–73% |
| Highlight | 100% | 92–96% (roll off) |

### 5.4 Scene Color Temperature Matching

| Scene | Grade Approach |
|---|---|
| Office | Neutralize to 5600K, add +500K warmth to skin |
| Outdoor (sunny) | ~5600K, slight +200K warmth |
| Commute | Neutralize mixed lighting to 5600K, contrast boost +5–10 IRE |
| Home | Accept warmth at 3800–4200K — do not fully correct to 5600K |
| Café | White balance off neutral surface, warm bias toward skin |

### 5.5 Platform-Specific Encoding

| Parameter | YouTube Shorts | Instagram Reels |
|---|---|---|
| Container | MP4, Fast Start | MOV or MP4, Fast Start |
| Video codec | H.264 High, progressive, 4:2:0 | HEVC or H.264, progressive, 4:2:0 |
| Audio codec | AAC-LC or Opus, 48kHz | AAC, 48kHz |
| Color space | BT.709 | BT.709 |
| Bitrate (1080p 24-30) | 8 Mbps | 25 Mbps max |
| Audio bitrate | 384 kbps | 128 kbps |

### 5.6 Compression-Aware Adjustments

| Platform | Saturation | Contrast | Notes |
|---|---|---|---|
| YouTube Shorts | No boost | No boost | Full range safe |
| Instagram Reels | +5–10% | +10% | Lift blacks slightly (compression crushes) |
| TikTok | +10–15% | +15% | Heaviest compression — overshoot |

---

## 6. Subtitle & Caption Style

### 6.1 Recommended: Hybrid Phrase + Active-Word Highlight

Show full phrase (3–7 words) in dim white [rgba(255, 255, 255, 0.6)]. Highlight the currently spoken word in gold (#D4AF37). Gives karaoke engagement lift without the "TikTok-y" feel — appropriate for editorial vlogs.

### 6.2 Typography

| Parameter | Value |
|---|---|
| Font | Montserrat Bold (700) |
| Size | 7–10% of frame height (60–80px for 1080×1920) |
| Fallback chain | Montserrat, Inter, Open Sans, Roboto, Helvetica Neue, sans-serif |

### 6.3 Position

| Aspect | Position |
|---|---|
| 9:16 (Vertical) | 65–85% from top, center-bottom |
| 16:9 (Landscape) | 75–90% from top |
| Width | Middle 80% of frame |
| Edge padding | 60px minimum |
| Shift to top | 10–25% when speaker face overlaps bottom-third |

### 6.4 Background Treatment

| Background | Value | When |
|---|---|---|
| Stroke + drop shadow | 4px black stroke + 2px drop shadow at 40% opacity | Clean backgrounds |
| Box fallback | rgba(0, 0, 0, 0.75) with 6px radius | Complex backgrounds |

Avoid box on clean backgrounds for editorial aesthetic.

### 6.5 Caption Limits & Timing

| Parameter | Value |
|---|---|
| Max chars per line | 37 |
| Max lines | 2 (3 for 9:16) |
| Line break | Natural clause boundaries |
| Display duration per block | 1.5–4s (sweet spot 2–3s) |
| Min duration | 1s |
| Max duration | 6s |
| Min gap between blocks | 2 frames |
| Reading speed | 180 wpm, max 20 chars/second |

### 6.6 Animation

| Element | Animation | Duration |
|---|---|---|
| Block enter | Slide-up fade-in, ease-out | 0.3s |
| Block exit | Fade-out, ease-in | 0.25s |
| Active-word highlight snap | Instant transition | 0.05s |
| Highlight color (editorial) | Gold #D4AF37 | N/A |
| Highlight color (modern/tech) | Cyan #00BFFF | N/A |

**Forbidden:** Bounce, typewriter, scale-up, particle effects on captions.

### 6.7 Contrast Compliance

- WCAG 2.1 AA: 4.5:1 minimum contrast ratio
- Target: 7:1 for readability
- White text (#FFFFFF) with dark background meets this

---

## 7. Intro & Hook Structure

### 7.1 The First 1.5 Seconds (Critical)

| Pattern | Visual | Audio | Duration |
|---|---|---|---|
| Hero shot | Slow-motion establishing of subject or environment | Ambient + soft riser | 1.5–3s |
| Detail hook | Extreme close-up of meaningful object, shallow DOF | Diegetic sound | 1.5–2.5s |
| Environment push-in | Slow push into workspace | Subtle drone or piano | 2–3s |
| Motion hook | Single deliberate movement (walking in, opening door) | Footsteps + ambient | 2.5–3s |

**Rule:** First frame must be the single most aesthetically composed shot. No text, no logo for the first 0.5s minimum.

**First-second audio:**
- Preferred: Diegetic sound (natural environment audio)
- Allowed: Soft ambient music (60–80 BPM, piano or strings, no beat drop)
- Never: Loud intro music, vocal stinger, voiceover starting at T=0 without visual context

### 7.2 Cold Open Structure

```
T=0 to T=5-10s: Cold open (single best 5-10s clip)
T=5-10s: Transition (0.5s dissolve or 1-frame black)
T=8-15s: Title card / name plate (3-5s)
T=10-15s: Curiosity hook (value proposition teaser)
Total intro: 8-20s max
```

**Retention decision window:**
- T=0–3s: 95–100% retention — hook must be visible by T=1.5s
- T=3–5s: 85–95% — first audio/visual pattern change
- T=5–10s: 70–85% — cold open payoff + transition
- T=10–15s: 60–75% — title card + value proposition
- T=15–30s: 55–65% — main content established

### 7.3 Title Card Rules

| Parameter | Value |
|---|---|
| Pre-pause | 2–3s (silence/stillness before card) |
| On-screen | 4–6s |
| Fade out | 0.5–1s (gentle ease-out) |
| Post-pause | 0.5–1s |
| Animation | Fade-in or slide-up, cubic-bezier(0.25, 0.1, 0.25, 1) |
| Typography | Serif for primary name, sans-serif for subtitle |
| Opacity | 90% (not 100%) |
| Letter-spacing | +0.05em for serif |
| Placement | Lower third left, 10% from bottom, 8% from left |
| Background | 40% opacity dark pill/gradient bar OR white text on dark footage (auto-detect) |

**Forbidden:** Scale-up, bounce, spin, 3D rotation, particle, glitch on title card.

### 7.4 Cold Open vs. Logo Intro Decision

| Condition | Recommendation |
|---|---|
| "Day in the life" / vlog | Cold open only (5–10s) |
| Returning audience / series | Compressed logo intro (2–3s) |
| Corporate / brand content | Logo intro only (3–5s) |
| Sponsored / branded hybrid | Cold open (5–8s) → short logo bumper (1.5–2s) |

**For "Day in the Life" format:** Must use cold open. Logo belongs at the end as a closing bumper.

### 7.5 Pattern Interrupts (Mid-Video Re-engagement)

Every 30 seconds (after first 60s), insert one of these:

| Type | Duration | When |
|---|---|---|
| Black frame + soft "thud" SFX | 0.15–0.3s | Every 45–60s |
| Single-word text overlay (serif) | 1–2s | Every 30–45s |
| Shot type contrast (wide → extreme CU) | Instant | Every 20–30s |
| Audio drop (music cuts to silence 1 beat) | 0.5–1s | Every 45–60s |
| Diegetic return (music fades, ambience swells) | 2–3s | Every 60–90s |
| Rapid montage (3–4 quick cuts, 0.5s each) | 2–3s total | At 50% mark |

**Forbidden in editorial:** Loud noise, flash frame, glitch, screen shake, speed ramp as interrupts.

### 7.6 Curiosity Gap Hook (After Title Card)

First verbal/on-screen statement after title card must create curiosity:
- "Here's how I structure my mornings" (process tease)
- "Most people get this wrong" (expertise framing)
- "This one change transformed my workflow" (transformation tease)
- "What does a day actually look like?" (curiosity question)

Duration: 3–5s. Tone: professional, calm, authoritative, understated.

---

## 8. Outro Patterns

### 8.1 8-Second Outro Sequence (for 59s Video)

| Time from end | Segment | Duration | Action |
|---|---|---|---|
| T–8s (51s) | Final thought | 2s | Speaker closes. Music begins –3dB fade. |
| T–6s (53s) | Series hook | 2s | "Next week: ..." text card, bottom-center |
| T–4s (55s) | CTA + Subscribe | 2s | Visual subscribe button bottom-right + verbal CTA |
| T–2s (57s) | Logo end card | 2.5s | Gold logo center, fade+scale animation |
| T–0.5s (58.5s) | Silence hold | 0.5s | Clean hold, no audio |

### 8.2 Music Fade

| Parameter | Value |
|---|---|
| Fade start | T–8s from video end (51s mark for 59s video) |
| Fade curve | Logarithmic |
| Duration | 7.5s — `afade=t=out:st=51:d=7.5:curve=log` |
| Level drop at start | –3dB (gentle attitude, not abrupt) |

### 8.3 CTA Rules (Editorial Style)

| Parameter | Value |
|---|---|
| Style | Soft identity — "subscribe if you build systems" |
| Mentions | One verbal mention only |
| Position | Bottom-right, 294×294px |
| Timing | Appears at T–4s from end |
| Stagger | Offset from series hook card (T–8s → T–4s) |

**Never:** "smash that like button," "don't forget to subscribe," aggressive CTAs.

### 8.4 Series Hook Card

| Parameter | Value |
|---|---|
| Formula | Reflect + curiosity gap + promise |
| Duration | 4s on screen |
| Position | Bottom-center |
| Typography | Sans-serif, gold accent on next topic |
| Example | "Next week: How I structure my deep work sessions" |

### 8.5 Logo End Card

| Parameter | Value |
|---|---|
| Animation | Fade + scale ease-in |
| Duration in | 1s |
| Hold | 1s |
| Color | Gold (#D4AF37) on dark background |
| Position | Center |
| Style | Minimal — no particles, glow, or 3D effects |
| Final audio | 0.5s silence hold after |

### 8.6 Outro Element Limits

| Rule | Value |
|---|---|
| Max end screen elements | 2 (video recommendation + subscribe) |
| Stagger timing | Elements appear sequentially, not all at once |
| Total outro duration | 7–9s (8s optimal for 59s format) |
| Final frame | Clean hold, text gone, logo settled |

---

## Appendix: Platform-Specific Adjustments

| Aspect | 59s Reels/Shorts | 6–10min YouTube |
|---|---|---|
| Clip duration | 1.5–3s average | 4–12s average |
| Cuts per minute | 25–40 | 10–20 |
| Hook phase | 8s total | 15–20s total |
| Subtitle size | 7–10% frame height | 5–7% frame height |
| Subtitle position | 65–85% down | 75–90% down |
| Music ducking | –10 dB | –6 dB (gentler) |
| Transition dissolve | 6 frames | 12–24 frames |
| Outro duration | 8s | 15–20s |

---

## Appendix: Configuration Constants Reference

```python
# Pacing
MIN_CLIP_DURATION = 1.0  # seconds
MAX_SAME_SHOT_TYPE_CONSECUTIVE = 2
VISUAL_SHIFT_INTERVAL = (3.0, 7.0)  # seconds
ENERGY_INJECTION_INTERVAL = (8.0, 15.0)  # seconds
MAX_SLOW_BEFORE_CUT = 10.0  # seconds
TARGET_CUTS_PER_MINUTE = (25, 40)
MAX_SILENCE_GAP = 1.5  # seconds
JUMP_CUT_MIN_ANGLE_CHANGE = 30  # degrees

# Transitions
HARD_CUT_RATIO = 0.90  # 90% of all transitions
DIP_TO_BLACK_DURATION = (0.5, 1.0)  # seconds
DIP_TO_WHITE_DURATION = (0.33, 0.66)  # seconds
MAX_DIP_TO_WHITE_PER_VIDEO = 2
MICRO_DISSOLVE_FRAMES = (4, 6)
STANDARD_DISSOLVE_FRAMES = (12, 24)

# Audio
VOICE_NORMALIZATION_TARGET_LUFS = -14
VOICE_COMPRESSION_RATIO = 2.0
VOICE_ATTACK_MS = 15  # 10-20 range
VOICE_RELEASE_MS = 75  # 50-100 range
VOICE_THRESHOLD_DBFS = -18
VOICE_HPF_HZ = 90  # 80-100 range
VOICE_PRESENCE_BOOST_DB = 1.5  # at 4kHz
MUSIC_DUCKING_LEVEL_LUFS = -24  # 10dB below voice
MUSIC_PAUSE_LEVEL_LUFS = -20
MUSIC_DUCK_ATTACK_MS = 20
MUSIC_DUCK_RELEASE_MS = 300
MUSIC_HPF_HZ = 250
MUSIC_SCOOP_DB = -2.5  # at 2kHz
AMBIENCE_LEVEL_LUFS = -33  # -30 to -36 range
AMBIENCE_CROSSFADE_MS = 500
SFX_WHOOSH_DURATION_MS = 300  # 200-400 range
SFX_HIT_DURATION_MS = 150  # 100-200 range
SFX_RISER_DURATION_S = 2.0  # 1-3 range

# Motion Graphics
LOWER_THIRD_ENTRY_S = 0.40
LOWER_THIRD_HOLD_S = 4.0
LOWER_THIRD_EXIT_S = 0.30
HUD_BG_COLOR = "rgba(18, 20, 28, 0.55)"
HUD_BLUR_PX = 12
BRAND_BUG_SIZE_PCT = 0.05  # 5% of frame width
BRAND_BUG_OPACITY_FULL = 0.65
BRAND_BUG_OPACITY_PERSIST = 0.30

# Color
SKIN_HUE_PROTECTION = (0, 40)  # degrees
SCENE_OFFICE_TEMP_K = 5600
SCENE_OUTDOOR_TEMP_K = 5600
SCENE_HOME_ACCEPT_TEMP_K = 4000  # 3800-4200 range
COMPRESSION_SATURATION_BOOST = {"youtube": 1.0, "instagram": 1.08, "tiktok": 1.12}

# Captions
CAPTION_FONT_SIZE_PCT = 0.085  # 7-10% of frame height
CAPTION_MAX_CHARS_PER_LINE = 37
CAPTION_MAX_LINES = 2  # 3 for 9:16
CAPTION_DISPLAY_MIN_S = 1.5
CAPTION_DISPLAY_MAX_S = 6.0
CAPTION_DISPLAY_SWEET_SPOT_S = 2.5  # 2-3 range
CAPTION_ENTER_DURATION_S = 0.30
CAPTION_EXIT_DURATION_S = 0.25
CAPTION_WORD_HIGHLIGHT_TRANSITION_S = 0.05
CAPTION_HIGHLIGHT_COLOR = "#D4AF37"  # gold
CAPTION_DIM_COLOR = "rgba(255, 255, 255, 0.6)"
CAPTION_BG_COLOR = "rgba(0, 0, 0, 0.75)"
CAPTION_MAX_CHARS_PER_SECOND = 20
CAPTION_READING_SPEED_WPM = 180
CAPTION_LINE_BREAK_STYLE = "clause"  # natural clause boundaries

# Intro/Hook
HOOK_FIRST_DEADLINE_S = 1.5  # hook must be visible by 1.5s
HOOK_COLD_OPEN_DURATION = (5.0, 10.0)
HOOK_NO_TEXT_FOR_S = 0.5  # no text in first 0.5s
HOOK_NO_LOGO_FOR_S = 3.0  # no logo in first 3s
TITLE_CARD_PRE_PAUSE_S = 2.5  # 2-3 range
TITLE_CARD_ON_SCREEN_S = 5.0  # 4-6 range
TITLE_CARD_FADE_OUT_S = 0.75  # 0.5-1 range
TITLE_CARD_POST_PAUSE_S = 0.75  # 0.5-1 range
PATTERN_INTERRUPT_INTERVAL_S = 30  # after first 60s

# Outro
OUTRO_TOTAL_DURATION_S = 8.0
OUTRO_MUSIC_FADE_START_S = 8.0  # seconds from end
OUTRO_MUSIC_FADE_DURATION_S = 7.5
OUTRO_CTA_POSITION = "bottom_right"
OUTRO_CTA_SIZE_PX = 294
OUTRO_LOGO_COLOR = "#D4AF37"
OUTRO_MAX_ELEMENTS = 2
OUTRO_FINAL_SILENCE_S = 0.5
```
