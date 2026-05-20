"""Configuration schema — Pydantic v2 models for ~/.deep-research/config.json."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelSpec(BaseModel):
    provider: str = Field(description="Provider name: deepseek, openai, google, custom")
    model: str = Field(description="Model identifier sent in API requests")
    base_url: str = Field(default="", description="API base URL (without /v1/chat/completions)")
    api_key: str = Field(default="", description="API key (Bearer token)")
    max_tokens: int = Field(default=8192, ge=256, le=131072)
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    enabled: bool = Field(default=True)


class GrokSearch(BaseModel):
    api_url: str = Field(default="")
    api_key: str = Field(default="")
    tavily_api_url: str = Field(default="https://api.tavily.com")
    tavily_api_key: str = Field(default="")


class ExaSearch(BaseModel):
    api_key: str = Field(default="")


class SearchConfig(BaseModel):
    grok: GrokSearch = Field(default_factory=GrokSearch)
    exa: ExaSearch = Field(default_factory=ExaSearch)


class Features(BaseModel):
    multi_model: bool = Field(default=False, description="Use external models for extraction/analysis")
    scope_expansion: bool = Field(default=True, description="Apply MECE 6-dimension scope expansion")
    gemini_search: bool = Field(default=False, description="Use Gemini Search grounding as supplementary source")


class WorkspaceConfig(BaseModel):
    base_dir: str = Field(default="workspace")


class Config(BaseModel):
    version: str = Field(default="1.2.0")
    models: dict[str, ModelSpec] = Field(default_factory=dict, description="Keyed by tier: FAST, SMART, SEARCH")
    search: SearchConfig = Field(default_factory=SearchConfig)
    features: Features = Field(default_factory=Features)
    workspace: WorkspaceConfig = Field(default_factory=WorkspaceConfig)

    def get_model(self, tier: str) -> ModelSpec | None:
        spec = self.models.get(tier)
        if spec is None or not spec.enabled or not spec.api_key:
            return None
        return spec

    def is_tier_available(self, tier: str) -> bool:
        return self.get_model(tier) is not None

    def available_tiers(self) -> list[str]:
        return [t for t in ("FAST", "SMART", "SEARCH") if self.is_tier_available(t)]


PROVIDER_DEFAULTS: dict[str, dict[str, str]] = {
    "deepseek": {"base_url": "https://api.deepseek.com", "model": "deepseek-chat"},
    "openai": {"base_url": "https://api.openai.com", "model": "gpt-5.5"},
    "google": {"base_url": "https://generativelanguage.googleapis.com", "model": "gemini-3.1-pro"},
}
