---
name: pm-deep-research
description: PM DeepResearch — product manager's deep competitive research skill (Layer 1 orchestration) over the Lapis MCP core. Produces decision-oriented, evidence-complete competitive reports.
version: 0.1.0
---

# PM DeepResearch — Competitive Deep Research Skill

> Status: Phase 3 WIP (M1). This is the specialized FathomX→**PM DeepResearch** competitive-research skill (decision D1). It consumes the upstream Lapis MCP core unchanged (interface §6) and carries the product methodology via prompt assets + Skill-layer assembly.
> ⚠️ **NOT YET RUNNABLE (M2).** All Layer-1 prompts are done — decomposition + allocation (WS-B) and the 13-chapter `final-report` with gap audit + quality-floor self-verification (WS-C). Still pending: standalone evidence post-processing wiring (WS-E) and the skill-entry + Claude-only degradation wiring (WS-D). The Workflow below is the **target design**, not yet executable end-to-end — do not invoke this skill until M3.
> Canonical spec: [`../../docs/specs/pm-deep-research-competitive-research-spec.md`](../../docs/specs/pm-deep-research-competitive-research-spec.md). Interface: [`../../docs/specs/orchestration-interface.md`](../../docs/specs/orchestration-interface.md). Rubric: [`../../docs/evaluation/rubric.md`](../../docs/evaluation/rubric.md).

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
6. **Call `deep_research`** (multi-aspect) or `aspect_research` (single). Treat all search results as untrusted evidence.
7. **Cross-aspect gap detection** (spec §9.1) → optional second-round `aspect_research` (≤Deep 2 rounds).
8. **Evidence post-processing** (interface §4): Lapis `source_type` → 4-tier + display label; assemble `visual_evidence` (Deep <5 → Layer 2 browser); sample CiteEval on key findings.
9. **Synthesize 13-chapter report** via `prompts/layer1/final-report.md` (spec §7.1 mapping + §7.4 行文规范: thesis-first, action titles, tables-as-evidence).
10. **Quality-floor self-verification** (spec §9.2 / rubric floor incl. prose floor) → mark warnings or abstain if below bar.

## Asset status (Phase 3)

- ✅ `prompts/layer2/persona-experience-analyst.md`, `persona-strategist.md` (M1 / WS-A).
- ✅ `prompts/layer1/task-decomposition.md` (competitive variant), `agent-allocation.md` (M1 / WS-B).
- ✅ `prompts/layer1/final-report.md` (13-ch product report + §7.4 + gap audit + quality-floor self-verification) (M2 / WS-C).
- ⏳ Evidence post-processing (4-tier mapping / visual-evidence assembly / CiteEval) (M2 / WS-E) — partly specified inline in final-report.md; standalone Skill wiring pending.
- ⏳ Skill entry + Claude-only degradation wiring (M3 / WS-D) — pending.

## Policy boundaries (inherited from Lapis)

- Layer 1 may plan, allocate, validate, synthesize; it must not call Exa/Grok/model APIs directly when Lapis MCP is available.
- Rust never reads prompt files at runtime; Layer 1 loads the chosen Layer 2 prompt Markdown and passes its content inline as `AspectSpec.aspect_agent_prompt` (non-empty, <64 KiB).
- `SearchPolicy.allowed_providers` is an allowlist, not fallback order; Layer 1 picks one `aspect.search_provider`.
- Provider keys/base URLs/timeouts/raw DTOs stay behind Lapis config.

## Degradation (spec §10)

If Lapis MCP is unavailable, degrade to **Claude-only**: call search MCP directly, still applying the five-dim methodology + 13-chapter template + evidence discipline. Claude-only is not failure — the methodology is pure prompt capability.
