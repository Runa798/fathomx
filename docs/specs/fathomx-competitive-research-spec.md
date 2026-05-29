# FathomX 竞品深度研究 — 业务需求规格（canonical · v2.0）

> Status: Phase 2 WS1 产出（2026-05-29，草稿待 Heye 评审）。
> **单一事实源**：本文件合并并取代早期 3 份草稿（`fathomx-business-supplement.md` / `fathomx-business-input-to-lapis.md` / `Lapis 业务层补充文档：Product Deep Research 模式.md`，已归档 [`docs/archive/`](../archive/)），全面对齐 Phase 1 方法决策。
> 上游：[ADR-0006](../decisions/0006-phase1-method-decisions.md)、[Track B](../research/track-b-product-methodology.md)、[Track A](../research/track-a-orchestration-credibility.md)、[Phase 2 计划](../plans/phase2-spec-and-orchestration.md)。
> 引擎接口设计见 [`orchestration-interface.md`](orchestration-interface.md)（WS4）；评测见 [`../evaluation/rubric.md`](../evaluation/rubric.md)（WS2）。

---

## 0. 定位与范围

FathomX = 产品深度研究的 **Skill 层（Layer 1 业务编排）**，MCP 工具能力主要由 **Lapis** 引擎提供。本规格定义其**首攻能力：竞品深度研究**（v2.0）。

- **范围决策（ADR-0006 + Heye 2026-05-29）**：本规格聚焦竞品深度研究，以 **B1 五维骨架**为报告主干；通用 **MECE-6** 作为跨能力顶层框架在 §2 记录、给后续能力留位。**跑通质量后**再泛化为全 MECE-6 通用规格（ROADMAP Phase 2′）。
- **四项产出标准**（承母版，竞品研究最低线）：

| 标准 | 定义 | 最低要求 |
|---|---|---|
| 准确 | 关键事实可追溯，判断不伪装成事实 | 核心结论绑定来源 + 时间 + 置信度（§6）|
| 有证据 | 结论来自资料/截图/视频/评论/竞品 | 关键判断必须有 evidence 或 visual_evidence |
| 有产品思考 | 从用户任务→功能路径→体验断点推导机会 | 必须含功能必要性分析与体验路径（§3 dim 2-3）|
| 可落地 | 结论能进 Roadmap/实验/指标/PRD | 必须含机会矩阵 + 优先级 + 验证计划（§4/§7）|

---

## 1. 触发、决策意图、复杂度路由

### 1.1 触发条件
竞品分析、差异化判断、功能机会对位、市场进入判断、AI 升级方向（含竞品对照）等请求命中即进入竞品深度研究模式。

### 1.2 决策意图推断（先于拆解）
Orchestration Layer 先推断 `decision_intent`——用户基于本次调研做什么决策。没有决策意图，Agent 产出泛泛信息罗列；有了它，每个分析锚定到决策。

| decision_intent | 研究目标 | 关键输出 |
|---|---|---|
| Enter / Not Enter | 是否进入某市场/方向 | 竞品格局、机会缺口、进入风险、推荐结论 |
| Differentiate | 如何形成差异化 | 竞品差异、能力缺口、定位白地 |
| Build / Not Build | 是否建设某功能 | 用户价值、能力对位、复杂度、验证计划 |
| Improve | 如何优化体验 | 体验路径、断点诊断、优化建议 |
| Grow | 提升增长/留存/转化 | 漏斗问题、机制对照、实验方案 |
| AI Upgrade | 用 AI 改造产品 | AI 能力映射、场景机会、风险边界 |

> 竞品研究最常见的是 **Enter / Differentiate**。

### 1.3 复杂度路由

| 等级 | 适用 | 证据要求 | 输出 |
|---|---|---|---|
| Quick | 窄问题、快速方向判断 | 5–10 来源，≥1 竞品 | 简版判断 |
| Standard | 常规竞品/功能调研 | 10–25 来源，≥3 竞品 | 标准竞品报告 |
| Deep | 战略方向/进入判断/PRD 前置 | 25+ 来源，3–5 竞品，**含视觉证据** | 完整竞品报告（13 章）|
| Deep + Evidence Pack | 需支持评审/沉淀 | 完整来源表 + 截图/视频 URL + 评论样本 + 矩阵 | 完整报告 + 证据资产表 |

Quick 是重要"短路"——避免对简单问题启动整个多 Agent 编排。

---

## 2. 维度框架（分层）

ADR-0006 决策 1：竞品研究用 B1 五维作**报告骨架**；MECE-6 是**跨能力顶层维度集**。二者**分层**，非替换。

### 2.1 顶层框架 · MECE-6（记录 + 留位，本规格不展开执行）

| 维度 | 研究对象 |
|---|---|
| Market Context 市场与场景 | 市场边界、场景、趋势、需求背景 |
| User & JTBD 用户与待办任务 | 用户分层、动机、痛点、未满足需求 |
| Competitive Landscape 竞品与替代 | 直接/间接竞品、替代方案 |
| Product & Experience Capabilities 产品能力与体验 | 功能、流程、交互、视觉证据 |
| Business & Growth Model 商业与增长 | 获客、激励、留存、转化、变现 |
| Future Capability & Strategic Opportunity 未来能力与机会 | AI/硬件/内容/社区/数据能力 |

### 2.2 主干 · 竞品研究五维骨架（B1，§3 展开）
Job 与真实竞争集 → 能力对位矩阵 → 功能重要性分级 → 竞争缺口打分 → 定位与白地。

> 分层关系：五维骨架是 MECE-6 中「Competitive Landscape + Product Capabilities + 部分 User & JTBD」在**竞品能力内的细化主干**；泛化时五维方法（teardown/Kano/ODI/定位图）成为通用规格里对应维度的方法库。

---

## 3. 竞品研究五维骨架（报告主干）

每维 = **主用方法 + 证据标准 + 报告落点 + 关联人格/TM**。

### 维度 1 · Job 与真实竞争集
- **方法**：JTBD（Christensen / Moesta switch interview）。先写 job statement（situation→motivation→outcome），再据"完成同一 job"找出**非显性替代者**（不止同品类）。
- **证据标准**：明确 job statement + 找出至少 1 个非显性竞争者并给纳入理由。
- **报告落点**：开篇"谁是真正的对手"；重构分析单元（Ch 4 JTBD + Ch 5 竞品图谱）。
- **人格/TM**：Experience Analyst（TM-1 Job→Feature→Gap）+ Strategist 框定竞争集。
- **真实依据**：Christensen 奶昔案例（对手是香蕉/百吉饼/无聊）；Facebook vs MySpace（两个不同 job）。

### 维度 2 · 能力对位矩阵（feature teardown）
- **方法**：跨竞品功能对位矩阵，按买家关注维度评分（12 维 rubric，每格 1–5 分）。
- **证据标准（强制）**：**每格必须附证据**——截图 / 应用商店评论数 / 操作步数 / 视频时间点。无证据的格标为假设。
- **报告落点**："功能版图"，竞品报告的事实底座（Ch 6）。
- **人格/TM**：Experience Analyst（TM-1、TM-2 metrics-informed、TM-12 言行分离）。

### 维度 3 · 功能重要性分级（Kano）
- **方法**：Kano 模型（唯一学术验证的功能分级框架，Witell 2013 综述 147 篇）。每竞品每功能标 Must-be / Performance / Attractive。
- **证据标准**：分级须有用户证据（评论/调研）或明确标为 practitioner 诠释（TM-4）。
- **报告落点**："什么才真正影响用户"，叠在能力矩阵上（Ch 6）。
- **人格/TM**：Experience Analyst。
- **真实依据**：Kano 1984 原始论文（J-STAGE 核实）；GitLab 对 12 功能跑过正式 Kano 调研。

### 维度 4 · 竞争缺口打分（ODI）
- **方法**：ODI Opportunity Algorithm（§4 完整公式）。
- **证据标准**：Importance / Satisfaction 来自一手问卷优先；无一手时用研究证据/市场代理**估算 + TM-4 标注证据等级**（ADR-0006 决策 3）。
- **报告落点**：**机会矩阵的直接打分逻辑**（Ch 9）。
- **人格/TM**：Strategist。
- **真实依据**：Cordis 案例（"最小化再闭塞概率"未满足缺口 → 市占 1%→20%，J&J $109/股收购）。

### 维度 5 · 定位与白地
- **方法**：Strategy Canvas / 感知图。用 **buyer-validated 轴**画 value curve，标白地。
- **证据标准**：轴必须是买家验证过的购买维度（非臆造）；白地须给"为何无人占据"的解释或假设。
- **报告落点**："竞争定位图"，每份竞品报告的可视化产物（Ch 5 / 独立定位小节）。
- **人格/TM**：Strategist（TM-9 杠杆点、TM-13 面向市场的未来）。

### 支撑段（非 MECE 核心，但标准报告段落）

| 段落 | 方法 | 用法约束 |
|---|---|---|
| 威胁分级 | Christensen 颠覆理论 | 每竞品标"维持性 vs 颠覆性"威胁 |
| 市场结构语境 | Porter 五力 | **仅行业层、可选**；**禁止在产品层误用**（Porter 是行业结构工具）|
| 战略小结 | SWOT | **仅沟通层**，证据收齐后用，每格转成带证据的具体含义；**不作发现工具**（Hill & Westbrook 1997：SWOT 极少转化为可行动战略）|
| 竞品速写 | Cagan 3 强项 / 3 弱项 | 每个竞品 profile 的快速开头 |

> **风险优先竞品分析**（Reforge / Sachin Rekhi "Connected" 案例）：先问"什么会杀死这个策略"——作为 Strategist 的 pre-mortem（TM-8）切入。

---

## 4. 机会优先级

### 4.1 主排序 · ODI Opportunity Score
```
Opportunity = Importance + max(0, Importance − Satisfaction)
```
- 量表 1–10。**Opportunity > 10 = 欠服务（机会）**；**< 7 = 过度服务**。
- 唯一有数学化、客户数据驱动公式的框架；RICE 是团队内部估算（"披着数学外衣的猜测"），仅作备选。

### 4.2 Kano 类型叠加
ODI 排序之上叠加 Kano 类型，区分机会**性质**：Must-be = 卫生/风险项；Performance = 线性投入；Attractive = 差异化下注。混进单一 RICE 分会丢失这个区分。

### 4.3 估算与证据标注（无一手问卷时）
允许用研究证据 / 市场代理（评论主题频次、应用商店评分分布、竞品迭代信号）估算 Importance/Satisfaction，**但必须以 TM-4 标注证据等级**（实证 / 专家观点 / 假设 / 推测）。估算值的可信度由 §6 的来源分级 + 原子核验兜底。

### 4.4 备选
- **RICE**：无客户调研数据时的团队 backlog 排序（Sean McBride/Intercom 2016）。
- **WSJF**：强时间敏感/风险削减场景（Reinertsen Cost of Delay）。

---

## 5. 研究人格 + 跨人格质量门

ADR-0006 决策 2：核心 **2 人格** + **跨人格质量门**。Market/CI Analyst **不强制独立**；其职能在竞品研究里被吸收（见 §5.3）。最终人格数 Phase 3 结合实测定。

### 5.1 两个核心人格

**Product Experience Analyst（用户/体验/证据）** — 携 TM：
- **TM-1 Job→Feature→Gap**（最高杠杆）：评估功能前先定位它服务的 user job，追 job→现有功能路径→体验 gap，按"填补 gap 程度"赋权。
- **TM-2 metrics-informed 非 metrics-driven**：每个量化发现配定性解读。
- **TM-6 听弦外之音**：记录用户没说/用行为而非语言表达的东西（Horowitz "吵车要的不是更响音响而是更安静的车"）。
- **TM-10 5Qs 测试**、**TM-12 言行分离**（访谈≠行为数据，冲突点名）。

**Product Strategist（战略/权衡/前瞻）** — 携 TM：
- **TM-3 四风险去险**：推荐须覆盖价值/可用性/可行性/商业可行性，缺一不完整。
- **TM-5 显性权衡**：每个选择写出代价"选 X = 在 [时段] 显式放弃 Y"。
- **TM-7 影响层级**：执行失败往下挖战略/激励/文化根因。
- **TM-8 pre-mortem**：假设 12–18 月后已失败，列三大死因。
- **TM-9 杠杆点**：区分 10x 乘数 vs 加法 vs overhead（Doshi LNO）。
- **TM-13 面向市场的未来**：锚在市场/技术/竞争前进轨迹上；纯现状分析标"时效受限"。

### 5.2 跨人格质量门（注入所有人格）
- **TM-4 认识论状态标注**：每条重要声明标 (a) 实证—附来源 / (b) 专家观点—注出处 / (c) 假设—给可证伪版 / (d) 推测—显式标注。**这是 FathomX 可信度使命的提示词级落点。**
- **TM-11 可证伪**：每个主要结论附最强反论 + 写出"什么条件下它是错的"。

### 5.3 五维 × 人格分配

| 五维 | 主人格 | TM |
|---|---|---|
| 1 Job 与真实竞争集 | Strategist 框定 + Experience 做 JTBD | TM-1 |
| 2 能力对位矩阵 | Experience Analyst | TM-1/2/12 |
| 3 功能重要性 (Kano) | Experience Analyst | TM-1/6 |
| 4 竞争缺口 (ODI) | Strategist | TM-9 |
| 5 定位与白地 | Strategist | TM-9/13 |
| 支撑：威胁/定位/速写 | Strategist | TM-8/13 |

> **CI/Market 吸收说明**：早期母版的 Competitive Intelligence Analyst 职能（竞品图谱、功能矩阵）落到 Experience Analyst 的 teardown + Strategist 的定位/威胁；Market & Context Analyst 职能在竞品研究里降为 Strategist 的市场语境输入（Porter 仅行业层）。是否在更宽能力里恢复独立 CI/Market，Phase 3 定。

### 5.4 人格 Prompt（骨架，Phase 3 落为 `prompts/layer2/persona-*.md`）
保留母版 11.3/11.4 的结构化输出字段，**注入对应 TM 作为思维约束**，并强制 §5.2 两个质量门。具体 prompt 文件在 Phase 3 产出。

---

## 6. 证据完整性 — 一等支柱（R2）

这是 FathomX「可信度远超普通 LLM」承诺的核心，也是早期草稿最缺的部分。

### 6.1 来源可信度：4-tier 逻辑底座 + 展示标签

**摄入/校验逻辑用 4-tier**（Phase 1 A1，研究过的）；**报告展示用标签**。映射：

| 4-tier（逻辑） | 定义 | 展示标签 | 使用方式 |
|---|---|---|---|
| Tier 1 | 同行评审论文/会议、权威数据库 | **High** | 可支撑事实性结论 |
| Tier 2 | 官方文档、一手工程博客(具名)、政府/机构报告、应用商店、上市公司财报 | **High** | 可支撑事实性结论 |
| Tier 3 | 可靠新闻、二手分析、可信评测、公开访谈、开发者博客（注日期、标二手）| **Medium** | 可支撑分析性判断 |
| Tier 3（社区子类）| 应用商店评论、社媒、论坛、问答 | **Low** | 只作用户情绪/线索/假设，**不写成事实** |
| Tier 4 | 无日期/匿名/无一手出处的 LLM 摘要/未录用投稿 | **Unknown** | **不进核心结论**，只进开放问题，flag 人工复核 |

> arxiv 来源须**确认录用状态**（非 "under review"/desk-rejected）才入 Tier 1（参见 [`citation-audit.md`](../research/citation-audit.md) 的先验真伪纪律）。

### 6.2 视觉证据 `visual_evidence`（first-class）
涉及功能设计、体验路径、竞品对比、页面对比、AI 功能体验的结论，**必须**输出 visual_evidence；无法获得图片/视频 URL **必须说明缺口**，且不得给强结论。

| 字段 | 说明 |
|---|---|
| product | 产品名称 |
| screen_or_flow | 页面/流程/功能名 |
| media_type | screenshot / video / app_store_image / official_page / social_post |
| source_url | 图片/页面/视频 URL |
| timestamp | 视频时间点（非视频可空）|
| observed_feature | 观察到的功能/交互 |
| related_claim | 支撑的结论 |
| confidence | high / medium / low |

> **获取路径（WS4 细化）**：纯 API 搜索常拿不到真实截图——Deep 模式下由 Layer 2 浏览器抓取（agent-browser / browser-use 走系统 Chrome）补截图/teardown 帧；获取成本计入预算（§A5）。

### 6.3 逐声明 provenance + 多层核验
1. **原子声明核验（FActScore 范式）**：报告关键结论拆成原子声明，逐条对照其引用源核验。
2. **语句级引用审计（DeepTRACE 8 维）**：核到语句级（生产级深研系统引用准确率仅 40–80%，必须显式审计）。
3. **引用忠实性 ≠ 正确性（CiteEval）**：声明必须真能从被引源推出（高达 57% 引用是"事后合理化"）。

### 6.4 反幻觉机制（落地 3 个，优先级从高到低）
1. **citation-grounding + abstention（宁少但真）**：无可靠来源时**弃权/标"未找到"**，不编。FathomX 第一天就自我执行（见 citation-audit 对自身文档的清洗）。
2. **verification chain（rubric 验证器）**：用"验证比生成简单"的不对称性，对产出做 rubric 引导自验证。
3. **有限 self-refine**：Gap 检测→补充→再检测，**有终止条件**（边际收益递减即停，过多迭代引噪）。

---

## 7. 报告模板

### 7.1 结构：五维骨架 → 13 章映射
竞品报告用 13 章结构承载，B1 五维是喂入各章的**分析主干**：

| 章 | 标题 | 主要来源（五维/支撑）|
|---|---|---|
| 1 | 研究结论摘要 | 全部收敛：核心判断 + 推荐 + 置信度 + 最大不确定性 |
| 2 | 研究输入与边界 | decision_intent、目标产品、人群、排除范围 |
| 3 | 目标产品定位与现状 | 竞品速写（Cagan 3强3弱）|
| 4 | 用户人群与 JTBD | **维度 1**（job statement）|
| 5 | 竞品与替代方案图谱 | **维度 1**（真实竞争集）+ **维度 5**（定位图）+ 威胁分级 |
| 6 | 功能架构与体验路径 | **维度 2**（能力对位矩阵）+ **维度 3**（Kano）|
| 7 | 视觉证据资产表 | §6.2 visual_evidence |
| 8 | AI/新能力映射 | （AI Upgrade 意图时展开；否则可裁剪）|
| 9 | 产品机会矩阵 | **维度 4**（ODI 打分）+ §4 |
| 10 | Roadmap 建议 | Strategist：P0/P1/P2 + 依赖 + 验证条件 |
| 11 | 验证实验与指标 | 指标定义模板（§7.3）|
| 12 | 风险、冲突与开放问题 | TM-8 pre-mortem + 低置信/冲突证据 |
| 13 | 附录：来源与搜索记录 | Evidence Table + Search Queries + Source List（含 tier/标签）|

### 7.2 裁剪规则
- **Quick**：Ch 1 + 核心判断 + 来源（含标签）。
- **Standard**：Ch 1/2/4/5/6/9/13 + 简化机会矩阵。
- **Deep**：全 13 章，**不得删** Ch 4/5/6/7/9/12/13。

### 7.3 关键模板
**机会矩阵**（Ch 9）：

| 机会点 | 对应 JTBD | 用户价值 | 商业价值 | 复杂度 | 证据强度 | 风险 | 优先级 | 验证方式 |
|---|---|---|---|---|---|---|---|---|

**定位图**（Ch 5）：buyer-validated 双轴 value curve + 白地标注。
**指标定义**（Ch 11）：指标 / 定义 / 计算方式 / 数据来源 / 成功标准（激活率、功能使用率、留存、付费转化、任务完成率、路径流失率为常用集）。

---

## 8. Aspect Report Schema（扩展字段）

继承 Lapis 原方面报告字段（`aspect`/`findings`/`evidence`/`assumptions`/`risks`/`open_questions`/`confidence`），竞品研究扩展：

```json
{
  "aspect": "capability-matrix",
  "dimension": "competitive_capability_matrix",   // B1 五维之一
  "persona": "product-experience-analyst",        // 2 核心人格之一
  "decision_intent": "differentiate",
  "target_product": { "name": "", "positioning": "", "core_scenarios": [], "target_users": [] },
  "findings": [],
  "evidence": [
    { "title": "", "url": "", "source_type": "official|app_store|media|social|forum|video|research|other",
      "tier": 1, "display_label": "High", "retrieved_at": "YYYY-MM-DD",
      "summary": "", "related_claim": "", "epistemic_status": "evidenced|expert|assumption|speculation" }
  ],
  "visual_evidence": [ /* §6.2 字段 */ ],
  "user_jobs": [],
  "feature_architecture": [],
  "capability_matrix": [],       // 维度 2
  "kano_grades": [],             // 维度 3
  "opportunity_scores": [],      // 维度 4：{outcome, importance, satisfaction, score, estimated:bool}
  "positioning": {},             // 维度 5
  "gap_status": {
    "source_count_pass": true, "source_diversity_pass": true, "contradiction_resolved": true,
    "factual_grounding": false, "recency_pass": true, "visual_evidence_pass": false
  },
  "search_iterations": 2,
  "confidence": "medium"
}
```

> `epistemic_status` = TM-4 标注；`tier`/`display_label` = §6.1；`estimated` = ODI 估算标记（§4.3）。Rust schema 的实际扩展为 Phase 3 工作，可选、最小（仅当需机器强校验产品字段）。

---

## 9. Gap 检测清单 + Quality Floor

### 9.1 Gap 检测（Layer 1 收齐 aspect 后跨维度执行）

| 检测项 | 不合格条件 | 处理 |
|---|---|---|
| 目标产品定位 | 无官方/高可信来源 | 标假设 + 补搜 |
| 竞品覆盖 | < 3 竞品且未说明原因 | 补直接/间接/替代竞品 |
| 真实竞争集 | 只有同品类竞品 | 按维度 1 补非显性替代者 |
| 用户证据 | 只有推测，无评论/反馈 | 降置信 + 补用户证据 |
| 能力矩阵证据 | 矩阵格无证据 | 补截图/评论数/步数，否则标假设 |
| 视觉证据 | 无截图/视频/页面 URL | 标缺口，**不得给强结论** |
| ODI 打分 | 无 Imp/Sat 依据 | 补一手或标估算 + TM-4 |
| 机会优先级 | 只有建议，无价值/复杂度/风险 | 补机会矩阵 |
| 指标与验证 | 无实验/指标 | 补验证计划 |
| 时效性 | 市场/竞品数据 > 12 月 | 加日期过滤重搜 |

**迭代规则**：Standard ≤1 轮、Deep ≤2 轮 Gap 补充；2 轮后仍不满足→在"限制"章明确标注，不继续搜（避免无界）。

### 9.2 Quality Floor（Deep 模式最低门槛）

| 质量项 | 最低要求 |
|---|---|
| 目标产品基础资料 | ≥3 来源，优先 Tier 1/2 |
| 竞品数量 | ≥3，覆盖直接/间接/替代 |
| 视觉证据 | ≥5 条截图/视频/官网/评测图 URL |
| 用户证据 | ≥20 条评论/社媒摘要（Low 标签）；无法获得须说明缺口 |
| 能力对位矩阵 | 每格有证据或标假设 |
| 机会矩阵 | ≥5 机会点，每个评估价值/复杂度/证据/优先级 |
| 置信度 | 每个关键结论标 high/medium/low + epistemic_status |
| 开放问题 | 证据不足/冲突/待验证假设单列 |

不达标→报告标置信度警告或对应结论弃权（§6.4）。**Quality floor 同时是 §WS2 评测 rubric 的硬下限。**

---

## 10. 优雅降级

| 条件 | 行为 |
|---|---|
| Lapis MCP 正常 + 全 Provider 可用 | 全功能：多 Agent 并行 + 浏览器取视觉证据 |
| 部分 Provider 不可用 | 用可用 Provider，方法论章标覆盖限制 |
| Lapis MCP 不可用 | 退化为 **Claude-only**：直接调搜索 MCP，仍用五维方法论 + 报告模板 + 证据纪律 |
| 某 aspect 超时/失败 | 返回已完成 aspect，失败者标 gap，由 Layer 1 决定重试/跳过 |

Claude-only 不是失败——方法论增强（五维、决策意图、Gap、证据完整性、模板）是纯 prompt 能力，不依赖 Rust MCP。

---

## 11. 与 Phase 1 决策对照（可追溯）

| 主题 | 早期草稿 | 本规格（对齐 Phase 1）|
|---|---|---|
| 维度框架 | 仅 MECE-6 | 竞品=五维骨架（§3）；MECE-6=顶层（§2.1）|
| 研究人格 | 3+1 / 3 人格 | 2 核心 + 跨人格质量门（§5）；CI/Market 吸收 |
| 可信度 | A-E 或 High/Med/Low | 4-tier 逻辑 + 展示标签映射（§6.1）|
| 机会优先级 | `Imp+(Imp−Sat)` 简化 | ODI 完整 `Imp+max(0,Imp−Sat)` + Kano（§4）|
| 证据完整性 | 部分（母版有 visual_evidence）| 立为一等支柱：4-tier + 视觉 + 原子核验 + 反幻觉（§6）|
| 产品专家味 | 无 | 13 条 TM 注入人格（§5）|
| 报告 | MECE-6 模板 / 13 章 | 五维→13 章映射（§7.1）|

---

## 附录 · 草稿归档

WS1 完成后，3 份早期草稿移入 `docs/archive/`（保留可追溯，不再作为事实源）：
- `fathomx-business-supplement.md`、`fathomx-business-input-to-lapis.md`、`Lapis 业务层补充文档：Product Deep Research 模式.md`。

本规格通过 [`../evaluation/rubric.md`](../evaluation/rubric.md) 自评（WS2），并由 [`../evaluation/golden/`](../evaluation/golden/) 海外跑步教练 app 黄金样例验证（WS3）。Layer1↔Lapis 每步接口见 [`orchestration-interface.md`](orchestration-interface.md)（WS4）。
