# ADR-0005: 许可证 = AGPL-3.0

Status: Accepted (2026-05-29)

## Context
Lapis 是 AGPL-3.0。PM DeepResearch 作为消费/分发 Lapis 的项目，且本身要公开 OSS，需明确许可证。

## Decision
**PM DeepResearch 采用 AGPL-3.0**，与 Lapis 一致。

## Consequences
- repo 已带 AGPL-3.0 `LICENSE` 全文 + README 声明（同步 Lapis 带入），基本满足。
- 待补：`Cargo.toml` 的 `license` 字段未声明；将来 PM DeepResearch 自有组件/品牌 README 要保留 AGPL 声明；考虑加入 Heye/PM DeepResearch 的 copyright 行。
- AGPL 网络条款：作为用户自部署工具无碍；若将来提供托管服务需提供源码。
- 收尾动作纳入 Phase 3/4。
