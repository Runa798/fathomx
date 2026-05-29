# Phase 3 · Skill 编排实现与验证（细化计划）

> Status: Phase 3（2026-05-30）。**M1/M2/M3/M4 全完成**：WS-A 人格 + WS-B 编排 + WS-C 13 章报告/自验证 + WS-E 证据后处理独立化 + WS-D Skill 入口可运行/Claude-only 降级；端到端实跑 6/6，13 章报告 **rubric 22/24**（B3 较手写黄金 1→2 → 方法论可被 prompt 承载，不需再提 4o3F 方法论需求）；引擎 SSE 事件上限本地补丁 + 提上游 [#8](https://github.com/4o3F/Lapis/issues/8)。剩 WS-F 结构重组（按 D2）+ WS-G v2.0 验收。见 §3e。
> rolling-wave：本文件 = Phase 3 细化计划；完成时回写 review 并调整 [`../../ROADMAP.md`](../../ROADMAP.md)。
> 上游：Phase 2 已签收（[规格](../specs/pm-deep-research-competitive-research-spec.md) / [rubric](../evaluation/rubric.md) / [接口](../specs/orchestration-interface.md) / [黄金样例](../evaluation/golden/running-coach-ai-upgrade.md) 23/24）。
> 目标版本：**v2.0 = 竞品深度研究端到端跑通 + 验证**（ROADMAP §3 Phase 3）。

---

## 0. 现状盘点（开工前必读）

repo 现有 skill/prompt 资产是**同步上游 Lapis 带入的通用版**，尚未承载 PM DeepResearch 竞品研究方法论：

| 资产 | 现状 | 与规格的差距 |
|---|---|---|
| `skills/deep-research.md` | Lapis 通用研究 skill（分类→拆解→调 MCP→校验→报告）| 无 decision_intent 路由、无五维骨架、无竞品触发、无 13 章/降级特化 |
| `prompts/layer1/task-decomposition.md` | 通用 MECE 拆解 → `DeepResearchRequest` | 未强制 decision_intent + 五维 aspect 映射（接口 §2）；Build 意图不拉版本历史 |
| `prompts/layer1/final-report.md` | 通用报告生成 | 非 13 章产品模板，无 §7.4 行文规范、无五维→13 章映射 |
| `prompts/layer2/aspect-agent.md` | 通用 aspect agent（含 byte-equal 证据纪律）| 无人格（Experience Analyst / Strategist）、无 13TM、无产品结构输出契约（矩阵/Kano/ODI 进 claim、visual_evidence 进 Evidence、build-cost 进 claim）|
| `prompts/layer2/evidence-extractor.md` / `search-planner.md` | 通用 | 待评估是否需竞品特化 |

**结论**：Phase 3 主体 = 在不改 Lapis Rust 源码的前提下（接口 §6），**新增/特化 Skill + prompt 资产**把规格落地，并端到端验证 prompt 承载是否够稳。

---

## 1. 目标与退出标准

- **目标**：竞品深度研究 skill 端到端可运行（Lapis MCP 正常时多 Agent；不可用时 Claude-only 降级），产出对照黄金样例达 rubric 门槛。
- **退出标准**（承 ROADMAP）：
  1. 竞品研究端到端产出 **floor 全过 + 行文 floor 过 + 总分 ≥18/24**；目标向黄金样例 23/24 看齐。
  2. 可复现：同一课题重跑结论稳定、证据可追溯。
  3. 验证 prompt 承载方案（接口 §3）是否够稳 → 决定是否触发"提 schema 需求给 4o3F"（接口 §6）。

---

## 2. 工作分解（WS）

### WS-A · 人格 prompt 资产（Layer 2）
落 `prompts/layer2/persona-experience-analyst.md` + `persona-strategist.md`，各自：
- 注入对应 **TM**（Experience: TM-1/2/6/10/12；Strategist: TM-3/5/7/8/9/13）+ 跨人格质量门 TM-4/TM-11（规格 §5）。
- **产品结构输出契约**（接口 §3）：能力矩阵/Kano/ODI/定位以 Markdown 表或 JSON 块写进 `Finding.claim`；`visual_evidence` 作 `Evidence`（url=媒体、summary 注 media_type+observed_feature）；**Build 意图：版本历史/迭代节奏 + build-cost 估算写进 claim，证据 url 指向 App Store Version History**（规格 §3 迭代节奏与建设成本）。
- 保持 Lapis 原生 byte-equal 证据纪律、untrusted-evidence 规则不变（继承 aspect-agent.md）。

### WS-B · Layer 1 编排资产 ✅（2026-05-29）
- ✅ 新建 `skills/pm-deep-research/prompts/layer1/agent-allocation.md`：五维 → aspect → 人格映射 + Quick/Standard/Deep aspect 子集 + **Build 意图追加 `build-cost-version-history` aspect**；W3 落定（`job-and-competitive-set` 归 strategist，JTBD 折叠进其问题/成功标准）。
- ✅ 特化 `skills/pm-deep-research/prompts/layer1/task-decomposition.md`（竞品变体）：**Step 1 强制推断 decision_intent**（6 意图表）→ Step 2 复杂度路由 → Step 3 五维 aspect（scope/boundaries/success_criteria 取自规格 §3 各维证据标准）→ Step 4 预算+策略；输出 `DeepResearchRequest` 含 decision_intent/complexity_tier 回显。
- 预算映射（接口 §5）：tier → budget + evidence_policy（`require_evidence_for_findings` 恒开；Deep `min_evidence_per_finding=2`）。**预算 timeout 决议**：per-aspect `timeout_ms` 恒 600000（D3 实测约束）；因此 `total_timeout_ms = ceil(max_agents/max_concurrent_agents) × 600000`（quick 660000 / standard·deep 1260000）——**覆盖接口 §5 表里的占位 total_timeout 值**（该表自标"示意/调参"）；待 WS-G 实跑后再校。
- SKILL.md 资产状态 + 横幅已更新（WS-B 标 ✅；仍未端到端可跑，待 WS-C/D/E）。

### WS-C · 报告装配 + 自验证 ✅（2026-05-29）
- ✅ 特化 `skills/pm-deep-research/prompts/layer1/final-report.md` → **13 章产品报告模板** + 五维→13 章映射（规格 §7.1）+ 裁剪规则（§7.2）+ **§7.4 行文规范作硬 floor**（BLUF/SCQA、标题即论点、表格作证据、按主题综合、给中心命名、吸收反论、校准不确定性、收尾给行动）。
- ✅ 分三相：Phase A 综合前 gap 审计（规格 §9.1，含 Build build-cost gap + failed_aspects；补搜 Std≤1/Deep≤2 轮有终止）；Phase B 13 章装配（从 `Finding.claim` 解析矩阵/Kano/ODI/build-cost；Ch7 视觉证据装配；Ch9 数值 ODI + build-cost 复杂度列；Ch13 4-tier 标签）；Phase C 综合后 quality floor 自验证（§9.2 + §6.4），不达标标警告/弃权 + 写「自验证记录」。
- ✅ 全程依实测 `DeepResearchResult`/`AspectReport`/`Finding`/`Evidence` 字段名对齐（report.rs）；byte-equal 证据纪律不破。
- ↪ WS-E（4-tier 映射/视觉证据/CiteEval）方法已内联于本 prompt 的 Phase B/C；独立 Skill 侧自动化装配仍列 WS-E。

### WS-D · Skill 入口 ✅（2026-05-30）
- ✅ `skills/pm-deep-research/SKILL.md` 改写为**可运行**：去 NOT-RUNNABLE 横幅 → 标 M4 已验证（22/24）；加 Prerequisite（lapis MCP 工具 `mcp__lapis__deep_research`/`aspect_research` + 验证过的 budget/timeout/supports_findings gotcha）；step 6 具体化为调 MCP 工具 + 可用性/降级分支；step 8 引用 WS-E；资产状态全 ✅。
- ✅ 新建 `prompts/layer1/claude-only-degradation.md`：MCP 不可用/硬失败时 Claude 兼任 Layer1+aspect agent，直接调搜索 MCP（Grok 主/Exa 语义）跑五维 + **自执行证据纪律**（无 Lapis byte-equal 校验器，禁捏造 URL、双向引用、宁少但真）+ 走 WS-E/final-report；partial 不算降级。

### WS-E · 证据后处理（Skill 侧）✅（2026-05-30）
- ✅ 新建 `prompts/layer1/evidence-postprocess.md` 作接口 §4 的独立 step-7：`source_type`+域名 → 4-tier+展示标签；视觉证据装配（扫 evidence_index + `Finding.claim` 视觉块，Deep <5 触发 Layer-2 浏览器补抓的具体流程 Step B′）；关键 finding 抽样 CiteEval（supported/partial/unsupported → keep/降置信/移 Ch12）。provenance 不可变铁律 + untrusted 规则继承。deep_research 与 Claude-only 两路复用；final-report.md 消费其产物。

### WS-F · 结构重组（ROADMAP 要求，时机见 §3 D2）
- 抽离 Lapis 引擎源码、PM DeepResearch 改为 skill 层 + 安装器、README/品牌改 PM DeepResearch。**依赖**一键安装 Lapis（ADR-0002）与运行环境就绪。

### WS-G · 端到端验证（v2.0 验收）
- 用黄金样例课题（Strava AI 升级）实跑 → 按 12 维 rubric + 行文 floor 打分 → 对照黄金样例 23/24。
- **同时验证接口 §3 prompt 承载**：agent 是否照契约填 claim、是否漏视觉证据、是否需机器强校验 → 决定是否触发接口 §6 的"提需求给 4o3F"。

---

## 3. 关键决策 / 待 Heye 对齐（开工前）

| # | 决策 | 选项与建议 |
|---|---|---|
| **D1** | Skill 是**新建** PM DeepResearch 竞品 skill 还是**改造**现有 `deep-research.md`？| 建议**新建特化 skill**（复用 Lapis 调用约定），保留通用 deep-research 作 fallback/其它能力底座。 |
| **D2** | **结构重组**（WS-F：抽离引擎、改品牌）放 Phase 3 **前段**还是**后段/推迟**？| 建议**后段或推迟**——先把 prompt/skill 资产 + 端到端验证（WS-A~E,G）做完证明方法论站得住，再动目录大重组，避免边改结构边改逻辑。 |
| **D3** | **端到端实跑前置**：Lapis MCP server 现在能在 heyev100 跑起来吗？provider key 就绪吗？| 需确认（见 memory `lapis-config-truth`）。若暂不可用：**先用 Claude-only 降级路径验证方法论资产**（规格 §10，纯 prompt 能力），不阻塞 WS-A~E。 |
| **D4** | 验证范围：仅黄金样例 1 例，还是再加 1-2 例（如"差异化"意图）？| 建议 v2.0 先 1 例端到端达标，泛化留 Phase 2′。 |

**Heye 已拍（2026-05-29）**：
- **D1 = 新建特化 skill**（保留通用 deep-research 作 fallback）。
- **D2 = 前段先重组**（先做结构重组/改名，再开发逻辑）。
- **D3 = 先开工 M1 prompt 资产**（不依赖运行环境），并行核查 Lapis 运行就绪度。
- **D4** 后定（v2.0 先 1 例端到端）。

**D3 核查结果（2026-05-29 已验证，heyev100）**：Lapis **运行就绪**——
- 二进制 `target/release/lapis`（2026-05-28 构建，可执行）；`~/.cargo/bin/cargo` 可重建；我们未碰 `crates/`，故 2026-05-28 的 E2E 全绿仍成立。
- 配置 `~/.lapis/lapis.toml`：exa（`EXA_API_KEY`）/ grok（`XAI_API_KEY`, `grok-4.3`）/ openai（CPA `gpt-5.5`）；budget 服务端不限（-1）。
- key：`XAI_API_KEY`(len84, **team_blocked=false 健康**) / `EXA_API_KEY`(len36) / `LAPIS_OPENAI_API_KEY`(len59, 桥映射为 `OPENAI_API_KEY`) 均 SET。
- 桥 `~/.lapis/lapis-mcp-bridge.sh` 在；运行会话用 `claude mcp add lapis -- ssh ... lapis-mcp-bridge.sh` 注册（见 memory `lapis-config-truth`）。
- **结论：M4 可全功能实跑（非仅 Claude-only）**。注意 budget 坑：CPA+grok 较慢，per-aspect `timeout_ms` 用 **600000(10min)**，否则 `budget_exceeded`。

---

## 3b. 改名 + 结构重组执行计划（WS-F 前段，Heye 2026-05-29）

**改名**：skill 项目名 **FathomX→ PM DeepResearch**（PM = Product Manager）。约定：
- 展示名（品牌）：**PM DeepResearch**（原样大小写）。
- skill slug / 目录名：`pm-deep-research`。
- **Lapis 引擎不改名**（上游 4o3F 所有，我们消费）。
- GitHub 仓库 `Runa798/fathomx`：**暂不改名**（外部、会断 URL，且 remote 内嵌 PAT，需单独慎重决定）。

**目标层布局**（D1 自包含 skill + D2 重组）：
```
skills/pm-deep-research/
  SKILL.md                      # 竞品研究特化 skill（D1，品牌 PM DeepResearch）
  prompts/
    layer1/{task-decomposition, agent-allocation, final-report}.md
    layer2/{persona-experience-analyst, persona-strategist, aspect-agent, ...}.md
docs/ · README.md（改品牌）· LICENSE
# 移除 vendored 引擎：crates/ · Cargo.toml · Cargo.lock · lapis.example.toml（改由安装器拉上游）
```

**执行分解（按可逆性分级）**：
| 步 | 动作 | 可逆性 | 处理 |
|---|---|---|---|
| R1 | 新建 `skills/pm-deep-research/` + SKILL.md + M1 人格 prompt | 加法/可逆 | ✅ 已做（M1/WS-A）|
| R2 | 文本改品牌 FathomX→PM DeepResearch + 文件名 | git 可回滚 | ✅ 已做（Heye 定"正文+文件名一起改"；2 个 live 文件改名 + 全内链修复，已验证零断链；archive/_raw 历史草稿与 repo URL/历史 python 引用有意保留）|
| R3 | 移动现有 top-level `prompts/` 进 skill；改 README 品牌 | git 可回滚 | ⏳ 随 R4 一起（引擎抽离时）|
| R4 | **移除 vendored Lapis 引擎源码**（`crates/` 61 文件 + Cargo* + lapis.example.toml）| **高 blast-radius**（删整个引擎源码，靠 git 历史/上游可恢复）| ⏸ Heye 定：**暂留引擎，验证后再删**（保本地可跑 Lapis 做 M4；待安装器拉上游 + 验证通过再删）|

> R4 暂缓：删的是整个上游 Rust 引擎，且删后本地无法跑 Lapis 验证（安装器未就绪）。先验证、后抽离。

---

## 3d. 交叉审计结果与修订（2026-05-29，Codex + subagent）

进 WS-B 前对 Phase2/3 产出做 Codex + 独立 subagent 交叉审计：**无 Critical 捏造；改名干净；五维/13TM/ODI/4-tier/build-cost/byte-equal 证据纪律跨文档一致**。已修订的发现：

| 级别 | 发现 | 修订 |
|---|---|---|
| Critical | 视觉证据契约让 agent 把 media_type 写进 `Evidence.summary`，违反 byte-equal | 人格 / 接口§3 / 规格§6.2：provenance 逐字复制，视觉元数据进 `Finding.claim`，Skill 后处理装配 |
| Critical | 接口§5 budget 缺真实 `deep_research` 必填字段 | §5 补完整 budget 形状 + per-aspect `timeout_ms`=600000 |
| Critical | 黄金 Ch9 ODI 非数值（高/中/低+星）与规格矛盾 | Ch9 改数值 `Imp+max(0,Imp−Sat)` + estimated + TM-4；B4 才诚实达 2 |
| Warning | 规格§8 `source_type` 扩展枚举非 Lapis 合法值 | §8 标注为 Skill 后处理视图/上游需求；v2.0 仅 7 合法枚举 |
| Warning | 能力矩阵"每格有证据"但无 per-cell id | 人格要求 per-cell 内联 evidence id；黄金 B3 诚实降 2→1（总分 22/24）|
| Warning | experience 人格缺 contradictory-sources 行 | 已补，与 strategist 对齐 |
| Warning | strategist 引 TM-12 但其 TM 列表无 TM-12 | strategist 显式标注"借用 TM-12 做 build-cost" |
| Warning | SKILL.md 工作流写成可执行但 layer1 prompt 未建 | 加 "⚠️ NOT YET RUNNABLE (M1)" banner |
| Warning | Layer-2 浏览器边界未明 | 接口§4 / 规格§6.2 标为 Skill 层外部步骤，非 aspect agent 能力 |
| Info | 状态横幅仍写"草稿" | spec/rubric/接口/黄金 横幅更新为"已签收/审计修订" |
| Info | archive/README 断链到旧 spec 名 | 已修为 `pm-deep-research-*` |

**W3 → WS-B 指令（Dim-1 人格归属消歧）**：一个 Lapis aspect = 一个 `aspect_agent_prompt` = 一个人格，故规格§5.3 的"Strategist 框定 + Experience 做 JTBD"不能字面拆进同一 aspect。**WS-B `agent-allocation.md` 定：`job-and-competitive-set` aspect 归 Strategist 人格、JTBD 框定折叠进其 prompt**（或显式拆成两个 aspect）。

---

## 3e. M4 端到端实跑发现（2026-05-30，✅ 完成 6/6 + 打分）

黄金课题 Strava AI 升级实跑（6 aspect deep_research）。详细数据见 [`../../.m4-run/m4-findings.md`](../../.m4-run/m4-findings.md)。实跑工具：持久 stdin 的 MCP stdio 客户端 `.m4-run/mcp_call.py`（容器→SSH 桥→heyev100 lapis serve，**不必注册 MCP**）。

**承载验证 = 通过**：strategist/experience 人格在真实引擎上按契约产出——结构化块进 `Finding.claim`（数值 ODI `I+max(0,I-S)`+estimated、定位价值曲线、Christensen 威胁分级、build-cost 版本时间线）、TM-4 认识论标注、TM-11 `contradicted_by`、byte-equal 证据全过逐字校验。这是 Phase 3 退出标准 3 的关键正向信号。

**修复/发现（按性质）**：
| 级别 | 发现 | 处理 |
|---|---|---|
| 阻塞(引擎) | `MAX_SSE_EVENTS=4096` 硬编码且不可配（测试 `rejects_network_stream_knobs` 强制拒 toml），gpt-5.5 推理综合轮实测峰值 **6485** 事件撞顶 → `network_failed`。缩证据量无效。 | 本地补 `lapis-net` `MAX_SSE_EVENTS` 4096→65536 + 重建（峰值仅占 9.9%）；total-data 上限保持上游 8MB（曾误改 64MB 撞坏测试，已回退 86847f8）；已提上游 **[4o3F/Lapis#8](https://github.com/4o3F/Lapis/issues/8)** |
| 阻塞(本侧 bug) | `task-decomposition.md` 误写 `execution_policy.timeout_ms = total_timeout_ms`；deep 执行时每 aspect 按"≤ 自身 budget.timeout_ms(600000)"复校 → 全 aspect `budget_exceeded` | 改为 `execution_policy.timeout_ms = per-aspect 600000`（≤ total）；prompt 已订正含两层校验说明 |
| 承载缺陷(本侧) | `capability-and-importance` aspect `schema_validation_failed: supports_findings_mismatch`——agent `evidence.supports_findings` 与 finding `evidence_refs` 双向不一致 | 两人格补「双向一致 invariant + 返回前自检」；**订正后补跑 status=ok，脚本校验双向一致 OK=True → 已解决，非引擎缺陷** |
| 瞬时 | `positioning-whitespace` `provider_unavailable`（3 并发下 CPA/grok 抖动，retryable:false） | 重试即过（status=ok）；非方法论问题 |

**最终 deep 结果**：**6/6 完成**。先 partial 4/6（job-set / opportunity-gaps / build-cost / experience-paths，16 证据）→ 用订正人格单独补跑 capability + positioning 两 aspect → 合并为 `.m4-run/deep-golden-6of6.result.json`（6 aspect / 26 证据 / dangling=0）。

**M4-3 装配 + 打分（完成）**：
1. ✅ 6/6（补跑脚本 `build_failed_aspects.py` + 合并 `merge_six.py`，补跑 evidence id 加 `<aspect_id>:` 前缀对齐）。
2. ✅ 13 章报告 `.m4-run/golden-report-strava.md`（按 `final-report.md` 装配；Deep 全 13 章；中心思想「社交图谱日教练」）。
3. ✅ Rubric 打分 `.m4-run/m4-rubric-score.md`：**引擎产出 = 22/24**，与手写黄金同分但 **B3 1→2 提升**（能力矩阵每格带 per-cell 证据，扛住黄金头号待办）；扣分仅 A4=1（build-cost 仅 2 证据，max_search_calls 预算所致）+ C1=1（视觉 3<5，需 Layer-2 抓图）——均非方法缺陷。floor 全过、行文 floor 过、无捏造。
4. **结论：方法论由 prompt 承载在真引擎上稳，不需再给 4o3F 提方法论需求**（唯一阻塞性上游需求仍是工程 issue #8 SSE 上限）。剩余 A4/C1 在 Skill 层解决（搜索预算↑ + Deep 接 Layer-2 抓图）。
5. 下一步 → WS-D（skill 入口/降级收尾）+ WS-E（证据后处理独立化）；再进 v2.0 收口。

---

## 4. 建议顺序与里程碑

1. **M1 · 方法论资产** ✅：WS-A 人格 + WS-B 编排。
2. **M2 · 报告 + 证据** ✅：WS-C 13 章模板/自验证 + WS-E 证据后处理独立化（`evidence-postprocess.md`）。
3. **M3 · Skill 入口 + 降级** ✅：WS-D（SKILL.md 可运行 + `claude-only-degradation.md`）。
4. **M4 · 端到端验证** ✅：全功能实跑 6/6（Lapis 可用，§3e）；承载验证通过；13 章报告 rubric **22/24**（B3 较手写黄金提升）。
5. **M5 · 结构重组（可选/按 D2）**：WS-F — 待办。

M4 全功能跑已确认可行（D3 + §3e）。

---

## 5. 风险

- **prompt 承载不稳**（agent 不照契约填 claim / 漏视觉证据）→ 由 WS-G 实测暴露；兜底是接口 §6 提需求给 4o3F（不自己改引擎）。
- **运行环境**（Lapis MCP / provider key / 网络）→ 用 Claude-only 降级先行验证方法论，解耦"方法论正确性"与"引擎可用性"。
- **结构重组与逻辑开发交织**（D2）→ 建议分离时段，降低返工。
