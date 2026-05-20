# Contributing to FathomX

Thanks for your interest in contributing! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/claude-deep-research.git`
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Make your changes
5. Test the installation: `./install.sh`
6. Commit with conventional commits: `git commit -m "feat: add new feature"`
7. Push and open a Pull Request

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code refactoring
- `chore:` — Maintenance tasks

## Project Structure

```
fathomx/
├── skill/              # Claude Code Skill (core)
│   ├── SKILL.md        # Skill manifest and workflow
│   ├── references/     # Strategy, methodology, and format guides
│   └── templates/      # Report templates
├── orchestrator/       # Python multi-model orchestrator
│   ├── src/fathomx/    # Source code
│   └── tests/          # Unit tests
├── mcp-setup/          # MCP registration scripts
├── install.sh          # Main installer
└── install.js          # npx installer
```

## What to Contribute

- Bug fixes for `install.sh` across different platforms
- New report templates or format improvements
- Documentation improvements and translations
- MCP tool integration enhancements
- Strategy refinements based on real-world research usage

## Guidelines

- Keep shell scripts POSIX-compatible where possible
- Test `install.sh` changes on both macOS and Linux
- Skill files (`.md`) should follow the existing structure in `skill/`
- Do not commit API keys or credentials

## Reporting Issues

Use the [GitHub issue templates](https://github.com/Runa798/claude-deep-research/issues/new/choose) to report bugs or request features.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
