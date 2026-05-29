#!/usr/bin/env python3
"""Rebuild single aspect_research requests for the 2 aspects that failed in the
partial 4/6 deep_research run, using the corrected persona prompts.

- capability-and-importance  -> experience-analyst persona (supports_findings invariant fix)
- positioning-whitespace     -> strategist persona (was transient provider_unavailable)
"""
import json, pathlib

ROOT = pathlib.Path("/home/heye/projects/claude-deep-research")
L2 = ROOT / "skills/pm-deep-research/prompts/layer2"
analyst = (L2 / "persona-experience-analyst.md").read_text(encoding="utf-8")
strategist = (L2 / "persona-strategist.md").read_text(encoding="utf-8")
for nm, p in (("analyst", analyst), ("strategist", strategist)):
    assert p.strip(), f"{nm} persona empty"
    assert len(p.encode("utf-8")) < 64 * 1024, f"{nm} persona >= 64 KiB"

SHARED = {
    "summary": (
        "decision_intent=ai_upgrade. Target product: a running/fitness app (anchor: Strava) "
        "weighing an AI running-coaching upgrade. Competitive set anchors: Strava, Runna, "
        "Garmin (Coach / Daily Suggested Workouts), Nike Run Club, adidas Running. No first-party "
        "survey data — estimate from public evidence and tag epistemic status (TM-4)."
    ),
    "known_facts": [],
    "excluded_assumptions": [],
    "prior_sources": [],
}
MODEL_POLICY = {"allowed_providers": ["openai"], "temperature": 0.2, "max_tokens": None, "require_tool_call_support": True}
SEARCH_POLICY = {"allowed_providers": ["grok"], "max_results_per_query": 3, "freshness": None,
                 "language": None, "region": None, "include_domains": [], "exclude_domains": []}
EVIDENCE_POLICY = {"require_evidence_for_findings": True, "min_evidence_per_finding": 1}
OUTPUT_POLICY = {"language": "zh", "max_findings_per_aspect": 6}
EXEC_POLICY = {"allow_partial_results": True, "fail_fast": False, "timeout_ms": 600000}
BUDGET = {"max_turns": 6, "max_tool_calls": 6, "max_search_calls": 2, "timeout_ms": 600000}


def req(request_id, aspect):
    return {
        "schema_version": "0.1",
        "request_id": request_id,
        "task": {"aspect": aspect, "budget": BUDGET},
        "shared_context": SHARED,
        "model_policy": MODEL_POLICY,
        "search_policy": SEARCH_POLICY,
        "evidence_policy": EVIDENCE_POLICY,
        "output_policy": OUTPUT_POLICY,
        "execution_policy": EXEC_POLICY,
    }


capability = req("m4-rerun-capability-001", {
    "aspect_id": "capability-and-importance",
    "name": "Capability matrix & Kano importance",
    "role": "product experience analyst",
    "research_question": "How do the named players compare on AI-coaching capabilities, and which capabilities are Must-be / Performance / Attractive (Kano)?",
    "scope": [
        "cross-competitor capability matrix on AI/adaptive coaching features, scored with inline per-cell evidence",
        "Kano grade per key feature grounded in user evidence or tagged practitioner interpretation",
    ],
    "boundaries": ["compare named players only", "every matrix cell needs evidence or is marked assumption"],
    "success_criteria": [
        "a capability matrix where each cell has an inline evidence id or is marked assumption",
        "Kano grades rest on user evidence or are tagged TM-4 interpretation",
    ],
    "aspect_agent_prompt": analyst,
    "allowed_tools": ["search"],
    "model_provider": "openai",
    "search_provider": "grok",
})

positioning = req("m4-rerun-positioning-001", {
    "aspect_id": "positioning-whitespace",
    "name": "Positioning & whitespace",
    "role": "product strategist",
    "research_question": "On buyer-validated axes, what is each player's value curve for AI coaching, where is the whitespace, and which threats are sustaining vs disruptive?",
    "scope": [
        "buyer-validated positioning axes (adaptivity, community, hardware integration, price)",
        "value curve per player + whitespace with a 'why unoccupied' reason",
        "sustaining vs disruptive threat grading",
    ],
    "boundaries": ["axes must be buyer-validated, not invented"],
    "success_criteria": [
        "a value curve per named player with cited evidence",
        "at least one whitespace with a stated reason it is unoccupied",
        "per-competitor sustaining/disruptive threat call",
    ],
    "aspect_agent_prompt": strategist,
    "allowed_tools": ["search"],
    "model_provider": "openai",
    "search_provider": "grok",
})

for name, obj in (("aspect-capability", capability), ("aspect-positioning", positioning)):
    out = ROOT / f".m4-run/{name}.args.json"
    out.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
print(f"analyst persona {len(analyst.encode('utf-8'))} bytes; strategist persona {len(strategist.encode('utf-8'))} bytes")
