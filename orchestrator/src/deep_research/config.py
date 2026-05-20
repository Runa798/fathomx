"""Configuration loading and management."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .config_schema import Config

CONFIG_DIR = Path.home() / ".deep-research"
CONFIG_PATH = CONFIG_DIR / "config.json"


class ConfigError(Exception):
    pass


def load_config(path: Path | None = None) -> Config:
    target = path or CONFIG_PATH
    if not target.exists():
        return Config()
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
        return Config.model_validate(raw)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {target}: {e}") from e
    except Exception as e:
        raise ConfigError(f"Config validation error: {e}") from e


def save_config(config: Config, path: Path | None = None) -> Path:
    target = path or CONFIG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    import os
    os.chmod(target.parent, 0o700)
    data = config.model_dump(mode="json")
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    target.write_text(content, encoding="utf-8")
    os.chmod(target, 0o600)
    return target


def check_config() -> dict[str, object]:
    """Return a status dict for `python3 -m deep_research config check`."""
    try:
        config = load_config()
    except ConfigError as e:
        return {"ok": False, "error": str(e)}

    tiers = config.available_tiers()
    return {
        "ok": True,
        "config_path": str(CONFIG_PATH),
        "config_exists": CONFIG_PATH.exists(),
        "available_tiers": tiers,
        "multi_model": config.features.multi_model and len(tiers) > 0,
        "scope_expansion": config.features.scope_expansion,
        "gemini_search": config.features.gemini_search and config.is_tier_available("SEARCH"),
    }


def print_check() -> None:
    status = check_config()
    json.dump(status, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.exit(0 if status["ok"] else 1)
