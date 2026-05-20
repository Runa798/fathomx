"""Textual app for interactive setup."""

from __future__ import annotations

from typing import Any

from textual.app import App

from ..config import save_config
from ..config_schema import Config
from .screens.model_config import ModelConfigScreen
from .screens.search_config import SearchConfigScreen
from .screens.summary import SummaryScreen
from .screens.validate import ValidateScreen
from .screens.welcome import WelcomeScreen


class SetupApp(App[None]):
    """Interactive onboarding app."""

    CSS = """
    Screen {
        align: center top;
    }

    .page {
        width: 92;
        max-width: 100%;
        padding: 1 2;
    }

    .title {
        text-style: bold;
        margin-bottom: 1;
    }

    .subtitle {
        color: $text-muted;
        margin-bottom: 1;
    }

    .section {
        border: solid $panel;
        padding: 1 2;
        margin: 1 0;
    }

    .row {
        height: auto;
        margin-bottom: 1;
    }

    .actions {
        height: auto;
        margin-top: 1;
    }

    Input, Select {
        margin-right: 1;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.config_data: dict[str, Any] = self._load_existing_or_default()

    def _load_existing_or_default(self) -> dict[str, Any]:
        from ..config import load_config
        try:
            existing = load_config()
            return existing.model_dump(mode="json")
        except Exception:
            return Config().model_dump(mode="json")

    def on_mount(self) -> None:
        self.install_screen(WelcomeScreen(), "welcome")
        self.install_screen(ModelConfigScreen(), "model_config")
        self.install_screen(SearchConfigScreen(), "search_config")
        self.install_screen(ValidateScreen(), "validate")
        self.install_screen(SummaryScreen(), "summary")
        self.push_screen("welcome")

    def default_config_data(self) -> dict[str, Any]:
        return Config().model_dump(mode="json")

    def reset_to_defaults(self) -> None:
        self.config_data = self.default_config_data()

    def save(self) -> None:
        save_config(Config.model_validate(self.config_data))


def run_setup() -> None:
    SetupApp().run()
