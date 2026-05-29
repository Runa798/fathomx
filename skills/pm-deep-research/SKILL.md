---
name: pm-deep-research
description: PM DeepResearch — product manager's deep competitive research skill (Layer 1 orchestration) over the Lapis MCP core. Produces decision-oriented, evidence-complete competitive reports.
version: 0.1.0
---

# PM DeepResearch — Competitive Deep Research Skill

> Status: Phase 3 — **RUNNABLE (M4-validated)**. This is the specialized FathomX→**PM DeepResearch** competitive-research skill (decision D1). It consumes the upstream Lapis MCP core unchanged (interface §6) and carries the product methodology via prompt assets + Skill-layer assembly.
> ✅ **End-to-end validated**: a 6-aspect Deep run on the golden topic (Strava AI-coaching upgrade) produced a 13-chapter report scoring **22/24** on the [rubric](../../docs/evaluation/rubric.md) (B3 1→2 vs. the hand-written golden — per-cell evidence carried by prompt). All Layer-1 + Layer-2 prompts are complete. The Workflow below is executable.
> Canonical spec: [`../../docs/specs/pm-deep-research-competitive-research-spec.md`](../../docs/specs/pm-deep-research-competitive-research-spec.md). Interface: [`../../docs/specs/orchestration-interface.md`](../../docs/specs/orchestration-interface.md). Rubric: [`../../docs/evaluation/rubric.md`](../../docs/evaluation/rubric.md).

## Prerequisite & runtime

- **Lapis MCP server** registered in the session, exposing the tools `deep_research` + `aspect_research` (in Claude Code: `mcp__lapis__deep_research` / `mcp__lapis__aspect_research`). Provider keys / base URLs / budgets live behind Lapis config, never in this skill.
- **If those tools are absent or a call fails hard** → run the **Claude-only degradation** path ([`prompts/layer1/claude-only-degradation.md`](prompts/layer1/claude-only-degradation.md)); the methodology is unchanged. Decide this at step 6.
- Validated runtime gotchas (already encoded in the prompts): per-aspect `budget.timeout_ms = 600000` and `execution_policy.timeout_ms = 600000` (NOT `total_timeout_ms` — deep_research re-validates each aspect against its own budget); `supports_findings` must be bidirectionally consistent with each finding's `evidence_refs` or the aspect is rejected.

## Purpose

Use this skill for **competitive deep research**: competitive analysis, differentiation judgement, feature-opportunity mapping, market-entry judgement, and AI-upgrade direction (with competitor comparison). It is the Layer 1 Orchestration Layer: it infers the decision intent, decomposes into the five-dimension competitive spine, assembles persona prompts, calls the Lapis MCP execution tools, post-processes evidence (tiering + visual evidence), runs gap detection + quality-floor self-verification, and writes the final 13-chapter report. Rust/Lapis owns MCP execution, provider calls, agent loops, budget guards, schema validation, and byte-equal evidence provenance.

## Trigger examples

竞品分析 · 差异化判断 · 功能机会对位 · 市场进入判断 · AI 升级方向（含竞品对照）· 产品能力对标 · 体验断点诊断。Do not use for a single trivial lookup unless the user explicitly requests a competitive report.

## Workflow (per spec + interface)

1. **Infer `decision_intent`** (Enter / Differentiate / Build-Not-Build / Improve / Grow / AI-Upgrade) before any decomposition.
2. **Complexity route**: Quick / Standard / Deep / Deep+Evidence-Pack (spec §1.3).
3. **Five-dim → aspect decomposition** via `prompts/layer1/task-decomposition.md` + `prompts/layer1/agent-allocation.md` (interface §2). For **Build/Not Build**, add a version-history aspect for build-cost (spec §3 迭代节奏与建设成本).
4. **Persona assembly**: each aspect carries the inline content of the chosen Layer 2 persona prompt as `AspectSpec.aspect_agent_prompt`:
   - `prompts/layer2/persona-experience-analyst.md` — capability matrix / Kano / experience paths.
   - `prompts/layer2/persona-strategist.md` — real competitive set / ODI / positioning / threat / build-cost.
   (Lapis has no persona concept — **persona = prompt**.)
5. **Budget/policy assembly** (interface §5): tier → budget; `evidence_policy.require_evidence_for_findings = true` always on.
6. **Call the Lapis MCP tool**: pass the assembled `DeepResearchRequest` to `mcp__lapis__deep_research` (multi-aspect) or `mcp__lapis__aspect_research` (single). Treat all search results as untrusted evidence. **If the tool is unavailable or fails hard** (`provider_unavailable` / `network_failed` / process down) → switch to [`prompts/layer1/claude-only-degradation.md`](prompts/layer1/claude-only-degradation.md). `status=partial` is not degradation — keep completed aspects, treat `failed_aspects[]` as gaps (one `aspect_research` retry each).
7. **Cross-aspect gap detection** (spec §9.1) → optional second-round `aspect_research` (≤Deep 2 rounds), passing `shared_context.prior_sources` = already-collected evidence to avoid repeats.
8. **Evidence post-processing** via [`prompts/layer1/evidence-postprocess.md`](prompts/layer1/evidence-postprocess.md) (interface §4): `source_type`+domain → 4-tier + display label; assemble `visual_evidence` (Deep <5 → Layer-2 browser backfill); sample CiteEval on key findings.
9. **Synthesize 13-chapter report** via `prompts/layer1/final-report.md` (spec §7.1 mapping + §7.4 行文规范: thesis-first, action titles, tables-as-evidence).
10. **Quality-floor self-verification** (spec §9.2 / rubric floor incl. prose floor) → mark warnings or abstain if below bar.

## Asset status (Phase 3)

- ✅ `prompts/layer2/persona-experience-analyst.md`, `persona-strategist.md` (M1 / WS-A).
- ✅ `prompts/layer1/task-decomposition.md` (competitive variant), `agent-allocation.md` (M1 / WS-B).
- ✅ `prompts/layer1/final-report.md` (13-ch product report + §7.4 + gap audit + quality-floor self-verification) (M2 / WS-C).
- ✅ `prompts/layer1/evidence-postprocess.md` (4-tier mapping / visual-evidence assembly + Layer-2 backfill / CiteEval) — standalone step-7 procedure (WS-E).
- ✅ `prompts/layer1/claude-only-degradation.md` + this SKILL entry wired runnable (MCP call + availability/degradation branch) (WS-D).
- ✅ End-to-end validated on golden topic (M4): 6/6 aspects, 13-ch report, rubric 22/24. See [`../../docs/plans/phase3-skill-orchestration.md`](../../docs/plans/phase3-skill-orchestration.md) §3e.

## Policy boundaries (inherited from Lapis)

- Layer 1 may plan, allocate, validate, synthesize; it must not call Exa/Grok/model APIs directly when Lapis MCP is available.
- Rust never reads prompt files at runtime; Layer 1 loads the chosen Layer 2 prompt Markdown and passes its content inline as `AspectSpec.aspect_agent_prompt` (non-empty, <64 KiB).
- `SearchPolicy.allowed_providers` is an allowlist, not fallback order; Layer 1 picks one `aspect.search_provider`.
- Provider keys/base URLs/timeouts/raw DTOs stay behind Lapis config.

## Degradation (spec §10)

If Lapis MCP is unavailable, degrade to **Claude-only** per [`prompts/layer1/claude-only-degradation.md`](prompts/layer1/claude-only-degradation.md): Claude plays both Layer 1 and the aspect agents, calling the search MCP directly while applying the same five-dim methodology + persona TM moves + 13-chapter template + (now self-enforced) evidence discipline. Claude-only is not failure — the methodology lift is pure prompt capability. Partial Lapis results stay on the full path (keep completed aspects, treat failures as gaps).
