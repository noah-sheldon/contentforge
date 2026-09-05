# Social Media Content Studio -- AI Agent Instructions

## Project Overview
Content pipeline for Noah Sheldon. Two tracks:
- **Text posts** with optional ByteByteGo-style animations (LinkedIn, X, Threads)
- **Short-form video** editing pipeline (Instagram, TikTok, YouTube Shorts, Facebook, YouTube long-form)

All video production is **HyperFrames-only**. Format templates live in `templates/short-form/`.

## Entry Points

### Chat (recommended)
Tell me a topic. I run the pipeline:
1. Copywriter writes draft in Noah's voice
2. You approve/edit
3. Platform experts adapt per platform
4. AnimationDirector decides if MP4 needed
5. I show you the final output

### Research
`make research` -- discovers trends, filters by niche, checks topic history, returns 3 approved topics.

### Video Editing
Tell me you have footage. I scan the folder, propose a shot list, you approve, I build the composition via HyperFrames.
- **MASTER = `skills/video-agent/SKILL.md` (v1.4.1, self-contained)** — load it and follow ALL rules inside (workflow, hard rules, screen recording, delivery, motion standard, self-review gate). It is the single source of truth for video production.
- Key rules in short: **Round PiP only** (never full-screen, both formats) · **Thumbnails always** (both formats, navy-blue headshot) · **Burned-in captions always** (word-synced as-I-speak in shorts; chunked in long-form + .srt) · **No music — SFX only, both formats** (≤-18dB vs voice) · **Word-accurate tightening** (never clip a word) · **Motion Graphics Standard mandatory** (kinetic hooks, speech-synced keywords, choreographed diagrams, ≥1 Three.js/WebGL beat in long-form) · **Self-review gate before preview/render**
- HITL: shot list approval -> rough cut review -> final render
- Quality settings: 1920x1080 / 1080x1920, 30fps, master CRF 10 + social CRF 14
- See `skills/video-agent/SKILL.md` for the full workflow (it supersedes the older `.qwen/skills/video-editor/` reference)

## Workflows

### Text Post (with optional animation)
```
Topic -> Copywriter -> [you approve] -> Platform Experts (LinkedIn, X, Threads)
  -> Review -> AnimationDirector checks if content needs visual blocks
    -> YES: render MP4 via HyperFrames
    -> NO: save text only
```

### Research -> Topic Selection
```
make research -> scrapes YouTube, X, web -> niche filter
  -> topic engine (novelty check, complexity score)
  -> review loop -> 3 approved topics
```

### Short-form Video
```
Footage folder -> edit_video.py selects best clips
  -> crop to 9:16
  -> build composition from template (HTML + GSAP, HyperFrames)
  -> Pixabay downloads SFX only (music is banned on all videos)
  -> npx hyperframes check -> render master -> ffmpeg CRF 14 social
```

### Weekly Planning Board
The week's plan lives on a GitHub Projects board (project 7, "short-form"): every video as one item with hook, 3 points, competitor proof, and per-platform captions in the notes body. Fields, item anatomy, views, weekly rhythm, and gh CLI commands: `docs/board-convention.md`. Weekly planning agent output must follow the item notes template in that file.

## Platforms (8 total)

| Text | Video |
|---|---|
| LinkedIn | Instagram |
| X | TikTok |
| Threads | YouTube Shorts |
| | YouTube Long-form |
| | Facebook |

Each has platform YAML rules + expert adapter + prompt.

## Key Files
| File | Purpose |
|---|---|
| `python/agents/copywriter.py` | Writes master draft in Noah's voice |
| `python/agents/experts/` | Platform expert adapters (all 8) |
| `python/agents/platforms/` | Platform YAML rules + templates |
| `python/agents/prompts/` | All LLM prompts by domain |
| `python/services/pixabay.py` | SFX downloader (music is banned on all videos) |
| `python/services/text_animator.py` | HyperFrames animation orchestration |
| `templates/short-form/` | Format templates: day-in-my-life / desk-setup / transformation (each a HyperFrames project) |
| `scripts/edit_video.py` | Short-form editing pipeline |
| `persona.yaml` | Creator persona + brand + strategy |
| `docs/platform-caption-limits.md` | Verified caption char limits per platform (single source of truth) |
| `docs/platform-delivery-formats.md` | Per-platform upload ratios + output file set (9:16 Reels vs 4:5 feed/carousel) |
| `docs/` | Research: platform rules, editing patterns |

## Naming Conventions (Mandatory)

### No underscore prefixes
- Do NOT use `_name` for "private" methods or variables.
- Methods: `def scrape()`, not `def _scrape()`
- Variables: `self.cache`, not `self._cache`
- Helpers: `def format_data()`, not `def _format_data()`

### No emojis in code
- Zero emojis in any source file, comment, prompt, or config.

### Everything else: standard Python
- `snake_case` for functions, `PascalCase` for classes, `UPPER_CASE` for constants

## Engineering Principles (Ordered by Priority)

### 1. SOLID
S=one job per file, O=new platform=new class, L=swappable interfaces, I=no unused methods, D=depend on ABCs.

### 2. KISS
No K8s, no microservices. Junior can understand any file in 5 min.

### 3. DRY
Retry in `@retry_on_failure()`. Prompts in separate files. Schemas in `schemas.py`. Credentials in `.env`. Paths in `config/settings.py`.

### 4. YAGNI
No V2 before V1 works. No DB until JSON is insufficient. No dashboard until CLI is proven.

### 5. SOC
schemas.py=models, base.py=interfaces, agents/=logic, prompts/=text, config/=paths.

### 6. Design Patterns
Factory (`get_expert`), Strategy (`SearchInterface`), Template Method (`PlatformExpert`), Decorator (`@retry_on_failure`), Registry (HyperFrames templates), Facade (`run_research`), Value Object (`schemas.py`).
