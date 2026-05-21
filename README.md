<div align="center">

# 🔍 FathomX

**多模型深度调研工具** — MECE 范围扩展 + 研究人格 + 多模型编排 + 格式化报告

[![Version](https://img.shields.io/github/v/release/Runa798/fathomx?label=version)](https://github.com/Runa798/fathomx/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/Runa798/fathomx)](https://github.com/Runa798/fathomx/graphs/contributors)

[English](README_EN.md) | 简体中文

</div>

---

## 这是什么

FathomX 是一个 Claude Code Skill，将多模型编排与产品研究方法论融合为一套完整的调研系统：

- **多模型编排**: FAST 层 (DeepSeek) 做数据提取, SMART 层 (GPT) 做分析, SEARCH 层 (Gemini) 做补充搜索, Claude 做战略综合
- **产品研究方法论**: MECE 6 维度范围扩展 + 3 个研究人格 + 间隙驱动迭代
- **三层搜索架构**: Grok MCP + Exa MCP + Gemini Search + 浏览器降级
- **格式化报告**: 按研究维度组织，来源标注 + 可信度评级 + 置信度标记

### 架构

```
用户提问
    │
    ▼
Claude (STRATEGIC 层)
    │
    ├── 1. 范围扩展 (MECE 6 维度)
    │       市场 / 竞品 / 用户 / 产品 / 战略 / 趋势
    │
    ├── 2. 多维搜索 (MCP 工具)
    │       Grok web_search ──┐
    │       Exa semantic  ────┤ 并行
    │       Gemini grounding ─┘
    │
    ├── 3. 外部模型编排 (Python orchestrator)
    │       ┌─────────────────────────────┐
    │       │ FAST (DeepSeek)  → 数据提取  │
    │       │ SMART (GPT)      → 人格分析  │
    │       │ FAST (DeepSeek)  → 信息压缩  │
    │       └─────────────────────────────┘
    │
    ├── 4. 间隙检测 + 补充搜索 (最多 2 轮)
    │
    └── 5. 综合报告 (SWOT / ERRC / JTBD / Porter)
```

**优雅降级**: 没有外部模型 key → 退化为 Claude-only 模式 + 方法论增强。部分配置有效。

---

## 前置条件

- **Claude Code** — CLI (`claude`) 或 Claude Desktop
- **Python 3.10+** 及 `uv`
- **Node.js 18+** 及 `npm`
- **(可选)** System Chrome + CDP 端口 9222（Layer 2 浏览器抓取）

```bash
python3 --version   # >= 3.10
uv --version        # >= 0.4
node --version      # >= 18
```

---

## 安装

### 通过 npx 安装（推荐）

```bash
npx fathomx
```

### 克隆安装

```bash
git clone https://github.com/Runa798/fathomx.git
cd claude-deep-research
./install.sh
```

> **支持的平台**: Claude Code (全自动) | OpenCode (Skill 自动 + MCP 手动) | Codex (Skill 自动 + MCP 手动)

### 配置多模型编排（可选）

安装后运行 TUI 配置向导：

```bash
npx fathomx --setup
# 或
python3 -m fathomx setup
```

TUI 会引导你配置：
- **FAST 层** — DeepSeek / 其他 OpenAI 兼容模型（数据提取）
- **SMART 层** — GPT / 其他 OpenAI 兼容模型（分析）
- **SEARCH 层** — Gemini 3.1 Pro（搜索补充）
- **搜索服务** — Grok / Exa 的 API Key（从 .env 自动迁移）

配置保存在 `~/.fathomx/config.json`（权限 0600）。

### API Keys 配置

| 变量 | 必填 | 说明 |
|------|------|------|
| `GROK_API_URL` | ✅ | Grok API 地址（OpenAI 兼容接口） |
| `GROK_API_KEY` | ✅ | Grok API Key |
| `TAVILY_API_KEY` | ❌ | Tavily API Key（网页内容抓取） |
| `EXA_API_KEY` | ❌ | Exa API Key（语义搜索，强烈推荐） |

---

## 使用方法

### 触发关键词

在 Claude Code 对话中，出现以下关键词时 Skill 自动触发：

```
调研 / research / 深度搜索 / 对比分析 / 产业分析 / 竞品分析 / 技术选型
```

也可以显式调用：

```
/fathomx 你的调研问题
```

### 三级调研

| 级别 | 触发 | 方法论 | 时间 |
|------|------|--------|------|
| **Quick** | 单一事实查询 | 直接搜索 | ~10 秒 |
| **Standard** | 对比/选型/评估 | MECE 4 维度 + 人格分析 | 2-5 分钟 |
| **Deep** | 产业分析/竞品图谱 | MECE 6 维度 + 多模型编排 + 间隙迭代 | 5-15 分钟 |

### 示例

**快速查询**

```
帮我调研一下 FastAPI 0.115 版本的主要变化
```

**标准调研**

```
对比 Next.js 和 Nuxt.js 的优劣势，从 SSR 性能、生态和 DX 角度分析
```

**深度调研**

```
调研中国智能健身镜市场的竞品格局，包括主要玩家、定价策略、技术差异和市场趋势
```

### 报告结构 (Deep 级)

```markdown
## 调研报告：{主题}

**决策意图**: {推断的用户决策目标}
**调研维度**: 6 个 MECE 维度

### 1. 市场环境 (Market Context)
### 2. 竞争格局 (Competitive Landscape)
### 3. 用户需求 (User Jobs & Needs)
### 4. 产品能力 (Product Capabilities)
### 5. 战略定位 (Strategic Position)
### 6. 未来趋势 (Future Trajectory)

### 战略分析
- SWOT（含 "so what" 启示）
- ERRC 网格
- JTBD 机会评分

### 来源表
- [n] 来源标题 (URL) — 可信度 A-E
```

---

## 卸载

```bash
# 移除 MCP 注册
claude mcp remove grok-search
claude mcp remove exa

# 移除 Skill
rm -rf ~/.claude/skills/fathomx

# 可选：移除配置
rm -rf ~/.fathomx
```

---

## 致谢

本项目依赖多个优秀的开源项目和服务，详见 [ATTRIBUTION.md](ATTRIBUTION.md)。

---

## 贡献者

<a href="https://github.com/huangguaheye">
  <img src="https://github.com/huangguaheye.png" width="50" height="50" alt="huangguaheye" style="border-radius: 50%;" />
</a>

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
