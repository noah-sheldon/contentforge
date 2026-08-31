---
description: "Write per-platform social captions for a video or topic. Reads config/persona.yaml for voice, platform YAMLs for rules, docs/platform-caption-limits.md for verified char limits. Outputs one caption per platform."
---

# Caption Writer

Writes captions for every platform from one source video or topic. Human voice, Grade 5-6 plain speech, platform-optimized.

## Inputs

- Video title / topic / hook text (what the video is about)
- Optional: master draft from `python/agents/copywriter.py` (if already written)
- Optional: platform list (default: all 8)

## Source of Truth (read these)

1. `config/persona.yaml` — creator name, title, tone, content pillars
2. `python/agents/platforms/<platform>.yaml` — per-platform tone, char limits, hooks, what_works
3. `docs/platform-caption-limits.md` — VERIFIED char limits + design rules (single source of truth)
4. `python/agents/prompts/copy/copywriter.yaml` — the voice prompt (Grade 5-6, first person, messy/typed feel)

## Voice Rules (HARD, all platforms)

- **ZERO em-dashes.** Plain punctuation: commas, periods, colons. Restructure if needed.
- **ZERO emoji in repo files.** (Add at post time only, 1-2 max.)
- **Human-written feel** — like typed on a phone, varied sentence lengths, no rhythmic parallel structures, no AI patterns.
- **Grade 5-6 words.** No jargon. Explain or drop any term a beginner wouldn't know.
- **No day numbers** ("Day 1 of 7"). Use "follow for the next one" / "follow along" instead.
- **No employer names.** First person. One specific story with real detail.
- **No meta-commentary** ("Here is the lesson", "The takeaway").
- **No triple-structure closings** ("Learn X. Understand Y. Know Z."). End naturally.

## Caption Design Rules (from platform-caption-limits.md)

- Captions are EXTREMELY DETAILED by default — context paragraph, every point expanded, save CTA, series tease; max out the platform limit.
- First ~100 chars = hook + save CTA. Every platform truncates in the feed.
- Full breakdown goes below the "more" fold.
- Detail drives saves, comments, reading time. Video watch time is owned by the video.

## Per-Platform Adaptations

| Platform | Limit | Hashtags | Special |
|---|---|---|---|
| Instagram | 2,200 | 3-5 | First line = hook zone; line breaks work |
| TikTok | 4,000 (native) / 2,200 (API) | 3-5 | Short punchy first line (~40-100 chars visible) |
| YouTube Shorts | 5,000 (web/Studio) | Max 15 | No separate title — description IS the title; first ~100 chars visible |
| LinkedIn | 3,000 | 3-5 | Professional narrative, line breaks = paragraphs |
| X | 280 (free) / 25,000 (Premium) | 1-2 | Thread format if >280; hook in first line |
| Threads | 500 | 1-3 | Conversational, community-building |
| Facebook | 63,206 | 2-3 | Long-form welcome; link + question |
| YouTube Long | 5,000 | Max 15 | Timestamps + description links |

Tone per platform from its YAML (instagram=visually-driven aspirational; linkedin=professional thought leadership; tiktok=casual trend-aware; x=tight; threads=conversational).

## Output Format

```markdown
# Captions — <video title>

## Instagram
<caption text>

## TikTok
<caption text>

## YouTube Shorts
<description text>

## LinkedIn
<caption text>

## X
<caption or thread>

## Threads
<caption text>

## Facebook
<caption text>

## YouTube Long
<description text>
```

## Checklist

- [ ] Zero em-dashes
- [ ] Zero emoji
- [ ] Grade 5-6 words, no jargon
- [ ] No day numbers, no employer names
- [ ] First ~100 chars = hook + save CTA
- [ ] Within verified char limits
- [ ] Reads human, not AI-drafted
