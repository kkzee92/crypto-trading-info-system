"""Large-cap spot: trend with a volatility gate. Sized for BTC/ETH sleeves."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal
from ctis.strategies.base import atr, sma

NAME = "large_cap_trend"
MAX_WEIGHT = 0.25
VOL_CAP = 0.06


def generate(bars: list[Bar]) -> Signal:
    last = bars[-1]
    closes = [b.close for b in bars]
    fast = sma(closes, 10)
    slow = sma(closes, 20)
    vol = atr(bars, 10)
    vol_ratio = (vol / last.close) if vol else 1.0
    if fast is None or slow is None:
        return Signal(last.symbol, AssetClass.LARGE_CAP, Side.HOLD, 0.0, 0.2, "insufficient history", NAME)
    if vol_ratio > VOL_CAP:
        return Signal(
            last.symbol,
            AssetClass.LARGE_CAP,
            Side.REDUCE,
            0.05,
            0.7,
            f"volatility gate: ATR/close {vol_ratio:.3f} > {VOL_CAP}",
            NAME,
        )
    if last.close > fast > slow:
        return Signal(
            last.symbol,
            AssetClass.LARGE_CAP,
            Side.BUY,
            MAX_WEIGHT,
            0.66,
            "close above fast SMA and fast above slow SMA",
            NAME,
        )
    if last.close < fast:
        return Signal(
            last.symbol,
            AssetClass.LARGE_CAP,
            Side.REDUCE,
            0.05,
            0.6,
            "close below fast SMA",
            NAME,
        )
    return Signal(last.symbol, AssetClass.LARGE_CAP, Side.HOLD, 0.10, 0.4, "trend not confirmed", NAME)
