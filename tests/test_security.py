import os

import pytest

from ctis.security.audit import AuditLog
from ctis.security.killswitch import engage, release, tripped
from ctis.security.policy import Policy
from ctis.security.redact import redact


def test_redact_secret_assignment():
    assert "supersecret" not in redact("api_key=supersecret")
    assert "[REDACTED]" in redact("api_key=supersecret")


def test_audit_chain(tmp_path):
    log = AuditLog(tmp_path / "audit.jsonl")
    log.append("one", {"symbol": "BTC"})
    log.append("two", {"api_key": "should-not-survive"})
    assert log.verify()
    text = (tmp_path / "audit.jsonl").read_text()
    assert "should-not-survive" not in text


def test_kill_switch_file(tmp_path):
    path = tmp_path / "KILL"
    assert tripped(path) is False
    engage(path, "manual halt")
    assert tripped(path) is True
    release(path)
    assert tripped(path) is False


def test_withdraw_scope_rejected():
    with pytest.raises(ValueError, match="forbidden"):
        Policy("paper", frozenset({"withdraw"}))


def test_live_mode_refused(monkeypatch):
    monkeypatch.delenv("CTIS_ALLOW_LIVE", raising=False)
    with pytest.raises(ValueError, match="live mode refused"):
        Policy("live", frozenset({"read"}))
    monkeypatch.setenv("CTIS_ALLOW_LIVE", "1")
    with pytest.raises(ValueError, match="not implemented"):
        Policy("live", frozenset({"read"}))
    os.environ.pop("CTIS_ALLOW_LIVE", None)
