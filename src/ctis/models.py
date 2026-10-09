"""Domain objects. Weights are fractions of paper equity, not exchange quantities."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AssetClass(str, Enum):
    LARGE_CAP = "large_cap"
    ALTCOIN = "altcoin"
    STABLECOIN = "stablecoin"
    PERPETUAL = "perpetual"
    YIELD = "yield"


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    REDUCE = "reduce"


@dataclass(frozen=True)
class Bar:
    ts: str
    symbol: str
    asset_class: AssetClass
    open: float
    high: float
    low: float
    close: float
    volume: float
    funding_rate: float = 0.0
    benchmark_close: float = 0.0
    apy: float = 0.0
    peg: float = 1.0

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError(f"{self.symbol} {self.ts}: high < low")
        if self.close <= 0 or self.volume < 0:
            raise ValueError(f"{self.symbol} {self.ts}: non-positive close or negative volume")


@dataclass(frozen=True)
class Signal:
    symbol: str
    asset_class: AssetClass
    side: Side
    target_weight: float
    confidence: float
    reason: str
    strategy: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if abs(self.target_weight) > 1.0:
            raise ValueError("target_weight must be in [-1, 1]")


@dataclass(frozen=True)
class RiskDecision:
    accepted: bool
    symbol: str
    strategy: str
    adjusted_weight: float
    reasons: tuple[str, ...]


@dataclass
class AccountState:
    equity: float
    cash: float
    positions: dict[str, float] = field(default_factory=dict)
    day_pnl_pct: float = 0.0
    mode: str = "paper"

    def gross_exposure(self) -> float:
        return sum(abs(w) for w in self.positions.values())
