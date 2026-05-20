"""FAST tier task: compress all findings into a synthesis-ready summary."""

from __future__ import annotations

import argparse
import sys

from ..client import ModelClient, ModelClientError, run_sync
from ..config import load_config
from ..workspace import Workspace

SYSTEM_PROMPT = """You are a research compression specialist. Your job is to distill extensive research findings into a concise, synthesis-ready summary.

Compression rules:
1. PRESERVE: causal chains, contradictions between sources, cross-source connections, exact numbers, source citations
2. REDUCE: redundant corroboration (note "confirmed by N sources" instead of repeating), verbose explanations
3. REMOVE: irrelevant tangents, filler text, low-confidence claims with no corroboration
4. Target: approximately 55% of the input length (never compress below 35%)

Output structure:
1. **Key Facts** — numbered list, each with source citation
2. **Contradictions** — where sources disagree, present both sides
3. **Cross-Cutting Themes** — patterns that span multiple dimensions/personas
4. **Information Gaps** — what remains unknown or poorly sourced
5. **Strategic Signals** — high-confidence insights that should anchor the final report

Write for an expert reader who will use this to produce the final research report."""


async def _run(workspace: Workspace, context: str) -> None:
    config = load_config()

    sections: list[str] = []
    for subdir in ("search", "analysis"):
        for f in workspace.list_files(subdir):
            if f.suffix == ".md" and not f.name.startswith("raw-"):
                content = f.read_text(encoding="utf-8")
                if len(content.strip()) > 50:
                    sections.append(f"## Source: {subdir}/{f.name}\n\n{content}")

    if not sections:
        workspace.log_error("compress", "No files found to compress")
        sys.exit(1)

    combined = "\n\n---\n\n".join(sections)

    max_input_chars = 400_000
    if len(combined) > max_input_chars:
        workspace.log_error("compress", f"Input too large ({len(combined)} chars), truncating to {max_input_chars}")
        combined = combined[:max_input_chars]

    input_tokens_approx = len(combined) // 4

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research context: {context}\nInput size: ~{input_tokens_approx} tokens\n\n---\n\n{combined}"},
    ]

    async with ModelClient(config) as client:
        try:
            result = await client.complete("FAST", messages, max_tokens=16384)
            workspace.write("compressed/findings-summary.md", f"# Compressed Research Findings\n\n{result}\n")
        except ModelClientError as e:
            workspace.log_error("compress", str(e))
            sys.exit(1)


def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Compress findings for synthesis")
    parser.add_argument("--workspace", required=True, help="Workspace directory path")
    parser.add_argument("--context", default="", help="Brief research context")
    parsed = parser.parse_args(args)

    ws = Workspace(".", "", session_dir=parsed.workspace)
    run_sync(_run(ws, parsed.context))
