# Cyber and data security architecture (Enhanced)

This is an engineering control design for a paper trading information system.
It is not a penetration-test report and not legal advice. Updated with additional controls for automated systems and AI agents.

## Trust boundaries

| Zone | Holds | Rule |
|---|---|---|
| Source repo | Code, synthetic tapes, docs | No secrets, no personal data, no production fills |
| Runtime env | `CTIS_MODE`, optional future read-only key | Env only. Never argv, never logs |
| `var/` | Kill switch, audit log | Git-ignored. Treat as sensitive operational data; encrypted at rest in production |
| Exchange | Out of scope | This build has no client; future adapters must use trade-only, withdraw-disabled keys |
| AI agents | Prompts, context | Strict AGENTS.md rules; no secrets or PII in context |

## Controls

1. **Default deny live.** `Policy` refuses `mode=live` unless `CTIS_ALLOW_LIVE=1`, and even then this build raises because order routing is not implemented.
2. **No withdrawal scope.** `withdraw`, `transfer`, and `internal_transfer` cannot be constructed. A future adapter must keep keys trade-disabled and withdraw-disabled at the exchange.
3. **Kill switch.** If `var/KILL` exists, every new target weight is forced to zero. Enhanced: also halt on consecutive risk gate violations.
4. **Risk gate before any paper fill.** Class caps, gross exposure, day-loss halt, **and** correlation caps sit in front of the brief.
5. **Redaction.** Audit payloads scrub keys matching api/secret/token/password/private, and free text is pattern-redacted. Extended to API responses.
6. **Hash-chained audit.** Each line commits to the previous hash. `AuditLog.verify()` detects a broken chain. This detects tampering; it does not stop a host-level attacker who rewrites the whole file. Production: sign with HSM or external timestamp.
7. **Secret tripwire.** `scripts/check_secrets.py` runs in CI. Add gitleaks before any real key material exists nearby. Enhanced with PDPA-style patterns for crypto addresses if needed.
8. **Least privilege for agents.** `AGENTS.md` forbids pasting exchange keys, seed phrases, NRIC/FIN, customer records, or wallet private keys into prompts.
9. **Rate limiting & input validation.** All market data ingest validates schema, bounds prices/volumes, and rate-limits external calls (even synthetic). Reject malformed bars.
10. **Dependency & supply chain.** Licence allow-list, Dependabot, and pin hashes for critical scripts.

## Data security

- Market tapes in-repo are synthetic. Live market data, if added later, should be pulled by an injectable fetcher and cached without account identifiers.
- Personal data is out of scope. Do not join KYC, email, or phone fields into this system.
- Logs must not include request headers, full API payloads, or wallet addresses. If an HTTP client is added, log status, symbol, and latency only.
- Retention: rotate `var/audit.jsonl` and keep the chain tip. Do not commit it. Encrypt sensitive operational data.
- Data minimization: only store necessary fields for strategy computation.

## Recommended production additions (not in this build)

- Secrets manager (not `.env` in the repo) and short-lived tokens (e.g., Vault or cloud KMS).
- Network egress allow-list to the exchange API host only; no arbitrary outbound.
- Separate read-only and trade-only keys; withdraw disabled at the venue.
- Human approval for any change that touches `security/` or risk caps (CODEOWNERS + required reviews).
- Independent reconciliation of paper briefs against venue balances if live mode is ever built.
- Anomaly detection on audit logs and strategy weight changes.
- Regular key rotation and zero-trust network segmentation.
