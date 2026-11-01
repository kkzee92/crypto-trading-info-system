# Strategies by asset class (Enhanced)

These are information rules for a paper brief. They are not a recommendation to trade. Enhanced with regime detection, momentum confirmation, and cross-sleeve risk controls.

## Shared Regime Filter
- Compute 20-bar SMA slope and 10-bar ATR/close across major assets (BTC as proxy).
- **Trend regime**: slope > 0 and ATR/close < 0.05 → full risk budget.
- **High-vol regime**: ATR/close > 0.06 → shrink all directional sleeves by 50%.
- **Range regime**: otherwise → favor mean-reversion or flat.
- Applied before individual sleeve signals.

## Large-cap spot (BTC, ETH)

- Signal: close above the 10-bar SMA and that SMA above the 20-bar SMA **plus** RSI(14) between 40-70 (avoid overbought).
- Volatility gate: if 10-bar ATR / close exceeds 6%, cut the sleeve to 5% or flat in high-vol regime.
- Cap: 25% target, 30% hard class cap.
- Volume confirmation: require above-average volume on breakout bars.
- Why: large-cap books can carry a trend sleeve; the vol gate + RSI is the risk control.

## Altcoin spot

- Signal: 5-bar excess return versus the BTC benchmark above 3%, own return positive, **and** relative volume > 1.5x average.
- Liquidity floor: last bar volume below 1,000,000 forces a flat sleeve.
- Correlation cap: refuse entry if 20-bar return correlation to any open altcoin > 0.75.
- Cap: 8% target, 10% hard class cap. Shrink further in high-vol regime.
- Why: altcoin edge is mostly relative strength and exit liquidity. Thin or highly correlated names are avoided.

## Stablecoin / cash

- Hold a 20% cash sleeve only while abs(peg - 1) is under 0.5% **and** no high-vol regime on majors.
- At or beyond 0.5%, the sleeve goes to zero. That is a circuit breaker.
- Cap: 40%, so cash can be the residual without becoming a hidden directional bet.
- In high-vol: increase cash to 40% automatically.

## Perpetual futures

- Funding at or above 0.04% per bar **and** basis agrees: paper short carry, weight -10%.
- Funding at or below -0.04% **and** basis agrees: paper long carry, weight +10%.
- Absolute funding at or above 0.3% or basis extreme: flat. Extremes are a stress flag.
- Leverage policy is 1.0. This build will not scale notional above the class cap.
- Regime: only active in trend regime; flat otherwise.

## Yield / venue information

- APY from 3% to 15%: informational 5% sleeve (tightened from 20%). The brief says no wallet signing.
- APY at or above 15%: risk flag, weight zero. Advertised APY is not treated as edge.
- Additional: require TVL > $10M equivalent (synthetic check) and no recent exploit flags in fixtures.
- No transaction construction, no private key, no approval spender logic.

## Enhancement backlog (updated)

- Full walk-forward validation on longer synthetic tapes with transaction costs.
- Dynamic position sizing based on Kelly fraction capped at 0.5 of class max.
- Multi-timeframe confirmation (e.g., daily bias for hourly signals).
- Explicit basis + funding agreement for perps (implemented above).
- Correlation matrix monitoring across all open sleeves.
