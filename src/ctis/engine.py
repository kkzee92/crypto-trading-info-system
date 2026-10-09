"""Information engine: tape -> strategy -> risk -> paper brief. No exchange client."""

from __future__ import annotations

from dataclasses import dataclass

from ctis.market import group_by_symbol
from ctis.models import AccountState, Bar, RiskDecision, Signal
from ctis.risk import evaluate
from ctis.security.policy import Policy
from ctis.strategies import generate


@dataclass(frozen=True)
class Brief:
    as_of: str
    signals: tuple[Signal, ...]
    decisions: tuple[RiskDecision, ...]
    posture: str

    def lines(self) -> list[str]:
        rows = [f"as_of={self.as_of} posture={self.posture}"]
        for signal, decision in zip(self.signals, self.decisions):
            rows.append(
                f"{signal.symbol:12} {signal.asset_class.value:12} {signal.side.value:6} "
                f"target={signal.target_weight:+.3f} adj={decision.adjusted_weight:+.3f} "
                f"accepted={decision.accepted} :: {signal.reason}"
            )
        return rows


def run(
    bars: list[Bar],
    account: AccountState,
    policy: Policy,
    *,
    kill_switch: bool = False,
) -> Brief:
    grouped = group_by_symbol(bars)
    signals: list[Signal] = []
    decisions: list[RiskDecision] = []
    as_of = max(bar.ts for bar in bars)
    for symbol in sorted(grouped):
        signal = generate(grouped[symbol])
        decision = evaluate(signal, account, policy, kill_switch=kill_switch)
        signals.append(signal)
        decisions.append(decision)
        if decision.accepted:
            account.positions[symbol] = decision.adjusted_weight
    posture = "halted" if kill_switch else "paper"
    return Brief(as_of, tuple(signals), tuple(decisions), posture)
