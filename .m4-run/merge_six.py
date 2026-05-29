#!/usr/bin/env python3
"""Merge the 2 rerun aspect_research results into the partial 4/6 deep_research
result to form a complete 6/6 DeepResearchResult for report assembly.

deep_research prefixes evidence ids + evidence_refs + supports_findings with
"<aspect_id>:"; standalone aspect_research does not. So we prefix the rerun
aspects to match, then append to aspect_reports + evidence_index.
"""
import json, pathlib

ROOT = pathlib.Path("/home/heye/projects/claude-deep-research")
M4 = ROOT / ".m4-run"

deep = json.load(open(M4 / "deep-golden.result.json", encoding="utf-8"))
data = deep["result"]["structuredContent"]["data"]

reruns = {
    "capability-and-importance": json.load(open(M4 / "aspect-capability.result.json", encoding="utf-8")),
    "positioning-whitespace": json.load(open(M4 / "aspect-positioning.result.json", encoding="utf-8")),
}


def prefix(aspect_id, rr):
    d = rr["result"]["structuredContent"]["data"]
    ar = d["aspect_report"]
    ev = d["evidence"]
    pfx = aspect_id + ":"

    def p(x):
        return x if x.startswith(pfx) else pfx + x

    for f in ar["findings"]:
        f["evidence_refs"] = [p(r) for r in f.get("evidence_refs", [])]
        f["contradicted_by"] = [p(r) for r in f.get("contradicted_by", [])]
    for e in ev:
        e["supports_findings"] = [p(s) for s in e.get("supports_findings", [])]
        e["id"] = p(e["id"])
    return ar, ev


for aid, rr in reruns.items():
    ar, ev = prefix(aid, rr)
    data["aspect_reports"].append(ar)
    data["evidence_index"].extend(ev)
    if aid not in data["completed_aspects"]:
        data["completed_aspects"].append(aid)

# resolved: clear failures (kept in m4-findings.md as history)
data["failed_aspects"] = []

# refresh summaries
data["coverage_summary"] = {
    "requested_aspects": 6,
    "completed_aspects": len(data["completed_aspects"]),
    "failed_aspects": 0,
    "note": "6/6 — capability + positioning recovered via single-aspect rerun with corrected personas (see m4-findings.md)",
}
confs = [a.get("confidence") for a in data["aspect_reports"]]
data["confidence_summary"] = {
    "per_aspect": {a["aspect_id"]: a.get("confidence") for a in data["aspect_reports"]},
    "overall": "medium",
    "basis": f"{confs.count('high')} high / {confs.count('medium')} medium / {confs.count('low')} low across 6 aspects",
}

out = M4 / "deep-golden-6of6.result.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# integrity re-check across the merged evidence_index
ev_ids = {e["id"] for e in data["evidence_index"]}
problems = 0
ref_map = {}
for ar in data["aspect_reports"]:
    for f in ar["findings"]:
        for r in f.get("evidence_refs", []):
            ref_map.setdefault(r, set())
            if r not in ev_ids:
                print("DANGLING evidence_ref:", r, "in", ar["aspect_id"], f["id"]); problems += 1
print(f"wrote {out} ({out.stat().st_size} bytes)")
print(f"aspect_reports={len(data['aspect_reports'])} evidence_index={len(data['evidence_index'])} dangling={problems}")
print("completed:", data["completed_aspects"])
