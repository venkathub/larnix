#!/usr/bin/env python3
"""Tests for the review_cards (spaced-repetition seeding) gate."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import review_cards_lint as rc  # noqa: E402

VALID = {
    "title": "x",
    "review_cards": [
        {"id": "what-is-a-model", "q": "What is a model?", "a": "A learned function."},
        {"q": "What does accuracy mean?", "a": "Fraction of correct predictions."},
    ],
}


class ReviewCardsTests(unittest.TestCase):
    def test_absent_is_ok(self):
        self.assertEqual(rc.validate_review_cards({"title": "x"}), [])

    def test_valid(self):
        self.assertEqual(rc.validate_review_cards(VALID), [])

    def test_not_a_list(self):
        self.assertTrue(rc.validate_review_cards({"review_cards": "nope"}))

    def test_empty_list(self):
        self.assertTrue(rc.validate_review_cards({"review_cards": []}))

    def test_missing_a(self):
        errs = rc.validate_review_cards({"review_cards": [{"q": "Q?"}]})
        self.assertTrue(any("a must be" in e for e in errs))

    def test_missing_q(self):
        errs = rc.validate_review_cards({"review_cards": [{"a": "A."}]})
        self.assertTrue(any("q must be" in e for e in errs))

    def test_empty_strings(self):
        errs = rc.validate_review_cards({"review_cards": [{"q": "  ", "a": ""}]})
        self.assertEqual(len(errs), 2)

    def test_item_not_mapping(self):
        self.assertTrue(rc.validate_review_cards({"review_cards": ["just a string"]}))

    def test_duplicate_id(self):
        errs = rc.validate_review_cards(
            {"review_cards": [{"id": "d", "q": "A?", "a": "1"}, {"id": "d", "q": "B?", "a": "2"}]}
        )
        self.assertTrue(any("duplicate id" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
