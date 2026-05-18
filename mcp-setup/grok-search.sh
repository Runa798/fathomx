#!/usr/bin/env bash
# mcp-setup/grok-search.sh — Register only the GrokSearch MCP server
# Idempotent: removes previous registration before adding.
#
# Usage:
#   ./mcp-setup/grok-search.sh
#
# Required env vars (or set in .env):
#   GROK_API_KEY   — Grok API key
#
# Optional:
#   GROK_API_URL   — Grok API endpoint (OpenAI-compatible)
#   TAVILY_API_URL — defaults to https://api.tavily.com
#   TAVILY_API_KEY — Tavily API key

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

# ─── Resolve variables ────────────────────────────────────────────────────────
GROK_API_URL="${GROK_API_URL:-}"
GROK_API_KEY="${GROK_API_KEY:-}"
TAVILY_API_URL="${TAVILY_API_URL:-https://api.tavily.com}"
TAVILY_API_KEY="${TAVILY_API_KEY:-}"

# ─── Validate ────────────────────────────────────────────────────────────────
if [[ -z "${GROK_API_KEY}" || -z "${GROK_API_URL}" ]]; then
  error "GROK_API_KEY and GROK_API_URL must both be set."
  echo
  echo "Usage:"
  echo "  export GROK_API_URL=https://your-endpoint/v1"
  echo "  export GROK_API_KEY=<your-key>"
  echo "  ./mcp-setup/grok-search.sh"
  echo
  echo "  — or — create ${REPO_ROOT}/.env with:"
  echo "  GROK_API_URL=https://your-endpoint/v1"
  echo "  GROK_API_KEY=<your-key>"
  echo "  TAVILY_API_KEY=<your-key>   # optional but recommended"
  exit 1
fi

# ─── Check prerequisites ─────────────────────────────────────────────────────
for cmd in claude uv; do
  if ! command -v "$cmd" &>/dev/null; then
    error "Required command not found: $cmd"
    exit 1
  fi
done

# ─── Build JSON config ────────────────────────────────────────────────────────
CONFIG=$(cat <<EOF
{
  "type": "stdio",
  "command": "uvx",
  "args": ["--from", "git+https://github.com/GuDaStudio/GrokSearch", "grok-search"],
  "env": {
    "GROK_API_URL": "${GROK_API_URL}",
    "GROK_API_KEY": "${GROK_API_KEY}",
    "TAVILY_API_URL": "${TAVILY_API_URL}",
    "TAVILY_API_KEY": "${TAVILY_API_KEY}"
  }
}
EOF
)

# ─── Register ────────────────────────────────────────────────────────────────
info "Removing existing grok-search registration (if any)..."
claude mcp remove grok-search 2>/dev/null || true

info "Registering GrokSearch MCP (scope: user)..."
if claude mcp add-json grok-search --scope user "${CONFIG}"; then
  ok "GrokSearch MCP registered successfully"
  echo
  echo "  Upstream: https://github.com/GuDaStudio/GrokSearch"
  echo "  API URL:  ${GROK_API_URL}"
  [[ -n "${TAVILY_API_KEY}" ]] && echo "  Tavily:   ${TAVILY_API_URL}" || warn "  Tavily key not set — Tavily supplementary search disabled"
  echo
  echo "  Verify with: claude mcp list"
else
  error "Failed to register GrokSearch MCP"
  exit 1
fi
