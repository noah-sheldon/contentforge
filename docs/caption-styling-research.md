# Caption Styling Research — Professional "Day in the Life" Vlogs

> Compiled for the AI-powered automatic video editing pipeline.
> Sources: DCMP Captioning Key, BBC Subtitle Guidelines, Netflix Timed Text Guide, Opus Pro, BlitzCut, SubtitleWise, OpenClip, VidNo, MakeAIClips, Captions.ai, WCAG accessibility standards.

---

## 1. Highlighting Pattern: Word-by-Word vs Phrase-by-Phrase

### Word-by-Word (Karaoke) Highlighting

**Mechanism:** Each word appears in muted/dim color. The currently spoken word is highlighted (bright color). Previously spoken words remain visible in dim color. Typically 3–4 words visible at a time.

| Metric | Value |
|---|---|
| Words visible per block | 3–4 (not full sentence) |
| Engagement lift vs static phrase | +18–23% watch time |
| Avg % watched (word-by-word) | 79% |
| Swipe-away rate (word-by-word) | 19% |
| Best video length | Any length; especially <60s social |
| Appropriate tone | Energetic, casual, fast-paced |

**Pros:**
- Creates visual rhythm that holds attention
- +18–23% watch time lift vs static captions (A/B tested over 40 Shorts)
- Nearly triples avg % watched vs sentence-level captions (79% vs 48%)
- Halves swipe-away rate (19% vs 41%)
- Works well for talking-head vlogs, listicles, storytelling

**Cons:**
- More complex to render (word-level timestamps required)
- Can feel "tiktok-y" — not ideal for formal/editorial content
- Viewers can lose mid-sentence context if only 1–2 words shown
- Requires precise word-level alignment

### Phrase-by-Phrase Highlighting

**Mechanism:** A phrase (3–7 words) appears on screen. As the speaker moves through the phrase, the entire phrase is displayed (no per-word highlight), or a subtle full-phrase fade-in. Preferred for editorial/professional content.

| Metric | Value |
|---|---|
| Words visible per block | 5–7 (narrative), 3–5 (energetic) |
| Engagement vs static | +12–17% engagement (pop-in style) |
| Avg % watched (phrase) | 48% |
| Swipe-away rate (phrase) | 41% |
| Best video length | Any length; preferred for >60s content |

**Pros:**
- Better comprehension and readability
- More professional/editorial aesthetic
- Works for longer-form content (viewers don't lose context)
- Simpler to render (phrase-level timing only)
- Preferred by Netflix, BBC, broadcast standards

**Cons:**
- 8–12% lower engagement than word-by-word animated styles
- Less visual rhythm for fast-paced content
- Can feel static if no animation applied

### RECOMMENDATION FOR "DAY IN THE LIFE" VLOG:

**Default: Phrase-by-phrase with active-word highlight.** Show the full phrase (3–7 words) in muted tone. Highlight the currently spoken word in a brighter shade. This hybrid approach gives professional editorial feel with the engagement benefit of word-level highlighting.

- Block size: 3–5 words (energetic vlog pacing)
- Display duration: 1.5–4 seconds per block (sweet spot: 2–3 seconds)
- Reading speed: 180–200 wpm (short-form social), 160–180 wpm (YouTube)
- Minimum display: 1 second per block
- Maximum display: 6 seconds per block
- Gap between blocks: minimum 2 frames (~0.08s at 24fps)

---

## 2. Caption Position & Safe Area

### General Position Rule

Captions should sit in the **lower-third zone** without overlapping faces, mouths, names, or essential graphics.

| Parameter | Value |
|---|---|
| Vertical position (from top of frame) | 65–85% down |
| Horizontal alignment | Center-justified |
| Horizontal safe zone | Middle 80% of frame width |
| Edge padding (minimum) | 60px from screen edges |
| Below system UI | Clear bottom 15% for platform UI (TikTok: bottom 10%) |

### Platform-Specific Safe Zones (9:16 vertical)

| Platform | Vertical safe zone (from top) |
|---|---|
| YouTube Shorts | 55–78% |
| Instagram Reels | 45–68% (Reels UI is thicker at top) |
| TikTok | 50–73% (bottom UI buttons) |

### Aspect Ratio Rules

| Aspect | Position adjustment | Reason |
|---|---|---|
| 9:16 (vertical/portrait) | 65–85% down, center | Default for Shorts/Reels/TikTok |
| 16:9 (landscape) | 75–90% down, center | Wider frame; move higher than broadcast to leave room |
| 1:1 (square) | 70–85% down, center | Compromise for cross-platform |
| 4:3 | 80–92% down, center | Legacy broadcast ratio |

### Safe Area Coordinates (percentage-based, for HyperFrames/FFmpeg)

```
// 9:16 frame (1080 × 1920)
safeArea = {
  x: 0.10,           // 10% from left edge
  y: 0.65,           // 65% from top (top of caption block)
  width: 0.80,       // 80% of frame width
  maxHeight: 0.20,   // max 20% of frame height for caption block
}

// 16:9 frame (1920 × 1080)
safeArea = {
  x: 0.10,
  y: 0.75,
  width: 0.80,
  maxHeight: 0.15,
}
```

### Position Adjustment Logic

- **Default:** Bottom-third, center-aligned
- **Speaker-dependency:** If speaker's face is in bottom-third, shift captions to top of frame (y: 10–25%)
- **Overlap detection:** Check no caption overlaps with detected face bounding boxes
- **Screen recording:** Place at top (y: 10–25%) when code/content is at bottom

---

## 3. Font Choices

### Recommended Fonts

| Font | Use case | Readability score |
|---|---|---|
| **Montserrat Bold** | Primary — editorial vlog caption | 8.8/10 |
| **Inter Bold** | Primary — clean, modern | — |
| **Open Sans Bold** | Primary — web-optimized, high legibility | 9.2/10 |
| **Roboto Bold** | Primary — YouTube auto-captions default | 9.0/10 |
| **Helvetica Neue Bold** | Primary — Apple ecosystem native | 9.5/10 |
| **Poppins Bold** | Primary — geometric, modern | — |
| **League Spartan Bold** | Primary — editorial, clean | — |
| **Source Sans Pro Bold** | Secondary — web font fallback | 8.5/10 |
| **Verdana Bold** | Secondary — low-resolution screens | — |

### Serif vs Sans-Serif

| Style | Recommendation |
|---|---|
| Sans-serif | **STRONGLY PREFERRED** for captions. Bold weight (700–900). Maximum readability at small sizes. |
| Serif | Avoid for captions in short-form video. Harder to read at small sizes. Acceptable only for title cards or cinematic text overlays in long-form. |

### Type Rules

| Rule | Specification |
|---|---|
| Weight | Bold (700) minimum. Never use Regular/Light/Thin. |
| Letter-spacing | 0–2px tracking. Avoid tight or wide spacing. |
| Kerning | Auto (default) |
| Case | Sentence case. Never ALL CAPS. |
| Fallback chain | `'Montserrat', 'Inter', 'Open Sans', 'Roboto', 'Helvetica Neue', sans-serif` |

---

## 4. Font Size & Character Limits

### Font Size (relative to frame height)

| Context | Size (% of frame height) | 1080p equivalent |
|---|---|---|
| Short-form social (9:16) | 7–10% | 60–80px (at 7%) to 134–192px (at 7–10%) |
| YouTube Shorts | 7–9% | 60–80px |
| TikTok | 8–10% | 70–90px (22–26% of SCREEN HEIGHT — note: this is a different metric in some sources, but 7–10% of frame height is the consistent standard) |
| Instagram Reels | 7–9% | 60–80px |
| YouTube (16:9 landscape) | 5–7% | 54–76px |
| Broadcast TV | 5–6% | 26–30px (at 1080p) |
| Cinema | 4–5% | 36–42px |

**Rule:** Min 7%, max 10% of frame height for social short-form. Min 5%, max 7% for landscape.

### Character Limits

| Source | Max chars per line |
|---|---|
| Netflix standard | 42 |
| BBC broadcast (Teletext) | 37 |
| BBC online (16:9) | 68% of frame width |
| BBC online (9:16) | 90% of frame width (~25 chars) |
| Social short-form (9:16) | 35–42 |
| Sweet spot for readability | 32–37 |

### Line Count

| Aspect ratio | Max lines | Preferred |
|---|---|---|
| 16:9 landscape | 2 | 2 |
| 4:3 | 2 | 2 |
| 9:16 vertical | 3 | 2 |
| 1:1 square | 2 | 2 |

**Line-break rule:** Break at natural phrase boundaries (clauses, prepositional phrases). Never split a single word across lines. Never break after a preposition.

---

## 5. Background Treatment

### Options (ranked by preference for editorial vlog)

| Treatment | Specification | Best for |
|---|---|---|
| **1. Drop shadow only** (no box) | 3–4px black stroke + 2–3px drop shadow at 30–50% opacity. Offset: (x:1, y:1). | Clean editorial aesthetic on varied backgrounds |
| **2. Semi-transparent box** | `rgba(0, 0, 0, 0.70–0.80)` — rounded corners: 4–6px. Padding: 8–12px horizontal, 4–8px vertical. | High readability on light/complex backgrounds |
| **3. Opaque box** | `rgba(0, 0, 0, 1.0)` | Accessibility requirement. |
| **4. Blurred background** | Backdrop blur: 8–16px Gaussian. Behind text only (not full-width bar). | Modern editorial aesthetic. Requires compositing. |

### Default Recommendation (Editorial Vlog)

| Parameter | Value |
|---|---|
| Primary treatment | 4px black stroke + 2px drop shadow at 40% opacity |
| Fallback (complex bg) | `rgba(0, 0, 0, 0.75)` box with 4px border-radius |
| Text shadow CSS | `text-shadow: #000 0px 2px 4px, #000 0px 0px 4px` |
| Box padding | 12px horizontal, 6px vertical |
| Box border-radius | 6px |

### WCAG Contrast Requirements

| Requirement | Ratio | Equivalent |
|---|---|---|
| Minimum (WCAG AA) | 4.5:1 | White with 1px black stroke ≈ barely passes |
| Target (WCAG AAA) | 7:1+ | White with 4px black stroke ≈ 12:1 |
| White on black box | 21:1 | Best possible |
| Yellow on dark bg | 12–15:1 | Excellent for highlights |
| White on 75% black box | ~15:1 | Very good |

---

## 6. Animation

### Styles (ranked for editorial professionalism)

| Style | Duration | Easing | Editorial fit |
|---|---|---|---|
| **Fade in/out** | 0.2–0.3s | ease-out | BEST — clean, professional |
| **Active-word highlight** | Instant (per word spoken) | none | BEST for hybrid word/phrase — highlight snaps to current word |
| **Slide up** | 0.3–0.4s | ease-out | Acceptable — subtle, feels natural |
| **Karaoke word highlight** | Per-word as spoken | none | GOOD for engagement but less editorial |
| **Pop-in (word by word)** | 0.15–0.2s per word | ease-out | CASUAL — best for <30s clips |
| **Bounce** | 0.4–0.5s | spring | AVOID for editorial content |
| **Typewriter** | Per character | none | AVOID — slow, distracting |

### Animation Rule Set (Editorial Vlog Default)

```
// Per-block animation
enter: fadeIn + slideUp
exit: fadeOut
enterDuration: 0.3s
exitDuration: 0.25s
enterEasing: ease-out
exitEasing: ease-in

// Active-word highlight (within block)
highlightColor: #FFD700 (gold/yellow) or #00BFFF (cyan)
unhighlightedColor: #FFFFFF (at 60% opacity)
highlightTransition: 0.05s (instant snap, no animation)
highlightStyle: color-shift only (no scale, no background)

// Karaoke word-by-word fallback (for high-energy segments)
wordAnimation: fadeIn (0.1s per word)
wordsVisible: 3-4 max
```

### Timing Standards (per caption block)

| Standard | Value |
|---|---|
| Netflix minimum duration | 5/6 second (~20 frames at 24fps) |
| Netflix maximum duration | 7 seconds |
| BBC minimum duration | 1 second |
| BBC maximum duration | 7 seconds |
| BBC minimum gap between blocks | 1 second (preferred 1.5s) |
| Social short-form sweet spot | 2–4 seconds per block |
| Max reading speed (Netflix adults) | 20 chars/second |
| Max reading speed (Netflix children) | 17 chars/second |
| Comfortable reading speed | 180–200 wpm |

---

## 7. Color

### Caption Color

| Element | Color | Hex |
|---|---|---|
| Default text | White | `#FFFFFF` |
| Highlighted word (editorial) | Gold | `#FFD700` |
| Highlighted word (modern) | Cyan | `#00BFFF` |
| Dimmed/unspoken word | White at 60% opacity | `rgba(255,255,255,0.6)` |
| Secondary text (speaker label) | Yellow | `#FFFF00` |
| Black text on light bg | Black | `#000000` |

### Highlight Color Options (by tone)

| Tone | Highlight color | Hex | When |
|---|---|---|---|
| Editorial / luxury | Gold | `#FFD700` | Default for professional content |
| Modern / tech | Cyan | `#00BFFF` | Tech/business vlogs |
| Energetic / casual | Yellow | `#FFEB3B` | High-energy content |
| Emotional | Warm pink | `#FF6B6B` | Storytelling moments |
| Brand match | Brand primary | — | When brand color contrasts with bg |

**Avoid for highlights:** Red (hard to read), Blue (blends into sky/water backgrounds), Dark gray (insufficient contrast), Pastels (low contrast).

### Speaker Identification Color

| Speaker | Color | Hex |
|---|---|---|
| Primary speaker (default) | White | `#FFFFFF` |
| Secondary speaker (label) | Yellow | `#FFFF00` |
| Off-screen narrator | Cyan | `#00FFFF` (BBC standard) |
| Sound effects/music desc | Green | `#00FF00` (BBC standard) |

---

## 8. Max Lines on Screen

### Rules

| Scenario | Max lines | Notes |
|---|---|---|
| Default (all aspects) | 2 | DCMP preferred standard |
| 9:16 vertical (emergency) | 3 | Only when short content cannot fit 2 lines |
| Single short phrase (<25 chars) | 1 | Preferred for fast-paced content |
| Two speakers | 2 max (1 per speaker) | Each speaker gets own line with dash or label |

### When to Break to Next Line

1. **Character overflow:** Text exceeds 37 chars (landscape) or ~25 chars (9:16)
2. **Natural pause:** At clause boundary or phrase boundary
3. **Speaker change:** Each speaker gets their own caption block (2 lines max)
4. **Bottom UI overlap:** If caption would overlap with platform UI buttons, break earlier or truncate

### Line-Break Algorithm

```
function breakCaption(text, maxCharsPerLine = 37) {
  if (text.length <= maxCharsPerLine) return [text]
  
  // Find natural break points, in priority order:
  // 1. Comma or semicolon boundary
  // 2. Conjunction boundary (and, but, or, so)
  // 3. Preposition boundary (in, on, at, for, with, etc.)
  // 4. Word boundary near maxCharsPerLine
  
  const breakPoints = [
    ...findIndexes(text, /[,;]\s/),
    ...findIndexes(text, /\s(and|but|or|so)\s/),
    ...findIndexes(text, /\s(in|on|at|for|with|by|from|to)\s/),
  ]
  
  // Pick the break point closest to (but not over) maxCharsPerLine
  const bestBreak = breakPoints
    .filter(p => p < maxCharsPerLine)
    .sort((a, b) => b - a)[0]
  
  // Max 2 lines; truncate with ... if still too long
  const line1 = text.slice(0, bestBreak).trim()
  const line2 = text.slice(bestBreak).trim().slice(0, maxCharsPerLine)
  return [line1, line2]
}
```

---

## Summary: Codeable Default Config

```yaml
caption_style:
  # Highlighting
  mode: phrase_with_active_word       # phrase, word_by_word, phrase_with_active_word
  words_per_block: 4                  # 3-5 energetic, 5-7 narrative
  active_word_highlight: true
  highlight_color: "#FFD700"

  # Position (percentage-based, 0-1 range)
  position:
    horizontal_align: center
    vertical_from_top: 0.65           # 65% down from top
    safe_width: 0.80                  # middle 80% of frame
    edge_padding_px: 60

  # Font
  font_family: "Montserrat, Inter, Open Sans, Roboto, Helvetica Neue, sans-serif"
  font_weight: 700                    # bold
  font_size_pct: 0.08                 # 8% of frame height
  letter_spacing_px: 1
  case: sentence

  # Limits
  max_chars_per_line: 37
  max_lines: 2
  max_lines_vertical: 3

  # Background
  background:
    type: shadow                       # shadow, box, blur, none
    stroke_width_px: 4
    shadow_blur_px: 4
    shadow_opacity: 0.40
    box_color: "rgba(0,0,0,0.75)"
    box_padding_x: 12
    box_padding_y: 6
    box_border_radius: 6
    blur_radius_px: 12

  # Animation
  animation:
    enter: slide_up_fade
    enter_duration_s: 0.3
    exit: fade
    exit_duration_s: 0.25
    enter_easing: ease-out
    exit_easing: ease-in
    highlight_transition_s: 0.05      # instant snap
    gap_frames: 2                     # minimum gap between blocks

  # Colors
  colors:
    text: "#FFFFFF"
    text_dimmed: "rgba(255,255,255,0.6)"
    highlight: "#FFD700"
    speaker_label: "#FFFF00"
    narrator: "#00FFFF"

  # Timing
  timing:
    min_display_s: 1.0
    max_display_s: 6.0
    sweet_spot_s: "2-4"
    reading_speed_wpm: 180
    max_reading_speed_cps: 20         # characters per second
```
