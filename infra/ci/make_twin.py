#!/usr/bin/env python3
"""Twin generator (P1-D10 / DECISIONS D0016) — build & verify CI twin notebooks.

Every `compute: browser` chapter runs its `{pyodide}` cells client-side, which a
headless CI render never executes. Its R10 guarantee instead comes from a CPython
"twin" `.ipynb` (DECISIONS D0010) that runs the same code under nbclient. Hand-
maintaining ~50 twins invites drift, so this tool **derives** each twin from its
chapter source and a CI `--check` fails if a committed twin no longer matches.

Extraction convention (D0016 implementation note):
  1. Every `{pyodide}` cell that is *not* an `exercise:` and *not* a `setup:` cell
     (the worked-example cells) is copied verbatim, in document order.
  2. One **grader bootstrap** cell makes `lib/grader.py` importable under CPython
     (single-source: the twin does not paste the grader either).
  3. For each *auto-graded* exercise (its cell calls `run_tests(`), the twin emits
     the hidden `<details>` **solution** code followed by the `run_tests(...)`
     assert block lifted from the exercise cell. Solutions must be runnable given
     the cells above them (an authoring requirement).
  4. Stretch / rubric exercises (no `run_tests`) are skipped — they are human-graded.

Usage:
    python3 make_twin.py --write [PATH ...]   # (re)generate twins (default: all browser chapters)
    python3 make_twin.py --check [PATH ...]   # fail if a committed twin differs from source
With no PATH, scans modules/**/*.qmd. A chapter twin is `<chapter-stem>.ipynb`.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter_lint import extract_frontmatter  # noqa: E402

DEFAULT_GLOBS = ["modules/**/*.qmd"]

# The 10-field schema (mirrors frontmatter_lint.REQUIRED_FIELDS), emitted in order.
TWIN_FIELDS = [
    "title", "module", "chapter", "difficulty", "prereqs",
    "learning_objectives", "compute", "status", "last_reviewed", "est_minutes",
]

# A `{pyodide}` fenced cell: capture its body (which includes any leading `#|` opts).
_CELL_RE = re.compile(r"^```\{pyodide\}[^\n]*\n(.*?)\n```", re.S | re.M)
# A hidden-solution block: <details> … </details>; capture inner HTML.
_DETAILS_RE = re.compile(r"<details>(.*?)</details>", re.S)
# A python fenced block (used to pull the solution out of a <details>).
_PYBLOCK_RE = re.compile(r"```python\n(.*?)\n```", re.S)
_OPT_RE = re.compile(r"^#\|\s*([\w-]+)\s*:\s*(.*?)\s*$")


# ── source parsing ───────────────────────────────────────────────────────────
def _split_options(body: str) -> tuple[dict, str]:
    """Split leading contiguous `#| key: value` option lines from the cell body."""
    opts: dict[str, str] = {}
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        m = _OPT_RE.match(lines[i])
        if not m:
            break
        opts[m.group(1)] = m.group(2)
        i += 1
    return opts, "\n".join(lines[i:]).strip("\n")


def _is_true(v: str) -> bool:
    return str(v).strip().strip('"').strip("'").lower() == "true"


def _run_tests_block(code: str) -> str | None:
    """Return the contiguous block from the first `run_tests(` line to end of cell."""
    lines = code.splitlines()
    for idx, ln in enumerate(lines):
        if ln.lstrip().startswith("run_tests("):
            return "\n".join(lines[idx:]).strip("\n")
    return None


def _solution_code(details_inner: str) -> str | None:
    m = _PYBLOCK_RE.search(details_inner)
    return m.group(1).strip("\n") if m else None


def parse_chapter(text: str) -> list[dict]:
    """Return ordered twin cells: worked-example code + paired exercise solutions.

    Each item: {"id": str, "code": str}. Pairing: an auto-graded exercise cell is
    matched to the next <details> solution that follows it in the document.
    """
    events: list[tuple[int, str, object]] = []
    for m in _CELL_RE.finditer(text):
        events.append((m.start(), "cell", m.group(1)))
    for m in _DETAILS_RE.finditer(text):
        events.append((m.start(), "sol", m.group(1)))
    events.sort(key=lambda e: e[0])

    cells: list[dict] = []
    worked_n = 0
    pending: dict | None = None  # an auto-graded exercise awaiting its solution

    for _pos, kind, payload in events:
        if kind == "cell":
            opts, body = _split_options(str(payload))
            if "exercise" in opts and not _is_true(opts.get("setup", "")):
                asserts = _run_tests_block(body)
                if asserts is not None:
                    pending = {"exercise": opts["exercise"], "asserts": asserts}
                # else: a non-graded exercise cell — skip.
            elif _is_true(opts.get("setup", "")):
                continue  # setup cells are replaced by the single grader bootstrap
            else:
                worked_n += 1
                cells.append({"id": f"worked-{worked_n}", "code": body})
        elif kind == "sol" and pending is not None:
            sol = _solution_code(str(payload))
            if sol is not None:
                cells.append({
                    "id": f"ex-{pending['exercise']}",
                    "code": f"{sol}\n\n{pending['asserts']}",
                })
            pending = None
    return cells


# ── notebook emission (deterministic) ────────────────────────────────────────
def _yaml_scalar(key: str, val) -> str:
    if isinstance(val, bool):  # not expected in TWIN_FIELDS, but be safe
        return f"{key}: {'true' if val else 'false'}"
    if isinstance(val, int):
        return f"{key}: {val}"
    if isinstance(val, (date, datetime)):
        d = val.date() if isinstance(val, datetime) else val
        return f'{key}: "{d.isoformat()}"'
    s = str(val).replace('"', '\\"')
    return f'{key}: "{s}"'


def _yaml_list(key: str, val: list) -> list[str]:
    if not val:
        return [f"{key}: []"]
    out = [f"{key}:"]
    for item in val:
        s = str(item).replace('"', '\\"')
        out.append(f'  - "{s}"')
    return out


def _frontmatter_lines(fm: dict, source_name: str) -> list[str]:
    lines = ["---"]
    for field in TWIN_FIELDS:
        val = fm.get(field)
        if field == "title":
            val = f"{val} (CI twin)"
        if isinstance(val, list):
            lines.extend(_yaml_list(field, val))
        else:
            lines.append(_yaml_scalar(field, val))
    lines.append("---")
    return lines


_GRADER_BOOTSTRAP = (
    "# Make the single-sourced grader importable under CPython (no paste; P1-D9).\n"
    "import sys, pathlib\n"
    "for _p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:\n"
    "    if (_p / 'lib' / 'grader.py').exists():\n"
    "        sys.path.insert(0, str(_p))\n"
    "        break\n"
    "from lib.grader import run_tests"
)


def _raw_cell(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "raw",
        "id": cell_id,
        "metadata": {},
        "source": _as_source(text),
    }


def _md_cell(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": _as_source(text),
    }


def _code_cell(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": _as_source(text),
    }


def _as_source(text: str) -> list[str]:
    """nbformat stores source as a list of lines, each (except the last) ending \\n."""
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + [lines[-1]]


def build_notebook(qmd_path: str) -> dict:
    text = Path(qmd_path).read_text(encoding="utf-8")
    fm = extract_frontmatter(qmd_path)
    if not isinstance(fm, dict):
        raise ValueError(f"{qmd_path}: no front-matter")
    name = Path(qmd_path).name
    cells = [
        _raw_cell("frontmatter", "\n".join(_frontmatter_lines(fm, name))),
        _md_cell(
            "twin-note",
            f"**CI twin of `{name}`.** Generated by `infra/ci/make_twin.py` "
            "(P1-D10); do not edit by hand. It runs the chapter's worked example and "
            "exercise solutions under CPython so the R10 gate proves they work "
            "(DECISIONS D0010).",
        ),
        _code_cell("grader-bootstrap", _GRADER_BOOTSTRAP),
    ]
    derived = parse_chapter(text)
    for cell in derived:
        cells.append(_code_cell(cell["id"], cell["code"]))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def notebook_text(qmd_path: str) -> str:
    nb = build_notebook(qmd_path)
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


# ── CLI ──────────────────────────────────────────────────────────────────────
def _twin_path(qmd_path: str) -> Path:
    return Path(qmd_path).with_suffix(".ipynb")


def _is_browser_chapter(qmd_path: str) -> bool:
    fm = extract_frontmatter(qmd_path)
    return isinstance(fm, dict) and fm.get("compute") == "browser"


def _has_pyodide(qmd_path: str) -> bool:
    return bool(_CELL_RE.search(Path(qmd_path).read_text(encoding="utf-8")))


def _collect(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            out.extend(glob.glob(a, recursive=True) if glob.has_magic(a) else [a])
    else:
        out = []
        for pat in DEFAULT_GLOBS:
            out.extend(glob.glob(pat, recursive=True))
    return sorted({p for p in out if p.endswith(".qmd")})


def _targets(args: list[str]) -> list[str]:
    return [p for p in _collect(args) if _is_browser_chapter(p) and _has_pyodide(p)]


def cmd_write(args: list[str]) -> int:
    targets = _targets(args)
    if not targets:
        print("make-twin: no browser chapters with runnable cells found")
        return 0
    for qmd in targets:
        twin = _twin_path(qmd)
        twin.write_text(notebook_text(qmd), encoding="utf-8")
        print(f"WROTE {twin}")
    print(f"\nGenerated {len(targets)} twin(s)")
    return 0


def cmd_check(args: list[str]) -> int:
    targets = _targets(args)
    if not targets:
        print("make-twin --check: no browser chapters with runnable cells found")
        return 0
    drift = 0
    for qmd in targets:
        twin = _twin_path(qmd)
        expected = notebook_text(qmd)
        if not twin.exists():
            drift += 1
            print(f"MISSING {twin} — run: python infra/ci/make_twin.py --write {qmd}")
            continue
        if twin.read_text(encoding="utf-8") != expected:
            drift += 1
            print(f"DRIFT {twin} — out of sync with {qmd}; run: "
                  f"python infra/ci/make_twin.py --write {qmd}")
        else:
            print(f"OK    {twin}")
    if drift:
        print(f"\n{drift} twin(s) out of sync with their chapter source")
        return 1
    print(f"\nAll {len(targets)} twin(s) match their source")
    return 0


def main(argv: list[str]) -> int:
    mode = "--check"
    rest = list(argv)
    if rest and rest[0] in ("--write", "--check"):
        mode = rest.pop(0)
    return cmd_write(rest) if mode == "--write" else cmd_check(rest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
