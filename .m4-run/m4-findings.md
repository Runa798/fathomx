# M4 端到端实跑发现（2026-05-30）

黄金课题：Strava AI 跑步教练升级（decision_intent=ai_upgrade，Deep + build-cost，6 aspect）。
线上：search=grok / model=openai(CPA gpt-5.5)；schema_version=0.1；服务端 budget 全 -1。

## SSE 事件用量（Heye 问：MAX_SSE_EVENTS 实际用多少）

原始日志：`.m4-run/deep-golden.result.json.err`（`lapis_core::net::reqwest_client=debug` 抽 "SSE upstream stream ended"）。

- 模型轮总数 19；`event_count`：min 13、**max 6485**、中位 ~213。
- **超旧上限 4096 的轮：4904 / 6485 / 4692**（3 个综合轮 = 生成完整 AspectResearchResult 的那几轮）。这正是补丁前全失败的原因。
- 峰值 `total_data_bytes` = 1.50 MB（旧 8MB 其实够；瓶颈一直是 event_count 不是字节）。

结论：
- 旧 4096 太低——结构化 deep 综合轮（含逐字证据 + 多张表）就要 ~4700–6500 事件。
- 新 65536：峰值 6485 = **9.9%**，约 10x 余量，安全且不浪费。**~16384 即够**；65536 给富输出留足。
- `MAX_SSE_TOTAL_DATA_BYTES` 8MB→64MB 非必需（峰值仅 1.5MB），但无害。
- 长期：作为需求提 4o3F（接口 §6）——逐字证据复制天然产大输出，引擎默认 4096 对 deep 综合偏紧。

## 端到端结果：6/6 完成（先 partial 4/6 → 订正人格补跑 2 → 合并）

第一次 deep 跑 partial（4/6）：job-and-competitive-set、opportunity-gaps、build-cost-version-history、experience-paths（16 证据，均 medium）。
两个失败 aspect 已用订正人格单独补跑（`aspect_research`）并合并到 6/6：
1. `capability-and-importance` → 首跑 **schema_validation_failed: supports_findings_mismatch at evidence[2]**。承载缺陷：experience-analyst agent 的 `evidence.supports_findings` 与 finding 的 `evidence_refs` 双向不一致。**修复 = 在两个人格 prompt 强化"双向引用不变式 + 返回前自检"**；补跑后 status=ok，脚本校验双向一致性 OK=True。**这是我方 prompt 问题，已修，非引擎缺陷。**
2. `positioning-whitespace` → 首跑 **provider_unavailable**（瞬时，3 并发下 CPA/grok 抖动）。直接重试即过（status=ok，5 findings + 价值曲线 + 威胁分级）。非方法论问题。

合并产物：`.m4-run/deep-golden-6of6.result.json`（6 aspect / 26 证据 / dangling=0）。补跑 aspect 的 evidence id 已加 `<aspect_id>:` 前缀对齐 deep_research 约定（脚本 `merge_six.py`）。

## 承载验证 + Rubric 打分（关键退出信号）

strategist/experience 人格均按契约产出：结构化块进 `Finding.claim`（定位价值曲线表、数值 ODI 表 `I+max(0,I-S)`+estimated、Christensen 威胁分级、build-cost 版本时间线、能力矩阵 per-cell 证据、体验路径矩阵 + 视觉块）、TM-1~13 系统出现、TM-4 认识论标注、TM-11 `contradicted_by`、byte-equal 证据（status=ok 即过逐字校验）。

**Rubric 实测（`.m4-run/m4-rubric-score.md`）：引擎产出报告 `.m4-run/golden-report-strava.md` = 22/24**，与手写黄金样例同分但形不同：
- **B3 1→2（提升）**：能力矩阵每格带 `evidence_refs`/`assumption`/`falsifiable_test`——人格 prompt 扛住了黄金样例头号待办（per-cell 证据）。Phase 3 退出标准 3（方法论可被 prompt 承载）最强正向证据。
- A4 2→1（预算 artifact）：build-cost aspect 仅 2 证据（max_search_calls=2），提搜索配额即修，非方法缺陷。
- C1 持平 1：3 条视觉 URL <5，需 Skill 层 Layer-2 抓图补；引擎已正确 abstain。

**结论：不需再给 4o3F 提方法论需求。** 引擎已承载 PM 方法论；剩余 A4/C1 都在 Skill 层解决（搜索预算 + Layer-2 抓图），与引擎无关。唯一阻塞性上游需求仍是工程 issue #8（SSE 上限）。
