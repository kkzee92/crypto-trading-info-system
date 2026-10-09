"""Altcoin spot: relative strength versus the BTC benchmark, with a liquidity floor."""

from __future__ import annotations

from ctis.models import AssetClass, Bar, Side, Signal
from ctis.strategies.base import return_over

NAME = "altcoin_relative_strength"
MAX_WEIGHT = 0.08
MIN_VOLUME = 1_000_000.0


def generate(bars: list[Bar]) -> Signal:
    last = bars[-1]
    if last.volume < MIN_VOLUME:
        return Signal(
            last.symbol,
            AssetClass.ALTCOIN,
            Side.REDUCE,
            0.0,
            0.8,
            f"liquidity floor: volume {last.volume:.0f} < {MIN_VOLUME:.0f}",
            NAME,
        )
    asset_ret = return_over([b.close for b in bars], 5)
    bench_ret = return_over([b.benchmark_close for b in bars], 5)
    if asset_ret is None or bench_ret is None or last.benchmark_close <= 0:
        return Signal(last.symbol, AssetClass.ALTCOIN, Side.HOLD, 0.0, 0.2, "no benchmark history", NAME)
    excess = asset_ret - bench_ret
    if excess > 0.03 and asset_ret > 0:
        return Signal(
            last.symbol,
            AssetClass.ALTCOIN,
            Side.BUY,
            MAX_WEIGHT,
            min(0.85, 0.5 + excess),
            f"excess return vs BTC {excess:.3f}",
            NAME,
        )
    if excess < -0.03:
        return Signal(
            last.symbol,
            AssetClass.ALTCOIN,
            Side.SELL,
            0.0,
            0.7,
            f"underperforming BTC by {excess:.3f}",
            NAME,
        )
    return Signal(last.symbol, AssetClass.ALTCOIN, Side.HOLD, 0.0, 0.4, "no relative-strength edge", NAME)
