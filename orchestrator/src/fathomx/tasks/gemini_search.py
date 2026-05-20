"""SEARCH tier task: Gemini Search grounded query."""

from __future__ import annotations

import argparse
import sys

import httpx

from ..client import run_sync
from ..config import load_config
from ..workspace import Workspace

GEMINI_GENERATE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


async def _run(workspace: Workspace, query: str, output: str) -> None:
    config = load_config()
    spec = config.get_model("SEARCH")
    if spec is None:
        workspace.log_error("gemini_search", "SEARCH tier not configured")
        sys.exit(1)

    model = spec.model or "gemini-3.1-pro"
    url = GEMINI_GENERATE_URL.format(model=model)

    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "tools": [
            {
                "google_search_retrieval": {
                    "dynamic_retrieval_config": {
                        "mode": "MODE_DYNAMIC",
                        "dynamic_threshold": 0.3,
                    }
                }
            }
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, params={"key": spec.api_key})
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        sanitized = e.response.text[:500].replace(spec.api_key, "***")
        workspace.log_error("gemini_search", f"HTTP {e.response.status_code}: {sanitized}")
        sys.exit(1)
    except httpx.RequestError as e:
        sanitized = str(e).replace(spec.api_key, "***")
        workspace.log_error("gemini_search", f"Connection error: {sanitized}")
        sys.exit(1)

    result_text = _extract_text(data)
    sources = _extract_sources(data)
    md = _format_markdown(query, result_text, sources)
    workspace.write(output, md)


def _extract_text(data: dict) -> str:
    try:
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        return "\n".join(p.get("text", "") for p in parts if "text" in p)
    except (KeyError, IndexError):
        return ""


def _extract_sources(data: dict) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    try:
        metadata = data.get("candidates", [{}])[0].get("groundingMetadata", {})
        chunks = metadata.get("groundingChunks", [])
        for chunk in chunks:
            web = chunk.get("web", {})
            if web.get("uri"):
                sources.append({"title": web.get("title", ""), "url": web["uri"]})
    except (KeyError, IndexError):
        pass
    return sources


def _format_markdown(query: str, text: str, sources: list[dict[str, str]]) -> str:
    lines = [f"# Gemini Search: {query}\n", text, "\n## Sources\n"]
    for i, src in enumerate(sources, 1):
        lines.append(f"- [{i}] [{src['title']}]({src['url']})")
    return "\n".join(lines) + "\n"


def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Gemini Search grounded query")
    parser.add_argument("--workspace", required=True, help="Workspace directory path")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--output", required=True, help="Output file subpath in workspace")
    parsed = parser.parse_args(args)

    ws = Workspace(".", "", session_dir=parsed.workspace)
    run_sync(_run(ws, parsed.query, parsed.output))
