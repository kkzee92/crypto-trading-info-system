"""Perpetual information sleeve: funding-rate carry, hard leverage cap, no liquidation chasing."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal

NAME = "perp_funding_carry"
MAX_WEIGHT = 0.10  # 0.10 of equity at 1x; engine refuses leverage above policy
EXTREME = 0.003


def generate(bars: list[Bar]) -> Signal:
    last = bars[-1]
    funding = last.funding_rate
    if abs(funding) >= EXTREME:
        return Signal(
            last.symbol,
            AssetClass.PERPETUAL,
            Side.REDUCE,
            0.0,
            0.9,
            f"funding extreme {funding:.5f}; stand aside",
            NAME,
        )
    # Positive funding: longs pay shorts. Paper sleeve leans short.
    if funding >= 0.0004:
        return Signal(
            last.symbol,
            AssetClass.PERPETUAL,
            Side.SELL,
            -MAX_WEIGHT,
            0.62,
            f"funding {funding:.5f} favours short carry",
            NAME,
        )
    if funding <= -0.0004:
        return Signal(
            last.symbol,
            AssetClass.PERPETUAL,
            Side.BUY,
            MAX_WEIGHT,
            0.62,
            f"funding {funding:.5f} favours long carry",
            NAME,
        )
    return Signal(last.symbol, AssetClass.PERPETUAL, Side.HOLD, 0.0, 0.35, "funding inside no-trade band", NAME)
