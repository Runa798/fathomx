#!/usr/bin/env bash
# install.sh — Install FathomX MCP tools and skill
# Idempotent: safe to run multiple times.
# Usage:
#   ./install.sh             Install everything
#   ./install.sh --uninstall Remove everything

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── Bash Guard ──────────────────────────────────────────────────────────────
if [ -z "${BASH_VERSION:-}" ]; then
  echo "This installer requires bash. Run: bash install.sh" >&2
  exit 1
fi

# ─── Platform Detection ─────────────────────────────────────────────────────
# Override via: FATHOMX_PLATFORM=codex ./install.sh
detect_platform() {
  if [[ -n "${FATHOMX_PLATFORM:-}" ]]; then
    PLATFORM="${FATHOMX_PLATFORM}"
  elif command -v claude &>/dev/null; then
    PLATFORM="claude-code"
  elif command -v opencode &>/dev/null; then
    PLATFORM="opencode"
  elif command -v codex &>/dev/null; then
    PLATFORM="codex"
  else
    PLATFORM="unknown"
  fi

  case "${PLATFORM}" in
    claude-code) SKILL_TARGET="${HOME}/.claude/skills/fathomx" ;;
    opencode)    SKILL_TARGET="${HOME}/.claude/skills/fathomx" ;;
    codex)       SKILL_TARGET="${CODEX_HOME:-${HOME}/.codex}/skills/fathomx" ;;
    *)           SKILL_TARGET="${HOME}/.claude/skills/fathomx" ;;
  esac
}

detect_platform

# ─── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
ok()      { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }
section() { echo -e "\n${BOLD}$*${RESET}"; }

# ─── Load .env ───────────────────────────────────────────────────────────────
if [[ -f "${SCRIPT_DIR}/.env" ]]; then
  info "Loading .env from ${SCRIPT_DIR}/.env"
  # shellcheck disable=SC1090
  set -a; source "${SCRIPT_DIR}/.env"; set +a
else
  warn ".env not found — using environment variables only"
fi

# ─── Defaults ────────────────────────────────────────────────────────────────
GROK_API_URL="${GROK_API_URL:-}"
GROK_API_KEY="${GROK_API_KEY:-}"
TAVILY_API_URL="${TAVILY_API_URL:-https://api.tavily.com}"
TAVILY_API_KEY="${TAVILY_API_KEY:-}"
EXA_API_KEY="${EXA_API_KEY:-}"

# ─── Uninstall ────────────────────────────────────────────────────────────────
uninstall() {
  section "=== Uninstalling FathomX ==="

  info "Removing GrokSearch MCP registration..."
  if claude mcp remove grok-search 2>/dev/null; then
    ok "grok-search removed"
  else
    warn "grok-search was not registered (skipping)"
  fi

  info "Removing Exa MCP registration..."
  if claude mcp remove exa 2>/dev/null; then
    ok "exa removed"
  else
    warn "exa was not registered (skipping)"
  fi

  info "Removing skill symlink/directory at ${SKILL_TARGET}..."
  if [[ -L "${SKILL_TARGET}" ]]; then
    rm -f "${SKILL_TARGET}"
    ok "Symlink removed: ${SKILL_TARGET}"
  elif [[ -d "${SKILL_TARGET}" ]]; then
    rm -rf "${SKILL_TARGET}"
    ok "Directory removed: ${SKILL_TARGET}"
  else
    warn "Skill not installed at ${SKILL_TARGET} (skipping)"
  fi

  echo
  ok "Uninstall complete."
}

# ─── Check flag ───────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
  uninstall
  exit 0
fi

# ─── Install ──────────────────────────────────────────────────────────────────
section "=== Installing FathomX ==="

# 1. Prerequisites
section "Step 1/7  Checking prerequisites..."

check_cmd() {
  local cmd="$1"
  if command -v "$cmd" &>/dev/null; then
    ok "$cmd found: $(command -v "$cmd")"
  else
    error "$cmd not found — please install it first"
    exit 1
  fi
}

check_cmd python3
check_cmd uv
check_cmd node
check_cmd npm

if [[ "${PLATFORM}" == "claude-code" ]]; then
  ok "Platform: Claude Code"
  check_cmd claude
elif [[ "${PLATFORM}" == "opencode" ]]; then
  ok "Platform: OpenCode"
  warn "MCP auto-registration not supported for OpenCode — you'll need to configure MCP servers manually"
  warn "See: https://github.com/Runa798/fathomx#opencode-setup"
elif [[ "${PLATFORM}" == "codex" ]]; then
  ok "Platform: Codex"
  warn "MCP auto-registration not supported for Codex — you'll need to configure MCP servers manually"
  warn "See: https://github.com/Runa798/fathomx#codex-setup"
else
  warn "No supported AI coding IDE found (claude / opencode / codex)"
  warn "Installing skill files only — configure MCP servers manually"
fi

# 2. Key validation
section "Step 2/7  Checking API keys..."

MISSING_KEYS=0

if [[ -z "${GROK_API_KEY}" ]]; then
  warn "GROK_API_KEY is not set — GrokSearch MCP will NOT be registered"
  MISSING_KEYS=1
else
  ok "GROK_API_KEY is set"
fi

if [[ -z "${GROK_API_URL}" ]]; then
  warn "GROK_API_URL is not set — GrokSearch MCP will NOT be registered"
  MISSING_KEYS=1
else
  ok "GROK_API_URL is set: ${GROK_API_URL}"
fi

if [[ -z "${TAVILY_API_KEY}" ]]; then
  warn "TAVILY_API_KEY is not set — Tavily supplementary search disabled"
else
  ok "TAVILY_API_KEY is set"
fi

if [[ -z "${EXA_API_KEY}" ]]; then
  info "EXA_API_KEY is not set — Exa MCP will be skipped (optional)"
else
  ok "EXA_API_KEY is set"
fi

# 3. Register GrokSearch MCP
section "Step 3/7  Registering GrokSearch MCP..."

if [[ "${PLATFORM}" != "claude-code" ]]; then
  info "Skipping MCP registration (not Claude Code — configure manually)"
elif [[ "${MISSING_KEYS}" -eq 0 ]]; then
  GROK_CONFIG=$(cat <<EOF
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

  # Remove existing registration first (idempotent)
  claude mcp remove grok-search 2>/dev/null || true

  if claude mcp add-json grok-search --scope user "${GROK_CONFIG}"; then
    ok "GrokSearch MCP registered (scope: user)"
  else
    error "Failed to register GrokSearch MCP"
    exit 1
  fi
else
  warn "Skipping GrokSearch registration (missing GROK_API_KEY)"
fi

# 4. Register Exa MCP (optional)
section "Step 4/7  Registering Exa MCP (optional)..."

if [[ "${PLATFORM}" != "claude-code" ]]; then
  info "Skipping Exa MCP registration (not Claude Code)"
elif [[ -n "${EXA_API_KEY}" ]]; then
  EXA_CONFIG=$(cat <<EOF
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

  # Remove existing registration first (idempotent)
  claude mcp remove exa 2>/dev/null || true

  if claude mcp add-json exa --scope user "${EXA_CONFIG}"; then
    ok "Exa MCP registered (scope: user)"
  else
    error "Failed to register Exa MCP"
    exit 1
  fi
else
  info "Skipping Exa MCP (EXA_API_KEY not set)"
fi

# 5. Install skill
section "Step 5/7  Installing FathomX skill..."

SKILL_SOURCE="${SCRIPT_DIR}/skill"

if [[ ! -d "${SKILL_SOURCE}" ]]; then
  error "Skill directory not found: ${SKILL_SOURCE}"
  exit 1
fi

# Ensure ~/.claude/skills/ exists
mkdir -p "${HOME}/.claude/skills"

# Remove existing install (symlink or real dir) for idempotency
if [[ -L "${SKILL_TARGET}" ]]; then
  rm -f "${SKILL_TARGET}"
  info "Removed existing symlink at ${SKILL_TARGET}"
elif [[ -d "${SKILL_TARGET}" ]]; then
  rm -rf "${SKILL_TARGET}"
  info "Removed existing directory at ${SKILL_TARGET}"
fi

# Try symlink first; fall back to copy
if ln -s "${SKILL_SOURCE}" "${SKILL_TARGET}" 2>/dev/null; then
  ok "Skill symlinked: ${SKILL_SOURCE} → ${SKILL_TARGET}"
else
  cp -r "${SKILL_SOURCE}" "${SKILL_TARGET}"
  ok "Skill copied to ${SKILL_TARGET}"
fi

# 6. Install Python orchestrator
section "Step 6/7  Installing Python orchestrator..."

ORCHESTRATOR_DIR="${SCRIPT_DIR}/orchestrator"

if [[ -d "${ORCHESTRATOR_DIR}" ]]; then
  if command -v pip3 &>/dev/null && pip3 install --user -e "${ORCHESTRATOR_DIR}" 2>/dev/null; then
    ok "Python orchestrator installed"
  else
    warn "Python orchestrator install failed (optional component)"
  fi
else
  warn "Python orchestrator directory not found: ${ORCHESTRATOR_DIR}"
fi

# 7. Create config directory
section "Step 7/7  Creating FathomX config directory..."

CONFIG_DIR="${HOME}/.fathomx"
CONFIG_PATH="${CONFIG_DIR}/config.json"
mkdir -p "${CONFIG_DIR}"

if [[ ! -f "${CONFIG_PATH}" ]]; then
  CONFIG_PATH="${CONFIG_PATH}" \
  GROK_API_URL="${GROK_API_URL}" \
  GROK_API_KEY="${GROK_API_KEY}" \
  TAVILY_API_URL="${TAVILY_API_URL}" \
  TAVILY_API_KEY="${TAVILY_API_KEY}" \
  EXA_API_KEY="${EXA_API_KEY}" \
  python3 - <<'PYEOF'
import json
import os
from pathlib import Path

path = Path(os.environ["CONFIG_PATH"])
config = {
    "version": "1.2.0",
    "models": {},
    "search": {
        "grok": {
            "api_url": os.environ.get("GROK_API_URL", ""),
            "api_key": os.environ.get("GROK_API_KEY", ""),
            "tavily_api_url": os.environ.get("TAVILY_API_URL", "https://api.tavily.com"),
            "tavily_api_key": os.environ.get("TAVILY_API_KEY", ""),
        },
        "exa": {
            "api_key": os.environ.get("EXA_API_KEY", ""),
        },
    },
    "features": {
        "multi_model": False,
        "scope_expansion": True,
        "gemini_search": False,
    },
    "workspace": {
        "base_dir": "workspace",
    },
}
path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PYEOF
  ok "Created default config: ${CONFIG_PATH}"
else
  ok "Config already exists: ${CONFIG_PATH}"
fi

info "Run python3 -m fathomx setup for full multi-model configuration"

# Disable CC native search (optional but recommended)
section "Configuring Claude Code native search..."

# CC_SETTINGS is the project-level settings file
CC_SETTINGS="${SCRIPT_DIR}/.claude/settings.json"
mkdir -p "$(dirname "${CC_SETTINGS}")"

if [[ ! -f "${CC_SETTINGS}" ]]; then
  echo '{}' > "${CC_SETTINGS}"
fi

# Use python3 to merge JSON (avoids jq dependency)
CC_SETTINGS="${CC_SETTINGS}" python3 - <<'PYEOF'
import json, sys, os

path = os.environ.get("CC_SETTINGS")
with open(path) as f:
    cfg = json.load(f)

# Disable WebSearch so Grok/Exa MCP tools are used instead
cfg.setdefault("env", {})
cfg["env"]["CLAUDE_CODE_DISABLE_WEBSEARCH"] = "1"

with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print("  Written:", path)
PYEOF

ok "Native CC WebSearch disabled in ${CC_SETTINGS}"

# ─── Summary ──────────────────────────────────────────────────────────────────
echo
echo -e "${BOLD}════════════════════════════════════════════${RESET}"
echo -e "${GREEN}  Installation complete!${RESET}"
echo -e "${BOLD}════════════════════════════════════════════${RESET}"
echo
echo "  Platform:    ${PLATFORM}"
echo "  Skill:       ${SKILL_TARGET}"
if [[ "${PLATFORM}" == "claude-code" ]]; then
  [[ "${MISSING_KEYS}" -eq 0 ]] && echo "  GrokSearch:  registered (user scope)" || echo "  GrokSearch:  SKIPPED (set GROK_API_KEY)"
  [[ -n "${EXA_API_KEY}" ]]     && echo "  Exa:         registered (user scope)" || echo "  Exa:         skipped  (set EXA_API_KEY)"
  echo
  echo "  To verify:   claude mcp list"
else
  echo "  MCP:         manual config required (see README)"
fi
echo "  To remove:   ./install.sh --uninstall"
echo
