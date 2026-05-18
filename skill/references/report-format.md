# Research Report Formatting Rules

Formatting standards for all research output produced by the deep-research skill.

---

## General Rules

1. **Language**: Write reports in the user's language. Default is Chinese (中文) unless the research context is explicitly English-language (e.g., the topic is an English-language product, the user writes in English, or the source material is exclusively English).
2. **Source attribution**: Every factual claim MUST carry a citation marker `[n]`. Claims without sources are not allowed.
3. **Markdown formatting**: Use headers (`##`, `###`), tables, and bullet points. Avoid raw prose walls.
4. **Confidence indicators**: Attach a confidence indicator to key conclusions and high-stakes claims.

### Confidence Indicators

| Indicator | Meaning | Criteria |
|-----------|---------|----------|
| 🟢 High confidence | Claim is well-supported | 3+ independent sources agree, no contradicting sources |
| 🟡 Medium confidence | Claim is plausible but not certain | 1–2 sources only, or sources partially conflict |
| 🔴 Low confidence | Claim is uncertain | Single unverified source, sources directly conflict, or claim extrapolated from indirect evidence |

---

## Report Structure

Adapt sections based on the report template (quick/standard/deep), but the general order is:

### 1. Executive Summary
2–3 sentences. What is the answer / main finding? What does the user need to know right now?

### 2. Key Findings
Numbered list. Each finding is one sentence, followed by its confidence indicator and source citation(s).

Example:
```
1. Market leader X holds ~42% market share as of Q1 2026. 🟢 [1][2]
2. Product Y launched a competing feature in March 2026. 🟡 [3]
3. Analyst forecasts suggest 18% CAGR through 2029, though estimates vary widely. 🔴 [4]
```

### 3. Detailed Analysis
Structured by topic dimension or research question — NOT by which tool produced the result. Use `###` subheaders. Include tables for comparisons.

### 4. Source Comparison (for Standard and Deep tiers)
Where do Grok and Exa results agree? Where do they diverge? Are there conflicting claims that the user should be aware of? This section surfaces uncertainty explicitly rather than hiding it in the prose.

### 5. Sources
Numbered list. Include title, URL, and access date for every source cited in the report.

```
[1] Title of the page — https://example.com/page (accessed 2026-05-18)
[2] Title of the article — https://another.com/article (accessed 2026-05-18)
```

If a source was retrieved via `web_fetch` for full-text verification, note it with `(full text retrieved)`.

### 6. Methodology
Brief notes on:
- Which research tier was used (Quick / Standard / Deep)
- Which tools were used (Grok, Exa, browser layer)
- Number of queries executed
- Any limitations: sources that could not be accessed, rate limits hit, CAPTCHAs encountered, login-walled content skipped

---

## Comparison Tables

Use tables for any side-by-side comparison. Always include a Source column.

```markdown
| Dimension   | Option A      | Option B      | Source  |
|-------------|---------------|---------------|---------|
| Price       | $10/mo        | $15/mo        | [1][2]  |
| Performance | 2ms p99       | 5ms p99       | [3]     |
| OSS license | MIT           | Apache 2.0    | [4]     |
| Last update | 2026-03       | 2025-11       | [1][5]  |
```

---

## Citation Format

**In-text**: Use `[n]` immediately after the claim, before any punctuation.

- Single source: `The API supports streaming responses [1].`
- Multiple sources: `This is widely reported [1][3][5].`
- Conflicting claim: `According to [1], the limit is 1000 RPM; however, [2] reports 500 RPM for free tier accounts.`

**Source list**: See Section 5 above.

---

## What NOT to Do

- Do not include a finding without at least one source citation.
- Do not silently resolve a conflict between sources — surface it.
- Do not present extrapolated conclusions with 🟢 confidence — if it's inferred, it gets 🟡 at best.
- Do not list sources that were not actually cited in the report body.
- Do not pad the report with filler text or caveats that add no informational value.
