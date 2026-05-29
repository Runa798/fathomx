# Phase 2 计划 · 业务需求规格 + 评测标尺 + 编排接口（定规格）

> Status: 草稿（2026-05-29 起草，待 Heye 过目后执行 WS1）。rolling-wave 细化计划。
> 上游：[`ROADMAP.md`](../../ROADMAP.md) §3 Phase 2、[ADR-0006](../decisions/0006-phase1-method-decisions.md)、Phase 1 产出 [`docs/research/`](../research/README.md)。
> 完成时在本文件追加 Review 小节并回写 ROADMAP。

## 0. 本阶段已确认的三个取舍（2026-05-29 Heye 拍板）

| # | 决策 | 结论 | 对计划的影响 |
|---|---|---|---|
| D1 | 3 份草稿怎么处理 | **合并为一份权威规格** | 旧 3 份归档；产出单一 canonical spec，全面对齐 Phase 1 |
| D2 | 规格范围 | **竞品研究优先**；跑通质量后再泛化为**全 MECE-6 通用**（授权调整整体计划、加泛化阶段）| Phase 2 规格聚焦竞品能力；新增"规格泛化"阶段（见 §6 ROADMAP 回写）|
| D3 | 黄金样例领域 | **海外健身/运动产品** | 黄金课题用真实可核实的海外健身 app/硬件竞品 |

## 1. 目标

把早于 Phase 1 的 3 份 AI 生成业务层草稿，**重做并合并**成一份科学、可落地、与 Phase 1 方法决策完全对齐的**竞品深度研究业务需求规格**；定义**可证伪的评测标尺 + 黄金样例**，使"可信度远超普通 LLM"能被检验；明确 **Layer1↔Lapis 每步接口**。

**R2 关键约束**：把"**证据完整性**"立为一等支柱——视觉证据（截图/teardown 图/图表）、来源可信度分级、"宁少但真"硬约束、逐声明 provenance。这是草稿里缺失、本阶段必须补的核心。

## 2. 输入

- **待合并的 3 份草稿**（都早于 Phase 1，有系统性分歧）：
  - [`docs/archive/fathomx-business-supplement.md`](../archive/fathomx-business-supplement.md)（11 条补充 + Lapis 开放问题回答）
  - [`docs/archive/fathomx-business-input-to-lapis.md`](../archive/fathomx-business-input-to-lapis.md)（业务层注入清单 1.1–1.11 + Q1–Q8）
  - [`docs/archive/Lapis 业务层补充文档：Product Deep Research 模式.md`](../archive/Lapis%20业务层补充文档：Product%20Deep%20Research%20模式.md)
- **Phase 1 方法决策**：[`track-b`](../research/track-b-product-methodology.md)（B1 五维 / B2 八段模板 / B3 13 条 TM）、[`track-a`](../research/track-a-orchestration-credibility.md)（A1 4-tier / A2 反幻觉 / A3 MECE 工程 / A4 多人格 / A5 动态预算）、[`citation-audit`](../research/citation-audit.md)。
- **ADR-0006** 的 3 条确认决策（五维↔MECE-6 分层 / 2 人格+质量门 / ODI 估算+TM-4 标注）。
- **评测可借素材**：DeepTRACE 8 维（arXiv 2509.04499）、ResearchRubrics（2511.07685）、DeepResearch Bench（2506.11763）——均已核实为真。

## 3. 草稿 ↔ Phase 1 分歧清单（合并时必须消解）

| 主题 | 草稿现状 | Phase 1 决策 | 合并口径 |
|---|---|---|---|
| 维度框架 | 只有 MECE-6 | 竞品=B1 五维骨架；MECE-6=跨能力顶层 | **分层**：规格主体用五维骨架；MECE-6 作顶层框架记录 + 给后续能力留位 |
| 研究人格 | 3 人格（Market/CI/Strategist），每个带框架 | 2 核心人格（Experience Analyst/Strategist）+ 跨人格质量门（TM-4/TM-11）| 收敛为 2 人格；13 条 TM 按 B3 分配注入；Market/CI 不强制 |
| 可信度分级 | A-E 五级（域名启发式）| 4-tier 来源分级 + 原子核验 + 语句级引用审计 + 忠实性 | **统一到 4-tier**（Phase 1 研究过的），A-E 作展示别名映射；叠加 FActScore/DeepTRACE/CiteEval 机制（**待 §7 确认**）|
| 机会优先级 | JTBD 机会分 `Imp+(Imp−Sat)`（简化）| ODI `Imp + max(0, Imp−Sat)` 主排序 + Kano 类型叠加 | 用 ODI 完整公式 + Kano 叠加；无一手问卷→代理估算 + TM-4 标注 |
| 报告模板 | Quick/Standard/Deep 按 MECE-6 组织 | B1 五维骨架 + B2 八段需求模板 | 竞品报告=五维骨架 + 支撑段（威胁分级/定位/竞品速写）+ 证据/方法论附录；Quick/Standard/Deep 作深度档位 |
| 证据完整性 | 仅有可信度评级 | R2：一等支柱 | **新增**：visual_evidence 必填项、逐声明 provenance、"宁少但真"弃权优先 |
| 产品专家味 | 无 | B3 13 条 TM | **新增**：把 TM 编码进 2 人格 system prompt |
| aspect 字段 | 有 dimension/persona/gap_status 等 | + visual_evidence / user_jobs | 扩展 schema 字段 |

## 4. 任务分解（Work Streams）

### WS1 · 权威业务需求规格（核心，最大头）
产出 `docs/specs/fathomx-competitive-research-spec.md`（单一 canonical）。按 §3 清单逐项消解分歧，结构建议：
1. 范围与决策驱动定位（竞品深度研究=v2.0；MECE-6 顶层框架）
2. 复杂度路由（Quick/Standard/Deep）+ 决策意图推断
3. **竞品研究五维骨架**（B1）：每维=主用方法 + 证据标准 + 报告落点
4. **机会优先级**：ODI 完整公式 + Kano 叠加 + 估算与 TM-4 标注规则
5. **2 研究人格 + 跨人格质量门**：13 条 TM 分配（B3）
6. **证据完整性一等支柱**（R2）：4-tier 来源分级 + 视觉证据要求 + 逐声明 provenance + 反幻觉（abstention/verification chain/有限 self-refine）
7. **报告模板**：五维骨架 + 支撑段 + 证据/方法论附录（含 Quick/Standard/Deep 档）
8. **aspect report schema**（扩展字段：dimension/persona/decision_intent/visual_evidence/user_jobs/gap_status/credibility/sources_used）
9. Gap 检测清单 + quality floor（不达标→标置信度警告/弃权）
10. 优雅降级（Claude-only fallback 仍保方法论）
- 完成后归档旧 3 份到 `docs/archive/`（保留可追溯）。

### WS2 · 评测 rubric + quality floor
产出 `docs/evaluation/rubric.md`。
- 借 **DeepTRACE 8 维**（答案：置信/单面性；来源：数量/质量；引用：充分性/准确性/无支撑率/必要性）+ **ResearchRubrics** + 竞品研究专属维（五维覆盖度、证据完整性含视觉证据、ODI/Kano 严谨度、TM 产品专家味、宁少但真弃权纪律）。
- 定义 quality floor 阈值（每维 ≥N 来源、引用准确率门槛、关键声明零无支撑、能力矩阵格必附视觉/可核实证据）。
- **自评闭环**：规格本身须通过自己的 rubric（= 退出标准之一）。

### WS3 · 黄金样例（海外健身/运动产品）
产出 `docs/evaluation/golden/`。
- 选 1–2 个真实可核实的海外健身/运动竞品课题（候选：connected strength 如 Tonal/Tempo；跑步教练 app 如 Strava/Runna/Nike Run Club；智能跳绳/可穿戴）。
- 产出**专家级参考产出**（应用五维骨架 + 证据完整性 + TM + 真实已核实来源），作为"远超普通 LLM"的可证伪基准。
- **深度待定（§7 确认）**：建议 Phase 2 先全规格化课题 + rubric + **1 个课题做到专家级完整参考**（兼作 dogfooding 规格）；另一课题留 Phase 3 验证时补。

### WS4 · Layer1↔Lapis 编排接口
产出 `docs/specs/orchestration-interface.md`。
- 逐步定义接口：复杂度路由 → 决策意图推断 → `research_plan`（tier/decision_intent/五维 aspects）→ `aspect_research`（人格 prompt/搜索策略/gap loop）→ Layer1 跨 aspect gap 检测 → 综合 → 报告模板 → 证据/方法论附录。
- 映射 Lapis MCP 工具与所需 schema 字段（decision_intent/tier/dimension/persona/gap_status/credibility/visual_evidence）。
- 注：Lapis 引擎的 Rust schema 实际扩展是 Phase 3 工作（最小、可选）；本阶段只做**文档级接口设计**，对照 Lapis 现有 schema。

### WS5 · ROADMAP 回写（泛化阶段，授权调整）
见 §6。

## 5. 排期与依赖
WS5（小，已授权）先做 → WS1（基础）→ WS2 与 WS4 可在 WS1 维度定稿后并行 → WS3 依赖 WS1+WS2（验证规格与 rubric）。

## 6. ROADMAP 回写（D2 泛化阶段）
按 Heye "跑通质量后做成全 MECE-6 通用、在合适位置加阶段"：
- **位置**：在 v2.0 竞品研究**通过 Phase 2 rubric 验证后**、构建 v2.1+ 其它能力**之前**，插入**"规格泛化"阶段**——把竞品 canonical 规格泛化为全 MECE-6 通用产品研究规格（4 项能力共用顶层框架）。
- 落点：更新 ROADMAP §3（Phase 2 标注"竞品优先"）+ §4 版本表（v2.0 后加泛化里程碑）。

## 7. Heye 确认结果（2026-05-29）
1. **可信度分级统一口径**：✅ 采纳 Phase 1 的 **4-tier 为逻辑底座**（摄入/校验用）+ 报告内**保留展示标签**（High/Med/Low/Unknown 或 A-E），文档给出映射。
2. **黄金样例深度**：✅ Phase 2 做 **1 份完整专家级**参考产出（兼 dogfooding 规格）+ rubric/课题规格化；第 2 个课题留 Phase 3 验证补。
3. **黄金课题品类**：✅ **跑步教练 app（Strava / Runna / Nike Run Club 等）**。

## 8. 退出标准
- 单一 canonical 竞品规格完成，§3 分歧全部消解（无 MECE-6/五维、人格、可信度、ODI 不一致），证据完整性为一等支柱。
- 评测 rubric 定义完成，且**规格通过自评 rubric**。
- ≥1 个海外健身竞品黄金课题有专家级参考产出（或确认的分期深度）。
- Layer1↔Lapis 每步接口在文档级明确。
- ROADMAP 已加入泛化阶段。

## 9. 风险
- **R1（无界综述复发）**：规格写作可能膨胀——每节锚定"决策驱动 + 落地点"，超出即砍。
- **证据完整性可执行性**：视觉证据在纯 API 搜索下获取成本高——WS4 需明确 Layer 2 浏览器抓取何时介入（截图/teardown）。
- **黄金样例真实性**：所有引用须过 `citation-audit` 同款核实（先验真伪），严守宁少但真。
- **ODI 估算可信度**：依赖 TM-4 标注纪律 + Track A 兜底——rubric 重点验证项（ADR-0006 风险延续）。

## Review（完成后追加）
（待 Phase 2 完成回写）
