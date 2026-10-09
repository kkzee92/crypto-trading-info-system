# Agent rules

- This repo is paper-only. Do not add an exchange order client, withdrawal call, or seed-phrase handling.
- Do not paste API keys, private keys, KYC records, NRIC/FIN, phone numbers, or emails into code, fixtures, or docs.
- Strategies must stay behind `risk.evaluate`. Do not write a path that applies a target weight without that gate.
- Keep fixtures synthetic and labelled.
- A change to `src/ctis/security/` or risk caps needs a human reviewer named in the PR.
