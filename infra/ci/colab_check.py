#!/usr/bin/env python3
"""Colab-policy gate (P2 §5.3 / DECISIONS D0020) — fail closed on any
`compute: colab` chapter whose free-GPU surface is broken.

For every `compute: colab` chapter under `modules/` this checks, in one place,
everything a learner's "Open in Colab" click depends on:

  (a) **Button ↔ notebook** — exactly one `{{< colab … >}}` shortcode, whose
      path is the chapter's own generated companion (`<stem>-colab.ipynb`,
      repo-relative), and that file exists.
  (b) **Companion drift** — the committed companion byte-matches what
      `make_colab.py` generates from the chapter today (single-sourced: this
      calls `make_colab.notebook_text`, it does not reimplement generation).
  (c) **Parameters cell** — the *committed* companion (not just the source)
      carries the `LARNIX_CI` parameters cell, so a hand-edited notebook cannot
      dodge the CPU-scaled CI tier (P2-D9).
  (d) **Torch guard** — a companion that imports torch must carry the
      version-floor guard cell (P2-D11).

And the inverse: a **non-colab** chapter carrying a `{{< colab >}}` button is an
error — browser chapters must stay ₹0 with no Colab surface (the P2 DoD's
"no Colab surface in M4" rule).

Usage:
    python3 colab_check.py [PATH ...]      # default: modules/**/*.qmd

Exit 0 = every chapter passes (or none to check); 1 = at least one violation.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter_lint import extract_frontmatter  # noqa: E402
from make_colab import companion_path, companion_relpath, notebook_text  # noqa: E402

DEFAULT_GLOBS = ["modules/**/*.qmd"]

_SHORTCODE_RE = re.compile(r"\{\{<\s*colab\s+([^>\s]+)\s*>\}\}")
_TORCH_RE = re.compile(r"^\s*(import torch\b|from torch\b)", re.M)


def _read_companion(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _code_cells(nb: dict) -> list[dict]:
    return [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]


def _cell_source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def check_chapter(qmd_path: str) -> list[str]:
    """All policy violations for one chapter (empty list = pass)."""
    p = Path(qmd_path)
    text = p.read_text(encoding="utf-8")
    fm = extract_frontmatter(qmd_path)
    compute = (fm or {}).get("compute")
    buttons = _SHORTCODE_RE.findall(text)

    if compute != "colab":
        if buttons:
            return [
                f"{qmd_path}: `compute: {compute}` chapter has a {{{{< colab >}}}} "
                "button — non-colab chapters must stay browser-only (₹0, no Colab "
                "surface; P2 DoD)"
            ]
        return []

    errors: list[str] = []

    # (a) button ↔ notebook
    expected_rel = companion_relpath(qmd_path)
    if len(buttons) != 1:
        errors.append(
            f"{qmd_path}: expected exactly one {{{{< colab >}}}} button, found "
            f"{len(buttons)}"
        )
    elif buttons[0] != expected_rel:
        errors.append(
            f"{qmd_path}: colab button points at '{buttons[0]}', expected the "
            f"generated companion '{expected_rel}'"
        )
    companion = companion_path(qmd_path)
    if not companion.exists():
        errors.append(
            f"{qmd_path}: companion {companion} missing — run: "
            f"python infra/ci/make_colab.py --write {qmd_path}"
        )
        return errors  # (b)–(d) need the file

    # (b) drift (single-sourced against the generator)
    try:
        expected = notebook_text(qmd_path)
    except ValueError as e:
        errors.append(f"{qmd_path}: companion cannot be regenerated — {e}")
        expected = None
    if expected is not None and companion.read_text(encoding="utf-8") != expected:
        errors.append(
            f"{qmd_path}: companion {companion} drifted from the chapter — run: "
            f"python infra/ci/make_colab.py --write {qmd_path}"
        )

    nb = _read_companion(companion)
    if nb is None:
        errors.append(f"{qmd_path}: companion {companion} is not valid JSON")
        return errors
    cells = _code_cells(nb)

    # (c) LARNIX_CI parameters cell present in the committed notebook
    if not any(
        c.get("id") == "parameters" and "LARNIX_CI" in _cell_source(c) for c in cells
    ):
        errors.append(
            f"{qmd_path}: companion {companion} has no LARNIX_CI parameters cell "
            "(P2-D9) — regenerate it; do not hand-edit companions"
        )

    # (d) torch guard cell when torch is used
    uses_torch = any(_TORCH_RE.search(_cell_source(c)) for c in cells)
    has_guard = any(
        c.get("id") == "torch-guard" and "torch.__version__" in _cell_source(c)
        for c in cells
    )
    if uses_torch and not has_guard:
        errors.append(
            f"{qmd_path}: companion {companion} imports torch but has no "
            "version-floor guard cell (P2-D11) — declare `torch-floor:` in the "
            "chapter front-matter and regenerate"
        )
    return errors


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


def main(argv: list[str]) -> int:
    targets = _collect(argv)
    if not targets:
        print("colab-check: no chapters found; nothing to check")
        return 0
    failures = 0
    checked = 0
    for qmd in targets:
        fm = extract_frontmatter(qmd)
        is_colab = isinstance(fm, dict) and fm.get("compute") == "colab"
        errs = check_chapter(qmd)
        if is_colab:
            checked += 1
        if errs:
            failures += len(errs)
            for e in errs:
                print(f"FAIL {e}")
        elif is_colab:
            print(f"OK   {qmd}")
    if failures:
        print(f"\n{failures} colab-policy violation(s)")
        return 1
    print(f"\nAll {checked} colab chapter(s) pass the colab policy"
          if checked else "\ncolab-check: no colab chapters; nothing to check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
