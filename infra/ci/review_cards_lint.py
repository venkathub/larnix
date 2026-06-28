#!/usr/bin/env python3
"""Spaced-repetition card seeding gate (P0 task 13 / P0-D3).

Validates an optional `review_cards:` block in chapter front-matter — Q/A pairs
seeded from the chapter's Key Takeaways. The scheduler that serves them is P6;
P0 only proves the *authoring convention* so no later chapter needs retrofitting.

Schema (optional; validated only when present):

    review_cards:
      - id: what-is-a-model        # optional, unique within the chapter
        q: "What is a model?"      # required, non-empty
        a: "A function learned from data that maps inputs to a prediction."  # required

Usage:
    python3 review_cards_lint.py [PATH ...]
Exit 0 = pass (or nothing to check); 1 = a malformed review_cards block.
"""
from __future__ import annotations

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter_lint import extract_frontmatter  # noqa: E402

DEFAULT_GLOBS = ["modules/**/*.qmd", "modules/**/*.ipynb"]


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def validate_review_cards(data) -> list[str]:
    """Return error strings for a chapter's review_cards block ([] = ok/absent)."""
    if not isinstance(data, dict) or "review_cards" not in data:
        return []
    cards = data["review_cards"]
    if not isinstance(cards, list) or not cards:
        return ["review_cards must be a non-empty list when present"]

    errors: list[str] = []
    seen_ids: set[str] = set()
    for i, card in enumerate(cards):
        where = f"review_cards[{i}]"
        if not isinstance(card, dict):
            errors.append(f"{where}: must be a mapping with q and a")
            continue
        if not _nonempty_str(card.get("q")):
            errors.append(f"{where}: q must be a non-empty string")
        if not _nonempty_str(card.get("a")):
            errors.append(f"{where}: a must be a non-empty string")
        if "id" in card:
            if not _nonempty_str(card["id"]):
                errors.append(f"{where}: id must be a non-empty string")
            elif card["id"] in seen_ids:
                errors.append(f"{where}: duplicate id '{card['id']}'")
            else:
                seen_ids.add(card["id"])
    return errors


def lint_file(path) -> list[str]:
    return validate_review_cards(extract_frontmatter(path))


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
        print("review-cards-lint: no chapters found; nothing to check")
        return 0
    failed = 0
    for path in targets:
        errors = lint_file(path)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK   {path}")
    if failed:
        print(f"\n{failed} chapter(s) have malformed review_cards")
        return 1
    print(f"\nAll {len(targets)} chapter(s) have valid review_cards (or none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
