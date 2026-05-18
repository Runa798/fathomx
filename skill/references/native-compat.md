# CC Native Search Compatibility

Strategy for managing Claude Code's built-in WebSearch/WebFetch tools alongside the enhanced MCP tools.

---

## Default State: Native Search DISABLED

When a research task begins, the first action is to call:

```
mcp__grok-search__toggle_builtin_tools with action: "on"
```

This disables CC's native WebSearch and WebFetch tools. All search traffic then routes through:
- **Grok Search MCP** — AI-synthesized results + Tavily key pool (149 keys)
- **Exa MCP** — Semantic discovery

This ensures consistent source tracking, better deduplication, and higher-quality results from the managed search infrastructure.

---

## When to RE-ENABLE Native Search

| Scenario | Action | Reason |
|----------|--------|--------|
| Anthropic/Claude-specific documentation | Enable native | CC's native search may have privileged access to Anthropic docs and the Claude.ai help center |
| All MCP APIs failing (rate limit, sustained outage) | Enable native as fallback | Degraded service beats no service |
| User explicitly requests native search | Enable native | User override always wins, no questions asked |
| Simple in-conversation fact check (non-research) | Keep disabled | Grok handles routine lookups fine |
| Grok and Exa both rate-limited simultaneously | Enable native temporarily | Route remaining queries through native until MCP recovers |

---

## How to Toggle

```
# Disable native search (default for all research tasks)
Call mcp__grok-search__toggle_builtin_tools with action: "on"

# Re-enable native search (for fallback or user override)
Call mcp__grok-search__toggle_builtin_tools with action: "off"

# Check current toggle state
Call mcp__grok-search__toggle_builtin_tools with action: "status"
```

Note: The `action: "on"` / `action: "off"` naming is inverted from what you might expect — "on" means "suppress native tools (turn on suppression)", "off" means "allow native tools (turn off suppression)". Always verify the state with `status` if uncertain.

---

## Conflict Resolution

If the same query returns different results from native search vs Grok/Exa:

1. **Check source dates** — Prefer the more recently published source.
2. **Check source authority** — Prefer primary sources (official docs, company announcements, peer-reviewed publications) over aggregators (news summaries, forums, blogs).
3. **If still ambiguous** — Present both versions with full source attribution. Let the user decide which to act on. Do not silently pick one.

Authority hierarchy (approximate):
1. Official documentation / primary source
2. Peer-reviewed research / official filings
3. Major news outlets with editorial standards
4. Industry analyst reports (Gartner, IDC, etc.)
5. Reputable tech publications (TechCrunch, Wired, etc.)
6. Community forums, blogs, aggregators

---

## Post-Research Cleanup

After the research task is complete:

1. Check if the user has an explicit preference for the native search state going forward.
2. If no preference stated: leave native search disabled. Grok Search MCP is generally superior for ongoing work due to the Tavily key pool and AI synthesis.
3. If the user is switching away from a research task to general coding/Q&A work: ask once whether they want native search re-enabled.

---

## Diagnostics

If toggle behavior seems unexpected, call `mcp__grok-search__get_config_info()` to inspect the current configuration state, active model, and key pool status.
