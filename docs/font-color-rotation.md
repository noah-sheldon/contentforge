# Rotation Registry — Every Video Must Be Different

**Rule: no two videos share the same combination.** Before building, check this registry + `docs/post-tracker.md` for the last video's fingerprint. Pick unused options across ALL dimensions. Log your row after render.

## Dimension 1 — Font Pairing

| # | Display (serif/headline) | Body / UI | Bundled? |
|---|---|---|---|
| 1 | Fraunces 900 (upright) | Inter 600-800 | Yes (fonts/fraunces.woff2, inter.woff2) |
| 2 | Fraunces 900 italic | Inter 600-800 | Yes (fraunces-italic.woff2) |
| 3 | Playfair Display 700 | Montserrat 600 | Bundle on use |
| 4 | Space Grotesk 700 | JetBrains Mono 400-700 | Bundle on use |
| 5 | DM Serif Display 400 | Work Sans 500 | Bundle on use |
| 6 | Bebas Neue 400 | Inter 600 | Bundle on use |

## Dimension 2 — Color Palette

| # | Name | Background | Accent | Secondary |
|---|---|---|---|---|
| 1 | Dark navy + gold | #0b0f14 | #dec261 | #9aa0aa |
| 2 | Deep teal + amber | #0a1418 | #f59e0b | #7dd3fc |
| 3 | Charcoal + cyan | #12161d | #22d3ee | #a78bfa |
| 4 | Warm black + red | #14100e | #e74c3c | #f5d97a |
| 5 | Slate + violet | #101018 | #a78bfa | #f472b6 |
| 6 | Cream + oxblood | #f5f0e6 | #6e1f1f | #2c2c2c |

## Dimension 3 — Hook Style

| # | Hook type | Example |
|---|---|---|
| 1 | Tension hook | "my boss texted me at 7am" |
| 2 | Stat hook | "£2,136. That's my desk." |
| 3 | Question hook | "What should I upgrade next?" |
| 4 | Wait-for-it | "wait for the transition" |
| 5 | Identity hook | "Day in the life of an AI lead" |
| 6 | Contrarian | "I stopped buying premium cables" |

## Dimension 4 — CTA Type

| # | CTA | Platform fit |
|---|---|---|
| 1 | Comment-bait | TikTok |
| 2 | Save/share | IG Reels (educational) |
| 3 | Part 2? / serialization | Both |
| 4 | DM-funnel ("comment PLAN") | IG (comment→DM automation) |
| 5 | Follow for value | Both |
| 6 | Question to comments | Both |

## Dimension 5 — Beat Structure

| # | Arc | Use when |
|---|---|---|
| 1 | Hook → 3 points → CTA | List/educational |
| 2 | Hook → build → payoff | Install/transformation |
| 3 | 5-beat montage | Day-in-life, fast cuts |
| 4 | 8-beat story (01-11 clip arc) | Narrated vlogs |
| 5 | Before → turning point → after | Transformation |
| 6 | Hook → one deep dive | Single-concept |

## Dimension 6 — SFX Pattern

| # | Pattern | Density |
|---|---|---|
| 1 | Whoosh on EVERY cut | High |
| 2 | Sparse (2-3 total: hook, reveal, CTA) | Low |
| 3 | Riser-led (build into climax) | Medium |
| 4 | Impact-driven (stamps, hits) | Medium |
| 5 | Tick/countdown | Low |
| 6 | Silent montage (music only) | None |

## Dimension 7 — Length

| # | Length | Platform sweet spot |
|---|---|---|
| 1 | 15s | Reels hook, TikTok fast |
| 2 | 30s | TikTok primary, Reels ideal |
| 3 | 45s | Reels, longer story |
| 4 | 60s | Reels, TikTok continuation |
| 5 | 90s | TikTok, story arc |
| 6 | 2-3min | Long-form, YouTube Shorts max |

## Dimension 8 — Grade Direction

| # | Direction | Note |
|---|---|---|
| 1 | Warm (warm-daylight) | Skin-safe, editorial |
| 2 | Teal-orange | Cinematic |
| 3 | B&W → color | Transformation arc |
| 4 | Desaturated | Muted, moody |
| 5 | High-contrast | Punchy |
| 6 | Neutral skin-safe | Talking-head default |

## Dimension 9 — Text Layout

| # | Layout | Use when |
|---|---|---|
| 1 | Lower-thirds | Talking head, minimal |
| 2 | Full-screen cards | Infographic/explainer |
| 3 | Corner stamps | Montage labels |
| 4 | Caption-strip (bottom 12%) | Key spoken lines |
| 5 | Center-top band (20-42%) | Hook/CTA |
| 6 | Mixed (per-beat) | Complex arcs |

## Dimension 10 — Transition Style

| # | Type | When |
|---|---|---|
| 1 | Hard cut (default, 70%+) | Most cuts |
| 2 | Punch-in zoom (200-300ms) | Gear items, labels |
| 3 | Blur morph | Tone changes |
| 4 | White dip (max 1/video) | Aspirational peak |
| 5 | Whip pan | Location/zone changes |
| 6 | Match cut | Similar objects |

## Dimension 11 — Title Animation

| # | Style |
|---|---|
| 1 | Word-by-word bounce |
| 2 | Single-line slide-up |
| 3 | Blur-in |
| 4 | Letter-by-letter |
| 5 | Mask wipe |
| 6 | Scale settle |

## Dimension 12 — Aspect

| # | Ratio | Use |
|---|---|---|
| 1 | 9:16 (primary) | Reels, TikTok, Shorts |
| 2 | 4:5 (feed) | IG feed carousel |
| 3 | 1:1 (square) | Carousel, static |
| 4 | 16:9 | Long-form, YouTube |

## Rules

1. **Never repeat the same option number in any dimension two videos in a row.**
2. When a series spans multiple days, each day gets a distinct fingerprint (see `docs/video-variation-ledger.md`).
3. Fonts must be bundled locally (`fonts/*.woff2`) before render — no remote font loading.
4. Log the fingerprint in `docs/post-tracker.md` after every render.

## Post-Tracker Format

```markdown
## YYYY-MM-DD — <video name>
- Fonts: D1#1 · Palette: D2#1 · Hook: D3#1 · CTA: D4#1
- Beat: D5#2 · SFX: D6#1 · Length: D7#2 · Grade: D8#3
- Text: D9#5 · Transitions: D10#2 · Title anim: D11#1 · Aspect: D12#1
- Music: <track> · Template: <format>
```
