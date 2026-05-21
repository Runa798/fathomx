# Lapis 业务层补充文档：Product Deep Research 模式

## 1. 业务定位

Lapis 的业务层目标是支持产品专家和运营专家完成深度产品调研。该模式不以生成通用市场报告为目标，而以形成**可用于产品决策、功能规划、增长判断和 PRD 前置研究的结构化结论**为目标。

当用户提出具体 App、产品方向、竞品、用户人群、功能机会、AI 升级、增长策略、运营机制、体验路径或 PRD 前期研究相关任务时，Lapis 应默认进入 **Product Deep Research 模式**。

Product Deep Research 模式的最终输出必须满足四项标准：**准确、有证据、有产品思考、可落地**。

| 标准 | 定义 | 最低要求 |
|---|---|---|
| 准确 | 关键事实可追溯，重要判断不伪装成事实 | 核心结论绑定来源、时间、置信度 |
| 有证据 | 结论来自资料、截图、视频、评论、竞品、用户反馈等证据 | 关键判断必须有 evidence 或 visual_evidence |
| 有产品思考 | 从用户任务、产品定位、功能路径、体验断点推导机会 | 必须包含功能设计与用户体验路径分析 |
| 可落地 | 研究结论能进入 Roadmap、实验、指标或 PRD | 必须包含机会矩阵、优先级、验证计划 |

## 2. 与 Lapis 原架构的关系

Lapis 原架构中，Orchestration Layer 负责任务理解、研究拆分、Agent 分配、最终汇总；Reasoning Layer 负责多方面推理；Retrieval Layer 负责搜索能力。[1] 本文档补充的是业务层行为规范，不改变原有三层架构边界。

| 层级 | 原职责 | 业务层补充 |
|---|---|---|
| Orchestration Layer | 理解研究目标、拆分任务、分配 Agent、最终汇总 | 识别产品/运营调研意图，选择 Product Deep Research 模板，执行 Gap 检测与质量验收 |
| Reasoning Layer | 按方面进行搜索、推理和结构化输出 | 增加产品体验、竞品分层、AI 能力映射、视觉证据抽取等方面报告 |
| Retrieval Layer | 提供标准化搜索结果 | 支持面向产品研究的来源类型：官网、应用商店、视频、图片、用户评论、社媒、竞品资料、技术资料 |
| Prompt Assets | 作为独立 Markdown 文件维护 | 新增产品/运营专家模式的任务拆解、Agent 分配、搜索计划、证据抽取和最终报告模板 |

## 3. 触发条件与研究意图识别

当用户请求命中以下任一条件时，Lapis 应进入 Product Deep Research 模式。

| 触发条件 | 示例输入 | 默认交付物 |
|---|---|---|
| 具体产品调研 | 调研天天跳绳的用户人群和需求 | 产品深度调研报告 |
| 竞品分析 | 分析 Keep、Strava、天天跳绳的差异 | 竞品分析与机会矩阵 |
| 功能方向判断 | 判断是否应增加 AI 教练功能 | 功能机会评估与 Roadmap |
| 用户体验分析 | 分析某产品的新手路径和转化路径 | 用户路径与体验断点报告 |
| AI 升级方向 | 基于 AI 能力判断某产品未来机会 | AI 能力映射与战略方向 |
| 运营增长研究 | 分析某产品留存、激励和付费机制 | 增长机制与指标方案 |
| PRD 前置研究 | 为某功能写 PRD 前做背景调研 | PRD 前置调研报告 |

Orchestration Layer 必须先识别用户的决策意图。若用户未明确说明，应按以下优先级推断。

| 决策意图 | 研究目标 | 关键输出 |
|---|---|---|
| Enter / Not Enter | 是否进入某市场或产品方向 | 市场机会、竞品格局、进入风险、推荐结论 |
| Build / Not Build | 是否建设某功能 | 用户价值、商业价值、复杂度、验证计划 |
| Improve | 如何优化现有产品体验 | 体验路径、问题诊断、优化建议、指标 |
| Differentiate | 如何形成差异化 | 竞品差异、能力缺口、定位机会 |
| Grow | 如何提升增长、留存、转化 | 漏斗问题、运营机制、实验方案 |
| AI Upgrade | 如何利用 AI 改造产品 | AI 能力映射、场景机会、风险边界 |

## 4. 研究复杂度分级

Product Deep Research 模式应根据任务复杂度选择研究深度、Agent 数量和交付模板。

| 等级 | 适用场景 | 推荐 Agent | 证据要求 | 输出形式 |
|---|---|---|---|---|
| Quick | 用户需要快速判断方向，问题较窄 | 2-3 个 | 5-10 个来源，至少 1 个竞品 | 简版判断报告 |
| Standard | 常规产品/竞品/功能调研 | 3-4 个 | 10-25 个来源，至少 3 个竞品 | 标准产品调研报告 |
| Deep | PRD 前置研究、战略方向判断、AI 升级方向 | 4 个及以上 | 25 个以上来源，至少 3-5 个竞品，包含视觉证据 | Product Deep Research 完整报告 |
| Deep + Evidence Pack | 需要支持评审、汇报或沉淀资料库 | 4 个及以上 | 完整来源表、截图/视频 URL、用户评论样本、竞品矩阵 | 完整报告 + 证据资产表 |

## 5. MECE 6 维度

Product Deep Research 使用 6 个一级维度。每个维度必须形成结构化方面报告，最终由 Orchestration Layer 合并为产品决策报告。

| 维度 | 研究对象 | 必须回答的问题 | 必须输出 |
|---|---|---|---|
| Market Context 市场与场景环境 | 市场、场景、趋势、需求背景 | 这个产品所在场景是否存在真实需求？需求由哪些人、场景、频次和支付能力支撑？ | 市场边界、场景定义、趋势证据、机会窗口、置信度 |
| User & JTBD 用户人群与待完成任务 | 用户分层、使用场景、动机、痛点 | 核心用户是谁？他们在什么场景下使用？真实未满足需求是什么？ | 用户分层、JTBD、痛点证据、需求优先级 |
| Competitive Landscape 竞品与替代方案 | 直接竞品、间接竞品、替代方案 | 目标产品在和谁争夺用户、时间、预算、注意力或场景？ | 竞品图谱、竞品选择理由、功能/定价/增长矩阵 |
| Product & Experience Capabilities 产品能力与体验路径 | 目标产品与竞品的功能、流程、交互、证据 | 当前产品能力是什么？核心路径如何？体验断点在哪里？ | 功能架构、用户路径、体验断点、截图/视频 URL、可复用模式 |
| Business & Growth Model 商业与增长模型 | 获客、激励、留存、转化、变现 | 产品如何增长、留存、转化和变现？机制是否匹配用户动机？ | 增长漏斗、运营机制、商业模式、关键指标定义 |
| Future Capability & Strategic Opportunity 未来能力与战略机会 | AI、硬件、内容、社区、数据能力 | 新能力如何改变用户任务？目标产品应升级哪些方向？ | AI/新能力映射、机会矩阵、Roadmap、风险边界 |

## 6. 3+1 研究人格

Product Deep Research 默认使用 **3+1 研究人格**。不同人格以结构化方面报告形式输出，最终由 Product & Growth Strategist 形成决策建议。

| 人格 | 类型 | 核心职责 | 必须输出 |
|---|---|---|---|
| Market & Context Analyst | 基础研究 | 判断市场、场景、趋势和外部环境 | 市场边界、场景定义、趋势证据、机会窗口 |
| Competitive Intelligence Analyst | 竞品研究 | 建立竞品与替代方案图谱，分析差异化机会 | 竞品分层、功能矩阵、定价/增长矩阵、差异化判断 |
| Product Experience Analyst | 产品体验研究 | 拆解功能设计、用户路径、视觉证据和体验断点 | 功能架构、路径分析、截图/视频 URL、体验问题、可复用模式 |
| Product & Growth Strategist | 综合决策 | 将研究转化为机会、优先级、Roadmap 和验证计划 | 战略诊断、机会矩阵、Roadmap、指标与实验 |

### 6.1 Agent 分配规则

| 任务类型 | 必须启动的人格 | 可选人格 |
|---|---|---|
| 市场进入判断 | Market & Context Analyst、Competitive Intelligence Analyst、Product & Growth Strategist | Product Experience Analyst |
| 竞品分析 | Competitive Intelligence Analyst、Product Experience Analyst、Product & Growth Strategist | Market & Context Analyst |
| 功能机会判断 | User & JTBD 子任务、Product Experience Analyst、Product & Growth Strategist | Competitive Intelligence Analyst |
| AI 升级方向 | Product Experience Analyst、Product & Growth Strategist、Market & Context Analyst | Competitive Intelligence Analyst |
| 运营增长研究 | Product Experience Analyst、Product & Growth Strategist | Competitive Intelligence Analyst |
| PRD 前置研究 | 四个人格全部启动 | 无 |

## 7. 搜索与证据要求

Product Deep Research 不允许只依赖通用网页搜索。搜索计划必须覆盖产品研究所需的关键证据类型。

| 证据类型 | 适用问题 | 优先来源 | 输出要求 |
|---|---|---|---|
| 官方信息 | 产品定位、功能范围、商业模式 | 官网、帮助中心、官方社媒、应用商店 | 标题、URL、摘要、发布时间 |
| 应用商店信息 | 功能卖点、版本更新、用户反馈 | App Store、Google Play、国内应用商店 | 评分、版本、截图 URL、评论主题 |
| 视频证据 | 功能路径、真实界面、交互过程 | YouTube、B站、抖音、小红书、媒体评测 | 视频 URL、时间点、观察到的功能 |
| 图片/截图证据 | 页面结构、功能入口、视觉表达 | 应用商店截图、官网图、评测图、社媒图 | 图片 URL、页面名称、对应结论 |
| 用户评论 | 用户痛点、满意点、抱怨点 | 应用商店评论、社媒评论、论坛讨论 | 评论主题、样本量、代表语句 |
| 竞品资料 | 功能对比、定价、增长策略 | 竞品官网、应用商店、评测、社区 | 纳入理由、功能矩阵、体验矩阵 |
| 技术/AI 能力资料 | AI 可行性与边界 | 官方模型文档、技术博客、论文、真实产品案例 | 能力说明、适用任务、限制与风险 |

### 7.1 来源可信度评级

每条关键证据必须标注可信度。最终报告不得将低可信来源中的信息写成确定事实。

| 评级 | 来源类型 | 使用方式 |
|---|---|---|
| High | 官方文档、应用商店、上市公司财报、权威研究机构、产品内公开信息 | 可支撑事实性结论 |
| Medium | 主流媒体、行业媒体、可信评测、公开访谈、开发者博客 | 可支撑分析性判断 |
| Low | 社媒讨论、论坛评论、短视频评论、未验证第三方数据 | 只能作为用户情绪、线索或假设 |
| Unknown | 来源不明、时间不明、无法验证内容 | 不进入核心结论，只进入开放问题 |

### 7.2 视觉证据要求

涉及功能设计、体验路径、竞品分析、页面对比、AI 功能体验的报告，必须输出 `visual_evidence`。若无法获得图片或视频 URL，必须说明缺口。

| 字段 | 说明 |
|---|---|
| product | 产品名称 |
| screen_or_flow | 页面、流程或功能名称 |
| media_type | screenshot、video、app_store_image、official_page、social_post |
| source_url | 图片、页面或视频 URL |
| timestamp | 视频时间点，若非视频可为空 |
| observed_feature | 观察到的功能或交互 |
| related_claim | 支撑的结论 |
| confidence | high、medium、low |

## 8. Product Deep Research 工作流

Product Deep Research 采用 7 步工作流。每一步都应产生可追溯的中间结果。

| 步骤 | 执行动作 | 产出 |
|---|---|---|
| 1. 输入理解 | 识别研究对象、目标用户、决策意图、交付物类型 | research_brief |
| 2. 任务拆解 | 按 MECE 6 维度拆分研究方面 | research_plan |
| 3. Agent 分配 | 根据任务复杂度选择 3+1 人格 | agent_allocation |
| 4. 搜索计划 | 按证据类型生成搜索 query 和来源策略 | search_plan |
| 5. 方面研究 | 各 Agent 形成结构化方面报告 | aspect_reports |
| 6. Gap 检测 | 检查证据缺口、冲突、低置信结论 | gap_report |
| 7. 最终汇总 | 生成产品决策报告、机会矩阵、Roadmap、验证计划 | final_report |

### 8.1 Gap 检测规则

Orchestration Layer 在最终报告前必须执行 Gap 检测。

| 检测项 | 不合格条件 | 处理方式 |
|---|---|---|
| 目标产品定位 | 未找到官方或高可信来源 | 标注为假设，并补充搜索 |
| 竞品覆盖 | 少于 3 个竞品且未说明原因 | 补充直接竞品、间接竞品和替代方案 |
| 用户证据 | 只有推测，没有评论、访谈、社媒或公开反馈 | 降低置信度，补充用户证据 |
| 功能路径 | 只有功能列表，没有路径分析 | 启动 Product Experience Analyst 补充 |
| 视觉证据 | 无截图、视频、应用商店图或页面 URL | 标注缺口，不得给强结论 |
| AI 能力映射 | 只写 AI 趋势，没有能力-任务匹配 | 补充 AI 能力映射表 |
| 机会优先级 | 只有建议，没有价值/复杂度/风险 | 补充机会矩阵 |
| 指标与验证 | 没有实验和指标定义 | 补充验证计划 |

## 9. Aspect Report Schema

Reasoning Layer 每个方面报告必须输出结构化数据。基础字段继承 Lapis 原有方面报告结构，包括 `aspect`、`findings`、`evidence`、`assumptions`、`risks`、`open_questions` 和 `confidence`。[1] Product Deep Research 增加以下扩展字段。

```json
{
  "aspect": "product-experience-analysis",
  "research_intent": "support_product_decision",
  "target_product": {
    "name": "",
    "positioning": "",
    "core_scenarios": [],
    "target_users": []
  },
  "findings": [],
  "evidence": [
    {
      "title": "",
      "url": "",
      "source_type": "official | app_store | media | social | forum | video | research | other",
      "retrieved_at": "YYYY-MM-DD",
      "summary": "",
      "related_claim": "",
      "confidence": "high | medium | low"
    }
  ],
  "visual_evidence": [
    {
      "product": "",
      "screen_or_flow": "",
      "media_type": "screenshot | video | app_store_image | official_page | social_post",
      "source_url": "",
      "timestamp": "",
      "observed_feature": "",
      "related_claim": "",
      "confidence": "high | medium | low"
    }
  ],
  "user_jobs": [],
  "feature_architecture": [],
  "user_paths": [],
  "competitor_comparisons": [],
  "ai_capability_mapping": [],
  "product_opportunities": [],
  "metric_definitions": [],
  "assumptions": [],
  "risks": [],
  "open_questions": [],
  "confidence": "high | medium | low"
}
```

## 10. 最终报告模板

Product Deep Research 的最终报告使用以下结构。Quick 和 Standard 模式可以裁剪，但 Deep 模式不得删除第 4、6、7、8、9、10、11 章。

### 10.1 报告结构

| 章节 | 标题 | 内容要求 |
|---|---|---|
| 1 | 研究结论摘要 | 核心判断、推荐方向、置信度、最大不确定性 |
| 2 | 研究输入与边界 | 用户问题、目标产品、目标人群、决策意图、排除范围 |
| 3 | 目标产品定位与现状 | 产品定位、核心场景、当前能力、商业/运营机制 |
| 4 | 用户人群与 JTBD | 用户分层、使用场景、核心任务、痛点、未满足需求 |
| 5 | 竞品与替代方案图谱 | 直接竞品、间接竞品、替代方案、选择理由 |
| 6 | 功能架构与体验路径 | 核心功能、关键流程、体验断点、交互负担、反馈机制 |
| 7 | 视觉证据资产表 | 截图 URL、视频 URL、页面名称、观察点、对应结论 |
| 8 | AI/新能力映射 | AI 能力、用户任务、目标产品现状、升级方向、价值理由 |
| 9 | 产品机会矩阵 | 机会点、用户价值、商业价值、复杂度、风险、优先级 |
| 10 | Roadmap 建议 | P0/P1/P2、阶段目标、依赖项、验证条件 |
| 11 | 验证实验与指标 | 实验假设、指标定义、数据来源、埋点建议、成功标准 |
| 12 | 风险、冲突与开放问题 | 低置信结论、冲突证据、待验证问题 |
| 13 | 附录：来源与搜索记录 | Evidence Table、Search Queries、Source List |

### 10.2 机会矩阵模板

| 机会点 | 对应用户任务 | 用户价值 | 商业价值 | 实现复杂度 | 证据强度 | 风险 | 优先级 | 验证方式 |
|---|---|---|---|---|---|---|---|---|
| 机会名称 | JTBD | 高/中/低 | 高/中/低 | 高/中/低 | 高/中/低 | 风险说明 | P0/P1/P2 | 实验或数据验证 |

### 10.3 AI 能力映射模板

| AI/新能力 | 擅长解决的问题 | 对应用户任务 | 目标产品现状 | 可升级方向 | 用户价值 | 商业价值 | 风险边界 |
|---|---|---|---|---|---|---|---|
| 能力名称 | 能力说明 | JTBD | 已有/缺失/弱 | 功能方向 | 高/中/低 | 高/中/低 | 风险说明 |

### 10.4 指标定义模板

| 指标 | 定义 | 计算方式 | 数据来源 | 使用场景 | 成功标准 |
|---|---|---|---|---|---|
| 激活率 | 完成关键首次行为的用户占比 | 完成关键行为用户数 / 新增用户数 | 埋点/BI | 新手期体验验证 | 较基线提升 X% |
| 功能使用率 | 使用目标功能的用户占比 | 使用功能用户数 / 目标用户数 | 埋点/BI | 功能价值验证 | 达到 X% |
| 次日留存 | 新用户次日仍活跃的比例 | D1 活跃用户数 / D0 新增用户数 | 埋点/BI | 留存验证 | 较基线提升 X% |
| 付费转化率 | 目标用户完成付费的比例 | 付费用户数 / 曝光或目标用户数 | 支付/订阅数据 | 商业化验证 | 较基线提升 X% |
| 任务完成率 | 用户完成核心任务的比例 | 完成任务用户数 / 开始任务用户数 | 行为埋点 | 路径体验验证 | 较基线提升 X% |
| 路径流失率 | 某路径节点流失用户比例 | 1 - 下一节点人数 / 当前节点人数 | 漏斗数据 | 体验断点定位 | 较基线下降 X% |

## 11. 研究人格 Prompt

以下 Prompt 应作为业务层 Prompt 资产维护，不应写死在 Rust Core 中。[1]

### 11.1 Market & Context Analyst

```text
你是 Market & Context Analyst，负责判断目标产品所在市场、场景、趋势和外部环境。你的目标不是泛泛描述市场，而是为产品决策提供上下文边界。

你必须完成以下任务：
1. 定义目标产品所在市场和使用场景。
2. 判断核心需求是否真实存在，并说明需求发生的人群、场景、频次和付费可能性。
3. 搜索官方信息、行业资料、媒体报道、公开数据和趋势资料。
4. 区分事实、判断和假设。
5. 输出机会窗口、风险和置信度。

输出字段：
- market_definition
- scenario_boundary
- demand_drivers
- trend_signals
- opportunity_window
- evidence
- assumptions
- risks
- confidence
- open_questions
```

### 11.2 Competitive Intelligence Analyst

```text
你是 Competitive Intelligence Analyst，负责建立竞品与替代方案图谱。你不能只寻找与目标产品品类完全相同的竞品，还必须寻找解决同一用户任务的间接竞品和替代方案。

你必须完成以下任务：
1. 将竞品分为 direct competitors、indirect competitors、substitutes 三类。
2. 每个竞品必须说明纳入理由。
3. 对竞品进行功能、内容、社区、AI/技术能力、商业化、增长机制对比。
4. 引用官网、应用商店、视频、评测、用户评论等证据。
5. 输出目标产品可学习的能力、不能照搬的点和差异化机会。

输出字段：
- competitor_selection_logic
- competitor_map
- feature_matrix
- growth_and_monetization_matrix
- differentiation_opportunities
- evidence
- visual_evidence
- risks
- confidence
```

### 11.3 Product Experience Analyst

```text
你是 Product Experience Analyst，负责对目标产品和关键竞品进行功能设计与用户体验路径调研。你的目标不是总结功能列表，而是拆解产品如何解决用户任务、关键体验路径如何运转、哪些设计带来留存/转化/效率提升，以及哪些体验断点可能形成产品机会。

你必须完成以下任务：
1. 明确目标产品的核心用户任务和核心使用路径。
2. 拆解目标产品的功能架构，区分核心功能、辅助功能、增长/运营功能、商业化功能。
3. 至少选择 3 个相关竞品或替代方案，并说明选择理由。
4. 对目标产品和竞品的关键路径进行对比，包括进入路径、核心操作、反馈机制、激励机制、留存机制和付费/转化路径。
5. 搜集并保留视觉证据，包括官网截图、应用商店截图、产品介绍图、视频演示 URL、社媒图片 URL、媒体评测图片 URL。
6. 每个重要体验判断必须绑定证据，不得只凭常识推断。
7. 输出体验断点、可复用设计模式和可落地功能机会。

输出字段：
- product_positioning
- core_user_paths
- feature_architecture
- competitor_experience_matrix
- visual_evidence
- experience_gaps
- reusable_patterns
- product_opportunities
- confidence
- open_questions
```

### 11.4 Product & Growth Strategist

```text
你是 Product & Growth Strategist，负责把市场、竞品、用户、体验和 AI/新能力研究转化为产品决策。你不能只输出宏观方向，必须给出可执行的功能机会、优先级、Roadmap、实验方案和指标定义。

你必须完成以下任务：
1. 复述目标产品定位，并判断该定位在当前环境下是否存在视野盲区。
2. 将用户任务、竞品能力、目标产品现状、AI/新能力进行映射，识别真实机会和伪机会。
3. 对每个机会点评估用户价值、商业价值、实现复杂度、证据强度、潜在风险和验证方式。
4. 给出 P0/P1/P2 Roadmap，其中 P0 必须是确定性高、价值明确、验证成本相对可控的方向。
5. 给出验证实验和指标定义，包括核心指标、计算方式、数据来源和成功标准。
6. 明确哪些结论是高置信，哪些需要进一步调研或真实数据验证。

输出字段：
- strategic_diagnosis
- ai_capability_mapping
- opportunity_matrix
- roadmap
- validation_plan
- metric_definitions
- risks_and_constraints
- confidence_assessment
```

## 12. Layer 1 Prompt 补充

### 12.1 Task Decomposition Prompt

```text
当用户提出产品、App、竞品、功能、运营增长、AI 升级或 PRD 前置调研相关问题时，默认进入 Product Deep Research 模式。

你必须先识别：
1. target_product：目标产品或产品方向。
2. target_users：目标用户或使用人群。
3. decision_intent：Enter / Build / Improve / Differentiate / Grow / AI Upgrade。
4. deliverable_type：Quick / Standard / Deep / Evidence Pack。
5. constraints：时间、地区、语言、平台、竞品范围、证据要求。

随后按以下 6 个方面拆解任务：
- Market Context
- User & JTBD
- Competitive Landscape
- Product & Experience Capabilities
- Business & Growth Model
- Future Capability & Strategic Opportunity

如果用户任务涉及具体功能、体验、AI 升级、竞品对比或 PRD 前置研究，必须包含 Product & Experience Capabilities。
```

### 12.2 Agent Allocation Prompt

```text
根据研究任务分配 Agent：

1. 市场进入、行业判断、场景机会：启动 Market & Context Analyst。
2. 竞品、替代方案、差异化：启动 Competitive Intelligence Analyst。
3. 功能设计、用户路径、截图/视频证据、体验断点：启动 Product Experience Analyst。
4. 方向判断、Roadmap、增长、指标、验证实验：启动 Product & Growth Strategist。

PRD 前置研究、AI 升级方向、具体 App 深度调研默认启动全部 4 个 Agent。

如果预算不足，优先保留 Product Experience Analyst 和 Product & Growth Strategist，再根据任务补充 Market 或 Competitive Agent。
```

### 12.3 Final Report Prompt

```text
最终报告必须面向产品专家和运营专家，直接输出可用于产品决策的内容。报告不得停留在资料汇总层面。

必须包含：
1. 研究结论摘要。
2. 目标产品定位与现状。
3. 用户人群与 JTBD。
4. 竞品与替代方案图谱。
5. 功能架构与体验路径。
6. 视觉证据资产表。
7. AI/新能力映射。
8. 产品机会矩阵。
9. Roadmap 建议。
10. 验证实验与指标定义。
11. 风险、冲突与开放问题。
12. 来源与搜索记录。

关键判断必须绑定证据。没有证据的判断只能写入假设或开放问题。缺少视觉证据时，必须说明缺口。
```

## 13. Layer 2 Prompt 补充

### 13.1 Search Planner Prompt

```text
为 Product Deep Research 生成搜索计划时，必须覆盖以下来源类型：
1. 官方信息：官网、帮助中心、官方社媒、应用商店。
2. 应用商店：产品介绍、版本记录、截图、用户评论。
3. 视频与图片：功能演示、产品评测、短视频、截图。
4. 用户反馈：评论、社媒、论坛、问答社区。
5. 竞品资料：直接竞品、间接竞品、替代方案。
6. 技术/AI 能力资料：官方模型文档、技术案例、论文、产品实践。

每个 query 必须标注目标：定位信息、用户证据、竞品证据、功能证据、视觉证据、AI 能力证据、商业/运营证据。
```

### 13.2 Evidence Extractor Prompt

```text
抽取证据时必须区分 fact、claim、interpretation、assumption。

每条证据必须包含：
- title
- url
- source_type
- retrieved_at
- summary
- related_claim
- confidence

涉及功能、页面、流程、体验、竞品对比、AI 功能时，必须额外抽取 visual_evidence：
- product
- screen_or_flow
- media_type
- source_url
- timestamp
- observed_feature
- related_claim
- confidence

不得把低可信来源中的用户评论或社媒观点写成确定事实。用户评论只能用于识别痛点、情绪、使用场景和假设。
```

## 14. 输出质量门槛

Deep 模式下，最终报告必须满足以下门槛。

| 质量项 | 最低要求 |
|---|---|
| 目标产品基础资料 | 至少 3 个来源，优先官方、应用商店、媒体或产品介绍 |
| 竞品数量 | 至少 3 个，覆盖直接竞品、间接竞品或替代方案 |
| 视觉证据 | 至少 5 条截图、视频、应用商店图、官网图或评测图 URL |
| 用户证据 | 至少 20 条用户评论或社媒讨论摘要；无法获得时必须说明缺口 |
| 功能体验路径 | 至少 1 条完整核心路径，覆盖进入、使用、反馈、留存或转化 |
| AI/新能力映射 | 至少 5 类能力或场景机会，每类说明价值和风险 |
| 机会矩阵 | 至少 5 个机会点，每个机会点评估价值、复杂度、证据和优先级 |
| 指标定义 | 核心指标必须给出定义、计算方式、数据来源和成功标准 |
| 置信度 | 每个关键结论必须标注 high、medium 或 low |
| 开放问题 | 证据不足、冲突结论和待验证假设必须单独列出 |

## 15. 示例：天天跳绳产品调研任务

当用户输入“调研天天跳绳产品用户人群和解决需求，基于天天跳绳 App 的产品定位，给出 AI 时代下的视野盲区和方向”时，Lapis 应按以下方式执行。

| 模块 | 执行要求 | 产出 |
|---|---|---|
| 目标产品基线 | 搜索天天跳绳官网、应用商店、媒体报道、产品介绍、用户评论 | 产品定位与现状表 |
| 用户人群 | 拆解儿童、家长、学校、教师、运动爱好者等角色 | 用户分层与 JTBD |
| 竞品图谱 | 不只找跳绳 App，还应找儿童运动、家庭健身、校园体育、AI 运动教练、智能硬件等产品 | 直接/间接/替代竞品地图 |
| 功能路径 | 分析训练进入、运动记录、动作反馈、激励、家长查看、复盘、分享等路径 | 核心路径与体验断点 |
| 视觉证据 | 保留应用商店截图、官网图、视频演示 URL、媒体评测图、社媒图片 URL | visual_evidence 表 |
| AI 能力 | 分析动作识别、姿态反馈、个性化计划、语音陪伴、成长报告、内容生成、赛事推荐等能力 | AI 能力映射表 |
| 视野盲区 | 对比当前产品能力与 AI 可改变的用户任务 | 盲区清单与战略判断 |
| 产品机会 | 评估用户价值、商业价值、复杂度、风险 | 机会矩阵与 Roadmap |
| 验证计划 | 设计实验和指标 | 激活、留存、路径完成率、付费转化等指标定义 |

最终结论应基于证据判断天天跳绳在 AI 时代的升级方向，而不是直接泛化为“做 AI 教练”或“做个性化推荐”。可接受的结论形式应包含：升级方向、理由、适用用户、功能形态、体验路径、商业价值、风险边界和验证方式。

## 16. 验收标准

Product Deep Research 业务层补充在以下条件下视为完成。

| 验收项 | 标准 |
|---|---|
| 模式识别 | 能识别产品/运营/竞品/AI 升级/PRD 前置研究任务，并进入 Product Deep Research 模式 |
| 维度拆解 | 能按 6 个业务维度拆解研究，不遗漏功能体验和产品机会 |
| Agent 分配 | 能根据任务选择 3+1 人格，具体产品深度调研默认启动 Product Experience Analyst |
| 证据覆盖 | 能覆盖官方、应用商店、视频、图片、用户评论、竞品、AI 能力等来源 |
| 视觉证据 | 能输出截图/视频/图片 URL、观察点和关联结论 |
| 功能体验 | 能输出功能架构、核心路径、体验断点和可复用设计模式 |
| AI 映射 | 能输出 AI/新能力与用户任务、产品现状、机会方向的映射 |
| 决策输出 | 能输出机会矩阵、Roadmap、验证实验和指标定义 |
| 置信度 | 能区分事实、判断、假设、风险和开放问题 |
| 报告可用性 | 最终报告可直接用于产品评审、PRD 前置研究或运营策略讨论 |

## 17. 建议文件变更

| 文件 | 建议变更 |
|---|---|
| `skills/deep-research.md` | 增加 Product Deep Research 触发条件、工作流和质量门槛 |
| `prompts/layer1/task-decomposition.md` | 增加研究意图识别和 MECE 6 维度拆解 |
| `prompts/layer1/agent-allocation.md` | 增加 3+1 人格与分配规则 |
| `prompts/layer1/final-report.md` | 增加 Product Deep Research 最终报告模板 |
| `prompts/layer2/aspect-agent.md` | 增加产品调研扩展字段 |
| `prompts/layer2/search-planner.md` | 增加产品研究证据类型和搜索策略 |
| `prompts/layer2/evidence-extractor.md` | 增加 visual_evidence 抽取规则 |
| `schema/report.rs` 或等价 schema | 可选增加产品研究字段，用于结构化传输与校验 |

## References

[1]: https://github.com/4o3F/Lapis/blob/main/docs/research-agent-product.md "Lapis Research Agent 产品文档"
[2]: 业务层补充—对Lapis架构的增量输入.docx "业务层补充—对 Lapis 架构的增量输入"
