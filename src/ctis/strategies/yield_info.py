"""Yield information sleeve. Scores an allow-listed venue. Does not sign transactions."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal

NAME = "yield_info_allowlist"
MAX_WEIGHT = 0.05
APY_FLOOR = 0.03
APY_CEILING = 0.20  # very high advertised APY is treated as a risk flag, not an opportunity


def generate(bars: list[Bar]) -> Signal:
    last = bars[-1]
    if last.apy >= APY_CEILING:
        return Signal(
            last.symbol,
            AssetClass.YIELD,
            Side.REDUCE,
            0.0,
            0.85,
            f"APY {last.apy:.2%} above ceiling; treat as risk flag",
            NAME,
        )
    if last.apy >= APY_FLOOR:
        return Signal(
            last.symbol,
            AssetClass.YIELD,
            Side.HOLD,
            MAX_WEIGHT,
            0.55,
            f"informational allocation; APY {last.apy:.2%} inside band. No wallet signing.",
            NAME,
        )
    return Signal(
        last.symbol,
        AssetClass.YIELD,
        Side.HOLD,
        0.0,
        0.5,
        f"APY {last.apy:.2%} below floor",
        NAME,
    )
