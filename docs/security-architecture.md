# Cyber and data security architecture

This is an engineering control design for a paper trading information system.
It is not a penetration-test report and not legal advice.

## Trust boundaries

| Zone | Holds | Rule |
|---|---|---|
| Source repo | Code, synthetic tapes, docs | No secrets, no personal data, no production fills |
| Runtime env | `CTIS_MODE`, optional future read-only key | Env only. Never argv, never logs |
| `var/` | Kill switch, audit log | Git-ignored. Treat as sensitive operational data |
| Exchange | Out of scope | This build has no client |

## Controls

1. **Default deny live.** `Policy` refuses `mode=live` unless `CTIS_ALLOW_LIVE=1`, and even then this build raises because order routing is not implemented.
2. **No withdrawal scope.** `withdraw`, `transfer`, and `internal_transfer` cannot be constructed. A future adapter must keep keys trade-disabled and withdraw-disabled at the exchange.
3. **Kill switch.** If `var/KILL` exists, every new target weight is forced to zero.
4. **Risk gate before any paper fill.** Class caps, gross exposure, and a day-loss halt sit in front of the brief.
5. **Redaction.** Audit payloads scrub keys matching api/secret/token/password/private, and free text is pattern-redacted.
6. **Hash-chained audit.** Each line commits to the previous hash. `AuditLog.verify()` detects a broken chain. This detects tampering; it does not stop a host-level attacker who rewrites the whole file.
7. **Secret tripwire.** `scripts/check_secrets.py` runs in CI. Add gitleaks before any real key material exists nearby.
8. **Least privilege for agents.** `AGENTS.md` forbids pasting exchange keys, seed phrases, NRIC/FIN, or customer records into prompts.

## Data security

- Market tapes in-repo are synthetic. Live market data, if added later, should be pulled by an injectable fetcher and cached without account identifiers.
- Personal data is out of scope. Do not join KYC, email, or phone fields into this system.
- Logs must not include request headers. If an HTTP client is added, log status and symbol only.
- Retention: rotate `var/audit.jsonl` and keep the chain tip. Do not commit it.

## Recommended production additions (not in this build)

- Secrets manager (not `.env` in the repo) and short-lived tokens.
- Network egress allow-list to the exchange API host only.
- Separate read-only and trade-only keys; withdraw disabled at the venue.
- Human approval for any change that touches `security/` or risk caps.
- Independent reconciliation of paper briefs against venue balances if live mode is ever built.
