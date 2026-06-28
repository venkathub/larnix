"""Larnix in-browser assert-grader helper.

Runs both inside a `{pyodide}` cell (in the learner's browser) and in CPython
(for these unit tests), so the grading logic is verifiable off-browser.

It gives every auto-graded exercise one consistent pass/fail UX:

    from grader import run_tests        # or paste this file into a `setup` cell
    run_tests([
        ("all correct", accuracy([1, 1], [1, 1]), 1.0),
        ("half right",  accuracy([1, 0], [1, 1]), 0.5),
    ])

On success it prints "All N tests passed ✅". On the first set of failures it
prints each result and raises AssertionError, so the cell shows an error.

Design notes:
- Pyodide-safe: standard library only (no imports beyond the stdlib).
- Floats compare with a tolerance (default 1e-9) so exercises that compute
  e.g. an accuracy don't fail on representation error.
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


def run_tests(tests, tol: float = 1e-9) -> bool:
    """Run a list of ``(label, got, expected)`` checks.

    Prints one line per check. Returns True if all pass; otherwise raises
    AssertionError after printing every result.
    """
    tests = list(tests)
    failures = []
    for label, got, expected in tests:
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
