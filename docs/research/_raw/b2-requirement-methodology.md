# B2 — How Excellent Product Requirements Are Actually Produced

> Research for FathomX "产品需求深度调研" capability.
> Every claim has a citable source. Unverified/inferred items are labelled **[UNVERIFIED]** or **[PRACTITIONER FRAMEWORK]**.
> Date: 2026-05-29

---

## 1. Marty Cagan / SVPG — Product Discovery + Four Big Risks

**What it is**
A continuous product team practice that de-risks ideas *before* committing engineering resources by explicitly addressing four distinct risk types. Discovery and delivery run as parallel tracks, not sequential phases.

**Primary source**
- Cagan, M. (2017). *Inspired: How to Create Tech Products Customers Love* (2nd ed.). SVPG Press / Wiley.
- Cagan, M. (2017-12-04). "The Four Big Risks." SVPG blog. <https://www.svpg.com/four-big-risks/>
- Cagan, M. (2007-09-24). "Product Discovery." SVPG blog. <https://www.svpg.com/product-discovery/>

**How it concretely works**

The product team (PM + Designer + Tech Lead) attacks four risks in parallel:

| Risk | Owner | Question |
|---|---|---|
| Value | PM | Will customers buy/use this? |
| Usability | Designer | Can users figure it out? |
| Feasibility | Tech Lead | Can we actually build it? |
| Business Viability | PM | Does it work for the business (revenue, legal, brand, partners)? |

Steps:
1. **Opportunity Assessment** — Written statement naming the business objective and identifying which of the four risks are significant. If no significant risk exists, skip discovery and move to delivery.
2. **Weekly customer interviews + prototype tests** — "Product trio" (PM, Designer, Engineer) meets real users weekly. Throw-away prototypes are the primary artifact.
3. **Parallel spikes** — High-fidelity prototypes for usability; technical spikes / proofs-of-concept for feasibility; pricing tests and margin models for value/viability.
4. **Threshold check** — Team exits discovery only when all four risks are reduced to an acceptable level.
5. **Delivery** — Engineering builds what discovery has validated.

Key artifact: **prototype + assumption list** (not a spec document). PRD-like documents are produced *after* discovery, as an output to engineering.

**Validation status**
Practitioner framework (SVPG consulting practice). Widely adopted by Silicon Valley product companies. Not peer-reviewed academic research.

**Real case**
Amazon Prime: Cagan cites at length (svpg.com/product-model-at-amazon, 2024). The Prime team ran discovery experiments on shipping cost/speed trade-offs before committing to the subscription model. The PRFAQ and six-pager documents served as the discovery artifacts.

**FathomX landing point**
FathomX should assess all four risks when producing a requirement research report. The report should include a "Risk Landscape" section (which risks are high/medium/low for this requirement, and what evidence reduces each risk). Discovery completeness — not just feature description — determines report quality.

---

## 2. Teresa Torres — Continuous Discovery Habits + Opportunity-Solution Tree (OST)

**What it is**
A weekly cadence in which the product trio conducts customer interviews and maps findings onto an Opportunity-Solution Tree (OST) — a visual structure connecting business outcome → customer opportunities → solutions → assumption tests.

**Primary source**
- Torres, T. (2021). *Continuous Discovery Habits: Discover Products That Create Customer Value and Business Value*. Product Talk LLC. ISBN 9781736633304.
- Torres, T. (2023-12-06). "Opportunity Solution Trees: Visualize Your Discovery to Stay Aligned and Drive Outcomes." producttalk.org. <https://www.producttalk.org/opportunity-solution-trees/>
- Torres, T. (2021-05-19). Book announcement. <https://www.producttalk.org/continuous-discovery-habits/>

**How it concretely works**

OST structure (four levels, root at top):

```
OUTCOME  (1 per tree — e.g., "Increase weekly active users 15% by Q3")
    └── OPPORTUNITY  (customer need / pain / desire — expressed from customer PoV)
            └── SOLUTION  (feature, workflow, content, integration, etc.)
                    └── ASSUMPTION TEST  (interview snippet, prototype, A/B test, landing page)
```

Building steps:
1. Align team on a single measurable **product outcome** (not a laundry list of goals).
2. Conduct ≥1 customer interview per week; capture unmet needs/pains as **opportunities**.
3. Map opportunities hierarchically — large opportunities break into sub-opportunities using "key moments in time" in the customer's experience journey (Chapter 6 of the book).
4. Choose a **target opportunity** to focus the team.
5. Generate ≥3 **solutions** per opportunity (compare-and-contrast discipline, prevents lock-in).
6. For each solution, identify the riskiest assumptions and design cheap **assumption tests** before building.
7. Continuously prune and re-structure the tree as learning accumulates.

Key artifacts: the OST visual (can be a whiteboard, Miro board, or dedicated tool); weekly interview notes; assumption test logs.

**Validation status**
Practitioner framework. Book is evidence-informed (Torres cites behavioural science and design research in footnotes) but the OST itself is not the subject of a controlled study. Over 135,000 copies sold (as of 2026).

**Real case**
- **Grailed** (fashion resale platform): Torres documents a 20% LTV lift after the team used OST to focus on a specific purchase-friction opportunity rather than broad "improve conversion." (producttalk.org case study, verifiable URL: <https://www.producttalk.org/opportunity-solution-trees/>)
- **Trivago**, **BBC Maestro**, **TextHelp**, **SuperAwesome**, **Seera Group** also cited on the same page.

**FathomX landing point**
The OST structure is the direct model for FathomX's opportunity-prioritization layer. A FathomX research output should always show: which outcome the requirement serves → which customer opportunity it addresses → what solutions have been considered → what assumptions remain untested. This maps directly onto OST levels 1–4.

---

## 3. Tony Ulwick — Outcome-Driven Innovation (ODI) + JTBD Opportunity Scoring

**What it is**
A quantitative innovation process built on the theory that customers hire products to get jobs done. ODI captures all desired outcomes (the metrics customers use to judge job completion), surveys their importance and current satisfaction, and calculates an opportunity score for each.

**Primary sources**
- Ulwick, A.W. (2002). "Turn Customer Input into Innovation." *Harvard Business Review*, January 2002. <https://hbr.org/2002/01/turn-customer-input-into-innovation> (paywalled; PDF at thecustomerconnection.nl)
- Ulwick, A.W. (2016). *JOBS TO BE DONE: Theory to Practice*. IDEA BITE Press. ISBN: verified publisher.
- Ulwick, A.W. (2017). "The Path to Growth: The Opportunity Algorithm." *The Marketing Journal*, July 9, 2017. <https://www.marketingjournal.org/the-path-to-growth-the-opportunity-algorithm-anthony-ulwick/>
- anthonyulwick.com/outcome-driven-innovation/ (primary company site, published 2016).

**Opportunity algorithm (exact formula, verified from marketingjournal.org)**

```
Opportunity Score = Importance + max(0, Importance − Satisfaction)
```

Where both Importance and Satisfaction are rated on a 1–10 scale by representative customer sample (typically n ≥ 180 for B2C, lower for B2B).

- Score > 10 → underserved opportunity (invest)
- Score 7–10 → appropriately served
- Score < 7 → overserved (do not invest; may reduce/remove)

**How it concretely works**

Five-step ODI process (from HBR 2002 article and Ulwick's site):

1. **Outcome-based interviews** — Customers are asked not "what features do you want?" but "what are you trying to accomplish?" and "what metrics do you use to judge success?" Each desired outcome follows a strict linguistic structure: *direction + metric + object + context* (e.g., "minimize the time it takes to restore blood flow in an occluded artery").
2. **Outcome consolidation** — 50–150 desired outcome statements are gathered per job. Duplicates and solutions-as-outcomes are eliminated.
3. **Quantitative survey** — Representative sample rates each outcome on: (a) importance and (b) how well current solutions satisfy it (both 1–10).
4. **Opportunity scoring** — Formula applied; results visualised on the **Opportunity Landscape** (2-axis scatter plot: importance × satisfaction; underserved quadrant = high importance, low satisfaction).
5. **Solution design** — R&D focuses on top-scored outcomes; existing products or new concepts are evaluated against these metrics before development begins.

**Validation status**
Practitioner framework with proprietary outcome data. Ulwick claims 86% innovation success rate vs 17% industry baseline (cited in Strategyn white paper at innovationroundtable.com — this 86% stat is Ulwick's own retrospective claim; it is **not independently peer-reviewed**). The HBR 2002 article and the formula are verifiable primary sources. The 86% figure should be treated as **[PRACTITIONER CLAIM, NOT INDEPENDENTLY VALIDATED]**.

**Real case (verified, primary source)**
**Cordis Corporation (1991):** Medical device company with <1% angioplasty balloon market share. Ulwick applied ODI with cardiologists and OR nurses, scoring 50+ desired outcomes. Top unmet outcome: "minimize the likelihood that the treated artery re-occludes." This pointed toward a then-nascent device (the coronary stent). Cordis became first-to-market; stent became fastest-growing medical device in history; Johnson & Johnson acquired Cordis at $109/share (vs ~$20 at start). Source: <https://strategyn.com/jobs-to-be-done/cordis-case-study/> and Ulwick's own account at <https://strategyn.com/predictable-innovation-business-growth-strategy/>.

**FathomX landing point**
FathomX's opportunity-scoring module should implement the ODI formula as its quantitative backbone. For any requirement research, FathomX should: (a) decompose the requirement into desired-outcome statements, (b) gather or infer importance/satisfaction data (via survey, user research excerpts, or market proxy), (c) output ranked opportunity scores. The Opportunity Landscape scatter plot is a natural FathomX report visualisation.

---

## 4. Kano Model — Feature Classification by Satisfaction Type

**What it is**
A survey methodology that classifies product features into five categories based on the non-linear relationship between feature presence/absence and customer satisfaction/dissatisfaction.

**Primary source**
- Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive Quality and Must-Be Quality." *Journal of the Japanese Society for Quality Control*, Vol. 14, No. 2, pp. 147–156. Published April 15, 1984. DOI via J-STAGE: <https://www.jstage.jst.go.jp/article/quality/14/2/14_KJ00002952366/_article/-char/en> (journal-restricted access; citation verified via SCIRP reference database and J-STAGE metadata).

**How it concretely works**

Survey pairs a **functional** ("if present, how do you feel?") and **dysfunctional** ("if absent, how do you feel?") question for each feature. Five-point response scale: Like / Expect / Neutral / Tolerate / Dislike.

Classification matrix (row = dysfunctional answer, column = functional answer):

| | Like | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| **Like** | Q (Questionable) | A (Attractive) | A | A | O (One-dim.) |
| **Expect** | R (Reverse) | I (Indifferent) | I | I | M (Must-be) |
| **Neutral** | R | I | I | I | M |
| **Tolerate** | R | I | I | I | M |
| **Dislike** | R | R | R | R | Q |

Categories:
- **Must-be (M)**: Absence causes dissatisfaction; presence is taken for granted (e.g., car brakes).
- **One-dimensional (O)**: Linear satisfaction — more is better, less is worse (e.g., battery life).
- **Attractive (A)**: Unexpected delight when present; no dissatisfaction when absent (e.g., pinch-to-zoom on first iPhone, per practitioner literature).
- **Indifferent (I)**: No impact either way.
- **Reverse (R)**: Presence decreases satisfaction (feature misaligned with this segment).

Priority rule when counts are tied: M > O > A > I.
Minimum sample: 30–50 respondents for statistical stability (practitioner guideline; no specific paper sets this threshold).

**Validation status**
Academically validated (1984 paper, 3,600+ citations per koji.so). Original paper is in Japanese; widely translated and applied in quality management and product development. Survey methodology is well-documented.

**Real case**
**iPhone pinch-to-zoom (2007)**: Cited across practitioner literature as a canonical Attractive feature — users did not ask for it, had no expectation of it, but reacted with delight. No dissatisfaction in its absence (pre-2007 phones). **[NOTE: This specific Kano classification is a retrospective practitioner interpretation, not from a published Kano study of the iPhone.]**

**FathomX landing point**
FathomX can use Kano classification to layer the opportunity landscape: Must-be requirements are baseline hygiene (risk if absent), Attractive requirements are differentiation candidates. In a research report, FathomX should flag whether a proposed requirement is M/O/A category — this changes the investment logic entirely.

---

## 5. Jeff Patton — User Story Mapping

**What it is**
A two-dimensional product backlog visualisation technique that organises user activities horizontally (as a "backbone") and breaks them into tasks and stories vertically, enabling teams to cut "walking skeleton" release slices rather than building features in isolation.

**Primary source**
- Patton, J. (2014). *User Story Mapping: Discover the Whole Story, Build the Right Product*. O'Reilly Media. ISBN 9781491904893. <https://www.oreilly.com/library/view/user-story-mapping/9781491904893/>
- Patton, J. (2005, Jan). "It's Not Just Standing Up." First written description of story mapping practice. (Predates book; referred to at jeffpatton.wpengine.com)

**How it concretely works**

Map structure:

```
[Activity 1]  →  [Activity 2]  →  [Activity 3]  ...  (BACKBONE — horizontal, left-to-right workflow)
   [Task 1a]       [Task 2a]       [Task 3a]           (sub-steps of each activity)
   [Task 1b]       [Task 2b]       ...
      [Story 1a1]  [Story 2a1]                         (vertical detail — smallest user needs)
      [Story 1a2]
--- RELEASE 1 (walking skeleton) --------------------------------
      [Story 1b1]  [Story 2b2]                         (Release 2)
```

Building steps:
1. **Frame the problem** — State the user goal and the business opportunity.
2. **Map the backbone** — Write activity cards (broad user goals) in left-to-right narrative order.
3. **Break down tasks** — Under each activity, add task cards (discrete observable actions).
4. **Add stories** — Under each task, add story cards (concrete user needs, classic "As a … I want … so that …" format).
5. **Identify the walking skeleton** — Draw a horizontal line after the topmost story in each column; everything above the line is the minimum viable product slice that exercises the full backbone end-to-end.
6. **Plan releases** — Additional horizontal lines create incremental release slices.

Key artifacts: physical card wall (or digital Miro/FigJam board); walking skeleton slice; release roadmap.

**Validation status**
Practitioner framework. No RCT or peer-reviewed study validates USM specifically. Widely adopted in Agile/product teams. Technique originated ~2002–2003 in Patton's consulting practice.

**Real case**
Patton uses the Globo.com video platform team in the book — backbone: "user arrives → browses → selects → watches." Walking skeleton deployed a working video stream in weeks; subsequent releases fleshed out the map. **[NOTE: The Grok search identified this case; not independently re-verified from book text in this session — treat as LIKELY ACCURATE based on consistent multi-source references to Globo.com in USM context.]**

**FathomX landing point**
USM is relevant for FathomX's "scope framing" step: before deep-diving a requirement, FathomX can use a lightweight story map structure to show where the requirement sits in the user's journey (which activity, which task), and whether the proposed solution addresses the full backbone slice or only a narrow task. This prevents requirements that "solve a task but break the journey."

---

## 6. Prioritization Frameworks: RICE, Value-vs-Effort, WSJF

### 6a. RICE

**What it is**
A numerical scoring formula that produces a single comparable score for each product initiative.

**Primary source**
- McBride, S. (2016). "RICE: Simple Prioritization for Product Managers." Intercom Blog. Originally published ~2016; later updated and republished 2018-01-05. <https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/>

**Formula (verified from primary source)**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| Factor | Definition | Unit |
|---|---|---|
| Reach | Users/events affected per time period | Customers per quarter |
| Impact | Effect on individual user for chosen goal | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| Confidence | Certainty in estimates | 100%=high, 80%=medium, 50%=low |
| Effort | Total work for all team members | Person-months |

**Validation status**
Practitioner framework (Intercom internal tool, published as blog post). No independent validation study. Widely cited and adopted 2016–present.

**Real case**
Intercom's own product team created and used RICE to address three specific biases they identified: (1) favoring "pet projects" over high-reach ideas, (2) insufficient scrutiny of goal impact, (3) no confidence penalty for speculative ideas. (Source: McBride's original article.)

**When RICE fits**: Comparing heterogeneous items in a backlog when team wants to surface high-reach, low-effort wins and penalise speculative bets.

**FathomX landing point**
RICE is the default scoring formula FathomX should recommend for opportunity prioritisation within a product team's existing backlog context. It is simple, teachable, and addresses confidence bias.

---

### 6b. Value-vs-Effort (2×2 Matrix)

**What it is**
A 2-axis prioritisation grid sorting work into four quadrants: Quick Wins (high value, low effort), Major Projects (high value, high effort), Fill-ins (low value, low effort), Time Sinks (low value, high effort).

**Primary source**
No single documented originator. Derives from the **Eisenhower Decision Matrix** (urgent/important), adapted for product/engineering contexts. Referenced without specific authorship in Roman Pichler, Marty Cagan, and general Agile/Scrum practitioner resources (2000s–2010s). **[PRACTITIONER FRAMEWORK — no traceable primary source with date.]**

**Validation status**
Practitioner heuristic. Useful for fast visual sorting in team workshops; no formula or statistical rigor.

**When it fits**: Sprint planning / workshop prioritisation when RICE data is unavailable and team needs quick alignment.

---

### 6c. WSJF (Weighted Shortest Job First)

**What it is**
A lean/agile prioritisation formula that sequences work by dividing the economic impact of delay (Cost of Delay) by the relative job size. Shorter jobs with high delay cost rise in priority.

**Primary sources**
- Reinertsen, D.G. (2009). *The Principles of Product Development Flow*. Celeritas Publishing. (Chapter 6 — original CoD framework)
- Scaled Agile, Inc. (2024). "Weighted Shortest Job First (WSJF)." *SAFe 6.0 Framework*. <https://framework.scaledagile.com/wsjf/> (full article requires login; formula confirmed via summary).

**Formula**
```
WSJF = Cost of Delay / Job Size

Cost of Delay = User-Business Value + Time Criticality + Risk Reduction/Opportunity Enablement
```

All four factors are scored using relative Fibonacci values (1, 2, 3, 5, 8, 13 …) to force clear distinctions.

**Validation status**
Academically grounded (Reinertsen's work is cited in operations research and lean literature). SAFe adaptation is practitioner framework. Reinertsen's CoD concept is the most rigorous theoretical underpinning of any common prioritisation framework.

**When WSJF fits**: Program-level (PI Planning) sequencing of features/epics; especially when time-to-market penalties and risk-reduction value are significant differentiators.

**FathomX landing point**
FathomX should recommend WSJF over RICE for requirements with strong time-sensitivity (regulatory deadlines, market windows, competitive threats) or significant risk-reduction value, as RICE does not capture these dimensions.

---

## 7. Amazon Working Backwards / PR-FAQ

**What it is**
A product ideation and requirements discipline requiring teams to write a mock customer-facing press release plus FAQ *before* any specification or engineering work begins. Forces customer-back thinking and serves as the single document for stakeholder alignment.

**Primary sources**
- Bryar, C. & Carr, B. (2021). *Working Backwards: Insights, Stories, and Secrets from Inside Amazon*. St. Martin's Publishing Group. ISBN: 9781250267597. <https://books.google.com/books/about/Working_Backwards.html?id=b9LtDwAAQBAJ>
- Amazon Staff. (2021-02-09). "An insider look at Amazon's culture and processes." aboutamazon.com. <https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes>
- workingbackwards.com/resources/working-backwards-pr-faq/ — derivative resource by Bryar/Carr, consistent with book.

**How it concretely works**

The PR/FAQ document (total ≤6 pages: PR <1 page, FAQ ≤5 pages) structure:

**Press Release section:**
1. Headline (customer benefit, one line)
2. Sub-headline (quantified outcome)
3. Summary paragraph (city, media outlet, launch date, product + benefit summary)
4. Problem paragraph (customer pain stated plainly)
5. Solution paragraph (how the product works)
6. Customer quote (voice-of-customer)
7. Amazon/company executive quote
8. Availability and pricing
9. Boilerplate

**FAQ section:**
- Customer FAQ — anticipated questions from end users
- Internal FAQ — business model, go-to-market, regulatory, partnership questions

After PR/FAQ is approved, every feature claim in the press release is converted into a requirements checklist: "what must be true for this press release to be accurate?"

**Validation status**
Practitioner framework (Amazon internal, since ~2004). Not peer-reviewed. Rigorously documented by two long-serving Amazon executives.

**Real case (verified)**
Amazon Kindle, Amazon Prime, Amazon Echo, and AWS are all cited by Bryar and Carr as products that went through the PR/FAQ process. Cagan (svpg.com/product-model-at-amazon, 2024) also documents that Amazon's PRFAQ is its primary product vision tool, with "six-pager" narratives as the strategy complement.

**FathomX landing point**
FathomX's PRD output template should adopt the PR/FAQ structure for the *framing* section of a requirement deep-research report: the first page should read as a customer-facing press release for what success looks like. This forces FathomX users to articulate *value* before *features*.

---

## 8. Modern PRD Best Practices — Structure

**What it is**
Evolved from traditional waterfall requirements documents into a lean, living document focused on outcomes rather than feature lists. Current industry standard (2023–2024) treats the PRD as a "single source of truth" that is version-controlled and updated throughout discovery.

**Primary sources**
No single authoritative paper defines the "modern PRD." Synthesised from:
- Cagan, M. (2017). *Inspired* — argues PRDs should follow discovery, not precede it.
- Torres, T. (2021). *Continuous Discovery Habits* — product trios maintain living OSTs not static PRDs.
- Bryar, C. & Carr, B. (2021). *Working Backwards* — Amazon's six-pager narrative replaces traditional PRDs.
- Industry practitioner consensus (2023–2024): Notion/Coda/Confluence templates from PM communities.

**[NOTE: No single peer-reviewed paper defines "modern PRD structure." This section synthesises practitioner consensus.]**

**Modern PRD canonical structure (synthesised)**

```
1. Problem Statement (1 paragraph — user pain or business gap + supporting data)
2. Goals (3–5 measurable objectives)
3. Non-Goals (explicit exclusions)
4. Success Metrics (3–7 KPIs with baselines and targets)
5. User/Customer Context (JTBD, personas, journey excerpt)
6. Requirements
   a. Functional (user stories or outcome statements, prioritised M/O/A or RICE)
   b. Non-functional (performance, security, accessibility)
   c. Constraints and dependencies
7. Open Questions / Risks
8. Timeline (milestones, not Gantt)
9. Appendix (research links, interview notes, competitive landscape)
```

Maximum length: 5–7 pages (excluding appendix). Link to supporting research rather than embedding it.

**Validation status**
Practitioner consensus. Not academically validated.

---

## FathomX Design Recommendations

### (A) Opportunity-Prioritisation Method

**Recommended: ODI Opportunity Score as primary ranking + Kano classification as overlay**

Rationale:
- ODI formula (Importance + max(0, Importance − Satisfaction)) is the *only* practitioner framework with a mathematically grounded, verifiable formula tied directly to customer outcomes rather than internal estimates.
- RICE is team-internal estimation (guesswork dressed as math). ODI is customer-validated data.
- Kano overlay adds the *type* of opportunity: Must-be opportunities are risk/hygiene items; Attractive opportunities are differentiation bets. Mixing them in a single RICE score loses this crucial distinction.
- WSJF is most appropriate for sequencing already-validated requirements in a delivery pipeline, not for upstream opportunity discovery.

**FathomX implementation**: For each discovered opportunity, FathomX should:
1. Score Importance and Satisfaction (from user research inputs, survey data, or market proxies)
2. Compute ODI score
3. Classify as M/O/A (Kano)
4. Visualise on Opportunity Landscape (scatter: importance × satisfaction)
5. Output top-N underserved opportunities ranked by ODI score, with Kano type label

### (B) Requirement Deep-Research Report Template

Proposed FathomX "产品需求深度调研" output structure:

```markdown
# [Requirement/Opportunity Name] — Deep Research Report

## 1. Press Release Frame (Amazon PR-FAQ style, ≤300 words)
   Customer headline | Problem | Solution | Value promise

## 2. Opportunity Validation
   - JTBD statement (job + context)
   - ODI scores: top 5 desired outcomes (Importance | Satisfaction | Opportunity Score)
   - Kano classification
   - Opportunity Landscape summary

## 3. Risk Assessment (Cagan Four Risks)
   - Value risk: evidence level (HIGH / MEDIUM / LOW) + sources
   - Usability risk: evidence level + sources
   - Feasibility risk: evidence level + sources
   - Business viability risk: evidence level + sources

## 4. Solution Space
   - OST: 3+ candidate solutions per target opportunity
   - Assumption list (riskiest assumptions per solution)
   - Existing solutions / competitive landscape

## 5. Requirements
   - Functional requirements (outcome statements, Kano-labelled)
   - Non-functional requirements
   - Non-goals

## 6. Success Metrics
   - Primary metric (leading indicator)
   - Secondary metrics
   - Guardrail metrics

## 7. Evidence & Sources
   - Primary research (interviews, surveys)
   - Secondary research (citations — real URLs only)
   - Confidence rating per claim

## 8. Open Questions & Next Steps
```

This template synthesises: Amazon PR-FAQ framing (customer-back) + ODI/Kano opportunity scoring + Cagan four-risk assessment + Torres OST solution space + modern PRD structure.

---

## Citation Verification Notes

| Claim | Verification Status |
|---|---|
| Cagan four risks: value/usability/feasibility/viability | VERIFIED — svpg.com/four-big-risks/ (primary source, retrieved 2026-05-29) |
| Torres OST four levels: outcome→opportunity→solution→test | VERIFIED — producttalk.org/opportunity-solution-trees/ (primary source, retrieved 2026-05-29) |
| Ulwick formula: Importance + max(0, Importance−Satisfaction) | VERIFIED — marketingjournal.org/the-path-to-growth (primary source, 2017) |
| Ulwick HBR 2002 five steps | PARTIALLY VERIFIED — article confirmed to exist at hbr.org/2002/01/...; full text paywalled; PDF fetch failed encoding |
| Cordis stent case ($109/share acquisition) | VERIFIED — strategyn.com/jobs-to-be-done/cordis-case-study/ (Ulwick primary site) |
| Kano 1984 paper: journal, volume, pages | VERIFIED — J-STAGE DOI metadata retrieved; journal restricted access |
| iPhone pinch-to-zoom as Kano Attractive | UNVERIFIED as primary study — retrospective practitioner interpretation only |
| Patton book: O'Reilly 2014, ISBN 9781491904893 | VERIFIED — oreilly.com/library/view/user-story-mapping/9781491904893/ |
| Globo.com USM case study | LIKELY ACCURATE — cited consistently across multiple sources; not directly re-verified from book text |
| RICE formula and author: Sean McBride, Intercom 2016 | VERIFIED — intercom.com/blog/rice-simple-prioritization-for-product-managers/ |
| WSJF formula | VERIFIED (partial) — SAFe site requires login for full content; formula components confirmed from Grok synthesis + Reinertsen 2009 primary source confirmed |
| Amazon PR-FAQ: <1 page PR + ≤5 page FAQ | VERIFIED — aboutamazon.com excerpt from Working Backwards book (2021) |
| ODI 86% success rate vs 17% baseline | UNVERIFIED as independent data — Ulwick/Strategyn proprietary claim; no peer-reviewed study confirms |
| Value-vs-Effort matrix originator | UNVERIFIABLE — no traceable primary source |
