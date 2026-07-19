#!/usr/bin/env python3
"""Colab companion generator (P2-D8 / DECISIONS D0020) — build & verify the
learner-facing `.ipynb` for every `compute: colab` chapter.

A colab chapter is a rendered `.qmd` (prose + code shown with recorded outputs;
nothing executes at render time) plus a **companion notebook** the learner opens
via the P0 `{{< colab >}}` button. Two artifacts invite drift — the exact class
P1-D10 killed for browser twins — so the companion is **derived** from the
chapter source and a CI `--check` fails if a committed companion no longer
matches.

Authoring convention (documented in infra/ci/README.md):
  Code destined for the companion lives in *Pandoc-attribute* fences —
  ```{.python} — which Quarto renders as highlighted, non-executed code (the
  render gate installs no Jupyter, so executable `{python}` cells are not an
  option). Fence attributes (invisible to the learner) assign roles:

    ```{.python}                        → worked cell, copied in document order
    ```{.python setup="true"}           → dropped (the generated grader bootstrap replaces it)
    ```{.python companion="false"}      → display-only; never copied
    ```{.python parameters="true"}      → the LARNIX_CI parameters cell (exactly one; P2-D9)
    ```{.python exercise="ex_id"}       → exercise starter; paired with the next
                                          <details> solution (P1 pattern)

  Plain ```python fences (e.g. inside <details> solutions) are prose, never cells.

Fail-closed rules (build errors, never silent):
  - exactly one parameters cell, and it must reference LARNIX_CI;
  - any torch-importing chapter must declare `torch-floor:` front-matter
    (emitted as the P2-D11 version-floor guard cell);
  - an auto-graded exercise (calls run_tests) must have a <details> solution.

Companion structure: front-matter raw cell → header (badge; generated-do-not-
edit note) → torch guard → parameters → grader bootstrap (repo raw-URL fetch
with an inlined fallback embedded at generation time — so a grader change
drifts every companion and the gate forces regeneration) → worked + exercise
cells. Exercise cells carry `metadata.larnix.solution` so the CI runner
(P2-D9) can substitute solutions when executing the scaled notebook; rubric
exercises (no run_tests) carry `metadata.larnix.rubric` instead and are
skipped by CI.

Usage:
    python3 make_colab.py --write [PATH ...]   # (re)generate companions (default: all colab chapters)
    python3 make_colab.py --check [PATH ...]   # fail if a committed companion differs from source
With no PATH, scans modules/**/*.qmd. A companion is `<chapter-stem>-colab.ipynb`.
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
from make_twin import (  # noqa: E402  (single-source the shared plumbing)
    TWIN_FIELDS,
    _DETAILS_RE,
    _as_source,
    _code_cell,
    _md_cell,
    _raw_cell,
    _run_tests_block,
    _solution_code,
    _yaml_list,
    _yaml_scalar,
)

DEFAULT_GLOBS = ["modules/**/*.qmd"]

# A Pandoc-attribute python fence: ```{.python key="value" ...}
_FENCE_RE = re.compile(r"^```\{\.python([^}\n]*)\}[ \t]*\n(.*?)\n```", re.S | re.M)
_ATTR_RE = re.compile(r'([\w-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+))')

_COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"


# ── config (never hardcode the repo — CLAUDE.md) ────────────────────────────
def colab_target() -> tuple[str, str]:
    """(repo, branch) for badge + raw URLs: _quarto.yml first, env fallback."""
    repo = branch = None
    cfg = Path("_quarto.yml")
    if cfg.exists():
        try:
            import yaml

            meta = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
            repo = meta.get("larnix-colab-repo")
            branch = meta.get("larnix-colab-branch")
        except Exception:  # noqa: BLE001 - fall through to env/defaults
            pass
    repo = repo or os.environ.get("LARNIX_COLAB_REPO") or "OWNER/REPO"
    branch = branch or os.environ.get("LARNIX_COLAB_BRANCH") or "main"
    return str(repo), str(branch)


def _grader_source() -> str:
    """The single-sourced grader, inlined as the bootstrap's offline fallback."""
    root = Path(__file__).resolve().parent.parent.parent
    return (root / "lib" / "grader.py").read_text(encoding="utf-8")


# ── source parsing ──────────────────────────────────────────────────────────
def _parse_attrs(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _ATTR_RE.finditer(raw):
        out[m.group(1)] = m.group(2) or m.group(3) or m.group(4) or ""
    return out


def _is_true(v: str | None) -> bool:
    return str(v).strip().lower() == "true"


def parse_chapter(text: str, source: str = "<chapter>") -> dict:
    """Extract companion cells from a colab chapter.

    Returns {"parameters": str, "cells": [{"kind", "id", "code", ...}]} where
    cells are worked/exercise items in document order. Raises ValueError on any
    fail-closed rule (see module docstring).
    """
    events: list[tuple[int, str, object]] = []
    for m in _FENCE_RE.finditer(text):
        events.append((m.start(), "cell", (m.group(1), m.group(2))))
    for m in _DETAILS_RE.finditer(text):
        events.append((m.start(), "sol", m.group(0)))
    events.sort(key=lambda e: e[0])

    parameters: list[str] = []
    cells: list[dict] = []
    worked_n = 0
    pending: dict | None = None  # an exercise awaiting its <details> solution

    for _pos, kind, payload in events:
        if kind == "cell":
            attrs_raw, body = payload  # type: ignore[misc]
            attrs = _parse_attrs(str(attrs_raw))
            body = str(body).strip("\n")
            if _is_true(attrs.get("companion")) is False and "companion" in attrs:
                continue  # companion="false" → display-only
            if _is_true(attrs.get("setup")):
                continue  # replaced by the generated grader bootstrap
            if _is_true(attrs.get("parameters")):
                parameters.append(body)
                continue
            if "exercise" in attrs:
                if pending is not None and pending["graded"]:
                    raise ValueError(
                        f"{source}: auto-graded exercise '{pending['id']}' has no "
                        "<details> solution before the next exercise"
                    )
                pending = {
                    "id": attrs["exercise"],
                    "code": body,
                    "graded": _run_tests_block(body) is not None,
                }
                cells.append({
                    "kind": "exercise",
                    "id": f"ex-{pending['id']}",
                    "exercise": pending["id"],
                    "code": body,
                    "solution": None,
                    "graded": pending["graded"],
                })
                continue
            worked_n += 1
            cells.append({"kind": "worked", "id": f"worked-{worked_n}", "code": body})
        elif kind == "sol" and pending is not None:
            details = str(payload)
            sol = _solution_code(_DETAILS_RE.search(details).group(1))  # type: ignore[union-attr]
            if sol is None:
                continue  # a hint <details> with no code (P1-D4) — keep waiting
            for c in reversed(cells):
                if c["kind"] == "exercise" and c["exercise"] == pending["id"]:
                    c["solution"] = sol
                    cells.append({
                        "kind": "solution",
                        "id": f"sol-{pending['id']}",
                        "markdown": details.strip(),
                    })
                    break
            pending = None

    if pending is not None and pending["graded"]:
        raise ValueError(
            f"{source}: auto-graded exercise '{pending['id']}' has no <details> solution"
        )
    if len(parameters) != 1:
        raise ValueError(
            f"{source}: expected exactly one parameters cell "
            f'(```{{.python parameters="true"}}), found {len(parameters)} (P2-D9)'
        )
    if "LARNIX_CI" not in parameters[0]:
        raise ValueError(
            f"{source}: the parameters cell must honour the LARNIX_CI env var (P2-D9)"
        )
    return {"parameters": parameters[0], "cells": cells}


def _uses_torch(parsed: dict) -> bool:
    code = "\n".join(
        c.get("code", "") for c in parsed["cells"] if c["kind"] != "solution"
    ) + "\n" + parsed["parameters"]
    return bool(re.search(r"^\s*(import torch\b|from torch\b)", code, re.M))


# ── cell builders ───────────────────────────────────────────────────────────
def _frontmatter_lines(fm: dict) -> list[str]:
    lines = ["---"]
    for field in TWIN_FIELDS:
        val = fm.get(field)
        if field == "title":
            val = f"{val} (Colab companion)"
        if isinstance(val, list):
            lines.extend(_yaml_list(field, val))
        else:
            lines.append(_yaml_scalar(field, val))
    lines.append("---")
    return lines


def _header_md(fm: dict, name: str, badge_url: str) -> str:
    return (
        f"# {fm.get('title')}\n\n"
        f"[![Open in Colab]({_COLAB_BADGE})]({badge_url})\n\n"
        f"**Colab companion of `{name}`.** Generated by `infra/ci/make_colab.py` "
        "(P2-D8); do not edit by hand — edit the chapter and regenerate. "
        "Run cells top to bottom; exercises grade themselves with `run_tests`. "
        "Free tier is enough: Runtime → Change runtime type → **T4 GPU** (₹0)."
    )


def _torch_guard(floor: str) -> str:
    return (
        "# Torch version-floor guard (P2-D11): Colab preinstalls torch and rolls it\n"
        "# forward, so we assert a floor rather than pin an exact version.\n"
        "import torch\n\n"
        "def _ver(v):\n"
        '    return tuple(int("".join(ch for ch in p if ch.isdigit()) or 0)\n'
        '                 for p in v.split("+")[0].split(".")[:3])\n\n'
        f'_FLOOR = "{floor}"\n'
        "assert _ver(torch.__version__) >= _ver(_FLOOR), (\n"
        f'    f"This notebook needs torch >= {{_FLOOR}}, but this runtime has "\n'
        '    f"{torch.__version__}. In Colab try Runtime -> Disconnect and delete '
        'runtime, then reconnect; if it persists, please open an issue."\n'
        ")\n"
        'print(f"torch {torch.__version__} (floor {_FLOOR}) OK")'
    )


def _grader_bootstrap(repo: str, branch: str) -> str:
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/lib/grader.py"
    fallback = _grader_source()
    if "'''" in fallback:  # keep the r'''…''' embedding safe against grader edits
        raise ValueError("lib/grader.py may not contain ''' (breaks the inlined fallback)")
    return (
        "# Larnix grader bootstrap (single-sourced — P1-D9/P2-D8). Colab has no\n"
        "# quarto-live VFS, so fetch lib/grader.py from the repo (Colab is online);\n"
        "# offline or in CI, use the inlined copy embedded at generation time.\n"
        f"_LARNIX_GRADER_FALLBACK = r'''{fallback}'''\n\n"
        "import os, pathlib\n"
        'pathlib.Path("lib").mkdir(exist_ok=True)\n'
        "_fetched = False\n"
        'if not os.environ.get("LARNIX_CI"):\n'
        "    try:\n"
        "        import urllib.request\n"
        f'        with urllib.request.urlopen("{url}", timeout=10) as _r:\n'
        '            pathlib.Path("lib/grader.py").write_bytes(_r.read())\n'
        "        _fetched = True\n"
        "    except Exception:\n"
        "        pass\n"
        "if not _fetched:\n"
        '    pathlib.Path("lib/grader.py").write_text(_LARNIX_GRADER_FALLBACK)\n'
        "from lib.grader import run_tests, between, decreased, changed, grad_check\n"
        'print("Larnix grader ready" + (" (fetched)" if _fetched else " (inlined copy)"))'
    )


def _exercise_cell(item: dict) -> dict:
    cell = _code_cell(item["id"], item["code"])
    larnix: dict = {"exercise": item["exercise"]}
    if item["solution"] is not None:
        larnix["solution"] = item["solution"]
    if not item["graded"]:
        larnix["rubric"] = True
    cell["metadata"]["larnix"] = larnix
    return cell


# ── notebook assembly ───────────────────────────────────────────────────────
def build_notebook(qmd_path: str) -> dict:
    text = Path(qmd_path).read_text(encoding="utf-8")
    fm = extract_frontmatter(qmd_path)
    if not isinstance(fm, dict):
        raise ValueError(f"{qmd_path}: no front-matter")
    parsed = parse_chapter(text, source=str(qmd_path))

    torch_floor = fm.get("torch-floor")
    if _uses_torch(parsed) and not torch_floor:
        raise ValueError(
            f"{qmd_path}: imports torch but declares no `torch-floor:` "
            "front-matter (P2-D11 version-floor guard)"
        )

    repo, branch = colab_target()
    name = Path(qmd_path).name
    badge_url = (
        f"https://colab.research.google.com/github/{repo}/blob/{branch}/"
        f"{companion_relpath(qmd_path)}"
    )

    cells = [
        _raw_cell("frontmatter", "\n".join(_frontmatter_lines(fm))),
        _md_cell("colab-header", _header_md(fm, name, badge_url)),
    ]
    if torch_floor:
        cells.append(_code_cell("torch-guard", _torch_guard(str(torch_floor))))
    cells.append(_code_cell("parameters", parsed["parameters"]))
    cells.append(_code_cell("grader-bootstrap", _grader_bootstrap(repo, branch)))
    for item in parsed["cells"]:
        if item["kind"] == "worked":
            cells.append(_code_cell(item["id"], item["code"]))
        elif item["kind"] == "exercise":
            cells.append(_exercise_cell(item))
        elif item["kind"] == "solution":
            cells.append(_md_cell(item["id"], item["markdown"]))

    return {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "larnix": {"compute": "colab", "generated_by": "infra/ci/make_colab.py"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def notebook_text(qmd_path: str) -> str:
    return json.dumps(build_notebook(qmd_path), indent=1, ensure_ascii=False) + "\n"


# ── CLI (mirrors make_twin.py) ──────────────────────────────────────────────
def companion_path(qmd_path: str) -> Path:
    p = Path(qmd_path)
    return p.with_name(p.stem + "-colab.ipynb")


def companion_relpath(qmd_path: str) -> str:
    """Companion path relative to the repo root (for the badge deep-link)."""
    p = companion_path(qmd_path)
    try:
        return p.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def _is_colab_chapter(qmd_path: str) -> bool:
    fm = extract_frontmatter(qmd_path)
    return isinstance(fm, dict) and fm.get("compute") == "colab"


def _has_cells(qmd_path: str) -> bool:
    return bool(_FENCE_RE.search(Path(qmd_path).read_text(encoding="utf-8")))


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
    return [p for p in _collect(args) if _is_colab_chapter(p) and _has_cells(p)]


def cmd_write(args: list[str]) -> int:
    targets = _targets(args)
    if not targets:
        print("make-colab: no colab chapters with companion cells found")
        return 0
    errors = 0
    for qmd in targets:
        try:
            out = companion_path(qmd)
            out.write_text(notebook_text(qmd), encoding="utf-8")
            print(f"WROTE {out}")
        except ValueError as e:
            errors += 1
            print(f"ERROR {e}")
    if errors:
        print(f"\n{errors} chapter(s) failed fail-closed checks")
        return 1
    print(f"\nGenerated {len(targets)} companion(s)")
    return 0


def cmd_check(args: list[str]) -> int:
    targets = _targets(args)
    if not targets:
        print("make-colab --check: no colab chapters with companion cells found")
        return 0
    bad = 0
    for qmd in targets:
        out = companion_path(qmd)
        try:
            expected = notebook_text(qmd)
        except ValueError as e:
            bad += 1
            print(f"ERROR {e}")
            continue
        if not out.exists():
            bad += 1
            print(f"MISSING {out} — run: python infra/ci/make_colab.py --write {qmd}")
        elif out.read_text(encoding="utf-8") != expected:
            bad += 1
            print(f"DRIFT {out} — out of sync with {qmd}; run: "
                  f"python infra/ci/make_colab.py --write {qmd}")
        else:
            print(f"OK    {out}")
    if bad:
        print(f"\n{bad} companion(s) out of sync or invalid")
        return 1
    print(f"\nAll {len(targets)} companion(s) match their source")
    return 0


def main(argv: list[str]) -> int:
    mode = "--check"
    rest = list(argv)
    if rest and rest[0] in ("--write", "--check"):
        mode = rest.pop(0)
    return cmd_write(rest) if mode == "--write" else cmd_check(rest)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
