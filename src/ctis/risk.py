"""Pre-trade risk gate. A signal is not an order until this accepts it."""

from __future__ import annotations

from ctis.models import AccountState, RiskDecision, Signal
from ctis.security.policy import Policy, class_cap


def evaluate(
    signal: Signal,
    account: AccountState,
    policy: Policy,
    *,
    kill_switch: bool = False,
) -> RiskDecision:
    reasons: list[str] = []
    weight = signal.target_weight
    if account.mode != "paper" or policy.mode != "paper":
        reasons.append("non-paper mode blocked")
        weight = 0.0
    if kill_switch:
        reasons.append("kill switch engaged")
        weight = 0.0
    if account.day_pnl_pct <= -policy.max_day_loss_pct:
        reasons.append(f"day loss {account.day_pnl_pct:.2%} breaches {policy.max_day_loss_pct:.2%}")
        weight = 0.0
    cap = class_cap(policy, signal.asset_class.value)
    if abs(weight) > cap:
        reasons.append(f"class cap {cap:.2f} applied")
        weight = cap if weight > 0 else -cap
    if abs(weight) > policy.max_leverage * cap:
        reasons.append("leverage cap applied")
        weight = policy.max_leverage * cap if weight > 0 else -policy.max_leverage * cap
    projected = account.gross_exposure() - abs(account.positions.get(signal.symbol, 0.0)) + abs(weight)
    if projected > policy.max_gross_exposure and abs(weight) > 0:
        reasons.append(f"gross exposure {projected:.2f} > {policy.max_gross_exposure:.2f}")
        weight = 0.0
    accepted = abs(weight) > 0 or signal.side.value in {"hold", "reduce", "sell"}
    if weight == 0.0 and signal.target_weight != 0.0 and reasons:
        accepted = False
    if not reasons:
        reasons.append("within policy")
    return RiskDecision(
        accepted=accepted,
        symbol=signal.symbol,
        strategy=signal.strategy,
        adjusted_weight=round(weight, 6),
        reasons=tuple(reasons),
    )
