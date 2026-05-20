"""CLI entry point: python3 -m deep_research <command>."""

from __future__ import annotations

import sys


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("Usage: python3 -m deep_research <command>")
        print()
        print("Commands:")
        print("  setup          Interactive TUI configuration")
        print("  config check   Check config status (JSON output)")
        print("  run <task>     Run an orchestrator task")
        print()
        print("Tasks:")
        print("  search_extract   Extract structured data from search results (FAST)")
        print("  analyze          Run persona analysis on findings (SMART)")
        print("  compress         Compress findings for synthesis (FAST)")
        print("  gemini_search    Gemini Search grounded query (SEARCH)")
        sys.exit(0)

    cmd = args[0]

    if cmd == "setup":
        from .tui.app import run_setup
        run_setup()

    elif cmd == "config" and len(args) > 1 and args[1] == "check":
        from .config import print_check
        print_check()

    elif cmd == "run" and len(args) > 1:
        task_name = args[1]
        task_args = args[2:]
        _run_task(task_name, task_args)

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


def _run_task(task_name: str, task_args: list[str]) -> None:
    if task_name == "search_extract":
        from .tasks.search_extract import main as task_main
    elif task_name == "analyze":
        from .tasks.analyze import main as task_main
    elif task_name == "compress":
        from .tasks.compress import main as task_main
    elif task_name == "gemini_search":
        from .tasks.gemini_search import main as task_main
    else:
        print(f"Unknown task: {task_name}", file=sys.stderr)
        sys.exit(1)

    task_main(task_args)


if __name__ == "__main__":
    main()
