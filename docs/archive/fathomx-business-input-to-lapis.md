# FathomX 业务层输入 → Lapis 架构

> 本文档聚焦两件事：
> 1. FathomX 已验证的业务能力如何注入 Lapis 三层架构
> 2. Lapis 开放问题的 FathomX 实践回答

---

## Part 1: 业务层注入清单

Lapis 产品文档专注于技术架构（Rust MCP、Agent Loop、Provider Trait），没有定义具体的研究方法论。FathomX 在 v1.0.0 → v1.2.0 中积累了一套经实际调研验证的业务规则。以下逐项说明每个业务能力应注入 Lapis 的哪一层、哪个模块、以什么形态存在。

### 1.1 复杂度路由 (Quick / Standard / Deep)

**现状**: `SKILL.md` Step 1 定义了三级复杂度评估表，决定启用多少搜索工具和方法论深度。

**注入位置**: Layer 1 Skill (`skills/deep-research.md`)

**注入方式**: 作为 Skill 的**第一个决策步骤**，在调用任何 Rust MCP tool 之前执行。Claude 评估复杂度后，选择不同的 MCP 调用策略：

| 复杂度 | MCP 调用策略 | 方法论深度 |
|--------|-------------|-----------|
| Quick | 不调 MCP，Claude 直接用 Grok 搜一次 | 无 MECE，无 persona |
| Standard | 调 `research_plan` + 3-4 个 `aspect_research` | MECE 4 维 + persona 视角(无独立agent) |
| Deep | 调 `research_plan` + 6 个 `aspect_research` + `compare_reports` | MECE 6 维 + 3 persona agent + Gap 迭代 |

**与 Lapis 的关系**: Lapis 有"广度/深度/平衡"三种模式（§8），但没有前置的复杂度分类。建议在 `research_plan` MCP tool 的返回值中包含 `tier: "quick" | "standard" | "deep"` 字段，让 Skill 据此决定后续调用深度。也可以让 Skill 在调用 `research_plan` 时传入 `suggested_tier`，由 Rust planner 确认或调整。

**Lapis 需要新增的 schema 字段**:
```
ResearchPlan {
  tier: "quick" | "standard" | "deep",
  mode: "breadth" | "depth" | "balanced",
  ...
}
```

---

### 1.2 MECE 6 维度范围扩展

**现状**: `methodology.md` §1 定义了 6 个互斥全覆盖的研究维度模板：
1. 市场环境 (Market Context)
2. 竞争格局 (Competitive Landscape)
3. 用户需求 (User Jobs & Needs)
4. 产品能力 (Product Capabilities)
5. 战略定位 (Strategic Position)
6. 未来趋势 (Future Trajectory)

每个维度有明确的调查内容和示例子问题。

**注入位置**: 两处——

1. **Layer 1 Prompt**: `prompts/layer1/task-decomposition.md` — 指导 Claude Skill 如何拆解任务
2. **Rust Planner**: `src/orchestrator/planner.rs` + `src/schema/plan.rs` — 作为 `research_plan` 的内置维度模板

**注入方式**:

对于 Layer 1：当 Claude 调用 `research_plan` 前，Skill prompt 指导它先用 MECE 6 维展开思考，然后将展开结果作为 `research_plan` 的输入。

对于 Rust Planner：Planner 收到 Skill 传来的自然语言研究目标后，用 LLM 调用（通过 ModelProvider）生成 aspect 列表。Planner 的 system prompt 应包含 MECE 6 维模板作为结构化指引，确保 aspect 不遗漏。

**建议**: MECE 6 维不应硬编码在 Rust 中，而应作为 `prompts/layer1/task-decomposition.md` 的一部分，让 Rust planner 加载这个 prompt 文件。这样产品迭代时只改 prompt 不改代码。

**具体 prompt 资产内容** (迁移自 `methodology.md` §1):
```markdown
# prompts/layer1/task-decomposition.md

当拆解研究任务时，按以下 MECE 6 维度展开：

| 维度 | 调查内容 |
|------|---------|
| Market Context | TAM/SAM/SOM, 增长率, 监管, 宏观趋势 |
| Competitive Landscape | 直接/间接竞品, 替代品, 潜在进入者 |
| User Jobs & Needs | JTBD, 痛点, 转换触发器, 未服务细分 |
| Product Capabilities | 功能对比, UX, 定价, 技术栈, 集成 |
| Strategic Position | 护城河, SWOT, ERRC, 机会 |
| Future Trajectory | 趋势, 颠覆, 非客户群体, 预测 |

第一步：推断用户的"决策意图"——他们会基于这次调研做什么决策？
第二步：按上述 6 维度生成子问题
第三步：Quick 只覆盖 1-2 维度，Standard 覆盖 4 维度，Deep 覆盖全部 6 维度
```

---

### 1.3 决策意图推断

**现状**: `methodology.md` §1 的第一步是"Infer the decision intent"——在开始搜索前，先理解用户最终要做什么决策。

**注入位置**: `prompts/layer1/task-decomposition.md` 的第一步 + `src/schema/plan.rs`

**注入方式**: `ResearchPlan` schema 增加 `decision_intent: String` 字段。Skill 在调用 `research_plan` 时传入推断的决策意图，Rust planner 将其写入 plan 并传递给每个 aspect agent 作为上下文。

**为什么重要**: 没有决策意图，agent 会产出泛泛的"信息罗列"。有了决策意图，agent 知道要为什么服务，输出变成"可行动的判断"。这是 FathomX 核心的产品洞察。

---

### 1.4 三研究人格 (Persona)

**现状**: `methodology.md` §2 + `tasks/analyze.py` 定义了 3 个专家视角：

| 人格 | 聚焦 | 分析框架 | 对应维度 |
|------|------|---------|---------|
| Market Analyst | 市场规模/趋势/风险 | TAM/SAM/SOM, 增长驱动力, 风险因子 | 维度 1+6 |
| CI Analyst | 竞品/定位/护城河 | Porter 五力, 特征矩阵(0-3), 护城河分析 | 维度 2+4 |
| Product Strategist | 用户需求/机会/建议 | JTBD 机会评分, ERRC, OST | 维度 3+5 |

**注入位置**: `prompts/layer2/persona-*.md` (3 个文件)

**注入方式**: 每个 persona 成为一个 prompt 文件，Rust `specialist.rs` 在创建 aspect agent 时根据分配的分析方面加载对应的 persona prompt 作为 system message。

**关键变化** (Codex 审计指出): 在 FathomX 中 persona 是"读全量搜索结果 → 单次 model completion"。在 Lapis 中，persona agent 应运行 **multi-turn loop**——它可以根据自己的分析框架主动发起搜索，而不是被动接收别人搜好的数据。例如 CI Analyst 可以自己调 `company_research_exa` 去搜竞品，而不是等 Claude 搜完了再喂给它。

**具体 prompt 资产** (迁移自 `analyze.py`):
```markdown
# prompts/layer2/persona-ci-analyst.md

You are a Competitive Intelligence Analyst...
Analytical frameworks you apply:
- Porter's Five Forces
- Competitive feature matrix (scored 0-3, buyer-importance weighted)
- Strategic group mapping
- Moat analysis (network effects, switching costs, data advantages, brand, regulatory)

Your output must include:
1. Competitor identification across 4 tiers
2. Feature comparison matrix with buyer-importance weighting
3. Competitive positioning map
4. Strategic moat assessment per major player

Every claim must cite the source material. Note information gaps explicitly.
```
(其他两个 persona 同理)

---

### 1.5 Gap 驱动迭代 (6 项检查 × 最多 2 轮)

**现状**: `methodology.md` §3 定义了 6 项 gap 检查清单：

| 检查 | 通过标准 | 失败时动作 |
|------|---------|-----------|
| 来源数量 | 每维度 ≥3 独立来源 | 对该维度补充搜索 |
| 来源多样性 | ≥2 种来源类型 | 用不同搜索工具补充 |
| 矛盾解决 | 所有冲突已标注 | 补充来源仲裁 |
| 人格覆盖 | 每个适用人格已覆盖 | 对缺失维度重跑分析 |
| 事实基础 | 关键声明有数值证据 | 搜索统计数据 |
| 时效性 | 市场/竞品数据 ≤12 月 | 加日期过滤重搜 |

**注入位置**: 两处——

1. **Rust Judge**: `src/orchestrator/judge.rs` — 作为 agent loop 的停止条件和质量门控
2. **Layer 1 Skill**: Skill 在收到 `deep_research` 结果后做二次验证

**注入方式**:

对于 Rust Judge: 每个 aspect agent 的 loop 中，judge 在每轮结束后检查是否满足上述 6 项标准。如果不满足，触发补充搜索（agent 继续 loop）。最大 2 轮后强制停止，未满足的项标记为 gap 写入 aspect report 的 `open_questions` 字段。

对于 Layer 1: Skill 收到所有 aspect report 后，做跨维度的 gap 检查——某个维度是否完全缺失？跨维度的矛盾是否已标注？如果发现全局性 gap，可再调 `aspect_research` 补充。

**Lapis 需要新增的 schema 字段**:
```
AspectReport {
  ...
  gap_checks: {
    source_count: bool,
    source_diversity: bool,
    contradiction_resolved: bool,
    persona_covered: bool,
    factual_grounding: bool,
    recency: bool,
  },
  gap_iterations_used: u8,  // 0-2
  ...
}
```

---

### 1.6 工具-维度映射

**现状**: `methodology.md` §4 定义了每个研究维度最适合哪些搜索工具：

| 维度 | 最佳工具 | 原因 |
|------|---------|------|
| Market Context | Grok (extra_sources=10), Gemini | 市场报告、分析师数据 |
| Competitive Landscape | Exa (company_research), Exa (advanced) | 实体发现、公司信息 |
| User Jobs & Needs | Grok, Exa (论坛/评论) | 用户评论、App Store 数据 |
| Product Capabilities | Exa (code_context), Grok (web_fetch) | 产品文档、技术规格 |
| Strategic Position | Grok, Exa (find_similar) | 分析师报告、战略文章 |
| Future Trajectory | Semantic Scholar, Grok, Gemini | 论文、趋势报告 |

**注入位置**: `prompts/layer1/agent-allocation.md` 或 `prompts/layer2/search-planner.md`

**注入方式**: 有两个选项——

- **Option A (Layer 1 驱动)**: Skill 在调用 `research_plan` 时附带工具偏好建议，Rust planner 将其写入 aspect 分配
- **Option B (Layer 2 自主)**: 每个 aspect agent 的 search-planner prompt 包含工具选择指引，agent 自己决定用什么搜索

推荐 Option B——让 agent 自主选择更符合 Lapis "agent 独立搜索"的设计哲学。

---

### 1.7 来源可信度评级 (A-E)

**现状**: `report-format.md` 定义了 5 级可信度评级：

| 等级 | 来源类型 | 示例 |
|------|---------|------|
| A | 学术期刊、官方统计 | PubMed, 国家统计局 |
| B | 权威媒体、行业报告 | Reuters, Gartner |
| C | 专业博客、公司官网 | TechCrunch, 产品官网 |
| D | 社区讨论、用户评论 | Reddit, 知乎 |
| E | 来源不明、AI 生成 | 无法追溯 |

**注入位置**: 
- `src/schema/source.rs` — 增加 `credibility: Option<String>` 字段
- `prompts/layer1/final-report.md` — 教 LLM 给来源评级

**注入方式**: Rust 的 `SearchResponse.results[]` 增加 `source_type` 字段（基于 URL 域名启发式判断：`.edu` → A, `reuters.com` → B 等）。最终评级由 Layer 1 报告生成 LLM 完成（因为需要理解上下文）。

---

### 1.8 报告模板 (Quick / Standard / Deep)

**现状**: FathomX 有 3 个报告模板，结构差异显著：

- **Quick**: 直接回答 + 来源列表
- **Standard**: 核心发现 + 对比分析 + 来源
- **Deep**: 按 6 维度组织 + SWOT/ERRC/JTBD 框架 + 来源表 + 方法论附录

**注入位置**: `prompts/layer1/report-template-{quick,standard,deep}.md`

**注入方式**: Layer 1 Skill 根据复杂度 tier 选择模板。Rust 不需要知道模板——它只输出结构化 aspect report，Skill 决定如何组织成最终报告。

**这是 Day 1 必须有的**——没有多模板，产品体验倒退回 v1.0.0。

---

### 1.9 优雅降级

**现状**: FathomX 定义了 4 级降级矩阵：

| 条件 | 行为 |
|------|------|
| Rust MCP + 完整配置 | 全功能 |
| 仅部分 Provider | 可用 provider 工作，缺失部分 Claude 补做 |
| MCP 不可用 | Claude-only + MECE 方法论 |
| 无任何配置 | v1.1.0 等效 + 方法论增强 |

**注入位置**: Layer 1 Skill (`skills/deep-research.md`)

**注入方式**: Skill 的第一步检查 Rust MCP 是否可用（调 `research_plan` 看是否报错）。如果不可用，Skill 退化为 Claude-only 模式但仍使用 MECE 方法论。Rust MCP 内部也应有 provider 级降级——如果 Exa 不可用，只用 Grok；如果所有搜索都不可用，返回错误让 Skill 处理。

Lapis 文档目前没有降级策略，这是必须补充的。

---

### 1.10 搜索升级链

**现状**: `strategy.md` 定义了 Grok → Exa → Gemini → Browser → 人工 的升级顺序。

**注入位置**: `prompts/layer2/search-planner.md` 或 Rust SearchService priority 配置

**注入方式**: 可以在 Rust `search/service.rs` 中实现 priority-based fallback chain（对应 Lapis 的 `search_providers.*.priority` 配置）。当高优先级 provider 失败或结果不足时，自动尝试下一个。

---

### 1.11 Context 压缩 (55% 保留率)

**现状**: `compress.py` 定义了压缩规则——保留因果链/矛盾/数字/引用，目标 55% 保留率，硬底线 35%。

**注入位置**: `prompts/layer2/compress-findings.md` + `src/orchestrator/workflow.rs`

**注入方式**: 压缩作为 `deep_research` workflow 中的可选步骤。当所有 aspect report 的总 token 超过某个阈值时，Rust workflow 触发一个"compression specialist" agent，使用 compress prompt 将内容压缩后再返回 Layer 1。

---

## Part 2: Lapis 开放问题的 FathomX 回答

### Q1: 任务拆分规则是否需要配置化？

**回答: 不需要。放 prompt 文件，不暴露给用户。**

FathomX 的 MECE 6 维框架编码在 `methodology.md` 中，不在 `config.json` 中。这是正确的。任务拆解规则是**产品方法论**，不是用户偏好。它们应该：

- 版本化为 prompt 文件 (`prompts/layer1/task-decomposition.md`)
- 由产品团队迭代
- 不暴露为用户配置

唯一的例外：复杂度 tier 选择可以是用户可覆盖的（如 "我要 Deep 级调研"），但分解逻辑本身不应配置化。

---

### Q2: MVP 阶段是否需要支持用户选择 model provider 和 search provider？

**回答: 按 tier 选模型 → 是。按查询选搜索 provider → 否。**

FathomX 的 `config.json` 让用户设置 FAST/SMART/SEARCH 三个 tier 的模型，这是正确的粒度。用户关心的是"谁来做我的分析"（成本/质量 tradeoff），不是"这次搜索用 Exa 还是 Grok"（后者是系统优化）。

**Lapis 建议**:
- 暴露给用户: model provider 选择（per-tier 或 per-aspect-type）
- 不暴露给用户: search provider 路由（由 Rust SearchService 自动 dispatch）
- 暴露给用户: search provider 的启用/禁用（比如"我没有 Exa key"）

---

### Q3: Agent 的 provider 选择固定还是动态？

**回答: 先固定 per-tier，后续按使用数据演进。**

FathomX 使用固定映射：FAST=DeepSeek, SMART=GPT-5.5, SEARCH=Gemini。这对 MVP 是务实的。

动态路由（按 context 长度、分析类型选模型）增加复杂度但初期收益有限。建议在以下条件满足后再加：
1. 有 ≥100 次真实调研的使用数据
2. 能测量不同 model × aspect type 组合的质量差异
3. 有成本优化的实际压力

**Codex 审计补充**: 建议 tier 概念弱化为 capability profile（`cheap_extraction`, `strong_reasoning`, `grounded_search`, `supports_tool_calls`, `max_context_tokens`），更灵活。在配置中保留 tier 名称作为语法糖，但底层用 capability matching。

---

### Q4: 配置文件格式 TOML / YAML / JSON？

**回答: TOML。**

- Rust 生态惯例（serde + toml crate）
- 比 JSON 对人类更友好（注释、多行字符串）
- 比 YAML 更安全（无隐式类型转换、无缩进地狱）

FathomX 当前用 JSON 是因为 Python Pydantic 方便。迁移到 Rust 后没有理由继续用 JSON。

**迁移注意**: `~/.fathomx/config.json` → `~/.fathomx/config.toml`，首次启动时自动迁移。

---

### Q5: 是否需要将搜索 query 和 source trace 暴露给最终用户？

**回答: 是，放在报告的方法论附录中。**

FathomX 的 deep-report 模板有一个 Methodology 章节，列出搜索工具使用情况和限制。这对建立用户信任至关重要——用户需要知道结论是怎么来的。

**建议实现**:
- Rust 在 `deep_research` 返回值中包含 `trace_summary`（搜索了什么、用了哪些 provider、多少来源）
- Layer 1 Skill 将 trace 格式化到报告的附录中
- 不需要暴露每一条原始 query（太噪），而是汇总统计

---

### Q6: 最终报告是否需要支持多种模板？

**回答: 必须 Day 1 就有。至少 3 种。**

这是 FathomX v1.0.0 就有的核心功能。报告模板的差异不只是长度，而是**结构和分析框架**的差异：

| 模板 | 结构 | 分析框架 |
|------|------|---------|
| Quick | 直接回答 + 来源 | 无 |
| Standard | 核心发现 + 对比 + 来源 | 简化的多维对比 |
| Deep | 6 维度分章 + 战略分析 + 来源表 + 附录 | SWOT, ERRC, JTBD, Porter |

如果只有一种报告格式，对"天天跳绳 AI 方向"的 Deep 调研和对"FastAPI 0.115 变化"的 Quick 查询会输出一样冗长的结构——这是产品退步。

**Lapis 实现**: 模板作为 `prompts/layer1/report-template-*.md` 维护。Skill 根据 tier 选择。Rust 不感知模板——它只输出结构化 aspect report。

---

### Q7: 是否需要对来源进行自动可信度评分？

**回答: 是，用 prompt 启发式（A-E），不需要 ML。**

FathomX 实践验证：让 LLM 基于来源域名和内容特征打 A-E 分，90%+ 情况下评级合理。例如：
- `nature.com` → A (学术)
- `reuters.com` → B (权威媒体)
- `techcrunch.com` → C (专业博客)
- `reddit.com` → D (社区)
- 无法识别 → E

**Lapis 实现建议**:

1. Rust `SearchResponse.results[]` 增加 `source_domain: String` 字段
2. Rust 可以做简单的域名 → 类别映射（规则表，不是 ML）
3. 最终 A-E 评级由 Layer 1 LLM 在生成报告时完成（需要理解上下文）
4. `prompts/layer1/final-report.md` 包含评级指引

---

### Q8: Rust 保存完整运行记录还是只返回给 Claude Code？

**回答: 返回结构化数据给 Skill，让 Skill 决定持久化。**

FathomX 的 workspace 协议存在 split-brain 问题——Python orchestrator 和 Claude 都往同一个目录写文件，互相不知道对方写了什么。

**Lapis 推荐**:
- Rust 返回结构化 JSON（aspect reports, trace, errors, session state）作为 MCP tool 的返回值
- Skill 收到后决定：哪些写到 workspace 文件（给用户看），哪些只在内存中用于综合
- **例外**: 如果调研中断需要恢复，Rust 应返回足够的 session state 让 Skill 写一个 recovery-friendly `state.json`

这避免了 Rust 和 Skill 同时写磁盘的协调问题，也更符合 Lapis "Rust 不做最终报告拼接"的原则。

**Codex 审计补充**: Workspace/Session 状态管理不应只留 Layer 1。Rust 侧应有 `session.rs` 管理中间状态，支持 `deep_research` 跨多次 tool call 延续（因为一次 `deep_research` 可能时间很长，Claude 可能超时重试）。但持久化到磁盘的决定权在 Skill。
