"""Prevent misleading completion labels and broken expanded learning paths."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from curriculum import load, validate


class CurriculumTest(unittest.TestCase):
    def setUp(self):
        self.curriculum, self.sources = load()

    def test_current_plan_and_original_urls_remain_valid(self):
        self.assertEqual(validate(self.curriculum, self.sources), [])
        ids = {lesson['id'] for m in self.curriculum['modules'] for lesson in m['lessons']}
        self.assertTrue({f'M{m:02}-L{l:02}' for m in range(1, 43) for l in range(1, 5)} <= ids)
        self.assertEqual(len(ids), 188)

    def test_completion_requires_contract_evidence_not_a_status_change(self):
        lesson = self.curriculum['modules'][0]['lessons'][0]
        lesson['status'] = 'complete'
        self.assertTrue(any('verified contract' in e for e in validate(self.curriculum, self.sources)))
        lesson['delivery']['full_contract'] = 'verified'
        # Nine copies of one path cannot substitute for named contract coverage.
        lesson['delivery']['completion_evidence'] = ['README.md'] * 9
        self.assertTrue(any('nine contract categories' in e for e in validate(self.curriculum, self.sources)))

    def test_planned_artifact_does_not_become_an_authored_preview(self):
        lesson = self.curriculum['modules'][1]['lessons'][4]
        self.assertEqual(lesson['delivery']['artifact'], 'runnable_data_lab')
        self.assertEqual(lesson['status'], 'planned')
        lesson['status'] = 'preview'
        self.assertTrue(any('manifest differ' in e for e in validate(self.curriculum, self.sources)))

    def test_estimate_and_artifact_evidence_are_required(self):
        lesson = self.curriculum['modules'][1]['lessons'][4]
        del lesson['estimate_basis']['work']
        lesson['delivery']['artifact_path'] = 'labs/no-such-lab/README.md'
        errors = validate(self.curriculum, self.sources)
        self.assertTrue(any('estimate basis work' in e for e in errors))
        self.assertTrue(any('missing runnable artifact' in e for e in errors))

    def test_new_lessons_cannot_hide_unknown_sources_or_cycles(self):
        lesson = self.curriculum['modules'][1]['lessons'][4]
        lesson['sources'].append('UNKNOWN')
        lesson['prerequisites'].append('M02-L07')
        errors = validate(self.curriculum, self.sources)
        self.assertTrue(any('unknown source' in e for e in errors))
        self.assertTrue(any('Prerequisite cycle' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
