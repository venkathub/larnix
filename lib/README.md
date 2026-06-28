# lib — shared grader & notebook helpers

Reusable utilities for exercises and notebooks. Pyodide-safe (standard library
only) so they run unchanged in the browser and in CPython tests.

| File | Purpose |
|------|---------|
| `grader.py` | In-browser **assert-grader** helper: `run_tests([(label, got, expected), …])` with a consistent pass/fail UX (`All N tests passed ✅`) and float tolerance. |
| `test_grader.py` | CPython unit tests for `grader.py` (run the grading logic off-browser). |

## The auto-grading approach (P0-D5, see DECISIONS D0009)

Larnix auto-graded exercises use **`run_tests` inside plain `{pyodide}` cells**.
This is the spec's V-1-safe path: the grading logic is plain Python, so it is
**unit-tested in CPython here** (deterministic, off-browser evidence) and then
runs identically in the learner's browser via Pyodide.

In a chapter, paste the helper into a `#| edit: false` setup cell (or, later,
load `lib/grader.py` into the Pyodide VFS), then:

```python
run_tests([
    ("all correct", accuracy([1, 1], [1, 1]), 1.0),
    ("half right",  accuracy([1, 0], [1, 1]), 0.5),
])
```

On failure it prints each result and raises `AssertionError`, so the cell shows
an error. Hidden solutions use the `<details>` pattern from `CHAPTER_TEMPLATE.md`.

quarto-live's **native** exercise widget (editor + hint + solution + a `check:`
grader) is also available and demonstrated in `site/sandbox-exercise.qmd §B`;
its Python `check`-cell contract is browser-only to verify and under-documented,
so it is reserved for richer UX, not the default grader.

## Run the tests

```bash
cd lib && python3 -m unittest -v
```
