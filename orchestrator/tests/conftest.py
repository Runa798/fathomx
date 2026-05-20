from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from deep_research.config import save_config  # noqa: E402
from deep_research.config_schema import Config, ModelSpec  # noqa: E402
from deep_research.workspace import Workspace  # noqa: E402


@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.json"
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
    save_config(config, config_path)
    return config_path


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Workspace:
    return Workspace(tmp_path, "Test Topic")
