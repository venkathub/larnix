#!/usr/bin/env python3
"""Quiz schema linter for Larnix `quiz.yml` files (P0 task 7).

Schema (one MCQ set per file):

    title: "Chapter 1 — quick check"      # optional string
    id: "m0-ch1"                          # optional string (storage key)
    shuffle: false                        # optional bool
    questions:                            # required, non-empty list
      - id: what-is-a-model               # optional string, unique within file
        prompt: "A model is…"             # required, non-empty string
        options:                          # required, >= 2 non-empty strings
          - "A spreadsheet of data"
          - "A function learned from data"
        answer: 1                         # required int, 0-based index into options
        explanation: "It is the learned function."   # optional string

Usage:
    python3 quiz_lint.py [PATH ...]

With no PATH, scans default globs. Exit 0 = pass (or nothing to check); 1 = fail.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

DEFAULT_GLOBS = ["modules/**/quiz*.yml", "site/**/quiz*.yml"]


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def validate_quiz(data) -> list[str]:
    """Return a list of error strings ([] means valid)."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["quiz file must be a YAML mapping (got %s)" % type(data).__name__]

    if "title" in data and not _nonempty_str(data["title"]):
        errors.append("title must be a non-empty string")
    if "id" in data and not _nonempty_str(data["id"]):
        errors.append("id must be a non-empty string")
    if "shuffle" in data and not isinstance(data["shuffle"], bool):
        errors.append("shuffle must be a boolean")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append("questions must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for i, q in enumerate(questions):
        where = f"question {i + 1}"
        if not isinstance(q, dict):
            errors.append(f"{where}: must be a mapping")
            continue

        if "id" in q:
            if not _nonempty_str(q["id"]):
                errors.append(f"{where}: id must be a non-empty string")
            elif q["id"] in seen_ids:
                errors.append(f"{where}: duplicate id '{q['id']}'")
            else:
                seen_ids.add(q["id"])

        if not _nonempty_str(q.get("prompt")):
            errors.append(f"{where}: prompt must be a non-empty string")

        options = q.get("options")
        if not isinstance(options, list) or len(options) < 2:
            errors.append(f"{where}: options must be a list of at least 2 entries")
            options = options if isinstance(options, list) else []
        elif not all(_nonempty_str(o) for o in options):
            errors.append(f"{where}: every option must be a non-empty string")

        answer = q.get("answer")
        if not _is_int(answer):
            errors.append(f"{where}: answer must be an integer (0-based option index)")
        elif options and not (0 <= answer < len(options)):
            errors.append(
                f"{where}: answer {answer} out of range for {len(options)} options"
            )

        if "explanation" in q and not _nonempty_str(q["explanation"]):
            errors.append(f"{where}: explanation must be a non-empty string if present")

    return errors


def lint_file(path) -> list[str]:
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as e:
        return [f"could not parse YAML: {e}"]
    return validate_quiz(data)


def collect_targets(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            matches = glob.glob(a, recursive=True)
            out.extend(matches if matches else [a])
        return sorted(set(out))
    out: list[str] = []
    for pattern in DEFAULT_GLOBS:
        out.extend(glob.glob(pattern, recursive=True))
    return sorted(set(out))


def main(argv: list[str]) -> int:
    targets = collect_targets(argv)
    if not targets:
        print("quiz-lint: no quiz.yml files found; nothing to check")
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
        print(f"\n{failed} file(s) failed quiz lint")
        return 1
    print(f"\nAll {len(targets)} file(s) passed quiz lint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
