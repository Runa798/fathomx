# Lapis 迁移审计报告：FathomX→ Lapis 架构

> 审计日期: 2026-05-21
> 审计方: Opus (架构级) + Codex/GPT-5.5 (代码级) 交叉审计
> 对象: Lapis Research Agent 产品文档 vs PM DeepResearch v1.2.0 现有实现

---

## 1. 核心结论

PM DeepResearch 现状不是 Lapis 目标中的"三层 Rust MCP + Rust 侧 multi-turn agent tool-call loop"。它当前是 **Layer 1 Claude Code Skill 驱动的研究工作流**，Python 只承担若干批处理任务。真正的规划、搜索循环、Gap 迭代、最终综合大多存在于 `skill/references/*.md` 的操作规程中，而不是可执行编排代码中。

Lapis 迁移的关键不是逐文件翻译 Python，而是把 PM DeepResearch 中"文档化但未代码化"的业务规则，注入 Rust 侧的 `planner`、`agent_loop`、`specialist`、`judge` 与 schema 中。

推荐 **分阶段混合迁移，目标收敛到原生 Lapis 架构**。

---

## 2. 架构层级映射

| Lapis 组件 | Lapis 位置 | PM DeepResearch 对应 | 状态 |
|---|---|---|---|
| Layer 1: Orchestration | Claude Code Skill | `skill/SKILL.md` + `references/*.md` | 存在且更丰富 |
| Layer 1 任务拆解 | Skill | `methodology.md` §1 (MECE 6-dim) | 存在，更结构化 |
| Layer 1 Agent 分配 | Skill | `strategy.md` (Quick/Standard/Deep) | 部分 (不同轴：复杂度 vs 广深) |
| Layer 1 最终报告 | Skill + `final-report.md` | Claude Phase 4/5 | 一致 |
| Layer 2: Reasoning (Rust MCP) | Rust `orchestrator/` | Python `orchestrator/src/fathomx/` | 根本不同 |
| MCP Server (4 tools) | `src/mcp/` | `python3 -m fathomx run` (Bash exec) | **缺失** |
| Agent tool-call loop | `orchestrator/agent_loop.rs` | **无** | **缺失 (最大差异)** |
| 预算/策略守卫 | `orchestrator/` | 无 | 缺失 |
| 输出 Schema 校验 | `orchestrator/judge.rs` | 无 | 缺失 |
| Model Provider trait | `model/provider.rs` | `client.py` ModelClient | 存在但更简单 |
| Search Provider trait | `search/provider.rs` | Claude 直调 MCP | 在不同层 |
| NetworkClient trait | `net/client.rs` | httpx 散落两处 | 部分 |
| Config | `config/loader.rs` | `config.py` + `config_schema.py` | 存在 |
| Prompt 资产 | `prompts/layer{1,2}/*.md` | `skill/references/*.md` + `templates/*.md` | 存在但组织不同 |

---

## 3. 关键差异分析

### 差异 1: Agent 执行模型 (Critical)

**PM DeepResearch**: Python task 是单次调用 (一个 prompt → 一个 response)
**Lapis**: Rust Agent 运行 multi-turn tool-call loop (搜索→推理→再搜索→判断停止)

Lapis Agent 可自主决定搜多少、搜什么。PM DeepResearch 依赖 Claude (Layer 1) 手动编排所有步骤。

### 差异 2: 搜索在不同层

**PM DeepResearch**: Claude 主模型直调 Grok/Exa MCP → 搜索是 Layer 1 的事
**Lapis**: Agent 通过 Rust SearchProvider → 搜索是 Layer 2/3 的事

### 差异 3: MCP 协议 vs Bash exec

**PM DeepResearch**: `python3 -m fathomx run search_extract --workspace ...` 靠 exit code + 文件
**Lapis**: 4 个 MCP tool (research_plan, deep_research, aspect_research, compare_reports)

### 差异 4: 复杂度路由 (互补)

PM DeepResearch 有 Quick/Standard/Deep 3 级路由，Lapis 有广度/深度/平衡 3 种模式。可组合。

### 差异 5: 结构化方法论 (PM DeepResearch 独有)

MECE 6 维、3 人格、Gap 迭代 — Lapis 只说"split into aspects"不规定方法论。这是 PM DeepResearch 的产品核心。

---

## 4. PM DeepResearch 业务层 → Lapis 注入点

| 业务能力 | PM DeepResearch 来源 | Lapis 注入位置 |
|---|---|---|
| 复杂度路由 (Q/S/D) | `SKILL.md` Step 1 | Layer 1 Skill + `research_plan` 返回 `ResearchTier` |
| MECE 6 维扩展 | `methodology.md` §1 | `prompts/layer1/task-decomposition.md` + `src/orchestrator/planner.rs` |
| 决策意图推断 | `methodology.md` §1 | `planner.rs` → `ResearchPlan.decision_intent` |
| 3 研究人格 | `methodology.md` §2 + `analyze.py` | `prompts/layer2/persona-{market,ci,product}.md` |
| Gap 驱动迭代 | `methodology.md` §3 | `src/orchestrator/judge.rs` (agent loop stop condition) |
| 工具-维度映射 | `methodology.md` §4 | `prompts/layer1/agent-allocation.md` |
| 来源可信度 A-E | `report-format.md` | `schema/source.rs` credibility 字段 + `final-report.md` |
| 报告模板 (3种) | `templates/*.md` | `prompts/layer1/report-template-{quick,standard,deep}.md` |
| 优雅降级 | `SKILL.md` + `strategy.md` | Layer 1 Skill (检查 MCP 可用性，路由 fallback) |
| 搜索升级链 | `strategy.md` | `prompts/layer2/search-planner.md` 或 Rust SearchService |
| 压缩规则 (55%目标) | `compress.py` | `prompts/layer2/compress-findings.md` |
| Session resume | `workspace.py` + `strategy.md` | `src/orchestrator/workflow.rs` + `session.rs` |
| Gemini Search | `gemini_search.py` | Lapis 缺失，需产品决策 → 可选 `src/search/gemini.rs` |
| Academic Search | `academic-search.md` | Lapis 缺失 → 后续 `src/search/semantic_scholar.rs` |
| Browser escalation | `browser-layer.md` | 不进首版 Rust core，Layer 1 fallback |

---

## 5. Python 代码处置清单 (逐函数级)

### 废弃 (Rust 重实现)

| Python 对象 | Rust 对应 |
|---|---|
| `ModelClient` | `src/model/client.rs` + `src/model/providers/openai_compatible.rs` |
| `ModelClient._request_with_retry` | `src/net/retry.rs` (统一重试层) |
| `ModelClientError` | `src/model/error.rs` |
| `run_sync` | Rust async runtime |
| `__main__.main` / `_run_task` | `src/mcp/server.rs` tool dispatch |
| `search_extract._run` | `src/orchestrator/specialist.rs` (嵌入 agent loop) |
| `analyze._run` | `src/orchestrator/specialist.rs` (persona agent multi-turn loop) |
| `compress._run` | `src/orchestrator/workflow.rs` synthesis preparation |
| 空 `__init__.py` 文件 | 无 |

### 迁移 Prompt 后废弃

| Python 对象 | Prompt 资产目标 |
|---|---|
| `search_extract.SYSTEM_PROMPT` | `prompts/layer2/extract-structured-data.md` |
| `PERSONA_PROMPTS["market-analyst"]` | `prompts/layer2/persona-market-analyst.md` |
| `PERSONA_PROMPTS["ci-analyst"]` | `prompts/layer2/persona-ci-analyst.md` |
| `PERSONA_PROMPTS["product-strategist"]` | `prompts/layer2/persona-product-strategist.md` |
| `compress.SYSTEM_PROMPT` | `prompts/layer2/compress-findings.md` |

### 迁移逻辑

| Python 对象 | Rust 对应 |
|---|---|
| `Config` / `ModelSpec` / `Features` | `src/schema/config.rs` (serde structs) |
| `PROVIDER_DEFAULTS` | `src/config/defaults.rs` |
| `load_config` / `save_config` | `src/config/loader.rs` |
| `check_config` | `src/config/validation.rs` 或 MCP diagnostic tool |
| `Workspace` (session/state/artifact) | `src/orchestrator/session.rs` + `artifact_store.rs` |
| `sanitize_slug` | `src/orchestrator/session.rs` helper |
| `gemini_search._run` + `_extract_*` | `src/search/providers/gemini.rs` (可选) |
| `validate_openai_compat` / `validate_exa` | `src/config/validation.rs` |

### 短期保留 (与 Rust 共存)

| Python 对象 | 理由 |
|---|---|
| `tui/app.py` + `screens/*.py` + `widgets/*.py` | 配置 onboarding 独立于 Rust 核心 |
| `utils/api_test.py` | 仅 TUI 使用 |

---

## 6. Lapis 开放问题回答

| 问题 | PM DeepResearch 实践回答 |
|---|---|
| 任务拆分规则配置化？ | 不要。放 prompt 文件，版本化管理 |
| MVP 用户选模型？ | 按 tier 选（不是按单次搜索选 provider） |
| Agent 选模型固定/动态？ | 先固定 per-tier，后续按数据演进 |
| 配置 TOML/YAML/JSON？ | TOML（Rust 惯例）|
| 搜索 trace 暴露？ | 是，放报告方法论附录 |
| 多种报告模板？ | 必须 Day 1 就有 3 种 |
| 自动可信度评分？ | 是，prompt 启发式 A-E |
| Rust 保存记录还是返回 Skill？ | 返回 Skill，避免 split-brain |

---

## 7. 交叉验证差异点 (Opus vs Codex)

| 维度 | Opus 判断 | Codex 判断 | 采纳 |
|---|---|---|---|
| `workspace.py` 归属 | Layer 1 或短期保留 | **Rust 侧必须管理 session/artifact** | Codex ✅ |
| FAST/SMART/SEARCH tier | 保留 | 弱化为 capability profile | Codex ✅ 更灵活 |
| `client.py` retry | 废弃 | retry 抽到 `net/retry.rs` 统一层 | Codex ✅ 更精确 |
| Persona 迁移 | 迁移 prompt | prompt + multi-turn loop（不是单次调用）| Codex ✅ 更深入 |
| Gemini Search | 降级路径 | 需产品决策 | 两者一致 |

---

## 8. 推荐迁移路径

### Phase 1: 类型边界 + Provider 层

建立 Lapis Rust 类型系统：
- `schema/` — config, source, plan, session, report 结构
- `model/` — ModelProvider trait + openai_compatible 实现
- `search/` — SearchProvider trait + exa + grok 实现
- `net/` — NetworkClient trait + retry policy
- `config/` — loader, validation, defaults

此阶段替代：`client.py`, `config_schema.py`, `config.py`, `utils/api_test.py`

### Phase 2: MCP + 基础编排

- `mcp/` — server + 4 个 tool (research_plan, deep_research, aspect_research, compare_reports)
- `orchestrator/workflow.rs` — 基础 workflow (无 agent loop，先单次调用)
- `orchestrator/session.rs` — session + artifact 管理

此阶段替代：`__main__.py`, `workspace.py`, Bash exec 协议

### Phase 3: Agent Loop + 业务规则下沉

- `orchestrator/agent_loop.rs` — multi-turn tool-call loop
- `orchestrator/planner.rs` — MECE 6-dim, decision intent
- `orchestrator/specialist.rs` — persona agents, extraction agents
- `orchestrator/judge.rs` — Gap checklist, confidence, schema validation
- `prompts/` — 迁移所有 prompt 资产

此阶段替代：`tasks/search_extract.py`, `tasks/analyze.py`, `tasks/compress.py`

### Phase 4 (可选): 扩展

- `search/providers/gemini.rs` — Gemini grounding
- `search/providers/semantic_scholar.rs` — 学术搜索
- TUI 迁移或保留
