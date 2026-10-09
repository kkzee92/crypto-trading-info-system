"""File-based kill switch. Presence of the file halts new risk acceptance."""

from __future__ import annotations

from pathlib import Path


def tripped(path: str | Path) -> bool:
    return Path(path).exists()


def engage(path: str | Path, reason: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(reason.strip() + "\n", encoding="utf-8")


def release(path: str | Path) -> None:
    target = Path(path)
    if target.exists():
        target.unlink()
