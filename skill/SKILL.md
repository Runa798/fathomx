---
name: deep-research
description: Multi-model deep research orchestrator for Claude Code. Routes queries through Grok Search MCP, Exa MCP, Gemini Search, and external analysis models. Applies product research methodology (MECE scope expansion, research personas, gap-driven iteration) to produce structured reports with source attribution.
version: 1.2.0
author: Runa798
license: MIT
metadata:
  tags: [research, search, mcp, orchestration, multi-model]
  related_skills: []
---

# Deep Research Skill

## Trigger Keywords

Activate this skill when the user's request contains any of:

- **Chinese**: 调研, 深度搜索, 对比分析, 产业分析, 竞品, 市场调研, 技术选型, 竞品分析
- **English**: research, deep search, compare, analyze, investigate, market research, tech evaluation, competitive analysis

## Core Workflow

### Step 1: Complexity Assessment

Classify the research request before doing anything else:

| Tier | Trigger | Primary Tools | Methodology |
|------|---------|---------------|-------------|
| **Quick** | Single fact, definition, simple lookup | Grok single query | Direct answer |
| **Standard** | Comparison, evaluation, multi-faceted question | Grok + Exa parallel, optional orchestrator | MECE 4-dimension + personas |
| **Deep** | Industry analysis, competitive landscape, comprehensive study | Full multi-model orchestration | MECE 6-dimension + personas + gap iteration |

### Step 2: Configuration Check

Check orchestrator availability:

```bash
python3 -m deep_research config check
```

Parse the JSON output to determine:
- Whether multi-model orchestration is available (`multi_model`)
- Which model tiers can be delegated (`available_tiers`)
- Whether Gemini Search is available (`gemini_search`)
- Whether scope expansion is enabled (`scope_expansion`)

If the command fails or returns `ok: false`, proceed in Claude-only mode — all methodology enhancements still apply, only model delegation is disabled.

### Step 3: Native Search Management

Call `mcp__grok-search__toggle_builtin_tools` with `action: "on"` to disable CC's built-in WebSearch/WebFetch. Read `references/native-compat.md` for exceptions.

### Step 4: Scope Expansion (Standard + Deep only)

Read `references/methodology.md` and apply the MECE scope expansion:
1. Infer the user's **decision intent** (what decision will they make?)
2. Expand into research dimensions (4 for Standard, 6 for Deep)
3. Generate expert viewpoints via the three research personas
4. Assign tools to each dimension

### Step 5: Execute Strategy

Read `references/strategy.md` for detailed execution per tier. Key integration points:

**For orchestrator-enhanced research** (read `references/orchestrator-protocol.md`):
- Raw MCP search results → write to workspace → orchestrator extracts (FAST tier)
- Extracted findings → orchestrator persona analysis (SMART tier)
- All findings → orchestrator compression → Claude final synthesis
- Supplementary search via Gemini (SEARCH tier)

**For Claude-only research**:
- All search via MCP tools (Grok + Exa)
- All extraction, analysis, and synthesis by Claude
- Still apply scope expansion, personas, and gap detection from methodology.md

### Step 6: Generate Report

Format output per `references/report-format.md`:
- Use the appropriate template from `templates/`
- Organize by research dimension, NOT by tool/source
- Every claim cited with source [n] and credibility rating A-E
- Confidence indicators (🟢🟡🔴) on key findings
- Recommendations trace back to evidence

### Step 7: Restore Search State

After research completes, optionally restore CC native search: call `toggle_builtin_tools` with `action: "off"`.

---

## MCP Tool Reference

### Grok Search MCP (`mcp__grok-search__*`)

| Tool | Use For |
|------|---------|
| `web_search` | AI-synthesized search. Use `extra_sources` for more depth. Returns `session_id`. |
| `get_sources` | Retrieve cached source URLs from a prior `web_search` call. |
| `web_fetch` | Extract webpage content as Markdown (Tavily → Firecrawl fallback). |
| `web_map` | Map site structure for systematic crawling. |
| `plan_intent` → `plan_execution` | 6-step planning pipeline for query decomposition. |
| `get_config_info` | Diagnostics: config and key pool status. |
| `switch_model` | Change the Grok model. |
| `toggle_builtin_tools` | Enable/disable CC native WebSearch/WebFetch. |

### Exa MCP (`mcp__exa__*`)

| Tool | Use For |
|------|---------|
| `web_search_exa` | Semantic web search. Best for entity/concept discovery. |
| `web_search_advanced_exa` | Advanced search with category and date filters. |
| `company_research_exa` | **MANDATORY** for competitive research. Company discovery and background. |
| `crawling_exa` | Extract full content from a URL. |
| `people_search_exa` | Find information about specific people. |
| `get_code_context_exa` | Code-specific semantic search. |
| `deep_researcher_start/check` | Async deep research jobs. |

### Orchestrator Tasks (via Bash)

Read `references/orchestrator-protocol.md` for full details.

| Task | Tier | Command |
|------|------|---------|
| Extract structured data | FAST | `python3 -m deep_research run search_extract --workspace ... --dimension ...` |
| Persona analysis | SMART | `python3 -m deep_research run analyze --workspace ... --persona ...` |
| Compress findings | FAST | `python3 -m deep_research run compress --workspace ...` |
| Gemini Search | SEARCH | `python3 -m deep_research run gemini_search --workspace ... --query ...` |

### Academic Search — Semantic Scholar

For scientific/technical topics. Read `references/academic-search.md` for details.

### Browser Tools — Layer 2

Use only when API layers fail. Read `references/browser-layer.md` before using.

---

## Important Rules

1. **Always read `references/methodology.md`** for Standard/Deep research — scope expansion is mandatory.
2. **Always read `references/strategy.md`** before executing — it contains the step-by-step per tier.
3. **Never skip source attribution** — every factual claim needs a `[n]` citation.
4. **Use `company_research_exa` for competitive research** — this is the #1 tool-routing improvement.
5. **For Deep research, use `references/orchestrator-protocol.md`** to invoke multi-model tasks.
6. **Organize reports by dimension, not by tool** — the user cares about the topic structure, not our search pipeline.
7. **Graceful degradation** — if orchestrator is unavailable, still apply methodology. If a tier fails, Claude does it.
8. **Escalation order**: Grok → Exa → Gemini → Browser → flag to user.
9. **Report language**: Output in the user's language (default Chinese unless context requires English).
10. **Conflict handling**: Present all versions with sources — do not silently pick one.
