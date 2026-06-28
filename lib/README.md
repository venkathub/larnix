# lib — shared grader & notebook helpers

Reusable utilities for exercises and notebooks. Pyodide-safe (standard library
only) so they run unchanged in the browser and in CPython tests.

| File | Purpose |
|------|---------|
| `grader.py` | In-browser **assert-grader** helper: `run_tests([(label, got, expected), …])` with a consistent pass/fail UX (`All N tests passed ✅`) and float tolerance. |
| `data.py` | **Vendored-dataset loader** (P1-D8): `load_csv("penguins")` reads `data/<name>.csv` relative to the cwd (the module dir) — identical in the Pyodide VFS and the CPython twin. pandas is imported lazily. Chapters declare the CSV (and `pandas`) in front-matter — see the docstring. |
| `test_grader.py` | CPython unit tests for `grader.py` (run the grading logic off-browser). |
| `test_data.py` | CPython unit tests for `data.py` (path helpers always; the pandas round-trip when pandas is present). |

## The auto-grading approach (P0-D5, see DECISIONS D0009)

Larnix auto-graded exercises use **`run_tests` inside plain `{pyodide}` cells**.
This is the spec's V-1-safe path: the grading logic is plain Python, so it is
**unit-tested in CPython here** (deterministic, off-browser evidence) and then
runs identically in the learner's browser via Pyodide.

In a chapter, **single-source** the helper (P1-D9 / DECISIONS D0016) — do not
paste it. Add it to the page front-matter so quarto-live copies it into the
Pyodide VFS at startup:

```yaml
resources:
  - ../../lib/grader.py        # path relative to the chapter; lands at lib/grader.py in the VFS
```

Then, because each `#| exercise:` widget runs in its **own** environment, give
every exercise a one-line `setup` cell that imports the grader:

````markdown
```{pyodide}
#| setup: true
#| exercise: ex_accuracy
from lib.grader import run_tests
```
````

…after which the exercise (and its solution) can call:

```python
run_tests([
    ("all correct", accuracy([1, 1], [1, 1]), 1.0),
    ("half right",  accuracy([1, 0], [1, 1]), 0.5),
])
```

On failure it prints each result and raises `AssertionError`, so the cell shows
an error. Hidden solutions use the `<details>` pattern from `CHAPTER_TEMPLATE.md`.
This was verified in-browser on M0 Ch1 (see DECISIONS D0016 implementation note).

quarto-live's **native** exercise widget (editor + hint + solution + a `check:`
grader) is also available and demonstrated in `sandbox-exercise.qmd §B`;
its Python `check`-cell contract is browser-only to verify and under-documented,
so it is reserved for richer UX, not the default grader.

## Run the tests

```bash
cd lib && python3 -m unittest -v
```
