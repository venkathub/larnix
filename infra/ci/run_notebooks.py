#!/usr/bin/env python3
"""R10 gate — execute notebooks in CI and fail on any cell error (P0 task 8).

Per P0-D7 / DECISIONS D0006: standalone Jupyter `.ipynb` notebooks are executed
with `nbclient`. Any cell that raises fails the gate.

Browser (`compute: browser`) chapters run their `{pyodide}` cells client-side, so
they are *not* executed by a headless render. Their R10 guarantee comes from a
companion executable notebook (the "CI-executed twin", DECISIONS D0010) that lives
under `modules/` and is executed here like any other notebook.

Colab chapters (P2-D9 / DECISIONS D0020): their **generated companions**
(`make_colab.py`, notebook metadata `larnix.generated_by`) are executed here
**CPU-scaled** — `LARNIX_CI=1` is set so the companion's parameters cell picks
tiny epochs/subsets, exercise-cell sources are substituted with their
`metadata.larnix.solution`, rubric cells (`metadata.larnix.rubric`) are dropped
(human-graded), and each companion must finish within a wall-clock budget
(`LARNIX_NB_BUDGET_S`, default 90 s) or the gate fails with a "scale it down"
message. Hand-authored GPU/colab notebooks (no `larnix.generated_by`) keep the
D0012 policy: skipped here, manually Colab-verified and recorded in the PR.

Usage:
    python3 run_notebooks.py [PATH ...]

With no PATH, executes every `modules/**/*.ipynb`. Exit 0 = all executed cleanly
(or nothing to run); 1 = at least one notebook errored.
"""
from __future__ import annotations

import glob
import os
import sys
import time
from pathlib import Path

DEFAULT_GLOBS = ["modules/**/*.ipynb"]

# Hand-authored notebooks whose front-matter / metadata marks them as GPU/colab
# are NOT run in CI (no GPU runner). They are manually executed on Colab and
# recorded in the PR (the GPU-notebook policy, DECISIONS D0012). This reads
# either chapter front-matter `compute:` or notebook metadata `larnix.compute`.
_SKIP_COMPUTE = {"colab", "gpu"}

# Notebook metadata marking a generated Colab companion (make_colab.py, P2-D8).
_COMPANION_GENERATOR = "infra/ci/make_colab.py"

_DEFAULT_BUDGET_S = 90.0


def budget_s() -> float:
    """Wall-clock budget per scaled companion (P2-D9), env-overridable."""
    try:
        return float(os.environ.get("LARNIX_NB_BUDGET_S", _DEFAULT_BUDGET_S))
    except ValueError:
        return _DEFAULT_BUDGET_S


def _notebook_larnix(path) -> dict:
    """The notebook-level `metadata.larnix` block ({} if absent/unreadable)."""
    import json

    try:
        with open(path, encoding="utf-8") as fh:
            nb = json.loads(fh.read())
    except (OSError, json.JSONDecodeError):
        return {}
    return (nb.get("metadata") or {}).get("larnix") or {}


def _notebook_compute(path) -> str | None:
    # 1) Quarto-style YAML front-matter in a raw/markdown cell.
    try:
        from frontmatter_lint import extract_frontmatter

        fm = extract_frontmatter(path)
        if isinstance(fm, dict) and fm.get("compute"):
            return str(fm["compute"]).strip().lower()
    except Exception:  # noqa: BLE001
        pass
    # 2) Notebook-level metadata: {"metadata": {"larnix": {"compute": "colab"}}}.
    larnix = _notebook_larnix(path)
    if larnix.get("compute"):
        return str(larnix["compute"]).strip().lower()
    if larnix.get("ci") is False:
        return "colab"  # explicit opt-out
    return None


def classify(path) -> str:
    """One of "run" (plain/twin), "run-scaled" (generated companion), "skip"."""
    if _notebook_larnix(path).get("generated_by") == _COMPANION_GENERATOR:
        return "run-scaled"
    if _notebook_compute(path) in _SKIP_COMPUTE:
        return "skip"
    return "run"


def should_run(path) -> bool:
    return classify(path) != "skip"


def scale_companion(nb):
    """Apply the P2-D9 execution contract to a generated companion, in place.

    Rubric cells are dropped (human-graded, like the twins); exercise cells
    execute their embedded solution instead of the learner-facing starter.
    """
    kept = []
    for cell in nb.cells:
        larnix = (cell.get("metadata") or {}).get("larnix") or {}
        if cell.get("cell_type") == "code" and larnix:
            if larnix.get("rubric"):
                continue
            if larnix.get("solution") is not None:
                cell["source"] = larnix["solution"]
        kept.append(cell)
    nb.cells = kept
    return nb


def run_ipynb(path, timeout: int = 600, scaled: bool = False) -> tuple[bool, str | None]:
    """Execute one notebook with nbclient. Returns (ok, error_message).

    With ``scaled=True`` (generated companions, P2-D9): solutions substituted,
    rubric cells dropped, ``LARNIX_CI=1`` exported to the kernel, and the
    wall-clock budget (`budget_s()`) enforced.
    """
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    try:
        nb = nbformat.read(path, as_version=4)
    except Exception as e:  # noqa: BLE001 - report any read/parse failure
        return False, f"could not read notebook: {type(e).__name__}: {e}"

    saved_ci = os.environ.get("LARNIX_CI")
    if scaled:
        scale_companion(nb)
        os.environ["LARNIX_CI"] = "1"  # inherited by the spawned kernel

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(Path(path).parent)}},
    )
    start = time.monotonic()
    try:
        client.execute()
    except CellExecutionError as e:
        lines = [ln for ln in str(e).splitlines() if ln.strip()]
        return False, lines[-1] if lines else "CellExecutionError"
    except Exception as e:  # noqa: BLE001 - kernel/startup failures, etc.
        return False, f"{type(e).__name__}: {e}"
    finally:
        if scaled:
            if saved_ci is None:
                os.environ.pop("LARNIX_CI", None)
            else:
                os.environ["LARNIX_CI"] = saved_ci

    if scaled:
        elapsed = time.monotonic() - start
        if elapsed > budget_s():
            return False, (
                f"companion took {elapsed:.1f}s, over the {budget_s():.0f}s "
                "CPU-scaled budget (P2-D9) — shrink the LARNIX_CI branch of its "
                "parameters cell (fewer epochs / smaller subset)"
            )
    return True, None


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
        kind = classify(path)
        if kind == "skip":
            print(f"SKIP {path} (GPU/colab, hand-authored — manually Colab-verified, not run in CI; D0012)")
            continue
        ran += 1
        scaled = kind == "run-scaled"
        start = time.monotonic()
        ok, err = run_ipynb(path, scaled=scaled)
        note = f" (companion, CPU-scaled, {time.monotonic() - start:.1f}s)" if scaled else ""
        if ok:
            print(f"OK   {path}{note}")
        else:
            failed += 1
            print(f"FAIL {path}{note}")
            print(f"  - {err}")

    if failed:
        print(f"\n{failed} notebook(s) failed to execute")
        return 1
    print(f"\nAll {ran} executed notebook(s) ran cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
