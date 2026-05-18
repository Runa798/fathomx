<div align="center">

# 🔍 Claude Deep Research

**Claude Code 深度调研工具** — 三层搜索架构 + 智能编排 + 格式化报告

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README_EN.md) | 简体中文

</div>

---

## 这是什么

Claude Deep Research 是一个 Claude Code Skill，将多个搜索 MCP 工具整合为一套完整的调研工作流：

- **Layer 1 — API 搜索**: Grok Search MCP (AI 搜索 + Tavily 抓取) + Exa MCP (语义搜索)
- **Layer 2 — 浏览器抓取**: agent-browser + browser-use (JS 渲染 / 登录态内容)
- **智能编排**: 自动判断调研复杂度，路由到对应策略
- **格式化报告**: 三级报告模板，来源标注，置信度标记

### 架构

```
Claude Code
    │
    └── deep-research skill
            │
            ▼
    ┌───────────────────┐
    │  Complexity Router │
    └───────────────────┘
         │        │        │
         ▼        ▼        ▼
      Quick    Standard   Deep
      (单次)   (并行)    (多轮)
         │        │        │
         │    Grok +    Grok + Exa
       Grok    Exa 并行   多轮发现
                       + browser
                         fallback
         │        │        │
         └────────┴────────┘
                  │
                  ▼
        格式化调研报告
     (摘要 + 来源 + 置信度)
```

**三层搜索策略**：

| 层级 | 工具 | 适用场景 |
|------|------|----------|
| Layer 1 — API 搜索 | Grok MCP + Exa MCP | 结构化信息、事实查询、语义发现 |
| Layer 2 — 浏览器抓取 | agent-browser / browser-use | JS 渲染页、登录态内容、反爬绕过 |
| Layer 3 — 人工介入 | noVNC + Chrome | 验证码、2FA、需要人工确认的场景 |

---

## 前置条件

- **Claude Code** — CLI (`claude`) 或 Claude Desktop
- **Python 3.10+** 及 `uv`（用于 GrokSearch MCP）
- **Node.js 18+** 及 `npm`（用于 Exa MCP）
- **(可选)** System Chrome + CDP 端口 9222（用于 Layer 2 浏览器抓取）

```bash
# 检查依赖
python3 --version   # >= 3.10
uv --version        # >= 0.4
node --version      # >= 18
npm --version
```

---

## 安装

### 一键安装

```bash
# 克隆并执行安装脚本
git clone https://github.com/Runa798/claude-deep-research.git
cd claude-deep-research
./install.sh
```

安装脚本会自动完成：注册 GrokSearch MCP、注册 Exa MCP、安装 Skill 到 `~/.claude/skills/`、创建 `.env` 配置文件。

### 手动安装

**1. 克隆仓库**

```bash
git clone https://github.com/Runa798/claude-deep-research.git
cd claude-deep-research
```

**2. 注册 GrokSearch MCP**

```bash
claude mcp add grok-search \
  --transport stdio \
  uvx grok-search-mcp
```

**3. 注册 Exa MCP**

```bash
claude mcp add exa \
  --transport stdio \
  -- npx -y exa-mcp-server
```

**4. 安装 Skill**

```bash
mkdir -p ~/.claude/skills
cp -r skill/ ~/.claude/skills/deep-research
```

**5. 配置 API Keys**

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Keys
$EDITOR .env
```

### API Keys 配置

复制 `.env.example` 为 `.env` 并填写对应的值：

| 变量 | 必填 | 说明 |
|------|------|------|
| `GROK_API_URL` | ✅ | Grok API 地址（OpenAI 兼容接口） |
| `GROK_API_KEY` | ✅ | Grok API Key |
| `TAVILY_API_URL` | ❌ | Tavily API 地址（默认使用官方 `api.tavily.com`） |
| `TAVILY_API_KEY` | ❌ | Tavily API Key（Layer 1 网页内容抓取） |
| `EXA_API_KEY` | ❌ | Exa API Key（语义搜索，强烈推荐配置） |
| `FIRECRAWL_API_KEY` | ❌ | Firecrawl API Key（GrokSearch 降级备用） |

> **Grok API 获取方式**：
> - 自建 [grok2api](https://github.com/chenyme/grok2api) 代理（共享访问）
> - 直接使用 [xAI API](https://console.x.ai/)（官方付费）
> - 使用 GuDa 一体化服务

---

## 使用方法

### 触发关键词

在 Claude Code 对话中，出现以下关键词时 Skill 会自动被路由：

```
调研 / research / 深度搜索 / 对比分析 / 产业分析 / 竞品分析 / 技术选型
帮我查一下 / 搜索 / 找资料 / 调查一下 / 市场分析
```

也可以在消息开头显式调用：

```
/deep-research 你的调研问题
```

### 三级调研示例

**快速查询** — 单一事实、定义查询（约 10 秒）

```
帮我调研一下 FastAPI 0.115 版本的主要变化
```

**标准调研** — 对比、选型、评估（约 30-60 秒）

```
对比 Next.js 和 Nuxt.js 的优劣势，从 SSR 性能、生态和 DX 角度分析
```

**深度调研** — 产业分析、竞品图谱、市场格局（约 2-5 分钟）

```
调研中国智能健身镜市场的竞品格局，包括主要玩家、定价策略、技术差异和市场趋势
```

### 报告格式

所有调研结果按统一模板输出：

```markdown
## 调研报告：{主题}

**调研深度**: 快速 / 标准 / 深度
**来源数量**: N 个
**置信度**: 高 / 中 / 低

### 核心发现

...

### 详细分析

...

### 来源

- [来源标题](URL) — 摘要描述
```

### 与 Claude Code 原生搜索的关系

本 Skill **默认禁用** Claude Code 原生 WebSearch / WebFetch，所有搜索流量通过 GrokSearch MCP + Exa MCP 路由。

仅在以下场景启用原生搜索作为降级：
- 所有 MCP API Key 不可用 / 响应超时
- 用户明确要求使用原生搜索（`/websearch`）
- 查询 Anthropic / Claude 自身文档（context7 MCP 优先）

---

## 卸载

```bash
# 移除 MCP 注册
claude mcp remove grok-search
claude mcp remove exa

# 移除 Skill
rm -rf ~/.claude/skills/deep-research

# 可选：移除配置文件
rm .env
```

---

## 致谢

本项目依赖多个优秀的开源项目和服务，详见 [ATTRIBUTION.md](ATTRIBUTION.md)。

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
