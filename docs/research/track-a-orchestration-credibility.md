# Track A · AI 编排 / 可信度方法论 — 方法决策

> Status: Phase 1 主体完成（2026-05-29）。回答 A1-A5，每条给出**选定方法 + 依据 + 落地点**。
> 来源全部过 [`citation-audit.md`](citation-audit.md)。早期素材见 [`../prompt-engineering-academic-foundations.md`](../prompt-engineering-academic-foundations.md)（已修正捏造引用）；
> 预算/可信度补差证据见 `_raw/a-verify-and-budget.md`。
>
> **定位**：Track A 是「手段」——保证 Track B 的产品研究产出**可信、可追溯、低幻觉**。这是 fathomx「可信度远超普通 LLM」承诺的实现层。

---

## A1 · 在 Lapis 逐字证据 provenance 之上，还需哪些机制达到"可信度远超普通 LLM"

### 决策结论

四层证据可信度机制（Lapis 已提供 byte-equal provenance 作为最底层）：

1. **来源分级（4 tier）**——摄入证据时即打标：
   - Tier 1：同行评审论文/会议（arxiv 须**确认录用状态**，非"under review"/desk-rejected）、权威数据库。
   - Tier 2：官方文档、一手工程博客（具名作者，如 Anthropic/OpenAI/Google）、政府/机构报告。
   - Tier 3：可靠新闻与二手分析（注日期，标二手）。
   - Tier 4：无日期网页/匿名/无一手出处的 LLM 摘要/未录用投稿 → **flag 人工复核**。
2. **原子声明核验（FActScore 范式）**：报告关键结论拆成原子声明，逐条对照其引用源核验。
3. **语句级引用审计（DeepTRACE 8 维）**：不止文档级——核到语句级。生产级深研系统引用准确率仅 40–80%，故必须显式审计。
4. **引用忠实性 ≠ 正确性（CiteEval）**：高达 57% 引用是"事后合理化"——引用存在不够，**声明必须真能从被引源推出**。

### 依据
- DeepTRACE（arXiv 2509.04499，ICLR 2026 Poster，MSR）：8 维审计（答案维：置信/单面性；来源维：数量/质量；引用维：充分性/准确性/无支撑率/必要性）。
- FActScore（arXiv 2305.14251，EMNLP 2023）：原子事实分解核验，RAG 事实性评估标准做法。
- CiteEval（ACL 2025）+ "Correctness is not Faithfulness"（SIGIR ICTIR 2025）。
- 信息素养框架 SIFT（Caulfield 2019）/ CRAAP 作为快速横向阅读补充。

### 落地点
Layer1/Layer2 prompts（来源分级与引用规则）+ 可选 Rust schema（机器强校验来源 tier 字段）。与 Track B 的 **TM-4 认识论标注**直接咬合。

---

## A2 · 注入哪些被验证有效的反幻觉技术

### 决策结论
落地 3 个，优先级从高到低：
1. **citation-grounding + abstention（宁少但真）**：无可靠来源时**宁可弃权/标"未找到"**，不编。这是 fathomx 最核心的反幻觉姿态，也是本项目第一天就该自我执行的（见 citation-audit 对自身的清洗）。
2. **verification chain（DeepVerifier rubric 验证器）**：用"验证比生成简单"的不对称性，对深研产出做 rubric 引导的自验证。
3. **self-consistency / self-refine 的有限迭代**：Gap 检测→补充→再检测，但**有终止条件**（边际收益递减，过多迭代引噪）。

### 依据
DeepVerifier（arXiv 2601.15808）DRA 失败分类学 + rubric 验证器（元评估 F1 超 vanilla agent-as-judge）；Self-Refine（Madaan 2023，+5–8 分但有终止条件）；SPP（2307.05300）报告多人格自协作"减少事实幻觉"。

### 落地点
Layer1/Layer2 prompts；gap 检测清单；quality floor（≥N 通过才出，否则报告标置信度警告）。

---

## A3 · 问题→研究维度的科学拆解如何承载 Track B 的产品维度

### 决策结论
- MECE 工程的收益按**机制**陈述（互斥减少冗余工具调用；穷尽由"覆盖预言器"=gap 清单维持；正交维度给每 agent 清晰搜索边界）——**不假托任何捏造的量化结论**（原"23-31%"已删，见审计）。
- **维度弹性**：B1 五维 / MECE-6 是默认脚手架，`research_plan` 阶段做"维度正交性检查"，可按题目增减。
- 用 A3 的拆解科学**校验** B1/B2 维度的 MECE 性（任意两维搜索是否大量重叠？决策所需信息是否有维度覆盖？）。

### 依据
STORM（2402.14207）动态维度发现；Meta-Prompting（2401.12954）任务无关脚手架 + 动态人格分配；Minto《金字塔原理》MECE 原始定义。

### 落地点
`prompts/layer1/task-decomposition.md`（强制产品 MECE）。

---

## A4 · 多 agent 研究人格分工的有效性证据；人格集合

### 决策结论
- 多细粒度专家人格 > 单一/固定，有实证支撑 → 支持 Track B 把 13 条 TM 编码进**专业人格**。
- 人格**思维 prompt** 用 B3 的 TM 填充；最终人格**数量**结合首攻"竞品研究"在 Phase 3 定（候选：Product Experience Analyst + Product Strategist + 跨人格质量门；是否加 Market/CI Analyst 待定）。
- 可选增强：Gap 迭代阶段引入"跨人格质疑"（Town Hall Debate / CAMEL 证明多视角碰撞发现盲点），但注意**最优辩论规模**，人多反增噪。

### 依据
SPP（2307.05300，细粒度多人格 + 降幻觉）、Expert Prompting（专家角色激活领域知识）、PersonaFlow（2409.12538，LLM 模拟专家视角做研究创意）、Town Hall Debate（2502.15725，有最优规模）、Delphi（独立专家聚合优于单专家）。

### 落地点
`prompts/layer1/agent-allocation.md`（待建）+ 各人格 prompt。

---

## A5 · 如何按需求动态分配 agent 数 / 搜索预算 / 迭代深度

### 决策结论
**先估难度 → 再分预算 → 执行中按信息增益门控**，分级：

| 场景 | subagent 数 | 工具调用 | 说明 |
|---|---|---|---|
| 简单事实 | 1 | 3–10 | 单 agent |
| 对比/选型 | 2–4 | 各 10–15 | 默认并行扇出 3–5 |
| 复杂深研 | 10+ | 分职责 | 仅当任务价值能 justify ~15× token 成本 |

关键启发式：
- **token 用量解释 ~80% 性能方差**；但**升级模型 > 翻倍 token 预算**（更高效的杠杆）。
- 每 subagent 内**3+ 工具并行**可省时高达 90%。
- **先估难度再路由**（DAAO）；树状研究**按信息增益门控**扩展、实时剪枝低价值分支（ParallelResearch，~5× 加速）；阶段预算用 water-filling（ZEBRA）；子问题级预算（Plan-and-Budget，+70% 准确 / −39% token）；**动作级预算**控制（何时检索/分解/直接作答，避免过度搜索）。
- 不适合多 agent：编码类、需全程共享上下文的任务。

### 依据
Anthropic《How we built our multi-agent research system》(2025-06-13，一手数据：3–5 并行、4×/15× 成本、80% 方差)；Anthropic《Building Effective Agents》(2024-12，"用最简够用方案")；DAAO (2509.11079, WWW 2026)；ParallelResearch (2510.05145)；ZEBRA (2605.20485)；Plan-and-Budget (2505.16122)；Inference-Time Budget Control (2605.05701)；Enterprise Deep Research (2510.17797)；用户示例 harness 论文 2603.05344 / 2605.13357（agent 运行基底/脚手架工程）。

### 落地点
skill 编排逻辑 + budget 配置（Lapis 已有 budget 字段：timeout_ms/搜索调用数等）。

---

## 退出标准对照（A 部分）

| 决策问题 | 方法 | 依据 | 落地点 | 状态 |
|---|---|---|---|---|
| A1 证据可信度 | 4-tier 来源分级 + 原子核验 + 语句级引用审计 + 忠实性 | DeepTRACE/FActScore/CiteEval | layer prompts + 可选 schema | ✅ |
| A2 反幻觉 | abstention(宁少但真) + verification chain + 有限 self-refine | DeepVerifier/Self-Refine/SPP | prompts + quality floor | ✅ |
| A3 MECE 工程 | 机制性收益 + 维度弹性 + 正交校验 | STORM/Meta-Prompting/Minto | task-decomposition.md | ✅ |
| A4 多人格 | 细粒度专家人格 + 可选跨人格质疑 | SPP/Expert/PersonaFlow/THDP | agent-allocation.md(待建) | ✅(数量待 Phase3 定) |
| A5 动态预算 | 难度估计→分级预算→信息增益门控 | Anthropic 多 agent 博客 + 5 篇预算论文 | skill + budget 配置 | ✅ |

> A4 人格"数量"留到 Phase 3 结合首攻能力定，不构成 Phase 1 方法论阻塞。
