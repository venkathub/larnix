#!/usr/bin/env python3
"""Unit tests for the in-browser assert-grader helper (stdlib unittest).

Run:  cd lib && python3 -m unittest -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import grader  # noqa: E402


def run_capture(tests, **kw):
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = grader.run_tests(tests, **kw)
    return result, buf.getvalue()


class GraderTests(unittest.TestCase):
    def test_all_pass_returns_true_and_prints_summary(self):
        result, out = run_capture([("a", 1, 1), ("b", "x", "x")])
        self.assertTrue(result)
        self.assertIn("All 2 tests passed ✅", out)
        self.assertIn("✅ a", out)

    def test_failure_raises_with_labels(self):
        with self.assertRaises(AssertionError) as cm:
            run_capture([("good", 1, 1), ("bad", 2, 3)])
        self.assertIn("bad", str(cm.exception))
        self.assertIn("1 of 2", str(cm.exception))

    def test_failure_prints_expected_value(self):
        try:
            run_capture([("bad", 2, 3)])
        except AssertionError:
            pass
        _, out = io.StringIO(), None
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                grader.run_tests([("bad", 2, 3)])
            except AssertionError:
                pass
        self.assertIn("expected 3", buf.getvalue())

    def test_float_tolerance_passes(self):
        # 0.1 + 0.2 != 0.3 exactly, but within tolerance.
        result, _ = run_capture([("sum", 0.1 + 0.2, 0.3)])
        self.assertTrue(result)

    def test_float_outside_tolerance_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([("off", 0.5, 0.6)], tol=1e-9)

    def test_accuracy_example_end_to_end(self):
        # The exact exercise the sample chapter will use.
        def accuracy(y_true, y_pred):
            correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
            return correct / len(y_true)

        result, out = run_capture([
            ("all correct", accuracy([1, 1, 1], [1, 1, 1]), 1.0),
            ("half right", accuracy([1, 0], [1, 1]), 0.5),
            ("none right", accuracy([0, 0], [1, 1]), 0.0),
        ])
        self.assertTrue(result)
        self.assertIn("All 3 tests passed ✅", out)


if __name__ == "__main__":
    unittest.main()
