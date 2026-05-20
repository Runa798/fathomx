"""Setup summary screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from ...config_schema import Config

if TYPE_CHECKING:
    from ..app import SetupApp


class SummaryScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(classes="page"):
            yield Label("Summary", classes="title")
            yield Static("", id="summary")
            with Horizontal(classes="actions"):
                yield Button("Back", id="back")
                yield Button("Save & Exit", variant="primary", id="save-exit")

    def on_mount(self) -> None:
        self._refresh_summary()

    def on_show(self) -> None:
        self._refresh_summary()

    def _refresh_summary(self) -> None:
        app = cast("SetupApp", self.app)
        config = Config.model_validate(app.config_data)
        tiers = ", ".join(config.available_tiers()) or "none"
        features = [
            f"Multi-model: {'enabled' if config.features.multi_model else 'disabled'}",
            f"Scope expansion: {'enabled' if config.features.scope_expansion else 'disabled'}",
            f"Gemini Search: {'enabled' if config.features.gemini_search else 'disabled'}",
        ]
        providers = []
        if config.search.grok.api_key and config.search.grok.api_url:
            providers.append("Grok Search")
        if config.search.grok.tavily_api_key:
            providers.append("Tavily")
        if config.search.exa.api_key:
            providers.append("Exa")
        provider_summary = ", ".join(providers) or "none"
        summary = "\n".join(
            [
                f"Configured tiers: {tiers}",
                f"Search providers: {provider_summary}",
                *features,
            ],
        )
        self.query_one("#summary", Static).update(summary)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast("SetupApp", self.app)
        if event.button.id == "back":
            app.pop_screen()
            return
        if event.button.id == "save-exit":
            app.save()
            app.exit()
