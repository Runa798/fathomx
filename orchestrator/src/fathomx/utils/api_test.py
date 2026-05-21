"""API key validation helpers for TUI onboarding."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class ValidationResult:
    provider: str
    ok: bool
    message: str
    latency_ms: int = 0


def _sanitize_error(text: str) -> str:
    """Remove potential API keys and tokens from error messages."""
    return re.sub(r'(sk-|xai-|tvly-|AIza)[A-Za-z0-9_-]{10,}', '***', str(text)[:200])


async def validate_openai_compat(provider: str, base_url: str, api_key: str, model: str) -> ValidationResult:
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": 5,
        "temperature": 0,
    }
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 401:
                return ValidationResult(provider, False, "Invalid API key (401)")
            if resp.status_code == 403:
                return ValidationResult(provider, False, "Access denied (403)")
            resp.raise_for_status()
            data = resp.json()
            if data.get("choices"):
                return ValidationResult(provider, True, "OK", latency_ms=int(resp.elapsed.total_seconds() * 1000))
            return ValidationResult(provider, False, "Unexpected response format")
    except httpx.TimeoutException:
        return ValidationResult(provider, False, "Timeout (>15s)")
    except httpx.RequestError as e:
        return ValidationResult(provider, False, f"Connection error: {e}")
    except Exception as e:
        return ValidationResult(provider, False, _sanitize_error(str(e)))


async def validate_gemini(api_key: str, model: str = "gemini-3.1-pro") -> ValidationResult:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {"contents": [{"parts": [{"text": "Say OK"}]}]}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload, params={"key": api_key})
            if resp.status_code == 400 and "API_KEY_INVALID" in resp.text:
                return ValidationResult("google", False, "Invalid API key")
            resp.raise_for_status()
            data = resp.json()
            if data.get("candidates"):
                return ValidationResult("google", True, "OK", latency_ms=int(resp.elapsed.total_seconds() * 1000))
            return ValidationResult("google", False, "Unexpected response format")
    except httpx.TimeoutException:
        return ValidationResult("google", False, "Timeout (>15s)")
    except httpx.RequestError as e:
        return ValidationResult("google", False, f"Connection error: {e}")
    except Exception as e:
        return ValidationResult("google", False, _sanitize_error(str(e)))


async def validate_exa(api_key: str) -> ValidationResult:
    url = "https://api.exa.ai/search"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {"query": "test", "numResults": 1, "useAutoprompt": False}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 401:
                return ValidationResult("exa", False, "Invalid API key (401)")
            resp.raise_for_status()
            return ValidationResult("exa", True, "OK", latency_ms=int(resp.elapsed.total_seconds() * 1000))
    except httpx.TimeoutException:
        return ValidationResult("exa", False, "Timeout (>15s)")
    except httpx.RequestError as e:
        return ValidationResult("exa", False, f"Connection error: {e}")
    except Exception as e:
        return ValidationResult("exa", False, _sanitize_error(str(e)))


async def validate_all(config_dict: dict[str, Any]) -> list[ValidationResult]:
    tasks = []
    models = config_dict.get("models", {})

    for tier in ("FAST", "SMART"):
        spec = models.get(tier, {})
        if spec.get("api_key"):
            tasks.append(validate_openai_compat(
                f"{tier} ({spec.get('provider', 'unknown')})",
                spec.get("base_url", ""),
                spec["api_key"],
                spec.get("model", ""),
            ))

    search_spec = models.get("SEARCH", {})
    if search_spec.get("api_key"):
        tasks.append(validate_gemini(search_spec["api_key"], search_spec.get("model", "gemini-3.1-pro")))

    search_cfg = config_dict.get("search", {})
    grok = search_cfg.get("grok", {})
    if grok.get("api_key") and grok.get("api_url"):
        tasks.append(validate_openai_compat("Grok Search", grok["api_url"], grok["api_key"], "grok-3"))

    exa = search_cfg.get("exa", {})
    if exa.get("api_key"):
        tasks.append(validate_exa(exa["api_key"]))

    if not tasks:
        return [ValidationResult("none", True, "No keys configured")]

    return await asyncio.gather(*tasks)
