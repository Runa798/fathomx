"""Welcome screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Static

if TYPE_CHECKING:
    from ..app import SetupApp


class WelcomeScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(classes="page"):
            yield Label("Claude Deep Research v1.2.0 Setup", classes="title")
            yield Static(
                "Configure external models and search providers for enhanced research",
                classes="subtitle",
            )
            with Horizontal(classes="actions"):
                yield Button("Continue", variant="primary", id="continue")
                yield Button("Skip (use defaults)", id="skip")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app = cast("SetupApp", self.app)
        if event.button.id == "continue":
            app.push_screen("model_config")
            return
        if event.button.id == "skip":
            app.reset_to_defaults()
            app.save()
            app.exit()
