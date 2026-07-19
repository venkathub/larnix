"""Vendored-dataset loader for Larnix chapters (P1-D8 / DECISIONS D0016).

Datasets are vendored in-repo next to the chapters that use them, at
``data/<name>.csv`` inside the module directory. This loader reads that path
**relative to the current working directory**, which is the chapter's module
directory both in the browser (the CSV is copied into the Pyodide VFS via the
page's ``resources:`` key) and in the CPython twin (executed with cwd = the
module dir). So ``load_csv("penguins")`` works unchanged in both places —
offline, ₹0, and deterministic (no runtime network fetch).

Usage in a chapter::

    # front-matter:
    #   pyodide:
    #     packages: [pandas]          # preload — see note below
    #     resources:
    #       - ../../lib/data.py
    #       - data/penguins.csv
    from lib.data import load_csv
    df = load_csv("penguins")

**Preload note.** quarto-live auto-loads only the packages it sees imported *in a
cell*. Because pandas is imported lazily *inside this module*, a chapter that uses
``load_csv`` without also writing ``import pandas`` must declare
``pyodide: packages: [pandas]`` in its front-matter, or pandas won't be loaded in
the browser. (Most EDA chapters import pandas directly anyway.)

Pyodide-safe: pandas is a Pyodide built-in. The import is lazy so the stdlib
path helpers stay usable (and testable) without pandas installed.
"""
from __future__ import annotations

from pathlib import Path

DATA_DIR = "data"


def dataset_path(name: str) -> Path:
    """Return the vendored CSV path ``data/<name>.csv`` (relative to cwd).

    ``name`` must be a bare dataset name with no path separators.
    """
    if not name or "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"invalid dataset name: {name!r}")
    return Path(DATA_DIR) / f"{name}.csv"


def load_csv(name: str, **read_csv_kwargs):
    """Load a vendored dataset as a pandas ``DataFrame`` (pandas imported lazily)."""
    path = dataset_path(name)
    if not path.exists():
        raise FileNotFoundError(
            f"dataset {name!r} not found at '{path}'. Datasets are vendored at "
            f"data/<name>.csv in the module directory; run from the chapter's "
            f"directory, and for browser chapters declare the CSV in the page "
            f"`resources:` so it is loaded into the Pyodide filesystem."
        )
    import pandas as pd  # lazy: Pyodide built-in; not needed for the path helpers

    return pd.read_csv(path, **read_csv_kwargs)
