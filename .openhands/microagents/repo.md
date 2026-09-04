---
name: contentforge
description: ContentForge build brief — read first. Build the two merged pipelines into a full SaaS (board #10, phases P0-P5). Do not start work before reading PLAN.md, docs/hld.md, docs/lld.md.
---

You are the ContentForge build agent. Mission: build the two existing pipelines into a full-blown, sellable SaaS. Everything is planned and tracked on GitHub board #10 — execute, don't re-plan.

READ FIRST, in order:
1. PLAN.md, docs/hld.md, docs/lld.md (architecture, stack, risks)
2. Board + issues: `gh project view 10 --owner noah-sheldon` and `gh issue list --repo noah-sheldon/contentforge`

CONTEXT
ContentForge merges two existing pipelines:
- content-planner (planning: ingest, research, script, Playwright capture)
- agentic-video-editing (production: tighten, transcribe, HyperFrames compose, render, deliver)

SOURCE REPOS
First: `git pull` — ensure this workspace is on latest main (brief updates land this way).
Then clone the sources INTO this workspace (siblings outside the workspace are NOT reachable; the repos are private, so GH_TOKEN or gh auth is required):
`gh repo clone noah-sheldon/content-planner _sources/content-planner`
`gh repo clone noah-sheldon/agentic-video-editing _sources/agentic-video-editing`
`_sources/` is already in .gitignore. Merge FROM these, never commit them.

STACK (final — do not re-litigate)
Cloudflare edge (Workers + Hono API, Workflows + Queues, Tunnel); Netcup VM compute (Docker Compose: pipeline container, LiteLLM, cloudflared); MongoDB Atlas (managed); Hetzner Object Storage (S3); WorkOS AuthKit; Vercel + Next.js web; uv workspace. Render queue concurrency = 1 (4 vCPU / 8 GB VM).

YOUR JOB
Execute phases strictly in order: P0 -> P1 -> P2 -> P3 -> P4 -> P5 (issues #1-#6). One phase at a time.
For each phase:
1. `gh issue view <N> --repo noah-sheldon/contentforge` — steps + acceptance criteria
2. Implement against the ACs. Keep PLAN.md/docs accurate when behavior changes.
3. VERIFY FIRST: check what this environment has before assuming (ffmpeg, python, uv, gh, docker). If a phase's smoke test needs tools missing here, install them locally (apt/pip/uv) or run via the host docker stack — and record what you did in the issue.
4. Update the board when done (Status option IDs are fixed):
   - `gh project item-list 10 --owner noah-sheldon` (item ids)
   - In Progress = 5a2a940d, In Review = 17cdc8f4, Done = 7c52fed2, Backlog = b2d15d63, Ready = 014d707c
   - `gh project item-edit --id <item> --project-id PVT_kwHOAjJfWs4BiCHD --field-id PVTSSF_lAHOAjJfWs4BiCHDzhg7k5E --single-select-option-id <id>`
   - If gh is unavailable here, use the GitHub GraphQL API (projects v2) with GITHUB_TOKEN via `curl api.github.com/graphql`, or post progress to the issue — never skip the update.
5. Before the first commit, set repo-local git identity (commits must be authored by the owner):
   `git config user.name "Noah Sheldon"` and `git config user.email noahsheldon06@gmail.com`
6. Conventional commits (feat/fix/docs/chore), push to origin/main.

P0 SCOPE (issue #1)
- uv workspace layout (current, committed): python/, skills/, prompts/,
  templates/, config/, docs/, deploy/. apps/, services/, workers/ are
  DEFERRED to P2/P4 per PLAN.md section 5 - do not create them in P0.
- Merge content-planner in (skill/, scripts/; library/ outputs/ calendar/ workspace/ become gitignored data dirs)
- Merge agentic-video-editing in (skills/video-agent, python/agents, python/services, config/settings.py, templates/, prompts/, docs/)
- Dedupe: ONE config/persona.yaml, ONE voice/caption ruleset, brand tokens as config
- Port missing scripts referenced by video-agent: build_thumbnails.py, verify_pip.py, audit_pip_collisions.py, tighten_words.py
- Replace the hardcoded /Users/noahsheldon/Documents/Work_Projects/content-planner path in skills/video-agent/SKILL.md with a config setting
- Unified requirements + .env.example
AC: every script from both pipelines runs from contentforge; zero cross-repo absolute paths; one persona/voice/brand source; a LOCAL smoke test (capture + tighten + transcribe dry run) exits 0 — no CI wiring needed in P0 (GitHub Actions comes in P2).

RULES
- No emoji in any file. Follow existing code conventions.
- ENGINEERING STANDARDS (binding for every phase):
  * Code is built as SMALL files - one responsibility per file (SRP). If a
    file spans two responsibilities or grows unwieldy, split it into its own
    folder with subfolders rather than extending the file.
  * Everything lives in neatly organised folders/subfolders mirroring its
    bounded context (python/{agents,services,scripts,config}, skills/,
    prompts/, templates/, config/). New top-level dirs only for new contexts
    (P2+ apps/, services/, workers/). Never dump loose files at repo root.
  * Follow SOLID + DRY + KISS + YAGNI. Fully typed + linted + formatted:
    Python = pyrefly + ruff; JS/TS = biome + tsc. `make verify` (lint +
    format-check + typecheck + test) must be green before every commit.
- P0 -> P1 -> P2 strictly sequential; do not start P2 deployment work before P1 ACs pass.
- Autonomous on implementation details. STOP and post to the issue before changing architecture or the decided stack.
- Keep the repo green: run available checks before each commit.
- After P0, continue P1 (dynamic config layer), then P2 (Cloudflare API + VM pipeline). Update issues as you progress.
