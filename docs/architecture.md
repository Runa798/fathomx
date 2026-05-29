# PM DeepResearch — 产品与技术架构文档

> 版本: v1.2.0 (当前) → v1.3.0 (规划中)
> 日期: 2026-05-21
> 维护者: Runa798

---

## 1. 产品定位

PM DeepResearch 是一个 Claude Code Skill，面向**专业产品经理和运营专家**，将多模型编排与产品研究方法论融合为一套完整的深度调研系统。

### 1.1 核心价值主张

| 维度 | 竞品（ChatGPT Deep Research / Perplexity） | PM DeepResearch |
| ---- | ---- | ---- |
| 研究方法论 | 无结构化方法论 | MECE 6维 + 3研究人格 + Gap迭代 |
| 工具精准度 | 单一搜索引擎 | Grok + Exa + Gemini + Browser 四层 |
| 成本控制 | 全部用大模型 | 分层模型，FAST层成本降低37x |
| 输出质量 | 信息罗列 | 可行动决策建议 + 多框架分析 |
| 集成方式 | 独立产品 | Claude Code Skill，嵌入开发者工作流 |

### 1.2 目标用户

```
PM / 运营专家
    │
    ├── 日常使用 Claude Code 做开发+调研
    ├── 需要产业级深度分析（竞品/市场/用户）
    ├── 关注研究质量而非速度
    └── 愿意配置工具以获得更好结果
```

### 1.3 三大核心问题

| # | 问题 | 根因 | 解决方案 |
| - | ---- | ---- | -------- |
| 1 | MCP工具调用不精准 | Skill prompt缺工具路由指令 | PM Persona Pack + 工具分配矩阵 |
| 2 | Token浪费 | 主模型做低价值抓取 | 分层模型 + CLI/Subagent委托 |
| 3 | 开放性问题缺深度 | 缺研究方法论 | MECE范围扩展 + Gap驱动迭代 |

---

## 2. 系统架构

### 2.1 整体架构图

```mermaid
graph TB
    subgraph User["用户层"]
        U[用户提问]
        TUI[TUI 配置向导]
    end

    subgraph Claude["Claude Code 主进程 (STRATEGIC)"]
        SKILL[PM DeepResearch Skill]
        ROUTER[复杂度路由器]
        SCOPE[范围扩展引擎]
        GAP[Gap 检测器]
        SYNTH[综合报告生成器]
    end

    subgraph MCP["MCP 工具层"]
        GROK[Grok MCP]
        EXA[Exa MCP]
        TAVILY[Tavily API<br/>内嵌于 Grok]
    end

    subgraph Delegate["委托执行层"]
        SUB[CC Subagent<br/>haiku/sonnet]
        CODEX[Codex CLI<br/>gpt-5.5]
        PYORCH[Python Orchestrator<br/>降级路径]
    end

    subgraph Search["搜索能力"]
        GROK_S[Grok AI Search]
        TAVILY_S[Tavily Search + Extract]
        EXA_S[Exa Semantic Search]
        GEMINI_S[Gemini Search Grounding]
        BROWSER[Browser Layer 2]
    end

    subgraph Config["配置层"]
        CFG[~/.pm-deep-research/config.json]
        ENV[环境变量 / CLI 检测]
    end

    U --> SKILL
    TUI --> CFG
    SKILL --> ROUTER
    ROUTER -->|Quick| GROK
    ROUTER -->|Standard| SCOPE
    ROUTER -->|Deep| SCOPE
    SCOPE --> SUB
    SCOPE --> CODEX
    SCOPE --> GROK
    SCOPE --> EXA
    SUB -->|共享 MCP| GROK
    SUB -->|共享 MCP| EXA
    GROK --> GROK_S
    GROK --> TAVILY_S
    EXA --> EXA_S
    CODEX -->|自带工具| CODEX
    PYORCH --> GEMINI_S
    GAP --> SCOPE
    SYNTH --> U

    CFG --> SKILL
    ENV --> SKILL

    style Claude fill:#e8f4fd,stroke:#2196F3
    style MCP fill:#fff3e0,stroke:#FF9800
    style Delegate fill:#f3e5f5,stroke:#9C27B0
    style Search fill:#e8f5e9,stroke:#4CAF50
```

### 2.2 模型分层架构

```mermaid
graph LR
    subgraph STRATEGIC["STRATEGIC 层 — Claude Opus"]
        S1[意图理解]
        S2[范围扩展]
        S3[Gap检测]
        S4[综合报告]
    end

    subgraph SEARCH_LAYER["搜索层 — MCP + Subagent"]
        M1[Grok MCP<br/>AI搜索+Tavily抓取]
        M2[Exa MCP<br/>语义搜索+实体发现]
        M3[Gemini Search<br/>Google grounding]
        M4[Browser Layer 2<br/>JS渲染/登录态]
    end

    subgraph FAST["FAST 层 — 数据处理"]
        F1[数据提取<br/>Codex CLI / Subagent]
        F2[信息压缩<br/>Codex CLI / Subagent]
    end

    subgraph SMART["SMART 层 — 深度分析"]
        A1[Market Analyst<br/>Codex CLI]
        A2[CI Analyst<br/>Codex CLI]
        A3[Product Strategist<br/>Codex CLI]
    end

    S2 --> SEARCH_LAYER
    SEARCH_LAYER --> F1
    F1 --> SMART
    SMART --> F2
    F2 --> S4

    style STRATEGIC fill:#ffebee,stroke:#f44336
    style SEARCH_LAYER fill:#fff3e0,stroke:#FF9800
    style FAST fill:#e8f5e9,stroke:#4CAF50
    style SMART fill:#e3f2fd,stroke:#2196F3
```

### 2.3 模型调用三级优先级

```mermaid
flowchart TD
    START[需要调用外部模型] --> CHECK_CLI{CLI 可用?<br/>codex / gemini}
    CHECK_CLI -->|是| CLI[优先级1: exec CLI<br/>零自建, auth/retry 自带]
    CHECK_CLI -->|否| CHECK_MCP{MCP Server 可用?<br/>DeepSeek / Kimi MCP}
    CHECK_MCP -->|是| MCP_CALL[优先级2: MCP 调用<br/>融入CC工具生态]
    CHECK_MCP -->|否| CHECK_KEY{有外部 API key?}
    CHECK_KEY -->|是| PYORCH[降级: Python httpx<br/>v1.2.0 路径]
    CHECK_KEY -->|否| SUBAGENT[优先级3: CC Subagent<br/>haiku/sonnet, 零配置]

    CLI --> RESULT[返回结果]
    MCP_CALL --> RESULT
    PYORCH --> RESULT
    SUBAGENT --> RESULT

    style CLI fill:#c8e6c9,stroke:#388E3C
    style MCP_CALL fill:#fff9c4,stroke:#F9A825
    style SUBAGENT fill:#e1bee7,stroke:#7B1FA2
    style PYORCH fill:#ffccbc,stroke:#E64A19
```

---

## 3. 数据流与泳道图

### 3.1 Deep 级调研完整泳道图 (v1.3.0 目标架构)

```mermaid
sequenceDiagram
    actor User as 用户
    participant Claude as Claude<br/>(STRATEGIC)
    participant Sub as CC Subagent<br/>(haiku)
    participant Codex as Codex CLI<br/>(gpt-5.5)
    participant Grok as Grok MCP
    participant Exa as Exa MCP
    participant WS as Workspace<br/>文件系统

    User->>Claude: 调研请求
    Note over Claude: 复杂度评估 → Deep

    rect rgb(255, 243, 224)
        Note over Claude: Phase 1: 范围扩展
        Claude->>Claude: MECE 6维分解
        Claude->>Claude: 3研究人格视角
        Claude->>WS: 写入 plan.md
    end

    rect rgb(232, 245, 233)
        Note over Claude,Exa: Phase 2: 多维搜索 (并行)
        par 维度1: 市场环境
            Claude->>Sub: Agent(model:haiku)<br/>"搜索市场数据"
            Sub->>Grok: web_search(extra_sources=10)
            Sub->>Exa: web_search_exa()
            Sub->>WS: 写入 search/raw-market.md
        and 维度2: 竞品格局
            Claude->>Sub: Agent(model:haiku)<br/>"搜索竞品信息"
            Sub->>Exa: company_research_exa()
            Sub->>Grok: web_search()
            Sub->>WS: 写入 search/raw-competitive.md
        and 维度3-6: 其他维度
            Claude->>Sub: Agent(model:haiku)<br/>"搜索其他维度"
            Sub->>Grok: web_search()
            Sub->>WS: 写入 search/raw-*.md
        end
    end

    rect rgb(227, 242, 253)
        Note over Claude,Codex: Phase 3: 数据提取 + 分析
        par 提取 (FAST)
            Claude->>Codex: codex exec "提取结构化数据"<br/>stdin: raw-market.md
            Codex->>WS: 写入 search/market.md
        and 分析 (SMART)
            Claude->>Codex: codex exec "CI分析"<br/>stdin: 所有search/*.md
            Codex->>WS: 写入 analysis/ci-analyst.md
        end
    end

    rect rgb(252, 228, 236)
        Note over Claude: Phase 4: Gap检测
        Claude->>WS: 读取所有文件
        Claude->>Claude: 检查6维覆盖度
        alt 存在Gap
            Claude->>Sub: 补充搜索
            Sub->>Grok: 定向搜索
            Sub->>WS: 写入 search/gap-*.md
        end
    end

    rect rgb(255, 235, 238)
        Note over Claude: Phase 5: 综合报告
        Claude->>Codex: codex exec "压缩"<br/>stdin: 所有文件
        Codex->>WS: 写入 compressed/summary.md
        Claude->>WS: 读取 summary + analysis
        Claude->>Claude: SWOT / ERRC / JTBD / Porter
        Claude->>WS: 写入 report.md
        Claude->>User: 输出报告
    end
```

### 3.2 搜索层内部流程

```mermaid
flowchart LR
    subgraph GrokMCP["Grok MCP Server"]
        WS[web_search] --> |并行| GROK_AI[Grok AI API<br/>streaming]
        WS --> |extra_sources>0| TAV_S[Tavily /search<br/>advanced mode]
        WS --> |有key时| FC_S[Firecrawl /search]
        GROK_AI --> MERGE[merge_sources<br/>URL去重]
        TAV_S --> MERGE
        FC_S --> MERGE
        MERGE --> CACHE[LRU Cache<br/>session_id → sources]

        WF[web_fetch] --> TAV_E[Tavily /extract<br/>返回Markdown]
        TAV_E -->|失败| FC_E[Firecrawl /scrape<br/>降级]

        WM[web_map] --> FC_M[Firecrawl /map<br/>站点结构]
    end

    subgraph ExaMCP["Exa MCP Server"]
        ES[web_search_exa] --> EXA_API[Exa API<br/>语义搜索]
        CR[company_research_exa] --> EXA_API
        CW[crawling_exa] --> EXA_API
    end

    style GrokMCP fill:#fff3e0,stroke:#FF9800
    style ExaMCP fill:#e8f5e9,stroke:#4CAF50
```

### 3.3 v1.2.0 vs v1.3.0 执行模型对比

```mermaid
graph TB
    subgraph V12["v1.2.0 当前架构"]
        C1[Claude 主模型] -->|串行MCP调用| G1[Grok]
        C1 -->|串行MCP调用| E1[Exa]
        C1 -->|Bash exec| P1[Python httpx<br/>调DeepSeek/GPT API]
        P1 -->|文件| C1
    end

    subgraph V13["v1.3.0 目标架构"]
        C2[Claude 主模型] -->|并行派发| S1[Subagent 1<br/>haiku 搜索]
        C2 -->|并行派发| S2[Subagent 2<br/>haiku 搜索]
        C2 -->|并行派发| S3[Subagent 3<br/>haiku 搜索]
        S1 -->|共享MCP| G2[Grok]
        S1 -->|共享MCP| E2[Exa]
        S2 -->|共享MCP| G2
        S3 -->|共享MCP| E2
        C2 -->|并行exec| CX1[Codex CLI<br/>提取]
        C2 -->|并行exec| CX2[Codex CLI<br/>分析]
    end

    style V12 fill:#ffebee,stroke:#f44336
    style V13 fill:#e8f5e9,stroke:#4CAF50
```

---

## 4. 任务类型 × 执行方案矩阵

### 4.1 按任务类型选择执行方式

| 任务类型 | 需要MCP? | 最优方案 | 降级方案 | 原因 |
| -------- | -------- | -------- | -------- | ---- |
| 搜索抓取 | ✅ 必须 | CC Subagent (haiku) | Claude 主模型直调 | 共享 Grok/Exa MCP |
| 数据提取 | ❌ | Codex CLI (gpt-5.5) | Python httpx → DeepSeek | 纯文本处理，无需MCP |
| 人格分析 | ❌ | Codex CLI (gpt-5.5) | Python httpx → GPT | 需要推理能力，不需要MCP |
| 信息压缩 | ❌ | Codex CLI 或 Subagent (haiku) | Python httpx → DeepSeek | 结构化转换 |
| 补充搜索 | ✅ | CC Subagent (haiku) | Gemini Search API | 需要 MCP 或独立搜索能力 |
| 最终综合 | ❌ | Claude 主模型 (Opus) | 不可降级 | 最高质量要求 |

### 4.2 硬约束

```
┌─────────────────────────────────────────────────────┐
│  搜索/抓取类 agent 必须具备网页抓取能力              │
│                                                     │
│  ✅ CC Subagent → 共享会话 MCP (Grok/Exa)           │
│  ✅ Codex CLI   → 自带 web 工具                     │
│  ✅ MCP Server  → 取决于具体 MCP 设计               │
│  ❌ 纯对话模型  → 不满足要求                        │
└─────────────────────────────────────────────────────┘
```

---

## 5. 配置与 TUI 架构

### 5.1 配置层级

```mermaid
graph TD
    subgraph Detection["能力检测 (自动)"]
        D1[检测 codex CLI] --> |which codex| R1{存在?}
        D2[检测 gemini CLI] --> |which gemini| R2{存在?}
        D3[检测 MCP servers] --> |claude mcp list| R3{已注册?}
        D4[检测环境变量] --> |DEEPSEEK_API_KEY etc| R4{有key?}
    end

    subgraph Config["配置生成"]
        R1 -->|是| C1[Codex 可用于分析/提取]
        R2 -->|是| C2[Gemini 可用于搜索]
        R3 -->|是| C3[Grok/Exa 搜索可用]
        R4 -->|是| C4[Python httpx 降级可用]
        R1 -->|否| C5[用 Subagent 替代]
        C1 --> CFG[~/.pm-deep-research/config.json]
        C5 --> CFG
    end

    subgraph TUI["TUI 向导流程"]
        T1[Welcome] --> T2[能力检测结果展示]
        T2 --> T3[模型角色分配<br/>搜索/提取/分析]
        T3 --> T4[API Key 填入<br/>按需]
        T4 --> T5[验证连通性]
        T5 --> T6[保存配置]
    end

    CFG --> TUI

    style Detection fill:#e3f2fd,stroke:#1976D2
    style Config fill:#fff9c4,stroke:#FBC02D
    style TUI fill:#f3e5f5,stroke:#7B1FA2
```

### 5.2 config.json 结构 (v1.3.0)

```json
{
  "version": "1.3.0",
  "execution": {
    "search": {
      "method": "subagent",
      "model": "haiku",
      "fallback": "claude-direct"
    },
    "extract": {
      "method": "codex-cli",
      "model": "gpt-5.5",
      "fallback": "subagent-haiku"
    },
    "analyze": {
      "method": "codex-cli",
      "model": "gpt-5.5",
      "fallback": "subagent-sonnet"
    },
    "compress": {
      "method": "codex-cli",
      "model": "gpt-5.5",
      "fallback": "subagent-haiku"
    }
  },
  "mcp": {
    "grok": { "registered": true },
    "exa": { "registered": true }
  },
  "cli": {
    "codex": { "available": true, "path": "/home/user/.npm-global/bin/codex" },
    "gemini": { "available": false }
  },
  "api_keys": {
    "deepseek": { "configured": true },
    "openai": { "configured": true }
  },
  "features": {
    "scope_expansion": true,
    "gap_iteration": true,
    "gemini_search": false
  }
}
```

---

## 6. Workspace 文件协议

```
workspace/research-{YYYY-MM-DD}-{slug}/
│
├── plan.md                    # Claude 写: 研究计划 + MECE 6维分解
├── state.json                 # 系统更新: 阶段跟踪
│
├── search/                    # 搜索结果
│   ├── raw-{dimension}.md     # Subagent 写: 原始 MCP 搜索结果
│   ├── {dimension}.md         # Codex CLI 写: 结构化提取数据
│   ├── gemini-{topic}.md      # Gemini 写: grounding 搜索结果
│   └── gap-{dimension}.md     # Subagent 写: 补充搜索结果
│
├── analysis/                  # 分析结果
│   ├── market-analyst.md      # Codex CLI 写: 市场分析
│   ├── ci-analyst.md          # Codex CLI 写: 竞争情报分析
│   └── product-strategist.md  # Codex CLI 写: 产品策略分析
│
├── compressed/
│   └── findings-summary.md    # Codex CLI 写: 压缩后的综合摘要
│
├── errors.log                 # 系统追加: 错误记录
└── report.md                  # Claude 写: 最终研究报告
```

---

## 7. 研究方法论

### 7.1 MECE 6 维度范围扩展

```mermaid
mindmap
  root((用户问题))
    市场环境
      TAM/SAM/SOM
      增长驱动力
      监管环境
    竞争格局
      直接竞品
      间接竞品
      替代品
      潜在进入者
    用户需求
      JTBD 分析
      痛点映射
      转换触发器
    产品能力
      功能对比矩阵
      定价架构
      技术栈
    战略定位
      护城河分析
      SWOT
      ERRC 网格
    未来趋势
      技术颠覆
      市场预测
      非客户群体
```

### 7.2 三研究人格

| 人格 | 聚焦 | 分析框架 | 对应维度 |
| ---- | ---- | -------- | -------- |
| Market Analyst | 市场规模/趋势/风险 | TAM/SAM/SOM, 增长驱动力 | 1.市场 + 6.趋势 |
| CI Analyst | 竞品/定位/护城河 | Porter五力, 特征矩阵, 护城河分析 | 2.竞品 + 4.产品 |
| Product Strategist | 用户需求/机会/建议 | JTBD, Blue Ocean ERRC, OST | 3.用户 + 5.战略 |

### 7.3 Gap 驱动迭代

```mermaid
flowchart TD
    SEARCH[搜索完成] --> CHECK{Gap 检测}
    CHECK --> |每维度≥3来源?| S1[✅ 通过]
    CHECK --> |来源多样性?| S2[✅ 通过]
    CHECK --> |矛盾已标注?| S3[✅ 通过]
    CHECK --> |有数值证据?| S4[✅ 通过]
    CHECK --> |数据≤12月?| S5[✅ 通过]

    S1 --> |否| FIX[定向补充搜索]
    S2 --> |否| FIX
    S3 --> |否| FIX
    S4 --> |否| FIX
    S5 --> |否| FIX

    FIX --> |max 2轮| CHECK
    S1 & S2 & S3 & S4 & S5 --> |全通过| SYNTH[进入综合阶段]
```

---

## 8. 优雅降级矩阵

```mermaid
flowchart TD
    FULL[完整配置<br/>Codex + MCP + Keys] --> |最优| BEST[全功能:<br/>Subagent搜索 + Codex分析<br/>真并行, 多模型]

    PARTIAL1[仅有 Codex CLI] --> |中等| MED1[Codex做分析<br/>Claude直接搜索<br/>串行MCP]

    PARTIAL2[仅有 API Keys] --> |中等| MED2[Python httpx<br/>v1.2.0 模式]

    NONE[无外部配置] --> |基础| BASE[Claude-only:<br/>直接MCP搜索<br/>+ 方法论增强<br/>仍优于v1.1.0]

    style BEST fill:#c8e6c9,stroke:#388E3C
    style MED1 fill:#fff9c4,stroke:#F9A825
    style MED2 fill:#fff9c4,stroke:#F9A825
    style BASE fill:#ffccbc,stroke:#E64A19
```

| 条件 | 行为 |
| ---- | ---- |
| 无 config.json | Claude-only + MECE方法论增强 |
| 仅 Codex CLI | 分析/提取委托Codex，搜索Claude直做 |
| 仅 API keys | v1.2.0 Python httpx 模式 |
| Codex + MCP | Subagent搜索 + Codex分析 (最优) |
| 外部API超时 | 记录error.log，Claude自行完成该步骤 |
| MCP不可用 | Subagent用CC内置WebSearch降级 |

---

## 9. 版本路线图

```mermaid
gantt
    title PM DeepResearch 版本路线图
    dateFormat YYYY-MM-DD
    axisFormat %m/%d

    section v1.0.0 ✅
    三层搜索 + Skill           :done, v10, 2026-05-18, 2d

    section v1.1.0 ✅
    落盘 + 评分 + npx + 多IDE  :done, v11, 2026-05-20, 1d

    section v1.2.0 ✅
    多模型编排 + 方法论 + TUI  :done, v12, 2026-05-20, 1d

    section v1.3.0
    Subagent + Codex CLI + TUI重构 :active, v13, 2026-05-21, 14d

    section v1.4.0
    MCP集成 + Gemini CLI       :v14, after v13, 14d
```

### v1.3.0 范围

| 模块 | 内容 | 优先级 |
| ---- | ---- | ------ |
| CC Subagent 搜索 | 用 haiku/sonnet subagent 并行搜索，共享 MCP | P0 |
| Codex CLI 分析 | 用 codex exec 做提取/分析/压缩 | P0 |
| TUI 重构 | 能力发现向导，检测 CLI/MCP/Key | P0 |
| Skill 层重写 | 从 python orchestrator 调用改为 CLI/subagent 编排 | P0 |
| Python 包精简 | 退化为 TUI + config + 能力检测 | P1 |

### v1.4.0 范围 (待定)

| 模块 | 内容 | 依赖 |
| ---- | ---- | ---- |
| DeepSeek MCP | 通过 MCP 调用 DeepSeek | Heye 的 MCP 研究 |
| Gemini CLI grounding | 验证 gemini CLI 是否支持 search grounding | CLI 功能验证 |
| Quality Gates | Hook 机制，研究各阶段自动检测质量 | v1.3.0 稳定 |
| 中文生态 | Bocha 搜索 + 微信公众号 MCP | 独立集成 |

---

## 10. 关键技术决策记录

| # | 决策 | 选择 | 理由 |
| - | ---- | ---- | ---- |
| 1 | 主模型调用方式 | Claude 就是主模型，不通过 API 调 | Claude Code CLI 本身就运行在 Claude 上 |
| 2 | 外部模型调用 | CLI > MCP > Subagent > httpx | 利用生态工具，减少自建代码 |
| 3 | 搜索 agent 实现 | CC Subagent (haiku) | 共享 MCP 工具，零额外配置 |
| 4 | 分析任务实现 | Codex CLI (gpt-5.5) | 不需要 MCP，纯文本处理，可真并行 |
| 5 | IPC 方式 | Workspace 文件系统 | 可靠、可恢复、可追溯 |
| 6 | 配置存储 | ~/.pm-deep-research/config.json | 全局用户级，权限 0600 |
| 7 | 框架 | 无 (不用 LangChain/CrewAI) | 是 CC Skill 不是独立 agent |
| 8 | Context 压缩 | 55% 保留率，35% 硬底线 | Chen et al. 2025 研究 |
