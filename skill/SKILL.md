---
name: deep-research
description: Deep research orchestrator for Claude Code. Routes queries through Grok Search MCP, Exa MCP, and browser automation based on complexity. Produces formatted research reports with source attribution.
version: 1.1.0
author: Runa798
license: MIT
metadata:
  tags: [research, search, mcp, orchestration]
  related_skills: []
---

# Deep Research Skill

## Trigger Keywords

Activate this skill when the user's request contains any of:

- **Chinese**: 调研, 深度搜索, 对比分析, 产业分析, 竞品, 市场调研, 技术选型
- **English**: research, deep search, compare, analyze, investigate, market research, tech evaluation

## Core Workflow

### Step 1: Complexity Assessment

Classify the research request before doing anything else:

| Tier | Trigger | Primary Tools |
|------|---------|---------------|
| **Quick** | Single fact, definition, simple lookup | Grok single query |
| **Standard** | Comparison, evaluation, multi-faceted question | Grok + Exa in parallel |
| **Deep** | Industry analysis, competitive landscape, comprehensive study | Multi-round Grok + Exa + browser fallback |

### Step 2: Native Search Management (FIRST action before any research)

Call `mcp__grok-search__toggle_builtin_tools` with `action: "on"` to disable CC's built-in WebSearch/WebFetch. This forces all search traffic through the enhanced MCP tools with better source tracking and the Tavily key pool.

Read `references/native-compat.md` for exceptions and fallback rules.

### Step 3: Execute Strategy

Based on the complexity tier determined in Step 1:

- Read `references/strategy.md` for detailed execution steps per tier
- Use the appropriate report template from `templates/`

### Step 4: Generate Report

Format output per `references/report-format.md`:

- Always include source URLs with access dates
- Cross-reference and deduplicate across Grok and Exa results
- Flag conflicting information explicitly with confidence indicators

### Step 5: Restore Search State

After research completes, optionally restore CC native search if the user prefers: call `toggle_builtin_tools` with `action: "off"`.

---

## MCP Tool Reference

### Grok Search MCP (`mcp__grok-search__*`)

| Tool | Signature | Description |
|------|-----------|-------------|
| `web_search` | `(query, platform?, model?, extra_sources?)` | AI-synthesized search via Grok + Tavily sources. Returns `session_id` + content. |
| `get_sources` | `(session_id)` | Retrieve cached source URLs from a prior `web_search` call. |
| `web_fetch` | `(url)` | Extract webpage content as Markdown (Tavily → Firecrawl fallback). |
| `web_map` | `(url, instructions?, max_depth?, max_breadth?, limit?)` | Map site structure for systematic crawling. |
| `plan_intent` | `(query)` | Step 1 of planning pipeline — parse research intent. |
| `plan_complexity` | `(...)` | Step 2 — assess complexity and suggest tier. |
| `plan_sub_query` | `(...)` | Step 3 — decompose into sub-queries. |
| `plan_search_term` | `(...)` | Step 4 — generate concrete search strings. |
| `plan_tool_mapping` | `(...)` | Step 5 — map search terms to tools. |
| `plan_execution` | `(...)` | Step 6 — produce final execution plan. |
| `get_config_info` | `()` | Diagnostics: show current config and key pool status. |
| `switch_model` | `(model)` | Change the Grok model used for search synthesis. |
| `toggle_builtin_tools` | `(action)` | Enable (`"off"`) or disable (`"on"`) CC native WebSearch/WebFetch. |

### Exa MCP (`mcp__exa__*`)

| Tool | Signature | Description |
|------|-----------|-------------|
| `web_search_exa` | `(query, numResults?, ...)` | Semantic web search. Best for entity/concept discovery. |
| `web_search_advanced_exa` | `(query, category?, ...)` | Advanced search with category and date filters. |
| `company_research_exa` | `(companyName)` | Company discovery and background research. |
| `crawling_exa` | `(url, ...)` | Extract full content from a specific URL. |
| `people_search_exa` | `(query)` | Find information about specific people. |
| `get_code_context_exa` | `(query)` | Code-specific semantic search (GitHub, Stack Overflow, etc.). |
| `deep_researcher_start` | `(...)` | Start an async deep research job. |
| `deep_researcher_check` | `(...)` | Poll status of a running deep research job. |

### Academic Search — Semantic Scholar (optional)

For scientific/technical research topics, use the Semantic Scholar API via `web_fetch`. No API key required.

Read `references/academic-search.md` for endpoint details, credibility mapping, and usage guidelines.

| Action | Method |
|--------|--------|
| Search papers | `web_fetch("https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=10&fields=title,url,year,authors,abstract,citationCount,venue,openAccessPdf")` |
| Parse results | JSON response → filter by year, sort by citationCount |

### Browser Tools — Layer 2

Use only when API layers (Grok + Exa) cannot access the content. Read `references/browser-layer.md` before using.

- **agent-browser** CLI: `agent-browser --cdp 9222 open/snapshot/click/get`
  - Best for precise step-by-step automation on known page structures
- **browser-use** CLI: `browser-use connect` or `browser-use open <url>`
  - Best for autonomous multi-step exploration on unknown page structures

---

## Important Rules

1. **Always read `references/strategy.md`** before executing research — it contains the detailed step-by-step for each tier.
2. **Never skip source attribution** — every factual claim in the output must link to a numbered source.
3. **Parallel sub-agents for deep research** — when doing Deep tier work, spawn parallel sub-agents where possible: one for Grok queries, one for Exa discovery.
4. **Tool defaults**:
   - Grok → structured/factual queries, AI-synthesized summaries
   - Exa → entity discovery, semantic search, competitive landscape
5. **Escalation order**: Grok → Exa → browser layer → flag to user
6. **Report language**: Output research reports in the user's language (default Chinese unless context requires English).
7. **Conflict handling**: If Grok and Exa return conflicting information on a key fact, present all versions with their sources — do not silently pick one.
