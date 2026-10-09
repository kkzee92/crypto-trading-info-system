"""CLI for the paper information brief."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ctis.engine import run
from ctis.market import load_bars
from ctis.models import AccountState
from ctis.security.audit import AuditLog
from ctis.security.killswitch import tripped
from ctis.security.policy import load_policy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Paper crypto trading information brief")
    parser.add_argument("bars", type=Path, help="CSV tape")
    parser.add_argument("--equity", type=float, default=100_000.0)
    parser.add_argument("--day-pnl", type=float, default=0.0)
    parser.add_argument("--kill-switch", type=Path, default=Path("var/KILL"))
    parser.add_argument("--audit", type=Path, default=Path("var/audit.jsonl"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    policy = load_policy()
    account = AccountState(equity=args.equity, cash=args.equity, day_pnl_pct=args.day_pnl, mode=policy.mode)
    brief = run(load_bars(args.bars), account, policy, kill_switch=tripped(args.kill_switch))
    audit = AuditLog(args.audit)
    audit.append(
        "brief",
        {
            "as_of": brief.as_of,
            "posture": brief.posture,
            "decisions": [
                {"symbol": d.symbol, "accepted": d.accepted, "weight": d.adjusted_weight, "reasons": list(d.reasons)}
                for d in brief.decisions
            ],
        },
    )
    if args.json:
        print(
            json.dumps(
                {
                    "as_of": brief.as_of,
                    "posture": brief.posture,
                    "lines": brief.lines(),
                },
                indent=2,
            )
        )
    else:
        print("\n".join(brief.lines()))
    return 0
