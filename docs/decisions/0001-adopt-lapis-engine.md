# ADR-0001: 采纳 Lapis 三层 Rust 引擎作基座

Status: Accepted (2026-05-21)

## Context
FathomX 需要一个可信、低幻觉的深度研究执行内核。自建 Python httpx 直调模型不是长久之计。Lapis 提供三层 Rust MCP 架构（Orchestration/Reasoning/Retrieval），自带预算治理与逐字证据 provenance 校验。

## Decision
采纳 Lapis 三层 Rust MCP 架构作为 FathomX 引擎基座。砍掉 Gemini Search（广度由 agent 多轮 loop 实现）与 Academic Search（Semantic Scholar 不进首版）。Search Provider 初始只有 Exa + Grok。业务层（MECE、人格、Gap、模板、可信度）作为 prompt 资产注入，不写进 Rust。

## Consequences
- Layer 1 业务编排留在 prompts/skill，Rust 只做机制（上轮三方核验已确认）。
- 注入清单见 `docs/archive/fathomx-business-input-to-lapis.md`（Phase 2 已合并入 `docs/specs/fathomx-competitive-research-spec.md`），审计见 `docs/lapis-migration-audit.md`。
