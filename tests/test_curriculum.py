"""Prevent misleading completion labels and broken expanded learning paths."""
from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from curriculum import load, validate, route_lessons
import curriculum as curriculum_cli


class CurriculumTest(unittest.TestCase):
    def setUp(self):
        self.curriculum, self.sources = load()

    def test_render_writes_every_document_with_one_trailing_newline(self):
        documents = curriculum_cli.render(self.curriculum, self.sources)
        with TemporaryDirectory() as directory, \
                patch.object(curriculum_cli, 'BASE', Path(directory)), \
                patch.object(curriculum_cli, 'load', return_value=(self.curriculum, self.sources)), \
                patch.object(sys, 'argv', ['curriculum.py', 'render']), \
                redirect_stdout(StringIO()):
            curriculum_cli.main()
            for relative, original in documents.items():
                with self.subTest(document=relative):
                    written = (Path(directory) / relative).read_bytes()
                    self.assertTrue(written.endswith(b'\n'))
                    self.assertFalse(written[:-1].endswith((b'\n', b'\r', b' ', b'\t')))
                    self.assertEqual(written, original.encode('utf-8'))

    def test_write_and_check_normalize_synthetic_builder_output(self):
        documents = {
            'no-newline.md': '# Test',
            'extra-newlines.md': '# Test\n\n\n',
            'trailing-whitespace.md': '# Test\n \t\r\n',
        }
        with TemporaryDirectory() as directory, \
                patch.object(curriculum_cli, 'BASE', Path(directory)), \
                patch.object(curriculum_cli, 'load', return_value=(self.curriculum, self.sources)), \
                patch.object(curriculum_cli, 'render', return_value=documents), \
                patch.object(curriculum_cli, 'check_local_links', return_value=[]), \
                redirect_stdout(StringIO()):
            with patch.object(sys, 'argv', ['curriculum.py', 'render']):
                curriculum_cli.main()
            for relative in documents:
                self.assertEqual((Path(directory) / relative).read_bytes(), b'# Test\n')
            with patch.object(sys, 'argv', ['curriculum.py', 'check']):
                curriculum_cli.main()
                for relative, original in documents.items():
                    with self.subTest(document=relative):
                        path = Path(directory) / relative
                        path.write_text(original)
                        with self.assertRaisesRegex(SystemExit, 'Missing or stale generated document'):
                            curriculum_cli.main()
                        path.write_bytes(b'# Test\n')

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
        # Append a throwaway plan so this guard survives every real lab becoming a preview.
        module = self.curriculum['modules'][1]
        lesson = deepcopy(module['lessons'][-1])
        lesson['id'] = f"{module['id']}-L{len(module['lessons']) + 1:02}"
        lesson['title'] = 'Test-only runnable artifact'
        lesson['interview']['question'] = 'Test-only artifact question?'
        lesson['production_exercise']['brief'] = 'Test-only artifact exercise.'
        lesson['status'] = 'planned'
        lesson['delivery'] = {
            'artifact': 'runnable_data_lab',
            'artifact_path': 'labs/data-foundations/README.md',
            'interaction': 'none', 'full_contract': 'not_met',
        }
        module['lessons'].append(lesson)
        module['lesson_order'].append(lesson['id'])
        self.curriculum['expected_lessons'] += 1
        self.assertEqual(validate(self.curriculum, self.sources), [])
        lesson['status'] = 'preview'
        self.assertTrue(any('manifest differ' in e for e in validate(self.curriculum, self.sources)))

    def test_runnable_lab_kinds_require_existing_lab_readmes(self):
        lesson = self.curriculum['modules'][0]['lessons'][0]
        for kind, name in [('runnable_data_lab', 'data-foundations'),
                           ('runnable_service_lab', 'service-foundations')]:
            with self.subTest(artifact=kind):
                lesson['delivery'].update(artifact=kind, artifact_path=f'labs/{name}/README.md')
                self.assertEqual(validate(self.curriculum, self.sources), [])
                for path in ('', 'README.md', 'labs/no-such-lab/README.md'):
                    lesson['delivery']['artifact_path'] = path
                    self.assertTrue(validate(self.curriculum, self.sources))
        lesson['delivery'].update(artifact='unrecognized_lab', artifact_path='labs/data-foundations/README.md')
        self.assertTrue(any('invalid artifact type' in e for e in validate(self.curriculum, self.sources)))

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
