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


class BetweenTests(unittest.TestCase):
    def test_inside_bounds_passes(self):
        result, out = run_capture([grader.between("acc", 0.97, 0.95, 1.0)])
        self.assertTrue(result)
        self.assertIn("✅ acc", out)

    def test_bounds_are_inclusive(self):
        result, _ = run_capture([
            grader.between("low edge", 0.95, 0.95, 1.0),
            grader.between("high edge", 1.0, 0.95, 1.0),
        ])
        self.assertTrue(result)

    def test_outside_bounds_fails_with_readable_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(AssertionError):
                grader.run_tests([grader.between("acc", 0.41, 0.95, 1.0)])
        self.assertIn("got 0.41", buf.getvalue())
        self.assertIn("between 0.95 and 1.0", buf.getvalue())

    def test_non_number_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.between("acc", None, 0.0, 1.0)])


class DecreasedTests(unittest.TestCase):
    def test_any_decrease_passes_without_min_drop(self):
        result, _ = run_capture([grader.decreased("loss", 2.3, 2.2)])
        self.assertTrue(result)

    def test_increase_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.decreased("loss", 2.3, 2.4)])

    def test_no_change_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.decreased("loss", 2.3, 2.3)])

    def test_min_drop_fraction_met(self):
        # 2.5 -> 0.4 is an 84% drop; require 80%.
        result, _ = run_capture([grader.decreased("loss", 2.5, 0.4, min_drop=0.8)])
        self.assertTrue(result)

    def test_min_drop_fraction_not_met(self):
        # 2.5 -> 1.0 is only a 60% drop.
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(AssertionError):
                grader.run_tests([grader.decreased("loss", 2.5, 1.0, min_drop=0.8)])
        self.assertIn("at least 80%", buf.getvalue())

    def test_non_number_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.decreased("loss", None, 1.0)])


class ChangedTests(unittest.TestCase):
    def test_scalar_changed_passes(self):
        result, _ = run_capture([grader.changed("w", 0.5, 0.4)])
        self.assertTrue(result)

    def test_scalar_unchanged_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.changed("w", 0.5, 0.5)])

    def test_within_tol_counts_as_unchanged(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.changed("w", 0.5, 0.5 + 1e-15)])

    def test_nested_list_changed_passes(self):
        before = [[0.1, 0.2], [0.3, 0.4]]
        after = [[0.1, 0.2], [0.3, 0.5]]
        result, _ = run_capture([grader.changed("weights", before, after)])
        self.assertTrue(result)

    def test_nested_list_unchanged_fails(self):
        before = [[0.1, 0.2], [0.3, 0.4]]
        with self.assertRaises(AssertionError):
            run_capture([grader.changed("weights", before, [list(r) for r in before])])

    def test_length_mismatch_counts_as_changed(self):
        result, _ = run_capture([grader.changed("weights", [1.0, 2.0], [1.0])])
        self.assertTrue(result)


class GradCheckTests(unittest.TestCase):
    def test_scalar_correct_gradient_passes(self):
        # f(x) = x^2, f'(3) = 6.
        result, out = run_capture([
            grader.grad_check("d(x^2)/dx", lambda x: x * x, 3.0, 6.0)
        ])
        self.assertTrue(result)
        self.assertIn("max relative gradient error", out)

    def test_scalar_wrong_gradient_fails(self):
        with self.assertRaises(AssertionError):
            run_capture([grader.grad_check("d(x^2)/dx", lambda x: x * x, 3.0, 5.0)])

    def test_vector_correct_gradient_passes(self):
        # f(w) = sum(w_i^2), grad = 2w.
        f = lambda w: sum(v * v for v in w)  # noqa: E731
        w = [1.0, -2.0, 0.5]
        result, _ = run_capture([
            grader.grad_check("d(sum sq)/dw", f, w, [2 * v for v in w])
        ])
        self.assertTrue(result)

    def test_vector_one_wrong_coordinate_fails(self):
        f = lambda w: sum(v * v for v in w)  # noqa: E731
        with self.assertRaises(AssertionError):
            run_capture([
                grader.grad_check("grad", f, [1.0, -2.0], [2.0, 4.0])  # sign flip
            ])

    def test_length_mismatch_fails_with_message(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(AssertionError):
                grader.run_tests([
                    grader.grad_check("grad", lambda w: sum(w), [1.0, 2.0], [1.0])
                ])
        self.assertIn("one gradient value per parameter", buf.getvalue())

    def test_does_not_mutate_params(self):
        w = [1.0, 2.0]
        run_capture([
            grader.grad_check("grad", lambda v: sum(x * x for x in v), w, [2.0, 4.0])
        ])
        self.assertEqual(w, [1.0, 2.0])


class MixedModeTests(unittest.TestCase):
    def test_classic_tuples_and_property_checks_mix(self):
        result, out = run_capture([
            ("exact value", 4, 4),
            grader.between("accuracy", 0.98, 0.95, 1.0),
            grader.decreased("loss", 2.5, 0.3, min_drop=0.8),
        ])
        self.assertTrue(result)
        self.assertIn("All 3 tests passed ✅", out)

    def test_mixed_failure_counts_all_checks(self):
        with self.assertRaises(AssertionError) as cm:
            run_capture([
                ("exact value", 4, 5),
                grader.between("accuracy", 0.5, 0.95, 1.0),
                grader.decreased("loss", 2.5, 0.3),
            ])
        self.assertIn("2 of 3", str(cm.exception))
        self.assertIn("exact value", str(cm.exception))
        self.assertIn("accuracy", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
