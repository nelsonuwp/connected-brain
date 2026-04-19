"""
Rich-based progress display for long-running sync operations.

Usage:
    async with SyncProgress("Backfill") as p:
        scout_task = p.add_task("Scouting ticket keys", total=None)   # indeterminate
        # ... do scout work ...
        p.update(scout_task, total=count, completed=count)

        process_task = p.add_task("Processing tickets", total=len(keys))
        for batch in batches:
            # ...
            p.advance(process_task, len(batch))
"""

from __future__ import annotations

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def install_rich_logging(level: str = "INFO") -> Console:
    """
    Replace basicConfig with a Rich handler. Call ONCE early in main().
    Returns the shared Console so the Progress can render on it.
    """
    console = Console(stderr=False)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                show_time=True,
                show_level=True,
                show_path=False,
                markup=False,
                rich_tracebacks=True,
            )
        ],
        force=True,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    return console


class SyncProgress:
    """Thin wrapper around rich.progress.Progress with sensible defaults for sync work."""

    def __init__(self, title: str, console: Optional[Console] = None) -> None:
        self.title = title
        self.console = console or Console()
        self._progress: Optional[Progress] = None

    def __enter__(self) -> SyncProgress:
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("•"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
            refresh_per_second=4,
        )
        self._progress.__enter__()
        self.console.rule(f"[bold]{self.title}")
        return self

    def __exit__(self, *exc: object) -> None:
        assert self._progress is not None
        self._progress.__exit__(*exc)
        self._progress = None

    def add_task(self, description: str, total: Optional[int] = None) -> TaskID:
        assert self._progress is not None
        return self._progress.add_task(description, total=total)

    def advance(self, task_id: TaskID, n: int = 1) -> None:
        assert self._progress is not None
        self._progress.advance(task_id, n)

    def update(self, task_id: TaskID, **kwargs: object) -> None:
        assert self._progress is not None
        self._progress.update(task_id, **kwargs)

    def stop_task(self, task_id: TaskID) -> None:
        assert self._progress is not None
        self._progress.update(task_id, visible=True)
