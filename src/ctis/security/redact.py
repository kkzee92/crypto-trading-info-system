"""Redact secrets before they reach logs, briefs or the audit trail."""

from __future__ import annotations

import re

_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+-----END [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|pk)_[A-Za-z0-9]{16,}\b"),
)


def redact(text: str) -> str:
    cleaned = text
    for pattern in _PATTERNS:
        cleaned = pattern.sub("[REDACTED]", cleaned)
    return cleaned
