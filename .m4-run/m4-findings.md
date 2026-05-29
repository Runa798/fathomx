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

## 端到端结果：partial（4/6 完成）

完成：job-and-competitive-set、opportunity-gaps、build-cost-version-history、experience-paths（16 证据，均 medium）。
失败 2：
1. `capability-and-importance` → **schema_validation_failed: supports_findings_mismatch at evidence[2]**。真实承载缺陷：experience-analyst agent 产出的 `evidence.supports_findings` 与 finding 的 `evidence_refs` 双向不一致。引擎强校验双向一致性 → 需在人格 prompt 强化该约束（也作为 agent 脆弱点记给 4o3F）。
2. `positioning-whitespace` → **provider_unavailable**（瞬时；3 并发下 CPA/grok 抖动）。重试大概率过；非方法论问题。

## 承载验证（M4-1 单 aspect + 本次 4 完成 aspect）

strategist/experience 人格均按契约产出：结构化块进 `Finding.claim`（定位价值曲线表、数值 ODI 表 `I+max(0,I-S)`+estimated、Christensen 威胁分级、build-cost 版本时间线）、TM-4 认识论标注、TM-11 `contradicted_by`、byte-equal 证据（status=ok 即过逐字校验）。
