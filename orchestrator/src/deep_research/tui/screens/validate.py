"""API validation screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView, Static

from ...utils.api_test import validate_all

if TYPE_CHECKING:
    from ..app import SetupApp


class ValidateScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(classes="page"):
            yield Label("Validate API keys", classes="title")
            yield Static("Configured keys", classes="subtitle")
            yield ListView(id="configured-keys")
            yield ListView(id="validation-results")
            with Horizontal(classes="actions"):
                yield Button("Back", id="back")
                yield Button("Validate All", variant="primary", id="validate-all")
                yield Button("Next", id="next", disabled=True)

    def on_mount(self) -> None:
        self._show_configured_keys()

    def _show_configured_keys(self) -> None:
        key_list = self.query_one("#configured-keys", ListView)
        key_list.clear()
        app = cast("SetupApp", self.app)
        models = app.config_data.get("models", {})
        for tier in ("FAST", "SMART", "SEARCH"):
            if models.get(tier, {}).get("api_key"):
                key_list.append(ListItem(Label(tier)))
        search = app.config_data.get("search", {})
        grok = search.get("grok", {})
        if grok.get("api_key"):
            key_list.append(ListItem(Label("Grok Search")))
        if grok.get("tavily_api_key"):
            key_list.append(ListItem(Label("Tavily")))
        if search.get("exa", {}).get("api_key"):
            key_list.append(ListItem(Label("Exa")))
        if not key_list.children:
            key_list.append(ListItem(Label("No API keys configured")))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast("SetupApp", self.app)
        button_id = event.button.id
        if button_id == "back":
            app.pop_screen()
            return
        if button_id == "next":
            app.push_screen("summary")
            return
        if button_id == "validate-all":
            await self._validate_all()

    async def _validate_all(self) -> None:
        app = cast("SetupApp", self.app)
        results_list = self.query_one("#validation-results", ListView)
        results_list.clear()
        results_list.append(ListItem(Label("Validating...")))
        self.query_one("#validate-all", Button).disabled = True
        results = await validate_all(app.config_data)
        results_list.clear()
        for result in results:
            if result.ok:
                text = f"✓ {result.provider}: OK ({result.latency_ms}ms)"
            else:
                text = f"✗ {result.provider}: Failed: {result.message}"
            results_list.append(ListItem(Label(text)))
        self.query_one("#next", Button).disabled = False
        self.query_one("#validate-all", Button).disabled = False
