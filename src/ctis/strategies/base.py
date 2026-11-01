"""Shared indicators. Pure functions, no I/O."""

from __future__ import annotations

from ctis.models import Bar


def sma(values: list[float], window: int) -> float | None:
    if window <= 0 or len(values) < window:
        return None
    sample = values[-window:]
    return sum(sample) / window


def atr(bars: list[Bar], window: int = 14) -> float | None:
    if len(bars) < window + 1:
        return None
    ranges: list[float] = []
    for prev, bar in zip(bars[-(window + 1) : -1], bars[-window:]):
        true_range = max(bar.high - bar.low, abs(bar.high - prev.close), abs(bar.low - prev.close))
        ranges.append(true_range)
    return sum(ranges) / len(ranges)


def return_over(values: list[float], window: int) -> float | None:
    if len(values) <= window or values[-window - 1] == 0:
        return None
    return values[-1] / values[-window - 1] - 1.0


def rsi(values: list[float], window: int = 14) -> float | None:
    """Simple RSI implementation (Wilder's method approximation)."""
    if len(values) < window + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(values)):
        delta = values[i] - values[i - 1]
        if delta > 0:
            gains.append(delta)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-delta)
    if len(gains) < window:
        return None
    avg_gain = sum(gains[-window:]) / window
    avg_loss = sum(losses[-window:]) / window
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))
