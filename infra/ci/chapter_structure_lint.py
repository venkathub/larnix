#!/usr/bin/env python3
"""Varsity-contract structure gate (P1-D4 / DECISIONS D0016).

P1 authors ~50 chapters across many sessions; this gate keeps every one of them
true to the Varsity contract (STYLE_GUIDE §2) so chapter #1 and chapter #50 read
as one course. It checks the *structural* pillars of the contract that can be
verified deterministically — the prose quality stays a human review (the
`docs/AUTHORING_CHECKLIST.md` PR checklist).

A chapter (`.qmd` whose front-matter declares `compute:`) must contain:
  1. a **Key Takeaways** box   — `::: {.key-takeaways}`
  2. at least one **runnable** cell — a ```` ```{pyodide} ```` block
  3. at least one **hidden solution** — a `<details>` block (graded exercises)

Non-chapter `.qmd` (module landing pages, sandboxes — no `compute:`) are skipped,
as are `.ipynb` twins (their structure is generated).

Usage:
    python3 chapter_structure_lint.py [PATH ...]
Exit 0 = pass (or nothing to check); 1 = a chapter is missing a contract pillar.
"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter_lint import extract_frontmatter  # noqa: E402

DEFAULT_GLOBS = ["modules/**/*.qmd"]

_KEY_TAKEAWAYS = re.compile(r":::+\s*\{\.key-takeaways\}")
_PYODIDE_CELL = re.compile(r"^`{3,}\{pyodide\}", re.MULTILINE)
_HIDDEN_SOLUTION = re.compile(r"<details\b", re.IGNORECASE)

# (label, compiled-regex, fix-hint) for each required pillar.
PILLARS = [
    ("Key Takeaways box", _KEY_TAKEAWAYS,
     "add `::: {.key-takeaways}` … `:::` near the end (STYLE_GUIDE §7)"),
    ("runnable {pyodide} cell", _PYODIDE_CELL,
     "add at least one ```{pyodide} worked-example cell (every chapter runs)"),
    ("hidden-solution exercise", _HIDDEN_SOLUTION,
     "add 2–4 graded exercises with <details>…</details> hidden solutions"),
]


def is_chapter(path: str) -> bool:
    """A chapter is a `.qmd` whose front-matter declares a compute tier."""
    if not path.endswith(".qmd"):
        return False
    fm = extract_frontmatter(path)
    return isinstance(fm, dict) and "compute" in fm


def check_text(text: str) -> list[str]:
    """Return missing-pillar messages for a chapter's source text."""
    problems = []
    for label, rx, hint in PILLARS:
        if not rx.search(text):
            problems.append(f"missing {label} — {hint}")
    return problems


def check_file(path: str) -> list[str]:
    if not is_chapter(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return check_text(fh.read())


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
    chapters = [p for p in targets if is_chapter(p)]
    if not chapters:
        print("chapter-structure-lint: no chapters found; nothing to check")
        return 0
    failed = 0
    for path in chapters:
        problems = check_file(path)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK   {path}")
    if failed:
        print(f"\n{failed} chapter(s) miss a Varsity-contract pillar")
        return 1
    print(f"\nAll {len(chapters)} chapter(s) satisfy the contract structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
