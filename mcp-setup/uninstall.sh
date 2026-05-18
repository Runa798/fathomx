#!/usr/bin/env bash
# mcp-setup/uninstall.sh — Remove all MCP registrations and skill symlink
#
# Usage:
#   ./mcp-setup/uninstall.sh

set -euo pipefail

SKILL_TARGET="${HOME}/.claude/skills/deep-research"

# ─── Colors ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'
ok()   { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
info() { echo -e "${CYAN}[INFO]${RESET}  $*"; }

echo -e "${BOLD}=== Uninstalling claude-deep-research ===${RESET}"
echo

# ─── Remove GrokSearch MCP ───────────────────────────────────────────────────
info "Removing GrokSearch MCP registration..."
if claude mcp remove grok-search 2>/dev/null; then
  ok "grok-search removed"
else
  warn "grok-search was not registered (skipping)"
fi

# ─── Remove Exa MCP ──────────────────────────────────────────────────────────
info "Removing Exa MCP registration..."
if claude mcp remove exa 2>/dev/null; then
  ok "exa removed"
else
  warn "exa was not registered (skipping)"
fi

# ─── Remove skill symlink/directory ──────────────────────────────────────────
info "Removing skill at ${SKILL_TARGET}..."
if [[ -L "${SKILL_TARGET}" ]]; then
  rm -f "${SKILL_TARGET}"
  ok "Symlink removed: ${SKILL_TARGET}"
elif [[ -d "${SKILL_TARGET}" ]]; then
  rm -rf "${SKILL_TARGET}"
  ok "Directory removed: ${SKILL_TARGET}"
else
  warn "Nothing found at ${SKILL_TARGET} (skipping)"
fi

# ─── Done ────────────────────────────────────────────────────────────────────
echo
ok "Uninstall complete."
echo
echo "  MCP registrations cleared (verify with: claude mcp list)"
echo "  Skill directory removed:  ${SKILL_TARGET}"
echo
echo "  Note: .env and shared-keys/ were NOT removed."
echo "  To fully clean up: rm -rf /path/to/claude-deep-research"
