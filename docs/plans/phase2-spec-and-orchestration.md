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
产出 `docs/specs/pm-deep-research-competitive-research-spec.md`（单一 canonical）。按 §3 清单逐项消解分歧，结构建议：
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

## Review（2026-05-29 · 主体完成，待 Heye 确认）

### 做了什么
1. **WS5 ROADMAP**：标 Phase 2 竞品优先 + 新增 Phase 2′ 规格泛化阶段 + 版本表里程碑。
2. **WS1 权威规格**（[`specs/pm-deep-research-competitive-research-spec.md`](../specs/pm-deep-research-competitive-research-spec.md)）：合并 3 份草稿，全面对齐 Phase 1（五维骨架/2人格+13TM+质量门/4-tier+展示标签/ODI 完整公式+Kano/证据完整性一等支柱/五维→13章/Gap+quality floor/降级）。**Heye 已认可 4 个合并判断**（人格吸收/可信度细分/五维映射/视觉证据方向）。
3. **归档**：3 份草稿移入 `docs/archive/`，统一目录 `specs/`，修全链接。
4. **WS2 rubric**（[`evaluation/rubric.md`](../evaluation/rubric.md)）：12 维可打分 + floor 硬门槛 + 普通 LLM 基线（可证伪）+ 捏造一票否决。
5. **WS4 接口**（[`specs/orchestration-interface.md`](../specs/orchestration-interface.md)）：对照 Lapis 真实 MCP。**关键发现**：Lapis 仅 `aspect_research`+`deep_research`，无 `research_plan`/`compare_reports` → 拆解/综合/对比/13章/分级全在 Skill；产品结构字段 v2.0 用 prompt+Skill 承载，不改 Rust（可选扩展留 Phase 3）。
6. **WS3 黄金样例**（[`evaluation/golden/running-coach-ai-upgrade.md`](../evaluation/golden/running-coach-ai-upgrade.md)）：Wide Research 4 子代理并行 + 主会话独立核实承重引用（Strava-Runna 收购/Nature npj 伤病预测 Tier-1/WHOOP Coach 均✅核实）；产出 Strava AI 升级方向专家报告，rubric 自评 **22/24**（按 Heye 审计改写为论点先行的专家叙事 + 补 build-cost/版本历史维度 + ODI 数值化；交叉审计后 B3 诚实降分，见下「Heye 审计反馈应用」）。

### 退出标准核对
| 项 | 状态 |
|---|---|
| canonical 规格完成、对齐 Phase 1、证据完整性一等支柱 | ✅ |
| 评测 rubric 定义；规格强制每维（自评通过）| ✅ |
| ≥1 海外健身黄金课题专家级参考产出 | ✅（22/24，含交叉审计修订）|
| Layer1↔Lapis 每步接口文档级明确 | ✅ |
| ROADMAP 加泛化阶段 | ✅ |

### 对 Phase 3 的输入（回写 ROADMAP §3 Phase 3）
- 接口已定 Skill 侧承载产品结构（无需先改 Rust）→ Phase 3 先落 `prompts/layer1/*` + `prompts/layer2/persona-*.md` 实体文件（按 WS4 §2 映射 + §3 prompt 契约 + §5 预算）。
- rubric 的 floor 维度 → 做成 skill 内自动 quality-gate。
- 黄金样例的改进点（C1 实抓截图、竞品完整版本时间线做定量 build-cost）= Phase 3 端到端要补的能力。

### Heye 确认结果（2026-05-29）
- **Phase 2 签收**：✅ **已签收**（2026-05-29，审计第一轮通过 —— Heye："这轮修订及格了，可以提交和继续"）。可进 Phase 3。
- **WS4 引擎路线**：✅ **第一版不动引擎**；后续跑通后若有需求，**整理成需求提给上游 4o3F**（引擎非我们做，我们只提需求）。详见 [接口 §6](../specs/orchestration-interface.md#6-引擎边界第一版不动引擎schema-扩展作为需求提给上游heye-2026-05-29-确认)。
- **push**：先不 push，留本地待评审。

### Heye 审计反馈应用（2026-05-29，第一轮）
Heye 详细评审给出两条反馈，已应用（保留确认锚点、只改指出维度、不推倒重来）：

1. **建设成本/迭代节奏是缺失的一等维度**：竞品研究判"是否建设某功能"必须研究**建设成本**；竞品 changelog/版本更新频率是其**实际动作（revealed strategy）**——既是 build-cost 信号，也暴露真实投入优先级。
   - 落地：规格 §1.2（Build/Not Build 输出加建设成本）、§3 新增「迭代节奏与建设成本（实际动作证据）」note（绑 TM-12 言行分离）、§4.3、§6.1（release notes 入 Tier 2）、§7.3（复杂度列用迭代节奏佐证）、§9.1（新增 Build 意图 gap 检测）；rubric B3（证据加"版本迭代记录"）+ C3（复杂度 build-cost 佐证）；接口 §2（Build 意图拉版本历史）+ §4（official 含 release notes）。
   - 真实性核实：子代理确认这是成熟 CI 实践（Trackmore/CI Alliance/Seeto 等），数据源 = App Store Version History（最丰富免费档）；**剔除** Grok 无法核实的 Crayon/Klue 引语。

2. **黄金样例不能机械堆砌表格，要按"给人读"的专业写法**：维度对，但行文是有专业惯例的 genre。
   - 落地：先 Wide Research 真实优质案例（Stratechery/Built for Mars/Lenny's/McKinsey 行动标题/Minto Pyramid/Amazon 六页备忘录），抽出 12+ 条写法惯例 → 写成规格 **§7.4 行文规范**（论点先行/标题即论点/表格作证据/按主题综合/校准不确定性/收尾给行动）+ rubric **行文 floor**（机械堆砌判不通过）。
   - 据此**改写黄金样例**为论点先行的专家叙事；顺带应用子代理事实核查：删未核实的 Athlete Intelligence "2025-02 GA"、更正 "Garmin Run Coach"→官方名、区分单独/捆绑定价。第一轮自评 22→23/24；**随后第二轮 Codex+subagent 交叉审计**指出 B3 单元格无 per-cell 证据 id（符号化矩阵），诚实回 **22/24**，并把 Ch9 ODI 数值化（详见 [phase3 计划](phase3-skill-orchestration.md) 审计记录）。
