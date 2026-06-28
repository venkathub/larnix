#!/usr/bin/env python3
"""R1 currency gate — frontier content must be freshly reviewed (P0 task 11).

Fails if any `status: frontier` chapter has a `last_reviewed` date older than
`MAX_AGE_DAYS` (90). `stable` chapters are exempt. No-op until frontier chapters
exist; the mechanism is proven now so it covers them automatically later.

Usage:
    python3 currency_check.py [PATH ...]
Exit 0 = pass (or nothing to check); 1 = a frontier chapter is overdue.
"""
from __future__ import annotations

import glob
import sys
from datetime import date

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))

from frontmatter_lint import _parse_date, extract_frontmatter  # noqa: E402

MAX_AGE_DAYS = 90
DEFAULT_GLOBS = ["modules/**/*.qmd", "modules/**/*.ipynb"]


def check_currency(data, *, today: date | None = None, max_age: int = MAX_AGE_DAYS) -> list[str]:
    """Return error strings for a single chapter's front-matter ([] = ok)."""
    if not isinstance(data, dict):
        return []
    if data.get("status") != "frontier":
        return []
    reviewed = _parse_date(data.get("last_reviewed"))
    if reviewed is None:
        return ["frontier chapter has missing/invalid last_reviewed"]
    age = ((today or date.today()) - reviewed).days
    if age > max_age:
        return [f"frontier chapter last_reviewed {age} days ago (> {max_age})"]
    return []


def _collect(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            out.extend(glob.glob(a, recursive=True) if glob.has_magic(a) else [a])
    else:
        out = []
        for pat in DEFAULT_GLOBS:
            out.extend(glob.glob(pat, recursive=True))
    return sorted({p for p in out if ".ipynb_checkpoints" not in p})


def main(argv: list[str]) -> int:
    targets = _collect(argv)
    if not targets:
        print("currency-check (R1): no chapters found; nothing to check")
        return 0
    failed = 0
    for path in targets:
        errors = check_currency(extract_frontmatter(path))
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK   {path}")
    if failed:
        print(f"\n{failed} frontier chapter(s) overdue for review")
        return 1
    print(f"\nAll {len(targets)} chapter(s) within currency window")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
