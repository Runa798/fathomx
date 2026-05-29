# M4-3 Rubric 打分：引擎实跑报告 vs 手写黄金样例

> 对象：`.m4-run/golden-report-strava.md`（Lapis deep_research 6/6 实跑 → final-report.md 装配，2026-05-30）
> 基线：`docs/evaluation/golden/running-coach-ai-upgrade.md`（Phase 2 手写黄金样例，22/24）
> Rubric：`docs/evaluation/rubric.md`（3 组 × 12 维，0/1/2）
> **关键意义**：这是第一次用**真引擎 + 人格 prompt 承载**端到端产出，检验方法论是否真能被 prompt 扛住，而非靠人手写。

## 总分：22 / 24（floor 全过，行文 floor 过，无捏造来源）

| # | 维度 | 黄金(手写) | M4(引擎) | 依据 |
|---|---|:---:|:---:|---|
| A1 | 引用充分性 | 2 | **2** | Ch1/4/5/6/9/10 关键声明均挂 `finding`/`ev` 引用；估计值标 estimated |
| A2 | 引用准确性/忠实性 | 2 | **2** | 抽样核验：收购事实←frontofficesports✓；能力矩阵每格←App Store/官页✓；解释类均标 medium |
| A3 | 无支撑率 | 2 | **2** | 事实性裸断言极少；推断/估计全部标注，不冒充事实 |
| A4 | 来源质量与多样性 | 2 | **1 ↓** | **build-cost aspect 仅 2 条证据**（<每维≥3）——预算 max_search_calls=2 所致，非方法缺陷 |
| A5 | 置信度校准+TM-4 | 2 | **2** | 全篇 medium + 逐项 evidenced/estimated；§12.4 自验证记录 |
| B1 | 五维骨架覆盖 | 2 | **2** | Job&竞争集/能力矩阵/Kano/ODI/定位白地 5 维全 + build-cost 第 6 维 |
| B2 | 真实竞争集 JTBD | 2 | **2** | job statement + LLM/人类教练等非显性替代 + 纳入理由 |
| B3 | 能力矩阵带证据 | 1 | **2 ↑** | **每格带 per-cell `evidence_refs` 或 assumption+falsifiable_test**（`capability:finding-1`）——补上了黄金样例的头号待办 |
| B4 | ODI/Kano 严谨 | 2 | **2** | 完整公式 `Imp+max(0,Imp−Sat)` + Kano 叠加 + estimated 标注 |
| C1 | 视觉证据 | 1 | **1** | 3 条 URL 级（<5），但缺口显式标注且 UI 强结论已 abstain（Ch7/§12.4） |
| C2 | 专家思维动作 TM | 2 | **2** | TM-1/2/3/4/5/6/7/8/9/11/12/13 系统体现 |
| C3 | 可落地 | 2 | **2** | Ch9 机会矩阵(价值/复杂度/证据/优先级) + Ch10 Roadmap + Ch11 实验指标；复杂度用竞品迭代节奏校准 |
| | **合计** | **22** | **22** | |

Floor（A1–A5/B1/B3/C1/C3）全部 ≥1 ✓ · 行文 floor（§7.4 论点先行/标题即论点/表格作证据/主题综合/命名中心思想"社交图谱日教练"/吸收反论/校准不确定/行动收尾）✓ · 一票否决（捏造来源）未触发 ✓

## 与黄金样例的差异画像（同分不同形）

引擎产出和手写样例同为 22/24，但**扣分点完全不同**，且方向有意义：

- **B3 从 1→2（提升，最重要信号）**：黄金样例扣在"矩阵符号化、无 per-cell 证据 id"——这是 rubric 第 70 行明确列的头号改进项。引擎产出的 `capability:finding-1` 直接给出每格 `evidence_refs`/`assumption`/`falsifiable_test` 的 fenced JSON，**人格 prompt 把 per-cell grounding 这件原本要人手补的事扛住了**。这正是 Phase 3 退出标准 3（方法论可被 prompt 承载）最强的正向证据。
- **A4 从 2→1（下降，但是预算 artifact 而非方法缺陷）**：build-cost-version-history aspect 只拿到 2 条证据，低于"每维 ≥3"。根因是 `max_search_calls=2` 的预算设定，不是 prompt 不会找源——把该 aspect（或全局）的 `max_search_calls` 提到 3–4 即可修复。属可调参数，不需改 prompt。
- **C1 仍为 1（持平）**：3 条视觉 URL <5。这是已知结构限制：deep_research 不内置 Layer-2 浏览器抓图；rubric 第 70 行已写明"Deep 模式实抓 ≥5 截图"需在 Skill 层补。引擎已正确 abstain（不靠想象写 UI 结论），符合预期。

## 承载稳定性结论

1. **方法论由 prompt 承载，在真引擎上稳。** 6 个 aspect 全部产出结构化 ODI 表 / 能力矩阵 / Kano / 价值曲线 / Christensen 威胁分级 / build-cost 版本线 / 体验路径矩阵 + 视觉块；TM-1~13 系统出现；evidence 字节级 provenance 通过校验；`supports_findings` 双向不变式在订正 prompt 后通过。
2. **B3 的提升证明"per-cell 证据"可以靠 prompt 强制，不必人手补**——这是相对黄金样例的实质进步。
3. **唯二的非满分项都是已知、可解释、非方法缺陷**：A4=预算（提 search 配额可修）、C1=结构（需 Skill 层 Layer-2 抓图，已在 roadmap）。
4. **不需要再给上游 4o3F 提方法论需求。** 引擎已能承载 PM 方法论；剩余两点都在 Skill 层（搜索预算、Layer-2 抓图）解决，与 Lapis 引擎无关。已提的工程 issue（#8 SSE 上限）仍是唯一阻塞性上游需求。

## 建议的后续微调（Skill 层，非引擎）
- 把 build-cost / 关键 aspect 的 `max_search_calls` 提到 3–4，回补 A4。
- Deep 模式接 Layer-2 浏览器抓 ≥5 张实图，回补 C1（agent-allocation.md 已注明此为外部步骤）。
