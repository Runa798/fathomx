# Track A Verification + Gap-Fill: Orchestration & Research Credibility

**Generated:** 2026-05-29 (Beijing time)
**Scope:** Task 1 — Suspect citation verdicts; Task 2 — A5 dynamic budget heuristics; Task 3 — A1 source credibility practices

---

## Task 1 — Suspect Citation Verdicts

### 1A. The "23-31% MECE recall improvement" claim and its three attributed papers

| Citation claimed | Search verdict | Evidence |
|---|---|---|
| Chen et al. (2024) ACL — "MECE-constrained dimensional decomposition improves recall 23–31% over flat prompting in multi-document synthesis" | **LIKELY FABRICATED** | arXiv API query `ti:MECE AND ti:prompting AND ti:recall` → 0 results. arXiv query `all:MECE AND all:recall AND all:flat prompting` → 0 results. ACL Anthology 2024 main proceedings search finds no such paper. Grok MCP first hallucinated a confident description of this paper; when cross-examined it could not produce a URL or DOI. No paper exists. |
| Kumar & Patel (2025) IEEE TKDE — same claim | **FABRICATED** | Grok search explicitly returned: "No such paper exists. Extensive searches across IEEE Xplore, Google Scholar, DBLP, and academic indexes return zero results." No DOI or preprint found anywhere. |
| Li et al. (2023) JAIR — same claim | **FABRICATED** | No JAIR 2023 paper by Li et al. matching this title or method found via arXiv, Google Scholar, or JAIR's own search. Grok: "no authoritative citation card could be located." |
| **The 23-31% numeric claim itself** | **UNVERIFIABLE / LIKELY FABRICATED** | No real paper on arXiv, ACL Anthology, IEEE Xplore, or JAIR contains this specific numerical finding. The claim appears AI-synthesized. Should be **removed from FathomX documentation entirely**. |

**Bottom line:** All three citations and the numeric claim are fabrications that must be deleted. No real published work establishing a "23-31% MECE vs flat-prompting recall improvement" could be found anywhere. This is a canonical example of Grok/LLM confabulation of plausible-sounding academic claims.

---

### 1B. The "OpenReview ICLR 2026" papers — real venue check

| Paper name claimed | Real status | Real venue/arxiv | Notes |
|---|---|---|---|
| **APOLLO** (iterative research+edit multi-agent) | EXISTS but **DESK REJECTED** from ICLR 2026 | OpenReview ID: `vlqwNZWZv2`; no arxiv preprint found | Full title: "APOLLO: A Self-Guided Multi-Agent System for Scientific Article Generation Inspired by Human Thinking". Desk-rejected Oct 2025; not a valid published citation. Do NOT cite as ICLR 2026. |
| **DeepTRACE** (8-dimension deep-research audit, statement-level citation checking) | EXISTS — **ICLR 2026 Poster (accepted)** | arXiv: `2509.04499` (Sep 2, 2025); OpenReview: `QkaeTea16Y`; Microsoft Research publication | Authors: Pranav Narayanan Venkit, Philippe Laban, Yilun Zhou, Kung-Hsiang Huang, Yixin Mao, Chien-Sheng Wu. Real and citable. |
| **ResearchRubrics** (rubric benchmark for deep research agents) | EXISTS — **ICLR 2026 Poster (accepted)** | arXiv: `2511.07685` (Nov 10, 2025); OpenReview: `ErnvfmSX0P`; Scale AI | Authors: Manasi Sharma et al. Real and citable. |
| **DeepResearch Bench** | EXISTS — **ICLR 2026 Poster (accepted)** | arXiv: `2506.11763` (Jun 13, 2025); OpenReview: `hQ0K2Hhq7H` | Authors: Mingxuan Du, Benfeng Xu, Chiwei Zhu, et al. Real and citable. |

**Summary:** DeepTRACE, ResearchRubrics, and DeepResearch Bench are all real ICLR 2026 accepted papers with valid arXiv IDs. APOLLO was desk-rejected and should not be cited as an ICLR 2026 paper.

---

## Task 2 — A5 Dynamic Budget Allocation: Real Citable Heuristics

### 2A. Anthropic Engineering Blog (primary source)

**Source:** "How we built our multi-agent research system," Anthropic Engineering Blog, June 13, 2025.
**URL:** https://www.anthropic.com/engineering/multi-agent-research-system

**Concrete heuristics extracted:**

| Heuristic | Value | Notes |
|---|---|---|
| Subagent count by task complexity | Simple fact-finding: 1 agent (3–10 tool calls); Direct comparisons: 2–4 subagents (10–15 calls each); Complex research: 10+ subagents with divided responsibilities | Directly from the post |
| Default parallel fan-out | Lead agent spawns **3–5 subagents in parallel** as baseline | Post specifies "For speed, we introduced two kinds of parallelization: (1) the lead agent spins up 3-5 subagents in parallel" |
| Tool parallelism within each subagent | Each subagent uses **3+ tools in parallel** | Cuts research time "up to 90%" |
| Token cost multipliers | Chat baseline = 1×; Single agent = ~4×; Multi-agent = ~15× | Core cost-tradeoff data |
| Token budget explains variance | Token usage alone explains **80% of performance variance** on BrowseComp; model choice and tool-call count are the other two factors | Critical finding for budget allocation |
| Model upgrade vs. token doubling | Upgrading from Claude Sonnet 3.7 → Sonnet 4 gives larger gains than **doubling token budget** at 3.7 | Model quality is a more efficient lever than raw token spend |
| Multi-agent vs. single-agent threshold | +90.2% improvement on internal eval (Opus 4 lead + Sonnet 4 subagents vs. single Opus 4); economically viable only when task value justifies 15× token cost | |
| Poor fit for multi-agent | Coding tasks (fewer parallelizable subtasks), tasks requiring shared context across all agents | |

---

### 2B. Additional Citable Budget-Allocation Papers

**1. DAAO — Difficulty-Aware Agentic Orchestration**
- **Citation:** Su et al. (2025). "Difficulty-Aware Agentic Orchestration for Query-Specific Multi-Agent Workflows." arXiv:2509.11079. Accepted WWW 2026.
- **URL:** https://arxiv.org/abs/2509.11079
- **Heuristic:** Use a VAE-based difficulty estimator to predict query complexity, then dynamically allocate workflow depth. Simple queries → simpler single-agent workflows; complex queries → multi-agent strategies. Validated on 6 benchmarks with improved accuracy and inference efficiency over static multi-agent baselines.

**2. ParallelResearch — Tree-Structured Adaptive Resource Allocation**
- **Citation:** Nie, Lipka, Rossi, Chaudhuri (2025). "Efficient Tree-Structured Deep Research with Adaptive Resource Allocation." arXiv:2510.05145. ICLR 2026 Workshop on Agents in the Wild (Spotlight).
- **URL:** https://arxiv.org/abs/2510.05145
- **Heuristic:** Model deep research as a dynamic tree traversal; expand breadth or depth only when expected information gain exceeds overhead. Runtime orchestrator prunes low-value branches and reallocates to promising paths mid-research. Result: up to 5× speedup at comparable quality.

**3. ZEBRA — Zero-Shot Budget Allocation**
- **Citation:** (2025). "ZEBRA: Zero-shot Budgeted Resource Allocation for LLM Orchestration." arXiv:2605.20485.
- **URL:** https://arxiv.org/abs/2605.20485
- **Heuristic:** Model per-phase utility as a saturating-exponential curve; solve as a continuous nonlinear knapsack (water-filling) to allocate a fixed total budget across pipeline phases before execution. Zero-shot, no fine-tuning required.

**4. Plan-and-Budget — Test-Time Reasoning Budget**
- **Citation:** (2025). "Plan and Budget: Effective and Efficient Test-Time Scaling on Large Language Model Reasoning." arXiv:2505.16122.
- **URL:** https://arxiv.org/abs/2505.16122
- **Heuristic:** Decompose complex queries into sub-questions; allocate token budgets per sub-question based on estimated local complexity using adaptive scheduling. Achieves up to 70% accuracy gains and 39% token reduction vs. fixed-budget approaches.

**5. Inference-Time Budget Control for Search Agents**
- **Citation:** (2025). "Inference-Time Budget Control for LLM Search Agents." arXiv:2605.05701.
- **URL:** https://arxiv.org/abs/2605.05701
- **Heuristic:** Under explicit tool-call and output-token budgets, control what action to take next (retrieve, decompose, or answer directly) and when to commit a final answer. Naive scaling leads to over-search and diminishing returns; action-level budget control outperforms token-level-only constraints.

**6. Anthropic "Building Effective Agents" — Foundational Guidance**
- **Citation:** Anthropic Engineering Blog, December 19, 2024. "Building Effective AI Agents."
- **URL:** https://www.anthropic.com/research/building-effective-agents
- **Heuristic:** Use the simplest approach that works; add multi-agent complexity only when single-agent + retrieval is insufficient. Agents trade latency and cost for task performance — make this tradeoff explicit.

---

## Task 3 — A1 Source Credibility: Real Citable Practices

### 3A. Atomic-Claim Factuality Evaluation (FActScore family)

| Paper | Citation | Key Practice |
|---|---|---|
| **FActScore** | Min et al. (2023). "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation." EMNLP 2023. arXiv:2305.14251. | Decompose output into atomic facts → verify each against a trusted knowledge source → score as percentage supported. Standard practice for factuality evaluation in RAG systems. |
| **CiteEval / CiteBench** | (2025). "CiteEval: Principle-Driven Citation Evaluation for Source Attribution." ACL 2025 long paper. https://aclanthology.org/2025.acl-long.1574 | Beyond NLI-based binary support: evaluate citation quality within full retrieval context including query and generated text. Introduces CiteBench multi-domain benchmark with human annotations. |
| **Citation Faithfulness vs. Correctness** | (2025). "Correctness is not Faithfulness in Retrieval Augmented Generation Attributions." ACM SIGIR ICTIR 2025. https://dl.acm.org/doi/10.1145/3731120.3744592 | Up to **57% of citations lack faithfulness** (post-rationalized rather than genuinely grounded). Both citation correctness AND faithfulness must be evaluated. |

### 3B. Deep Research System Auditing

| Paper | Citation | Key Practice |
|---|---|---|
| **DeepTRACE** | Venkit et al. (2025). arXiv:2509.04499. ICLR 2026 Poster. | Eight-dimension audit framework: answer-text dimensions (confidence, one-sidedness), source dimensions (source count, source quality), citation dimensions (citation thoroughness, citation accuracy, unsupported-statement rate, citation necessity). Citation accuracy ranges 40–80% across production systems. Deep research reduces overconfidence but not one-sidedness. |
| **Web Search Credibility Evaluation** | (2026). "Assessing Web Search Credibility and Response Groundedness in Chat Assistants." EACL 2026. https://aclanthology.org/2026.eacl-long.115 | Evaluates source credibility + groundedness across GPT-4o, GPT-5, Perplexity, Qwen. Perplexity achieves highest source credibility; GPT-4o shows elevated citation of non-credible sources on sensitive topics. Systematic source credibility scoring is necessary. |

### 3C. CRAAP / SIFT Information Literacy Frameworks

| Framework | Reference | Criteria |
|---|---|---|
| **CRAAP Test** | Blakeslee, S. (2004, extended). Currency, Relevance, Authority, Accuracy, Purpose. Standard academic information literacy framework. | Source evaluation along 5 axes: how recent, how relevant, who produced it, how accurate, what purpose/bias. |
| **SIFT** | Caulfield, M. (2019). "SIFT (The Four Moves)." WebLiteracy.ca. | Stop; Investigate the source; Find better coverage; Trace claims to original source. Designed for quick lateral reading / source verification. |
| **ZODIAC** | (2025). "ZODIAC of information evaluation for a generative AI-dominated information environment." Journal of New Librarianship. | AI-specific extension: Zooming in, Other opinions, Dataset, Intent, Authenticity, Consistency. Addresses AI-generated content specifically. |

### 3D. Practical Source-Tiering Recommendations for FathomX

Based on real deployed deep research systems and the academic literature above, the following source-tiering approach is grounded in real practice:

**Tier 1 (highest credibility):** Peer-reviewed journals and conference proceedings (arXiv with venue confirmation, ACL Anthology, IEEE Xplore, PubMed). Cross-verify author affiliations; check actual venue acceptance status (not just "under review").

**Tier 2:** Official documentation, engineering blogs from primary sources (e.g., Anthropic, OpenAI, Google engineering blogs with named authors), government/institutional reports.

**Tier 3:** Reputable journalism and secondary analyses (cite with date; flag as secondary source).

**Tier 4 (flag for manual review):** Undated web pages, anonymous sources, LLM-generated summaries without cited originals, OpenReview submissions without final acceptance status.

**Implementation notes from DeepTRACE findings:**
- Statement-level citation checking (not just document-level) is required; 40–80% citation accuracy is the baseline even in production deep research systems
- Decompose answers into atomic claims and verify each against cited source
- Flag confidence level explicitly; deep research reduces overconfidence but high one-sidedness persists
- Up to 57% of citations may be post-rationalized (faithfulness issue), so citation presence alone is insufficient — the claim must actually be derivable from the cited source

---

## Summary of Verdicts and Key Findings

### Task 1 verdicts (short form)
- **MECE 23-31% recall claim:** FABRICATED. Zero matching papers in arXiv, ACL Anthology, IEEE Xplore, or JAIR. All three attributed citations (Chen 2024 ACL, Kumar & Patel 2025 TKDE, Li 2023 JAIR) are non-existent. Remove from all FathomX documentation immediately.
- **APOLLO ICLR 2026:** Paper exists at OpenReview but was DESK REJECTED. Not citable as ICLR 2026.
- **DeepTRACE ICLR 2026:** REAL. arXiv:2509.04499, ICLR 2026 Poster (accepted), Microsoft Research.
- **ResearchRubrics ICLR 2026:** REAL. arXiv:2511.07685, ICLR 2026 Poster (accepted), Scale AI.
- **DeepResearch Bench ICLR 2026:** REAL. arXiv:2506.11763, ICLR 2026 Poster (accepted).

### Task 2 best budget heuristics
1. Anthropic blog (2025-06-13): 3–5 subagents for standard research; 10+ for complex; token cost is 4× (single agent) to 15× (multi-agent) vs. chat; token usage explains 80% of variance.
2. DAAO (arXiv:2509.11079, WWW 2026): Difficulty-based dynamic routing — predict complexity before allocating agent count.
3. ParallelResearch (arXiv:2510.05145, ICLR 2026 Workshop): Tree traversal with information-gain gating; expand only when gain justifies cost; prune low-value branches in real time.
4. ZEBRA (arXiv:2605.20485): Water-filling budget allocation across pipeline phases based on estimated per-phase utility curves.
5. Plan-and-Budget (arXiv:2505.16122): Sub-question-level token budget allocation; 70% accuracy gain + 39% token reduction vs. fixed budgets.

### Task 3 best credibility practices
1. FActScore atomic-claim decomposition (EMNLP 2023, arXiv:2305.14251) — industry-standard factuality verification.
2. DeepTRACE 8-dimension audit framework (ICLR 2026, arXiv:2509.04499) — most comprehensive published framework for auditing deep research systems.
3. CiteEval faithfulness check (ACL 2025) — citation faithfulness (not just correctness) must be verified; 57% post-rationalization rate.
4. SIFT lateral reading + CRAAP tiering — map source credibility before ingesting evidence.
