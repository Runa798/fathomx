<div align="center">

# 🔍 Claude Deep Research

**Deep Research Skill for Claude Code** — Three-Layer Search Architecture + Smart Orchestration + Formatted Reports

[![Version](https://img.shields.io/github/v/release/Runa798/claude-deep-research?label=version)](https://github.com/Runa798/claude-deep-research/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/Runa798/claude-deep-research)](https://github.com/Runa798/claude-deep-research/graphs/contributors)

[English](README_EN.md) | [简体中文](README.md)

</div>

---

## What is this?

Claude Deep Research is a Claude Code Skill that integrates multiple search MCP tools into a complete research workflow:

- **Layer 1 — API Search**: Grok Search MCP (AI search + Tavily extraction) + Exa MCP (semantic search)
- **Layer 2 — Browser Scraping**: agent-browser + browser-use (JS-rendered pages / authenticated content)
- **Smart Orchestration**: Automatically assesses research complexity and routes to the appropriate strategy
- **Formatted Reports**: Three-tier report templates with source attribution and confidence markers

### Architecture

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
     (single)  (parallel) (multi-round)
         │        │        │
         │    Grok +    Grok + Exa
       Grok    Exa in     multi-round
               parallel   discovery
                       + browser
                         fallback
         │        │        │
         └────────┴────────┘
                  │
                  ▼
       Formatted Research Report
      (summary + sources + confidence)
```

**Three-layer search strategy**:

| Layer | Tools | Use Cases |
|-------|-------|-----------|
| Layer 1 — API Search | Grok MCP + Exa MCP | Structured data, factual queries, semantic discovery |
| Layer 2 — Browser Scraping | agent-browser / browser-use | JS-rendered pages, authenticated content, anti-bot bypass |
| Layer 3 — Manual Intervention | noVNC + Chrome | CAPTCHAs, 2FA, human-confirmation scenarios |

---

## Prerequisites

- **Claude Code** — CLI (`claude`) or Claude Desktop
- **Python 3.10+** and `uv` (for GrokSearch MCP)
- **Node.js 18+** and `npm` (for Exa MCP)
- **(Optional)** System Chrome with CDP on port 9222 (for Layer 2 browser automation)

```bash
# Verify dependencies
python3 --version   # >= 3.10
uv --version        # >= 0.4
node --version      # >= 18
npm --version
```

---

## Installation

### One-Command Install

```bash
# Clone and run the install script
git clone https://github.com/Runa798/claude-deep-research.git
cd claude-deep-research
./install.sh
```

The install script handles everything: registering GrokSearch MCP, registering Exa MCP, installing the Skill to `~/.claude/skills/`, and generating a `.env` config file.

### Manual Installation

**1. Clone the repository**

```bash
git clone https://github.com/Runa798/claude-deep-research.git
cd claude-deep-research
```

**2. Register GrokSearch MCP**

```bash
claude mcp add grok-search \
  --transport stdio \
  uvx grok-search-mcp
```

**3. Register Exa MCP**

```bash
claude mcp add exa \
  --transport stdio \
  -- npx -y exa-mcp-server
```

**4. Install the Skill**

```bash
mkdir -p ~/.claude/skills
cp -r skill/ ~/.claude/skills/deep-research
```

**5. Configure API Keys**

```bash
cp .env.example .env
# Edit .env and fill in your API keys
$EDITOR .env
```

### API Keys Reference

Copy `.env.example` to `.env` and fill in the relevant values:

| Variable | Required | Description |
|----------|----------|-------------|
| `GROK_API_URL` | ✅ | Grok API endpoint (OpenAI-compatible) |
| `GROK_API_KEY` | ✅ | Grok API key |
| `TAVILY_API_URL` | ❌ | Tavily API endpoint (defaults to `api.tavily.com`) |
| `TAVILY_API_KEY` | ❌ | Tavily API key (Layer 1 web content extraction) |
| `EXA_API_KEY` | ❌ | Exa API key (semantic search — strongly recommended) |
| `FIRECRAWL_API_KEY` | ❌ | Firecrawl API key (GrokSearch fallback) |

> **How to get a Grok API key**:
> - Self-host [grok2api](https://github.com/chenyme/grok2api) as an OpenAI-compatible proxy
> - Use the [xAI API](https://console.x.ai/) directly (official, paid)
> - Use the GuDa all-in-one service

---

## Usage

### Trigger Keywords

The Skill is automatically routed when the following keywords appear in a Claude Code conversation:

```
research / deep search / competitive analysis / industry analysis / tech evaluation
compare / investigate / market analysis / look into / find information on
```

You can also invoke it explicitly at the start of a message:

```
/deep-research your research question here
```

### Three Research Tiers — Examples

**Quick Query** — Single fact or definition lookup (≈10 seconds)

```
What are the main changes in FastAPI 0.115?
```

**Standard Research** — Comparison, evaluation, tech selection (≈30–60 seconds)

```
Compare the pros and cons of Next.js vs Nuxt.js from the perspective of SSR performance, ecosystem, and DX
```

**Deep Research** — Industry analysis, competitive landscape, market trends (≈2–5 minutes)

```
Research the competitive landscape of the smart fitness mirror market in China — major players, pricing strategies, technical differentiation, and market trends
```

### Report Format

All research results are returned using a consistent template:

```markdown
## Research Report: {Topic}

**Research Depth**: Quick / Standard / Deep
**Sources**: N sources
**Confidence**: High / Medium / Low

### Key Findings

...

### Detailed Analysis

...

### Sources

- [Source Title](URL) — Summary description
```

### Relationship with Claude Code's Native Search

This Skill **disables** Claude Code's native WebSearch / WebFetch by default. All search traffic is routed through GrokSearch MCP + Exa MCP.

Native search is only enabled as a fallback in these cases:
- All MCP API keys are unavailable or requests time out
- The user explicitly requests native search (`/websearch`)
- Querying Anthropic / Claude's own documentation (context7 MCP takes priority)

---

## Uninstall

```bash
# Remove MCP registrations
claude mcp remove grok-search
claude mcp remove exa

# Remove the Skill
rm -rf ~/.claude/skills/deep-research

# Optional: remove config file
rm .env
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
