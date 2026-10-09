from ctis.models import AssetClass, Bar, Side
from ctis.strategies import generate


def _bars(asset: AssetClass, closes, **extra):
    rows = []
    for i, close in enumerate(closes):
        rows.append(
            Bar(
                ts=f"2026-01-{i+1:02d}",
                symbol="X",
                asset_class=asset,
                open=close,
                high=close + 0.2,
                low=close - 0.2,
                close=close,
                volume=extra.get("volume", 2_000_000),
                funding_rate=extra.get("funding_rate", 0.0),
                benchmark_close=extra.get("benchmark", close),
                apy=extra.get("apy", 0.0),
                peg=extra.get("peg", 1.0),
            )
        )
    return rows


def test_large_cap_buys_confirmed_uptrend():
    signal = generate(_bars(AssetClass.LARGE_CAP, [float(100 + i) for i in range(25)]))
    assert signal.side is Side.BUY
    assert signal.target_weight == 0.25


def test_altcoin_rejects_thin_book():
    signal = generate(_bars(AssetClass.ALTCOIN, [10, 11, 12, 13, 14, 15], volume=10))
    assert signal.target_weight == 0.0
    assert "liquidity" in signal.reason


def test_stablecoin_depeg():
    signal = generate(_bars(AssetClass.STABLECOIN, [1, 1], peg=0.99))
    assert signal.side is Side.SELL
    assert signal.target_weight == 0.0


def test_perp_short_carry():
    signal = generate(_bars(AssetClass.PERPETUAL, [100, 101], funding_rate=0.0008))
    assert signal.side is Side.SELL
    assert signal.target_weight < 0


def test_yield_flags_extreme_apy():
    signal = generate(_bars(AssetClass.YIELD, [1, 1], apy=0.80))
    assert signal.target_weight == 0.0
    assert "ceiling" in signal.reason
