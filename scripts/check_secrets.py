#!/usr/bin/env python3
"""Tripwire for committed secrets. Not a substitute for gitleaks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "var", "__pycache__"}
PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|api[_-]?secret|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}['\"]"),
    re.compile(r"\b(?:sk|pk)_[A-Za-z0-9]{20,}\b"),
)


def main() -> int:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts):
            continue
        if path.suffix not in {".py", ".md", ".yml", ".toml", ".csv", ".txt", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PATTERNS:
            if pattern.search(text):
                hits.append(f"{path.relative_to(ROOT)} matches {pattern.pattern}")
    if hits:
        print("\n".join(hits))
        return 1
    print("secret tripwire: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
