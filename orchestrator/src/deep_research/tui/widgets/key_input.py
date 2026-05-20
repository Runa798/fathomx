"""Masked API key input widget."""

from __future__ import annotations

from textual.widgets import Input


class KeyInput(Input):
    """Input that keeps the API key value while showing a compact mask on blur."""

    def __init__(self, *, value: str = "", placeholder: str = "API key", id: str | None = None):
        super().__init__(value=value, placeholder=placeholder, password=True, id=id)
        self._secret_value = value
        self._showing_mask = False

    @property
    def secret_value(self) -> str:
        if self._showing_mask:
            return self._secret_value
        return self.value

    @secret_value.setter
    def secret_value(self, value: str) -> None:
        self._secret_value = value
        self.value = value
        self._showing_mask = False

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input is self and not self._showing_mask:
            self._secret_value = event.value

    def on_focus(self) -> None:
        if self._showing_mask:
            self.value = self._secret_value
            self.password = True
            self._showing_mask = False

    def on_blur(self) -> None:
        self._secret_value = self.secret_value
        if self._secret_value:
            self.password = False
            self._showing_mask = True
            self.value = self._masked_value(self._secret_value)

    def _masked_value(self, value: str) -> str:
        if value.startswith("sk-"):
            return "sk-****"
        if len(value) <= 4:
            return "****"
        return f"{value[:4]}****"
