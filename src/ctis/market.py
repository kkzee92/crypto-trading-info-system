"""Offline market tape. Network access is intentionally not in this module."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from ctis.models import AssetClass, Bar


def load_bars(path: str | Path) -> list[Bar]:
    bars: list[Bar] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ts", "symbol", "asset_class", "open", "high", "low", "close", "volume"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"bars file missing columns: {required}")
        for row in reader:
            bars.append(
                Bar(
                    ts=row["ts"],
                    symbol=row["symbol"].upper(),
                    asset_class=AssetClass(row["asset_class"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                    funding_rate=float(row.get("funding_rate") or 0.0),
                    benchmark_close=float(row.get("benchmark_close") or 0.0),
                    apy=float(row.get("apy") or 0.0),
                    peg=float(row.get("peg") or 1.0),
                )
            )
    bars.sort(key=lambda b: (b.symbol, b.ts))
    return bars


def group_by_symbol(bars: list[Bar]) -> dict[str, list[Bar]]:
    grouped: dict[str, list[Bar]] = defaultdict(list)
    for bar in bars:
        grouped[bar.symbol].append(bar)
    return dict(grouped)
