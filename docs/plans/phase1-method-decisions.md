# Phase 1 计划草稿 · 方法预研（method decisions）

> Status: 草稿（待 Phase 1 启动时细化）。产出 = `docs/research/` 下的方法决策文档。

## 目标
为 PM DeepResearch 找到**真实可借鉴、科学**的方法论，回答下列**决策驱动问题**——每个产出"选定方法 + 依据(文献/真实实践案例) + 在 PM DeepResearch 的落地点"。**不是写文献综述**。

两大支柱，**产品方法论是目的，AI/编排方法论是手段**：
- **Track B｜产品专家真实方法论**（定义"好的产品研究产出长什么样"）—— 驱动 MECE 维度、报告结构、机会矩阵、"产品专家视角"。
- **Track A｜AI 编排 / 可信度方法论**（如何可靠、低幻觉地执行 Track B）。

## 防无界综述（R1 约束）
- 由决策问题牵引；与 Phase 2 交织（得到一个方法立刻拿业务需求检验值不值得用）。
- 每问题限定 source 数量与时间盒；够回答即停。**优先真实实践案例 + 权威框架原始出处**，不堆二手博客。
- **先验真伪**：用户给的 arxiv 示例 `2603.05344`/`2605.13357` 是未来日期 ID，第一步先核实是否真实存在再补充。
- **复用已有**：`docs/prompt-engineering-academic-foundations.md` 是前次 Phase 1（Track A）尝试的产出 —— 先 review 已覆盖什么、缺什么，补差不重来。

---

## Track B · 产品专家真实方法论（新增，先行）

| # | 决策问题 | 候选可借鉴方法论 / 真实实践（待验证取舍）| 落地点 |
|---|---|---|---|
| B1 | 真实产品专家/咨询机构**怎么做竞品深度研究**？哪些框架被验证有效 + 真实案例？| feature teardown / 能力矩阵 / 定位图 / JTBD-based competitive / Kano / Christensen JTBD&disruption / Porter & SWOT 的正确用法 | MECE 竞品维度、竞品报告结构、机会矩阵 |
| B2 | **优秀的产品需求/功能是怎么产出的**？| Product Discovery (Cagan/SVPG) · Continuous Discovery & Opportunity-Solution Tree (Teresa Torres) · JTBD/ODI (Ulwick) · User Story Mapping · Kano · RICE/价值-复杂度优先级 · PRD 最佳实践 | 需求/机会优先级方法、PRD/报告产出模板 |
| B3 | 什么让分析有**"产品专家味"**而非泛泛而谈？| 从 user task→功能路径→体验 gap 推导；证据驱动；权衡(trade-off)显性化；假设可证伪 | 研究人格(尤其 Product Experience Analyst / Strategist)的思维 prompt |

## Track A · AI 编排 / 可信度方法论

| # | 决策问题 | 要决策的 | 落地点 |
|---|---|---|---|
| A1 | 在 Lapis 已有逐字证据 provenance(byte-equal) 之上，还需哪些机制达到"可信度远超普通 LLM"？| 证据可信度模型(来源分级、交叉验证、引用粒度)| layer2 prompts + 可选 Rust schema |
| A2 | 哪些被验证有效的反幻觉技术(self-consistency / verification chain / abstention / citation-grounding / "宁少但真")适合注入？| 选 2-3 个落地 | layer1/layer2 prompts |
| A3 | 问题→研究维度的科学拆解方法(taxonomy / MECE 工程)如何**承载 Track B 的产品维度**？| MECE-6 最终定义+拆解依据 | task-decomposition.md |
| A4 | 多 agent 研究人格分工的有效性证据？3+1 人格是否最优？| 人格集合+分配规则 | agent-allocation.md（待建）|
| A5 | 如何按需求动态分配 agent 数/搜索预算/迭代深度？(plan-execute / iterative deepening 等)| 编排与预算策略 | skill + budget 配置 |

## 两支柱收敛
- B1/B2 产出 → **直接定义** MECE 维度与报告/机会矩阵模板；A3 用拆解科学**校验**其 MECE 性。
- B3 产出 → **直接定义**研究人格的"产品专家思维"；A4 用多 agent 有效性证据校验分工。
- A1/A2 → 保证上述产出**可信、可追溯、低幻觉**。

## 研究方法
- dogfooding：用 PM DeepResearch/Lapis 自身工具(grok/exa、deep_research) + 必要时 Layer 2 浏览器抓权威页/案例。
- 跨模型交叉(Claude/Codex/subagent)验证关键方法可信度。

## 退出标准
B1-B3 + A1-A5 各有"方法 + 依据(含真实案例) + 落地点"，无未解方法论阻塞 → 进入 Phase 2。

## 产出物
`docs/research/` 下按 Track/问题组织的方法决策文档。
