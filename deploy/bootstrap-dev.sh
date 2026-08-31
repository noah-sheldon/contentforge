#!/usr/bin/env bash
# ContentForge — Netcup VPS development bootstrap
# One command, idempotent. Run as root on a fresh Ubuntu 24.04 / Debian 12.
#   curl -fsSL https://raw.githubusercontent.com/noah-sheldon/contentforge/main/deploy/bootstrap-dev.sh | bash
set -euo pipefail

DEV_USER="${DEV_USER:-dev}"
WORKSPACE="/home/${DEV_USER}"
REPO_URL="https://github.com/noah-sheldon/contentforge.git"

echo "==> ContentForge VPS bootstrap (user: ${DEV_USER})"

# 0. must be root
[ "$(id -u)" -eq 0 ] || { echo "error: run as root (sudo -i)"; exit 1; }

# 1. system packages (ffmpeg for the pipeline, docker for the compose stack)
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y curl git build-essential ca-certificates gnupg tmux ufw fail2ban \
  ffmpeg docker.io docker-compose-v2

# 2. dev user (non-root) + docker group
id -u "${DEV_USER}" >/dev/null 2>&1 || useradd -m -s /bin/bash -G docker "${DEV_USER}"
usermod -aG docker "${DEV_USER}"

# 3. Node 22+ (NodeSource) — required for HyperFrames (npx) and tooling
if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

# 4. uv (Python version manager + package manager)
su - "${DEV_USER}" -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'

# 5. Qwen Code CLI (official standalone installer)
su - "${DEV_USER}" -c 'curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.sh | bash'

# 6. GitHub CLI (official apt repo) — for gh auth + private repo clones
if ! command -v gh >/dev/null 2>&1; then
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg -o /usr/share/keyrings/githubcli-archive-keyring.gpg
  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list
  apt-get update -y
  apt-get install -y gh
fi

# 7. clone contentforge (public) into the workspace
su - "${DEV_USER}" -c "git clone ${REPO_URL} ${WORKSPACE}/contentforge 2>/dev/null || (cd ${WORKSPACE}/contentforge && git pull --ff-only)"

# 8. .env from example if present
if [ -f "${WORKSPACE}/contentforge/.env.example" ] && [ ! -f "${WORKSPACE}/contentforge/.env" ]; then
  cp "${WORKSPACE}/contentforge/.env.example" "${WORKSPACE}/contentforge/.env"
  chown "${DEV_USER}:" "${WORKSPACE}/contentforge/.env"
  echo "==> created .env from example — fill in API keys"
fi

# 9. firewall: SSH only. fail2ban on.
ufw allow OpenSSH >/dev/null 2>&1 || true
ufw --force enable >/dev/null 2>&1 || true
systemctl enable --now fail2ban >/dev/null 2>&1 || true

echo ""
echo "==> BOOTSTRAP DONE"
echo "    Next steps:"
echo "    1. su - ${DEV_USER}"
echo "    2. gh auth login          # device flow — grants access to private repos"
echo "    3. cd ~/contentforge && tmux new -s dev && qwen"
echo "    4. First run of qwen: /auth  (or copy ~/.qwen/settings.json from your Mac via scp)"
echo "    5. Paste the AGENT BRIEF from HANDOFF.md"
echo ""
echo "    Recommend: SSH key auth for root + dev user (PasswordAuthentication no)."
echo "    VPS specs assumed: Netcup VPS 1000 G12 (4 vCPU / 8 GB)."
