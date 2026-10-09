"""Runtime security policy. Live trading and withdrawals are denied by default."""

from __future__ import annotations

import os
from dataclasses import dataclass


FORBIDDEN_SCOPES = frozenset({"withdraw", "transfer", "internal_transfer"})
ALLOWED_SCOPES = frozenset({"read", "paper_trade"})


@dataclass(frozen=True)
class Policy:
    mode: str
    scopes: frozenset[str]
    max_gross_exposure: float = 0.80
    max_class_weight: dict[str, float] | None = None
    max_day_loss_pct: float = 0.03
    max_leverage: float = 1.0

    def __post_init__(self) -> None:
        if self.mode not in {"paper", "live"}:
            raise ValueError("mode must be paper or live")
        illegal = self.scopes & FORBIDDEN_SCOPES
        if illegal:
            raise ValueError(f"forbidden scopes requested: {sorted(illegal)}")
        unknown = self.scopes - ALLOWED_SCOPES
        if unknown:
            raise ValueError(f"unknown scopes: {sorted(unknown)}")
        if self.mode == "live" and os.environ.get("CTIS_ALLOW_LIVE") != "1":
            raise ValueError("live mode refused: set CTIS_ALLOW_LIVE=1 only after a human change review")
        if self.mode == "live":
            raise ValueError("live order routing is not implemented in this build")


def load_policy() -> Policy:
    mode = os.environ.get("CTIS_MODE", "paper")
    raw = os.environ.get("CTIS_SCOPES", "read,paper_trade")
    scopes = frozenset(part.strip() for part in raw.split(",") if part.strip())
    return Policy(mode=mode, scopes=scopes)


def class_cap(policy: Policy, asset_class: str) -> float:
    defaults = {
        "large_cap": 0.30,
        "altcoin": 0.10,
        "stablecoin": 0.40,
        "perpetual": 0.10,
        "yield": 0.05,
    }
    overrides = policy.max_class_weight or {}
    return overrides.get(asset_class, defaults[asset_class])
