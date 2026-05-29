### Problem

`deep_research` aspects fail with `network_failed: "SSE stream exceeded event limit"` when the model is a reasoning model streamed via the OpenAI Responses API (`stream: true`). One structured `AspectResearchResult` synthesis turn emits more SSE events than the hardcoded `MAX_SSE_EVENTS = 4096` in `crates/lapis-net/src/reqwest_client.rs`.

### Measured

gpt-5.5 (OpenAI-compatible endpoint), 6-aspect `deep_research`: synthesis turns reached **4904 / 6485 / 4692** events (peak 6485); peak stream data ~1.5 MB. Every turn over 4096 aborts and fails its aspect.

### Why it blocks consumers

The caps are compile-time constants and intentionally not configurable — the `rejects_network_stream_knobs` test rejects `stream_max_events` etc. from config. So the only workaround is patching + rebuilding.

### Request

Raise the default `MAX_SSE_EVENTS` (e.g. ≥ 16384), or expose `MAX_SSE_EVENTS` / `MAX_SSE_TOTAL_DATA_BYTES` as `[network]` config knobs.
