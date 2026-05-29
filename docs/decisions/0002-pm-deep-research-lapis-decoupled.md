# ADR-0002: PM DeepResearch 与 Lapis 解耦 + 后期一键安装

Status: Accepted (2026-05-29)

## Context
当前 PM DeepResearch 仓库 vendored 着 Lapis 引擎源码（同步上游带入）。需要确定 PM DeepResearch 与 Lapis 的长期关系：monorepo vendored vs 解耦依赖。这影响仓库结构、部署方式、上游同步、AGPL 边界。

## Decision
**解耦**：PM DeepResearch 仓库只含 skill 层（skills/prompts）+ 安装/配置引导；Lapis 作为独立 MCP server 消费（上游 `4o3F/Lapis`）。PM DeepResearch 后期提供**一键部署安装 Lapis** 的能力，使用户体验仍是"装一个"。

## Consequences
- 现阶段（Phase 1/2 设计期）保留 vendored 副本当工作参考。
- **结构重组（抽离引擎源码、README/品牌改 PM DeepResearch）放到 Phase 3 入口**。
- 一键安装需明确如何拉取/构建 Lapis（依赖 `4o3F/Lapis` 是否 Heye 可控 — 见 ROADMAP §7）。
- PM DeepResearch 通过 MCP stdio 调用 Lapis（独立进程），利于 AGPL 边界清晰。
