# ContentForge — VPS Build Handoff (OpenHands)

OpenHands is already running on the Netcup VPS. This doc is about driving the build, not setup. The plan and stack live in PLAN.md + docs/hld.md + docs/lld.md; progress lives on board #10.

## Quick reference

| Thing | Where |
|---|---|
| OpenHands UI | http://localhost:3000 (or your Cloudflare Tunnel URL) |
| Workspace (mounted) | `/workspace` = `~/contentforge` on the host |
| Build brief | `.openhands/microagents/repo.md` — auto-loaded by the agent |
| Board | #10 — `gh project view 10 --owner noah-sheldon` |
| Repo | github.com/noah-sheldon/contentforge |

## Kickoff (one message in a new OpenHands conversation)

Open the contentforge workspace in OpenHands and send:

```text
Start P0.
```

The microagent loads automatically and drives the build: reads the docs + board, executes P0 (monorepo merge of the two source systems into the uv workspace), verifies acceptance criteria, updates the board, commits, pushes — then proceeds P1, P2, ... in order. It stops and posts to the issue before any architecture change.

If the microagent does not auto-load in your OpenHands version, paste the contents of `.openhands/microagents/repo.md` as the first message instead.

## Supervision

- **Watch progress**: the board (Backlog -> In Progress -> Done) and the issue threads.
- **Blockers**: the agent posts to the issue and waits. Answer there — that is its go/no-go channel.
- **RAM budget** (8 GB box): OpenHands ~1-2 GB + one render at a time (3-4 GB). Never run parallel renders.
- **Backups** (from P2): nightly `mongodump` to Hetzner OBJ; Netcup COW snapshots for the VM.

## What the agent will build (in order)

- **P0** — merge content-planner + agentic-video-editing into the contentforge uv workspace; dedupe persona/voice/brand; port missing scripts; kill hardcoded paths. (Issue #1)
- **P1** — dynamic config layer: TenantConfig (Pydantic), prompt/template/recipe registries; runtime generation instead of hand-authored videos. (Issue #2)
- **P2** — Cloudflare Workers API (Hono) + Workflows orchestration + VM pipeline container + LiteLLM; HITL checkpoints as API. (Issue #3)
- **P3** — WorkOS orgs/tenants, isolation, metering. (Issue #4)
- **P4** — Next.js dashboard + brand studio on Vercel. (Issue #5)
- **P5** — Stripe billing, onboarding, security review, sellable demo. (Issue #6)

## Troubleshooting

| Problem | Fix |
|---|---|
| Agent can't find source repos | They must be inside the workspace: `~/contentforge/_sources/` (the brief clones them at P0 start) |
| Missing tools in the sandbox (ffmpeg/gh/python) | Brief is written to verify first and install locally or use the host docker stack; check the issue for what it recorded |
| Board not updating | gh missing or GITHUB_TOKEN not reaching the sandbox — agent falls back to the GitHub REST API / issue posts; ensure GITHUB_TOKEN is set on the host env |
| OpenHands container down | `docker start openhands` (host) |
| Disconnected | Reconnect via Termius; the UI is a web app, nothing runs in your terminal |
| Agent stuck / looping | Open the conversation in the UI, steer it, or cancel and start a new conversation with "Start P0" again (state lives in git + the board) |
