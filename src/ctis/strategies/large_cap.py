"""Large-cap spot: trend with a volatility gate and RSI filter. Sized for BTC/ETH sleeves."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal
from ctis.strategies.base import atr, rsi, sma

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
    rsi_val = rsi(closes, 14)
    if fast is None or slow is None or rsi_val is None:
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
    # Enhanced: require RSI in 40-70 range for buy (avoid extremes)
    if last.close > fast > slow and 40 <= rsi_val <= 70:
        return Signal(
            last.symbol,
            AssetClass.LARGE_CAP,
            Side.BUY,
            MAX_WEIGHT,
            0.75,
            f"close above fast SMA, fast above slow, RSI={rsi_val:.1f} in range",
            NAME,
        )
    if last.close < fast or rsi_val > 75:
        return Signal(
            last.symbol,
            AssetClass.LARGE_CAP,
            Side.REDUCE,
            0.05,
            0.65,
            f"close below fast SMA or RSI={rsi_val:.1f} overbought",
            NAME,
        )
    return Signal(last.symbol, AssetClass.LARGE_CAP, Side.HOLD, 0.10, 0.4, "trend not confirmed or RSI out of range", NAME)
