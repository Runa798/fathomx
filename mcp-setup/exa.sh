#!/usr/bin/env bash
# mcp-setup/exa.sh — Register only the Exa MCP server
# Idempotent: removes previous registration before adding.
#
# Usage:
#   ./mcp-setup/exa.sh
#
# Required env vars (or set in .env):
#   EXA_API_KEY — Exa API key (get one at https://exa.ai)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

# ─── Colors ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; RESET='\033[0m'
ok()   { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error(){ echo -e "${RED}[ERROR]${RESET} $*" >&2; }
info() { echo -e "${CYAN}[INFO]${RESET}  $*"; }

# ─── Load .env ───────────────────────────────────────────────────────────────
if [[ -f "${REPO_ROOT}/.env" ]]; then
  info "Loading ${REPO_ROOT}/.env"
  set -a; source "${REPO_ROOT}/.env"; set +a
fi

EXA_API_KEY="${EXA_API_KEY:-}"

# ─── Validate ────────────────────────────────────────────────────────────────
if [[ -z "${EXA_API_KEY}" ]]; then
  error "EXA_API_KEY is not set."
  echo
  echo "Usage:"
  echo "  export EXA_API_KEY=<your-key>"
  echo "  ./mcp-setup/exa.sh"
  echo
  echo "  — or — create ${REPO_ROOT}/.env with:"
  echo "  EXA_API_KEY=<your-key>"
  echo
  echo "  Get a key at: https://exa.ai"
  exit 1
fi

# ─── Check prerequisites ─────────────────────────────────────────────────────
for cmd in claude node npm; do
  if ! command -v "$cmd" &>/dev/null; then
    error "Required command not found: $cmd"
    exit 1
  fi
done

# ─── Build JSON config ────────────────────────────────────────────────────────
CONFIG=$(cat <<EOF
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "exa-mcp-server"],
  "env": {
    "EXA_API_KEY": "${EXA_API_KEY}"
  }
}
EOF
)

# ─── Register ────────────────────────────────────────────────────────────────
info "Removing existing exa registration (if any)..."
claude mcp remove exa 2>/dev/null || true

info "Registering Exa MCP (scope: user)..."
if claude mcp add-json exa --scope user "${CONFIG}"; then
  ok "Exa MCP registered successfully"
  echo
  echo "  Package:  exa-mcp-server (via npx)"
  echo "  Docs:     https://docs.exa.ai"
  echo
  echo "  Verify with: claude mcp list"
else
  error "Failed to register Exa MCP"
  exit 1
fi
