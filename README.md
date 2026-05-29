# PM DeepResearch

**PM DeepResearch** is a product manager's **deep competitive-research skill** for Claude Code. It turns a product decision ("should we enter / differentiate / build / upgrade to AI?") into a decision-oriented, evidence-complete **13-chapter competitive report**, applying a five-dimension product methodology (Job & real competitive set, capability matrix, Kano, ODI opportunity gaps, positioning & whitespace) with explicit epistemic tagging and falsifiability.

It is a **Skill / orchestration layer (Layer 1)** that runs on top of the **Lapis** MCP research core (Rust, upstream [`4o3F/Lapis`](https://github.com/4o3F/Lapis), AGPL-3.0). Lapis owns MCP execution, provider calls, agent loops, budget guards, schema validation, and byte-equal evidence provenance; PM DeepResearch carries the product methodology via prompt assets + Skill-layer assembly. Lapis is consumed unchanged — any engine-schema needs are filed upstream as requirements, not patched in.

> Status: Phase 3 — **v2.0 core validated**. A 6-aspect Deep run on a golden topic (Strava AI-coaching upgrade) produced a 13-chapter report scoring **22/24** on the project rubric. Structure reorg (vendored-engine extraction + one-click installer) is scheduled for Phase 4.

## The skill

| Path | What it is |
| --- | --- |
| [`skills/pm-deep-research/SKILL.md`](skills/pm-deep-research/SKILL.md) | The competitive deep-research skill entry: decision-intent routing, complexity tiers, five-dim decomposition, persona assembly, Lapis MCP calls, evidence post-processing, gap audit + quality-floor self-verification, 13-chapter report. |
| `skills/pm-deep-research/prompts/layer1/` | Orchestration prompts: `task-decomposition`, `agent-allocation`, `evidence-postprocess`, `final-report`, `claude-only-degradation`. |
| `skills/pm-deep-research/prompts/layer2/` | Persona prompts: `persona-strategist`, `persona-experience-analyst`. |
| [`skills/deep-research.md`](skills/deep-research.md) | Generic Lapis research skill kept as a fallback / base. |

When the Lapis MCP server is unavailable, the skill degrades to **Claude-only** (search MCP directly, same methodology) — degradation is not failure; the methodology lift is pure prompt capability.

## Key documents

| Document | Purpose |
| --- | --- |
| [`ROADMAP.md`](ROADMAP.md) | Single source of truth for the plan (rolling-wave). |
| [`docs/specs/pm-deep-research-competitive-research-spec.md`](docs/specs/pm-deep-research-competitive-research-spec.md) | Canonical competitive-research spec (five-dim, 13 chapters, evidence discipline). |
| [`docs/specs/orchestration-interface.md`](docs/specs/orchestration-interface.md) | Layer 1 ↔ Lapis interface (request/result, budget, evidence post-processing, degradation). |
| [`docs/evaluation/rubric.md`](docs/evaluation/rubric.md) | 12-dimension scoring rubric + prose floor; golden-sample anchor. |
| [`docs/decisions/`](docs/decisions/README.md) | Architecture decision records (ADR-0001…0006). |

## Vendored Lapis engine

This repository currently **vendors the Lapis engine source** (`crates/`, `Cargo.toml`, `lapis.example.toml`) so the MCP core can be built and run locally during development and validation. The engine is upstream-owned ([`4o3F/Lapis`](https://github.com/4o3F/Lapis)); we do not develop it here. Per [ADR-0002](docs/decisions/README.md), Phase 4 replaces the vendored copy with a one-click installer that fetches and builds upstream Lapis, at which point the vendored source is extracted.

Build and run the engine locally:

```bash
cargo build --release
cp lapis.example.toml lapis.toml          # then enable providers + export the referenced API keys
./target/release/lapis serve --config lapis.toml
```

The server speaks MCP over stdio and exposes two tools:

| Tool | Purpose |
| --- | --- |
| `aspect_research` | Runs one research aspect and returns an `AspectResearchResult`. |
| `deep_research` | Runs multiple research aspects and returns a `DeepResearchResult`. |

Supported request `schema_version`: `0.1`. Engine-side details:

| Document | Purpose |
| --- | --- |
| [`docs/mcp-usage.md`](docs/mcp-usage.md) | MCP client interface and tool schemas. |
| [`docs/configuration.md`](docs/configuration.md) | Runtime configuration, providers, budgets, logging. |
| [`docs/development.md`](docs/development.md) | Repository layout and contributor commands. |

## Requirements

- Rust toolchain with Rust 2024 edition support (to build the vendored engine).
- Claude Code (or another MCP client) able to run stdio MCP servers.
- At least one enabled model provider, and a search provider for aspects that allow search.

## Common development checks

```bash
cargo fmt --all -- --check
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
```

## License

GNU Affero General Public License v3.0. See [`LICENSE`](LICENSE) for details.
