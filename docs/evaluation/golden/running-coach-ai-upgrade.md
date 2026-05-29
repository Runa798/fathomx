# 黄金样例 · Strava 的 AI 教练升级方向（竞品深度研究）

> Status: Phase 2 WS3 产出（2026-05-29 改写为专家叙事；2026-05-29 交叉审计修订：ODI 数值化、B3 诚实降分，自评 23→**22/24**）。这是 PM DeepResearch 竞品深度研究能力的**专家级参考产出**，校准 [`../rubric.md`](../rubric.md)，并证明"可信度远超普通 LLM"可证伪。
> **写法**：本稿按规格 [`../../specs/pm-deep-research-competitive-research-spec.md`](../../specs/pm-deep-research-competitive-research-spec.md) §7.4「行文规范」改写——论点先行（BLUF/SCQA）、标题即论点、表格作论点下的证据而非论证本身、按主题综合而非逐竞品流水账。写法依据：Stratechery / Built for Mars / Lenny's / McKinsey 行动标题 / Minto Pyramid / Amazon 六页备忘录的真实惯例。
> **证据纪律**：关键事实经主会话独立核实（HTTP+标题）；ODI 重要性/满意度为研究证据**估算**并显式标注 [估]；Grok 合成且未溯源的数字（市占率、弃用率等）**不进结论**，仅在 Ch12 列为"未采纳"。本轮另修正三处事实（见 Ch12）：删除未经核实的 Athlete Intelligence "2025-02 GA"；"Garmin Run Coach" 更正为官方名 "Garmin Coach + Daily Suggested Workouts"；区分 Strava/Runna 单独定价与捆绑价。来源 tier/标签见 Ch13。

---

## Ch1 · 结论：Strava 真正的 AI 杠杆是"群体智能护城河"，不是再做一个自适应计划

**情境**：Strava 是运动社交与活动追踪的龙头——逾亿级注册运动员、靠 Segments / Kudos / 多设备聚合形成的网络效应立身。但所有人都同意，它最大的产品缺口是**教练能力**：它历史上只会"向后看"（记录、总结），不会"向前看"（今天该练什么）。

**冲突**：2025-04-17，Strava 官方宣布收购 AI 训练计划领导者 **Runna**（金额未披露，短期两 App 独立运营），CEO 明确说动机就是补"训练指导=训练计划"这块最大缺口。[T2-Strava][T3-DCR] 表面上，缺口已被收购填上了。

**问题**：那么 AI 时代，Strava 还该建哪些 AI 教练能力？哪里才是别人看不到、它却独有的盲区？

**核心判断**：收购 Runna 补上的是"结构化训练计划"——但**那条赛道已经拥挤**（Garmin、COROS、TrainingPeaks、Runna 自己都在做），再投一份"更好的自适应计划"只是追平，不是拉开。Strava 真正独有、对手**结构上无法复制**的资产，是逾亿用户的**群体活动数据 + 社交图谱**。我把围绕它的机会称为**「群体智能护城河」**：用"和你同等 VO₂max/配速/训练史的人，这周最有效的训练模式是什么"这类只有 Strava 数据规模才答得出的问题，去做个性化教练。这是设备厂商（Garmin/WHOOP）**买不到、攒不出**的东西——他们有传感器，没有社交规模。

由此推出两个 P0、两个 P1、一个 P2（依据见 Ch9，优先级见 Ch10）：

| 方向 | 为什么是它 | 优先级 |
|---|---|---|
| Athlete Intelligence **前向化**（从"跑后总结"升级为"今天该不该练/练多少"，接 Runna 计划引擎做动态调整）| 这是补齐与 Garmin Daily Suggested Workouts 的**最小差距**，技术路径清晰 | **P0** |
| **群体智能个性化**（"同类跑者最有效模式"）| Strava 数据护城河的**唯一 AI 变现路径**，设备生态无法复制 | **P0** |
| **多模态跑姿 × 计划闭环**（手机 CV 发现问题→计划自动插入纠正→追踪）| 全市场无人打通，系统性空白 | **P1** |
| 实时 AI 语音教练 | 体验差异化，但受延迟/音频质量门控 | **P1** |
| 伤病风险预测 | 价值高，但受医疗责任与模型成熟度门控（见 Ch12）| **P2** |

**置信度（校准）**：对"机会方向的判断"信心**中-高**——竞品功能现状、Runna 收购、各家 AI 落地状态均有一手来源核实；对"用户为群体智能/当日决策**付费**的意愿"信心**低**，缺一手数据，是最该先验证的假设。

**最大不确定性**：① Strava 整合 Runna 的速度与订阅策略未定，直接决定机会窗口期；② 用户对"AI 当日决策"的真实付费意愿无一手数据；③ 伤病预测的法律责任边界。

---

## Ch2 · 研究输入与边界

本报告把 Strava 当作"强社交/追踪、教练为缺口"的现有平台代表，决策意图是 **AI Upgrade**——该建哪些 AI 教练能力、盲区在哪。深度为 Deep（五维全覆盖 + 13 章 + 视觉证据）。竞争集、目标人群、排除范围如下：

| 项 | 内容 |
|---|---|
| 目标产品 | Strava |
| decision_intent | AI Upgrade |
| 目标用户 | 新手减脂跑 / 进阶备赛 / 伤后恢复 / 习惯养成（Ch4 展开）|
| 竞争集 | 直接：Runna、Garmin Coach、Nike Run Club、adidas Running、COROS、TrainingPeaks；替代：WHOOP/Oura、真人教练、C25K、跑团 |
| 排除范围 | 骑行/铁三/力量专项；非英文市场细分；硬件本身评测 |

---

## Ch3 · Strava 的护城河在"社交与聚合"，它的命门是"只会向后看"

Strava 的立身之本不是教练，而是**网络效应 + 中立聚合**：Segments 排名、Kudos、好友动态构成社交护城河；Garmin/Apple/COROS/Wahoo 的数据都回流进 Strava，使它成为运动数据的聚合层。变现靠订阅（美区个人年费约 $79.99，2025-07 起按国统一定价）。[T3-DCR][T3-pricing]

但同样的"聚合"基因带来命门：**它自己没有穿戴传感器，也从不生成前向计划**。把它的强弱并排看，缺口指向同一处——

| 3 强项（独有、难复制）| 3 弱项（结构性、指向同一缺口）|
|---|---|
| 逾亿用户的社交图谱 + 群体活动数据 | 历史上无前向训练计划生成——收购 Runna 前的公认最大缺口 [T2-Strava][T3-Verge] |
| 多设备中立聚合（竞品数据都进 Strava）| 现有 AI（Athlete Intelligence）**只做跑后摘要**，不是前向处方 [T2-Strava] |
| 路线发现 / Segments 的不可替代体验 | 自身无传感器，readiness/HRV 依赖第三方推送 |

**战略事件（已核实）**：2025-04-17 Strava 官方宣布收购 Runna，CEO 表述动机是补"训练指导=训练计划"的最大缺口，短期两 App 独立运营。[T2-Strava][T3-DCR][T3-Verge] 这印证了上表的判断：Strava 自己也认这块是命门，所以它**买**了一个，而不是从头建——这本身就是后文 build-cost 讨论的第一个数据点（Ch6）。

---

## Ch4 · 跑者雇的不是一个 App，而是"被靠谱地教练"——所以真正的对手在 App 之外

用 JTBD 看，跑者并不是在"挑一个跑步软件"，而是在"雇一个能靠谱地教练自己的东西"（TM-1）。这句话直接改变竞争集：能完成这个 job 的，不止跑步 App。

四类跑者的 job statement（情境→动机→结果）：

| 跑者类型 | Job statement |
|---|---|
| 新手减脂跑 | 刚决定跑步减重，怕受伤又怕没效果 → 要"今天跑什么"的计划，8 周跑完 5K 且看到体重变化 |
| 进阶备赛 | 报名半马/全马，有基础但缺系统周期 → 按赛事倒计时自动调量调配速，比当前预估更快完赛 |
| 伤后恢复 | 医生说可复跑，怕再伤又怕停太久 → 渐进复跑方案 + 每日症状检查，安全回到赛前量 |
| 习惯养成 | 反复"三天打鱼" → 小承诺 + 即时反馈 + 社群打卡，30 天内成默认习惯 |

**由此得到本章的关键洞察**：既然 job 是"被靠谱地教练"，真实对手就包括**真人教练 + TrainingPeaks**（高信任、高价）、**WHOOP/Oura 的当日 readiness 建议**（直接替代"今天该不该跑"的决策）、甚至**跑团的社群问责**（习惯养成 job 的现成解）。Strava 若只把 AI 升级对标其它跑步 App，就会错失"当日决策"这个**已经被穿戴设备占据**的战场——而这恰恰是 Ch5 白地的来源。

---

## Ch5 · 真正的对手是占据"当日决策"的穿戴设备，不是另一个跑步 App

把玩家放到三条**买家验证过**的轴上——社交动机↔结构化训练、休闲大众↔竞技精英、免费↔专业付费——格局立刻清楚：Strava 独占"强社交"一端，而"当日生理决策"一端被**绑定硬件**的 Garmin/COROS/WHOOP 占着。中间那块"大众跑者要的、不必买表的当日 AI 决策教练"几乎没人很好地占据。

下表是定位的证据底座（每格结论的来源见 Ch13），但请先记住上面的判断，再看表：

| 玩家 | 社交 | 人群 | 付费 | 核心差异化 |
|---|---|---|---|---|
| Strava | 强 | 大众偏中 | 免费+订阅($79.99/yr) | 网络效应、群体数据 |
| Runna（已被 Strava 收购）| 弱 | 业余→进阶 | $119/yr（与 Strava 捆绑约 $149.99/yr）| AI 自适应计划（人类教练设计 + AI 调整）|
| Garmin Coach + Daily Suggested Workouts | 弱 | 进阶→竞技 | 免费(绑设备)+Connect+ | 生理指标深度(HRV/VO₂)、每日自适应建议 |
| COROS（EvoLab）| 弱 | 进阶→竞技 | 免费(绑设备) | 负荷分析、性价比 |
| Nike Run Club | 中 | 大众 | 免费 | 品牌 + 音频引导跑 |
| TrainingPeaks | 弱 | 竞技/教练 | 高价订阅 | 教练-运动员协同、TSS/CTL |

**两块白地，命名出来才好讨论：**

1. **「大众跑者的前向当日 AI 决策教练」**（社交中段 × 大众 × 合理付费）：既不是 Garmin 式硬件绑定，也不是 Runna 式计划自适应，而是**对话式 + 群体数据驱动的当日决策**。为什么无人占据？因为它需要同时有大众社交规模（设备厂没有）和前向计划能力（Strava 收购 Runna 前没有）——而 Strava 现在两样都有了。[T2-Strava][T3-Verge]
2. **「无硬件绑定的实时跑姿反馈」**：手机 CV 路线已被垂类 app（Ochy/GaitLab）证明可行，但主流教练 app 无一原生集成（Ch6）。

**威胁分级（Christensen，按对 Strava 的意义排序）**：对 Strava 自己而言，**Strava+Runna 整合体**是对"社交平台 + 外部教练 app"这种组合的**颠覆性**替代（一站式）；**Garmin** 是**维持性**威胁——它用 Training Readiness/HRV 锁住进阶硬件用户，但设备绑定限制了大众渗透；**COROS** 同为维持性，低价蚕食 Garmin 进阶份额，对社交平台威胁有限。真正的**潜在颠覆者**是不依赖设备、不依赖大社区的 **AI 原生轻量教练**——LLM 降低了训练 AI 的门槛，但目前无具体产品证据，标推测。

---

## Ch6 · 能力版图：全行业在"对话教练/跑姿"上空白，而谁在认真投 AI——看版本历史就知道

先给本章的两个事实底座，再上矩阵：(a) **跑姿分析是全行业空白**——下表 7 家主流无一原生集成，只有垂类 Ochy/GaitLab 证明手机 CV 可行；(b) **Strava 在"自适应计划/对话教练"上是空白，但在"社交/聚合"上独强**——收购 Runna 补的是"自适应计划"那一格的前半（计划生成），"对话教练"与"跑姿"两格仍空。

AI 教练能力对位矩阵（✅最佳 / 🔵基础 / ❌缺失；证据编号见 Ch13）——它是上面判断的证据，不是判断本身：

| 能力 | Runna | adidas | NRC | Garmin | COROS | Strava | TrainingPeaks |
|---|---|---|---|---|---|---|---|
| 自适应训练计划 | ✅(人设计+AI调) | 🔵 | 🔵(偏静态) | ✅(每日重排) | ✅ | ❌ | ✅(负荷模型) |
| 实时配速/语音 | ✅(in-ear) | 🔵(规则) | ✅(人录) | 🔵(表端) | 🔵 | ❌ | ❌ |
| 跑姿/动作分析 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 恢复/就绪度 | 🔵 | ❌ | ❌ | ✅(免费) | ✅(EvoLab/免费) | ✅(Relative Effort/付费) | ✅(TSB) |
| 个性化(穿戴) | ✅ | 🔵 | 🔵 | ✅(原生最深) | ✅(原生) | ✅(聚合) | ✅ |
| AI 对话教练 | 🔵(入口有限) | ❌ | ❌ | ❌ | ❌ | 🔵(仅跑后摘要) | ❌ |
| 社交/激励 | 🔵 | 🔵 | ✅ | 🔵 | 🔵 | ✅(最强) | ❌ |

**哪些功能才真正影响用户（Kano）**：实时语音/配速指导已是 **Must-be**（NRC 免费、Runna 标配，成主流标配）[T3-RW]；自适应训练计划是 **Performance** 且正快速 Must-be 化（3+ 竞品提供，用户期待升高）；恢复/就绪度是 **Performance**（Garmin/COROS/TP 已深做）；AI 对话式教练仍是 **Attractive**（仅 Runna 有限入口，用户尚未普遍预期）；跑姿实时反馈是 **Attractive 蓝海**（全主流空白，尤其进阶细分）。

**该不该自己建？先看对手"实际动作"——版本历史是最硬的证据（点 1）**：判断 Strava 该不该自建某能力，不能只看用户价值，还要看**建设成本**；而竞品的 **App Store 版本历史 / release notes** 是其建设成本与真实优先级的可观测代理——营销说什么是"言"，版本里真正发了什么、发几版、隔多久发是"行"（TM-12 言行分离）。三条可核实的观察：

- **Strava 选择"买"而非"建"自适应计划**：它有逾亿用户和工程能力，却用收购补这块缺口（2025-04）。这是关于自适应计划 build-cost 的最强信号——连龙头都判断从头建不如买。**推论**：PM DeepResearch/任何新进者更不该把"再做一个自适应计划"当差异化。[T2-Strava]
- **Strava 的版本节奏显示 AI 仍是"摘要级"投入**：其 App Store 版本历史可查到持续的功能迭代（如近期版本的力量训练、设备 HR 串流等），但 Athlete Intelligence 自 2024-10 公测以来仍停留在**跑后摘要**形态，未见"前向决策/对话"级的版本条目。**推论**：前向化是一个**尚未被任何主流玩家在版本里兑现**的空白，窗口仍开。[T2-Strava 版本历史]
- **跑姿分析的 build-cost 由垂类标定**：Ochy/GaitLab 作为小团队已把手机 CV 跑姿做到上线（60s 关节角度/步幅分析），说明**技术可行且成本可控**，主流教练 app 的"空白"是**选择不做**而非"做不到"——这把"跑姿×计划闭环"从"高不可攀"重新定价为"P1 可经合作 PoC 验证"。[T2-AppStore]

> **方法与陷阱（诚实标注）**：版本历史是"已建成"的证据，但有盲区——营销化 release notes（"bug 修复与性能优化"）会隐藏真实工作量，灰度/feature flag 的功能常不写进 notes，6 周静默可能是大重构而非停滞。因此上面三条都用"节奏 + 内容 + 是否兑现到 GA"交叉判断，不靠单一版本号；精确的"几版才稳定"为 to-verify（需抓取完整 Version History 按 AI 关键词打标，见 Ch13）。

---

## Ch7 · 视觉证据资产表

涉及功能/体验/对比的结论须附视觉证据。以下是**可核实的视觉证据指针 URL**（应用商店截图页/官方功能图/权威评测含 UI）；生产中由 Layer 2 浏览器抓取实际帧，本样例提供可访问 URL + 观察点 + 关联结论（满足规格 §6.2 source_url 要求）。

| # | media_type | source_url | observed_feature | related_claim | 标签 |
|---|---|---|---|---|---|
| V1 | official_page | runna.com 定价/计划页 | Runna 计划+定价 | Runna 计划由人类教练设计 + AI 调整 | High |
| V2 | app_store_image | apps.apple.com/.../adidas-running id336599882 | adidas Running 功能截图 | adidas 计划为规则驱动自适应 | High |
| V3 | official_page | garmin.com/.../garmin-coach 概览 | Garmin Coach 功能图 | Garmin Coach 自适应计划 + 每日建议 | High |
| V4 | official_page | press.strava.com/.../athlete-intelligence... | Athlete Intelligence 功能说明 | Strava AI 仅跑后摘要，非前向 | High |
| V5 | review | dcrainmaker.com/2025/04/strava-acquires-runna-thoughts-forward.html | 收购解读 + Runna 流程走查 | 计划→推送至 Garmin/COROS/Apple 互操作 | Medium |
| V6 | review | runnersworld.com/.../runna-app-review-i-tried-it/ | Runna 6 周实测含界面 | in-ear 实时配速指导有效 | Medium |
| V7 | app_store_image | apps.apple.com/us/app/gaitlab.../id6755685826 | GaitLab 逐帧跑姿分析 | 手机 CV 跑姿分析技术可行 | High |

> **缺口（显式标注）**：本样例未实际渲染截图（需 Layer 2 浏览器）；Deep 模式生产应抓取 ≥5 帧实图。当前 7 条 URL 指针满足证据可追溯，但"实图"为 to-capture。

---

## Ch8 · AI 能力映射：哪些已被产品验证，哪些还是研究难题

把"AI 能做的"和"AI 现在真能做的"分开，是这章的纪律。按"已被真实产品验证"到"仍是研究难题"排列：

- **已被产品验证的对话教练**：**WHOOP Coach**（GPT-4，2023-09-26 上线，结合个人 HRV/睡眠/strain 对话，OpenAI zero-retention）是"LLM 教练真能落地"的实证 [T2-WHOOP]。局限：LLM 有取悦倾向，不知伤史时可能给激进建议；零输入"一键生成"质量存疑——有运动科学研究提示纯 prompt 计划达不到专业教练设计水准（JSSM，文章细节本轮未独立复核，按 Medium 对待）。
- **已被产品验证的自适应计划**：**Garmin Coach 自适应训练计划 + Daily Suggested Workouts**（2024-09-19 更新，基于 VO₂max/睡眠/恢复每日重排）与 **Runna** 自适应引擎 [T2-Garmin]。局限：Garmin 计划深但理由解释生硬；二者都需要么绑设备、要么单独订阅。
- **已被垂类验证的 CV 跑姿**：**Ochy**（pose-estimation CV）与 **GaitLab**（逐帧视频分析，关联伤病给纠正）均已上线 [T2-AppStore]。局限：2D 单摄像头有角度盲区；无主流教练 app 原生集成。
- **仍依赖第三方的 readiness**：**WHOOP** Recovery、**Garmin** Training Readiness 成熟，但跑步 app 端无自有传感器，必须依赖第三方推送 [T2-WHOOP/Garmin]。
- **尚无人原生做好的实时 AI 语音**：NRC/adidas 都是**预录**音频，**无主流 app 原生 AI 生成实时语音**——受 LLM+语音延迟、BLE 音频质量门控。
- **仍是研究难题的伤病预测**：学术上，Nature npj Digital Medicine 2026《Multidisciplinary prediction of running-related injuries using ML》报告随机森林 **AUC≈0.78**（0.781±0.016）[T1-Nature]；产品端只有"负荷过高"代理告警，无个体级前瞻预测。结论：个体伤病预测**仍是研究前沿**（最佳 AUC 仅 ~0.78），叠加医疗责任灰区，只能 P2。

**各家 AI 现状一句话核实**：WHOOP Coach = 真 GPT-4 对话；Garmin = 真自适应 + 每日建议；Strava Athlete Intelligence = **仅跑后摘要**（2024-10 公测；GA 时点本轮未独立核实，不锁定），无前向计划/对话/伤病预测；adidas/NRC = 规则驱动 + 人录音频，无实质 AI 对话。[T2-Strava]

---

## Ch9 · 机会矩阵：群体智能与前向化是唯二的 P0

用 ODI 给"期望结果"排序：**Opportunity = Importance + max(0, Importance − Satisfaction)**，量表 1–10，**>10 = 欠服务（机会）**。所有 Imp/Sat 为研究证据**估算**（标 [估] + TM-4 认识论），非一手问卷——这本身是最该一手验证的假设：

| Desired Outcome | Imp[估] | Sat[估] | **Opportunity** | 认识论(TM-4) | 依据 |
|---|---|---|---|---|---|
| 实时跑姿纠正（进阶细分）| 8 | 1 | **15** | 估算/推测 | 全主流空白；进阶需求强度待一手验证 |
| 不受伤前提下提升配速 | 9 | 4 | **14** | 估算/社区线索 | 高频抱怨"线性推量忽视疲劳"（社区, Low）|
| 计划随生活变化自动调整 | 8 | 3 | **13** | 估算/社区线索 | TP 静态、Runna 被投诉调整不足（社区）|
| 知道今天该不该练/练多少 | 8 | 5 | **11** | 估算 | Garmin/COROS 有但需买硬件；Strava 端空白 |
| 备赛计划与社交记录无缝打通 | 6 | 3 | **9** | 估算 | 并购前需双订阅；Runna CEO 点名"被多次移交"痛点 [T3-Verge] |

> **ODI 排的是"原始欠服务度"，不是最终优先级**：跑姿(15)虽 ODI 最高，但落到下面的机会矩阵会因**复杂度高 + 非护城河**降为 P1；当日决策(11)/群体智能虽 ODI 不是最高，却因**独有数据护城河 + 低复杂度**升为 P0。这正是 ODI（欠服务）× 商业价值 × build-cost 的综合，而非唯 ODI 论。

把它落成可执行的机会矩阵——注意**「复杂度」列优先用竞品迭代节奏（Ch6 版本历史）做 build-cost 代理**，而非团队臆测：

| 机会 | 对应 job | 用户价值 | 商业价值 | 复杂度（build-cost 依据）| 证据强度 | 风险 | 优先级 | 验证 |
|---|---|---|---|---|---|---|---|---|
| 群体智能个性化 | 进阶备赛/提升配速 | 高 | 高（独有护城河）| 中（数据已在手，难在推荐质量）| 中（需一手验证需求）| 隐私 | **P0** | 灰度 A/B + 付费意愿调研 |
| Athlete Intelligence 前向化 | 当日该不该练 | 高 | 高 | 中（对标 Garmin DSW；Strava 已有摘要底座 + Runna 引擎）| 高 | LLM 误导 | **P0** | 与 Garmin DSW 盲测对比 |
| 跑姿×计划闭环 | 跑姿纠正 | 中-高(进阶) | 中 | 高但**已被垂类标定可控**（Ochy/GaitLab 小团队已上线）| 高（技术可行）| 准确度 | **P1** | 与 Ochy 类合作 PoC |
| 实时 AI 语音教练 | 跑中反馈 | 中 | 中 | 高（延迟/音频；无人原生兑现）| 中 | 体验 | **P1** | 延迟<300ms 原型 |
| 伤病预测 | 防伤 | 高 | 中 | 高（研究前沿，AUC~0.78）| 中（学术）| **医疗责任** | **P2** | 学术合作 + 免责设计 |

---

## Ch10 · Roadmap：先把数据护城河变现，再扩体验前沿

- **P0（确定性高、价值明、可控）**：① **Athlete Intelligence 前向化**——接 Runna 计划引擎做当日动态调整，把"跑后摘要"变成"今天该不该练/练多少"；这是补齐与 Garmin Daily Suggested Workouts 的最小差距。② **群体智能个性化 v1**——"与你同 VO₂max 跑者的有效模式"，纯数据 + 推荐，不下医疗处方。依赖：Runna 整合进度、数据管线。
- **P1**：③ **跑姿×计划闭环**——与 CV 垂类合作 PoC，先打进阶细分（build-cost 已由 Ochy/GaitLab 标定为可控）；④ **实时 AI 语音教练原型**——先验证延迟与体验，不急上线。
- **P2**：⑤ **伤病预测**——待学术合作成熟 + 法律/免责设计到位再启动。

---

## Ch11 · 验证实验与指标

每个 P0 都配一个可证伪的指标，含一条护栏指标（防 AI 建议致害）：

| 指标 | 定义 | 计算 | 数据源 | 成功标准 |
|---|---|---|---|---|
| AI 教练激活率 | 体验过前向当日建议的订阅者占比 | 体验用户/订阅用户 | 埋点 | 较基线 +X% |
| 当日建议采纳率 | 按 AI 当日建议执行的比例 | 采纳次数/建议次数 | 埋点 | ≥阈值 |
| 群体推荐采纳留存 | 用群体推荐者的 D30 留存 | D30 活跃/采纳用户 | 埋点 | 高于对照组 |
| 计划-社交打通转化 | Runna 计划在 Strava 内完成率 | 完成/启动 | 整合埋点 | 较双 app 时期提升 |
| AI 建议安全事件率（护栏）| AI 建议关联的过训/伤病投诉率 | 投诉/建议 | 客服+埋点 | 低于护栏阈值 |

---

## Ch12 · 风险、冲突与开放问题（含本轮事实更正）

**AI 风险**：LLM 取悦倾向给激进计划（需接伤史 + 护栏）；医疗建议法律灰区（伤病预测受此门控）；健康数据隐私（WHOOP 用 zero-retention，但这不是行业标准）；零输入计划质量不足。

**本轮事实更正（先验真伪纪律）**：
- **删除** Athlete Intelligence "2025-02 GA"——独立核实只确认 2024-10 公测，无 GA 时点的一手来源，故不锁定。
- **更正** "Garmin Run Coach" → 官方名 **"Garmin Coach"（自适应计划）+ "Daily Suggested Workouts"**；"Run Coach" 非 Garmin 官方产品名。
- **区分定价**：Strava 单独 $79.99/yr、Runna 单独 $119/yr、**Strava+Runna 捆绑约 $149.99/yr（美区）**——不可混为一谈。
- 收购日期 **2025-04-17**（注意：无来源的合成答案曾误作 "4 月 29 日"，提示无溯源数字不可信）。

**未采纳（Grok 合成但未溯源，仅作待核实线索，Tier 4/Unknown）**：COROS 市占 8%→14%、"67% 用户两周放弃跑姿功能"、"12% 顶级 app 有实时反馈"、COROS EvoLab "AUC 85%"、Strava "2025-03 AI 训练计划/对话"——一律未进结论。

**开放问题**：用户对"AI 当日决策 / 群体智能"的真实付费意愿（需一手调研）；Strava-Runna 整合时间表与订阅策略；各竞品 AI 功能的**完整版本时间线**（Ch6 build-cost 推论需抓全 App Store Version History 才能从"节奏判断"升级为"几版才稳定"的定量）。

---

## Ch13 · 附录：来源与搜索记录

**搜索方法**：Wide Research——4 个独立子代理（grok web_search + exa web_search / company_research / advanced）并行覆盖五维 + 写法预研 + 版本历史；主会话独立核实承重引用（HTTP + 标题），并对子代理回传逐条交叉验真（已剔除 Grok 无溯源的市占/弃用率与误作的收购日期）。

| 标签 | tier | 来源 | URL | 核实 |
|---|---|---|---|---|
| T2-Strava | 2/High | Strava 官方新闻稿（收购 Runna）+ Athlete Intelligence 说明 + App Store 版本历史 | press.strava.com/articles/strava-to-acquire-runna... · apps.apple.com/.../id426826309 | ✅标题/页面核实 |
| T1-Nature | 1/High | npj Digital Medicine 2026 伤病预测 ML（RF AUC 0.781）| nature.com/articles/s41746-026-02413-y | ✅核实 |
| T2-WHOOP | 2/High | WHOOP Coach（GPT-4，2023-09-26）| businesswire.com/news/home/20230926899032/en/ | ✅核实 |
| T2-Garmin | 2/High | Garmin Coach 自适应 + Daily Suggested Workouts（2024-09-19）| garmin.com/.../personalized-garmin-coach... | ✅核实 |
| T2-AppStore | 2/High | Ochy / GaitLab / adidas App Store 页 | apps.apple.com/.../id6755685826（GaitLab）· ochy.io | ✅核实 |
| T3-DCR | 3/Medium | DC Rainmaker 收购解读（Runna 流程 + $119/yr）| dcrainmaker.com/2025/04/strava-acquires-runna-thoughts-forward.html | ✅核实 |
| T3-Verge | 3/Medium | The Verge 收购报道（含 CEO 引语）| theverge.com/.../strava-runna... | 子代理取证 |
| T3-RW | 3/Medium | Runner's World Runna 6 周实测 | runnersworld.com/training/a69110486/... | ✅核实 |
| T3-pricing | 3/Medium | Strava 定价（$79.99/yr 美区）| pricetimeline.com/data/price/strava | 子代理取证 |
| JSSM | Medium* | ChatGPT 训练计划质量研究 | jssm.org（文章细节未独立复核）| ⚠️按 Medium 对待 |
| (社区) | 3-community/Low | App Store 评论 / Reddit（经 Grok）| — | 仅作情绪/线索 |

\* JSSM 文章具体细节未在本轮独立确认，按 Medium 实际对待，不作强结论支撑。

---

## 附 · 12 维 Rubric 自评（[`../rubric.md`](../rubric.md)）

| 维 | 分 | 说明 |
|---|---|---|
| A1 引用充分性 ⛔ | 2 | 关键声明基本带来源标签 |
| A2 引用准确性 ⛔ | 2 | 承重引用主会话独立核实；本轮另修正 3 处事实 |
| A3 无支撑率 ⛔ | 2 | 未核实数字一律剔出结论（Ch12）|
| A4 来源质量/多样性 ⛔ | 2 | 官方+学术+媒体+社区+版本历史分层 |
| A5 置信度/认识论标注 ⛔ | 2 | [估]/Tier/Low + 校准的可能性vs信心（Ch1）|
| B1 五维覆盖 ⛔ | 2 | 五维 + 支撑段齐全 |
| B2 真实竞争集 | 2 | 含 WHOOP/真人教练/跑团非显性竞争者 |
| B3 能力矩阵带证据 ⛔ | 1 | 矩阵有 Ch13 来源指针 + Ch6 build-cost 证据，但单元格是符号化 ✅/🔵/❌、**无 per-cell 证据 id**——按 rubric"每格有证据"严格判 **1**；per-cell 证据加厚 = Deep 生产改进点（诚实降分，交叉审计 Codex W-a 指出）|
| B4 ODI/Kano | 2 | 完整公式 `Imp+max(0,Imp−Sat)` 数值化（Ch9）+ Kano（Ch6）+ 估算/TM-4 标注 |
| C1 视觉证据 ⛔ | 1 | 7 条 URL 指针达标（**视觉 URL 指针基准，非 Deep 生产实图**），未渲染实图需 Layer 2 |
| C2 产品味(TM) | 2 | TM-1/5/8/11/12 + 群体智能护城河洞察 |
| C3 可落地 ⛔ | 2 | 机会矩阵（复杂度用 build-cost 佐证）+Roadmap+护栏指标 |
| **合计** | **22/24** | floor 全过；行文 floor 过（论点先行、表格作证据、按主题综合）|

**对"远超普通 LLM"的证伪检验**：普通 LLM 单次作答此题，预期失分项——A2/A3（会引用 Grok 式未溯源数字甚至编造收购日期）、C1（无视觉证据 URL）、B3（无证据矩阵、更不会查版本历史做 build-cost）、B4（不会用 ODI 数值公式）、A5（不标估算/不分可能性与信心）、行文（堆功能清单而非论点先行）。本样例在这些项系统性拉开差距 ⇒ 价值主张**未被证伪**。未满分项 **C1（实图待 Layer 2）/ B3（per-cell 证据待加厚）**均为 Deep 生产期改进点，已显式标注，不掩饰。
