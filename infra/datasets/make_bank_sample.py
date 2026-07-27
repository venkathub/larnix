#!/usr/bin/env python3
"""Vendor a seeded stratified sample of UCI Bank Marketing (P2-D2 / R11).

Source: UCI ML Repository ID 222 (Moro, Laureano & Cortez), licence CC BY 4.0.
Full set: 45,211 telemarketing calls, 16 features + target `y` ("did the
customer subscribe a term deposit?"), naturally imbalanced (~11.7% yes).

The M4 capstone vendors a **1,500-row stratified sample** (~150 KB). This
deliberately exceeds the ≤~50 KB vendoring rule as a documented exception
(DECISIONS D0021): under 50 KB the sample would hold ~50 positive customers —
too few for an imbalanced-workflow capstone — and the rule's purpose (page
weight) is barely dented next to the Pyodide runtime the page already loads.

Determinism: stratified `.sample(frac=..., random_state=SEED)` per class, rows
re-sorted by original index. Re-running must reproduce the committed CSV
byte-for-byte.

Run from the repo root:
    python infra/datasets/make_bank_sample.py
"""
from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
SEED = 0
N_ROWS = 1500
OUT = Path("modules/04-classical-ml/data/bank-marketing-sample.csv")


def fetch_full_table():
    import pandas as pd

    print(f"fetching {URL} …")
    with urllib.request.urlopen(URL, timeout=120) as resp:
        outer = zipfile.ZipFile(io.BytesIO(resp.read()))
    # The UCI archive nests bank.zip (bank-full.csv) inside the outer zip.
    inner = zipfile.ZipFile(io.BytesIO(outer.read("bank.zip")))
    with inner.open("bank-full.csv") as fh:
        df = pd.read_csv(fh, sep=";")
    print(f"full table: {df.shape[0]} rows, {df.shape[1]} columns, "
          f"{(df['y'] == 'yes').mean():.1%} yes")
    return df


def build(df):
    frac = N_ROWS / len(df)
    sample = (
        df.groupby("y", group_keys=False)[df.columns.tolist()]
        .apply(lambda g: g.sample(frac=frac, random_state=SEED))
        .sort_index()
    )
    return sample


def main() -> int:
    sample = build(fetch_full_table())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(OUT, index=False, lineterminator="\n")
    size_kb = OUT.stat().st_size / 1024
    print(f"WROTE {OUT} ({len(sample)} rows, "
          f"{(sample['y'] == 'yes').mean():.1%} yes, {size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
