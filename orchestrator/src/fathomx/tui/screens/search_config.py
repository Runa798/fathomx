"""Search provider configuration screen."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static

from ..widgets.key_input import KeyInput

if TYPE_CHECKING:
    from ..app import SetupApp


class SearchConfigScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(classes="page"):
            yield Label("Search providers", classes="title")
            yield Static("Configure Grok Search, Tavily, and Exa credentials.", classes="subtitle")
            with Vertical(classes="section"):
                yield Label("Grok Search")
                yield Input(placeholder="Grok API URL", id="grok-api-url")
                yield KeyInput(id="grok-api-key", placeholder="Grok API key")
                yield Input(value="https://api.tavily.com", placeholder="Tavily API URL", id="tavily-api-url")
                yield KeyInput(id="tavily-api-key", placeholder="Tavily API key")
            with Vertical(classes="section"):
                yield Label("Exa")
                yield KeyInput(id="exa-api-key", placeholder="Exa API key")
            with Horizontal(classes="actions"):
                if Path(".env").exists():
                    yield Button("Pre-fill from .env?", id="prefill-env")
                yield Button("Back", id="back")
                yield Button("Next", variant="primary", id="next")

    def on_mount(self) -> None:
        app = cast("SetupApp", self.app)
        search = app.config_data.get("search", {})
        grok = search.get("grok", {})
        exa = search.get("exa", {})
        self.query_one("#grok-api-url", Input).value = grok.get("api_url", "")
        self.query_one("#grok-api-key", KeyInput).secret_value = grok.get("api_key", "")
        self.query_one("#tavily-api-url", Input).value = grok.get("tavily_api_url", "https://api.tavily.com")
        self.query_one("#tavily-api-key", KeyInput).secret_value = grok.get("tavily_api_key", "")
        self.query_one("#exa-api-key", KeyInput).secret_value = exa.get("api_key", "")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast("SetupApp", self.app)
        button_id = event.button.id
        if button_id == "prefill-env":
            self._prefill_from_env()
            return
        if button_id == "back":
            app.pop_screen()
            return
        if button_id == "next":
            self._write_config_data(app.config_data)
            app.push_screen("validate")

    def _prefill_from_env(self) -> None:
        values = self._read_env(Path(".env"))
        self.query_one("#grok-api-url", Input).value = values.get("GROK_API_URL", "")
        self.query_one("#grok-api-key", KeyInput).secret_value = values.get("GROK_API_KEY", "")
        self.query_one("#tavily-api-url", Input).value = values.get("TAVILY_API_URL", "https://api.tavily.com")
        self.query_one("#tavily-api-key", KeyInput).secret_value = values.get("TAVILY_API_KEY", "")
        self.query_one("#exa-api-key", KeyInput).secret_value = values.get("EXA_API_KEY", "")

    def _read_env(self, path: Path) -> dict[str, str]:
        values: dict[str, str] = {}
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
        return values

    def _write_config_data(self, config_data: dict[str, Any]) -> None:
        search = config_data.setdefault("search", {})
        search["grok"] = {
            "api_url": self.query_one("#grok-api-url", Input).value.strip(),
            "api_key": self.query_one("#grok-api-key", KeyInput).secret_value.strip(),
            "tavily_api_url": self.query_one("#tavily-api-url", Input).value.strip() or "https://api.tavily.com",
            "tavily_api_key": self.query_one("#tavily-api-key", KeyInput).secret_value.strip(),
        }
        search["exa"] = {
            "api_key": self.query_one("#exa-api-key", KeyInput).secret_value.strip(),
        }
