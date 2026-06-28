#!/usr/bin/env python3
"""Dataset license-ledger gate (R11 / P1-D8, DECISIONS D0016).

Every vendored data file under `modules/**/data/` must be recorded in
`docs/ASSETS.md` with a source + license. This gate fails if a data file is not
ledgered, so a dataset can never ship without a known license.

Check: each data file's repo-relative path (and, as a fallback, its basename)
must appear in `docs/ASSETS.md`.

Usage:
    python3 assets_check.py [LEDGER]
Exit 0 = pass (or no data files); 1 = an un-ledgered data file (or missing ledger).
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

LEDGER = "docs/ASSETS.md"
DATA_GLOBS = ["modules/**/data/**"]


def find_data_files(globs=DATA_GLOBS) -> list[str]:
    out: list[str] = []
    for pat in globs:
        out.extend(p for p in glob.glob(pat, recursive=True) if Path(p).is_file())
    return sorted({p for p in out if ".ipynb_checkpoints" not in p})


def unledgered(data_files, ledger_text: str) -> list[str]:
    """Return data files whose path nor basename appears in the ledger text."""
    missing = []
    for f in data_files:
        rel = f.replace("\\", "/")
        if rel in ledger_text or Path(f).name in ledger_text:
            continue
        missing.append(f)
    return missing


def main(argv: list[str]) -> int:
    ledger = argv[0] if argv else LEDGER
    data_files = find_data_files()
    if not data_files:
        print("assets-check (R11): no data files found; nothing to check")
        return 0

    ledger_path = Path(ledger)
    if not ledger_path.exists():
        print(f"FAIL: ledger {ledger} not found, but {len(data_files)} data file(s) exist")
        for f in data_files:
            print(f"  - {f}")
        return 1

    text = ledger_path.read_text(encoding="utf-8")
    missing = unledgered(data_files, text)
    for f in data_files:
        print(("MISSING " if f in missing else "OK      ") + f)
    if missing:
        print(
            f"\n{len(missing)} data file(s) not ledgered in {ledger} — add a row "
            f"(file, source, license) per R11."
        )
        return 1
    print(f"\nAll {len(data_files)} data file(s) ledgered in {ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
