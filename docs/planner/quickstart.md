# Quickstart — where things are, how to run

## Layers

```
library/<slug>/     raw transcripts (gitignored, re-ingest anytime)
outputs/<slug>/     canonical work — analysis, research, scripts, storyboards, diagrams, code
workspace/          per-video production folders (generated, rebuild anytime)
calendar/           7/14-day plans + board card lists
skill/              SKILL.md (orchestrator) + agents/ (7 stages) + templates/ + persona.yaml
config.yaml         board numbers, model, paths
```

## Commands (from repo root, use .venv)

```bash
# ingest any source (video/playlist/blog/audio/text)
.venv/bin/python scripts/ingest.py "<URL or text>"

# materialize per-video folders (after agents produced outputs/<slug>/)
rm -rf workspace && .venv/bin/python scripts/workspace.py

# sync board cards (items files in calendar/)
.venv/bin/python scripts/board.py --project 7 calendar/items_shorts.json
.venv/bin/python scripts/board.py --project 8 calendar/items_longs.json
```

## Where to review everything

- **Boards (live status):** https://github.com/users/noah-sheldon/projects/7 (short) · https://github.com/users/noah-sheldon/projects/8 (long)
- **Content plan:** `calendar/module-content-plan.md` (module → long-form + shorts)
- **Old week plans:** `calendar/archive/` (superseded, kept for history)
- **Film kits:** `workspace/short-form/<date>/<video>/` and `workspace/long-form/<date>/<video>/`
- **Skill docs:** `docs/PLAN.md` (architecture) · `docs/production-setup.md` (filming kit)

## How the pipeline works (one line)

Paste source → ingest → agents (analyze → research → script → director → plan) → workspace folders + board cards.

**Your topics win:** give Noah's topics (e.g. "framework vs from scratch — trade-offs"), agents build around them. No topic list = pipeline fills from source gaps (rejectable).
