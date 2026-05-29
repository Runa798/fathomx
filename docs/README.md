# PM DeepResearch 文档地图

> **单一事实源原则**：本项目的计划、决策、规格、进度以 **repo 内文档**为准，不依赖会话记忆。任何计划/决策/进度变更，先落到这里的文档，再在别处引用。

## 顶层
- [`../ROADMAP.md`](../ROADMAP.md) — 总计划（北极星、架构决策、4 Phase、版本切分、方法论）。**先读这个**。

## 目录约定

| 目录 | 用途 | 何时填充 |
|---|---|---|
| `decisions/` | ADR（架构决策记录），一决策一文件，只增不改（变更用新 ADR 标记 supersede）| 每做出一个结构性决策 |
| `plans/` | rolling-wave 计划：每 Phase/阶段开始写细化计划，完成写 review | 每 Phase/阶段开始 |
| `research/` | Phase 1 方法预研产出（文献笔记、方法对比、决策依据）| Phase 1 |
| `specs/` | Phase 2 业务需求规格（重做后的业务层文档、skill 编排设计）| Phase 2 |
| `evaluation/` | 评测标尺 rubric + 黄金样例 + 评测结果 | Phase 2 起 |
| `examples/` | MCP/用法示例 | 现有 |

## 现有文档归属（解耦前的过渡标注）

> 现阶段 repo 仍 vendored 着 Lapis 引擎（见 ROADMAP §2）。下列文档按归属分类，Phase 3 结构重组时引擎类随源码抽离。

**Lapis 引擎（上游 `4o3F/Lapis`，AGPL-3.0）**
- `architecture.md`、`configuration.md`、`development.md`、`mcp-usage.md` — 引擎自身架构/配置/开发/MCP API

**PM DeepResearch 业务层（本项目自有）**
- `specs/pm-deep-research-competitive-research-spec.md` — **竞品深度研究业务需求规格（canonical · v2.0）**，Phase 2 WS1 合并 3 份草稿而成，单一事实源
- `lapis-migration-audit.md` — 迁移审计（Opus+Codex 交叉）
- `prompt-engineering-academic-foundations.md` — 提示词工程学术依据（Phase 1 相关）
- `research-agent-product.md` — 研究 agent 产品说明

**已归档（`archive/`，被 canonical 规格取代，仅留可追溯）**
- `Lapis 业务层补充文档：Product Deep Research 模式.md`、`fathomx-business-supplement.md`、`fathomx-business-input-to-lapis.md` — 3 份早期业务层草稿（早于 Phase 1，已合并入 `specs/` canonical 规格）
