# Research Methodology — Scope Expansion, Personas, and Gap-Driven Iteration

This file encodes the product research methodology that transforms a literal question into a comprehensive investigation. Read this file during Standard and Deep tier research, AFTER complexity assessment but BEFORE any searching.

---

## 1. Scope Expansion Engine

When the user asks a research question, DO NOT answer it literally. First, expand it into a comprehensive research scope using the MECE 6-dimension framework.

### The MECE 6-Dimension Template

For ANY product/market research question, decompose into these six mutually exclusive, collectively exhaustive dimensions:

| # | Dimension | What to Investigate | Example Sub-Questions |
|---|-----------|--------------------|-----------------------|
| 1 | **Market Context** | TAM/SAM/SOM, growth rate, regulatory landscape, macroeconomic trends, industry lifecycle stage | What is the market size? What drives growth? What regulatory constraints exist? |
| 2 | **Competitive Landscape** | Direct competitors, indirect competitors, substitutes, potential entrants, competitive dynamics | Who are the top 5 players? What are their strategies? Where is white space? |
| 3 | **User Jobs & Needs** | Jobs-to-be-Done, outcome expectations, pain points, switching triggers, underserved segments | What job does the user hire this product for? What outcomes matter most? Where are users most frustrated? |
| 4 | **Product Capabilities** | Feature comparison, UX quality, pricing architecture, technology stack, integration ecosystem | How do products compare on dimensions buyers care about? What is each product's core strength? |
| 5 | **Strategic Position** | Moats, gaps, opportunities, SWOT, ERRC (Eliminate-Reduce-Raise-Create) | What competitive moats exist? Where are the biggest opportunities? What should be eliminated/created? |
| 6 | **Future Trajectory** | Emerging trends, technology disruptions, market forecasts, noncustomer segments, adjacent opportunities | What trends will reshape this market in 2-3 years? Who are the noncustomers and why? |

### How to Apply

1. Read the user's question carefully
2. Infer the **decision intent**: "What decision will the user make based on this research?"
3. Generate sub-questions for ALL six dimensions, tailored to the specific topic
4. For Quick tier: pick the 1-2 most relevant dimensions only
5. For Standard tier: cover at least 4 dimensions
6. For Deep tier: cover ALL 6 dimensions with multiple sub-questions each
7. Write the expanded scope to `workspace/plan.md`

### Example Expansion

**User asks**: "调研天天跳绳APP的用户人群，给出AI时代下的方向"

**Inferred decision intent**: "Decide what AI features to build for the TianTian Jump Rope app"

**Expanded scope**:
1. Market Context: Chinese fitness app market size, growth, AI fitness trend adoption rates
2. Competitive Landscape: Direct competitors (Keep, 薄荷健康), indirect (Apple Fitness+), AI fitness startups
3. User Jobs: Why users "hire" a jump rope app (tracking, motivation, community), underserved outcomes
4. Product Capabilities: Feature comparison across competitors, AI features already deployed in fitness
5. Strategic Position: TianTian's moats (jump rope specialization), gaps vs. competitors, ERRC grid for AI features
6. Future Trajectory: AI capabilities applicable to fitness (computer vision, personalized coaching), market forecasts

---

## 2. Three Research Personas

After scope expansion, apply three distinct research personas to ensure multi-perspective coverage. Each persona brings a different analytical lens and produces a different type of output.

### Persona 1: Market Analyst

**Focus**: Market sizing, trends, growth dynamics, regulatory landscape
**Frameworks**: TAM/SAM/SOM estimation, market lifecycle analysis, macro trend mapping
**Output**: Market size estimates with methodology, growth trajectory, trend analysis, risk factors
**Reasoning style**: Data-driven, quantitative, macro-level

Use this persona for Dimensions 1 (Market Context) and 6 (Future Trajectory).

### Persona 2: Competitive Intelligence Analyst

**Focus**: Competitor strategies, positioning, feature parity, moats, vulnerabilities
**Frameworks**: Porter's Five Forces, competitive feature matrix (scored 0-3, buyer-importance weighted), strategic group mapping, moat analysis
**Output**: Competitor identification (4 tiers), feature matrix, positioning map, moat assessment
**Reasoning style**: Comparative, strategic, opportunity-focused

Use this persona for Dimensions 2 (Competitive Landscape) and 4 (Product Capabilities).

### Persona 3: Product Strategist

**Focus**: User needs, jobs-to-be-done, opportunity scoring, strategic recommendations
**Frameworks**: JTBD (job map, outcome expectations, opportunity score), Blue Ocean ERRC Grid, Opportunity Solution Tree
**Output**: Core jobs identification, opportunity scores, ERRC grid, prioritized recommendations with evidence
**Reasoning style**: User-centric, synthesis-oriented, action-focused

Use this persona for Dimensions 3 (User Jobs) and 5 (Strategic Position).

### How to Apply Personas

**Standard tier**: Claude applies all three persona lenses itself during synthesis. No external model calls needed — just read the persona descriptions above and adopt each perspective sequentially.

**Deep tier with multi-model**: Call the orchestrator to run persona analyses on external models:
```bash
python3 -m deep_research run analyze --persona market-analyst --workspace {session-dir} --context "{topic}"
python3 -m deep_research run analyze --persona ci-analyst --workspace {session-dir} --context "{topic}"
python3 -m deep_research run analyze --persona product-strategist --workspace {session-dir} --context "{topic}"
```
These produce separate analysis files in `workspace/analysis/` that Claude reads for final synthesis.

---

## 3. Gap-Driven Iteration

After initial search and analysis, evaluate completeness before synthesizing. This is the quality assurance loop that prevents shallow research.

### Gap Detection Checklist

For each of the 6 MECE dimensions, check:

| Check | Passing Criteria | If Failing |
|-------|-----------------|------------|
| **Source count** | ≥ 3 independent sources per dimension | Trigger supplementary search for that dimension |
| **Source diversity** | At least 2 different source types (e.g., not all from same search engine) | Run additional search tool (Exa if only Grok was used, or vice versa) |
| **Contradiction resolution** | All conflicting claims have been noted with both sides presented | Fetch additional sources to arbitrate |
| **Persona coverage** | Each applicable persona has addressed its assigned dimensions | Re-run persona analysis on missing dimensions |
| **Factual grounding** | Key claims have numerical evidence (not just qualitative assertions) | Search specifically for data/statistics on that claim |
| **Recency** | Data is from within the last 12 months for market/competitive dimensions | Add date filter to supplementary searches |

### Iteration Rules

- **Standard tier**: Maximum 1 gap-fill iteration
- **Deep tier**: Maximum 2 gap-fill iterations
- **Stop condition**: All dimensions pass all checks, OR maximum iterations reached
- **Diminishing returns**: If a dimension still fails after 2 iterations, note the gap explicitly in the report's Limitations section rather than continuing to search

### How to Execute Gap-Fill

1. Read all search and analysis files from workspace
2. Apply the checklist above
3. For each failing dimension:
   a. Identify what specific information is missing
   b. Construct targeted search queries (not broad — specific to the gap)
   c. Execute searches via MCP tools (Grok, Exa) or orchestrator (Gemini)
   d. Write supplementary results to `workspace/search/gap-{dimension}.md`
4. Update the state.json to reflect the gap-fill phase
5. Re-read all files and proceed to synthesis

---

## 4. Tool-to-Dimension Mapping

Different search tools are better suited for different research dimensions:

| Dimension | Best Tools | Why |
|-----------|-----------|-----|
| Market Context | Grok (web_search, extra_sources=10), Gemini Search | Market reports, analyst data, industry publications |
| Competitive Landscape | Exa (company_research_exa), Exa (web_search_advanced_exa) | Entity discovery, company-specific information |
| User Jobs & Needs | Grok (web_search), Exa (web_search_exa for reviews/forums) | User reviews, forum discussions, app store data |
| Product Capabilities | Exa (get_code_context_exa), Grok (web_fetch for product pages) | Product documentation, feature pages, technical specs |
| Strategic Position | Grok (web_search), Exa (find_similar) | Analyst reports, strategy articles, adjacent companies |
| Future Trajectory | Semantic Scholar (academic-search.md), Grok, Gemini Search | Research papers, trend reports, forecasts |

Use this mapping to assign the right tools to each dimension during the search phase.

---

## 5. Integration with Report Structure

The final report MUST be organized by dimension, not by tool or search round. See `templates/deep-report.md` for the template.

Each dimension section should contain:
1. Key findings with confidence indicators (🟢🟡🔴)
2. Source citations with credibility ratings (A-E)
3. Persona analysis insights (which persona contributed what)
4. Explicit gaps and limitations

The Executive Summary should directly address the user's **decision intent** (inferred in scope expansion), not just summarize facts.

The Recommendations section should trace each recommendation back to evidence in specific dimensions and persona analyses. No recommendation without evidence.
