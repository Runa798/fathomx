# Gemini Search Grounding — Supplementary Search Source

Gemini 3.1 Pro with Google Search grounding provides an additional search perspective beyond Grok MCP and Exa MCP.

---

## When to Use

| Scenario | Use Gemini Search? |
|----------|-------------------|
| Deep tier research, after Grok+Exa searches | Yes — as third parallel source |
| Gap detection found insufficient coverage on a dimension | Yes — supplementary search |
| Query about recent events (last 30 days) | Yes — Google index is most current |
| Standard tier with specific need for Google-indexed content | Optional |
| Quick tier | No — not worth the latency |

## How to Invoke

Via the orchestrator:

```bash
python3 -m fathomx run gemini_search \
  --workspace workspace/research-{date}-{slug} \
  --query "your search query" \
  --output "search/gemini-{topic-slug}.md"
```

## Output Format

The task writes a Markdown file with:
1. Gemini's synthesized response (with Google Search grounding)
2. Source list extracted from `groundingMetadata.groundingChunks`
3. Each source has title and URL

## Integration with Other Sources

Gemini Search results should be:
- **Deduplicated** against Grok and Exa results by URL
- **Cross-referenced** for factual claims — if Gemini confirms a Grok finding, increase confidence
- **Treated as supplementary** — Grok + Exa remain the primary search tools
- **Cited** in the report using the same `[n]` notation as other sources
- **Rated** for credibility (A-E) based on the underlying Google Search sources, not Gemini's synthesis

## Configuration

Requires:
- SEARCH tier configured in `~/.fathomx/config.json`
- Google API key with access to Gemini API
- `features.gemini_search: true`

If unconfigured, skip silently — Gemini Search is always optional.
