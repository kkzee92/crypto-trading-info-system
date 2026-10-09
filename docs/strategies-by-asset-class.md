# Strategies by asset class

These are information rules for a paper brief. They are not a recommendation to trade.

## Large-cap spot (BTC, ETH)

- Signal: close above the 10-bar SMA and that SMA above the 20-bar SMA.
- Volatility gate: if 10-bar ATR / close exceeds 6%, cut the sleeve to 5%.
- Cap: 25% target, 30% hard class cap.
- Why: large-cap books can carry a trend sleeve; the vol gate is the risk control, not a forecast.

## Altcoin spot

- Signal: 5-bar excess return versus the BTC benchmark above 3%, and own return positive.
- Liquidity floor: last bar volume below 1,000,000 forces a flat sleeve.
- Cap: 8% target, 10% hard class cap.
- Why: altcoin edge is mostly relative strength and exit liquidity. Thin names are not traded.

## Stablecoin / cash

- Hold a 20% cash sleeve only while abs(peg - 1) is under 0.5%.
- At or beyond 0.5%, the sleeve goes to zero. That is a circuit breaker, not a mean-reversion trade.
- Cap: 40%, so cash can be the residual without becoming a hidden directional bet.

## Perpetual futures

- Funding at or above 0.04% per bar: paper short carry, weight -10%.
- Funding at or below -0.04%: paper long carry, weight +10%.
- Absolute funding at or above 0.3%: flat. Extremes are a stress flag.
- Leverage policy is 1.0. This build will not scale notional above the class cap.

## Yield / venue information

- APY from 3% to 20%: informational 5% sleeve. The brief says no wallet signing.
- APY at or above 20%: risk flag, weight zero. Advertised APY is not treated as edge.
- No transaction construction, no private key, no approval spender logic.

## Enhancement backlog

- Regime filter shared across sleeves (trend vs range) so altcoin risk budget shrinks when large-cap vol gate is on.
- Correlation cap: refuse a second altcoin if its 20-bar return correlation to an open altcoin exceeds 0.8.
- Funding and basis together, so a perp sleeve requires both to agree.
- Walk-forward report on a longer synthetic tape before any live-data experiment.
