#!/usr/bin/env python3
"""Build the deep_research arguments for the golden topic (Strava AI-coaching upgrade).

6 aspects = Deep 5-dim spine + build-cost-version-history, personas assigned per
agent-allocation.md. Providers fixed to live config: search=grok, model=openai.
"""
import json, pathlib

ROOT = pathlib.Path("/home/heye/projects/claude-deep-research")
L2 = ROOT / "skills/pm-deep-research/prompts/layer2"
STRAT = (L2 / "persona-strategist.md").read_text(encoding="utf-8")
EXP = (L2 / "persona-experience-analyst.md").read_text(encoding="utf-8")
for name, p in [("strategist", STRAT), ("experience", EXP)]:
    assert p.strip() and len(p.encode("utf-8")) < 64 * 1024, f"{name} prompt bad size"

DECISION = ("decision_intent=ai_upgrade. Target product: a running/fitness app (anchor: Strava) "
            "weighing an AI running-coaching upgrade. Competitive set anchors: Strava, Runna, "
            "Garmin (Coach / Daily Suggested Workouts), Nike Run Club, adidas Running. "
            "No first-party survey data — estimate from public evidence and tag epistemic status (TM-4).")

# Per-aspect budget bounded to stay under Lapis hardcoded MAX_SSE_EVENTS=4096:
# verbatim evidence copying + long synthesis blows the SSE cap (M4 finding).
# 2 searches x 3 results ~= <=6 evidence/aspect; 6 aspects ~= ~36 sources (>= Deep floor 25+).
BUDGET = {"max_turns": 6, "max_tool_calls": 6, "max_search_calls": 2, "timeout_ms": 600000}


def aspect(aid, name, role, persona, question, scope, boundaries, success):
    return {
        "aspect": {
            "aspect_id": aid, "name": name, "role": role,
            "research_question": question, "scope": scope, "boundaries": boundaries,
            "success_criteria": success, "aspect_agent_prompt": persona,
            "allowed_tools": ["search"], "model_provider": "openai", "search_provider": "grok",
        },
        "budget": dict(BUDGET),
    }


aspects = [
    aspect("job-and-competitive-set", "Job & real competitive set", "product strategist", STRAT,
           "What job do runners hire a running app for, and by that job who is the real competitive set "
           "(including non-obvious substitutes) for AI running coaching?",
           ["JTBD job statement (situation->motivation->outcome) for runners seeking coaching",
            "real competitive set by job, including non-obvious substitutes (human coaches, generic LLMs, watch-native coaching)"],
           ["running/endurance coaching only", "no first-party surveys; tag estimates TM-4"],
           ["an explicit job statement", "at least one non-obvious substitute with a stated inclusion reason",
            "each major claim carries a TM-4 tag and a TM-11 falsification condition"]),
    aspect("capability-and-importance", "Capability matrix & Kano importance", "product experience analyst", EXP,
           "How do the named players compare on AI-coaching capabilities, and which capabilities are "
           "Must-be / Performance / Attractive (Kano)?",
           ["cross-competitor capability matrix on AI/adaptive coaching features, scored with inline per-cell evidence",
            "Kano grade per key feature grounded in user evidence or tagged practitioner interpretation"],
           ["compare named players only", "every matrix cell needs evidence or is marked assumption"],
           ["a capability matrix where each cell has an inline evidence id or is marked assumption",
            "Kano grades rest on user evidence or are tagged TM-4 interpretation"]),
    aspect("opportunity-gaps", "Competitive gaps (ODI)", "product strategist", STRAT,
           "For the key desired outcomes of AI running coaching, what are Importance and Satisfaction, "
           "and the ODI opportunity ranking?",
           ["desired outcomes for AI coaching with Importance/Satisfaction (1-10) and computed Opportunity",
            "rank underserved (>10) vs overserved (<7) outcomes"],
           ["no first-party surveys; mark Importance/Satisfaction estimated + TM-4"],
           ["an ODI table with Importance, Satisfaction, computed Opportunity, and an estimated flag per outcome",
            "estimates carry TM-4 tags"]),
    aspect("positioning-whitespace", "Positioning & whitespace", "product strategist", STRAT,
           "On buyer-validated axes, what is each player's value curve for AI coaching, where is the "
           "whitespace, and which threats are sustaining vs disruptive?",
           ["buyer-validated positioning axes (adaptivity, community, hardware integration, price)",
            "value curve per player + whitespace with a 'why unoccupied' reason", "sustaining vs disruptive threat grading"],
           ["axes must be buyer-validated, not invented"],
           ["a value curve per named player with cited evidence", "at least one whitespace with a stated reason it is unoccupied",
            "per-competitor sustaining/disruptive threat call"]),
    aspect("experience-paths", "Experience paths & breakpoints", "product experience analyst", EXP,
           "On the core running-coaching paths (onboarding/plan-setup, daily workout, feedback/adaptation, "
           "retention), where are the experience breakpoints, backed by visual evidence?",
           ["core path walkthrough with breakpoints", "visual evidence (screenshot/video/app-store page URLs) per UI claim"],
           ["UI/experience claims need a visual-evidence item or go to open_questions"],
           ["each UI conclusion is backed by a visual-evidence item or its gap is logged in open_questions",
            "visual metadata recorded in the citing Finding.claim, not in Evidence.summary"]),
    aspect("build-cost-version-history", "Iteration velocity & build-cost", "product strategist", STRAT,
           "How fast and on what have competitors shipped AI-coaching capability (changelog/version history), "
           "and what does that imply about build-cost for an AI running-coaching upgrade?",
           ["competitor release-notes / App Store version-history timeline for AI/adaptive coaching",
            "inferred investment priority (revealed strategy, TM-12) + build-cost estimate for the target capability"],
           ["evidence url must point at version-history/release-notes pages",
            "if no reliable timeline, mark it an assumption rather than guessing cadence"],
           ["a datable version timeline for at least one competitor with evidence url = version history",
            "a build-cost estimate tied to iteration cadence, tagged TM-4"]),
]

request = {
    "schema_version": "0.1",
    "request_id": "m4-golden-strava-ai-upgrade-001",
    "user_question": "Should a running app (anchor: Strava) upgrade to AI-assisted running coaching, "
                     "and how should it differentiate against Runna / Garmin / Nike Run Club?",
    "aspect_tasks": aspects,
    "budget": {
        "max_agents": 6, "max_concurrent_agents": 3, "max_total_model_calls": 70,
        "max_total_search_calls": 56, "total_timeout_ms": 1260000, "max_tokens": None,
    },
    "model_policy": {"allowed_providers": ["openai"], "temperature": 0.2, "max_tokens": None,
                     "require_tool_call_support": True},
    "search_policy": {"allowed_providers": ["grok"], "max_results_per_query": 3, "freshness": None,
                      "language": None, "region": None, "include_domains": [], "exclude_domains": []},
    "evidence_policy": {"require_evidence_for_findings": True, "min_evidence_per_finding": 1},
    "output_policy": {"language": "zh", "max_findings_per_aspect": 6},
    "shared_context": {"summary": DECISION, "known_facts": [], "excluded_assumptions": [], "prior_sources": []},
    # execution_policy.timeout_ms must be <= the PER-ASPECT budget.timeout_ms (600000):
    # deep_research re-validates each aspect as an AspectResearchRequest where the
    # ceiling is the aspect budget, not total_timeout_ms. Setting it to total (1260000)
    # made every aspect fail budget_exceeded ("execution timeout must not exceed agent
    # budget timeout"). 600000 satisfies both that and execution<=total.
    "execution_policy": {"allow_partial_results": True, "fail_fast": False, "timeout_ms": 600000},
}

out = ROOT / ".m4-run/deep-golden.args.json"
with out.open("w", encoding="utf-8") as f:
    json.dump(request, f, ensure_ascii=False)
print(f"wrote {out} ({out.stat().st_size} bytes); aspects={len(aspects)} "
      f"strat={len(STRAT.encode('utf-8'))}B exp={len(EXP.encode('utf-8'))}B")
