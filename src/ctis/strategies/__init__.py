"""Strategy router by asset class."""

from __future__ import annotations

from collections.abc import Callable

from ctis.models import AssetClass, Bar, Signal
from ctis.strategies import altcoin, large_cap, perpetual, stablecoin, yield_info

Generator = Callable[[list[Bar]], Signal]

REGISTRY: dict[AssetClass, Generator] = {
    AssetClass.LARGE_CAP: large_cap.generate,
    AssetClass.ALTCOIN: altcoin.generate,
    AssetClass.STABLECOIN: stablecoin.generate,
    AssetClass.PERPETUAL: perpetual.generate,
    AssetClass.YIELD: yield_info.generate,
}


def generate(bars: list[Bar]) -> Signal:
    if not bars:
        raise ValueError("empty tape")
    asset_class = bars[-1].asset_class
    if asset_class not in REGISTRY:
        raise ValueError(f"no strategy for {asset_class}")
    return REGISTRY[asset_class](bars)
