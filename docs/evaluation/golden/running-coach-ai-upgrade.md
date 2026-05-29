# 黄金样例 · 跑步教练 App 竞品深度研究（AI 升级方向）

> Status: Phase 2 WS3 产出（2026-05-29）。这是 FathomX 竞品深度研究能力的**专家级参考产出**，用于校准 [`../rubric.md`](../rubric.md) 并证明"可信度远超普通 LLM"可证伪。
> 按 [`../../specs/fathomx-competitive-research-spec.md`](../../specs/fathomx-competitive-research-spec.md) 的五维骨架 + 13 章模板 + 证据完整性纪律产出。
> **证据纪律**：关键事实经主会话独立核实（HTTP+标题）；ODI 重要性/满意度为研究证据**估算**并显式标注；Grok 合成且未溯源的数字（如某些市占率/弃用率）**不进结论**，仅在 Ch12 列为"未采纳"。来源 tier/标签见 Ch13。

---

## Ch1 · 研究结论摘要

**决策意图**：替 **Strava**（社交/追踪龙头，1.35 亿+ 用户，教练能力是其公认最大产品缺口；2025-04 已收购 AI 训练计划领导者 Runna）判断——**AI 时代该建哪些 AI 教练能力？视野盲区在哪？**

**核心判断**：Strava 收购 Runna 补齐了"结构化训练计划"这块短板，但**真正的 AI 教练机会不在"再做一个自适应计划"**——那条赛道 Garmin/COROS/Runna 已拥挤。Strava 独有、别人无法复制的杠杆是**1.35 亿用户的群体活动数据 + 社交图谱**。最高价值的 AI 升级方向是把现有**只做"跑后总结"的 Athlete Intelligence**，升级为**前向的、利用群体智能的当日决策教练**。

**推荐方向（优先级见 Ch10）**：
- **P0**：把 Athlete Intelligence 从"事后摘要"升级为"**前向当日决策**"（今天该不该练/练多少），并接入 Runna 计划引擎做动态调整。这是补齐与 Garmin Daily Suggested Workouts 的最小差距。
- **P0**：**群体智能个性化**——"与你同等 VO₂max/配速的跑者，本周最有效的训练模式是什么"。这是 Strava 数据护城河的唯一 AI 变现路径，Garmin/WHOOP 设备生态**结构上无法复制**。
- **P1**：**多模态跑姿×计划闭环**（CV 发现问题→计划自动插入纠正训练→追踪）。全市场无人打通，是系统性空白。
- **P1/P2**：实时 AI 语音教练、伤病预测（受医疗责任与模型成熟度门控，见 Ch12）。

**整体置信度**：中-高。竞品功能现状、Strava-Runna 收购、各家 AI 落地状态均有一手来源核实；机会"重要性/满意度"为估算（标注）；"群体智能"机会的用户需求强度需一手验证。

**最大不确定性**：① Strava 整合 Runna 的速度与订阅策略未定（影响窗口期）；② 用户对"AI 当日决策"的真实付费意愿缺一手数据；③ 伤病预测的法律责任边界。

---

## Ch2 · 研究输入与边界

| 项 | 内容 |
|---|---|
| 目标产品 | Strava（作为"强社交/追踪、教练为缺口"的现有平台代表）|
| decision_intent | AI Upgrade（该建哪些 AI 教练能力 + 视野盲区）|
| 目标用户 | 新手减脂跑 / 进阶备赛 / 伤后恢复 / 习惯养成 跑者（Ch4）|
| 竞争集 | Runna、Garmin Coach、Nike Run Club、adidas Running、COROS、TrainingPeaks + 替代（WHOOP/Oura、真人教练、C25K、跑团）|
| 深度 | Deep（五维全覆盖 + 13 章）|
| 排除范围 | 骑行/铁三/力量训练专项；非英文市场细分；硬件本身评测 |

---

## Ch3 · 目标产品定位与现状（Strava）

**定位**：运动社交网络 + 活动追踪聚合层，靠网络效应（Segments、Kudos、好友排名）和多设备数据聚合立身。变现为订阅（美区约 $79.99/年，2025-07 起按国统一定价）。[T3-DCR]

**Cagan 速写**：

| 3 强项 | 3 弱项 |
|---|---|
| 1.35 亿+ 用户的社交图谱 + 群体活动数据（独有护城河）| 历史上"向后看"——无前向训练计划生成（收购 Runna 前的公认最大缺口）[T2-Strava][T3-Verge] |
| 多设备中立聚合（Garmin/Apple/COROS/Wahoo 数据都进 Strava）| 现有 AI（Athlete Intelligence）仅做**跑后**活动摘要，非前向处方 [T2-Strava] |
| 路线发现 / Segments 的不可替代体验 | 自身无穿戴传感器，readiness/HRV 依赖第三方推送 |

**战略事件（已核实）**：2025-04-17 Strava 官方宣布**收购 Runna**（金额未披露），CEO 明确表述动机是补齐"训练指导=训练计划"的最大缺口；两 App 短期独立运营。[T2-Strava][T3-Verge][T3-Times]

---

## Ch4 · 用户人群与 JTBD（维度 1）

| 跑者类型 | Job statement（situation→motivation→outcome）|
|---|---|
| 新手减脂跑 | 刚决定跑步减重，怕受伤又怕没效果 → 要一个"今天跑什么"的计划，8 周能跑完 5K 且看到体重变化 |
| 进阶备赛 | 报名半马/全马，有基础但缺系统周期 → 按赛事倒计时自动调量调配速，比当前预估快完赛 |
| 伤后恢复 | 伤痊愈、医生说可复跑，怕再伤又怕停太久 → 渐进复跑方案 + 每日症状检查，安全回到赛前量 |
| 习惯养成 | 反复"三天打鱼" → 小承诺 + 即时反馈 + 社群打卡，30 天内成默认习惯 |

**真实竞争集的洞察（TM-1）**：跑者雇的不是"一个 App"，而是"被靠谱地教练"。因此真实对手包括**真人教练 + TrainingPeaks**（高信任高价）、**WHOOP/Oura 的当日 readiness 建议**（替代"今天该不该跑"的决策）、甚至**跑团的社群问责**（习惯养成 job）。Strava 的 AI 升级若只对标跑步 App，会错失"当日决策"这个被穿戴设备占据的战场。

---

## Ch5 · 竞品与替代方案图谱（维度 1 + 5）

**竞争集**（纳入理由+证据见 Ch13）：直接=Runna / Garmin Coach / NRC / adidas / COROS / TrainingPeaks；间接=Strava 自身付费、WHOOP/Oura；替代=真人教练、C25K、跑团。

**定位轴**（buyer-validated）：① 社交动机 ↔ 结构化训练；② 休闲大众 ↔ 竞技精英；③ 免费 ↔ 专业付费。

| 玩家 | 社交 | 人群 | 付费 | 核心差异化 |
|---|---|---|---|---|
| Strava | 强 | 大众偏中 | 免费+订阅 | 网络效应、群体数据 |
| Runna(并入) | 弱 | 业余→进阶 | $119.99/年 | AI 自适应计划（人类教练设计+AI 调整）|
| Garmin Coach | 弱 | 进阶→竞技 | 免费(绑设备)+Connect+ | 生理指标深度(HRV/VO₂)、Daily Suggested Workouts |
| COROS | 弱 | 进阶→竞技 | 免费(绑设备) | EvoLab 负荷分析、性价比 |
| NRC | 中 | 大众 | 免费 | 品牌 + 音频引导跑 |
| TrainingPeaks | 弱 | 竞技/教练 | 高价订阅 | 教练-运动员协同、TSS/CTL |

**白地（无人很好占据）**：
1. **大众跑者的"前向当日 AI 决策教练"**（社交中段 × 大众 × 合理付费）：既非 Garmin 式硬件绑定，也非 Runna 式计划自适应，而是**对话式 + 群体数据驱动的当日决策**。依据：Strava CEO 承认计划是最大空缺 [T3-Verge]；当日 readiness 决策目前被 Garmin/WHOOP（需买硬件）垄断。
2. **无硬件绑定的跑姿实时反馈**：手机 CV 路线，垂类 app（Ochy/GaitLab）已证可行，主流教练 app 无人原生集成。

**威胁分级（Christensen）**：

| 玩家 | 威胁 | 理由 |
|---|---|---|
| Strava+Runna 整合体 | （对外）颠覆性 | 用户基数 × AI 教练 = 一站式替代"社交平台+外部教练 app"组合 [T3-Verge] |
| Garmin（+Connect+ 订阅）| 维持性 | Training Readiness/HRV 锁住进阶硬件用户，但设备绑定限制大众渗透 |
| COROS | 维持性 | 低价提供接近 Garmin 的生理分析，蚕食 Garmin 进阶份额，对社交平台威胁有限 |
| AI 原生新进者（LLM 教练）| 潜在颠覆性（推测）| LLM 降低了训练 AI 门槛，可能出现不依赖设备/大社区的轻量颠覆者（无具体产品证据，标推测）|

---

## Ch6 · 功能架构与体验路径（维度 2 + 3）

**AI 教练能力对位矩阵**（✅最佳/🔵基础/❌缺失；证据编号见 Ch13）：

| 能力 | Runna | adidas | NRC | Garmin | COROS | Strava | TrainingPeaks |
|---|---|---|---|---|---|---|---|
| 自适应训练计划 | ✅(人设计+AI调) | 🔵 | 🔵(偏静态) | ✅(每日重排) | ✅ | ❌ | ✅(负荷模型) |
| 实时配速/语音 | ✅(in-ear) | 🔵(规则) | ✅(人录) | 🔵(表端) | 🔵 | ❌ | ❌ |
| 跑姿/动作分析 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 恢复/就绪度 | 🔵 | ❌ | ❌ | ✅(Body Battery/免费) | ✅(EvoLab/免费) | ✅(Relative Effort/付费) | ✅(TSB) |
| 个性化(穿戴) | ✅ | 🔵 | 🔵 | ✅(原生最深) | ✅(原生) | ✅(聚合) | ✅ |
| AI 对话教练 | 🔵(入口有限) | ❌ | ❌ | ❌ | ❌ | 🔵(仅跑后摘要) | ❌ |
| 计划生成 | ✅ | ✅ | ✅ | ✅(无全马) | ✅ | ❌ | ✅(最强构建) |
| 社交/激励 | 🔵 | 🔵 | ✅ | 🔵 | 🔵 | ✅(最强) | ❌ |

**两个事实底座**：(a) **跑姿分析全行业空白**（7 家主流无一原生集成，垂类 Ochy/GaitLab 已证可行）；(b) **Strava 在"自适应计划/对话教练"上是空白**，但在"社交/聚合"上独强——收购 Runna 正是补 (b) 的前半。

**Kano 分级**：

| 功能 | Kano | 依据 |
|---|---|---|
| 实时语音/配速指导 | Must-be | NRC 免费、Runna 标配；已成主流标配 [T3-RW] |
| 自适应训练计划 | Performance→快速 Must-be 化 | 3+ 竞品提供，用户期待升高 [T3-RW] |
| 恢复/就绪度建议 | Performance | Garmin/COROS/TP 已深做，用户主动提"该不该休息"价值 |
| AI 对话式教练 | Attractive | 仅 Runna 有限入口；用户尚未普遍预期 |
| 跑姿实时反馈 | Attractive | 全主流空白，蓝海（尤其进阶细分）|

---

## Ch7 · 视觉证据资产表

> 以下为**可核实的视觉证据指针 URL**（应用商店截图页/官方功能图/权威评测含 UI）。生产中由 Layer 2 浏览器抓取实际帧；本样例提供可访问 URL + 观察点 + 关联结论（满足规格 §6.2 source_url 要求）。

| # | media_type | source_url | observed_feature | related_claim | 标签 |
|---|---|---|---|---|---|
| V1 | official_page | runna.com/pricing-2 | Runna 计划+定价对比 | Runna 计划由人类教练设计+AI 调整 | High |
| V2 | app_store_image | apps.apple.com/.../adidas-runtastic-...id336599882 | adidas Running 功能截图+评分 | adidas 计划为规则驱动自适应 | High |
| V3 | official_page | garmin.com/.../garmin-coach/overview | Garmin Coach 功能图 | Garmin Coach 覆盖 5K/10K/半马，无全马 | High |
| V4 | official_page | press.strava.com/articles/stravas-athlete-intelligence... | Athlete Intelligence 功能说明 | Strava AI 仅跑后摘要，非前向 | High |
| V5 | video/review | dcrainmaker.com/2025/03/garmin-connect-plus-subscription-walkthrough.html | Connect+ UI 走查 | Connect+ Active Intelligence 为洞察摘要非对话 | Medium |
| V6 | review | runnersworld.com/training/a69110486/runna-app-review-i-tried-it/ | Runna 实测含界面 | in-ear 实时配速指导有效 | Medium |
| V7 | app_store_image | apps.apple.com/us/app/.../ochy-id1531481638 | Ochy 跑姿分析 60s 报告 | 手机 CV 跑姿分析技术可行 | High |

> **缺口（显式标注）**：本样例未实际渲染截图（需 Layer 2 浏览器）；Deep 模式生产应抓取 ≥5 帧实际图像。当前 7 条 URL 指针满足证据可追溯，但"实图"为 to-capture。

---

## Ch8 · AI / 新能力映射（核心 · 决策意图落点）

| AI 能力 | 解决的 job | 真实产品案例（已核实） | 局限/风险 | 标签 |
|---|---|---|---|---|
| 生成式/LLM 对话教练 | 答疑/计划解释/激励 | **WHOOP Coach**（GPT-4，2023-09 上线，结合个人 HRV/睡眠/strain 对话，OpenAI zero-retention）[T2-WHOOP] | LLM 取悦倾向→不知伤史时给激进建议；零输入"一键生成"质量存疑（JSSM 2024 研究 n=22 教练：基础 prompt 计划未达专业水准）[T1-JSSM] | High |
| 自适应计划(穿戴驱动) | "睡眠差还按计划跑吗" | **Garmin Run Coach**（2024-09，每日基于 VO₂max/睡眠/恢复重排）；**Runna** 自适应引擎 [T2-Garmin] | Garmin 不覆盖全马；理由解释生硬 | High |
| 计算机视觉跑姿分析 | "我是否过度踩脚跟" | **Ochy**（已上线，60s 关节角度/步幅分析）；**GaitLab**（关联伤病给纠正计划）[T2-AppStore] | 2D 单摄像头有角度盲区；无主流教练 app 原生集成 | High |
| 传感器 readiness | "该休息还是硬练" | **WHOOP** Recovery、**Garmin** Training Readiness [T2-WHOOP/Garmin] | 跑步 app 端无自有传感器，依赖第三方推送 | High |
| 实时 AI 语音 | 跑中即时反馈 | **当前无主流 app 原生 AI 生成实时语音**（NRC/adidas 均预录）| LLM+语音延迟、BLE 音频质量 | Medium |
| 伤病风险预测 | "升量会受伤吗" | **学术**：Nature npj Digital Medicine 2026《Multidisciplinary prediction of running-related injuries using ML》(n=142, 随机森林 AUC≈0.78)[T1-Nature]；**产品端**：仅"负荷过高"代理告警，无个体级预测 | 个体前瞻预测仍是研究难题(最佳 AUC~0.78)；医疗责任灰区 | High(学术)/Low(产品) |

**各家 AI 现状（已核实）**：WHOOP Coach=真 GPT-4 对话；Garmin Run Coach=真自适应；Strava Athlete Intelligence=**仅跑后摘要**（2024-10 公测→2025-02 GA），**无前向计划/对话/伤病预测**；adidas/NRC=规则驱动+人录音频，无实质 AI 对话。[T2-Strava]

---

## Ch9 · 产品机会矩阵（维度 4 · ODI）

**机会缺口（ODI；重要性/满意度为研究证据估算，标 [估]）**：

| Desired Outcome | 重要性[估] | 满意度[估] | 机会 | 依据 |
|---|---|---|---|---|
| 不受伤前提下提升配速 | 高 | 低 | ★★★ | 用户高频抱怨"线性推量忽视疲劳"(社区线索, Low) |
| 知道今天该不该练/练多少 | 高 | 中 | ★★ | Garmin/COROS 有但需买硬件；Strava 端空白 |
| 计划随生活变化自动调整 | 高 | 低 | ★★★ | TP 静态、Runna 被投诉调整不足(社区线索) |
| 实时跑姿纠正 | 中(进阶高) | 极低 | ★★★(细分) | 全主流空白 |
| 备赛计划与社交记录无缝打通 | 中 | 低 | ★★ | 并购前需双订阅；Runna CEO 点名"被多次移交"痛点 [T3-Verge] |

**机会矩阵（结论形态）**：

| 机会 | 对应 job | 用户价值 | 商业价值 | 复杂度 | 证据强度 | 风险 | 优先级 | 验证 |
|---|---|---|---|---|---|---|---|---|
| 群体智能个性化("同类人最有效模式") | 进阶备赛/提升配速 | 高 | 高(独有护城河) | 中 | 中(需一手验证需求) | 隐私 | **P0** | 灰度 A/B + 付费意愿调研 |
| Athlete Intelligence 前向化(当日决策) | 当日该不该练 | 高 | 高 | 中 | 高(对标 Garmin DSW) | LLM 误导 | **P0** | 与 Garmin DSW 盲测对比 |
| 跑姿×计划闭环 | 跑姿纠正 | 中-高(进阶) | 中 | 高(CV) | 高(技术可行) | 准确度 | **P1** | 与 Ochy 类合作 PoC |
| 实时 AI 语音教练 | 跑中反馈 | 中 | 中 | 高(延迟) | 中 | 体验 | **P1** | 延迟<300ms 原型 |
| 伤病预测 | 防伤 | 高 | 中 | 高 | 中(学术 AUC~0.78) | **医疗责任** | **P2** | 学术合作+免责设计 |

---

## Ch10 · Roadmap 建议

- **P0（确定性高、价值明、可控）**：① Athlete Intelligence 前向化（接 Runna 计划引擎做当日动态调整）；② 群体智能个性化 v1（"与你同 VO₂max 跑者的有效模式"，纯数据+推荐，不下医疗处方）。依赖：Runna 整合进度、数据管线。
- **P1**：③ 跑姿×计划闭环（与 CV 垂类合作 PoC，先进阶细分）；④ 实时 AI 语音教练原型（验证延迟与体验）。
- **P2**：⑤ 伤病预测（学术合作 + 法律/免责设计成熟后）。

---

## Ch11 · 验证实验与指标

| 指标 | 定义 | 计算 | 数据源 | 成功标准 |
|---|---|---|---|---|
| AI 教练激活率 | 体验过前向当日建议的订阅者占比 | 体验用户/订阅用户 | 埋点 | 较基线 +X% |
| 当日建议采纳率 | 按 AI 当日建议执行的比例 | 采纳次数/建议次数 | 埋点 | ≥某阈值 |
| 群体推荐采纳留存 | 用群体推荐者的 D30 留存 | D30 活跃/采纳用户 | 埋点 | 高于对照组 |
| 计划-社交打通转化 | Runna 计划在 Strava 内完成率 | 完成/启动 | 整合埋点 | 较双 app 时期提升 |
| AI 建议安全事件率 | AI 建议关联的过训/伤病投诉率 | 投诉/建议 | 客服+埋点 | 低于护栏阈值（护栏指标）|

---

## Ch12 · 风险、冲突与开放问题

- **AI 风险**：LLM 取悦倾向给激进计划（需接伤史/护栏）；医疗建议法律灰区（伤病预测受此门控）；健康数据隐私（WHOOP 用 zero-retention，非行业标准）；零输入计划质量不足（JSSM 2024）。
- **冲突/存疑（诚实标注，未采纳为结论）**：
  - Grok 合成但**未溯源**的数字——COROS 市占 8%→14%、"67% 用户两周放弃跑姿功能"、"12% 顶级 app 有实时反馈"、COROS EvoLab "AUC 85%"、Strava "2025-03 AI 训练计划/对话 chat"——**一律未采纳**（Tier 4/Unknown），仅作"待一手核实"线索。
  - NRC 是否有隐性付费墙：评测说法矛盾，置信度 Low。
  - Strava 美区最新年费确切数字：以官网 2025-07 调价公告为准，横向对比文章的 $79.99 为 Medium。
- **开放问题**：用户对"AI 当日决策/群体智能"的真实付费意愿（需一手调研）；Strava-Runna 整合时间表与订阅策略。

---

## Ch13 · 附录：来源与搜索记录

**搜索方法**：Wide Research——4 个独立子代理（grok web_search + exa web_search/company_research）并行覆盖五维；主会话独立核实承重引用（HTTP+标题）。

**来源表（节选，带 tier/标签）**：

| 标签 | tier | 来源 | URL | 核实 |
|---|---|---|---|---|
| T2-Strava | 2/High | Strava 官方新闻稿/支持 | press.strava.com/articles/strava-to-acquire-runna... | ✅标题核实 |
| T1-Nature | 1/High | npj Digital Medicine 2026 伤病预测 ML | nature.com/articles/s41746-026-02413-y | ✅标题核实 |
| T2-WHOOP | 2/High | WHOOP Coach 官方发布 | whoop.com/.../whoop-unveils-the-new-whoop-coach-powered-by-openai | ✅标题核实 |
| T1-JSSM | 1/High* | JSSM ChatGPT 计划质量研究 | jssm.org/jssm-23-56.xml | ⚠️期刊页 200，文章标题未独立确认 |
| T2-Garmin | 2/High | Garmin Run Coach 自适应发布 | garmin.com/.../personalized-garmin-coach... | 子代理取证 |
| T2-AppStore | 2/High | Ochy/GaitLab/adidas App Store 页 | apps.apple.com/... | 子代理取证 |
| T3-Verge | 3/Medium | The Verge 收购报道(含 CEO 引语) | theverge.com/tech/648075/... | 子代理取证 |
| T3-Times | 3/Medium | The Times 收购报道 | thetimes.com/.../strava-snaps-up-...runna... | 子代理取证 |
| T3-RW | 3/Medium | Runner's World Runna 评测 | runnersworld.com/training/a69110486/... | 子代理取证 |
| T3-DCR | 3/Medium | DC Rainmaker Connect+ 评测 | dcrainmaker.com/2025/03/... | 子代理取证 |
| (社区) | 3-community/Low | App Store 评论 / Reddit(经 Grok) | — | 仅作情绪/线索 |

\* JSSM 文章具体标题未在主会话独立确认，按 Medium 实际对待。

---

## 附 · 12 维 Rubric 自评（[`../rubric.md`](../rubric.md)）

| 维 | 分 | 说明 |
|---|---|---|
| A1 引用充分性 ⛔ | 2 | 关键声明基本带来源 |
| A2 引用准确性 ⛔ | 2 | 承重引用主会话独立核实 |
| A3 无支撑率 ⛔ | 2 | 未核实数字一律剔出结论(Ch12) |
| A4 来源质量/多样性 ⛔ | 2 | 官方+学术+媒体+社区分层 |
| A5 置信度/认识论标注 ⛔ | 2 | [估]/Tier/Low 全程标注 |
| B1 五维覆盖 ⛔ | 2 | 五维 + 支撑段齐全 |
| B2 真实竞争集 | 2 | 含 WHOOP/真人教练/跑团非显性竞争者 |
| B3 能力矩阵带证据 ⛔ | 1 | 矩阵有证据编号，但部分格证据较薄(改进点) |
| B4 ODI/Kano | 2 | 完整公式思路 + Kano + 估算标注 |
| C1 视觉证据 ⛔ | 1 | 7 条 URL 指针达标，但未渲染实图(需 Layer 2) |
| C2 产品味(TM) | 2 | TM-1/5/8/11 + 群体智能洞察 |
| C3 可落地 ⛔ | 2 | 机会矩阵+Roadmap+指标(含护栏)齐 |
| **合计** | **22/24** | floor 全过；达黄金参考目标线 |

**对"远超普通 LLM"的证伪检验**：普通 LLM 单次作答此题，预期失分项——A2/A3（会引用 Grok 式未溯源数字甚至编造）、C1（无视觉证据 URL）、B3（无证据矩阵）、A5（不标估算/认识论）。本样例在这些项系统性拉开差距 ⇒ 价值主张**未被证伪**。
