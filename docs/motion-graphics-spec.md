# Motion Graphics Technical Specification

> Codeable rules for the AI-powered automatic video editing pipeline.
> Style: MINIMAL, EDITORIAL, LUXURY (Monocle, Apple commercial, high-end corporate).
> Reference frame: **1920x1080 (16:9)** — all values percentage-based for resolution independence.
> Reference frame alt: **1080x1920 (9:16)** — for vertical/Reels output.
> Aligned with `persona.yaml` brand identity: Obsidian, Alabaster, Gold, Silent Gray.

---

## 1. Lower Third Animation

### 1.1 Position (Safe Area)

Lower thirds sit in the **bottom-left title-safe zone** — never center, never right. This follows the Monocle/Apple editorial convention: left-aligned, anchored to the frame edge, never floating mid-frame.

| Parameter | Value (16:9) | Value (9:16) |
|---|---|---|
| Horizontal padding from left edge | **5% of frame width** (96px at 1920x1080) | **4%** (43px at 1080x1920) |
| Vertical from bottom edge | **8% of frame height** (86px at 1920x1080) | **6%** (115px at 1080x1920) |
| Max width | **55% of frame width** (1056px at 1920x1080) | **70% of frame width** (756px) |
| Text alignment | **Left** — always left-aligned | Left |

### 1.2 Typography

Reference the `persona.yaml` brand system. The lower third uses a two-line hierarchy: **name line** (larger, bold) and **descriptor line** (smaller, regular weight, tracked out).

| Property | Name Line (top) | Descriptor Line (bottom) |
|---|---|---|
| Font | Inter (from brand: `fonts.primary`) | Inter |
| Size (16:9) | **32px** (1.7% of frame height) | **22px** (1.1%) |
| Size (9:16) | **28px** (1.5%) | **18px** (0.9%) |
| Weight | **600 (Semi-Bold)** | **400 (Regular)** |
| Color | `alabaster` (#FAFAFA) at 95% | `alabaster` at 70% |
| Letter-spacing (tracking) | **0.04em** | **0.08em** |
| Line height | 1.3 | 1.3 |
| Vertical gap between lines | **8px** | — |
| Case | **Sentence case** | UPPERCASE (or sentence) |
| Text shadow | `0 2px 8px rgba(0,0,0,0.5)` | Same |

### 1.3 Gold Accent Bar

Each lower third is preceded by a thin gold bar — the signature editorial flourish.

| Parameter | Value |
|---|---|
| Position | Above name line, left-aligned |
| Width | **40px** (animated: grows from 0 to 40) |
| Height | **3px** |
| Color | `gold` (#D4AF37) |
| Border radius | **2px** |
| Margin below bar | **16px** (gap to name line) |
| Animation | Width interpolates 0 → 40px over **0.25s** (first 40% of entry) |

### 1.4 Animation Timing

| Phase | Duration | Easing | Notes |
|---|---|---|---|
| **Entry** | **0.40s** (12 frames at 30fps) | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Deceleration curve |
| **Hold** | **4.0s** | — | Adjust per line length (180 wpm reading speed) |
| **Exit** | **0.30s** (9 frames) | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` | Acceleration curve |
| **Total on-screen** | **4.7s** | — | In + hold + out |
| **Stagger (multi-line)** | **0.08s** between lines | — | Second line enters after first |

### 1.5 Entry Animation

Preferred luxury style: **fade + slide from left** with a subtle blur dissolve.

| Property | Entry | Exit |
|---|---|---|
| Opacity | 0 → 1 | 1 → 0 |
| Slide X | **-48px → 0** (from left) | 0 → **-30px** (slide left out) |
| Slide Y | None | None |
| Blur (gaussian) | **8px → 0px** over entry duration | 0 → 4px |
| Easing | Deceleration | Acceleration |

### 1.6 GSAP Implementation Reference

```js
// Core pattern — reusable across all lower third instances (on the master timeline)
const ENTRY = 0.4;   // seconds
const EXIT = 0.3;
const HOLD = 4.0;

// entry: slide from -48px + fade, cubic deceleration
tl.fromTo("#lt", { opacity: 0, x: -48 }, { opacity: 1, x: 0, duration: ENTRY, ease: "power3.out" }, t0);
// gold bar: width 0 → 40px
tl.fromTo("#bar", { width: 0 }, { width: 40, duration: 0.2, ease: "power2.out" }, t0);
// exit: fade + slide down
tl.to("#lt", { opacity: 0, y: 20, duration: EXIT, ease: "power2.in" }, t0 + ENTRY + HOLD);
```

---

## 2. Text Reveal / Kinetic Typography

Used for: pull quotes, key stats, emphasis lines, section headers within the video. Not for captions (see `caption-styling-research.md` for those).

### 2.1 Positioning

| Placement | Vertical (from top) | Horizontal |
|---|---|---|
| **Hero quote** (full screen) | **38–45%** from top (centered vertical band) | **Center** at 50% |
| **Lower emphasis** | **65–72%** from top | **Center** at 50% |
| **Top header** (timestamp, location stamp) | **3%** from top, **4%** from left edge | **Left** |
| **Section marker** (chapter title) | **42%** from top | **Left** at 5% inset |
| Max line width (single) | — | **70% of frame width** |
| Max line width (multi) | — | **60% of frame width** |

### 2.2 Typography — Display Text

| Property | Hero / Headline | Body / Subtitle | Kicker / Label |
|---|---|---|---|
| Font | Inter (primary) | Inter | Inter |
| Size (16:9) | **56px** (2.9% of frame height) | **28px** (1.5%) | **18px** (0.9%) |
| Size (9:16) | **48px** (2.5%) | **24px** (1.25%) | **16px** (0.8%) |
| Weight | **700 (Bold)** | **400 (Regular)** | **500 (Medium)** |
| Color | `alabaster` #FAFAFA | `alabaster` at 80% | `gold` #D4AF37 |
| Letter-spacing | **-0.02em** (tight) | **0.02em** | **0.12em** (wide, uppercase) |
| Line height | **1.2** | **1.5** | **1.4** |
| Case | Sentence | Sentence | **UPPERCASE** |
| Text shadow | `0 2px 12px rgba(0,0,0,0.5)` | Same, lighter | None |

### 2.3 Entry Animation Styles

**Primary style (editorial): Per-word fade + slide up**

| Parameter | Value |
|---|---|
| Words appear | **Left to right**, one word at a time |
| Per-word delay | **0.10s** between words |
| Per-word duration | **0.20s** fade + slide |
| Slide distance | **24px** upward (from below final position) |
| Opacity curve | 0 → 1 over the per-word duration |
| Easing | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` |
| Max total entry time | **2.0s** for an 8-word line |
| Stagger between lines | **0.15s** gap after prior line finishes |

**Secondary style (minimal): Full-line fade up**

| Parameter | Value |
|---|---|
| Entire line fades in | **0.35s** duration |
| Slide up distance | **20px** (translateY) |
| Opacity | 0 → 1 |
| Easing | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` |

**Kicker/label style: Gold bar + text**

Kicker always appears with the gold accent bar (same as lower third).

| Parameter | Value |
|---|---|
| Gold bar animates first | 0 → 40px width over **0.25s** |
| Text follows | After 0.10s delay — **0.30s** fade + slide up |
| Total entry | **0.65s** for the kicker-bar pair |

### 2.4 Hold & Exit

| Phase | Duration | Easing |
|---|---|---|
| **Hold** | **3.0–5.0s** (depends on reading time) | — |
| **Exit: fade out** | **0.30s** | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` |
| **Exit: slide down** | **0.35s**, translateY +20px | Same |
| Exit delay (from block end) | **0.50s** before next block enters | — |

### 2.5 Word-by-Word GSAP Pattern

```js
// Per-word reveal — each word is its own span element
const WORDS_GAP = 0.10;   // seconds between words
const WORD_FADE = 0.20;   // fade duration per word

const words = text.split(" ");
words.forEach((word, i) => {
  const el = document.getElementById(`w${i}`);
  tl.fromTo(el, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: WORD_FADE, ease: "power3.out" }, t0 + i * WORDS_GAP);
  // Render each word with display:inline-block and margin-right: 8px
});
```

---

## 3. HUD Overlay Positioning

HUD elements display data overlays: calendar items, meeting times, stats counters, code metrics, location data. They must feel **instrument-panel precise**, never decorative.

### 3.1 Frame Positions

Two primary positions are used — never more than two HUD elements on screen simultaneously.

#### Position A — Top-Left Info Stamp
| Parameter | Value (16:9) | Value (9:16) |
|---|---|---|
| Inset from left | **4%** (77px) | **4%** (43px) |
| Inset from top | **3%** (32px) | **3%** (58px) |
| Max width | **30% of frame width** (576px) | **40%** (432px) |
| Content | Location, date, time, weather — text-only | Same |

#### Position B — Bottom-Left Metric Card
| Parameter | Value (16:9) | Value (9:16) |
|---|---|---|
| Inset from left | **5%** (96px) | **5%** (54px) |
| Inset from bottom | **18%** (194px) | **16%** (307px) |
| Max width | **30% of frame width** (576px) | **40%** (432px) |
| Content | Stats, counters, code line counts, meeting duration | Same |

#### Position C — Top-Right Data Cluster (rare — for data-rich montages)
| Parameter | Value (16:9) |
|---|---|
| Inset from right | **4%** (77px) |
| Inset from top | **3%** (32px) |
| Max width | **25% of frame width** (480px) |
| Content | Secondary metrics, mini progress bars |

### 3.2 Typography for HUD Elements

| Property | Primary Data | Secondary Label | Unit / Badge |
|---|---|---|---|
| Font | JetBrains Mono (brand `monoFont`) | Inter | JetBrains Mono |
| Size (16:9) | **32px** (1.7%) | **16px** (0.8%) | **14px** (0.7%) |
| Size (9:16) | **28px** (1.5%) | **14px** (0.7%) | **12px** (0.6%) |
| Weight | **500 (Medium)** | **400 (Regular)** | **400** |
| Color | `alabaster` | `alabaster` at **60%** | `silentGray` #6B7280 |
| Letter-spacing | **-0.02em** | **0.04em** UPPERCASE | **0.02em** |

### 3.3 Visual Treatment

Glassmorphism panel — subtle, translucent, never opaque.

| Property | Value |
|---|---|
| Background | `rgba(18, 20, 28, 0.55)` (obsidian at 55%) |
| Backdrop blur | **12px** Gaussian blur |
| Border | **1px** at `rgba(250, 250, 250, 0.08)` (alabaster 8%) |
| Border radius | **6px** |
| Padding | **12px 16px** (vertical horizontal) |
| Inner element gap | **6px** between data rows |
| Inner group gap | **12px** between distinct data groups |
| Opacity (entire panel) | Max **80%** — never fully opaque |
| Box shadow | `0 4px 24px rgba(0,0,0,0.3)` |

### 3.4 HUD Animation

HUD elements animate on a **staggered per-element** basis, not as a group.

| Phase | Duration | Easing | Notes |
|---|---|---|---|
| **Panel appear** | **0.25s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Opacity 0 → 0.80 |
| **Data element stagger** | **0.06s** between rows | — | Each row appears after panel |
| **Count-up (numbers)** | **1.0–1.5s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Number animates from 0 → target |
| **Panel disappear** | **0.20s** | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` | Faster than appear |
| **Hover breathe** | **±2% scale** over **2.0s** loop | Sine wave | Subtle — only for hero metrics |

### 3.5 Content Rules

| Rule | Specification |
|---|---|
| Max HUD elements on screen | **2** simultaneously |
| HUD placement | Must **avoid face bounding boxes** (overlap detection) |
| HUD vs subject | If subject occupies >60% of frame, only use top-left (A) |
| Context | HUD data must be **relevant to current scene** — never decorative |
| Empty panels | Never show empty or zero-data panels |

---

## 4. Data Visualization Overlays

Used during time-lapse, performance metrics, productivity stats, or progress tracking sections. Must feel like Bloomberg terminal meets Apple design.

### 4.1 Chart/Display Types

| Type | Best For | Position | Max Size |
|---|---|---|---|
| **Progress bar (horizontal)** | Task completion, timeline progress | Bottom **15–18%** from bottom, center | Width: **70% of frame** — height: **6px bar + 22px label** |
| **Timeline indicator** | Day timeline, schedule overview | Bottom **15%** from bottom, center | Width: **65% of frame** — height: **3px rail** |
| **Ring / gauge** | Single metric (e.g., "8/10 tasks") | Top-right (Pos C) | Diameter: **90px** — stroke: **5px** |
| **Stat counter** | Key number with label | Bottom-left (Pos B) | Text: **32px mono + 14px label** |
| **Mini bar chart** | Multi-metric comparison | Top-right (Pos C) | **200px wide x 100px height** |
| **Activity dot grid** | Daily status, GitHub-style | Bottom-right | **80px wide x 80px height** |

### 4.2 Color Palette (Luxury Editorial)

| Role | Color | Usage |
|---|---|---|
| **Active fill** | `gold` (#D4AF37) | Primary data: bars, rings, counters |
| **Background track** | `rgba(250, 250, 250, 0.10)` | Bar background, gauge track |
| **Label text** | `alabaster` (#FAFAFA) at 75% | Labels and units |
| **Secondary metric** | `silentGray` (#6B7280) at 60% | Comparison/secondary data |
| **Accent positive** | `rgba(75, 200, 138, 0.7)` | Green for positive change |
| **Accent negative** | `rgba(239, 68, 68, 0.7)` | Red for negative change |
| **Grid lines** | `rgba(255, 255, 255, 0.06)` | Very faint — barely visible |
| **Chart background** | None (transparent) | Never show chart bounding box |

**Rule: One accent color per visualization.** In editorial mode, the default accent is always `gold`. Green/red only for performance metrics.

### 4.3 Animation Timings

| Phase | Duration | Easing |
|---|---|---|
| **Bar fill (width or height)** | **0.8s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` deceleration |
| **Ring draw (circumference)** | **1.0s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` |
| **Count-up (number)** | **1.0–1.5s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` |
| **Stagger between bars** | **0.08s** per bar | — |
| **Stagger between chart elements** | **0.12s** | Axis label → bar → data label |
| **Hold visible** | **4.0–6.0s** (matched to scene) | — |
| **Exit** | **0.30s** fade | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` |

### 4.4 Progress Bar Specification

```tsx
// Horizontal progress bar — used for task completion, timeline progress
const BAR_WIDTH = frameWidth * 0.70;   // 70% of frame
const BAR_HEIGHT = 6;                  // 6px height
const RAIL_COLOR = "rgba(250,250,250,0.10)";
const FILL_COLOR = "#D4AF37";         // gold
const ANIMATE_DURATION = fps * 0.8;   // 24 frames at 30fps

// Animate fill width from 0 to target %
const fillWidth = interpolate(frame, [0, ANIMATE_DURATION], [0, targetPercent * BAR_WIDTH], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
  easing: (t) => 1 - Math.pow(1 - t, 3),
});
```

### 4.5 Timeline Indicator Specification

```tsx
// Bottom-center timeline — used for "my day" time-lapse sections
const RAIL_WIDTH = frameWidth * 0.65;  // 65% of frame
const RAIL_Y = frameHeight * 0.85;     // 85% from top

// Active node (current time)
const activeNodeRadius = interpolate(
  frame, 
  [0, fps * 0.5], 
  [6, 10],          // pulses from 6 → 10px radius
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

// Completed segments glow gold, future segments are dim
```

---

## 5. Logo / Brand Bug

The logo/brand identifier is used sparingly — this is editorial content, not broadcast news. No persistent bug.

### 5.1 Position

| Placement | Inset from edges |
|---|---|
| **Bottom-right** (preferred — follows Apple/content standard) | **3% from right edge, 4% from bottom edge** |
| **Bottom-left** (alternative — only when bottom-right conflicts) | **3% from left edge, 4% from bottom edge** |

At 1920x1080: 3% = 58px from right, 4% = 43px from bottom.

### 5.2 Size

| Parameter | Value |
|---|---|
| **Width relative to frame** | **5% of frame width** (96px at 1920x1080; 54px at 1080x1920) |
| **Max height** | **3% of frame height** (32px at 1920x1080) |
| Constrain by | Larger dimension — preserve aspect ratio |
| Minimum legible | 3% of frame width (58px — below this, text is illegible) |

### 5.3 Opacity

| Context | Opacity |
|---|---|
| Default | **50%** |
| Against dark background | **65%** |
| Against bright background | **40%** |
| After intro (persistent low state) | **30%** |

### 5.4 Visual Treatment

| Property | Value |
|---|---|
| Color | `alabaster` (#FAFAFA) or `gold` (#D4AF37) |
| Background shield | Optional: `rgba(18, 20, 28, 0.30)` pill, 4px border radius, 12px padding |
| Text shadow | No — prefer the background shield for legibility |
| Content | **"NOAH SHELDON"** in `Inter 600 (Semi-Bold)`, 14px (16:9), 0.08em letter-spacing, UPPERCASE |

### 5.5 Animation

The brand bug follows an **intro → fade-back** pattern: prominent at intro, then fades to background.

| Phase | Duration | Easing | Opacity target |
|---|---|---|---|
| **Fade-in** (at scene start) | **0.50s** | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | 0 → 65% |
| **Hold prominent** | **2.0s** | — | 65% |
| **Fade to persistent** | **0.40s** | `cubic-bezier(0.4, 0.0, 0.2, 1.0)` | 65% → 30% |
| **Fade-out** (end of video) | **0.40s** | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` | 30% → 0 |
| **Exit delay** (relative to scene) | Fade out **0.5s after** content ends | — | — |

**Usage rule:** Show brand bug only during video content, never on title cards or end cards. Max one appearance per video.

### 5.6 When NOT to Show

- Over face B-roll (speaking to camera)
- Over text overlays that occupy >50% of frame width
- On title/end cards (separate branding handled there)
- When user on-screen content is in bottom-right corner (detect via bounding box)

---

## 6. Unified Easing Reference

All easing curves verified from Material Design 2 motion specifications.

| Use Case | GSAP ease | CSS cubic-bezier equivalent |
|---|---|---|
| **Entry** (lower third, text reveal, HUD appear) | `power3.out` | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` |
| **Exit** (fade out, disappear) | `power2.in` | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` |
| **Standard motion** (data viz build, transitions) | `power2.inOut` | `cubic-bezier(0.4, 0.0, 0.2, 1.0)` |
| **Sharp exit** (utility elements) | `power1.inOut` | `cubic-bezier(0.4, 0.0, 0.6, 1.0)` |
| **Breathe / pulse** (hover animation) | Sine wave via `sine.inOut` loop | Sine wave |

### Duration Hierarchy Table

| Element Scale | Entry Duration | Exit Duration | Example |
|---|---|---|---|
| **Small** (< 60px size) | **0.20–0.25s** | **0.15–0.20s** | HUD data point, icon, badge |
| **Medium** (60–200px) | **0.30–0.40s** | **0.25–0.30s** | Lower third, stat card, text block |
| **Large** (> 200px) | **0.40–0.50s** | **0.30–0.40s** | Full-width title, hero stat, brand logo |

---

## 7. Safe Area & Frame Layout Reference

### 7.1 16:9 (1920x1080) — Title/Action Safe Zones

| Zone | Margin from edge | Content rule |
|---|---|---|
| **Title safe** | **10%** from all edges (80% inner box) | All text must be inside this zone |
| **Action safe** | **3.5%** from all edges (93% inner box) | All visual content must be inside this zone |
| **Margin ignored** | Beyond 3.5% | Content may be clipped on some displays |

### 7.2 Layer Priority (Z-Order)

```
Layer 0: Video background (A-Roll or B-Roll)
Layer 1: Gold accent elements (bars, lines)
Layer 2: Text overlays (lower thirds, text reveals, labels)
Layer 3: HUD panels (glassmorphism)
Layer 4: Data visualizations (bars, rings, counters)
Layer 5: Brand bug (topmost, but smallest)
Layer 6: Captions (from caption-styling-research.md)
```

### 7.3 Avoidance Zones

| Element | Avoid in this area |
|---|---|
| **Face** (detected bounding box) | No overlays within box + 20px padding |
| **Bottom text zone** (y: 75–92%) | Reserved for captions (16:9) |
| **Bottom text zone** (y: 65–85%) | Reserved for captions (9:16) |
| **Top 5% of frame** | Empty — breathing room. Only top-left HUD permitted. |

---

## 8. Cross-Reference: Existing Project Assets

| Asset | File | Notes |
|---|---|---|
| `templates/short-form/` | HyperFrames format templates | day-in-my-life / desk-setup / transformation — each has `spec.md` + `index.html`. Scene titles and lower-thirds follow this spec's positioning; use entry/exit timing + gold bar pattern from §1. |
| `skills/video-editor/` | Editorial rules (Hollywood appendix) | Gold accent, mono numbers, standardized easing + per-word stagger from §2, counter build duration §4 (1.0s). |
| `skills/video-agent/technologies/gsap.md` | GSAP runtime rules | Paused master timeline, seek-safe, visual-property allowlist — the motion contract for this spec. |
| `captions doc` | `docs/caption-styling-research.md` | Caption animation uses separate 0.3s fade in/out with active-word highlights. This is Layer 6 and follows caption rules, not text-reveal rules. |
| `transitions doc` | `docs/transition-patterns-research.md` | Hard cuts preferred. Motion graphics on this page handle the overlays over those cuts — they do not replace cuts. |

---

## 9. Quick-Reference Decision Matrix

```
Scene has a person speaking?
  ├─ YES → No HUD, no text reveals. Lower third for intro only. Captions handle text.
  └─ NO  → Apply motion graphics based on scene type:

Scene type = montage / time-lapse / B-roll sequence
  ├─ Show: Timeline indicator (§4.5) + HUD data panels (§3)
  └─ Duration per overlay: 4–6s hold, 0.3s animate

Scene type = stat / data moment
  ├─ Show: Hero stat counter or progress bar (§4)
  └─ Position: Bottom-left metric card (§3.1 Pos B)

Scene type = quote / emphasis
  ├─ Show: Hero text reveal (§2) with gold kicker
  └─ Enter: Per-word fade up over 2.0s max

Scene type = chapter transition
  ├─ Show: Section header text (§2.2)
  └─ Position: 42% from top, left-aligned

Always show: Brand bug (§5) — once per video intro only
Always show: Gold accent line with every text element
Never show: Two competing text overlays at once
```
