# ContentForge

Fully dynamic agentic content production SaaS: ingest any source, plan and write in your brand voice, capture live web footage, produce short/long-form video, deliver MP4 / SRT / thumbnails / captions.

Built by merging two existing pipelines (P0, 2026-08-31):
- **content-planner** -> `skills/planner/`, `python/scripts/` (ingest, research, script, capture, board sync)
- **agentic-video-editing** -> `skills/video-agent/`, `python/` (agents, services, tighten, transcribe, compose, render)

Everything is generated at runtime from validated config + LLM — nothing hardcoded per video — and every tenant customizes brand, voice, and templates.

## Monorepo (uv workspace)

```
apps/        web app (Next.js, P4)
services/    Cloudflare Workers API (Hono, P2)
workers/     pipeline + LiteLLM containers (P2)
python/      agents + pipeline scripts (merged from both source repos)
skills/      production runbooks (planner, video-agent, post-writer; video-editor = legacy editorial reference)
prompts/     versioned prompt registry
templates/   HyperFrames composition templates
config/      persona.yaml (single source), voice.md, planner.yaml, brand
docs/        hld.md, lld.md, planner/, design docs
deploy/      VPS bootstrap, handoff, compose
library/ outputs/ calendar/ workspace/   gitignored data dirs
```

## Quick start

```bash
uv sync                # install python/ workspace deps (requires uv)
uv run python python/scripts/capture.py --help
```

## Design docs

- **[PLAN.md](PLAN.md)** — phased roadmap P0-P5 (tracked on the ContentForge — Build GitHub project)
- **[docs/hld.md](docs/hld.md)** — high-level: Cloudflare edge (Workers API, Workflows, Queues, Tunnel), Netcup VM compute (Docker Compose), MongoDB Atlas, Hetzner Object Storage, WorkOS AuthKit, LiteLLM BYOK gateway, Vercel web
- **[docs/lld.md](docs/lld.md)** — low-level: schemas, endpoints, workflow steps, LLM layer, package map
- **[deploy/HANDOFF.md](deploy/HANDOFF.md)** — VPS build agent handoff
