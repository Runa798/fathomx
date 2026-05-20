"""Unified model client for OpenAI-compatible APIs."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .config import load_config
from .config_schema import Config, ModelSpec


class ModelClientError(Exception):
    def __init__(self, tier: str, message: str):
        self.tier = tier
        super().__init__(f"[{tier}] {message}")


class ModelClient:
    """Calls external model APIs. All providers use OpenAI-compatible chat completions."""

    def __init__(self, config: Config | None = None):
        self._config = config or load_config()
        self._http = httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0))

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> ModelClient:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    def _get_spec(self, tier: str) -> ModelSpec:
        spec = self._config.get_model(tier)
        if spec is None:
            raise ModelClientError(tier, f"Tier {tier} is not configured or disabled")
        return spec

    async def complete(
        self,
        tier: str,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        spec = self._get_spec(tier)
        url = f"{spec.base_url}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {spec.api_key}", "Content-Type": "application/json"}

        payload: dict[str, Any] = {
            "model": spec.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else spec.temperature,
            "max_tokens": max_tokens if max_tokens is not None else spec.max_tokens,
        }
        if response_format:
            payload["response_format"] = response_format

        return await self._request_with_retry(tier, url, headers, payload)

    async def _request_with_retry(
        self,
        tier: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
        max_retries: int = 3,
    ) -> str:
        last_error: Exception | None = None
        for attempt in range(max_retries):
            try:
                resp = await self._http.post(url, json=payload, headers=headers)
                if resp.status_code == 429:
                    retry_after = float(resp.headers.get("retry-after", 2 ** (attempt + 1)))
                    await asyncio.sleep(min(retry_after, 30))
                    continue
                resp.raise_for_status()
                try:
                    data = resp.json()
                except ValueError as exc:
                    raise ModelClientError(tier, "Non-JSON response from API") from exc
                choices = data.get("choices", [])
                if not choices:
                    raise ModelClientError(tier, "Empty choices in response")
                content = choices[0].get("message", {}).get("content")
                if content is None:
                    raise ModelClientError(tier, "No content in response message")
                return content
            except httpx.HTTPStatusError as e:
                last_error = ModelClientError(tier, f"HTTP {e.response.status_code}: {e.response.text[:500]}")
                if e.response.status_code >= 500:
                    await asyncio.sleep(2 ** (attempt + 1))
                    continue
                raise last_error from e
            except httpx.TimeoutException:
                last_error = ModelClientError(tier, f"Request timed out (attempt {attempt + 1})")
                await asyncio.sleep(2 ** attempt)
                continue
            except httpx.RequestError as e:
                last_error = ModelClientError(tier, f"Connection error: {e}")
                await asyncio.sleep(2 ** attempt)
                continue

        raise last_error or ModelClientError(tier, "Max retries exceeded")


def run_sync(coro: Any) -> Any:
    """Run an async coroutine synchronously (for CLI task entry points)."""
    return asyncio.run(coro)
