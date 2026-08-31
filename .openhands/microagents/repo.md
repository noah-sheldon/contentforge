---
name: contentforge
description: ContentForge build instructions — read first. Phased SaaS build (P0-P5) tracked on GitHub board #10. Do not start work without reading PLAN.md, docs/hld.md, docs/lld.md.
---

You are the ContentForge build agent, running on the Netcup VPS (4 vCPU / 8 GB).

READ FIRST: PLAN.md, docs/hld.md, docs/lld.md, then the project board:
`gh project view 10 --owner noah-sheldon`

CONTEXT
ContentForge is a sellable, fully dynamic, multi-tenant content production SaaS, merging two existing pipelines:
- content-planner (planning: ingest, research, script, Playwright capture) — sibling dir `../content-planner`
- agentic-video-editing (production: tighten, transcribe, HyperFrames compose, render) — sibling dir `../agentic-video-editing`
Working repo: this repo (contentforge). The board tracks phases P0-P5 as issues #1-#6.

STACK (final — do not re-litigate): Cloudflare edge (Workers + Hono API, Workflows + Queues, Tunnel); Netcup VM compute (Docker Compose: pipeline container, LiteLLM, cloudflared); MongoDB Atlas (managed); Hetzner Object Storage (S3); WorkOS AuthKit; Vercel + Next.js web; uv workspace. Render queue concurrency = 1 (VM is 4 vCPU / 8 GB).

YOUR JOB
Execute phases in order, one at a time. Start with P0 (issue #1). For each phase:
1. `gh issue view <N> --repo noah-sheldon/contentforge` — read steps + acceptance criteria
2. Implement against the ACs. Keep PLAN.md/docs accurate when behavior changes.
3. Verify: run the phase's acceptance checks for real (scripts must execute).
4. Update the board when done:
   `gh project item-list 10 --owner noah-sheldon` (get item ids)
   `gh project item-edit --id <item> --project-id PVT_kwHOAjJfWs4BiCHD --field-id PVTSSF_lAHOAjJfWs4BiCHDzhg7k5E --single-select-option-id <option>`
   (option: In Progress while working, Done when ACs pass)
5. Conventional commits (feat/fix/docs/chore) matching existing history. Push.

P0 SCOPE (issue #1)
- Create the uv workspace layout: apps/web, services/api, workers/pipeline, workers/litellm, python/, skills/, prompts/, templates/, config/, docs/, deploy/
- Move content-planner content in (skill/, scripts/; library/ outputs/ calendar/ workspace/ become gitignored data dirs)
- Move agentic-video-editing content in (skills/video-agent, python/agents, python/services, config/settings.py, templates/, prompts/, docs/)
- Dedupe: ONE config/persona.yaml, ONE voice/caption ruleset, brand tokens as config
- Port missing scripts referenced by video-agent: build_thumbnails.py, verify_pip.py, audit_pip_collisions.py, tighten_words.py
- Replace the hardcoded /Users/noahsheldon/Documents/Work_Projects/content-planner path in skills/video-agent/SKILL.md with a config setting
- Unified requirements + .env.example
AC: every script from both pipelines runs from contentforge; zero cross-repo absolute paths; one persona/voice/brand source; CI smoke test (capture + tighten + transcribe dry run) exits 0.

RULES
- No emoji in any file. Follow existing code conventions. SOLID/KISS/DRY.
- P0 -> P1 -> P2 strictly sequential; do not start P2 deployment work before P1 ACs pass.
- Autonomous on implementation details inside a phase. STOP and post to the issue before changing architecture or the decided stack.
- Run pipeline work through the host docker compose stack (docker.sock is mounted) — do not reinstall ffmpeg/whisper inside the sandbox.
- Keep the repo green: run available checks before each commit.
- After P0, continue to P1 (dynamic config layer), then P2 (Cloudflare API + VM pipeline). Update issues as you progress.
