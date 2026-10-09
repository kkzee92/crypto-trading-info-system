from ctis.models import AccountState, AssetClass, Side, Signal
from ctis.risk import evaluate
from ctis.security.policy import Policy


def _signal(weight: float = 0.25, asset=AssetClass.LARGE_CAP) -> Signal:
    return Signal("BTC", asset, Side.BUY, weight, 0.6, "test", "large_cap_trend")


def test_class_cap_clips_weight():
    decision = evaluate(_signal(0.5), AccountState(100, 100), Policy("paper", frozenset({"read"})))
    assert decision.adjusted_weight == 0.30
    assert any("class cap" in reason for reason in decision.reasons)


def test_kill_switch_blocks():
    decision = evaluate(_signal(), AccountState(100, 100), Policy("paper", frozenset({"paper_trade"})), kill_switch=True)
    assert decision.accepted is False
    assert decision.adjusted_weight == 0.0


def test_day_loss_halts():
    account = AccountState(100, 100, day_pnl_pct=-0.04)
    decision = evaluate(_signal(), account, Policy("paper", frozenset({"read"})))
    assert decision.accepted is False
