# ContentForge — VPS Development Handoff (OpenHands)

Run the build on your Netcup VPS with a persistent OpenHands agent. Everything below is turnkey; the docs in this repo (PLAN.md, docs/hld.md, docs/lld.md) and board #10 are the single source of truth.

## 1. Provision the VPS (one command)

On a fresh Ubuntu 24.04 / Debian 12 Netcup VPS, as root:

```bash
curl -fsSL https://raw.githubusercontent.com/noah-sheldon/contentforge/main/deploy/bootstrap-dev.sh | bash
```

Installs: git, ffmpeg, Docker + compose, Node 22, uv, GitHub CLI, tmux; creates a non-root `dev` user; clones `contentforge`; enables UFW (SSH only) + fail2ban.

## 2. Configure secrets + GitHub (one-time)

```bash
su - dev
gh auth login        # device flow — needed for private repo clones + board access
cd ~/contentforge && cp .env.example .env && nano .env   # set DEEPSEEK_API_KEY (and others)
export GITHUB_TOKEN="<classic PAT with repo + project scopes>"   # for OpenHands GitHub integration
```

## 3. Start OpenHands (detached, survives disconnects)

```bash
su - dev
cd ~/contentforge
./deploy/openhands-run.sh     # starts OpenHands on port 3000, repo mounted at /workspace
docker logs openhands | grep -i password   # first-run access password
```

- **The build brief is a microagent**: `.openhands/microagents/repo.md` — OpenHands loads it automatically when it works in the repo. Nothing to paste.
- **Phone access**: Termius port-forward (`3000`) or a Cloudflare Tunnel:
  `cloudflared tunnel --url http://localhost:3000`
- **Restart after reboot**: `docker start openhands` (or add `--restart unless-stopped` to the run command).
- **Stop/start**: `docker stop openhands` / `./deploy/openhands-run.sh` again.

Clone the merge sources (the agent needs them as siblings):

```bash
cd ~ && gh repo clone noah-sheldon/content-planner && gh repo clone noah-sheldon/agentic-video-editing
```

## 4. The agent brief (what the microagent instructs)

The microagent tells the agent to:
1. Read PLAN.md, docs/hld.md, docs/lld.md and board #10 first.
2. Execute phases **P0 -> P1 -> P2** strictly in order (issues #1-#3, then #4-#6 later).
3. For each phase: implement against the issue's acceptance criteria, verify by actually running the checks, update the board (`gh project item-edit` → In Progress / Done), commit conventional, push.
4. Stop and post to the issue before any architecture change; autonomous on implementation details.

P0 in short: merge `content-planner` + `agentic-video-editing` into the uv workspace, dedupe persona/voice/brand, port the missing scripts, kill hardcoded paths. Full steps + ACs: issue #1.

## 5. Development loop

- Agent works in `/workspace` (mounted from `~/contentforge`), pushes to GitHub, updates board #10 after each phase.
- Pipeline work runs through the host docker compose stack (docker.sock is mounted to the sandbox) — same images as production.
- Scratch media lives under `~/contentforge/workspace/` (gitignored); clean weekly:
  `find ~/contentforge/workspace -type f -mtime +14 -delete`
- Dev database: MongoDB Atlas M0 (free) or a local `mongo` container — never point dev at production data.

## 6. Security + maintenance

- SSH: keys only; set `PasswordAuthentication no` once key auth is confirmed.
- UFW allows only SSH; the OpenHands UI is reached via port-forward or Tunnel, never exposed publicly.
- RAM budget (8 GB total): OpenHands ~1-2 GB + one render at a time (3-4 GB). Keep the render queue at concurrency 1; do not run parallel renders on this box.
- Nightly backups (from P2): `mongodump` to Hetzner OBJ; Netcup COW snapshots for the VM.
- Updates: `apt update && apt upgrade`; `docker compose pull`; `docker pull ghcr.io/all-hands-ai/openhands:main` — weekly.

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| OpenHands not starting | `docker logs openhands` — check LLM_API_KEY / GITHUB_TOKEN are set |
| Access password lost | `docker logs openhands | grep -i password` |
| Private repo clone fails | `gh auth login` again; `gh auth status` |
| Docker permission denied | `sudo usermod -aG docker dev` then re-login |
| Agent stuck on a decision | Answer on the issue — the agent posts blockers there |
| Want a lighter agent instead | Qwen CLI alternative: `tmux new -s dev` then `qwen` (auth via `~/.qwen/settings.json` or `/auth`) |
