# ADR-0006: Phase 1 方法论确认决策

Status: Accepted (2026-05-29)

## Context
Phase 1 方法预研（[`docs/research/`](../research/README.md)）产出后，有 3 个非证据可推导的产品判断留待 Heye 拍板。Heye 已逐条确认。本 ADR 固化这些决策，供 Phase 2/3 依赖。

## Decision

1. **竞争五维与 MECE-6 分层**：「竞品深度研究」能力以 B1 的**五维 MECE**（Job与真实竞争集 / 能力对位矩阵 / Kano 分级 / ODI 缺口打分 / 定位与白地）作**报告骨架**；通用 **MECE-6** 仍为跨能力的**顶层维度集**。二者是分层关系，非替换。

2. **研究人格集合**：按 B3 新判断收敛——核心 **2 人格**（Product Experience Analyst / Product Strategist）+ **跨人格质量门**（TM-4 认识论标注、TM-11 可证伪，注入所有人格）。早期 foundations 文档的 Market/CI Analyst **不强制保留**；人格最终数量在 Phase 3 结合首攻"竞品研究"定。

3. **ODI 数据来源**：ODI 的 Importance/Satisfaction 在无一手问卷时，**允许用研究证据/市场代理估算**，但**必须以 TM-4 显式标注其证据等级**（实证 / 专家观点 / 假设 / 推测）。

## Consequences
- Phase 2 业务需求规格直接采用：竞品报告=五维骨架；需求报告=B2 八段模板；机会矩阵=ODI 打分（含估算+证据标注）。
- Phase 3 prompt 资产：2 人格 thinking prompt 用 B3 的 13 条 TM 填充；`agent-allocation.md` 按 2+门设计，人格数留弹性。
- ROADMAP §7 对应 3 个待确认项移除；`track-b` 与 `phase1-review` 的"待拍板"段已标确认。
- 风险：ODI 估算值的可信度依赖 TM-4 标注纪律与 Track A 的来源分级/原子核验兜底——这是 Phase 2 评测 rubric 要重点验证的点。
