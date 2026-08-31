# ContentForge

Fully dynamic agentic content production SaaS: ingest any source, plan and write in your brand voice, capture live web footage, produce short/long-form video, deliver MP4 / SRT / thumbnails / captions.

Built by merging two existing pipelines:
- **content-planner** — planning half: ingest, research, script, capture (Playwright), board sync
- **agentic-video-editing** — production half: tighten, transcribe, compose (HyperFrames), render, deliver

Everything is generated at runtime from validated config + LLM — nothing hardcoded per video — and every tenant customizes brand, voice, and templates.

See **[PLAN.md](PLAN.md)** for the phased build roadmap (tracked on the ContentForge — Build GitHub project), **[docs/hld.md](docs/hld.md)** for the high-level design (Cloudflare-first: Workers API, Workflows, D1, R2; Cloud Run compute; WorkOS auth; LiteLLM BYOK gateway), and **[docs/lld.md](docs/lld.md)** for the low-level design (schemas, endpoints, LLM layer, package map).
