#!/usr/bin/env python3
"""Vendor a seeded 800-row sample of California Housing (P2-D2 / R11).

Source: scikit-learn's own `fetch_california_housing` loader (1990 U.S. Census
block-group data via StatLib — public domain; see `docs/ASSETS.md`). The full
set is 20,640 rows; M4's browser chapters vendor a fixed sample so pages load
offline at ₹0 and CI twins stay deterministic (P1-D8's ≤~50 KB rule).

Determinism: `.sample(n=N_ROWS, random_state=SEED)`, rows re-sorted by original
index, all columns rounded to 4 dp (more precision than the source
measurements; the derived ratio columns otherwise carry full float64 tails).
Re-running must reproduce the committed CSV byte-for-byte.

Run from the repo root:
    python infra/datasets/make_california_sample.py
"""
from __future__ import annotations

from pathlib import Path

from sklearn.datasets import fetch_california_housing

SEED = 0
N_ROWS = 800  # with 4-dp rounding ≈ 50 KB (the P1-D8 vendoring cap)
OUT = Path("modules/04-classical-ml/data/california-housing-sample.csv")


def build() -> "pandas.DataFrame":  # noqa: F821 - imported lazily below
    bunch = fetch_california_housing(as_frame=True)
    df = bunch.frame  # 8 features + MedHouseVal target, 20,640 rows
    sample = df.sample(n=N_ROWS, random_state=SEED).sort_index()
    # The ratio columns (AveRooms/AveBedrms/AveOccup) are derived quantities
    # with full float64 tails; 4 dp keeps more precision than the source
    # measurements while halving the file size.
    return sample.round(4)


def main() -> int:
    sample = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # index=True keeps the original row id — honest provenance back to the
    # full dataset, and a stable join key if a chapter ever needs it.
    sample.to_csv(OUT, index=True, index_label="row_id", lineterminator="\n")
    size_kb = OUT.stat().st_size / 1024
    print(f"WROTE {OUT} ({len(sample)} rows, {size_kb:.1f} KB)")
    if size_kb > 55:
        print("WARN: sample exceeds the ~50 KB vendoring rule — reduce N_ROWS")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
