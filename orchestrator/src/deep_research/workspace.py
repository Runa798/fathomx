"""Workspace directory management and file I/O."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from .utils.slug import sanitize_slug


class Workspace:
    """Manages a single research session's workspace directory."""

    def __init__(self, base_dir: str | Path, topic: str, *, session_dir: Path | None = None):
        if session_dir:
            self.dir = Path(session_dir)
        else:
            slug = sanitize_slug(topic)
            self.dir = Path(base_dir) / f"research-{date.today().isoformat()}-{slug}"

        self.dir.mkdir(parents=True, exist_ok=True)
        for sub in ("search", "analysis", "compressed"):
            (self.dir / sub).mkdir(exist_ok=True)

    def write(self, subpath: str, content: str) -> Path:
        target = self._safe_path(subpath)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def read(self, subpath: str) -> str | None:
        target = self._safe_path(subpath)
        if not target.exists():
            return None
        return target.read_text(encoding="utf-8")

    def exists(self, subpath: str) -> bool:
        return self._safe_path(subpath).exists()

    def list_files(self, subdir: str) -> list[Path]:
        target = self._safe_path(subdir)
        if not target.is_dir():
            return []
        return sorted(target.iterdir())

    def load_state(self) -> dict[str, object]:
        content = self.read("state.json")
        if content is None:
            return self._default_state()
        return json.loads(content)

    def save_state(self, state: dict[str, object]) -> None:
        state["updatedAt"] = datetime.now().isoformat()
        self.write("state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")

    def log_error(self, task: str, error: str) -> None:
        entry = f"[{datetime.now().isoformat()}] [{task}] {error}\n"
        errors_path = self.dir / "errors.log"
        with errors_path.open("a", encoding="utf-8") as f:
            f.write(entry)

    def _safe_path(self, subpath: str) -> Path:
        resolved = (self.dir / subpath).resolve()
        try:
            resolved.relative_to(self.dir.resolve())
        except ValueError:
            raise ValueError(f"Path traversal detected: {subpath}") from None
        return resolved

    def _default_state(self) -> dict[str, object]:
        return {
            "topic": "",
            "tier": "deep",
            "status": "in_progress",
            "currentPhase": 1,
            "startedAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "sourceCount": 0,
            "dimensions": {},
            "personas": {},
            "checkpoints": [],
        }
