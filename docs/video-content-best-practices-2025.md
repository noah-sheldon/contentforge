# Video Content Best Practices 2025/2026

Research compiled July 2026. Structured rules per topic for coding into agent prompts. Specific numbers (font sizes, durations, dB levels, percentages) included where available.

> **Note on sources:** Synthesized from creator resources (Buffer, Sprout Social, TechCrunch, The Verge), video production blogs (Opus.pro, Kapwing, SubtitlesFast, KeyframeKit, Orchid Media, JoySpace, Project Aeon), sound design references (toneproduction.net, mytasker.com, filmlocal.com), and color grading references (DaVinci Resolve docs, MCM Creative Studios, Color Archive, ReelMind AI, Clouds Agency, Filmmaker Genius, Daniel Grindrod). Not peer-reviewed academic research — industry consensus among social media creators and video professionals.

---

## 1. Threads (Meta) Video Best Practices

### 1.1 Conversational Tone — Video in a Text-First Culture

- **Text-first, video-second.** Threads is text-first by design. Meta explicitly values a "quieter, less video-centric experience" vs TikTok/Reels.
- **Images outperform video.** Images get 0.6% more engagement than videos, 37% more than link posts, 60% more than text-only posts (Buffer, analysis of 2.5M posts).
- **Video takes second place** behind images. Use short clips (<60s) as accent pieces, not primary format.
- **Don't repurpose** long-form YouTube/Instagram content directly. Threads video works best when it serves a conversational purpose.

### 1.2 Reply Culture — #1 Engagement Lever

- **Replying to comments boosts engagement by 42% per post** (Buffer, 128K posts analyzed).
- **Algorithm favors conversation:** weights replies, profile visits, time spent, repeat interactions over passive likes.
- **Median engagement rate: 6.25%** — 73.6% higher than X (3.6%).
- **Ask open-ended questions** in every post to trigger reply chains.
- **Replying to others' threads in your niche** is as effective as original content for growth (Buffer).

### 1.3 Thread Density

- **Post limit:** 500 characters per post.
- **Text attachments:** Optional up to 10,000 characters — but NOT indexed by search engines or federated to fediverse.
- **Video limit:** Up to 5 minutes per video.
- **Photo limit:** Up to 10 photos per post.
- **No optimal thread length data found** — keep individual posts concise (500 chars forces brevity). Reserve 10K text dumps for existing audience, not discovery.

### 1.4 Hashtag Strategy — Minimal, Topic-Focused

- Threads uses "tags" not hashtags — they function as **topic signals**, not search filters.
- **Use tags sparingly** to mark your niche community.
- Threads has 200+ official communities (Dec 2025) for dedicated topic spaces.
- New "Your Algo" and "Dear Algo" tools (2026) let users privately/publicly signal content preferences.
- **No recommended tag count data** — qualitative guidance: tag your niche, don't keyword-stuff.

### 1.5 Video Length — What Works

| Source | Recommendation |
|--------|---------------|
| Instagram Help Center | Max 5 minutes |
| Sprout Social | Under 60 seconds drives most interaction |
| Buffer | Video has "higher lift" — worth trying if you already create video |

### 1.6 Posting Cadence & Platform Stats

| Metric | Value |
|--------|-------|
| Monthly active users | 500M (June 2026) |
| Daily active users | 115M |
| Brands on Threads | 57% |
| Best posting window | Weekday mornings 6am–11am |
| Best single slot | Thursday 9am |
| Fast growth cadence | 3+ posts/day |
| Minimum to maintain | 1 post/day |

---

## 2. Audio / SFX Best Practices

### 2.1 Whoosh / Transition Sound Design

**When to use:**
- Add kinetic energy to cut points and motion-graphic transitions.
- **Sound bridges (J-cuts):** Start audio from incoming scene BEFORE picture cut — smooths jarring transitions.
- **Silence as a tool:** Use deliberately after a hook/reveal to force attention, or before a punchline.

**How much to use:**
- **Use sparingly.** If you can consciously notice every transition sound, remove half. Goal is felt, not consciously noticed.

**Volume levels:**
| Element | Target Level |
|---------|-------------|
| Sound effects (whooshes, transitions) | -10 dB to -20 dB |
| Dialogue/Voiceover (anchor) | -6 dB to -12 dB |
| Background music (under dialogue) | -20 dB to -30 dB |
| Background music (no dialogue) | -12 dB to -18 dB |
| Final mix peak | -3 dB or lower |

**Transition effect durations:**
| Type | Duration | Use Case |
|------|----------|----------|
| Swoosh/Whoosh | 0.3–1.0s | Fast cuts, scene changes, motion transitions |
| Riser | 1.0–3.0s | Building tension toward a reveal or drop |
| Impact | 0.2–1.0s | Hard cuts, beat drops, reveal moments |
| Stinger | 0.5–2.0s | Emphasis on punchline, hook, logo reveal |
| Reverse cymbal | 0.5–2.0s | Cinematic build-ups, dream-like transitions |

### 2.2 Ambient Layers — Background Audio

**Foundation - Room Tone:**
- Record 30–60 seconds of room tone (empty room, no talking) on every shoot.
- Lay under entire timeline to remove "seams" between clips.
- If unavailable, use iZotope RX Ambience Match to generate substitutes.

**Layering architecture:**
1. Build ambient bed first — continuous, low-level room tone under every scene.
2. Add secondary elements — one-shots (doors, distant traffic, creaking pipes) with random timing/position/pitch.
3. Layer multiple ambient elements at different distances (distant street + interior air handler + crowd murmur).

**EQ for ambient layers:**
- Low-pass filter distant sounds (mimics air's treble absorption).
- Roll off below 150–200 Hz for distance illusion.
- Reduce middle frequencies (350 Hz–2 kHz) to avoid competing with dialogue.
- Place EQ after reverb.

**Volume levels:**
- Ambient layers: **-25 dB to -35 dB** (felt, not consciously heard).
- Maintain **18 dB gap** between ambient noise and desired signals.
- Use volume automation for ebb and flow.

### 2.3 Audio Ducking (Critical Technique)

- **Single highest-impact fix** for amateur-sounding video.
- Automatically lower background music by **6–10 dB** when someone speaks.
- Use gentle release when speaker finishes.
- Available in Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut.

### 2.4 Music Trends — Genre by Platform

| Platform | Genres | Style |
|----------|--------|-------|
| YouTube (long-form) | Cinematic orchestral, lo-fi, ambient | Supports narrative development |
| TikTok | Trending pop, EDM, hip-hop | Energetic, beat-driven for engagement |
| Instagram Reels | Jazz, lo-fi, chill, trending audio | Sophisticated lifestyle; beat-synced for ads |
| Threads | Lo-fi, chill, conversational indie | Low-energy backdrop — text-first culture |
| Educational | Clear instrumental, optimistic, lo-fi | Unobtrusive, maintains focus |
| Documentary | Cinematic orchestral, ambient, piano | Storytelling tool — builds atmosphere |

### 2.5 Loudness & Export Standards

| Metric | Target |
|--------|--------|
| YouTube loudness | -14 LUFS |
| Social (Reels, TikTok) | -14 to -16 LUFS |
| True peak ceiling | -1 dBTP |
| Export format | 48 kHz, 24-bit WAV, stereo |

### 2.6 Copyright-Safe Music Sources

**Paid:** Epidemic Sound (55K+ tracks), Artlist (900K+ assets), Musicbed (cinematic focus), Soundstripe (50K+ tracks), Uppbeat (free + paid tiers).
**Free:** YouTube Audio Library, Clipchamp Content Library, platform-native libraries (TikTok, Instagram, CapCut).
**AI-generated:** Artlist AI, Suno — simpler licensing, reduced plagiarism risk.

---

## 3. Text Overlay & Closed Caption Best Practices

### 3.1 Font Size — Minimum Readability

| Use Case | Size |
|----------|------|
| Primary text (mobile) | 18–24pt / 18–32px minimum |
| Secondary / supporting text | 16–20pt |
| Hook / emphasis words | 1.5x larger than filler words |
| YouTube subtitle default | 24–32px (Roboto or Arial) |
| Instagram Stories | ~20% larger than YouTube (smaller viewport) |

**Font readability scores (ranked):**
1. Helvetica Neue (9.5/10)
2. Open Sans (9.2/10)
3. Roboto (9.0/10)
4. Montserrat (8.8/10)
5. Source Sans Pro (8.5/10)

**Platform-specific fonts:**
| Platform | Recommendation |
|----------|---------------|
| TikTok | Bold, chunky sans-serif |
| Instagram Reels | TikTok-style bold text with animations |
| YouTube | Roboto or Arial, 24–32px |
| LinkedIn | Clean sans-serif, professional |

### 3.2 Position — Text Safe Zones (1080×1920 Vertical)

| Platform | Safe Zone (W×H) | Top Margin | Bottom Margin | Left Margin | Right Margin |
|----------|----------------|-----------|-------------|------------|-------------|
| TikTok | 720×1030 px | 220 px | 640 px | 120 px | 240 px |
| Instagram Reel | 900×1500 px | 110 px | 320 px | 60 px | 120 px |
| Instagram Story | 1080×1420 px | 250 px | 250 px | 60 px | 60 px |
| YouTube Shorts | 820×1510 px | 140 px | 270 px | 70 px | 190 px |

**For horizontal (16:9) YouTube (1920×1080):**
- Safe zone: 1540×870 px
- Margins: 120px top/bottom, 150px left/right

**General safe zone rules:**
- TikTok: Avoid bottom 450px (caption bar + buttons) and top 300px (username overlays).
- Instagram Reels: Avoid bottom 20% (UI overlap).
- YouTube Shorts: Keep text at least 300px from bottom (progress bar + engagement buttons).
- Danger zone = bottom 20% + right 15% of screen.
- Gold zone = center-middle block, slightly above eye level.
- Keep within middle 80% of screen width.
- 60px minimum distance from screen edges (gesture clearance).

### 3.3 Text Animation — Types and Timing

**Animation types (preferred):**
- Kinetic typography — fade-in, text flowing across screen, key phrases subtly pulsing.
- Active word-by-word highlight — standard on TikTok, Instagram, YouTube Shorts.
- Smart fade-in: 100–200ms opacity increase.
- Subtle pop-in for emphasis.
- Simple transitions — fades preferred over flashy effects.
- Use easing for smooth transitions.

**Text timing rules:**

| Platform / Content | Duration per caption | Reading speed (WPM) |
|--------------------|--------------------|--------------------|
| TikTok | 1–3 seconds | 220–250 WPM |
| Instagram | 2–4 seconds | 200–240 WPM |
| YouTube | 2–6 seconds | 180–220 WPM |
| LinkedIn | 3–5 seconds | 160–200 WPM |
| Fast-paced content | 1.5–2s min | 220–250 WPM |
| Conversational | 2–3s min | 180–220 WPM |
| Educational | 3–4s min | 160–180 WPM |
| Technical | 4–5s min | 140–160 WPM |

**Universal timing rules:**
- Minimum display duration: **1.5 seconds** (regardless of character count).
- Maximum display duration: **6 seconds** (maintains engagement).
- Pre-roll: Text appears **0.5–1 second** before audio begins.
- Post-speech: Text lingers **0.3–0.5 seconds** after speech ends.
- Synchronization tolerance: **±200ms** from audio.
- Transition smoothness: **100–200ms** fade in/out.
- **2-frame gaps** between consecutive captions.
- Social media text slides: **4–5 seconds max** for brief text.

### 3.4 Closed Captions — Styling

**Characters per line:**
| Format | Max characters |
|--------|---------------|
| Short-form (TikTok, Reels) | 15–20 per line |
| Long-form (YouTube, LinkedIn) | 32 per line max |
| Two-line max | 64 total (32 per line) |

**Contrast ratios (gold standard = white text on black):**
| Combination | Ratio |
|------------|-------|
| White text on black | 21:1 (gold standard) |
| Black text on white | 21:1 |
| Yellow text on black | 18:1 |
| White text on dark blue | 15:1 |
| WCAG 2.1 AA minimum | 4.5:1 (7:1 optimal) |

**Recommended styling per platform:**
- **TikTok:** White or yellow text + black outline + bold chunky font.
- **Instagram Reels:** Bold text + active word-by-word highlight + brand colors.
- **YouTube:** White text + black outline or semi-transparent background.
- **LinkedIn:** White or light gray on dark background, professional.
- **Accent backgrounds:** Brand primary color at 70–80% opacity.

**Keyword highlighting:**
- Highlight key words with different colors.
- Active word-by-word highlighting common on TikTok/Reels.
- Hook words 1.5x larger than filler words.
- Use emojis sparingly.
- Sentence case (not all caps).
- Keep font, size, color consistent throughout video.

**Performance impact of captions:**
- 85% of Facebook videos watched without sound.
- 80% higher engagement with subtitled videos.
- 12–15% longer watch times with captions.
- 15–25% more shares for subtitled videos.
- 20–40% increase in video completion rate with well-designed captions.
- Text overlays boost engagement by up to 25%.
- Text overlays improve message retention by up to 30%.

---

## 4. Color Grading Best Practices

### 4.1 Platform-Specific Grading Guidelines

**Instagram (Reels & Stories):**
| Property | Guideline |
|----------|-----------|
| Saturation | Slightly less than broadcast — aggressive compression artifacts |
| Aesthetic | Polished, editorial, aspirational |
| Brand approach | 3–5 consistent colors across all content |
| Text treatment | High-contrast (white + black outline) — survives compression |

**TikTok:**
| Property | Guideline |
|----------|-----------|
| Grade target | **Grade 5–10% cooler and slightly lower contrast** than your target — TikTok's compression warms footage and boosts contrast |
| Saturation | High-saturation combos work (vivid bg + white text, neon on black) |
| Immediacy | First 0.5s must grab — vivid gradient overlays (pink-purple, blue-green) |
| LUT intensity | 65–75% — verify on iPhone screen before publishing |

**YouTube:**
| Property | Guideline |
|----------|-----------|
| Quality | Best compression — supports 4K HDR |
| Color space | Master Rec. 709 for most feeds, PQ/HLG for HDR |
| Vertical crop | Ensure 9:16 vertical crop brightness matches horizontal source |

**Pinterest:**
| Property | Guideline |
|----------|-----------|
| Palette | Warm — cream/white backgrounds, warm neutrals, soft pastels (blush, sage) |
| Brightness | Light, airy, aspirational |
| Adaptation | Cool-aesthetic brands should create warm-adapted content series for Pinterest |

### 4.2 Building a Consistent Visual Look

**Core brand palette strategy:**
1. Define **3–5 non-negotiable brand colors**.
2. Pick: primary background, 1–2 accents, photography treatment rule (warm/cool, light/dark, saturation level).
3. Create platform-specific expression rules without altering core identity.
4. Never permanently alter brand palette for algorithmic trends — use limited series or seasonal campaigns.

**LUT workflow for batch content:**
1. Shoot with log profile (maximizes dynamic range).
2. Color correct first — balance white balance + exposure; match clips from different cameras.
3. Apply technical LUT (Log → Rec. 709 — exact match to camera profile).
4. Apply creative LUT on adjustment layer — dial to **65–85% intensity**.
5. Check skin tones + scopes (waveform + vectorscope).
6. Fine-tune per clip (correction below LUT, refinement above).

### 4.3 Skin Tone Handling

**The skin tone line (I-line):**
- Natural skin tone across all ethnicities falls along a consistent diagonal line on the vectorscope.
- **Target range:** 20–50% saturation, 40–70 IRE luminance on waveform.
- ~50–60% IRE in sunlight, ~50% window light, ~30% bar light, ~20% moonlight.

**How to grade skin tones:**
1. Turn on skin tone indicator in vectorscope.
2. Use qualifier/power window to isolate skin from background.
3. Check position on vectorscope — skin should fall on or near the skin tone line.
4. Use Hue vs Hue curve or Offset to correct casts.
5. After correction, add environmental color into highlights — maintain natural reds in mid-tones and shadows.

**Common mistakes to avoid:**
- Pushing skin into cool tones → looks green/sickly.
- Over-saturating skin → waxy, unnatural.
- Heavy teal-and-orange on faces → orange skin looks fake.
- Ignoring the vectorscope → color casts undetected.
- Testing only on lightest skin tone → grade fails on darker skin tones.
- Overusing LUTs without context → clipping, unnatural skin.

**Pro rule:** Test every grade on reference frames containing full range of skin tones in your content. A grade that only looks right on the lightest person is unfinished.

### 4.4 2025 Color Grading Trends

| Trend | Look | Settings |
|-------|------|----------|
| Hyper-Realism | Natural tones, lifelike, balanced | Subtle saturation, organic shadows, balanced skin tones |
| Desaturated Pastels | Wellness/lifestyle — high-key, soft | Saturation below 30%, lifted black point (shadows → light gray) |
| Hyper-Vibrant Neon-Pop | Tech/energy — selective color boost | Select hues at 80–100% saturation, crushed blacks, peaky whites |
| Split Toning | Cinematic dual-tone | Warm highlights + cool shadows |
| Mocha Mousse + Cherry Red (Pantone) | #A47864 + #FF1744 | Mocha for backgrounds/borders, Cherry for CTAs/accents |

### 4.5 Mobile-Conscious Grading

- Design grade for 9:16 vertical format.
- Central 80% of frame has priority for color clarity — edges matter less.
- Increase mid-tone contrast for small-screen readability.
- Avoid chroma smearing / color banding — high-saturation colors degrade faster on mobile.
- Perceived brightness of vertical crop must match horizontal source.

### 4.6 Export & Delivery

| Platform | Resolution | Bitrate | Codec |
|----------|-----------|---------|-------|
| YouTube | 4K HDR | Highest | H.264/H.265 |
| TikTok | 1080p | 6–10 Mbps | H.264 |
| Instagram | 1080p | 6–8 Mbps | H.264 |
| General | Rec. 709 | Check for clipping/gamma shift | — |

---

## Quick Reference Cheat Sheet

### Audio Mixing Levels (Dialogue-Referenced)
| Element | Level |
|---------|-------|
| Dialogue (anchor) | -6 dB to -12 dB |
| Music (under dialogue) | -20 dB to -30 dB |
| Music (no dialogue) | -12 dB to -18 dB |
| Sound effects | -10 dB to -20 dB |
| Ambience | -25 dB to -35 dB |
| Audio ducking | -6 to -10 dB lower |
| Final loudness | -14 to -16 LUFS |

### Text Overlay (Mobile Vertical)
| Setting | Value |
|---------|-------|
| Font size (minimum) | 18–24px |
| Characters per line (short-form) | 15–20 |
| Characters per line (long-form) | 32 max |
| Minimum display time | 1.5s |
| Maximum display time | 6s |
| Fade transition | 100–200ms |
| Pre-roll before audio | 0.5–1s |
| Post-speech linger | 0.3–0.5s |
| Contrast minimum | 4.5:1 (AA), 21:1 ideal |

### Color Grading Quick Rules
| Rule | Value |
|------|-------|
| Skin saturation | 20–50% |
| Skin luminance | 40–70 IRE |
| Creative LUT intensity | 65–85% |
| TikTok temp compensation | Grade 5–10% cooler |
| Brand palette size | 3–5 colors |
