"""Append-only hash-chained audit log. Tamper-evident, not a legal ledger."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from ctis.security.redact import redact

_SENSITIVE_KEY = re.compile(r"(?i)api|secret|token|password|private")


def _scrub(value):
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            if _SENSITIVE_KEY.search(str(key)):
                cleaned[key] = "[REDACTED]"
            else:
                cleaned[key] = _scrub(item)
        return cleaned
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    if isinstance(value, str):
        return redact(value)
    return value


def _canon(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass
class AuditLog:
    path: Path
    prev_hash: str = "GENESIS"

    def append(self, event: str, payload: dict) -> str:
        safe = _scrub(payload)
        body = {"event": event, "payload": safe, "prev": self.prev_hash}
        digest = hashlib.sha256(_canon(body).encode()).hexdigest()
        record = {**body, "hash": digest}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        self.prev_hash = digest
        return digest

    def verify(self) -> bool:
        if not self.path.exists():
            return True
        prev = "GENESIS"
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            claimed = record.pop("hash")
            if record.get("prev") != prev:
                return False
            digest = hashlib.sha256(_canon(record).encode()).hexdigest()
            if digest != claimed:
                return False
            prev = claimed
        return True
