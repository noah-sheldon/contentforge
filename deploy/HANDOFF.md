# ContentForge — VPS Development Handoff

Run the build on your Netcup VPS with a persistent coding agent. Everything below is turnkey; the docs in this repo (PLAN.md, docs/hld.md, docs/lld.md) and board #10 are the single source of truth.

## 1. Provision the VPS (one command)

On a fresh Ubuntu 24.04 / Debian 12 Netcup VPS, as root:

```bash
curl -fsSL https://raw.githubusercontent.com/noah-sheldon/contentforge/main/deploy/bootstrap-dev.sh | bash
```

Installs: git, ffmpeg, Docker + compose, Node 22, uv, Qwen Code CLI, GitHub CLI, tmux; creates a non-root `dev` user; clones `contentforge`; enables UFW (SSH only) + fail2ban.

## 2. Configure auth (one-time)

```bash
su - dev
gh auth login        # device flow in your browser — needed to clone the private source repos
```

Qwen Code auth — headless servers cannot do browser OAuth, use an API key / Coding Plan key. Either:

- Copy your Mac config: `scp ~/.qwen/settings.json dev@<vps-ip>:~/.qwen/settings.json` (from your Mac), or
- Run `qwen`, then `/auth` and pick your provider (DeepSeek, OpenRouter, ModelStudio, etc.).

## 3. Start the persistent agent session

```bash
su - dev
cd ~/contentforge
tmux new -s dev        # session survives SSH disconnects
qwen                   # start the agent
```

Reconnect anytime — from your laptop or your phone via Termius:
`ssh dev@<vps-ip>` then `tmux attach -t dev`. The agent keeps working while you are away.

Clone the source repos the agent will merge (needs `gh auth login` first):

```bash
cd ~ && gh repo clone noah-sheldon/content-planner && gh repo clone noah-sheldon/agentic-video-editing
```

## 4. The AGENT BRIEF — paste this into the Qwen Code session on the VPS

```text
You are the ContentForge build agent, running on the Netcup VPS.

FIRST: read PLAN.md, docs/hld.md, docs/lld.md in this repo, then view the project board:
gh project view 10 --owner noah-sheldon

CONTEXT
ContentForge is a sellable, fully dynamic, multi-tenant content production SaaS.
It merges two existing pipelines:
- content-planner  (planning: ingest, research, script, Playwright capture)  -> ~/content-planner
- agentic-video-editing (production: tighten, transcribe, HyperFrames compose, render) -> ~/agentic-video-editing
The working repo is this one: ~/contentforge. The board tracks phases P0-P5 as issues #1-#6.

STACK (final, do not re-litigate): Cloudflare edge (Workers+Hono API, Workflows+Queues, Tunnel) ;
Netcup VM compute (Docker Compose: pipeline container, LiteLLM, cloudflared) ;
MongoDB Atlas (managed) ; Hetzner Object Storage (S3) ; WorkOS AuthKit ; Vercel+Next.js web ;
uv workspace. Render queue concurrency = 1 (VM is 4 vCPU / 8 GB).

YOUR JOB
Execute the phases in order, one at a time. Start with P0 (issue #1). For each phase:
1. gh issue view <N> --repo noah-sheldon/contentforge  (read steps + acceptance criteria)
2. Implement against the ACs. Update PLAN.md/docs only when behavior changes.
3. Verify: run the phase's acceptance checks (scripts must actually run).
4. Mark the board: set the phase item to In Progress while working, Done when ACs pass:
   gh project item-list 10 --owner noah-sheldon   (get item ids)
   gh project item-edit --id <item> --project-id PVT_kwHOAjJfWs4BiCHD --field-id PVTSSF_lAHOAjJfWs4BiCHDzhg7k5E --single-select-option-id <InProgress|Done option id>
5. Commit with conventional commits (feat/fix/docs/chore) matching existing history. Push.

P0 SCOPE (from issue #1)
- Create the uv workspace layout: apps/web, services/api, workers/pipeline, workers/litellm, python/, skills/, prompts/, templates/, config/, docs/, deploy/
- Move content-planner content in (skill/, scripts/; library/ outputs/ calendar/ workspace/ become gitignored data dirs)
- Move agentic-video-editing content in (skills/video-agent, python/agents, python/services, config/settings.py, templates/, prompts/, docs/)
- Dedupe: ONE config/persona.yaml, ONE voice/caption ruleset, brand tokens as config
- Port the missing scripts referenced by video-agent: build_thumbnails.py, verify_pip.py, audit_pip_collisions.py, tighten_words.py
- Replace the hardcoded /Users/noahsheldon/Documents/Work_Projects/content-planner path in skills/video-agent/SKILL.md with a config setting
- Unified requirements + .env.example
AC: every script from both pipelines runs from contentforge; zero cross-repo absolute paths;
one persona/voice/brand source; CI smoke test (capture + tighten + transcribe dry run) exits 0.

RULES
- No emoji in any file. Follow existing code conventions. SOLID/KISS/DRY.
- P0 -> P1 -> P2 strictly sequential; do not start P2 deployment work before P1 ACs pass.
- Autonomous on implementation details inside a phase; STOP and ask via the board/issue before changing architecture or the decided stack.
- Keep the repo green: run available checks before each commit.
- When P0 is done, continue to P1 (dynamic config layer), then P2 (Cloudflare API + VM pipeline). Report progress by updating issues.
```

## 5. Development loop

- Agent works in `~/contentforge`, pushes to GitHub, updates board #10 after each phase.
- Pipeline scripts run natively on the box (ffmpeg, whisper, HyperFrames) — same environment as production.
- Scratch media lives under `~/contentforge/workspace/` (gitignored); clean it weekly:
  `find ~/contentforge/workspace -type f -mtime +14 -delete`
- Dev database: MongoDB Atlas M0 (free) or a local `mongo` container via compose — do not point dev at production data.

## 6. Security + maintenance

- SSH: use keys only; set `PasswordAuthentication no` in sshd once key auth is confirmed working.
- UFW allows only SSH; the pipeline exposes nothing publicly (Cloudflare Tunnel comes with P2).
- Nightly backups (from P2): `mongodump` to Hetzner OBJ; Netcup COW snapshots for the VM itself.
- Updates: `apt update && apt upgrade`, `docker compose pull` — weekly.

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| Disconnected session | `ssh dev@<vps-ip>` → `tmux attach -t dev` |
| qwen not found | Re-run the installer (step 5 of bootstrap), or `source ~/.bashrc` |
| Private repo clone fails | `gh auth login` again; check `gh auth status` |
| Docker permission denied | `sudo usermod -aG docker dev` then re-login |
| Agent stuck on a decision | It should post to the issue; answer there or on the board |
