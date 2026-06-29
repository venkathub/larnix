#!/usr/bin/env python3
"""R3 browser-import gate — `compute: browser` chapters must be Pyodide-safe (P0 task 11).

A chapter whose front-matter is `compute: browser` runs its code in the learner's
browser via Pyodide. This gate fails such a chapter if it imports a package that
is not Pyodide-safe, so a broken "zero-install" promise is caught at PR time.

Policy: strict allow-list = the Python standard library (`sys.stdlib_module_names`)
plus a curated Pyodide-safe set. A known-unsafe denylist gives a clearer message.
Anything unknown fails with guidance (add to the safe set, or use a colab chapter).

Runtime-installed pure-Python packages: a chapter that installs a pure-Python wheel
at runtime (`micropip.install("seaborn")`) and then imports it must **declare** that
import with a `# micropip: <name>[, <name>...]` annotation anywhere in its code. The
annotation exempts only the named module(s) — a bare, unannotated `import torch`
still fails, and a `KNOWN_UNSAFE` package (e.g. torch) fails even if annotated,
because it has no pure-Python wheel to micropip-install. This is the P1-D7 guard:
seaborn-by-`micropip` is allowed only when explicit and deliberate.

Usage:
    python3 browser_import_lint.py [PATH ...]
Exit 0 = pass (or nothing to check); 1 = a browser chapter imports something unsafe.
"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontmatter_lint import extract_frontmatter  # noqa: E402

# Annotation a chapter uses to declare a deliberately micropip-installed import.
_MICROPIP_RE = re.compile(r"#\s*micropip:\s*(.+)$", re.IGNORECASE)

# Curated Pyodide-safe import names (extend deliberately as chapters need them).
PYODIDE_SAFE = {
    "numpy", "pandas", "scipy", "matplotlib", "sklearn", "PIL", "sympy",
    "statsmodels", "networkx", "joblib", "threadpoolctl", "micropip",
    "pyodide", "js", "dateutil", "pytz", "six", "regex", "requests",  # pyodide ships a patched requests
    "lib",  # Larnix in-repo shared helpers (e.g. lib.grader), loaded into the VFS via `resources:` (P1-D9)
}
# Known-unsafe heavyweights — fail with a pointed message.
KNOWN_UNSAFE = {
    "torch": "PyTorch", "tensorflow": "TensorFlow", "transformers": "HF Transformers",
    "jax": "JAX", "jaxlib": "JAX", "keras": "Keras", "accelerate": "accelerate",
    "vllm": "vLLM", "tokenizers": "HF tokenizers", "datasets": "HF datasets",
    "sentencepiece": "sentencepiece", "xgboost": "XGBoost", "lightgbm": "LightGBM",
}

_STDLIB = set(getattr(sys, "stdlib_module_names", set()))

DEFAULT_GLOBS = ["modules/**/*.qmd", "modules/**/*.ipynb"]
_FENCE = re.compile(r"^(`{3,})(.*)$")


def _fence_lang(info: str) -> str:
    info = info.strip()
    if not info:
        return ""
    return info.split()[0].strip("{}").lower()


def extract_code(text: str, langs=("pyodide", "python")) -> str:
    """Concatenate the source of fenced code blocks whose language is in `langs`."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if m:
            lang = _fence_lang(m.group(2))
            j, buf = i + 1, []
            while j < len(lines) and not re.match(r"^`{3,}\s*$", lines[j]):
                buf.append(lines[j])
                j += 1
            if lang in langs:
                out.append("\n".join(buf))
            i = j + 1
        else:
            i += 1
    return "\n".join(out)


def imported_modules(code: str) -> set[str]:
    mods: set[str] = set()
    for raw in code.splitlines():
        s = raw.strip()
        if s.startswith("from "):
            m = re.match(r"from\s+([.\w]+)\s+import\b", s)
            if m:
                top = m.group(1).lstrip(".").split(".")[0]
                if top.isidentifier():
                    mods.add(top)
        elif s.startswith("import "):
            for part in s[len("import "):].split(","):
                name = part.strip().split(" as ")[0].strip().split(".")[0]
                if name.isidentifier():
                    mods.add(name)
    return mods


def micropip_declared(code: str) -> set[str]:
    """Module names a chapter explicitly declares as runtime-`micropip`-installed.

    Recognises `# micropip: name1, name2` annotation lines anywhere in the code.
    """
    declared: set[str] = set()
    for raw in code.splitlines():
        m = _MICROPIP_RE.search(raw)
        if m:
            for part in m.group(1).split(","):
                name = part.strip().split(".")[0].split(" ")[0]
                if name.isidentifier():
                    declared.add(name)
    return declared


def check_imports(modules, micropip_allowed=frozenset()) -> list[str]:
    problems = []
    for mod in sorted(modules):
        if mod in _STDLIB or mod in PYODIDE_SAFE:
            continue
        if mod in KNOWN_UNSAFE:
            # A heavyweight C-extension package: never micropip-installable, so a
            # `# micropip:` annotation cannot rescue it.
            problems.append(
                f"imports '{mod}' ({KNOWN_UNSAFE[mod]}) — not Pyodide-safe; "
                f"use a colab/gpu chapter or a Pyodide-safe alternative"
            )
        elif mod in micropip_allowed:
            # Declared as a deliberate runtime micropip install (pure-Python wheel).
            continue
        else:
            problems.append(
                f"imports '{mod}', which is not on the Pyodide-safe allow-list; "
                f"if it runs in Pyodide add it to PYODIDE_SAFE, if it is a pure-Python "
                f"package installed at runtime annotate it with `# micropip: {mod}`, "
                f"otherwise use a colab chapter"
            )
    return problems


def check_file(path: str) -> list[str]:
    fm = extract_frontmatter(path)
    if not isinstance(fm, dict) or fm.get("compute") != "browser":
        return []
    if path.endswith(".ipynb"):
        import json

        try:
            with open(path, encoding="utf-8") as fh:
                nb = json.loads(fh.read())
        except (OSError, json.JSONDecodeError):
            return [f"{path}: could not read notebook"]
        code = "\n".join(
            "".join(c.get("source", "")) if isinstance(c.get("source"), list) else c.get("source", "")
            for c in nb.get("cells", [])
            if c.get("cell_type") == "code"
        )
    else:
        with open(path, encoding="utf-8") as fh:
            code = extract_code(fh.read())
    return check_imports(imported_modules(code), micropip_declared(code))


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
        print("browser-import-lint (R3): no chapters found; nothing to check")
        return 0
    failed = 0
    for path in targets:
        problems = check_file(path)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK   {path}")
    if failed:
        print(f"\n{failed} browser chapter(s) import non-Pyodide-safe packages")
        return 1
    print(f"\nAll {len(targets)} chapter(s) Pyodide-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
