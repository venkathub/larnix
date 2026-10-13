"""Run the lesson's actual file, including the learner's broken-guard experiment."""
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes


class ErrorsTestsLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L10']
        cls.program = cls.note['practice']['starter']

    @staticmethod
    def execute(program, *args):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'rental_errors.py'
            path.write_text(program + '\n', encoding='utf-8')
            result = subprocess.run([sys.executable, '-I', str(path), *args],
                                    cwd=directory, capture_output=True,
                                    text=True, timeout=10)
            # Only the directory is machine-specific; keep source lines and frames.
            result.stderr = result.stderr.replace(str(path), 'rental_errors.py')
            return result

    def assert_two_tests_pass(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertRegex(result.stderr, r'Ran 2 tests in [0-9.]+s')
        self.assertEqual(result.stderr.splitlines()[0], '..')
        self.assertEqual(result.stderr.splitlines()[-1], 'OK')

    def test_listing_is_first_27_lines_and_fits_desktop(self):
        lines = self.note['listing']['lines']
        self.assertEqual(lines, self.program.splitlines()[:27])
        self.assertEqual(len(lines), 27)
        self.assertTrue(all(len(line) < 60 for line in lines))
        self.assertEqual(lines[4], '    if days <= 0:')
        self.assertEqual(lines[5], '        raise ValueError("days must be positive")')
        self.assertEqual(lines[22], '        rental_total("2", 7)')
        self.assertEqual(lines[24], '        rental_total(0, 7)')

    def test_default_reports_two_tests_and_authored_summary(self):
        result = self.execute(self.program)
        self.assert_two_tests_pass(result)
        evidence = dict(self.note['lab']['scenarios'][0]['evidence'])
        for line in evidence['Exact progress / final summary'].splitlines():
            self.assertIn(line, result.stderr.splitlines())
        self.assertIn('returns 14', evidence['Counts / calculation'])
        # Ask the same file's function for its value; the function does not print it.
        probe = self.program.split('if __name__')[0] + '\nprint(rental_total(2, 7))'
        actual = self.execute(probe)
        self.assertEqual((actual.returncode, actual.stdout), (0, '14\n'))

    def test_zero_rejection_message_and_frames_match_case(self):
        result = self.execute(self.program, 'zero')
        evidence = dict(self.note['lab']['scenarios'][1]['evidence'])
        self.assertEqual((result.returncode, result.stdout), (1, ''))
        self.assertEqual(result.stderr.splitlines()[-1], evidence['Exact final traceback line'])
        self.assertEqual(re.findall(r'line (\d+), in (.+)', result.stderr),
                         [('25', '<module>'), ('6', 'rental_total')])
        self.assertIn(evidence['Exact final traceback line'], self.note['example'])

    def test_wrong_type_traceback_matches_authored_lines_and_frames(self):
        result = self.execute(self.program, 'wrong')
        evidence = dict(self.note['lab']['scenarios'][2]['evidence'])
        self.assertEqual((result.returncode, result.stdout), (1, ''))
        self.assertEqual(result.stderr.splitlines()[-1], evidence['Exact final traceback line'])
        self.assertEqual(re.findall(r'line (\d+), in (.+)', result.stderr),
                         [('23', '<module>'), ('5', 'rental_total')])
        for key in ('Header and calling frame', 'Failed frame and operation'):
            for line in evidence[key].splitlines():
                # Caret formatting differs across supported Python versions.
                if set(line.strip()) != {'^'}:
                    self.assertIn(line, result.stderr.splitlines())
        self.assertIn('\n'.join(evidence.values()), self.program)
        for text in evidence.values():
            for line in text.splitlines():
                self.assertIn(line.strip(), self.note['example'])
        self.assertIn('real traceback', ' '.join(self.note['story']))
        self.assertIn('last line', self.note['example'])

    def test_broken_guard_fails_and_restored_guard_passes(self):
        self.assertEqual('\n'.join(self.note['listing']['lines']).count('days <= 0'), 1)
        broken = self.program.replace('days <= 0', 'days < 0', 1)
        result = self.execute(broken)
        self.assertEqual(result.returncode, 1)
        self.assertIn('AssertionError: ValueError not raised', result.stderr.splitlines())
        self.assertEqual(result.stderr.splitlines()[-1], 'FAILED (failures=1)')
        self.assertRegex(result.stderr, r'Ran 2 tests in [0-9.]+s')
        for line in ('AssertionError: ValueError not raised', 'FAILED (failures=1)'):
            self.assertIn(line, self.note['practice']['steps'][2])
        restored = broken.replace('days < 0', 'days <= 0')
        self.assertEqual(restored, self.program)
        self.assert_two_tests_pass(self.execute(restored))

    def test_message_assertion_and_transfer_boundaries(self):
        # An altered rejection message must fail the authored message assertion.
        altered = self.program.replace('raise ValueError("days must be positive")',
                                       'raise ValueError("bad days")')
        result = self.execute(altered)
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAILED (failures=1)', result.stderr)
        negative = self.program.replace('        rental_total(0, 7)\n    else:',
                                        '        rental_total(-1, 7)\n    else:')
        result = self.execute(negative, 'zero')
        self.assertEqual(result.stderr.splitlines()[-1], 'ValueError: days must be positive')
        probe = self.program.split('if __name__')[0] + '\nprint(rental_total(2, -7))'
        result = self.execute(probe)
        self.assertEqual((result.returncode, result.stdout), (0, '-14\n'))
        self.assertIn('-14', self.note['transfer'][1]['answer'])


if __name__ == '__main__':
    unittest.main()
