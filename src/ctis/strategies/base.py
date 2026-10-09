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
