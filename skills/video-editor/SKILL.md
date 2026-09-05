---
description: "LEGACY — superseded by skills/video-agent/SKILL.md (v1.4+). Keep ONLY as an editorial-rules reference (Hollywood gate, GSAP patterns, caption timing) cited by docs/motion-graphics-spec.md. Do NOT use for production builds — video-agent is the master."
---

# Video Editor

> **LEGACY — production rule of record is `skills/video-agent/SKILL.md` (v1.4+).**
> This file is kept as the editorial-rules reference only. If a rule here conflicts with
> video-agent, video-agent wins. Notably: NO MUSIC on any video (all music sections below
> are dead), SFX ≤ -18dB vs voice, burned-in word-synced captions in shorts.

## Workflow

```
You: footage in folder X
 Me: scan filenames -> propose shot list (HITL) -> trim clips -> build composition (index.html) -> check -> render -> deliver
```

## Technical Procedures

### 1. Trim Clips

```bash
# From source folder, copy clips to the project media/ dir
# Use offset (0.5-1.5s) to skip shaky starts, use middle of footage
# Near-lossless quality: CRF 5, preset slow
ffmpeg -y -ss <OFFSET> -i <SOURCE_FILE> -t <DURATION> \
  -c:v libx264 -preset slow -crf 5 media/<NUM>.mp4

# Renumber sequentially: 01.mp4, 02.mp4, etc.
```

### 2. Download SFX (Playwright MCP)

Use Playwright MCP browser to download from pixabay.com. NO music ever — superseded by the video-agent v1.2.0 no-music rule (music banned on all videos, any runtime):

| File | Search term | Purpose |
|---|---|---|
| `whoosh_sfx.mp3` | pixabay.com/sound-effects/search/whoosh/ | Scene transitions |
| `impact_sfx.mp3` | pixabay.com/sound-effects/search/impact/ | Title card reveals, numbered pills |
| `riser_sfx.mp3` | pixabay.com/sound-effects/search/riser/ | Build tension before climax |

Steps per file:
1. Open browser to pixabay.com → search → click result
2. Click "Free download" → file saves to ~/Downloads/
3. `cp ~/Downloads/<FILE> <project>/media/<NAME>.mp3`

### 3. Build the Composition

Copy a format template from `templates/short-form/<format>/` (each is a complete HyperFrames project). Replace the placeholder footage slots and text. Structure:

- Root `<div>` with `data-composition-id`, `data-start="0"`, `data-width`, `data-height`, `data-duration`
- One clip per scene: `class="clip"`, `data-start`, `data-duration`, `data-track-index`
- Media via `<video>`/`<audio>` elements (framework owns playback — see `hyperframes-core` → `variables-and-media.md`)
- One paused GSAP timeline on `window.__timelines["<id>"]`
- Validate with `npx hyperframes check` before rendering

### 4. Scene Transitions (No Black Gaps)

Black screens between scenes is amateur editing. Replace all gaps with creative transitions:

| Transition | Motion | Duration | When to use |
|---|---|---|---|
| **Zoom out** | scale 1.0→1.12 + blur 0→4px on clip end | 0.2s | Hook→BTS, energetic shifts |
| **Blur morph** | blur 0→8px on clip end, next clip starts blur 5→0 | 0.33s | Setup→Points, tone changes |
| **White dip** | White overlay opacity 0→1 on clip end | 0.33s | Before CTA, aspirational moments (max 1 per video) |
| **Hard cut** | Instant | 0s | Default — use for 70%+ of cuts |
| **Zoom in** | Next clip starts scale 0.92→1.0 + blur 3→0 | 0.13s | BTS jump cuts, fast-paced |

**Rules:** never more than 7 transitions total in 60s; never the same type twice in a row; one deliberate breather before CTA; keep the post-credits pause.

### 5. Color Grading Filters

Apply as CSS filters on the `<video>` elements:

| Filter | Effect | Use for |
|---|---|---|
| `brightness(1.05) contrast(1.1) saturate(1.1)` | Warm, punchy | Hook, CTA |
| `brightness(1.02) contrast(1.05) saturate(1.0)` | Neutral, warm | Setup |
| `brightness(1.0) contrast(1.05) saturate(0.95)` | Cool, focused | Points |
| `brightness(0.95) contrast(1.05) saturate(0.9)` | Muted, desaturated | Transition breathers |
| `brightness(1.1) saturate(0.9) sepia(0.08)` | Warm sepia, nostalgic | Kicker |
| `brightness(1.05) contrast(1.1) saturate(1.1)` | Warm punchy | CTA bookend |

## Render Command

```bash
npx hyperframes render   # from the project dir; see hyperframes-cli for flags
```

- Resolution: 1728x3072 (native DJI 3K portrait) or 1080x1920 for platform-native
- FPS: 30 (matches source footage)
- Master: `--crf 10`; social re-encode at CRF 14 via ffmpeg (avoids platform re-compression)

## HITL Checkpoints

1. **Shot list** — propose order + titles → you approve
2. **Rough cut** — first render → you review (mute clips? change titles? adjust filters?)
3. **Final** — apply changes → render master → deliver

## Posts (AUTOMATIC after final render — social copy, not burned captions)

After the master renders, write per-platform post copy using the post-writer skill (`skills/post-writer/SKILL.md`) and save to `<project>/captions.md`. Always run AFTER the render so the hook text, beat times, and CTA in the posts match the final edit.

1. Give the LLM the exact final hook text, beat structure with REAL times, and CTA from the composition.
2. Apply the hard voice rules: zero em-dashes, zero emoji, Grade 5-6 words, human typed-quickly feel, no day numbers, no employer names.
3. Detailed posts that max out platform limits; first ~100 chars = hook + save CTA.
4. Verify YouTube Long timestamps against the actual edit times (not guessed).
5. Save to `<project>/captions.md`.

---

# HOLLYWOOD EDITORIAL

## Lessons Learned (Never Repeat)

| # | Mistake | Why It Failed | Fix |
|---|---|---|---|
| 1 | Shuffled clip order | Filenames encode the story sequence. Director shot them in order | Keep clips in filename order: 01, 02, 03... Never reorder. |
| 2 | Used same clip multiple times | Violates "one clip, one use." Viewer sees recycled footage | Each clip plays once. Use transition clips for variety. |
| 3 | Imported B-roll from other dates | The source folder has all clips needed. Extra B-roll distracts | Only use clips from the target folder. |
| 4 | Missed built-in transitions | BTS clips are the periods between sentences | Treat them as muted breathers that separate story beats. |
| 5 | Hardcoded keyword lists for captions | Fragile. Misses words. Breaks when captions change | Use broad theme-based matching or skip highlighting. |
| 6 | Over-complicated music automation | Too many keyframes. Hard to debug. Crashes | Keep it simple: 12-18 keyframes max. Per-act volume mapping. |
| 7 | First version flattened the story | Tried to add external B-roll, reorder clips, invent structure. The story already exists | Read the transcript. Clips tell the story in order. Your job is to ENHANCE, not rewrite. |

## The 8-Beat Story Structure

Every video has this natural arc embedded in the clip sequence (filenames 01-11):

```
01 — HOOK        Opening statement, grabs attention
02 — TRANSITION  BTS breather (muted, 2-3s)
03 — SETUP       Context, "what this is about"
04 — ROADMAP     Preview of what's coming
05 — POINT 01    First key idea
06 — POINT 02    Second key idea
07 — POINT 03    Third key idea
08 — TRANSITION  Mid-roll breather (muted, 3-4s)
09 — KICKER      The big line, emotional peak
10 — TRANSITION  Humor/personality beat (muted)
11 — CTA         Call to action
```

Transition clips (02, 08, 10): muted audio, desaturated filter, 2-4s max.

## Platform Safe Zones (Text Overlays)

TikTok / IG Reels / YouTube Shorts cover the extreme top and bottom of the frame with UI. Validated on the 2026-07-31 desk-setup video.

| Rule | Value |
|---|---|
| Vertical safe band | Text between **y=20%** and **y=80%** of frame height |
| Top margin | Keep clear of 0-20% (top UI) — hero text starts at/below **20%** |
| Bottom margin | Keep clear of 75-100% (caption + action UI) — no text below **~65%** |
| Side margins | **8% padding** on left and right (0-8% and 92-100% clear) |
| Container | `padding: 0 8%; text-align: center;` on every text block |

Also add a **text scrim** (soft gradient band behind the text zone, e.g. `linear-gradient` black 0.34 alpha) so type stays legible regardless of footage brightness.

## HUD

### Progress Bar (REQUIRED)
Always include a thin progress bar at the very top of the frame.

| Property | Value |
|---|---|
| Position | Top, full width |
| Height | **10px** (3K 1728x3072; scale proportionally) |
| Background track | `rgba(255,255,255,0.06)` |
| Fill | `linear-gradient(90deg, #D4AF37, #F5D97A)` |
| Animation | GSAP width tween L→R matching `frame / totalFrames` |
| Z-index | Highest (above everything) |

No other persistent HUD elements.

### Visual Effects

| Element | Position | Style |
|---|---|---|
| Film grain | Full overlay | 80 random dots at 0.03 opacity |
| Vignette | Full overlay | Inset shadow, 0.15→0.30 across runtime |

## Brightness Determination (Dynamic)

Do NOT hardcode a single brightness value. Determine per clip by lighting + skin tone:

1. **Look at the clip's lighting** — indoor, outdoor, shade, mixed?
2. **Look at the speaker's skin tone** — brown/Indian skin needs higher brightness (1.2-1.6) to avoid looking dark. Fair skin: 1.0-1.2.
3. **Check clip exposure** — bright background → lower brightness; dark background → higher.
4. **Rule of thumb:** When in doubt, go brighter. A slightly overexposed face is better than a face that disappears.

Reference values for Indian skin on DJI Osmo Pocket 3 footage:

| Condition | Brightness | Contrast | Saturation |
|---|---|---|---|
| Bright indoor (well-lit office) | 1.25 | 1.08 | 1.1 |
| Dark indoor (low light, evening) | 1.6 | 1.05 | 1.0 |
| Outdoor shade | 1.4 | 1.05 | 0.95 |
| Outdoor direct sun | 1.15 | 1.1 | 1.1 |
| Transition/BTS clips | 1.25 | 1.0 | 0.9 |
| Kicker/emotional moment | 1.2 | 0.95 | 0.9 + sepia(0.06) |

## Font Sizes for 3K (1728x3072)

All sizes MUST be ×1.6 from standard 1080p reference. Bundle fonts locally (fonts/*.woff2) for deterministic renders.

| Element | 3K Size | Font Family | Weight |
|---|---|---|---|
| Hero hook title | **78px** | Playfair Display | 700 |
| Setup title | **60px** | Playfair Display | 700 |
| Numbered cards (pills) | **56px** number / **36px** label | JetBrains Mono / Space Grotesk | 700 / 600 |
| Kicker reveal | **90px** | Playfair Display | 700 |
| Kicker subtitle | **18px** | JetBrains Mono | 400 |
| Captions | **46px** | Space Grotesk | 500 |
| End card title | **70px** | Playfair Display | 700 |
| End card subtitle | **16px** | JetBrains Mono | 400 |
| Pillar circles | **140px** diameter | — | — |
| Brand text (mono) | **12-16px** | JetBrains Mono | 400 |

Fonts: **Playfair Display** (serif — hero, kicker, end card), **Space Grotesk** (sans — captions, labels), **Inter** (sans — fallback), **JetBrains Mono** (mono — numbers, code).

## Captions

Only when needed — not every scene. Key spoken lines only.

| Property | Value |
|---|---|
| Font | Space Grotesk, 46px, weight 500 |
| Position | bottom: 12%, centered, padding: 0 40px |
| Background | rgba(0,0,0,0.55) with backdrop-filter: blur(6px) |
| Border | Left gold accent: 3px solid #D4AF37 |
| Padding | 24px 48px |
| Key words | Highlight in #D4AF37 |
| Fade in/out | 0.3s |

**Caption Timing Rule:** appear 0.3-0.5s AFTER the speaker starts (not simultaneous); disappear 0.3-0.5s BEFORE the speaker finishes. Min 1.5s, max 4s. Never cut mid-word. Never show captions during transition clips.

**Clip Duration Determination:** trim to speaking start/end from transcript, +0.5s padding (15f headroom, 15f tail). Never trim mid-sentence. If a clip is 10s but speech is 4s, trim to 4.5s.

## Sound Design Rules

### NO MUSIC (video-agent v1.2.0 rule, supersedes everything below)
Music beds are BANNED on all videos, any runtime. SFX only — see the SFX Cue Points table below.

### Music Automation (per-act)
REMOVED — no music element exists. Do not add a music `<audio>` track or volume automation to any composition.

### Music Selection by Content Tone
REMOVED — no music. Skip this table entirely.

### SFX Cue Points

| SFX | Count | Location | Volume |
|---|---|---|---|
| Whoosh | 2-3 | Act boundaries, before transition clips | 0.18 |
| Impact | 3 | On each numbered card/pillar reveal | 0.22 |
| Riser | 1 | 1s before kicker climax | 0.20 |

### Beat Sync
No music — beat sync applies only when the footage itself has a detectable beat. Otherwise smooth interpolations.

## No Two Videos Look Alike — Variety System

Every video MUST differ from the last on ALL of these dimensions:

1. **VFX Treatment:** film grain, light leaks, color halation, lens flare, analog noise, chromatic aberration. Never same combo twice.
2. **Cut Rhythm:** Fibonacci-like durations. Never 3 consecutive clips the same duration. `[2s, 3s, 5s, 3s, 2s, 4s, 6s, 2s, 5s, 3s, 4s]` good; `[3s,3s,3s,4s,4s,4s]` bad.
3. **Motion Graphic Template:** pillars, hero-word blur-in, split-screen, charts, timeline reveal, card flip. Never repeat back-to-back.
4. **Motion/Audio Variation:** SFX pattern (whoosh/impact/riser placement), beat structure, sound-design texture. Never same twice in a row. (No music dimension — music is banned.)
5. **Title Animation:** word-by-word bounce, single-line slide-up, blur-in, letter-by-letter, mask wipe, scale settle. Never repeat.
6. **Color Grade:** warm golden, cool teal, neutral clean, high-contrast BW-split, vintage film. Never repeat.
7. **Font Pairing:** Playfair+Space Grotesk, Inter+JetBrains Mono, DM Serif+Work Sans, Fraunces+Satoshi. Never same twice.

**Plus the fingerprint dimensions** — hook style, CTA type, beat structure, SFX pattern, length, grade direction, text layout, transition style, aspect ratio. Full option lists with row numbers in `docs/font-color-rotation.md` (12 dimensions). Pick a fingerprint (D1-D12 row numbers) different from the last video in `docs/post-tracker.md`, then log it after render. No two videos share the same combination.

## Pre-Render Checklist

- [ ] Clips in director's order (01→02→03→...)
- [ ] Each clip used exactly once
- [ ] Transition clips identified and muted
- [ ] Burned-in captions present on ALL videos — compulsory in shorts, no exceptions
- [ ] No music track present (banned — SFX only)
- [ ] Full-screen motion graphics at key moments
- [ ] Color grade progression matches emotional arc
- [ ] SFX at 2-3 key moments (not every transition)
- [ ] No black gaps between scenes — hard cuts or transitions
- [ ] Progress bar active (gold gradient, top)
- [ ] Film grain + vignette active
- [ ] Duration respects story pace (not forced to 60s)
- [ ] VFX/title/font/SFX all different from last video (post-tracker)
- [ ] Fingerprint (D1-D12) different from last video — check docs/font-color-rotation.md + post-tracker
- [ ] `npx hyperframes check` passes
- [ ] Post tracker updated after render (fingerprint row)
- [ ] Posts written to <project>/captions.md after render (post-writer skill)

## Pre-Render Approval Workflow

**ALWAYS present a full scene-by-scene breakdown before rendering. Never skip this.**

| Field | What to describe |
|---|---|
| **Video** | Which clip, what it shows, what grade/filter |
| **Audio** | SFX at this moment |
| **Motion Graphics** | What overlay, what animation, where |
| **Transition** | How it ends (hard cut, zoom, SFX) |

Plus a creativity assessment: color arc, sound design, motion graphics, transitions, pacing.

### Hollywood-Style Gate
Before starting any edit, verify:
- [ ] Full-screen motion graphic at the kicker moment?
- [ ] Visual treatment for transition clips? (Muted + desaturated + shorter)
- [ ] No music track present (banned — SFX only)
- [ ] Color grade progression? (Changes across the arc)
- [ ] At least 2 SFX cue points?
- [ ] A personality/humor moment?
- [ ] Progress bar + film grain + vignette active?
- [ ] Would a viewer say "professionally edited" not "templated"?
- [ ] Visually distinct from the last video?

If any answer is no, redesign the missing element before proposing.

## Autonomy Rules for the Orchestrator

When given a new footage folder and asked to make a video:

1. **Read all filenames** — they encode the story order.
2. **Transcribe each clip** — faster-whisper or similar. The transcript IS the script.
3. **Identify clip roles**: content (spoken) vs transition (BTS, breathers, humor). Transition clips are usually shorter, awkward, self-aware.
4. **Pick the format template** from `templates/short-form/` that matches the story — never the same as the previous video.
5. **Choose fonts** — different pairing from last time.
6. **Set brightness** — dynamically by clip lighting + skin tone. Default 1.25 minimum for brown skin.
7. **Design SFX placement** — 2-3 cue points, never flat. No music track at all.
8. **Add SFX** — 2-3 cue points. Never 0, never more than 5.
9. **Build the composition** — clips in order, each once. No black gaps. Full-screen motion at key moments.
10. **Present scene-by-scene breakdown** — get approval before rendering.
11. **Render** — master CRF 10, social CRF 14.
12. **Log lessons** — what worked, what didn't.

Never skip step 10. Never use a clip twice. Never import footage from other folders unless asked. Never use the same template as the previous video.

## Transition Clip Identification

1. **Filename** — contains "transition", "bts", "blooper", "filler", "take", "mistake" → transition.
2. **Transcript** — no clear spoken message (filler, laughter, "let me", camera adjustments) → transition.
3. **Duration** — transition clips are typically <4s vs >4s.
4. **Rule:** not a complete thought → transition. Mute, desaturate, trim to 2-4s.

**Generic structure:** `[Content×N] → [Transition] → [Content×N] → [Transition] → [Content] → [Transition] → [Content]`. No transition clips → add hard cuts instead. More than 3 → keep the 3 most distinct. LAST clip is always CTA, FIRST is always hook.

## Layout Rules

### "Nothing Centered" Rule
**No element should ever be vertically centered in the frame.** Center of frame shows the speaker/video.

60/40 split:
- **Top 60%**: Titles, motion graphics, visual elements
- **Bottom 40%**: Speaker's face visible, captions below

Exception: full-black end card — even then text sits higher than dead center.

### Creative transitions (see above) — hard cut is the default.

---

## Vox-Style Production Reference

Vox's visual explainer style is the gold standard for educational short-form. Their formula (framework-neutral — implement with GSAP in HyperFrames):

### Core Principles

| Principle | How |
|---|---|
| **Kinetic typography** | Text never static — words animate in one by one, or phrases slide/fade |
| **Full-screen takeovers** | Every 3-5 seconds the ENTIRE screen changes. Video is accent (15-20%), graphics primary (80-85%) |
| **Card-based structure** | Each key point gets its own full-screen card (text + icon + data) |
| **Hand-drawn aesthetic** | Imperfect circles, sketch arrows, rough annotations (SVG stroke-dasharray) |
| **Data visualization** | Animated bar charts, line graphs, pie charts that draw in as narrator speaks |
| **Map storytelling** | Routes animate with path drawing, markers pulse (SVG) |
| **Color-coded sections** | Each chapter gets a distinct color — creates visual memory |
| **Icon-driven concepts** | Simple SVG icons animate in before text |

### Visual Grammar

| Element | When | Animation |
|---|---|---|
| **Big number** | List/count | Scale 0.5→1.0 with bounce, accent color |
| **Quote card** | Key line | Full-screen dark bg, serif, fade in with blur |
| **Bar chart** | Comparing quantities | Bars grow bottom→target, staggered |
| **Line graph** | Trends over time | SVG stroke-dashoffset draw, points pulse |
| **Map pin** | Locations | Pin drops with bounce, ripple ring expands |
| **Timeline** | Chronology | Line draws, nodes stagger in |
| **Split screen** | Comparison | Panels slide apart, A→B transition |
| **Callout** | Highlight a detail | Magnifier zooms in, line to label |

### Pacing Rules

- **1 frame = 1 idea.** No screen with more than one main visual plus supporting text.
- **3-5 second rule.** If a frame stays the same >5s, viewer loses interest.
- **Text first, then audio, then visual.** Text appears (0.5s) → narrator reads (2s) → visual illustrates (2s) → cut.
- **Sound design minimal.** Light whoosh on transitions, subtle pop on data. No music track.
- **Voice is king.** Voice = 0dB, SFX = -6dB.

### GSAP Patterns

```js
// 1. Kinetic text — words stagger in
words.forEach((_, i) => tl.fromTo(`#w${i}`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }, 0.2 + i * 0.12));

// 2. Bar chart bar grow
tl.fromTo("#bar1", { width: 0 }, { width: "60%", duration: 0.5, ease: "power2.out" }, 2.0);

// 3. SVG line draw
tl.fromTo("#path", { strokeDashoffset: pathLen }, { strokeDashoffset: 0, duration: 2, ease: "none" }, 3.0);

// 4. Card slide in
tl.fromTo("#card", { x: 1080, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.1);
```

### Color System

Vox uses a restrained palette with one or two accents per video:

| Role | Primary | Accent | Background |
|---|---|---|---|
| Default | White (#FFFFFF) | Gold (#D4AF37) | Dark navy (#0A0A1A) |
| Researcher | White | Red (#E74C3C) | Dark red overlay |
| ML Engineer | White | Blue (#3498DB) | Dark blue overlay |
| AI Engineer | White | Gold (#D4AF37) | Dark gold overlay |

Max 3 colors per video. Use opacity variants (33, 44, 66, 88, BB) for depth.

### No Emoji Rule
Zero emoji in any composition text, captions, or overlays. No exceptions. Plain text or special characters only.

---

## Video Agent System

See `skills/video-agent/` for the production system:

| File | Purpose |
|---|---|
| SKILL.md | Template selection, tech stack, rules |
| technologies/easing.md | AE-quality motion curves (GSAP) |
| technologies/gsap.md | GSAP — the HyperFrames runtime |
| technologies/lucide.md | Icon system (Brain, Server, AppWindow) |
| technologies/fonts.md | Fonts, sizing, pairings |
| transitions/README.md | Transition catalog |
| rotations/README.md | Variety/rotation system |
| layouts/README.md | Layout patterns |
