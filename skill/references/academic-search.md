# Academic Search Integration

Optional academic search capability via Semantic Scholar API. No API key required for basic usage.

---

## When to Use

Activate academic search when the research topic involves:
- Scientific claims that need peer-reviewed backing
- Technology comparisons where academic benchmarks exist
- Medical, biological, or pharmaceutical topics
- AI/ML model evaluations, benchmarks, or architecture comparisons
- Any topic where the user explicitly requests "学术论文" / "papers" / "research papers"

Do NOT use for:
- Product pricing, market share, or business intelligence (Grok + Exa are better)
- Current events or news (academic papers lag by months)
- Software documentation or API references (use context7 or Grok)

---

## Semantic Scholar API

**Base URL**: `https://api.semanticscholar.org/graph/v1`

**No API key required** for basic usage (100 requests/5 minutes). For higher limits, request a key at https://www.semanticscholar.org/product/api.

### Paper Search

```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=10&fields=title,url,year,authors,abstract,citationCount,venue,openAccessPdf
```

Use `web_fetch` to call this endpoint. Parse the JSON response.

### Key Fields

| Field | Use |
|-------|-----|
| `title` | Paper title for citation |
| `url` | Semantic Scholar page URL |
| `year` | Publication year — filter for recency |
| `authors` | Author list for credibility assessment |
| `abstract` | Summary — use for relevance judgment |
| `citationCount` | Higher = more influential |
| `venue` | Conference/journal name — credibility signal |
| `openAccessPdf.url` | Direct PDF link if available |

### Credibility Mapping

| Venue Type | Credibility Rating |
|------------|-------------------|
| Top-tier conferences (NeurIPS, ICML, ACL, CVPR, SIGCHI) | A |
| Respected journals (Nature, Science, IEEE, ACM) | A |
| Workshop papers, preprints (arXiv) | C |
| Unknown venue, no venue listed | D |

Papers with `citationCount > 50` get a credibility boost (e.g., C → B).

---

## Integration with Research Tiers

### Quick Tier
- Not used. Academic search adds latency that isn't justified for single-fact lookups.

### Standard Tier
- **Optional**: Run one Semantic Scholar search in parallel with Grok + Exa if the topic is technical/scientific.
- Limit to 5 results. Use abstracts only — no full-paper retrieval.

### Deep Tier
- **Recommended for technical topics**: Add as a parallel sub-task in Wave 1.
- Search with 2-3 query variations (broad + specific).
- For high-citation papers (`citationCount > 100`), fetch the full PDF via `openAccessPdf.url` if available.
- Cross-reference academic findings with Grok/Exa web results in the synthesis phase.

---

## Example Workflow

```
1. Construct query: "transformer architecture efficiency inference optimization"
2. web_fetch("https://api.semanticscholar.org/graph/v1/paper/search?query=transformer+architecture+efficiency&limit=10&fields=title,url,year,authors,abstract,citationCount,venue,openAccessPdf")
3. Parse JSON → filter by year >= 2024, sort by citationCount
4. Top 3-5 papers → extract key claims from abstracts
5. Cross-reference with Grok/Exa findings
6. Cite in report with credibility rating A or B
```

---

## Rate Limits

- **Without API key**: 100 requests per 5 minutes
- **With API key**: 1 request per second (more generous)
- If rate-limited (HTTP 429), receiving malformed JSON, or an empty result set: do not retry aggressively. Record the failure in Methodology and continue with other sources. Academic search is supplementary — its failure should never block the overall research.
