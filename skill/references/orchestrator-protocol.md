# Orchestrator Protocol — How Claude Interacts with the Multi-Model Orchestrator

This file defines the exact protocol for Claude (the running model in Claude Code CLI) to invoke the Python orchestrator for multi-model research tasks.

---

## Prerequisites Check

Before any orchestrator call, verify availability:

```bash
python3 -m deep_research config check
```

This returns JSON:
```json
{
  "ok": true,
  "config_path": "/home/user/.deep-research/config.json",
  "config_exists": true,
  "available_tiers": ["FAST", "SMART", "SEARCH"],
  "multi_model": true,
  "scope_expansion": true,
  "gemini_search": true
}
```

- If `ok: false` → skip all orchestrator calls, use v1.1.0 mode
- If `multi_model: false` → skip model calls, but still use scope expansion
- Check `available_tiers` to know which tasks can be delegated

---

## Command Reference

All commands follow the pattern:
```bash
python3 -m deep_research run <task> --workspace <path> [--args]
```

### search_extract — Extract structured data (FAST tier)

```bash
python3 -m deep_research run search_extract \
  --workspace workspace/research-2026-05-20-topic-slug \
  --dimension "competitive-landscape" \
  --context "Research on X product market" \
  --input "search/raw-competitive-landscape.md"  # optional, defaults to search/raw-{dimension}.md
```

**Prerequisite**: Claude must first write raw search results to `workspace/search/raw-{dimension}.md` using MCP tools (Grok, Exa).

**Output**: `workspace/search/{dimension}.md` — Structured extracted data with source citations.

**When to use**: After MCP search results are collected and need extraction/structuring. The FAST model (DeepSeek) does this 37x cheaper than Opus.

### analyze — Run persona analysis (SMART tier)

```bash
python3 -m deep_research run analyze \
  --workspace workspace/research-2026-05-20-topic-slug \
  --persona market-analyst \
  --context "Research on X product market"
```

**Prerequisite**: Extracted search files must exist in `workspace/search/` (non-raw files).

**Output**: `workspace/analysis/{persona-name}.md`

**Valid personas**: `market-analyst`, `ci-analyst`, `product-strategist`

**When to use**: After extraction, to apply analytical frameworks via the SMART model (GPT-5.5). Each persona produces a different analytical lens.

### compress — Compress findings (FAST tier)

```bash
python3 -m deep_research run compress \
  --workspace workspace/research-2026-05-20-topic-slug \
  --context "Research on X product market"
```

**Prerequisite**: Both search and analysis files must exist.

**Output**: `workspace/compressed/findings-summary.md`

**When to use**: Before final synthesis. Compresses all findings into a synthesis-ready summary at ~55% token retention. This is the primary artifact Claude reads for report generation.

### gemini_search — Grounded search (SEARCH tier)

```bash
python3 -m deep_research run gemini_search \
  --workspace workspace/research-2026-05-20-topic-slug \
  --query "2026 AI fitness market trends China" \
  --output "search/gemini-market-trends.md"
```

**Output**: Specified file with Gemini's grounded search results including Google Search citations.

**When to use**: As a supplementary search source alongside Grok+Exa. Especially useful for recent events and Google-indexed content.

---

## Workspace File Protocol

All orchestrator I/O goes through workspace files. Claude writes inputs, orchestrator processes them, Claude reads outputs.

```
workspace/research-{date}-{slug}/
├── plan.md                    # Claude writes: research plan with expanded scope
├── state.json                 # Orchestrator updates: phase tracking
├── search/
│   ├── raw-{dimension}.md     # Claude writes: raw MCP search results
│   ├── {dimension}.md         # Orchestrator writes: extracted structured data
│   └── gemini-{topic}.md      # Orchestrator writes: Gemini search results
├── analysis/
│   ├── market-analyst.md      # Orchestrator writes: Market Analyst analysis
│   ├── ci-analyst.md          # Orchestrator writes: CI Analyst analysis
│   └── product-strategist.md  # Orchestrator writes: Product Strategist analysis
├── compressed/
│   └── findings-summary.md    # Orchestrator writes: compressed synthesis input
├── errors.log                 # Orchestrator appends: any errors encountered
└── report.md                  # Claude writes: final research report
```

---

## Error Handling

After each orchestrator call, check exit code and errors:

1. **Exit code 0**: Success. Read the output file.
2. **Exit code non-zero**: Check `workspace/errors.log` for details.
3. **Fallback rule**: If an orchestrator task fails, Claude performs that step itself using MCP tools. Announce to user: "External model unavailable for {task}, proceeding with direct analysis."

Never let an orchestrator failure block the research. Always fall back gracefully.

---

## Typical Deep Research Orchestration

```
1. python3 -m deep_research config check
   → Determine available tiers

2. Claude: Apply scope expansion (methodology.md)
   → Write workspace/plan.md

3. Claude: Run MCP searches per dimension (parallel)
   → Write workspace/search/raw-{dim}.md for each dimension

4. For each dimension with raw data:
   python3 -m deep_research run search_extract --dimension {dim} ...
   → workspace/search/{dim}.md

5. (If SEARCH tier available):
   python3 -m deep_research run gemini_search --query "..." --output "search/gemini-{topic}.md"

6. For each persona:
   python3 -m deep_research run analyze --persona {name} ...
   → workspace/analysis/{name}.md

7. Claude: Read all files, apply gap detection (methodology.md §3)
   → If gaps: targeted supplementary searches → re-extract

8. python3 -m deep_research run compress ...
   → workspace/compressed/findings-summary.md

9. Claude: Read findings-summary.md + all analysis files
   → Synthesize final report with multi-framework analysis
   → Write workspace/report.md
   → Present to user
```
