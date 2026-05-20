from __future__ import annotations

from pathlib import Path

import pytest

from fathomx.utils.slug import sanitize_slug
from fathomx.workspace import Workspace


def test_create_dirs(tmp_workspace: Workspace) -> None:
    assert (tmp_workspace.dir / "search").is_dir()
    assert (tmp_workspace.dir / "analysis").is_dir()
    assert (tmp_workspace.dir / "compressed").is_dir()


def test_write_read(tmp_workspace: Workspace) -> None:
    tmp_workspace.write("search/result.md", "content")

    assert tmp_workspace.read("search/result.md") == "content"


def test_path_traversal(tmp_workspace: Workspace) -> None:
    with pytest.raises(ValueError):
        tmp_workspace.write("../outside.md", "nope")


def test_state_management(tmp_workspace: Workspace) -> None:
    state = {"topic": "Test Topic", "currentPhase": 2}

    tmp_workspace.save_state(state)
    loaded = tmp_workspace.load_state()

    assert loaded["topic"] == "Test Topic"
    assert loaded["currentPhase"] == 2
    assert "updatedAt" in loaded


def test_error_log(tmp_workspace: Workspace) -> None:
    tmp_workspace.log_error("task", "failed")

    content = (tmp_workspace.dir / "errors.log").read_text(encoding="utf-8")
    assert "[task] failed" in content


def test_slug_sanitization() -> None:
    values = {
        "Simple Topic": "simple-topic",
        "../Unsafe Path": "unsafe-path",
        "Symbols! @#$": "symbols",
        "": "untitled",
    }

    for raw, expected in values.items():
        slug = sanitize_slug(raw)
        assert slug == expected
        assert "/" not in slug
        assert "\\" not in slug
        assert slug == slug.lower()


def test_workspace_uses_slug(tmp_path: Path) -> None:
    workspace = Workspace(tmp_path, "../Unsafe Path")

    assert workspace.dir.name.endswith("-unsafe-path")
