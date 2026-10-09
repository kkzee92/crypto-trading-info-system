from pathlib import Path

from ctis.engine import run
from ctis.market import load_bars
from ctis.models import AccountState
from ctis.security.policy import Policy

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "bars.csv"


def test_brief_covers_each_asset_class():
    bars = load_bars(FIXTURE)
    brief = run(bars, AccountState(100_000, 100_000), Policy("paper", frozenset({"read", "paper_trade"})))
    classes = {signal.asset_class.value for signal in brief.signals}
    assert classes == {"large_cap", "altcoin", "stablecoin", "perpetual", "yield"}
    assert brief.posture == "paper"
    assert any("depeg" in signal.reason for signal in brief.signals)


def test_kill_switch_halts_brief():
    bars = load_bars(FIXTURE)
    brief = run(
        bars,
        AccountState(100_000, 100_000),
        Policy("paper", frozenset({"read"})),
        kill_switch=True,
    )
    assert brief.posture == "halted"
    assert all(decision.adjusted_weight == 0.0 for decision in brief.decisions)
