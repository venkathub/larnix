# lib — shared grader & notebook helpers

Reusable utilities for exercises and notebooks. Pyodide-safe (standard library
only) so they run unchanged in the browser and in CPython tests.

| File | Purpose |
|------|---------|
| `grader.py` | In-browser **assert-grader** helper: `run_tests([(label, got, expected), …])` with a consistent pass/fail UX (`All N tests passed ✅`) and float tolerance — plus the **property-based check-builders** for stochastic training (`between`, `decreased`, `changed`, `grad_check` — P2-D7, DECISIONS D0020). |
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

## The two grading modes for training exercises (P2-D7, DECISIONS D0020)

Training a model is stochastic — identical code gives different weights per
run — so P2+ exercises grade in one of two explicit modes, **chosen by the
chapter's `compute:` tier**. Every auto-graded training exercise states in
prose which mode grades it.

### 1. Seeded-deterministic (`compute: browser` chapters and CPU twins)

Pin every source of randomness at the top of the exercise, then grade with
ordinary `(label, got, expected)` tuples and the existing `tol`. Same seed +
pinned runtime ⇒ same result, and the CI twin proves it.

```python
import random
random.seed(0)                      # stdlib
import numpy as np
np.random.seed(0)                   # numpy (browser chapters)
# torch chapters (CPU twins only — never asserted bit-exact on GPU):
# torch.manual_seed(0); torch.use_deterministic_algorithms(True)
```

Conventions: seed **before** any data shuffle/init, pass `random_state=` to
every sklearn API that accepts one, and never assert bit-exactness on values a
compliant learner run could legitimately vary.

### 2. Property-based (`compute: colab` / GPU chapters)

GPU nondeterminism (cuDNN kernels, atomics, image drift) makes bit-exactness a
lie, so assert *properties of a successful training run* instead, using the
check-builders — they drop straight into `run_tests` and mix freely with
classic tuples:

```python
run_tests([
    between("test accuracy", acc, 0.95, 1.0),                    # bounds inclusive
    decreased("training loss", first_loss, final_loss, min_drop=0.80),
    changed("weights updated", w_before, w_after),               # params actually moved
    grad_check("dL/dw", loss_fn, w, analytic_grad),              # vs finite differences
])
```

- `between(label, value, low, high)` — `low <= value <= high`.
- `decreased(label, before, after, min_drop=0.0)` — `after < before`; with
  `min_drop` also requires a drop of at least that *fraction* of `|before|`
  (e.g. `0.8` = "loss fell ≥ 80%").
- `changed(label, before, after, tol=1e-12)` — a scalar or (nested) list/tuple
  actually changed by more than `tol`.
- `grad_check(label, f, x, analytic, eps=1e-5, tol=1e-4)` — central
  finite-difference check of scalar `f` at `x` (scalar or flat list) against
  the claimed analytic gradient, by relative error. Also the workhorse for the
  M5 micrograd chapters (which are `browser` — the modes share helpers; the
  *tier* only decides what you may assert).

Thresholds for colab exercises are calibrated on **≥3 recorded Colab runs**
and set with generous margin (see `P2_SPEC.md` P2-D7); a property assert must
never flake on a compliant learner run.

## Run the tests

```bash
cd lib && python3 -m unittest -v
```
