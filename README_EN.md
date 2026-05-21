<div align="center">

# 🔍 FathomX

**Multi-Model Deep Research Tool** — MECE Scope Expansion + Research Personas + Multi-Model Orchestration + Formatted Reports

[![Version](https://img.shields.io/github/v/release/Runa798/fathomx?label=version)](https://github.com/Runa798/fathomx/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/Runa798/fathomx)](https://github.com/Runa798/fathomx/graphs/contributors)

[English](README_EN.md) | [简体中文](README.md)

</div>

---

## What is this?

FathomX is a Claude Code Skill that combines multi-model orchestration with product research methodology into a complete research system:

- **Multi-Model Orchestration**: FAST tier (DeepSeek) for data extraction, SMART tier (GPT) for analysis, SEARCH tier (Gemini) for supplementary search, Claude for strategic synthesis
- **Product Research Methodology**: MECE 6-dimension scope expansion + 3 research personas + gap-driven iteration
- **Three-Layer Search**: Grok MCP + Exa MCP + Gemini Search + browser fallback
- **Formatted Reports**: Organized by research dimension with source attribution + credibility ratings + confidence markers

### Architecture

```
User Query
    │
    ▼
Claude (STRATEGIC tier)
    │
    ├── 1. Scope Expansion (MECE 6 dimensions)
    │       Market / Competitive / User / Product / Strategic / Future
    │
    ├── 2. Multi-Dimensional Search (MCP tools)
    │       Grok web_search ──┐
    │       Exa semantic  ────┤ parallel
    │       Gemini grounding ─┘
    │
    ├── 3. External Model Orchestration (Python)
    │       ┌──────────────────────────────────┐
    │       │ FAST (DeepSeek)  → extraction     │
    │       │ SMART (GPT)      → persona analysis│
    │       │ FAST (DeepSeek)  → compression    │
    │       └──────────────────────────────────┘
    │
    ├── 4. Gap Detection + Supplementary Search (max 2 rounds)
    │
    └── 5. Synthesis Report (SWOT / ERRC / JTBD / Porter)
```

**Graceful Degradation**: No external model keys → falls back to Claude-only mode + methodology enhancements. Partial configuration works.

---

## Prerequisites

- **Claude Code** — CLI (`claude`) or Claude Desktop
- **Python 3.10+** and `uv`
- **Node.js 18+** and `npm`
- **(Optional)** System Chrome with CDP on port 9222 (for Layer 2 browser scraping)

```bash
python3 --version   # >= 3.10
uv --version        # >= 0.4
node --version      # >= 18
```

---

## Installation

### Install via npx (recommended)

```bash
npx fathomx
```

### Clone and Install

```bash
git clone https://github.com/Runa798/fathomx.git
cd claude-deep-research
./install.sh
```

> **Supported platforms**: Claude Code (fully automatic) | OpenCode (Skill auto + MCP manual) | Codex (Skill auto + MCP manual)

### Configure Multi-Model Orchestration (optional)

After installation, run the TUI setup wizard:

```bash
npx fathomx --setup
# or
python3 -m fathomx setup
```

The TUI guides you through configuring:
- **FAST tier** — DeepSeek / other OpenAI-compatible model (data extraction)
- **SMART tier** — GPT / other OpenAI-compatible model (analysis)
- **SEARCH tier** — Gemini 3.1 Pro (supplementary search)
- **Search providers** — Grok / Exa API keys (auto-migrates from .env)

Configuration is saved to `~/.fathomx/config.json` (permissions 0600).

### API Keys Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GROK_API_URL` | ✅ | Grok API endpoint (OpenAI-compatible) |
| `GROK_API_KEY` | ✅ | Grok API key |
| `TAVILY_API_KEY` | ❌ | Tavily API key (web content extraction) |
| `EXA_API_KEY` | ❌ | Exa API key (semantic search — strongly recommended) |

---

## Usage

### Trigger Keywords

The Skill is automatically routed when these keywords appear in a Claude Code conversation:

```
research / deep search / competitive analysis / industry analysis / tech evaluation
compare / investigate / market analysis / 调研 / 竞品分析
```

You can also invoke it explicitly:

```
/fathomx your research question here
```

### Three Research Tiers

| Tier | Trigger | Methodology | Time |
|------|---------|-------------|------|
| **Quick** | Single fact lookup | Direct search | ~10 sec |
| **Standard** | Comparison / evaluation | MECE 4-dimension + personas | 2-5 min |
| **Deep** | Industry analysis / competitive landscape | MECE 6-dimension + multi-model + gap iteration | 5-15 min |

### Examples

**Quick Query**

```
What are the main changes in FastAPI 0.115?
```

**Standard Research**

```
Compare Next.js vs Nuxt.js — SSR performance, ecosystem, and developer experience
```

**Deep Research**

```
Research the competitive landscape of the smart fitness mirror market in China — major players, pricing strategies, technical differentiation, and market trends
```

### Report Structure (Deep tier)

```markdown
## Research Report: {Topic}

**Decision Intent**: {inferred user decision goal}
**Dimensions**: 6 MECE dimensions

### 1. Market Context
### 2. Competitive Landscape
### 3. User Jobs & Needs
### 4. Product Capabilities
### 5. Strategic Position
### 6. Future Trajectory

### Strategic Analysis
- SWOT (with "so what" implications)
- ERRC Grid
- JTBD Opportunity Scores

### Source Table
- [n] Source Title (URL) — Credibility A-E
```

---

## Uninstall

```bash
# Remove MCP registrations
claude mcp remove grok-search
claude mcp remove exa

# Remove the Skill
rm -rf ~/.claude/skills/fathomx

# Optional: remove config
rm -rf ~/.fathomx
```

---

## Attribution

This project depends on several excellent open-source projects and services. See [ATTRIBUTION.md](ATTRIBUTION.md) for full details.

---

## Contributors

<a href="https://github.com/huangguaheye">
  <img src="https://github.com/huangguaheye.png" width="50" height="50" alt="huangguaheye" style="border-radius: 50%;" />
</a>

## License

MIT License — see [LICENSE](LICENSE)
