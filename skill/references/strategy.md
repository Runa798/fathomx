# Research Execution Strategy

Detailed strategy for the deep-research skill. Read this file before executing any research task.

This is the v1.2.0 strategy with multi-model orchestration support. When orchestrator is unavailable, each phase falls back to Claude-only execution (v1.1.0 compatible).

---

## Pre-Execution: Configuration Check

Before any research, run:

```bash
python3 -m deep_research config check
```

Parse the JSON output. Key fields:
- `multi_model: true` → orchestrator available, use multi-model flow
- `multi_model: false` → Claude-only mode (still use new methodology)
- `available_tiers` → which model tiers can be delegated
- `gemini_search: true` → Gemini Search available as supplementary source

If the command fails (exit code non-zero or not found), proceed in Claude-only mode.

---

## Tier 1: Quick Research (单一事实查询)

**Trigger**: Simple factual question, definition, or single data point.

**Execution**:
1. Run one `mcp__grok-search__web_search` call with the user's query.
2. If empty or irrelevant, rephrase once and retry.
3. No orchestrator, no scope expansion, no personas.

**Report**: Use `templates/quick-report.md`

**Expected time**: ~30 seconds

---

## Tier 2: Standard Research (对比/选型/评估)

**Trigger**: Comparison, evaluation, multi-source synthesis needed.

### Phase 1 — Scope Expansion + Planning

Read `references/methodology.md` §1 and apply MECE scope expansion:
1. Infer the decision intent from the user's question
2. Generate sub-questions for at least 4 of the 6 MECE dimensions
3. Apply the three research personas mentally (no orchestrator calls for Standard)
4. Create a brief research plan (can be in-conversation, no need for workspace file)

### Phase 2 — Multi-Tool Search

Use the Grok planning pipeline for query decomposition:
`plan_intent` → `plan_complexity` → `plan_sub_query` → `plan_search_term` → `plan_tool_mapping` → `plan_execution`

Execute searches in parallel:
- **Grok**: `web_search` with `extra_sources=5` per sub-query
- **Exa**: `web_search_exa` or `web_search_advanced_exa` for semantic discovery
- **Exa company**: `company_research_exa` for each identified competitor (DO NOT skip this for competitive research)
- **(If gemini_search available)**: `python3 -m deep_research run gemini_search --workspace {session-dir-or-temp} --query "..." --output "search/gemini-{topic}.md"`

Collect all `session_id` values for source retrieval.

### Phase 3 — Optional Extraction (if FAST tier available)

If `multi_model: true` and FAST tier is available:
1. Write raw search results to `workspace/search/raw-{dimension}.md`
2. Call orchestrator: `python3 -m deep_research run search_extract --dimension {dim} ...`
3. Read extracted results from `workspace/search/{dim}.md`

If FAST tier unavailable: Claude synthesizes directly from raw search results.

### Phase 4 — Synthesis

Apply all three persona lenses (§2 of methodology.md) during synthesis:
- Market Analyst perspective on market/trend dimensions
- CI Analyst perspective on competitive dimensions
- Product Strategist perspective on user/strategic dimensions

Perform one gap check (§3 of methodology.md). If gaps found, run targeted supplementary searches (max 1 iteration).

**Report**: Use `templates/standard-report.md`

**Expected time**: 2-5 minutes

---

## Tier 3: Deep Research (产业分析/竞品图谱/市场格局)

**Trigger**: Industry analysis, competitive landscape, market sizing, or any research requiring 10+ distinct sources.

**Disk Persistence**: Deep research MUST write intermediate results to disk.

**Session directory**: `workspace/research-{YYYY-MM-DD}-{topic-slug}/`

Topic slug sanitization rules: lowercase ASCII, replace non-ASCII with `-`, remove shell metacharacters, collapse repeated `-`, cap at 60 chars.

### Phase 1 — Scope Expansion + Planning (Claude, STRATEGIC)

Read `references/methodology.md` §1 and apply FULL MECE scope expansion:

1. Infer decision intent
2. Generate sub-questions for ALL 6 dimensions:
   - Market Context
   - Competitive Landscape
   - User Jobs & Needs
   - Product Capabilities
   - Strategic Position
   - Future Trajectory
3. Apply STORM-style perspective discovery: generate 3 expert viewpoints via the research personas
4. Create tool-to-dimension mapping (§4 of methodology.md)

**Checkpoint**: Write `{session-dir}/plan.md` with the expanded scope and dimension assignments.

Write `{session-dir}/state.json`:
```json
{
  "topic": "research topic",
  "tier": "deep",
  "status": "in_progress",
  "currentPhase": 1,
  "startedAt": "ISO datetime",
  "updatedAt": "ISO datetime",
  "sourceCount": 0,
  "dimensions": {
    "market-context": "pending",
    "competitive-landscape": "pending",
    "user-jobs": "pending",
    "product-capabilities": "pending",
    "strategic-position": "pending",
    "future-trajectory": "pending"
  },
  "personas": {},
  "checkpoints": ["plan.md"]
}
```

### Phase 2 — Multi-Dimensional Search + Extract

Run ALL of the following in parallel where possible:

**MCP searches (Claude directly)**:
- **Grok broad**: `web_search` with `extra_sources=20` per dimension
- **Exa semantic**: `web_search_exa` for entity/concept discovery
- **Exa company**: `company_research_exa` for EACH major player — this is MANDATORY for competitive research
- **Exa similar**: `web_search_advanced_exa` with find_similar queries
- **Academic** (if scientific topic): Semantic Scholar via `web_fetch` (see `references/academic-search.md`)

Write raw results to `{session-dir}/search/raw-{dimension}.md` for each dimension.

**Orchestrator extraction (if FAST tier available)**:
For each dimension with raw data:
```bash
python3 -m deep_research run search_extract \
  --workspace {session-dir} \
  --dimension {dimension-name} \
  --context "{brief topic context}"
```

This calls the FAST model (DeepSeek) to extract structured data. Output: `{session-dir}/search/{dimension}.md`.

If FAST tier unavailable: Claude extracts directly (higher cost, same quality).

**Gemini supplementary search (if SEARCH tier available)**:
```bash
python3 -m deep_research run gemini_search \
  --workspace {session-dir} \
  --query "{dimension-specific query}" \
  --output "search/gemini-{dimension}.md"
```

**Checkpoint**: Update dimensions in state.json to "searched". Add checkpoint files.

### Phase 3 — Persona Analysis + Gap Detection

**Orchestrator persona analysis (if SMART tier available)**:
```bash
python3 -m deep_research run analyze --persona market-analyst --workspace {session-dir} --context "..."
python3 -m deep_research run analyze --persona ci-analyst --workspace {session-dir} --context "..."
python3 -m deep_research run analyze --persona product-strategist --workspace {session-dir} --context "..."
```

This calls the SMART model (GPT) with embedded analytical frameworks. Output: `{session-dir}/analysis/{persona}.md`.

If SMART tier unavailable: Claude applies persona lenses directly during synthesis.

**Gap Detection (Claude directly)**:
Read all search and analysis files. Apply gap checklist from methodology.md §3:
- Source count per dimension (≥3 independent sources?)
- Source diversity (≥2 source types?)
- Contradiction resolution (all conflicts noted?)
- Factual grounding (numerical evidence for key claims?)
- Recency (data within 12 months?)

If gaps found:
1. Construct targeted supplementary searches
2. Execute via MCP tools
3. Write to `{session-dir}/search/gap-{dimension}.md`
4. Re-run extraction if orchestrator available

Maximum 2 gap-fill iterations.

**Checkpoint**: Update state.json currentPhase, add checkpoint files.

### Phase 4 — Compression + Synthesis

**Compression (if orchestrator available)**:
```bash
python3 -m deep_research run compress --workspace {session-dir} --context "..."
```

Output: `{session-dir}/compressed/findings-summary.md` — all findings compressed to ~55% token retention, preserving reasoning chains and contradictions.

If orchestrator unavailable: Claude reads all files directly for synthesis.

**Synthesis (Claude, STRATEGIC tier with max thinking)**:

Read `{session-dir}/compressed/findings-summary.md` (or all raw files if no compression).
Read all `{session-dir}/analysis/*.md` files.

Apply multi-framework analysis:
1. SWOT with evidence citations and "so what" implications
2. ERRC Grid (Eliminate, Reduce, Raise, Create)
3. JTBD opportunity scores where applicable
4. Porter's Five Forces for competitive dimensions

Generate the final report following `templates/deep-report.md`:
- Organized by the 6 MECE dimensions, NOT by tool or search round
- Every claim cited with source [n]
- Every source rated A-E for credibility
- Confidence indicators (🟢🟡🔴) on key findings
- Recommendations trace back to evidence
- Explicit gaps and limitations in Methodology section

**Write**: `{session-dir}/report.md` and present to user.

Update state.json: `status: "completed"`, `currentPhase: 4`.

**Expected time**: 5-15 minutes

### Resuming an Interrupted Session

If `{session-dir}/state.json` exists with `status: "in_progress"`:
1. Read state.json to determine currentPhase
2. Read all existing checkpoint files
3. Resume from the next incomplete phase — do NOT re-execute completed phases
4. Check dimension status in state.json to know which dimensions need work

---

## Escalation Rules

| Situation | Action |
|-----------|--------|
| Grok returns empty | Rephrase once and retry; if still fails, route to Exa |
| Exa also poor results | Escalate to browser layer (read `references/browser-layer.md`) |
| Browser hits CAPTCHA | Stop automation; inform user; provide URL for manual access |
| All layers fail for a URL | Skip that source; note in Methodology section |
| Sources conflict | Present all versions with full citations; do not silently resolve |
| Rate limit on Grok/Exa | Wait 5s and retry once; if blocked, switch to the other tool |
| Orchestrator task fails | Claude does that step itself; announce degraded mode to user |
| Orchestrator not installed | Full v1.1.0 compatible mode with methodology enhancements |

## Parallel Execution Note

For Deep tier, maximize parallelism:
- MCP searches across dimensions: parallel sub-agents or parallel tool calls
- Orchestrator extract tasks: can be called sequentially (each is fast, ~10-30s)
- Persona analyses: call all three in rapid succession (each takes 30-60s)
- Gap-fill searches: parallel where possible
