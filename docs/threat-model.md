# Threat model

| Threat | Effect | Mitigation in this build |
|---|---|---|
| Secret committed | Account takeover if the key can trade or withdraw | No keys in repo; CI tripwire; withdraw scope cannot be constructed |
| Prompt injection into an agent | Agent writes a live router or leaks a key | `AGENTS.md` forbids live routing and secret handling; human review on `security/` |
| Kill-switch bypass | Brief keeps sizing into a halt | Engine checks the flag before acceptance; test covers halted posture |
| Audit tamper | False history of decisions | Hash chain verification. Host compromise can still rewrite the file |
| Depeg ignored | Cash sleeve holds a broken stablecoin | Stablecoin strategy forces weight 0 at 50 bps |
| Over-size altcoin | Concentration | Class cap and gross exposure gate |
| Personal data in fixtures | PDPA exposure, as in the weather harness | Synthetic tape only; do not add KYC fields |

Out of scope: exchange outages, oracle manipulation on a live venue, and smart-contract exploits. Those need a different system than this paper brief.
