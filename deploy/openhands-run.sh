#!/usr/bin/env bash
# ContentForge — start OpenHands on the VPS (detached, survives SSH disconnects)
# The build brief is auto-loaded from .openhands/microagents/repo.md in the repo.
# Usage: run as the dev user.
set -euo pipefail

# Model config (DeepSeek as OpenAI-compatible endpoint). Override via env if needed.
LLM_MODEL="${LLM_MODEL:-deepseek-chat}"
LLM_BASE_URL="${LLM_BASE_URL:-https://api.deepseek.com}"
LLM_API_KEY="${DEEPSEEK_API_KEY:-}"

[ -n "$LLM_API_KEY" ] || { echo "error: set DEEPSEEK_API_KEY (e.g. in ~/contentforge/.env)"; exit 1; }
[ -n "${GITHUB_TOKEN:-}" ] || echo "warn: GITHUB_TOKEN not set — board updates and private repo clones need it"

docker rm -f openhands >/dev/null 2>&1 || true

docker run -d --name openhands \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE="${SANDBOX_RUNTIME_CONTAINER_IMAGE:-docker.all-hands.dev/all-hands-ai/runtime:0.53-nikolaik}" \
  -e LLM_MODEL="$LLM_MODEL" \
  -e LLM_BASE_URL="$LLM_BASE_URL" \
  -e LLM_API_KEY="$LLM_API_KEY" \
  -e GITHUB_TOKEN="${GITHUB_TOKEN:-}" \
  -e WORKSPACE_MOUNT_PATH="$HOME/contentforge" \
  -v "$HOME/contentforge":/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$HOME/.openhands":/.openhands \
  ghcr.io/all-hands-ai/openhands:main

echo "OpenHands running on http://localhost:3000"
echo "First run: check the container log for the access password:"
echo "  docker logs openhands | grep -i password"
echo "Phone access via Cloudflare Tunnel (recommended):"
echo "  cloudflared tunnel --url http://localhost:3000"
