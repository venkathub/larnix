#!/usr/bin/env python3
"""R10 gate — execute notebooks in CI and fail on any cell error (P0 task 8).

Per P0-D7 / DECISIONS D0006: standalone Jupyter `.ipynb` notebooks are executed
with `nbclient`. Any cell that raises fails the gate.

Browser (`compute: browser`) chapters run their `{pyodide}` cells client-side, so
they are *not* executed by a headless render. Their R10 guarantee comes from a
companion executable notebook (the "CI-executed twin", DECISIONS D0010) that lives
under `modules/` and is executed here like any other notebook.

Usage:
    python3 run_notebooks.py [PATH ...]

With no PATH, executes every `modules/**/*.ipynb`. Exit 0 = all executed cleanly
(or nothing to run); 1 = at least one notebook errored.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

DEFAULT_GLOBS = ["modules/**/*.ipynb"]

# Notebooks whose front-matter / metadata marks them as GPU/colab are NOT run in
# CI (no GPU runner). They are manually executed on Colab and recorded in the PR
# (the GPU-notebook policy, DECISIONS D0012). This reads either chapter
# front-matter `compute:` or notebook metadata `larnix.compute`.
_SKIP_COMPUTE = {"colab", "gpu"}


def _notebook_compute(path) -> str | None:
    import json

    # 1) Quarto-style YAML front-matter in a raw/markdown cell.
    try:
        from frontmatter_lint import extract_frontmatter

        fm = extract_frontmatter(path)
        if isinstance(fm, dict) and fm.get("compute"):
            return str(fm["compute"]).strip().lower()
    except Exception:  # noqa: BLE001
        pass
    # 2) Notebook-level metadata: {"metadata": {"larnix": {"compute": "colab"}}}.
    try:
        with open(path, encoding="utf-8") as fh:
            nb = json.loads(fh.read())
        larnix = (nb.get("metadata") or {}).get("larnix") or {}
        if larnix.get("compute"):
            return str(larnix["compute"]).strip().lower()
        if larnix.get("ci") is False:
            return "colab"  # explicit opt-out
    except (OSError, json.JSONDecodeError):
        pass
    return None


def should_run(path) -> bool:
    return _notebook_compute(path) not in _SKIP_COMPUTE


def run_ipynb(path, timeout: int = 600) -> tuple[bool, str | None]:
    """Execute one notebook with nbclient. Returns (ok, error_message)."""
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    try:
        nb = nbformat.read(path, as_version=4)
    except Exception as e:  # noqa: BLE001 - report any read/parse failure
        return False, f"could not read notebook: {type(e).__name__}: {e}"

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(Path(path).parent)}},
    )
    try:
        client.execute()
        return True, None
    except CellExecutionError as e:
        lines = [ln for ln in str(e).splitlines() if ln.strip()]
        return False, lines[-1] if lines else "CellExecutionError"
    except Exception as e:  # noqa: BLE001 - kernel/startup failures, etc.
        return False, f"{type(e).__name__}: {e}"


def collect_targets(args: list[str]) -> list[str]:
    if args:
        targets: list[str] = []
        for a in args:
            if glob.has_magic(a):
                # A glob pattern: expand it (possibly to nothing).
                targets.extend(glob.glob(a, recursive=True))
            else:
                # A literal path: keep as-is (a missing file errors on read).
                targets.append(a)
    else:
        targets = []
        for pattern in DEFAULT_GLOBS:
            targets.extend(glob.glob(pattern, recursive=True))
    # Never execute checkpoint copies.
    targets = [t for t in targets if ".ipynb_checkpoints" not in t]
    return sorted(set(targets))


def main(argv: list[str]) -> int:
    targets = collect_targets(argv)
    if not targets:
        print("run-notebooks: no notebooks found; nothing to execute")
        return 0

    failed = 0
    ran = 0
    for path in targets:
        if not should_run(path):
            print(f"SKIP {path} (GPU/colab — manually Colab-verified, not run in CI)")
            continue
        ran += 1
        ok, err = run_ipynb(path)
        if ok:
            print(f"OK   {path}")
        else:
            failed += 1
            print(f"FAIL {path}")
            print(f"  - {err}")

    if failed:
        print(f"\n{failed} notebook(s) failed to execute")
        return 1
    print(f"\nAll {ran} executed notebook(s) ran cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
