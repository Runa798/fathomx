# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-05-20

### Added
- Multi-model orchestrator (Python): delegate extraction to FAST tier (DeepSeek), analysis to SMART tier (GPT), search to SEARCH tier (Gemini)
- Product research methodology: MECE 6-dimension scope expansion, 3 research personas (Market Analyst, CI Analyst, Product Strategist), gap-driven iteration
- TUI onboarding: interactive Textual-based setup for model tiers, search providers, and feature toggles
- Workspace file protocol: structured I/O between Claude and orchestrator via workspace/ directory
- Orchestrator tasks: search_extract, analyze, compress, gemini_search
- Gemini 3.1 Pro Search grounding as supplementary search source
- Config system: `~/.fathomx/config.json` with Pydantic v2 validation
- Deep report template: 6-dimension structure with SWOT, ERRC, JTBD frameworks
- CI: Python lint (ruff) + type check (mypy) + test (pytest) job
- Input size limits for analyze/compress tasks (400K char cap)
- base_url validation in config schema
- API key sanitization in validation error messages

### Changed
- **Renamed project to FathomX** — npm package, Python package, config directory, skill name all unified
- SKILL.md rewritten for multi-model workflow with graceful degradation
- strategy.md restructured into 4-phase orchestrator-integrated flow
- install.sh/install.js updated for orchestrator installation and config migration
- Package name: `claude-deep-research` → `fathomx` (npm), `deep_research` → `fathomx` (Python)
- Config directory: `~/.deep-research/` → `~/.fathomx/`

## [1.1.0] - 2026-05-20

### Added
- Source credibility scoring system (A–E ratings) in report templates
- Disk checkpointing for deep research sessions (resumable research)
- `npx claude-deep-research` one-command installer
- Multi-IDE support: OpenCode and Codex alongside Claude Code
- Semantic Scholar integration for academic research
- CHANGELOG.md, CONTRIBUTING.md, GitHub issue templates, CI workflow

### Changed
- Updated report-format.md with source-level credibility assessment
- Enhanced strategy.md with disk persistence and academic search phases
- Expanded install.sh with platform detection for OpenCode/Codex

## [1.0.0] - 2026-05-18

### Added
- Three-layer search architecture (API → Browser → Manual)
- GrokSearch MCP integration (AI search + Tavily extraction)
- Exa MCP integration (semantic search + entity discovery)
- Browser automation layer (agent-browser + browser-use)
- Intelligent complexity routing (Quick / Standard / Deep)
- Formatted report templates with source attribution and confidence indicators
- One-command installation via `install.sh`
- Bilingual documentation (Chinese + English)

[1.2.0]: https://github.com/Runa798/fathomx/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Runa798/fathomx/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Runa798/fathomx/releases/tag/v1.0.0
