# Crypto trading information system (paper only)

Paper brief for automated crypto research: one strategy per asset class, a risk gate, and a cyber/data security architecture.

Inspired by the agent harness in [zeekiankok92/aixtech-agent-harness-demo](https://github.com/zeekiankok92/aixtech-agent-harness-demo) (CI gates, disclosure trail, synthetic fixtures, no production personal data). This repo was created on the connected account `kkzee92` because that account has pull-only access to `zeekiankok92`.

**Not financial advice. Not a live trading bot. No withdrawal path.**

## Run

```bash
python -m pytest -q
python scripts/check_secrets.py
PYTHONPATH=src python -m ctis fixtures/bars.csv
```

## Layout

- `src/ctis/strategies/` — large-cap, altcoin, stablecoin, perpetual, yield info
- `src/ctis/risk.py` — class caps, day-loss halt, gross exposure
- `src/ctis/security/` — policy, kill switch, redaction, hash-chained audit
- `docs/security-architecture.md` — trust boundaries and controls
- `docs/strategies-by-asset-class.md` — sleeve rules and enhancement backlog

Live mode is refused unless `CTIS_ALLOW_LIVE=1`, and even then this build does not route orders.
