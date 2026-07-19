#!/usr/bin/env python3
"""Unit tests for ai_review (stdlib unittest; no network — the pure parts only)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ai_review as ar  # noqa: E402


class ClipDiffTests(unittest.TestCase):
    def test_small_diff_untouched(self):
        text, truncated = ar.clip_diff("small diff")
        self.assertEqual(text, "small diff")
        self.assertFalse(truncated)

    def test_large_diff_truncated_with_visible_note(self):
        text, truncated = ar.clip_diff("x" * (ar.MAX_DIFF_CHARS + 100))
        self.assertTrue(truncated)
        self.assertIn("DIFF TRUNCATED", text)  # never silently incomplete
        self.assertLess(len(text), ar.MAX_DIFF_CHARS + 200)


class RubricTests(unittest.TestCase):
    def test_rubric_loads_from_repo(self):
        rubric = ar.load_rubric()
        # Both perspectives must be present in the steering text.
        self.assertIn("Senior AI engineer", rubric)
        self.assertIn("Tutor", rubric)
        # Path-scoped content rubric is folded in (single source of truth).
        self.assertIn("Varsity contract", rubric)

    def test_missing_rubric_raises(self):
        from pathlib import Path
        with self.assertRaises(FileNotFoundError):
            ar.load_rubric(Path("/nonexistent"))


class MessageBuildTests(unittest.TestCase):
    def test_messages_shape_and_content(self):
        msgs = ar.build_messages("diff --git a/x b/x", "title", "body", "RUBRIC")
        self.assertEqual([m["role"] for m in msgs], ["system", "user"])
        self.assertIn("RUBRIC", msgs[0]["content"])
        self.assertIn("[blocking]", msgs[0]["content"])  # severity convention
        self.assertIn("diff --git", msgs[1]["content"])
        self.assertIn("title", msgs[1]["content"])

    def test_empty_body_is_labelled(self):
        msgs = ar.build_messages("d", "t", "", "R")
        self.assertIn("(none)", msgs[1]["content"])


class ResponseTests(unittest.TestCase):
    def test_extract_review(self):
        resp = {"choices": [{"message": {"role": "assistant", "content": " ok "}}]}
        self.assertEqual(ar.extract_review(resp), "ok")

    def test_bad_response_raises(self):
        with self.assertRaises(ValueError):
            ar.extract_review({"unexpected": True})


class CommentTests(unittest.TestCase):
    def test_comment_has_marker_and_advisory_note(self):
        c = ar.render_comment("review body")
        self.assertTrue(c.startswith(ar.COMMENT_MARKER))  # sticky-update anchor
        self.assertIn("Advisory only", c)
        self.assertIn("review body", c)
        self.assertNotIn("TRUNCATED", c)

    def test_truncation_note_shown(self):
        self.assertIn("truncated", ar.render_comment("r", truncated=True))


class RetryLadderTests(unittest.TestCase):
    """413 (request too large) shrinks the diff and retries — observed live on
    PR #5 where the free tier rejected the first attempt."""

    def _http_error(self, code):
        import urllib.error
        return urllib.error.HTTPError("url", code, "msg", None, None)

    def test_413_retries_with_smaller_cap_then_succeeds(self):
        calls = []

        def fake_call(messages, token):
            calls.append(len(messages[1]["content"]))
            if len(calls) == 1:
                raise self._http_error(413)
            return {"choices": [{"message": {"content": "review"}}]}

        orig = ar.call_model
        ar.call_model = fake_call
        try:
            review, cap, err = ar.review_with_retry("x" * 100_000, "t", "T", "B", "R")
        finally:
            ar.call_model = orig
        self.assertEqual(review, "review")
        self.assertEqual(cap, ar.DIFF_CAPS[1])
        self.assertIsNone(err)
        self.assertEqual(len(calls), 2)
        self.assertLess(calls[1], calls[0])  # second attempt really was smaller

    def test_non_413_does_not_retry(self):
        calls = []

        def fake_call(messages, token):
            calls.append(1)
            raise self._http_error(429)

        orig = ar.call_model
        ar.call_model = fake_call
        try:
            review, _, err = ar.review_with_retry("d", "t", "T", "B", "R")
        finally:
            ar.call_model = orig
        self.assertIsNone(review)
        self.assertEqual(len(calls), 1)
        self.assertIsNotNone(err)

    def test_all_413_gives_none_with_error(self):
        def fake_call(messages, token):
            raise self._http_error(413)

        orig = ar.call_model
        ar.call_model = fake_call
        try:
            review, cap, err = ar.review_with_retry("d", "t", "T", "B", "R")
        finally:
            ar.call_model = orig
        self.assertIsNone(review)
        self.assertEqual(cap, ar.DIFF_CAPS[-1])
        self.assertIsNotNone(err)


if __name__ == "__main__":
    unittest.main()
