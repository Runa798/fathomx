# Attribution & Dependencies

This project builds upon and integrates the following open-source projects and services:

## Core Dependencies

### GrokSearch MCP

- **Repository**: [GuDaStudio/GrokSearch](https://github.com/GuDaStudio/GrokSearch)
- **License**: MIT
- **Role**: Primary search engine — Grok AI search + Tavily Extract/Map + Firecrawl fallback
- **Relationship**: Used as MCP dependency (installed via uvx)

### Exa MCP Server

- **Repository**: [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)
- **License**: Proprietary
- **Role**: Semantic web search, entity discovery, company research
- **Relationship**: Used as MCP dependency (installed via npx)

### grok2api

- **Repository**: [chenyme/grok2api](https://github.com/chenyme/grok2api)
- **License**: Check upstream
- **Role**: OpenAI-compatible API proxy for Grok (optional, for shared API access)
- **Relationship**: Self-hosted deployment, not bundled

## Browser Automation (Layer 2)

### agent-browser

- **Package**: [npm: agent-browser](https://www.npmjs.com/package/agent-browser)
- **Role**: Precise CLI-based browser automation via CDP

### browser-use

- **Package**: [pip: browser-use](https://pypi.org/project/browser-use/)
- **Role**: AI-driven autonomous browser navigation

## Infrastructure

### Tavily API

- **Website**: [tavily.com](https://tavily.com)
- **Role**: Web content extraction and site mapping (via pool or direct API)

### FastMCP

- **Repository**: [jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **License**: MIT
- **Role**: MCP server framework used by GrokSearch
