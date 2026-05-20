"""FAST tier task: extract structured data from raw search results."""

from __future__ import annotations

import argparse
import sys

from ..client import ModelClient, ModelClientError, run_sync
from ..config import load_config
from ..workspace import Workspace

SYSTEM_PROMPT = """You are a research data extraction specialist. Your job is to extract structured, factual information from raw search results.

Given raw search results about a specific research dimension, extract:
1. Key entities (companies, products, people, organizations)
2. Factual claims with numbers (market sizes, growth rates, dates, prices)
3. Direct quotes that provide unique insight
4. Source URLs for each extracted item

Output format: Markdown with clear sections. Every fact must reference its source.

Rules:
- Extract ONLY what is in the source material. Do NOT add your own knowledge.
- If a claim appears in multiple sources, note all sources.
- If sources conflict, note the conflict explicitly.
- Discard irrelevant or low-signal content.
- Preserve exact numbers, dates, and proper nouns.
"""


async def _run(workspace: Workspace, dimension: str, context: str, input_path: str | None) -> None:
    config = load_config()
    raw_content = None

    if input_path:
        raw_content = workspace.read(input_path)
    if raw_content is None:
        raw_content = workspace.read(f"search/raw-{dimension}.md")
    if raw_content is None:
        workspace.log_error("search_extract", f"No input found for dimension: {dimension}")
        sys.exit(1)

    if len(raw_content.strip()) < 50:
        workspace.log_error("search_extract", f"Input too short for dimension: {dimension}")
        workspace.write(f"search/{dimension}.md", f"# {dimension}\n\nNo meaningful content found.\n")
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research dimension: {dimension}\nContext: {context}\n\n---\n\nRaw search results:\n\n{raw_content}"},
    ]

    async with ModelClient(config) as client:
        try:
            result = await client.complete("FAST", messages, max_tokens=8192)
            workspace.write(f"search/{dimension}.md", f"# {dimension}\n\n{result}\n")
        except ModelClientError as e:
            workspace.log_error("search_extract", str(e))
            sys.exit(1)


def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Extract structured data from search results")
    parser.add_argument("--workspace", required=True, help="Workspace directory path")
    parser.add_argument("--dimension", required=True, help="Research dimension name")
    parser.add_argument("--context", default="", help="Brief research context")
    parser.add_argument("--input", default=None, help="Input file subpath (default: search/raw-{dimension}.md)")
    parsed = parser.parse_args(args)

    ws = Workspace(".", "", session_dir=parsed.workspace)
    run_sync(_run(ws, parsed.dimension, parsed.context, parsed.input))
