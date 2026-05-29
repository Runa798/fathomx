#!/usr/bin/env python3
"""Build MCP JSONL for a single aspect_research smoke test (strategist persona)."""
import json, pathlib, sys

ROOT = pathlib.Path("/home/heye/projects/claude-deep-research")
persona = (ROOT / "skills/pm-deep-research/prompts/layer2/persona-strategist.md").read_text(encoding="utf-8")
assert persona.strip(), "persona prompt empty"
assert len(persona.encode("utf-8")) < 64 * 1024, "persona prompt >= 64 KiB"

aspect_request = {
    "schema_version": "0.1",
    "request_id": "m4-smoke-positioning-001",
    "task": {
        "aspect": {
            "aspect_id": "positioning-whitespace",
            "name": "Positioning & whitespace — AI running coaching",
            "role": "product strategist",
            "research_question": (
                "On buyer-validated axes, how are Strava, Runna, Garmin (Coach / Daily Suggested Workouts) and "
                "Nike Run Club positioned for AI-assisted running coaching, and where is the whitespace?"
            ),
            "scope": [
                "AI/adaptive running-coaching capability and how each is positioned to buyers",
                "buyer-validated purchase axes (e.g. adaptivity, social/community, hardware integration, price)",
                "value curve per player and the unoccupied whitespace + why",
                "sustaining vs disruptive threat grading (Christensen)",
            ],
            "boundaries": [
                "running/endurance coaching only; exclude strength-only or nutrition-only apps",
                "no first-party survey data is available — estimate from public evidence and tag TM-4",
            ],
            "success_criteria": [
                "axes are buyer-validated purchase dimensions, not invented",
                "a value curve per named player with at least one cited evidence item each",
                "at least one whitespace with a stated reason why it is unoccupied",
                "each major conclusion carries a TM-4 epistemic tag and a TM-11 falsification condition",
            ],
            "aspect_agent_prompt": persona,
            "allowed_tools": ["search"],
            "model_provider": "openai",
            "search_provider": "grok",
        },
        "budget": {"max_turns": 6, "max_tool_calls": 6, "max_search_calls": 2, "timeout_ms": 600000},
    },
    "shared_context": {
        "summary": (
            "decision_intent=ai_upgrade. Target product: a running app considering an AI-coaching upgrade. "
            "This aspect covers dimension 5 (positioning & whitespace) of the competitive spine."
        ),
        "known_facts": [],
        "excluded_assumptions": [],
        "prior_sources": [],
    },
    "model_policy": {
        "allowed_providers": ["openai"],
        "temperature": 0.2,
        "max_tokens": None,
        "require_tool_call_support": True,
    },
    "search_policy": {
        "allowed_providers": ["grok"],
        "max_results_per_query": 3,
        "freshness": None,
        "language": None,
        "region": None,
        "include_domains": [],
        "exclude_domains": [],
    },
    "evidence_policy": {"require_evidence_for_findings": True, "min_evidence_per_finding": 1},
    "output_policy": {"language": "zh", "max_findings_per_aspect": 5},
    "execution_policy": {"allow_partial_results": True, "fail_fast": False, "timeout_ms": 600000},
}

args_out = ROOT / ".m4-run/aspect-smoke.args.json"
with args_out.open("w", encoding="utf-8") as f:
    json.dump(aspect_request, f, ensure_ascii=False)
print(f"wrote {args_out} ({args_out.stat().st_size} bytes); persona {len(persona.encode('utf-8'))} bytes")
