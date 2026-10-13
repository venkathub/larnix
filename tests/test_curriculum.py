"""Prevent misleading completion labels and broken expanded learning paths."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from curriculum import load, validate, route_lessons


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

    def test_hours_and_artifact_evidence_are_required(self):
        lesson = self.curriculum['modules'][1]['lessons'][4]
        del lesson['estimated_hours']['exercise']
        lesson['delivery']['artifact_path'] = 'labs/no-such-lab/README.md'
        errors = validate(self.curriculum, self.sources)
        self.assertTrue(any('invalid exercise estimate' in e for e in errors))
        self.assertTrue(any('missing runnable artifact' in e for e in errors))

    def test_new_lessons_cannot_hide_unknown_sources_or_cycles(self):
        lesson = self.curriculum['modules'][1]['lessons'][4]
        lesson['sources'].append('UNKNOWN')
        lesson['prerequisites'].append('M02-L07')
        errors = validate(self.curriculum, self.sources)
        self.assertTrue(any('unknown source' in e for e in errors))
        self.assertTrue(any('Prerequisite cycle' in e for e in errors))

    def test_predictive_route_is_dependency_closed_without_llm_detours(self):
        lessons = {l['id']: l for m in self.curriculum['modules'] for l in m['lessons']}
        route = self.curriculum['learning_routes'][0]
        order = route_lessons(self.curriculum, route['targets'])
        self.assertTrue(set(route['targets']) <= set(order))
        self.assertFalse({lid[:3] for lid in order} &
                         {f'M{i:02}' for i in range(7, 25)})
        self.assertFalse({'M27', 'M28', 'M32'} & {lid[:3] for lid in order})
        prior = set()
        for lid in order:
            self.assertTrue(set(lessons[lid]['prerequisites']) <= prior, lid)
            prior.add(lid)

    def test_route_validator_rejects_an_indirect_llm_dependency(self):
        # This edge remains acyclic and in module order; only the route contract
        # catches the accidental return of LLM prerequisites through packaging.
        self.curriculum['modules'][28]['lessons'][0]['prerequisites'].append('M09-L04')
        self.assertTrue(any('excluded prerequisite module' in e
                            for e in validate(self.curriculum, self.sources)))

    def test_entry_lessons_and_advanced_release_keep_appropriate_requirements(self):
        self.assertEqual(route_lessons(self.curriculum, ['M02-L05']), ['M02-L01', 'M02-L05'])
        self.assertNotIn('M29-L04', route_lessons(self.curriculum, ['M29-L05']))
        self.assertNotIn('M35-L01', route_lessons(self.curriculum, ['M35-L05']))
        self.assertNotIn('M29-L07', route_lessons(self.curriculum, ['M35-L06']))
        self.assertNotIn('M29-L08', route_lessons(self.curriculum, ['M40-L05']))
        self.assertNotIn('M40-L05', route_lessons(self.curriculum, ['M40-L06']))
        self.assertIn('M28-L04', route_lessons(self.curriculum, ['M29-L03']))

    def test_teaching_order_can_branch_but_cannot_skip_or_precede_requirements(self):
        module = self.curriculum['modules'][1]
        module['lesson_order'] = ['M02-L05', 'M02-L01', *module['lesson_order'][2:]]
        self.assertTrue(any('before prerequisite M02-L01' in e
                            for e in validate(self.curriculum, self.sources)))
        module['lesson_order'].pop()
        self.assertTrue(any('teaching order must include every lesson' in e
                            for e in validate(self.curriculum, self.sources)))


if __name__ == '__main__':
    unittest.main()
