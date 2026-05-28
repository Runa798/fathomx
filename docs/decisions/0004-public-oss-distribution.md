# ADR-0004: 分发范围 = 真正公开 OSS

Status: Accepted (2026-05-29)

## Context
Phase 4 的目标用户范围有两档：仅 Heye+小圈子（可沿用现有 mihomo/CPA 基建）vs 真正公开 OSS 分发（普通用户无此基建）。这决定 key/网络故事要做到多硬，并反向影响 Phase 1/2 的设计野心。

## Decision
**面向真正公开 OSS 分发。** 目标用户=互联网产品/运营/业务专家、独立开发者，自助部署。

## Consequences
- Phase 4 核心难点：普通用户**自助注册/配置 exa/tavily/grok key + 无代理基建的网络故事**，而非 TUI 长相。
- Phase 1/2 的可信度机制与评测标尺必须按"通用、可被他人复现"的标准设计，不能依赖 Heye 私有环境。
- 需文档英文化（公开前）。
