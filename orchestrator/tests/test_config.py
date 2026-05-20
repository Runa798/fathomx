from __future__ import annotations

from pathlib import Path

import pytest

from deep_research.config import ConfigError, load_config, save_config
from deep_research.config_schema import Config, ModelSpec


def test_default_config(tmp_path: Path) -> None:
    config = load_config(tmp_path / "missing.json")

    assert config.version == "1.2.0"
    assert config.models == {}
    assert config.features.scope_expansion is True


def test_save_and_load(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    config = Config(
        models={
            "FAST": ModelSpec(
                provider="deepseek",
                model="deepseek-chat",
                base_url="https://api.deepseek.com",
                api_key="fast-key",
            ),
        },
    )

    save_config(config, path)
    loaded = load_config(path)

    assert loaded == config


def test_partial_config(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        """
        {
          "models": {
            "FAST": {
              "provider": "openai",
              "model": "gpt-5.5",
              "base_url": "https://api.openai.com",
              "api_key": "fast-key"
            }
          }
        }
        """,
        encoding="utf-8",
    )

    config = load_config(path)

    assert config.get_model("FAST") is not None
    assert config.get_model("SMART") is None


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(path)


def test_available_tiers(tmp_config: Path) -> None:
    config = load_config(tmp_config)

    assert config.available_tiers() == ["FAST"]


def test_get_model_returns_none() -> None:
    config = Config()

    assert config.get_model("FAST") is None
