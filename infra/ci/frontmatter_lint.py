#!/usr/bin/env python3
"""Front-matter linter for Larnix chapters (P0 task 4).

Validates the 10-field chapter front-matter schema defined in
`docs/CHAPTER_TEMPLATE.md`:

    title, module, chapter, difficulty, prereqs, learning_objectives,
    compute, status, last_reviewed, est_minutes

Works on Quarto `.qmd` (leading `---` YAML block) and Jupyter `.ipynb`
(YAML in the first raw/markdown cell). Unknown extra keys are allowed so future
conventions (e.g. `review_cards:` in P0 task 13) do not break this gate.

Usage:
    python3 frontmatter_lint.py [PATH ...]

With no PATH, scans the default chapter globs (modules/**/*.qmd, *.ipynb).
Exit code 0 = all good (or nothing to check); 1 = at least one file failed.
"""
from __future__ import annotations

import glob
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

REQUIRED_FIELDS = [
    "title", "module", "chapter", "difficulty", "prereqs",
    "learning_objectives", "compute", "status", "last_reviewed", "est_minutes",
]
DIFFICULTIES = {"beginner", "intermediate", "advanced"}
COMPUTES = {"browser", "colab", "gpu"}
STATUSES = {"stable", "frontier"}
MODULE_RE = re.compile(r"^M\d+\b")

DEFAULT_GLOBS = ["modules/**/*.qmd", "modules/**/*.ipynb"]


# ── front-matter extraction ─────────────────────────────────────────────────
def _yaml_between_fences(text: str):
    """Return the dict parsed from a leading `---` ... `---` YAML block, or None."""
    lines = text.lstrip("\ufeff").splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return None
    start = i + 1
    for j in range(start, len(lines)):
        if lines[j].strip() in ("---", "..."):
            block = "\n".join(lines[start:j])
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                return None
            return data if isinstance(data, dict) else None
    return None


def extract_frontmatter(path):
    """Extract the YAML front-matter dict from a .qmd or .ipynb file (or None)."""
    p = Path(path)
    if p.suffix == ".ipynb":
        try:
            nb = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        for cell in nb.get("cells", []):
            if cell.get("cell_type") in ("raw", "markdown"):
                src = cell.get("source", "")
                if isinstance(src, list):
                    src = "".join(src)
                fm = _yaml_between_fences(src)
                if fm is not None:
                    return fm
        return None
    return _yaml_between_fences(p.read_text(encoding="utf-8"))


# ── value helpers ───────────────────────────────────────────────────────────
def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_int(v) -> bool:
    # bool is a subclass of int — exclude it.
    return isinstance(v, int) and not isinstance(v, bool)


def _is_list_of_str(v, *, allow_empty: bool) -> bool:
    if not isinstance(v, list):
        return False
    if not v:
        return allow_empty
    return all(_nonempty_str(x) for x in v)


def _parse_date(v):
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        try:
            return datetime.strptime(v.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


# ── schema validation ───────────────────────────────────────────────────────
def validate_frontmatter(data, *, today: date | None = None) -> list[str]:
    """Return a list of human-readable error strings ([] means valid)."""
    if data is None:
        return ["no YAML front-matter found"]
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")

    if "title" in data and not _nonempty_str(data["title"]):
        errors.append("title must be a non-empty string")

    if "module" in data:
        if not _nonempty_str(data["module"]) or not MODULE_RE.match(str(data["module"])):
            errors.append('module must be a string like "M0 — Module name"')

    if "chapter" in data and not (_is_int(data["chapter"]) and data["chapter"] >= 0):
        errors.append("chapter must be a non-negative integer")

    if "difficulty" in data and data["difficulty"] not in DIFFICULTIES:
        errors.append(f"difficulty must be one of {sorted(DIFFICULTIES)}")

    if "prereqs" in data and not _is_list_of_str(data["prereqs"], allow_empty=True):
        errors.append("prereqs must be a list of strings (may be empty)")

    if "learning_objectives" in data:
        lo = data["learning_objectives"]
        if not _is_list_of_str(lo, allow_empty=False):
            errors.append("learning_objectives must be a non-empty list of strings")
        elif not (2 <= len(lo) <= 4):
            errors.append("learning_objectives must have 2–4 items")

    if "compute" in data and data["compute"] not in COMPUTES:
        errors.append(f"compute must be one of {sorted(COMPUTES)}")

    if "status" in data and data["status"] not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    if "last_reviewed" in data:
        d = _parse_date(data["last_reviewed"])
        if d is None:
            errors.append("last_reviewed must be a date in YYYY-MM-DD format")
        elif d > (today or date.today()):
            errors.append("last_reviewed is in the future")

    if "est_minutes" in data and not (_is_int(data["est_minutes"]) and data["est_minutes"] > 0):
        errors.append("est_minutes must be a positive integer")

    return errors


def lint_file(path) -> list[str]:
    return validate_frontmatter(extract_frontmatter(path))


# ── CLI ─────────────────────────────────────────────────────────────────────
def collect_targets(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            matches = glob.glob(a, recursive=True)
            out.extend(matches if matches else [a])
        return sorted(set(out))
    out = []
    for pattern in DEFAULT_GLOBS:
        out.extend(glob.glob(pattern, recursive=True))
    return sorted(set(out))


def main(argv: list[str]) -> int:
    targets = collect_targets(argv)
    if not targets:
        print("frontmatter-lint: no chapter files found; nothing to check")
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
        print(f"\n{failed} file(s) failed front-matter lint")
        return 1
    print(f"\nAll {len(targets)} file(s) passed front-matter lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
