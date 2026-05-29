# Track B · 产品专家真实方法论 — 方法决策

> Status: Phase 1 主体完成（2026-05-29）。本文件回答 B1-B3 三个决策问题，每条给出
> **选定方法 + 依据（含真实案例）+ PM DeepResearch 落地点**。全部来源已过 [`citation-audit.md`](citation-audit.md)。
> 完整证据与逐源 URL 见 `_raw/b1-competitive-research.md`、`_raw/b2-requirement-methodology.md`、`_raw/b3-product-expert-thinking.md`。
>
> **定位**：Track B 是「目的」——它**直接定义**「好的产品研究产出长什么样」。Track A（手段）保证这些产出可信、可追溯、低幻觉。

---

## B1 · 真实产品专家/咨询机构怎么做竞品深度研究

### 决策结论

竞品深度研究采用**五维 MECE 主干**，每维绑定一个被验证有效的方法、并强制证据标准。这五维构成 PM DeepResearch **「竞品深度研究」能力（v2.0 首攻）的报告骨架**：

| # | 维度 | 主用方法 | 证据标准 | 落地点 |
|---|---|---|---|---|
| 1 | **Job 与真实竞争集** | JTBD（Christensen/Moesta switch interview）| 明确 job statement + 找出非显性替代者 | 报告开篇"谁是真正的对手"；重构分析单元 |
| 2 | **能力对位矩阵** | Feature teardown（12 维评分 rubric）| 每格 1–5 分 + **必须附证据**（截图/评论数/步数）| "功能版图"，竞品报告的事实底座 |
| 3 | **功能重要性分级** | Kano 模型（唯一学术验证）| 每竞品每功能标 Must-be/Performance/Attractive | "什么才真正影响用户"，叠在矩阵上 |
| 4 | **竞争缺口打分** | ODI Opportunity Algorithm | Importance + max(Imp−Sat,0) → 排序机会清单 | **机会矩阵的直接打分逻辑** |
| 5 | **定位与白地** | Strategy Canvas / 感知图 | buyer-validated 轴、画 value curve、标白地 | "竞争定位图"，每份竞品报告的可视化产物 |

**支撑层（非 MECE 核心，但标准报告段落）**：
- 威胁分级（Christensen 颠覆理论）→ 每竞品标"维持性 vs 颠覆性"威胁。
- 市场结构语境（Porter 五力）→ **仅行业层、可选**；明确**禁止在产品层误用**。
- 战略小结（SWOT）→ **仅作沟通层**，在证据收齐后用，且每格转成带证据的具体含义；不作发现工具。
- 竞品速写（Cagan 3 强项 / 3 弱项）→ 每个竞品 profile 的快速开头。

### 关键依据（真实案例）

- **JTBD 重构竞争集**：Christensen 奶昔案例（真正对手是香蕉/百吉饼/无聊，非其它奶昔）。ODI 量化版的 **Cordis 案例**：心脏支架"最小化再闭塞概率"未满足缺口 → 市占 1%→20%，J&J 以 $109/股收购（一手 Strategyn + 公开并购记录交叉佐证）。
- **Kano 是唯一学术验证**的功能分级框架（Witell et al. 2013 综述了 1984–2012 的 147 篇）。GitLab 对 12 个候选功能跑过正式 Kano 调研（GitLab Handbook，可核实）。
- **Porter 五力被系统性误用**：它是**行业结构**工具，不是产品工具；在产品竞品分析里出现几乎都是误用 → PM DeepResearch 显式排除出核心。
- **SWOT 是沟通工具不是分析工具**（Hill & Westbrook 1997，研究 50 家英国公司发现 SWOT 产出极少转化为可行动战略）。Reforge 的 Sachin Rekhi「Connected」案例展示了替代物：**风险优先**竞品分析（先问"什么会杀死这个策略"）。
- **真实 teardown 范式**：Loom（异步视频，新市场颠覆，$975M 被 Atlassian 收购）、Facebook vs MySpace（"管理真实社交关系" vs "向陌生人表达身份"两个不同 job）。

### 与既有 wiki 规格的关系（需 Heye 确认，见文末）

既有业务 wiki 定义了产品研究的**通用 MECE-6**（市场/用户-JTBD/竞争/产品体验/商业增长/未来）。本 B1 的五维是**「竞争」这一能力的内部主干**，不是替换 MECE-6。建议：竞品深度研究能力以 B1 五维为报告骨架；MECE-6 仍是跨能力的顶层维度集。

---

## B2 · 优秀的产品需求/功能怎么产出

### 决策结论

1. **机会优先级**：以 **ODI Opportunity Score 为主排序** + **Kano 类型叠加**。
   - 理由：ODI 是唯一有**数学化、客户数据驱动**公式的框架（`Importance + max(0, Importance − Satisfaction)`，1–10 分；>10=未充分服务，<7=过度服务）；RICE 是团队内部估算（"披着数学外衣的猜测"）。Kano 叠加补上机会**类型**：Must-be=卫生/风险项，Attractive=差异化下注——混进单一 RICE 分会丢失这个关键区分。
   - **RICE / WSJF 作为备选**：无客户调研数据时用 RICE（团队 backlog 排序）；强时间敏感/风险削减场景用 WSJF（Reinertsen 的 Cost of Delay 是最有理论根基的）。
2. **需求深度调研报告模板**（8 段，全部锚定可核实一手来源）：
   1. **Press Release Frame**（Amazon PR-FAQ 风格，≤300 字）——先讲价值再讲功能。
   2. **机会验证**：JTBD statement + ODI 前 5 desired outcomes（Imp|Sat|Opportunity Score）+ Kano 分级 + Opportunity Landscape。
   3. **风险评估**（Cagan 四大风险）：价值/可用性/可行性/商业可行性，每项给证据等级（高/中/低）+ 来源。
   4. **解空间**（Torres OST）：每个目标机会 ≥3 个候选方案 + 最危险假设清单 + 既有/竞争方案。
   5. **需求**：功能需求（outcome 语句，标 Kano 类型）+ 非功能需求 + 非目标。
   6. **成功度量**：主指标（leading）+ 次指标 + 护栏指标。
   7. **证据与来源**：一手/二手（只用真实 URL）+ 每条声明置信度。
   8. **未决问题与下一步**。

### 关键依据（真实案例 + 验证状态）

- **ODI 公式与 Cordis 案例**：一手出处 marketingjournal.org (Ulwick 2017) + HBR 2002；案例市占 1%→20%。⚠️ Ulwick 自报"86% 成功率"**未经独立验证**，按 practitioner claim 标注。
- **Torres OST**（outcome→opportunity→solution→assumption test 四层）：一手 producttalk.org；Grailed LTV +20% 案例可核实。
- **Cagan 四大风险**（价值/可用性/可行性/商业可行性，PM/设计/技术分担）：一手 svpg.com/four-big-risks。Amazon Prime/Kindle 用 PR-FAQ + six-pager 作 discovery 产物。
- **Kano 1984 原始论文**（学术验证，J-STAGE 元数据核实）。
- **Amazon PR-FAQ**：Bryar & Carr《Working Backwards》(2021) + aboutamazon.com 一手。
- **RICE**：Sean McBride/Intercom 2016 一手；**WSJF**：Reinertsen 2009 + SAFe。
- ⚠️ "Value-vs-Effort 2×2" 无可追溯一手出处；iPhone pinch-to-zoom 作 Kano Attractive 是事后 practitioner 诠释，非已发表 Kano 研究——均按此标注。

---

## B3 · 什么让分析有"产品专家味"而非泛泛而谈

### 决策结论

把资深产品专家的**思维动作**显式编码进研究人格 system prompt。共 **13 条 Thinking Moves（TM）**，全部可追溯到真实产品思想家。其中 **TM-4（认识论状态标注）与 TM-11（可证伪/"我哪里错了"）是跨人格的质量门**，注入每个人格；其余按两个核心人格分配：

**Product Experience Analyst（用户/体验/证据）**：
- **TM-1 Job→Feature→Gap**：评估任何功能前先定位它服务的 user job（situation/motivation/outcome），再追 job→现有功能路径→体验 gap，按"填补 gap 的程度"赋权。（最高杠杆，直接把"功能点评"升级为"功能必要性分析"）
- **TM-2 metrics-informed 而非 metrics-driven**：指标是判断的输入不是结论；每个量化发现配定性解读。
- **TM-6 听弦外之音**：显式记录用户**没说/没要/用行为而非语言表达**的东西（Horowitz"吵车要的不是更响音响而是更安静的车"）。
- **TM-10 5Qs 测试**、**TM-12 言行分离**（访谈≠行为数据，冲突要点名并推理）。

**Product Strategist（战略/权衡/前瞻）**：
- **TM-3 四风险去险**：任何推荐须覆盖价值/可用性/可行性/商业可行性，缺一即不完整。
- **TM-5 显性权衡**：每个战略选择写出代价"选 X = 在 [时段] 内显式放弃 Y"。
- **TM-7 影响层级**：执行失败别止于执行，往下挖战略/激励/文化根因。
- **TM-8 pre-mortem**：假设 12–18 月后已失败，列三大最可能死因（Tigers/Paper Tigers/Elephants）。
- **TM-9 杠杆点**：区分 10x 乘数项 vs 加法项 vs overhead（Doshi LNO）。
- **TM-13 面向市场的未来**：把分析锚在市场/技术/竞争的**前进轨迹**上，纯现状分析须标"时效受限"。

**跨人格质量门（注入所有人格）**：
- **TM-4 认识论状态标注**：每条重要声明标 (a) 有实证—附来源 / (b) 专家观点—注出处 / (c) 假设—给可证伪版 / (d) 推测—显式标注。**这是 PM DeepResearch 可信度使命的提示词级落点。**
- **TM-11 可证伪**：每个主要结论附最强反论 + 写出"什么条件下它是错的"。

### 关键依据

来源全部一手核实（Cagan/SVPG、Shreyas Doshi 多条 Twitter thread+Substack、Julie Zhuo Medium/a16z、Ben Horowitz a16z 1998/2012、Lenny Rachitsky）。少数仅二手佐证的（Saffo "strong opinions weakly held" 原文未取到、Lenny 付费墙内容）已在 _raw/b3 的核验表标注。

---

## 两支柱收敛（Track B → 交给 Track A 校验）

- B1 五维 + B2 报告模板 → 由 **A3（MECE 工程）** 校验维度正交性与穷尽性。
- B3 的 13 条 TM → 由 **A4（多人格有效性证据）** 校验人格分工；TM 与 SPP/Expert Prompting 的"细粒度专家人格"主张一致。
- 全部产出的真实性 → 由 **A1/A2（证据可信度 + 反幻觉）** 兜底：TM-4 标注 + 来源分级 + 原子声明核验。

## 退出标准对照（B 部分）

| 决策问题 | 方法 | 依据(含真实案例) | 落地点 | 状态 |
|---|---|---|---|---|
| B1 竞品研究法 | 五维 MECE + 各维主用方法 | JTBD/Cordis、Kano/GitLab、Loom、Rekhi 风险优先 | 竞品报告骨架 + 机会矩阵 | ✅ |
| B2 需求/功能法 | ODI 主排序 + Kano 叠加；8 段模板 | ODI/Cordis、Torres/Grailed、Cagan、Amazon PR-FAQ | 需求深研报告模板 + 优先级模块 | ✅ |
| B3 产品专家味 | 13 条 Thinking Move + 人格分配 | Cagan/Doshi/Zhuo/Horowitz 一手 | 研究人格 thinking prompt | ✅ |

---

## 产品判断 — ✅ 已确认（2026-05-29，见 [ADR-0006](../decisions/0006-phase1-method-decisions.md)）

1. **竞争维度与 MECE-6 的关系**：✅ 认可分层——竞品能力用 B1 五维作报告骨架，MECE-6 为跨能力顶层维度集。
2. **研究人格集合**：✅ 按 B3 新判断——2 核心人格（Experience Analyst / Strategist）+ 跨人格质量门；Market/CI 不强制保留，最终数量 Phase 3 结合首攻能力定。
3. **ODI 数据来源**：✅ 接受——无一手问卷时允许用研究证据/市场代理估算，但**必须以 TM-4 显式标注证据等级**。
