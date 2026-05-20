"""Model tier configuration screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Input, Label, Select, Static

from ...config_schema import PROVIDER_DEFAULTS
from ..widgets.key_input import KeyInput

if TYPE_CHECKING:
    from ..app import SetupApp


PROVIDER_OPTIONS = [("DeepSeek", "deepseek"), ("OpenAI", "openai"), ("Custom", "custom")]


class ModelConfigScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(classes="page"):
            yield Label("Model tiers", classes="title")
            yield Static("Configure external model access for orchestration.", classes="subtitle")
            for tier, description in (
                ("FAST", "Fast extraction and compression"),
                ("SMART", "Deep analysis and reasoning"),
            ):
                lower = tier.lower()
                defaults = PROVIDER_DEFAULTS["deepseek"]
                with Vertical(classes="section", id=f"{lower}-section"):
                    yield Label(f"{tier} tier")
                    yield Static(description, classes="subtitle")
                    yield Select(PROVIDER_OPTIONS, value="deepseek", id=f"{lower}-provider")
                    yield KeyInput(id=f"{lower}-api-key", placeholder=f"{tier} API key")
                    yield Input(value=defaults["base_url"], placeholder="Base URL", id=f"{lower}-base-url")
                    yield Input(value=defaults["model"], placeholder="Model name", id=f"{lower}-model")
                    with Horizontal(classes="actions"):
                        yield Button(f"Skip {tier}", id=f"skip-{lower}")
            with Vertical(classes="section", id="search-section"):
                yield Label("SEARCH tier")
                yield Checkbox("Enable Gemini Search", id="search-enabled")
                yield KeyInput(id="search-api-key", placeholder="Gemini API key")
                with Horizontal(classes="actions"):
                    yield Button("Skip SEARCH", id="skip-search")
            with Horizontal(classes="actions"):
                yield Button("Back", id="back")
                yield Button("Next", variant="primary", id="next")

    def on_mount(self) -> None:
        self._load_existing_values()

    def _load_existing_values(self) -> None:
        app = cast("SetupApp", self.app)
        models = app.config_data.get("models", {})
        for tier in ("FAST", "SMART"):
            lower = tier.lower()
            model = models.get(tier, {})
            provider = model.get("provider", "deepseek")
            if provider not in {"deepseek", "openai", "custom"}:
                provider = "custom"
            self.query_one(f"#{lower}-provider", Select).value = provider
            self.query_one(f"#{lower}-api-key", KeyInput).secret_value = model.get("api_key", "")
            self.query_one(f"#{lower}-base-url", Input).value = model.get(
                "base_url",
                PROVIDER_DEFAULTS["deepseek"]["base_url"],
            )
            self.query_one(f"#{lower}-model", Input).value = model.get("model", PROVIDER_DEFAULTS["deepseek"]["model"])

        search_model = models.get("SEARCH", {})
        self.query_one("#search-enabled", Checkbox).value = bool(search_model.get("api_key"))
        self.query_one("#search-api-key", KeyInput).secret_value = search_model.get("api_key", "")

    def on_select_changed(self, event: Select.Changed) -> None:
        select_id = event.select.id or ""
        if not select_id.endswith("-provider"):
            return
        provider = str(event.value)
        if provider not in PROVIDER_DEFAULTS:
            return
        prefix = select_id.removesuffix("-provider")
        defaults = PROVIDER_DEFAULTS[provider]
        self.query_one(f"#{prefix}-base-url", Input).value = defaults["base_url"]
        self.query_one(f"#{prefix}-model", Input).value = defaults["model"]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast("SetupApp", self.app)
        button_id = event.button.id
        if button_id == "back":
            app.pop_screen()
            return
        if button_id in {"skip-fast", "skip-smart", "skip-search"}:
            tier = button_id.removeprefix("skip-").upper()
            app.config_data.setdefault("models", {}).pop(tier, None)
            self._clear_tier(tier)
            return
        if button_id == "next":
            self._write_config_data(app.config_data)
            app.push_screen("search_config")

    def _clear_tier(self, tier: str) -> None:
        if tier in {"FAST", "SMART"}:
            lower = tier.lower()
            self.query_one(f"#{lower}-api-key", KeyInput).secret_value = ""
            return
        if tier == "SEARCH":
            self.query_one("#search-enabled", Checkbox).value = False
            self.query_one("#search-api-key", KeyInput).secret_value = ""

    def _write_config_data(self, config_data: dict[str, Any]) -> None:
        models = config_data.setdefault("models", {})
        for tier in ("FAST", "SMART"):
            lower = tier.lower()
            api_key = self.query_one(f"#{lower}-api-key", KeyInput).secret_value.strip()
            if not api_key:
                models.pop(tier, None)
                continue
            provider = str(self.query_one(f"#{lower}-provider", Select).value)
            models[tier] = {
                "provider": provider,
                "api_key": api_key,
                "base_url": self.query_one(f"#{lower}-base-url", Input).value.strip(),
                "model": self.query_one(f"#{lower}-model", Input).value.strip(),
                "enabled": True,
            }

        search_enabled = self.query_one("#search-enabled", Checkbox).value
        search_api_key = self.query_one("#search-api-key", KeyInput).secret_value.strip()
        if search_enabled and search_api_key:
            google_defaults = PROVIDER_DEFAULTS["google"]
            models["SEARCH"] = {
                "provider": "google",
                "api_key": search_api_key,
                "base_url": google_defaults["base_url"],
                "model": google_defaults["model"],
                "enabled": True,
            }
            config_data.setdefault("features", {})["gemini_search"] = True
        else:
            models.pop("SEARCH", None)
            config_data.setdefault("features", {})["gemini_search"] = False

        config_data.setdefault("features", {})["multi_model"] = bool(models.get("FAST") or models.get("SMART"))
