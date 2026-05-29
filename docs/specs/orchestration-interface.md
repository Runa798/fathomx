# Layer1 ↔ Lapis 编排接口（WS4）

> Status: Phase 2 WS4 产出（2026-05-29，草稿待评审）。
> 目的：把 [`fathomx-competitive-research-spec.md`](fathomx-competitive-research-spec.md) 的工作流落到 **Lapis 真实 MCP 接口**（依据 [`../mcp-usage.md`](../mcp-usage.md)），明确每步谁做、传什么、schema 缺口怎么补。

---

## 0. 关键现实约束（先读）

对照 Lapis MCP 实际表面（`docs/mcp-usage.md`），早期草稿的假设需要修正：

| 草稿假设 | Lapis 实际 | 影响 |
|---|---|---|
| 有 `research_plan` 工具做拆解 | **不存在**。只有 `aspect_research` + `deep_research` | **拆解（5 维→aspect 列表）必须在 Skill 层做**，作为 `deep_research.aspect_tasks` 传入 |
| 有 `compare_reports` 工具 | **不存在** | **跨竞品对比/综合/13 章报告拼装在 Skill 层做** |
| aspect report 带 `dimension/persona/decision_intent/visual_evidence/user_jobs/gap_status` | Lapis `AspectReport` 只有 `findings/assumptions/risks/counterarguments/open_questions/confidence/limitations` | 产品结构字段**当前无 schema 位**，v2.0 用 prompt+Skill 编码承载（见 §3）|
| evidence 有 `tier/credibility A-E/visual` | Lapis `Evidence` 有 `source_type`(7 枚举) + `confidence`(low/med/high) | 4-tier 与视觉证据由 **Skill 映射/装配**（见 §4）|

**结论**：v2.0 **不改 Lapis 源码**——FathomX 作为 Skill 消费上游 Lapis 原样接口；产品方法论（五维/人格/证据完整性）通过 **`aspect_agent_prompt` 注入 + Skill 层装配**实现。可选的 Rust schema 小幅扩展留 Phase 3（§6）。

---

## 1. 端到端步骤（谁做 / 传什么）

| 步 | 动作 | 执行方 | 输入 → 输出 |
|---|---|---|---|
| 1 | 复杂度路由 + 决策意图推断 | **Skill** | 用户问题 → `decision_intent`（Enter/Differentiate/…）+ tier（Quick/Standard/Deep）|
| 2 | 五维 → aspect 拆解 | **Skill** | 决策意图 + 目标产品 → `aspect_tasks[]`（§2 映射）|
| 3 | 人格 prompt 装配 | **Skill** | 每个 aspect 填 `role` + `aspect_agent_prompt`（注入 2 人格 + TM + 输出契约，§3）|
| 4 | 预算/策略装配 | **Skill** | tier → `budget` + `model_policy`/`search_policy`/`evidence_policy`（§5）|
| 5 | 调 `deep_research` | **Skill→Lapis** | 上述组装为一次 `deep_research` 调用；Lapis 并行跑各 aspect 的 agent loop（带 search）并聚合 |
| 6 | 跨 aspect Gap 检测 | **Skill** | `DeepResearchResult` → 按规格 §9.1 清单查缺口 → 必要时对缺口 aspect 再调 `aspect_research`（≤Deep 2 轮）|
| 7 | 证据分级 + 视觉证据装配 | **Skill** | `evidence_index` → 4-tier + 展示标签 + visual_evidence 表（§4）|
| 8 | 综合 + 13 章报告 | **Skill** | aspect_reports + 证据 → 五维→13 章映射（规格 §7.1）+ 机会矩阵 + Roadmap |
| 9 | 自评 quality floor | **Skill** | 报告 → 规格 §9.2 / [rubric](../evaluation/rubric.md) floor；不达标标警告或弃权 |

> Lapis 负责的是 **步骤 5 内部**：每个 aspect 的多轮 agent loop、并行调度、搜索、逐条 evidence 绑定 finding、预算执行、partial 聚合。其余编排智能在 Skill。

---

## 2. 五维 → `aspect_tasks` 映射

每个 aspect = 一个独立 agent（自带搜索预算）。竞品研究默认拆为 4–5 个 aspect：

| aspect_id | 五维来源 | role | research_question（示意）|
|---|---|---|---|
| `job-and-competitive-set` | 维度 1 | product strategist | 用户雇这个产品完成什么 job？按 job 谁是真实竞争集（含非显性替代者）？|
| `capability-and-importance` | 维度 2+3 | product experience analyst | 目标产品与竞品在买家关注维度上的能力对位如何？哪些功能按 Kano 是 Must-be/Performance/Attractive？|
| `opportunity-gaps` | 维度 4 | product strategist | 各 desired outcome 的 Importance/Satisfaction？ODI 机会分排序？|
| `positioning-whitespace` | 维度 5 | product strategist | buyer-validated 轴上各家 value curve 如何？白地在哪？维持性 vs 颠覆性威胁？|
| `experience-paths`（Deep）| 维度 2 深化 | product experience analyst | 核心路径（进入/操作/反馈/留存/转化）的体验断点 + 视觉证据 |

- **Quick**：只跑 `job-and-competitive-set` + `capability-and-importance`。
- **Standard**：前 4 个。**Deep**：全部 5 个（+ 按需每竞品 profile）。
- `scope`/`boundaries`/`success_criteria` 由 Skill 按维度的"证据标准"（规格 §3）填，使 Lapis 的 success_criteria 即我们的证据门槛。

---

## 3. 产品结构字段如何承载（无 Rust 改动）

Lapis `Finding.claim` 是自由文本，`finding_type ∈ {fact, interpretation, recommendation, risk, assumption}`，`Evidence` 带 url/source_type/confidence。v2.0 用如下约定承载产品结构：

| 规格要的字段 | v2.0 承载方式（prompt + Skill）|
|---|---|
| `decision_intent` | 写入 `shared_context.summary`，对所有 aspect 可见 |
| 能力对位矩阵 / Kano / ODI 打分 / 定位 | `aspect_agent_prompt` 要求 agent 把结构化结果作为 **Markdown 表/JSON 块写进 `Finding.claim`**；Skill 解析装配 |
| `visual_evidence`（截图/视频 URL）| 作为 `Evidence` 条目：`url` = 媒体 URL，`source_title`/`summary` 注明 media_type + observed_feature；Skill 据约定抽成视觉证据表 |
| TM-4 认识论标注 | 复用 `finding_type`（fact/interpretation/assumption）+ `confidence`；推测类入 `assumptions`，反论入 `counterarguments`（Lapis 原生有此字段，正好承 TM-11）|
| 4-tier 可信度 | Skill 后处理：`Evidence.source_type` + URL 域名 → 4-tier + 展示标签（§4）|

> **`aspect_agent_prompt` = 人格落点**：Skill 把 2 人格（Experience Analyst / Strategist）的 TM-laden system prompt + "输出契约（哪些结构进 claim、证据要带 url、缺视觉证据要进 open_questions）" 作为 inline prompt 传入。Lapis 无 persona 概念——**persona 即 prompt**。

---

## 4. 证据分级与视觉证据装配（Skill 后处理）

Lapis `Evidence.source_type` ∈ `{official, documentation, news, blog, forum, repository, unknown}`。Skill 映射到规格 §6.1 的 4-tier + 展示标签：

| Lapis source_type | + 域名启发式 | 4-tier | 展示标签 |
|---|---|---|---|
| official / documentation | 官网/财报/应用商店/.gov/.edu | Tier 1–2 | High |
| news / blog | 主流媒体/具名评测/开发者博客 | Tier 3 | Medium |
| forum | 应用商店评论/社媒/论坛 | Tier 3（社区子类）| Low（仅情绪/线索/假设）|
| unknown | 无日期/无法追溯 | Tier 4 | Unknown（不进核心结论）|

- **视觉证据**：Skill 扫 `evidence_index`，凡 url 指向图片/视频/应用商店页且 prompt 约定的 media 标记命中 → 进规格 §6.2 的 visual_evidence 表（Ch 7）。Deep 模式若 <5 条 → 触发 Layer 2 浏览器（agent-browser/browser-use 走系统 Chrome）补抓，再回填。
- **原子核验/语句级审计**（FActScore/DeepTRACE）：Skill 对关键 finding 抽样核验 `claim` 能否从 `evidence_refs` 指向的源推出（CiteEval）；不达标降置信或弃权。

---

## 5. 预算映射（规格复杂度 tier → Lapis budget）

依据 Track A A5（先估难度→分级预算→信息增益门控）。示意值（Phase 3 调参）：

| tier | `budget.max_agents` | 每 aspect `max_search_calls` | `max_concurrent_agents` | `total_timeout_ms` |
|---|---|---|---|---|
| Quick | 2 | 3 | 2 | 120000 |
| Standard | 4 | 6 | 2 | 300000 |
| Deep | 5–6 | 8 | 2–3 | 600000 |

- `evidence_policy.require_evidence_for_findings = true` 恒开（强制"宁少但真"——finding 必须带 evidence）。`min_evidence_per_finding`：Standard=1，Deep=2。
- `model_policy.allowed_providers` / `search_policy.allowed_providers`：由用户 key 配置决定（无 Exa key 则只 grok）。**注意**：policy 的 allowed_providers 是授权白名单**不是 fallback 顺序**——降级顺序在 Skill 控制。
- Gap 第 2 轮补搜用单独 `aspect_research` 调用（带 `shared_context.prior_sources` = 已有证据，避免重复）。

---

## 6. 引擎边界：第一版不动引擎；schema 扩展作为「需求」提给上游（Heye 2026-05-29 确认）

**引擎不是我们做的**——Lapis 由上游 **4o3F** 维护，FathomX 是消费方（见 [ADR-0002](../decisions/0002-fathomx-lapis-decoupled.md)）。因此：

- **v2.0 第一版不碰引擎**：纯 prompt+Skill 承载产品字段（§3），用 [rubric](../evaluation/rubric.md) + 黄金样例实测是否够稳。
- **后续若实测承载不稳**（agent 不照约定填 claim / 漏视觉证据 / 需机器强校验），把下列 schema 扩展整理成**需求清单提给 4o3F 上游**（我们提需求，不自己改引擎源码）：
  - `Evidence` 加 `media_type` + `visual` 标记；`source_type` 扩 `app_store|social|video|research`。
  - `AspectReport` 加 `extensions: object`（自由结构）承载五维结构化输出。
  - `EvidencePolicy` 加 `require_visual_evidence_for_aspects: string[]`。
- 规格已将这些标为**可选**，不构成 v2.0 阻塞。

---

## 7. 降级（MCP 不可用）

`deep_research` 调用失败（`provider_unavailable`/`network_failed`/进程不可用）→ Skill 退化为 **Claude-only**：直接用搜索 MCP（grok/exa）按五维方法论自己跑 + 装配报告，证据纪律不变（规格 §10）。`status=partial` 时用已完成 aspect + 把 `failed_aspects` 标为 gap。

## 待办
- [ ] WS3 黄金样例实跑时，验证 §3 的 prompt 承载方案是否够稳（决定 §6 是否触发）。
- [ ] Phase 3：把 §2 映射、§3 prompt 契约、§5 预算落成 `prompts/layer1/*` + `prompts/layer2/persona-*.md` 实体文件。
