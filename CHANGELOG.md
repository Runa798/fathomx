# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.1.0]: https://github.com/Runa798/claude-deep-research/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Runa798/claude-deep-research/releases/tag/v1.0.0
