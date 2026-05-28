# FathomX Roadmap (v0.1 draft — 2026-05-29)

> 活文档（rolling-wave）。本文件 = **总计划**；每个 Phase / 阶段开始时另写细化计划 `docs/plans/phaseN-*.md`，完成时回写 review 并调整本文件。

## 1. 北极星 / Vision

FathomX = **产品深度研究的 Skill 层（Layer 1 业务编排）**，MCP 工具能力主要由 **Lapis** 引擎提供（必要时不局限于 Lapis）。

- **目标用户**：互联网产品专家 / 运营专家 / 业务专家 / 独立开发者。要易用、易部署。
- **能力（≥4）**：竞品深度研究、产品能力研究、创新方向研究、产品需求深度调研。
- **核心价值（最核心 = 易读·真实·有用）**：产出符合业务实际需要、可信度远超常规 LLM/agent 编排、大量降低 AI 幻觉、按需兼具广度与深度的文档；具体告诉使用者**如何推进他想要的产品需求**。
- **差异化**：丰富图文视频证据；"宁少但真"的数据维度佐证与分析；真正的产品专家视角思考。

## 2. 架构决策（2026-05-29 确认）

| 决策 | 结论 |
|---|---|
| 引擎边界 | **解耦**：fathomx 只含 skill/prompts/installer；Lapis 作独立 MCP server 消费（上游 `4o3F/Lapis`，AGPL-3.0）。fathomx 后期提供**一键部署安装 Lapis** 能力 |
| 首攻能力 | **竞品深度研究** = v2.0 第一份真实价值 |
| 分发范围 | **真正公开 OSS 分发** → key/网络故事必须对无基建的普通用户跑通 |
| 许可证 | fathomx 与 Lapis 同为 **AGPL-3.0**（已带 LICENSE+README 声明；待补 Cargo/组件声明）|

目标形态：
```
使用者机器
 └─ fathomx（skill 层 + TUI 安装/配置引导）   ← AGPL-3.0
      ├─ 一键安装/拉起 Lapis MCP server        ← 消费上游 4o3F/Lapis（AGPL-3.0）
      └─ 驱动 Layer 1 编排：问题→MECE维度→人格分配→search计划→aspect执行→gap检测→产品决策报告
```
当前状态：repo 仍 vendored 着 Lapis 引擎源码（同步上游带入）。**结构重组（抽离引擎源码、改 README/品牌为 fathomx）放到 Phase 3 入口**；Phase 1/2 期间保留 vendored 副本当工作参考。

## 3. 四阶段（Phase）

### Phase 1 · 方法预研（学科学）
- **目标**：找到真实可借鉴、科学的方法论。**双支柱**——
  - **Track B｜产品专家真实方法论（目的）**：真实的竞品调研方法论、产品需求/功能方法论、真实实践案例（驱动 MECE 维度、报告结构、机会矩阵、"产品专家视角"）。
  - **Track A｜AI 编排/可信度方法论（手段）**：证据可信度、降幻觉、MECE 工程、研究人格、广度深度预算——如何可靠低幻觉地执行 Track B。
- **关键约束（R1 防无界综述）**：由决策驱动问题牵引 + 限时 + 明确产出物；**与 Phase 2 交织**；优先真实实践案例+权威框架原始出处。
- **细化计划与决策问题**：见 [`docs/plans/phase1-method-decisions.md`](docs/plans/phase1-method-decisions.md)（B1-B3 + A1-A5）。
- **输入**：业务需求（§Phase2）、产品方法论权威来源（Cagan/Torres/Ulwick/Kano/Christensen 等）、专业文献（用户示例 arxiv 2603.05344 / 2605.13357 — ✅ 已核实为真）。
- **产出**：`docs/research/` 方法决策文档。
- **退出标准**：B1-B3 + A1-A5 各有"方法+依据(含真实案例)+落地点"，无未解方法论阻塞。
- **✅ 状态（2026-05-29）：主体完成**。见阶段 review [`docs/plans/phase1-review.md`](docs/plans/phase1-review.md) 与产出 [`docs/research/`](docs/research/README.md)。亮点：21 个 arxiv 引用全核实为真，并清除前次素材里 1 处捏造统计+3 个假引用（[`citation-audit.md`](docs/research/citation-audit.md)）。

### Phase 2 · 业务需求文档打磨（定规格）
- **目标**：把 AI 生成的业务层草稿打磨成科学、可落地的最佳业务需求规格 + 基于 MCP(主 Lapis) 的 skill 编排设计。**不排斥重做**。
- **输入**：Lapis 业务层 wiki / `docs/Lapis 业务层补充文档…md`、Phase 1 方法决策。
- **关键(R2)**：把"证据完整性"立为一等支柱（视觉证据、来源可信度分级、宁少但真强约束）；**定义评测标尺 + 黄金样例**，使"可信度远超普通 LLM"可证伪。
- **产出**：重做的业务需求规格；skill 编排架构设计；评测 rubric + 1-2 个黄金研究课题与专家级参考产出。
- **退出标准**：规格通过自评 rubric；编排设计明确 Layer1↔Lapis 的每步接口。

### Phase 3 · skill 编排实现与验证（建实现）
- **目标**：产出完整 skill 编排，**先把竞品深度研究端到端跑通+验证** = v2.0；其余能力逐版加。
- **含结构重组**：抽离 Lapis 引擎源码、fathomx 改为 skill 层 + 安装器、README/品牌改为 fathomx。
- **要补的 Layer 1 资产**（上轮三方核验确认缺口）：`prompts/layer1/agent-allocation.md`、强制产品 MECE-6 的 `task-decomposition.md`、3+1 人格 prompt、`aspect-agent.md` 产品扩展字段（visual_evidence/user_jobs…）、13 章产品报告模板、gap 检测清单、quality floor。Rust 仅在需机器强校验产品字段时小幅扩 schema（规格标为可选）。
- **产出**：可运行的竞品深度研究 skill；用 Phase 2 rubric/黄金样例验证。
- **退出标准**：竞品研究端到端产出达到 rubric 门槛；可复现。

### Phase 4 · 易部署 / OSS 分发（可交付）
- **目标**：普通用户在自己机器/网络下可部署使用。
- **关键(R3)**：核心难点不是 TUI 长相，而是**普通用户自助获取/配置 exa/tavily/grok key + 无代理基建的网络故事**。
- **产出**：TUI 安装引导、TUI key 配置引导（含各 provider 注册获取指引）、一键安装 Lapis、打包分发、文档英文化。
- **退出标准**：一台干净机器按引导能从零跑出一份竞品研究报告。

## 4. 版本切分（strawman，逐 Phase 细化）

| 版本 | Phase | 产物 | 性质 |
|---|---|---|---|
| 现状 v1.2.0 | — | 刚吸收 Lapis 引擎 | 基线 |
| v2.0-design | 1+2 | 方法决策 + 业务规格 + 编排设计 + 评测标尺 | 设计冻结（内部里程碑）|
| **v2.0** | 3 首能力 | 竞品深度研究端到端+验证 + 结构重组 | 第一份用户价值 |
| v2.1 / v2.2 / v2.3 | 3 续 | 产品能力 / 创新方向 / 需求调研 | 能力扩展 |
| v2.x → v2.5 | 4 | TUI 安装+key 引导、一键装 Lapis、OSS 打包 | 产品化分发 |

## 5. 规划方法论（rolling-wave）
1. 本 `ROADMAP.md` = 总计划。
2. 每 Phase / 阶段**开始**：写 `docs/plans/phaseN[-stage].md` 细化计划与方案。
3. 每 Phase / 阶段**完成**：review，回写本文件调整后续。
4. 多讨论澄清、多深度研究，与 Heye 迭代。

## 6. 决策日志
决策以 ADR 为准，见 [`docs/decisions/`](docs/decisions/README.md)：ADR-0001 采纳 Lapis 引擎 · 0002 解耦+一键安装 · 0003 首攻竞品研究 · 0004 公开 OSS · 0005 AGPL-3.0。

## 7. 未决 / 待澄清

**Phase 1 遗留的产品判断（待 Heye 拍板，不阻塞，但影响 Phase 2/3）：**
- 竞争五维 vs 通用 MECE-6 的分层关系（建议：五维=竞品报告骨架，MECE-6=跨能力顶层）。
- 研究人格最终数量/集合（建议：Experience Analyst + Strategist + 跨人格质量门）。
- 无一手问卷时 ODI 的 Imp/Sat 是否允许用研究证据/市场代理估算 + TM-4 标注证据等级。

**仍待澄清：**
- 评测 rubric 的具体维度与门槛（Phase 2 定；可借 DeepTRACE 8 维 + ResearchRubrics）。
- `4o3F/Lapis` 是否 Heye 可控（影响一键安装如何拉取/构建 Lapis）？
- ROADMAP / 文档英文化时机（公开 OSS 前）。

**已解决：** Phase 1 的 8 个决策问题（B1-B3 + A1-A5）已齐全并落定；arxiv 示例真伪已核实。
