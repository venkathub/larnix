#!/usr/bin/env python3
"""Unit tests for quiz_lint (stdlib unittest)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import quiz_lint as ql  # noqa: E402

VALID = {
    "title": "Chapter 1 — quick check",
    "id": "m0-ch1",
    "questions": [
        {
            "id": "what-is-a-model",
            "prompt": "A model is…",
            "options": ["A spreadsheet of data", "A function learned from data"],
            "answer": 1,
            "explanation": "It is the learned function.",
        },
        {
            "prompt": "Running in the browser buys you…",
            "options": ["A GPU", "Zero install", "A database"],
            "answer": 1,
        },
    ],
}


def q(**over):
    base = {"prompt": "P?", "options": ["a", "b"], "answer": 0}
    base.update(over)
    return base


class ValidateQuizTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(ql.validate_quiz(VALID), [])

    def test_not_mapping(self):
        self.assertTrue(ql.validate_quiz([1, 2, 3]))

    def test_questions_required_nonempty(self):
        self.assertTrue(any("questions" in e for e in ql.validate_quiz({"questions": []})))
        self.assertTrue(any("questions" in e for e in ql.validate_quiz({"title": "x"})))

    def test_prompt_required(self):
        errs = ql.validate_quiz({"questions": [q(prompt="")]})
        self.assertTrue(any("prompt" in e for e in errs))

    def test_options_min_two(self):
        errs = ql.validate_quiz({"questions": [q(options=["only one"])]})
        self.assertTrue(any("at least 2" in e for e in errs))

    def test_option_nonempty(self):
        errs = ql.validate_quiz({"questions": [q(options=["a", ""])]})
        self.assertTrue(any("non-empty string" in e for e in errs))

    def test_answer_must_be_int(self):
        errs = ql.validate_quiz({"questions": [q(answer="1")]})
        self.assertTrue(any("answer must be an integer" in e for e in errs))

    def test_answer_bool_rejected(self):
        errs = ql.validate_quiz({"questions": [q(answer=True)]})
        self.assertTrue(any("answer must be an integer" in e for e in errs))

    def test_answer_out_of_range(self):
        errs = ql.validate_quiz({"questions": [q(options=["a", "b"], answer=2)]})
        self.assertTrue(any("out of range" in e for e in errs))

    def test_duplicate_question_id(self):
        errs = ql.validate_quiz(
            {"questions": [q(id="dup"), q(id="dup")]}
        )
        self.assertTrue(any("duplicate id" in e for e in errs))

    def test_explanation_optional_but_typed(self):
        errs = ql.validate_quiz({"questions": [q(explanation="")]})
        self.assertTrue(any("explanation" in e for e in errs))
        self.assertEqual(ql.validate_quiz({"questions": [q()]}), [])


if __name__ == "__main__":
    unittest.main()
