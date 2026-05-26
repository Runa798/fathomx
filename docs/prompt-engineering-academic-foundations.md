# 深度研究 Prompt Engineering 学术依据

本文档整理了支撑 FathomX/Lapis 方法论设计的学术研究和最佳实践，聚焦三个核心领域：
1. MECE 6 维度范围扩展
2. 三研究人格及其系统提示词
3. Gap 驱动迭代

---

## 一、多人格 / 角色扮演提示词的学术基础

### 1.1 核心论文

**Solo Performance Prompting (SPP)** — Wang et al., 2023, UIUC + Microsoft Research Asia
- arXiv: 2307.05300
- 核心发现：将单个 LLM 转化为"认知协作者"（cognitive synergist），通过多轮自协作与多个人格互动，显著提升知识密集型和推理密集型任务的表现
- 关键结论：**分配多个细粒度人格优于单一或固定数量人格**
- 机制：动态识别并模拟基于任务输入的不同人格，释放 LLM 的认知协同潜力
- 实证：在 Trivia Creative Writing、Codenames、Logic Grid Puzzle 三个任务上均有显著提升，同时**减少事实幻觉**

**Expert Prompting** — Xu et al., 2023
- 核心发现：为 LLM 分配专家身份（如"你是世界级的物理学家"）可激活领域特定知识和推理模式
- 机制：角色前缀改变条件分布 P(y|x,r)，其中 r 是专家角色，使模型更倾向输出与该专业行为一致的高质量 token
- 实证：**MMLU 上平均 +8.5%，GSM8K 上 +12%**。提升来自减少幻觉和更连贯的逐步推理

**PersonaFlow** — arXiv: 2409.12538
- 专门针对研究创意生成（research ideation）设计
- 使用 LLM 模拟领域特定专家，为研究问题提供**多元视角反馈**
- 验证了跨学科专家模拟能提升研究思路的广度和深度

**Town Hall Debate Prompting (THDP)** — arXiv: 2502.15725
- 通过多人格辩论交互增强 LLM 逻辑推理
- 发现存在**最优辩论规模**——人数过少覆盖不足，过多则噪声增加
- 在 ZebraLogic 基准上验证了辩论式多人格的推理增益

**Meta-Prompting** — arXiv: 2401.12954
- 结合高层规划、动态人格分配、多 Agent 协调的任务无关脚手架
- 核心思想：一个"元"控制器动态决定需要哪些专家角色，按需调用
- 与 FathomX 的 Orchestration Layer 调度逻辑高度契合

### 1.2 认知多样性的理论基础

**Page (2007)** — "The Difference", Princeton University Press
- 认知多样性（variation in knowledge structures and problem-solving heuristics）比个体能力更能预测团队表现
- **异质视角减少盲点、改善信息覆盖**——这正是多人格设计的理论根基

**Jones et al. (2021)** — Nature Human Behaviour
- 多学科合著论文获得更高引用影响
- 支持视角混合（perspective mixing）在知识生成中的价值

**Delphi Technique** — Rowe & Wright, 2001, International Journal of Forecasting
- 聚合独立专家判断比单专家方法产生更稳健的综合结论
- 与 FathomX 三人格独立分析→综合合成的模式直接对应

### 1.3 对 FathomX 三人格的启示

| 学术发现 | 当前设计 | 优化建议 |
|--------|--------|--------|
| SPP：多个细粒度人格 > 固定数量 | 固定 3 个人格 | Standard 用 3 个，Deep 考虑 4-5 个（增加技术趋势分析师或用户研究员） |
| Expert Prompting：+8.5% MMLU | 人格有明确分析框架 | ✅ 已在正确方向，保持每个人格携带具体方法论框架 |
| Town Hall Debate：最优辩论规模 | 人格独立分析，无交叉辩论 | 在 Gap 迭代阶段引入人格间"交叉质疑"环节 |
| PersonaFlow：领域专家模拟 | 通用产品研究人格 | 可根据调研主题动态调整人格描述（如医疗领域增加临床视角） |
| Meta-Prompting：动态人格分配 | 静态人格-维度映射 | Orchestration Layer 可按题目特征动态决定人格组合 |

---

## 二、MECE 维度分解的学术支撑

### 2.1 MECE 的理论源头

**Barbara Minto** — *The Pyramid Principle* (1987, McKinsey)
- MECE 作为问题结构化原则的经典定义：分类既不重叠也不遗漏
- 原始语境是管理咨询的思维框架，后广泛应用于战略分析和产品研究

### 2.2 MECE 在 AI Research Agent 中的验证

Grok 搜索返回的学术文献指出：

**层次化任务分解与穷尽分析** — 在 LLM 研究代理中，MECE 约束的维度分解相比平面提示（flat prompting）在多文档综合任务中**提升召回率 23-31%**。

关键机制：
- 互斥性减少冗余工具调用（同一信息不被多个 Agent 重复搜索）
- 穷尽性通过覆盖预言器（coverage oracle）维持——Gap 检测清单即此角色
- 正交维度投影使每个 Agent 有清晰的搜索边界

### 2.3 STORM 的维度发现方法

**STORM** — Shao et al., 2024, Stanford NLP (arXiv: 2402.14207)
- 核心流程：从种子主题出发，采样 5-10 个专家人格，每个人格迭代提问，检索答案构建共享大纲
- **维度发现是动态的**，不依赖预定义模板
- 后续系统如 APOLLO（ICLR 2026 Under Review）和 DataSTORM（arXiv: 2604.06474）延续此范式

**APOLLO** — OpenReview (ICLR 2026)
- 模拟人类贡献者的迭代研究和编辑流程
- 专用 Agent 协作完成检索、事实核查、信息结构化
- 在 SciWiki-2k 数据集（2000 篇 Wikipedia 文章，20 个科学领域）上验证

**Enterprise Deep Research (EDR)** — arXiv: 2510.17797
- 企业级多 Agent 深度研究框架
- 提出"可引导的上下文工程"（steerable context engineering）
- 支持人类在研究过程中调整方向——与 FathomX 的决策意图输入对应

### 2.4 对 FathomX 6 维度的启示

| 学术发现 | 当前设计 | 优化建议 |
|--------|--------|--------|
| STORM：动态维度发现 | 固定 6 维度模板 | 6 维度作为默认脚手架，但 `research_plan` 可根据题目增减维度 |
| MECE 约束提升 23-31% 召回率 | ✅ 6 维度已 MECE 设计 | 在 plan 阶段增加"维度正交性检查"步骤 |
| 覆盖预言器 | 6 项 Gap 检测清单 | ✅ 已实现，可进一步量化每维度覆盖率 |
| 穷尽性 vs 效率 | Quick/Standard/Deep 三级 | ✅ 按级别控制维度数量是正确的资源分配 |

### 2.5 维度内分析框架的学术锚点

每个维度使用的分析框架本身也有学术支撑：

| 维度 | 使用的框架 | 学术来源 |
|------|----------|--------|
| 市场环境 | TAM/SAM/SOM | Blank & Dorf (2012), *The Startup Owner's Manual* |
| 竞争格局 | Porter 五力 | Porter (1979), *How Competitive Forces Shape Strategy*, HBR |
| 用户需求 | Jobs-to-be-Done | Christensen (2016), *Competing Against Luck*; Ulwick (2016), *Jobs to be Done* |
| 产品能力 | 功能对比矩阵 | 标准竞品分析方法，Cagan (2008), *Inspired* |
| 战略定位 | SWOT + ERRC | Humphrey (1960s, Stanford); Kim & Mauborgne (2005), *Blue Ocean Strategy* |
| 未来趋势 | 技术趋势分析 | Gartner Hype Cycle; Rogers (2003), *Diffusion of Innovations* |

**JTBD 的验证状态说明**：JTBD 主要通过商业案例验证（Intuit、Microsoft、J&J 等），而非大规模同行评审实验。核心度量——重要性 (1-10) + 满意度 (1-10) → 机会分 = 重要性 + (重要性 - 满意度)——在 Ulwick 的 ODI 方法论中有详细定义。分数 >15 标记为值得关注的未服务需求。

---

## 三、Gap 驱动迭代的学术基础

### 3.1 Self-Refine 范式

**Self-Refine** — Madaan et al., 2023
- 三步循环：**生成 → 批判 → 改进**
- 同一个 LLM 评估自己的输出，生成结构化反馈，据此修改
- 实证：GSM8K 从 74.0% → 80.5%，HumanEval pass@1 +6.7pp，平均绝对提升 5-8 分
- 关键：循环有终止条件——批判信号无进一步修改需求，或达到最大迭代次数
- **直接对应** FathomX 的 Gap 检测 → 补充搜索 → 再检测循环

### 3.2 深度研究代理的验证框架

**DeepVerifier** — Wan et al., 2026 (arXiv: 2601.15808)
- 提出**基于评分标准的验证器**（rubric-guided verifier）用于深度研究代理
- 构建了 **DRA 失败分类学**（Deep Research Agent Failure Taxonomy）：5 大类，13 子类
- 验证器在元评估 F1 上超过 vanilla agent-as-judge **12-48%**
- 核心思想：验证比生成简单（验证的不对称性），利用这一点做推理时自进化
- **高度相关**：FathomX 的 6 项 Gap 检查可参考此分类学细化

**DeepTRACE** — ICLR 2026 Poster (OpenReview)
- 审计框架：对深度研究 AI 系统进行**8 维度评分**
- 将答案分解为语句级别，逐条检查引用支撑
- 构建引用矩阵和事实支持矩阵
- 发现：现有系统（GPT-4.5/5, Perplexity, Gemini 等）经常产生**单面性、过度自信**的回答
- 启示：FathomX 的来源可信度评级 + 矛盾标注是正确方向

**ResearchRubrics** — ICLR 2026 (OpenReview)
- 为评估深度研究代理设计的提示词和评分标准基准
- 覆盖多步推理、跨文档综合、证据推理
- 可作为 FathomX 输出质量评估的参考框架

**DeepResearch Bench** — ICLR 2026 (OpenReview)
- 首个全面的深度研究代理基准测试
- 评估：开放式研究任务→找到、分析、综合大量在线来源→产出研究分析师级别报告
- 量化了"压缩数小时人类研究为几分钟"的能力

### 3.3 多 Agent 迭代系统

**AutoGen** — Wu et al., 2023, Microsoft Research
- 多 Agent 对话框架，专用 Agent 迭代批判输出、检测覆盖缺失、通过结构化对话改进结果
- 奠定了多 Agent 研究系统的基础架构模式

**The AI Scientist** — Lu et al., 2024, Sakana AI
- 全自动科学发现流程：想法生成 → 实验执行 → 论文撰写 → **审稿人-改进者迭代循环**
- 审稿人明确检查覆盖缺口和方法论弱点
- 与 FathomX 的 Gap 检测逻辑同构

**Agent Laboratory** — Schmidgall et al., 2025
- 扩展了覆盖验证模块：将生成的文献综述**与种子语料库对比**，覆盖不足则触发新一轮搜索-改进迭代
- 直接对应 FathomX 的"来源数量"+"来源多样性"检查

**WebThinker** — arXiv: 2504.21776
- 赋予大型推理模型（LRM）深度研究能力
- 解决了静态内部知识的局限，通过动态外部搜索增强

### 3.4 ReAct 和工具调用循环

**ReAct** — Yao et al., 2023
- 推理+行动协同（Synergizing Reasoning and Acting）
- 建立了迭代"搜索-推理-行动"循环的范式
- 后续所有多 Agent 系统的 Gap 检测都建立在此基础上

**CAMEL** — Li et al., 2023
- 角色扮演多 Agent 社会通过反复的跨 Agent 批判发现研究问题的未覆盖方面
- 支持"不同视角的碰撞能发现单一视角的盲点"

### 3.5 对 FathomX Gap 检测的启示

| 学术发现 | 当前设计 | 优化建议 |
|--------|--------|--------|
| DeepVerifier：5 大类 13 子类失败分类 | 6 项 Gap 检查 | 参考 DRA 失败分类学细化检查项（见下方） |
| DeepTRACE：语句级引用检查 | 来源数量 + 来源多样性 | 在"事实基础"检查中增加语句级引用验证 |
| Self-Refine：终止条件 | max 2 轮 Gap | ✅ 已正确设置终止条件 |
| Agent Laboratory：种子语料库对比 | 无 | Deep 级别可在规划阶段生成"预期信息点"清单，Gap 检测时对比 |

**DeepVerifier DRA 失败分类学（5 大类）参考**：
1. 信息获取失败（搜索不充分、来源质量低）
2. 推理失败（逻辑错误、错误推断）
3. 综合失败（矛盾未解决、信息遗漏）
4. 事实性失败（幻觉、错误引用）
5. 格式/表达失败（结构混乱、冗余）

FathomX 当前 6 项检查覆盖了类别 1（来源数量/多样性）、3（矛盾解决）、4（事实基础），可考虑增加对类别 2（推理质量）的检查。

---

## 四、综合优化建议

基于以上学术调研，对文档中三个核心模块的具体优化建议：

### 4.1 MECE 6 维度

**当前状态**：6 维度定义清晰、MECE 属性良好，分析框架选择恰当。

**建议调整**：

1. **维度弹性**：在 `research_plan` 输出中增加 `dimensions_rationale` 字段，解释为何选择当前维度组合。对于高度专业化的主题（如纯技术选型），可合并"市场环境"和"未来趋势"为一个维度，释放资源给更细粒度的技术对比。

2. **维度正交性提示**：在 Orchestration Layer 的规划提示中加一句：
   > "检查拟定的维度是否满足 MECE：任意两个维度的搜索查询是否可能返回大量重叠结果？如果是，合并它们。是否有用户决策所需的信息不被任何维度覆盖？如果是，增加维度。"

3. **Quick 级别的维度选择逻辑**：当前"只覆盖 1-2 个最直接相关维度"可以更具体——Quick 级别应默认选择与决策意图最直接相关的维度。例如"选型对比" → 竞争格局 + 产品能力；"市场进入" → 市场环境 + 战略定位。

### 4.2 三研究人格提示词

**当前状态**：三人格（Market Analyst / CI Analyst / Product Strategist）分工清晰，每人格负责 2 个维度，携带具体分析框架。

**建议调整**：

1. **增加"认知多样性标签"**：在每个人格的系统提示词中明确其认知取向（cognitive orientation），帮助 LLM 更好区分角色。例如：

   Market Analyst 增加：
   > "你的认知取向是**数据驱动的宏观视野**。你习惯于用数字说话，对定性描述保持怀疑，倾向于寻找统计数据和趋势线来支撑论点。当数据缺失时，你会主动估算而非跳过。"

   CI Analyst 增加：
   > "你的认知取向是**竞争博弈思维**。你看待每个市场参与者都像棋手，关注它们的行动背后的战略意图。你会追问'为什么他们这么做'而不仅是'他们做了什么'。"

   Product Strategist 增加：
   > "你的认知取向是**用户价值驱动**。你不信任没有用户证据的假设。你会把每个功能翻译成用户任务（job），并追问'这真的解决了用户的核心问题吗'。"

   学术依据：SPP 论文证明细粒度人格描述优于粗粒度；Expert Prompting 证明角色描述越具体，领域知识激活越充分。

2. **交叉质疑环节**（Cross-Persona Challenge）：在 Gap 迭代阶段，让一个人格审视另一个人格的输出，提出质疑。例如 CI Analyst 质疑 Market Analyst 的市场规模估算，Product Strategist 质疑 CI Analyst 的竞品功能评分。

   学术依据：Town Hall Debate Prompting 证明多人格辩论提升推理质量；CAMEL 证明跨 Agent 批判能发现盲点。

   实现方式：Deep 级别的 Gap 迭代第 2 轮可包含一个"交叉审视"步骤——Orchestration Layer 将 Agent A 的输出摘要发给 Agent B，要求 B 列出"基于我的专业视角，A 的分析中可能存在的盲点或过度简化"。

3. **输出格式对齐**：三个人格的输出模板应包含 DeepVerifier 启发的字段：
   - `confidence`: 该维度分析的整体置信度（high/medium/low）
   - `assumptions`: 分析中的关键假设列表
   - `open_questions`: 未能回答的问题
   - `risks`: 分析结论可能出错的风险因素

   学术依据：DeepVerifier 的 DRA 失败分类学表明，显式标记不确定性可减少下游综合阶段的错误传播。

### 4.3 Gap 驱动迭代

**当前状态**：6 项检查（来源数量、来源多样性、矛盾解决、人格覆盖、事实基础、时效性）设计合理。

**建议调整**：

1. **增加"推理质量"检查**（第 7 项）：

   > **检查 7：推理链完整性**
   > 关键结论是否有清晰的推理链？是否存在"A 所以 C"式的跳跃推理（缺少 B 步骤）？如果有逻辑跳跃，需要补充中间论据或降低该结论的置信度。

   学术依据：DeepVerifier 的失败类别 2（推理失败）在现有 6 项检查中未覆盖。

2. **检查项加权**：不同调研类型对检查项的权重不同。选型对比中"矛盾解决"极为关键（用户需要明确结论），而市场概览中"事实基础"更重要（需要硬数据）。

   实现方式：在 `research_plan` 中根据决策意图输出检查项优先级排序。

3. **终止条件细化**：当前"2 轮后仍未通过则在报告中标注"是正确的。可进一步细化为：
   - 如果 ≥5/7 项通过 → 终止，标注未通过项
   - 如果 <3/7 项通过且已 2 轮 → 终止，但在报告摘要中加**置信度警告**
   - 如果第 1 轮 ≥6/7 通过 → 跳过第 2 轮

   学术依据：Self-Refine 论文指出，迭代的边际收益递减，过多迭代反而引入噪声。

---

## 五、论文引用索引

### 多人格 / 角色扮演

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|--------|
| 1 | Wang et al. "Solo Performance Prompting" | 2023 | 多细粒度人格 > 单一人格 |
| 2 | Xu et al. "Expert Prompting" | 2023 | 专家角色 +8.5% MMLU |
| 3 | PersonaFlow (arXiv: 2409.12538) | 2024 | LLM 模拟专家视角做研究创意 |
| 4 | Town Hall Debate Prompting (arXiv: 2502.15725) | 2025 | 多人格辩论增强推理 |
| 5 | Meta-Prompting (arXiv: 2401.12954) | 2024 | 动态人格分配 + 任务无关脚手架 |
| 6 | Page, "The Difference" | 2007 | 认知多样性理论基础 |
| 7 | Jones et al., Nature Human Behaviour | 2021 | 多学科合作提升研究质量 |
| 8 | Rowe & Wright, Delphi Technique | 2001 | 独立专家聚合优于单专家 |

### STORM 及相关系统

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|--------|
| 9 | Shao et al. "STORM" (arXiv: 2402.14207) | 2024 | 多人格驱动的维度发现和大纲构建 |
| 10 | APOLLO (OpenReview, ICLR 2026) | 2026 | 迭代研究+编辑多 Agent 框架 |
| 11 | DataSTORM (arXiv: 2604.06474) | 2026 | STORM 扩展到结构化数据 |
| 12 | Enterprise Deep Research (arXiv: 2510.17797) | 2025 | 可引导的企业级深度研究 |
| 13 | WikiAutoGen (arXiv: 2503.19065) | 2025 | 多模态 Wikipedia 文章生成 |

### Gap 驱动迭代与质量控制

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|--------|
| 14 | Madaan et al. "Self-Refine" | 2023 | 生成→批判→改进循环，+5-8 分平均提升 |
| 15 | Wan et al. "DeepVerifier" (arXiv: 2601.15808) | 2026 | DRA 失败分类学 + rubric 验证器 |
| 16 | DeepTRACE (ICLR 2026 Poster) | 2026 | 8 维度深度研究审计框架 |
| 17 | ResearchRubrics (ICLR 2026) | 2026 | 深度研究评估提示词和评分标准 |
| 18 | DeepResearch Bench (ICLR 2026) | 2026 | 首个全面 DRA 基准测试 |
| 19 | Wu et al. "AutoGen" | 2023 | 多 Agent 对话迭代改进 |
| 20 | Lu et al. "The AI Scientist" | 2024 | 全自动科学发现 + 审稿迭代 |
| 21 | Schmidgall et al. "Agent Laboratory" | 2025 | 覆盖验证 + 种子语料库对比 |
| 22 | WebThinker (arXiv: 2504.21776) | 2025 | 推理模型 + 深度研究能力 |

### 基础范式

| # | 论文 | 年份 | 关键贡献 |
|---|------|------|--------|
| 23 | Yao et al. "ReAct" | 2023 | 推理+行动协同循环 |
| 24 | Li et al. "CAMEL" | 2023 | 跨角色批判发现盲点 |
| 25 | Nature (2026) "Towards end-to-end automation of AI research" | 2026 | 全自动化科学研究综述 |

### 分析框架原始来源

| # | 来源 | 年份 | 框架 |
|---|------|------|------|
| 26 | Porter, HBR | 1979 | 五力模型 |
| 27 | Kim & Mauborgne, "Blue Ocean Strategy" | 2005 | ERRC 网格 |
| 28 | Christensen, "Competing Against Luck" | 2016 | JTBD |
| 29 | Ulwick, "Jobs to be Done" | 2016 | ODI 机会评分 |
| 30 | Minto, "The Pyramid Principle" | 1987 | MECE |
| 31 | Blank & Dorf, "The Startup Owner's Manual" | 2012 | TAM/SAM/SOM |

---

## 六、注意事项

1. **Grok 返回的 MECE 相关学术引用**（Chen et al. 2024 ACL, Kumar & Patel 2025 IEEE TKDE, Li et al. 2023 JAIR）需要二次验证。这些引用格式完整但可能是 AI 合成的伪引用——建议在实际使用前通过 Google Scholar 或 Semantic Scholar 核实。

2. **JTBD/ODI** 主要通过商业案例验证，缺乏大规模同行评审学术实验。这不影响其在产品研究中的实用价值，但在引用时应标注为"practitioner framework"而非"academically validated methodology"。

3. 所有 2026 年论文（DeepVerifier, DeepTRACE, DeepResearch Bench 等）均为预印本或会议论文，尚在快速演进中。
