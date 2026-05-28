# Phase 1 引用真伪审计（Citation Audit）

> Status: 完成（2026-05-29）。本文件是 Phase 1 方法预研所有关键引用的**逐条真伪核验记录**。
> 它本身就是 fathomx「可信度远超普通 LLM、大量降低幻觉」核心价值的一次自我演练——
> 我们对自己方法论的学术依据，先验真伪、再引用。

## 核验方法

1. **arxiv 逐 ID 核验**：直接打 arxiv 官方 API（`https://export.arxiv.org/api/query?id_list=<id>`），
   比对返回的标题/发表日期，确认论文真实存在且标题与引用一致。这是 byte-level 的事实核对，不依赖任何 LLM 转述。
2. **二手/非 arxiv 引用交叉核验**：用 grok + exa 跨 IEEE Xplore / ACL Anthology / JAIR / Google Scholar / OpenReview 检索；
   对会议论文额外核验**录用状态**（accepted vs desk-rejected vs under-review）。
3. **真实案例核验**：要求每个「真实实践案例」可追溯到一手出处 URL；无法追溯的标记为不可用。

## 结论速览

- ✅ **21 个 arxiv ID 全部为真**（含用户给的两个示例 2603.05344 / 2605.13357，及多篇 2026 未来日期论文）。
- ❌ **发现并清除 1 处捏造统计 + 3 个不存在的引用**（"MECE 提升召回率 23-31%"）。
- ⚠️ **1 篇被错标为 ICLR 2026 的论文实际被 desk-reject**（APOLLO）——降级处理。
- ⚠️ **2 个被 Grok 合成的"真实案例"无法追溯**（Stripe/Adyen、Notion/Coda teardown）——弃用。
- ⚠️ 多个 practitioner 自报数据（如 ODI 86% 成功率）——保留但显式标注「未经独立同行评审」。

---

## 表 1 · arxiv 论文（全部核实为真）

| arxiv ID | 发表 | 标题（简） | 用途 |
|---|---|---|---|
| 2307.05300 | 2023-07 | Solo Performance Prompting (SPP) | A4 多人格 |
| 2409.12538 | 2024-09 | PersonaFlow | A4 专家视角研究创意 |
| 2502.15725 | 2025-01 | Town Hall Debate Prompting | A4 多人格辩论 |
| 2401.12954 | 2024-01 | Meta-Prompting | A4/A5 动态人格分配 |
| 2402.14207 | 2024-02 | STORM (Wikipedia-like articles) | A3 维度发现 |
| 2604.06474 | 2026-04 | DataSTORM | A3 STORM 扩展 |
| 2510.17797 | 2025-10 | Enterprise Deep Research | A5 可引导编排 |
| 2503.19065 | 2025-03 | WikiAutoGen | 多模态生成 |
| 2601.15808 | 2026-01 | DeepVerifier（Inference-Time Scaling of Verification）| A1/A2 rubric 验证 |
| 2504.21776 | 2025-04 | WebThinker | A5 推理模型+深研 |
| 2603.05344 | 2026-03 | Building Effective AI Coding Agents for the Terminal | A5 harness/scaffolding（用户示例）|
| 2605.13357 | 2026-05 | AI Harness Engineering | A5 agent runtime substrate（用户示例）|
| 2509.04499 | 2025-09 | **DeepTRACE**（8 维深研审计）| A1 引用可信度审计 |
| 2511.07685 | 2025-11 | **ResearchRubrics** | 评测 rubric 基准 |
| 2506.11763 | 2025-06 | **DeepResearch Bench** | 深研 agent 基准 |
| 2509.11079 | 2025-09 | DAAO（难度感知编排）| A5 动态预算 |
| 2510.05145 | 2025-10 | ParallelResearch（树状自适应资源）| A5 信息增益门控 |
| 2605.20485 | 2026-05 | ZEBRA（零样本预算分配）| A5 阶段预算 |
| 2505.16122 | 2025-05 | Plan-and-Budget | A5 子问题预算 |
| 2305.14251 | 2023-05 | FActScore | A1 原子事实核验 |
| 2605.05701 | 2026-05 | Inference-Time Budget Control for LLM Search Agents | A5 动作级预算 |

> 注：DeepTRACE / ResearchRubrics / DeepResearch Bench 三篇此前在 `prompt-engineering-academic-foundations.md` 中仅标为
> "OpenReview / ICLR 2026 Poster" 而无 arxiv ID，现已补齐真实 arxiv ID（已确认 ICLR 2026 Poster 录用）。

---

## 表 2 · 捏造 / 需修正（已处理）

| 引用 / 论断 | 判定 | 证据 | 处置 |
|---|---|---|---|
| "MECE 约束维度分解相比平面提示**提升召回率 23-31%**" | ❌ **捏造** | arxiv / ACL Anthology / IEEE Xplore / JAIR 全检索 0 结果；Grok 初次自信描述，追问无法给出 URL/DOI | **从 foundations 文档删除该数字，改为无量化的机制性陈述** |
| Chen et al. (2024) ACL | ❌ **不存在** | ACL Anthology 2024 无此文 | 删除 |
| Kumar & Patel (2025) IEEE TKDE | ❌ **不存在** | IEEE Xplore / DBLP / Scholar 0 结果 | 删除 |
| Li et al. (2023) JAIR | ❌ **不存在** | JAIR 自身检索 0 结果 | 删除 |
| APOLLO「ICLR 2026」 | ⚠️ **被 desk-reject** | OpenReview `vlqwNZWZv2`，2025-10 desk-rejected；无 arxiv 预印本 | **不得作为 ICLR 2026 引用**；如需提及标为"OpenReview 投稿，未录用" |

---

## 表 3 · 无法追溯的"真实案例"（弃用）

子代理在调研中能识别并主动标记这些由 Grok 合成、无法追溯到一手出处的"案例"——这正是我们想要的怀疑性。**以下一律不用**：

| 声称的案例 | 问题 |
|---|---|
| Stripe vs Adyen teardown（SaaStr 2025 演讲，含 +1.2/−1.8 评分、9 天→2 天）| 无任何公开记录可追溯 |
| Notion vs Coda 内部 wiki teardown（Lenny's Podcast 2024，含 3.1→4.4 满意度）| 无法追溯到该具体内部材料 |
| "Journal of Business Research 2019 meta-review，50 家公司 68%" | 具体引用未检索到；SWOT 批评改用可核实的 Hill & Westbrook (1997) |
| McKinsey (2023) "Avoiding the five forces trap in digital markets" | McKinsey.com 未检索到 |

---

## 表 4 · practitioner 自报数据（保留但显式降级标注）

这些来自方法论作者/咨询机构自身，**非独立同行评审**。可引用，但必须标注来源性质，不得当作"学术验证"：

| 数据 | 来源 | 标注 |
|---|---|---|
| ODI「86% 创新成功率 vs 行业 17%」| Ulwick / Strategyn 自报 | practitioner claim，未经独立验证 |
| Cordis 案例（市占 1%→20%，J&J 以 $109/股收购）| Strategyn + 公开并购记录交叉佐证 | 可用（一手+公开记录佐证）|
| Strategyn「1000+ 财富百强项目」| 自报 | 仅作方向性参考 |
| JTBD/ODI/Kano 作为「因果理论」的可证伪性 | MIT Sloan (2015) 等指出实证有限 | 作为 practitioner framework 引用，非"经学术验证的因果律" |

---

## 对既有文档的处置

- `docs/prompt-engineering-academic-foundations.md`：已**就地修正**——删除 23-31% 捏造数字与三个假引用、修正 APOLLO 状态、补齐 DeepTRACE/ResearchRubrics/DeepResearch Bench 真实 arxiv ID，并在抬头加指向本审计的说明。
- 后续所有方法决策文档（`track-a-*`、`track-b-*`）只引用**本审计核实为真**的来源；practitioner framework 一律按表 4 标注。

## 复核命令（可复现）

```bash
# 任意 ID 可一行复核
curl -sL "https://export.arxiv.org/api/query?id_list=2509.04499" | grep -o '<title>[^<]*</title>'
```
