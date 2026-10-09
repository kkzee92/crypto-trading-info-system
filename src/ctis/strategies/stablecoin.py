"""Stablecoin sleeve: cash parking with a depeg circuit breaker. Not a yield chase."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal

NAME = "stablecoin_peg_guard"
CASH_WEIGHT = 0.20
DEPEG = 0.005


def generate(bars: list[Bar]) -> Signal:
    last = bars[-1]
    deviation = abs(last.peg - 1.0)
    if deviation >= DEPEG:
        return Signal(
            last.symbol,
            AssetClass.STABLECOIN,
            Side.SELL,
            0.0,
            0.95,
            f"depeg circuit breaker: peg {last.peg:.4f}",
            NAME,
        )
    return Signal(
        last.symbol,
        AssetClass.STABLECOIN,
        Side.HOLD,
        CASH_WEIGHT,
        0.9,
        f"peg inside band ({deviation:.4f} < {DEPEG})",
        NAME,
    )
