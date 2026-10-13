"""Acceptance checks for authored foundation coverage and teaching fixtures."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes, validate_notes


class FoundationLessonsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curriculum = json.loads((ROOT / 'docs/curriculum/curriculum.json').read_text())
        cls.manifest = json.loads((ROOT / 'web/lessons.json').read_text())
        cls.notes = load_notes()

    def test_all_six_modules_are_authored_without_replacing_vector_lab(self):
        expected = {l['id'] for m in self.curriculum['modules'][:6] for l in m['lessons'][:4]}
        self.assertEqual(len(expected), 24)
        self.assertEqual(set(self.notes), expected - {'M03-L01'})
        self.assertTrue(expected <= self.manifest.keys())
        self.assertEqual(self.manifest['M03-L01']['directory'], 'vector-similarity')
        validate_notes(self.notes, self.curriculum)

    def test_saved_check_keys_match_the_rendered_lesson_answers(self):
        for lesson_id, note in self.notes.items():
            with self.subTest(lesson=lesson_id):
                self.assertEqual(self.manifest[lesson_id]['answers'],
                                 {f'check{i+1}': str(q['answer']) for i, q in enumerate(note['checks'])})
                self.assertEqual(self.manifest[lesson_id]['checks'], len(note['checks']))
                self.assertEqual(self.manifest[lesson_id]['format'], 'foundation')

    def test_threshold_fixture_counts_match_the_original_six_tickets(self):
        scores = [.9, .8, .7, .4, .3, .1]
        labels = [1, 0, 1, 1, 0, 0]
        for threshold, case in zip([.8, .4, .1], self.notes['M04-L03']['lab']['scenarios']):
            predictions = [score >= threshold for score in scores]
            caught = sum(p and y for p, y in zip(predictions, labels))
            values = {b['label']: b['value'] for b in case['bars']}
            self.assertEqual(values['Reviewed tickets'], sum(predictions))
            self.assertEqual(values['Caught urgent tickets'], caught)
            if 'Missed urgent tickets' in values:
                self.assertEqual(values['Missed urgent tickets'], sum(labels) - caught)
            if 'Over capacity: tickets' in values:
                self.assertEqual(values['Over capacity: tickets'], max(0, sum(predictions) - 4))

    def test_baselines_do_not_confuse_accuracy_with_catching_rare_cases(self):
        cases = self.notes['M04-L01']['lab']['scenarios']
        # 8 on-time, 2 late. Models: always on-time; 2 TP + 2 FP;
        # strict rule with 1 TP + 0 FP. These tradeoffs are the lesson.
        for case, (tp, fp) in zip(cases, [(0, 0), (2, 2), (1, 0)]):
            values = {b['label']: b['value'] for b in case['bars']}
            self.assertEqual(values['Correct records'], tp + (8-fp))
            self.assertEqual(values['Missed late records'], 2-tp)
            self.assertEqual(values['False alarms: records'], fp)

    def test_training_fixtures_match_independent_scalar_calculations(self):
        x, target, weight, rate = 2, 6, 1, .1
        loss = (weight*x-target)**2
        gradient = 2*(weight*x-target)*x
        updated = weight-rate*gradient
        after = (updated*x-target)**2
        for case, expected in zip(self.notes['M05-L01']['lab']['scenarios'], [loss, loss, after]):
            bars = {b['label']: b['value'] for b in case['bars']}
            self.assertAlmostEqual(bars['Current squared loss'], expected)
        for rate, case in zip([.25, 1, 1.2], self.notes['M05-L02']['lab']['scenarios']):
            weight = 0
            for _ in range(2):
                weight -= rate * 2 * (weight-3)
            bars = {b['label']: b['value'] for b in case['bars']}
            self.assertAlmostEqual(bars['After 2: squared loss'], (weight-3)**2)

    def test_shared_filter_fixture_reuses_the_same_local_operation(self):
        strips = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]]
        for strip, case in zip(strips, self.notes['M05-L04']['lab']['scenarios']):
            expected = [b-a for a, b in zip(strip, strip[1:])]
            self.assertEqual([b['value'] for b in case['bars']], expected)


if __name__ == '__main__':
    unittest.main()
