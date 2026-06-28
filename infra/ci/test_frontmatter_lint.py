#!/usr/bin/env python3
"""Unit tests for frontmatter_lint (stdlib unittest — runs with zero installs
beyond PyYAML; also discoverable by pytest).

Run:  python3 -m unittest -v   (from infra/ci/)
"""
import json
import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import frontmatter_lint as fl  # noqa: E402

TODAY = date(2026, 6, 28)

VALID = {
    "title": "Train your first model — in your browser",
    "module": "M0 — Orientation",
    "chapter": 1,
    "difficulty": "beginner",
    "prereqs": [],
    "learning_objectives": [
        "Run Python in the browser with zero install",
        "Train and call a scikit-learn classifier",
    ],
    "compute": "browser",
    "status": "stable",
    "last_reviewed": "2026-06-28",
    "est_minutes": 20,
}


def with_field(**overrides):
    d = dict(VALID)
    d.update(overrides)
    return d


def without(field):
    d = dict(VALID)
    d.pop(field)
    return d


class ValidateTests(unittest.TestCase):
    def test_valid_passes(self):
        self.assertEqual(fl.validate_frontmatter(VALID, today=TODAY), [])

    def test_valid_with_date_object(self):
        # YAML may parse an unquoted YYYY-MM-DD as a date object.
        self.assertEqual(
            fl.validate_frontmatter(with_field(last_reviewed=date(2026, 1, 1)), today=TODAY), []
        )

    def test_extra_keys_allowed(self):
        d = with_field(review_cards=[{"q": "?", "a": "."}])
        self.assertEqual(fl.validate_frontmatter(d, today=TODAY), [])

    def test_none_data(self):
        self.assertEqual(fl.validate_frontmatter(None, today=TODAY), ["no YAML front-matter found"])

    def test_each_missing_field_reported(self):
        for field in fl.REQUIRED_FIELDS:
            errs = fl.validate_frontmatter(without(field), today=TODAY)
            self.assertIn(f"missing required field: {field}", errs)

    def test_bad_difficulty(self):
        errs = fl.validate_frontmatter(with_field(difficulty="easy"), today=TODAY)
        self.assertTrue(any("difficulty" in e for e in errs))

    def test_bad_compute(self):
        errs = fl.validate_frontmatter(with_field(compute="tpu"), today=TODAY)
        self.assertTrue(any("compute" in e for e in errs))

    def test_bad_status(self):
        errs = fl.validate_frontmatter(with_field(status="draft"), today=TODAY)
        self.assertTrue(any("status" in e for e in errs))

    def test_objectives_too_few(self):
        errs = fl.validate_frontmatter(with_field(learning_objectives=["only one"]), today=TODAY)
        self.assertTrue(any("2–4" in e for e in errs))

    def test_objectives_too_many(self):
        errs = fl.validate_frontmatter(
            with_field(learning_objectives=["a", "b", "c", "d", "e"]), today=TODAY
        )
        self.assertTrue(any("2–4" in e for e in errs))

    def test_chapter_must_be_int(self):
        errs = fl.validate_frontmatter(with_field(chapter="one"), today=TODAY)
        self.assertTrue(any("chapter" in e for e in errs))

    def test_chapter_bool_rejected(self):
        errs = fl.validate_frontmatter(with_field(chapter=True), today=TODAY)
        self.assertTrue(any("chapter" in e for e in errs))

    def test_est_minutes_positive(self):
        errs = fl.validate_frontmatter(with_field(est_minutes=0), today=TODAY)
        self.assertTrue(any("est_minutes" in e for e in errs))

    def test_module_format(self):
        errs = fl.validate_frontmatter(with_field(module="Module Zero"), today=TODAY)
        self.assertTrue(any("module" in e for e in errs))

    def test_bad_date_format(self):
        errs = fl.validate_frontmatter(with_field(last_reviewed="28-06-2026"), today=TODAY)
        self.assertTrue(any("last_reviewed" in e for e in errs))

    def test_future_date_rejected(self):
        errs = fl.validate_frontmatter(with_field(last_reviewed="2099-01-01"), today=TODAY)
        self.assertTrue(any("future" in e for e in errs))

    def test_prereqs_must_be_list(self):
        errs = fl.validate_frontmatter(with_field(prereqs="none"), today=TODAY)
        self.assertTrue(any("prereqs" in e for e in errs))


class ExtractTests(unittest.TestCase):
    def _write(self, name, text):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_extract_qmd(self):
        path = self._write(
            "ch.qmd",
            '---\ntitle: "X"\ncompute: "browser"\n---\n\n# Body\n',
        )
        fm = fl.extract_frontmatter(path)
        self.assertEqual(fm["title"], "X")
        self.assertEqual(fm["compute"], "browser")

    def test_extract_qmd_no_frontmatter(self):
        path = self._write("plain.qmd", "# Just a heading\n")
        self.assertIsNone(fl.extract_frontmatter(path))

    def test_extract_ipynb_raw_cell(self):
        nb = {
            "cells": [
                {"cell_type": "raw", "source": ['---\n', 'title: "Y"\n', 'compute: "colab"\n', "---\n"]},
                {"cell_type": "code", "source": ["print(1)"]},
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path = self._write("ch.ipynb", json.dumps(nb))
        fm = fl.extract_frontmatter(path)
        self.assertEqual(fm["title"], "Y")
        self.assertEqual(fm["compute"], "colab")

    def test_lint_file_end_to_end(self):
        body = "---\n" + "\n".join(
            [
                'title: "T"',
                'module: "M0 — Orientation"',
                "chapter: 1",
                'difficulty: "beginner"',
                "prereqs: []",
                "learning_objectives:",
                '  - "Do a thing"',
                '  - "Do another"',
                'compute: "browser"',
                'status: "stable"',
                'last_reviewed: "2026-01-01"',
                "est_minutes: 20",
            ]
        ) + "\n---\n\n# Body\n"
        path = self._write("good.qmd", body)
        # lint_file uses date.today(); a past date avoids any future-date flake.
        self.assertEqual(fl.lint_file(path), [])


if __name__ == "__main__":
    unittest.main()
