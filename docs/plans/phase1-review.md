# Phase 1 · 方法预研 — 阶段 Review（rolling-wave）

> Status: 主体完成（2026-05-29）。本 review 对照退出标准盘点 Phase 1 产出，并回写 ROADMAP 后续。
> 配套细化计划见 [`phase1-method-decisions.md`](phase1-method-decisions.md)。

## 做了什么

1. **先验真伪**（[`../research/citation-audit.md`](../research/citation-audit.md)）：
   - 21 个 arxiv ID 经 arxiv 官方 API 逐个核实**全部为真**（含用户示例 2603.05344/2605.13357 及多篇 2026 论文）。
   - **发现并清除**前次 Track A 文档里的 1 处捏造统计（"MECE 召回率 +23-31%"）+ 3 个不存在的引用（Chen/Kumar&Patel/Li）。
   - APOLLO 实为 desk-reject，降级；DeepTRACE/ResearchRubrics/DeepResearch Bench 补齐真实 arxiv ID。
2. **Track B（产品专家方法论，本轮新增重点）**：B1/B2/B3 三个决策问题各落定方法+真实案例+落地点（[`track-b`](../research/track-b-product-methodology.md)）。
3. **Track A（编排/可信度）**：A1-A5 在修正后的早期素材上补差完成（[`track-a`](../research/track-a-orchestration-credibility.md)）。
4. 方法：Wide Research——4 个独立 subagent 并行调研（各自干净上下文），主会话综合；关键 arxiv 主会话独立复核。

## 退出标准核对

| 项 | 退出标准 | 状态 |
|---|---|---|
| B1-B3 | 各有方法+依据(含真实案例)+落地点 | ✅ |
| A1-A5 | 各有方法+依据+落地点 | ✅（A4 人格"数量"留 Phase3 定，非阻塞）|
| 先验真伪 | arxiv 示例核实、伪引用清除 | ✅ |
| 无未解方法论阻塞 | — | ✅ |

**结论：Phase 1 方法论层面无阻塞，具备进入 Phase 2（业务需求规格打磨 + 评测标尺）的条件。**

## 产品判断 — ✅ 已确认（2026-05-29，见 [ADR-0006](../decisions/0006-phase1-method-decisions.md)）

1. ✅ 竞争五维=竞品报告骨架，MECE-6=跨能力顶层（分层关系）。
2. ✅ 2 核心人格（Experience Analyst + Strategist）+ 跨人格质量门；Market/CI 不强制保留，最终数量 Phase 3 定。
3. ✅ 无一手问卷时 ODI 允许用研究证据/市场代理估算 + TM-4 标注证据等级。

## 对 ROADMAP 的回写

- §7 未决项「arxiv 示例真伪」「文档英文化时机」相关项更新；新增上述 3 个产品判断待确认项。
- Phase 2 入口：把 Track B 的报告模板/机会矩阵 + Track A 的可信度机制，落成"业务需求规格 + 评测 rubric + 黄金样例"。

## 下一步（Phase 2 预告）

1. 用 B2 的 8 段模板 + B1 五维，重做/校准业务需求规格。
2. 定义评测 rubric（可借 DeepTRACE 8 维 + ResearchRubrics）+ 1-2 个黄金研究课题与专家级参考产出，使"可信度远超普通 LLM"可证伪。
3. 明确 Layer1↔Lapis 每步接口。
