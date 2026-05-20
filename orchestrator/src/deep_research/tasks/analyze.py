"""SMART tier task: run persona-based analysis on research findings."""

from __future__ import annotations

import argparse
import sys

from ..client import ModelClient, ModelClientError, run_sync
from ..config import load_config
from ..workspace import Workspace

PERSONA_PROMPTS: dict[str, str] = {
    "market-analyst": """You are a Senior Market Analyst specializing in market sizing, industry dynamics, and growth forecasting.

Analytical frameworks you apply:
- TAM/SAM/SOM estimation with bottom-up and top-down cross-validation
- Market growth drivers and inhibitors analysis
- Industry lifecycle stage assessment
- Regulatory and macroeconomic impact evaluation

Your output must include:
1. Market size estimates with methodology notes
2. Growth trajectory with supporting evidence
3. Key trends and inflection points
4. Risk factors and market uncertainties

Every claim must cite the source material. Flag low-confidence estimates explicitly.""",

    "ci-analyst": """You are a Competitive Intelligence Analyst specializing in competitive positioning, strategic moves, and market dynamics.

Analytical frameworks you apply:
- Porter's Five Forces (rivalry, new entrants, substitutes, supplier power, buyer power)
- Competitive feature matrix (scored 0-3: absent/basic/competitive/best-in-class)
- Strategic group mapping
- Moat analysis (network effects, switching costs, data advantages, brand, regulatory)

Your output must include:
1. Competitor identification across 4 tiers (direct, indirect, substitutes, potential entrants)
2. Feature comparison matrix with buyer-importance weighting
3. Competitive positioning map (2x2 on most relevant dimensions)
4. Strategic moat assessment per major player

Every claim must cite the source material. Note information gaps explicitly.""",

    "product-strategist": """You are a Product Strategist specializing in product-market fit, user needs analysis, and strategic recommendations.

Analytical frameworks you apply:
- Jobs-to-be-Done (job map, outcome expectations, opportunity scoring)
- Blue Ocean ERRC Grid (Eliminate, Reduce, Raise, Create)
- Opportunity Solution Tree (outcomes → opportunities → solutions → experiments)
- Switching trigger analysis (what causes users to leave/adopt)

Your output must include:
1. Core jobs and supporting jobs identification
2. Opportunity scores: importance + (importance - satisfaction) for key outcomes
3. ERRC Grid with specific recommendations
4. Prioritized strategic recommendations with evidence basis
5. Suggested validation experiments

Every recommendation must trace back to evidence in the source material. Distinguish between evidence-backed insights and inferences.""",
}


async def _run(workspace: Workspace, persona: str, context: str) -> None:
    if persona not in PERSONA_PROMPTS:
        workspace.log_error("analyze", f"Unknown persona: {persona}. Valid: {list(PERSONA_PROMPTS.keys())}")
        sys.exit(1)

    config = load_config()
    search_files = workspace.list_files("search")
    contents: list[str] = []
    for f in search_files:
        if f.suffix == ".md" and not f.name.startswith("raw-"):
            contents.append(f.read_text(encoding="utf-8"))

    if not contents:
        workspace.log_error("analyze", f"No extracted search files found for persona: {persona}")
        sys.exit(1)

    combined = "\n\n---\n\n".join(contents)

    messages = [
        {"role": "system", "content": PERSONA_PROMPTS[persona]},
        {"role": "user", "content": f"Research context: {context}\n\n---\n\nExtracted research findings across all dimensions:\n\n{combined}"},
    ]

    async with ModelClient(config) as client:
        try:
            result = await client.complete("SMART", messages, max_tokens=16384)
            workspace.write(f"analysis/{persona}.md", f"# {persona.replace('-', ' ').title()} Analysis\n\n{result}\n")
        except ModelClientError as e:
            workspace.log_error("analyze", str(e))
            sys.exit(1)


def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Run persona-based analysis")
    parser.add_argument("--workspace", required=True, help="Workspace directory path")
    parser.add_argument("--persona", required=True, choices=list(PERSONA_PROMPTS.keys()), help="Research persona")
    parser.add_argument("--context", default="", help="Brief research context")
    parsed = parser.parse_args(args)

    ws = Workspace(".", "", session_dir=parsed.workspace)
    run_sync(_run(ws, parsed.persona, parsed.context))
