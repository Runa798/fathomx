# Research Execution Strategy

Detailed three-tier strategy for the deep-research skill. Read this file before executing any research task.

---

## Tier 1: Quick Research (单一事实查询)

**Trigger**: Simple factual question, definition, or single data point that can be answered from one authoritative source.

**Execution**:
1. Run one `mcp__grok-search__web_search` call with the user's query.
2. If the result is empty or irrelevant, rephrase once and retry.
3. No need to use Exa or browser for Quick tier.

**Report**: Use `templates/quick-report.md`

**Expected time**: ~30 seconds

---

## Tier 2: Standard Research (对比/选型/评估)

**Trigger**: Comparison between products/technologies, vendor evaluation, multi-source synthesis needed.

**Execution**:

1. **Planning** — Decompose the query using the Grok planning pipeline:
   - `plan_intent(query)` → `plan_complexity(...)` → `plan_sub_query(...)` → `plan_search_term(...)` → `plan_tool_mapping(...)` → `plan_execution(...)`
   - This produces a structured list of sub-queries and tool assignments.

2. **Grok searches** — For each sub-query from the plan:
   - Call `mcp__grok-search__web_search` with `extra_sources=5`
   - Collect all `session_id` values for source retrieval later

3. **Exa searches** (parallel with Grok):
   - Use `mcp__exa__web_search_exa` or `mcp__exa__web_search_advanced_exa` for semantic discovery
   - For product/company comparisons, run `mcp__exa__company_research_exa` for each subject

4. **Source collection**:
   - Call `mcp__grok-search__get_sources(session_id)` for each Grok session
   - Aggregate all source URLs from both Grok and Exa

5. **Deduplication**:
   - Remove duplicate URLs across Grok and Exa source lists
   - Merge overlapping content from the same source

6. **Verification** (for key claims only):
   - Use `mcp__grok-search__web_fetch(url)` to get full page content for the most critical claims
   - No need to fetch every source — spot-check the most consequential ones

**Report**: Use `templates/standard-report.md`

**Expected time**: 2–5 minutes

---

## Tier 3: Deep Research (产业分析/竞品图谱/市场格局)

**Trigger**: Industry-wide analysis, comprehensive competitive landscape, market sizing study, or any research requiring 10+ distinct sources.

**Execution**:

### Phase 1 — Planning
Use the full Grok planning pipeline: `plan_intent` → `plan_complexity` → `plan_sub_query` → `plan_search_term` → `plan_tool_mapping` → `plan_execution`. This produces a multi-wave execution plan.

### Phase 2 — Wave 1: Broad Sweep
Run all of the following in parallel where possible:

- **Grok broad searches**: `mcp__grok-search__web_search` with `extra_sources=20` across multiple angles (e.g., "market overview", "key players", "recent trends", "competitive dynamics")
- **Exa semantic search**: `mcp__exa__web_search_exa` for entity and concept discovery
- **Exa company research**: `mcp__exa__company_research_exa` for each major player identified
- **Exa similar entities**: Use `mcp__exa__web_search_advanced_exa` with `find_similar` style queries to discover unknown competitors or alternatives

### Phase 3 — Wave 2: Deep Dive
Based on Wave 1 discoveries:

- **Grok secondary searches**: Validate entities and claims discovered by Exa in Wave 1
- **Full-page extraction**: `mcp__grok-search__web_fetch(url)` for the 5–10 most important pages
- **Site mapping**: `mcp__grok-search__web_map(url)` for structured documentation sites or company blogs when systematic coverage is needed
- **Async deep research**: For known domains with rich content, use `mcp__exa__deep_researcher_start(...)` and poll with `mcp__exa__deep_researcher_check(...)`

### Phase 4 — Wave 3: Gap Filling (conditional)
Only if Wave 1 + 2 leave unresolved gaps:

- Check if missing content is behind a login wall or requires JavaScript rendering
- If yes: escalate to browser layer (read `references/browser-layer.md`)
- Use **agent-browser** for known page structures (targeted extraction)
- Use **browser-use** for exploratory multi-step navigation

### Phase 5 — Synthesis
1. Aggregate all sources: Grok sessions (`get_sources`), Exa results, browser extractions
2. Deduplicate by URL and content similarity
3. Resolve conflicts: where sources disagree, note the conflict and present all versions
4. Structure findings by topic dimension (not by tool used)
5. Assign confidence indicators per finding (see `references/report-format.md`)

**Report**: Use `templates/deep-report.md`

**Expected time**: 5–15 minutes

---

## Escalation Rules

| Situation | Action |
|-----------|--------|
| Grok returns empty or irrelevant result | Rephrase query once and retry; if still fails, route same query to Exa |
| Exa also returns poor results | Escalate to browser layer |
| Browser layer hits Cloudflare Turnstile or CAPTCHA | Stop automation; inform user; provide the URL for manual access |
| All three layers fail for a specific URL | Skip that source; note it in the Methodology section of the report |
| Sources conflict on a key fact | Present all conflicting versions with full citations; do not silently resolve |
| Rate limit on Grok or Exa | Wait 5 seconds and retry once; if still blocked, switch to the other tool for the remaining queries |

## Parallel Execution Note

For Deep tier research, sub-tasks that do not depend on each other should be dispatched as parallel sub-agents:
- Sub-agent A: All Grok searches
- Sub-agent B: All Exa discovery searches
- Main agent: Planning, synthesis, report generation

This reduces total wall-clock time from 15+ minutes to 5–8 minutes for comprehensive studies.
