# Content Planner

Turn ANY input — YouTube video/playlist, blog, website, audio file, or pasted text — into
short-form + long-form content ideas, researched briefs, scripts in Noah's voice, storyboards
with equipment call sheets, teleprompter text, and 7/14-day publishing plans synced to
GitHub Projects boards.

## Layout

```
config.yaml            ← pipeline config (boards, models, lifecycle) — edit this
requirements.txt       ← pip deps (install into .venv)
skill/
  SKILL.md             ← the orchestrator — how the whole pipeline runs
  persona.yaml         ← voice, goals, platform strategy (single source of truth)
  voice.md             ← mandatory voice rules (grade 5-6, Indian English, no jargon)
  agents/              ← 7 agent definitions (analyze, marketing, ideate, research,
                         script, director, plan) — markdown + frontmatter
scripts/               ← deterministic glue only (no per-run logic):
  ingest.py            ← download/transcribe (yt-dlp, transcript-api, mlx-whisper)
  diagram.py           ← valid .excalidraw JSON from a spec
  board.py             ← GitHub Projects cards (create + set fields)
  workspace.py         ← per-video production folders
library/<slug>/        ← ingested source (transcript + metadata)
outputs/<slug>/        ← source-level: analysis, ideas, research, scripts, storyboard, specs
calendar/              ← 7/14-day plans + board card lists (items_*.json)
workspace/             ← per-video folders: <form>/<date>/<video>/ with
                          00_script.md · 01_teleprompter.txt · 02_storyboard.md
                          03_diagrams/ · 04_research/ · 05_code/ · metadata.json
docs/                  ← PLAN.md (architecture), production-setup.md (filming kit),
                           quickstart.md (where things are)
```

## Course repo

The course content lives in its own repo:
https://github.com/noah-sheldon/ai-agents-zero-to-hero
(private; flip public when portfolio-ready). This pipeline generates the
videos for it: one high-level long-form per module + shorts per lesson.

## Quickstart

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 1. Ingest any source
.venv/bin/python scripts/ingest.py "https://www.youtube.com/watch?v=..."

# 2. Run the pipeline stages (orchestrated by skill/SKILL.md via sub-agents):
#    analyze → marketing → ideate → research → script → director → plan
#    Each stage is an agent (skill/agents/*.md) writing into outputs/<slug>/

# 3. Materialize the production workspace
.venv/bin/python scripts/workspace.py

# 4. Sync board cards
.venv/bin/python scripts/board.py --project 7 calendar/items_shorts.json
.venv/bin/python scripts/board.py --project 8 calendar/items_longs.json
```

## Principles

- **Code only for deterministic, stable mechanics.** Everything creative is an agent
  (markdown); everything configurable lives in `config.yaml` / `skill/persona.yaml`.
- **One asset → five platforms.** Same cut, watermark-free, per-platform variants.
- **Batch filming.** Plans group videos into filming days — never one session per day.
- **Voice is mandatory.** Grade 5-6 words, short sentences, one idea per line, Indian
  English, no marketing voice.
