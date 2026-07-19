"""Larnix in-browser assert-grader helper.

Runs both inside a `{pyodide}` cell (in the learner's browser) and in CPython
(for these unit tests), so the grading logic is verifiable off-browser.

It gives every auto-graded exercise one consistent pass/fail UX:

    from grader import run_tests        # or paste this file into a `setup` cell
    run_tests([
        ("all correct", accuracy([1, 1], [1, 1]), 1.0),
        ("half right",  accuracy([1, 0], [1, 1]), 0.5),
    ])

Loading it in a chapter (single source of truth — P1-D9 / DECISIONS D0016):
add this file to the page's `resources:` front-matter key so quarto-live copies
it into the Pyodide VFS at startup, then `from lib.grader import run_tests` in a
hidden `#| edit: false` cell. No more pasting the helper into every chapter.

On success it prints "All N tests passed ✅". On the first set of failures it
prints each result and raises AssertionError, so the cell shows an error.

Two grading modes (P2-D7, DECISIONS D0020):

1. **Seeded-deterministic** (browser / CPU-twin chapters): the exercise pins
   every seed, so plain ``(label, got, expected)`` tuples with the existing
   float tolerance are enough. Nothing new to import.
2. **Property-based** (colab / GPU chapters, where training is stochastic):
   assert *properties of a successful run* instead of exact values, via the
   check-builders below, which drop straight into ``run_tests``:

    run_tests([
        between("test accuracy", acc, 0.95, 1.0),
        decreased("training loss", first_loss, final_loss, min_drop=0.80),
        changed("weights updated", w_before, w_after),
        grad_check("dL/dw", loss_fn, w, analytic_grad),
    ])

Design notes:
- Pyodide-safe: standard library only (no imports beyond the stdlib).
- Floats compare with a tolerance (default 1e-9) so exercises that compute
  e.g. an accuracy don't fail on representation error.
- Check-builders evaluate immediately and return a ``_Check`` record;
  ``run_tests`` prints them with the same ✅/❌ UX as classic tuples.
"""
from __future__ import annotations

_NUMERIC = (int, float)


def _is_number(x) -> bool:
    # bool is a subclass of int; treat True/False as non-numeric for tolerance.
    return isinstance(x, _NUMERIC) and not isinstance(x, bool)


def _equalish(got, expected, tol: float) -> bool:
    if _is_number(got) and _is_number(expected):
        return abs(got - expected) <= tol
    return got == expected


class _Check:
    """A pre-evaluated property check (P2-D7 property-based grading mode).

    Built by :func:`between`, :func:`decreased`, :func:`changed` and
    :func:`grad_check`; consumed by :func:`run_tests`. ``got`` and
    ``expected`` are pre-formatted, learner-readable strings.
    """

    __slots__ = ("label", "ok", "got", "expected")

    def __init__(self, label: str, ok: bool, got: str, expected: str):
        self.label = label
        self.ok = bool(ok)
        self.got = got
        self.expected = expected


def between(label: str, value, low, high) -> _Check:
    """Check ``low <= value <= high`` (bounds inclusive).

    The property-mode workhorse for training exercises, e.g.
    ``between("test accuracy", acc, 0.95, 1.0)``.
    """
    ok = _is_number(value) and low <= value <= high
    return _Check(label, ok, repr(value), f"a number between {low!r} and {high!r}")


def decreased(label: str, before, after, min_drop: float = 0.0) -> _Check:
    """Check that ``after`` fell below ``before``.

    With ``min_drop`` (a fraction, e.g. ``0.8`` = "fell by at least 80%"),
    also require ``before - after >= min_drop * abs(before)`` — the
    "loss fell ≥ N% during training" property assert.
    """
    numeric = _is_number(before) and _is_number(after)
    if numeric and min_drop > 0:
        ok = after < before and (before - after) >= min_drop * abs(before)
        expected = f"a drop of at least {min_drop * 100:g}% from {before!r}"
    else:
        ok = numeric and after < before
        expected = f"any decrease from {before!r}"
    return _Check(label, ok, f"{before!r} -> {after!r}", expected)


def _differs(a, b, tol: float) -> bool:
    """True if a and b differ by more than tol (recursing into sequences)."""
    if _is_number(a) and _is_number(b):
        return abs(a - b) > tol
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return True
        return any(_differs(x, y, tol) for x, y in zip(a, b))
    return a != b


def changed(label: str, before, after, tol: float = 1e-12) -> _Check:
    """Check that a value (or nested list/tuple of values) actually changed.

    The "weights actually moved after one training step" property assert.
    """
    ok = _differs(before, after, tol)
    return _Check(
        label,
        ok,
        "values changed" if ok else "values unchanged",
        f"a change larger than tol={tol:g}",
    )


def grad_check(
    label: str, f, x, analytic, eps: float = 1e-5, tol: float = 1e-4
) -> _Check:
    """Check an analytic gradient of scalar ``f`` against central finite differences.

    ``x`` and ``analytic`` are either both scalars, or a flat list/tuple of
    parameter values and the claimed gradient per parameter. For each
    coordinate i the numeric gradient ``(f(x + eps*e_i) - f(x - eps*e_i)) /
    (2*eps)`` is compared to ``analytic[i]`` by relative error
    ``|num - ana| / max(1, |num|, |ana|)``; the check passes if the largest
    relative error is <= ``tol``.
    """
    if _is_number(x):
        xs, ans = [x], [analytic]
        call = lambda vals: f(vals[0])  # noqa: E731
    else:
        xs, ans = list(x), list(analytic)
        call = lambda vals: f(list(vals))  # noqa: E731
    if len(xs) != len(ans):
        return _Check(
            label,
            False,
            f"{len(ans)} gradient value(s) for {len(xs)} parameter(s)",
            "one gradient value per parameter",
        )
    max_err = 0.0
    for i in range(len(xs)):
        plus = list(xs)
        minus = list(xs)
        plus[i] += eps
        minus[i] -= eps
        num = (call(plus) - call(minus)) / (2 * eps)
        ana = ans[i]
        if not _is_number(ana):
            return _Check(label, False, f"non-numeric gradient {ana!r}", "a number")
        err = abs(num - ana) / max(1.0, abs(num), abs(ana))
        max_err = max(max_err, err)
    ok = max_err <= tol
    return _Check(
        label,
        ok,
        f"max relative gradient error {max_err:.2e}",
        f"<= {tol:g} (analytic vs finite-difference)",
    )


def run_tests(tests, tol: float = 1e-9) -> bool:
    """Run a list of checks: ``(label, got, expected)`` tuples and/or
    property checks built by :func:`between` / :func:`decreased` /
    :func:`changed` / :func:`grad_check` — freely mixed.

    Prints one line per check. Returns True if all pass; otherwise raises
    AssertionError after printing every result.
    """
    tests = list(tests)
    failures = []
    for item in tests:
        if isinstance(item, _Check):
            label, ok = item.label, item.ok
            line = f"{'✅' if ok else '❌'} {label}: got {item.got}"
            if not ok:
                line += f", expected {item.expected}"
        else:
            label, got, expected = item
            ok = _equalish(got, expected, tol)
            line = f"{'✅' if ok else '❌'} {label}: got {got!r}"
            if not ok:
                line += f", expected {expected!r}"
        print(line)
        if not ok:
            failures.append(label)

    if failures:
        raise AssertionError(
            f"{len(failures)} of {len(tests)} test(s) failed: " + ", ".join(failures)
        )
    print(f"\nAll {len(tests)} tests passed ✅")
    return True
