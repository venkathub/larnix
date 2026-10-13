"""Verify the authored script and cell order offline; never install packages in tests."""
import ast
from contextlib import redirect_stdout
import io
from pathlib import Path
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes


class EnvironmentsLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L11']
        cls.program = cls.note['practice']['starter']
        cls.listing = '\n'.join(cls.note['listing']['lines'])
        cls.cell_a = cls.program.split('CELL A (displayed first)\n')[1].split('\n\nCELL B')[0]
        cls.cell_b = cls.program.split('CELL B (displayed second)\n')[1].split('\n\nRun B')[0]

    @staticmethod
    def execute(program):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'rental_summary.py'
            path.write_text(program + '\n', encoding='utf-8')
            return subprocess.run([sys.executable, '-I', str(path)], cwd=directory,
                                  text=True, capture_output=True, timeout=10)

    def test_listing_is_first_19_lines_and_under_60_columns(self):
        lines = self.note['listing']['lines']
        self.assertEqual(len(lines), 19)
        self.assertEqual(lines, self.program.splitlines()[:19])
        self.assertTrue(all(len(line) < 60 for line in lines))
        self.assertEqual(lines[11], 'expected = 31')

    def test_script_in_fresh_processes_reports_fixture_total_and_actual_python(self):
        expected = ('fixture: SYNTHETIC rental desk\ntickets: 2\n'
                    f'total units: 31\npython: {platform.python_version()}\n')
        for program in (self.program, self.listing):
            with self.subTest(program='complete' if program == self.program else 'listing'):
                result = self.execute(program)
                self.assertEqual((result.returncode, result.stderr), (0, ''))
                self.assertEqual(result.stdout, expected)
        for line in expected.splitlines()[:3]:
            self.assertIn(line, self.note['example'])
        self.assertIn('python: 3.12.13', self.program)

    def test_remembered_fresh_bad_and_repaired_cell_orders(self):
        evidence = dict(self.note['lab']['scenarios'][0]['evidence'])
        live = {}
        exec(self.cell_b, live)
        output = io.StringIO()
        with redirect_stdout(output):
            exec(self.cell_a, live)
        self.assertEqual(output.getvalue().strip(), evidence['Live kernel: B then A'])
        self.assertEqual(live['costs'], [16, 15])
        # A fresh namespace models restarting the kernel: displayed A fails first.
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaises(NameError) as error:
                exec(self.cell_a, {})
        self.assertEqual(output.getvalue(), '')
        self.assertEqual(f'NameError: {error.exception}',
                         evidence['Restart, displayed A first: final error line'])
        repaired = {}
        output = io.StringIO()
        with redirect_stdout(output):
            for cell in (self.cell_b, self.cell_a):
                exec(cell, repaired)
        self.assertEqual(output.getvalue().strip(),
                         evidence['Repair to B then A in a fresh kernel'])
        self.assertEqual(sum(repaired['costs']), 31)

    def test_notebook_and_script_use_identical_explicit_tickets(self):
        def tickets(code):
            node = next(n for n in ast.parse(code).body
                        if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == 'tickets' for t in n.targets))
            return ast.literal_eval(node.value)
        rows = tickets(self.listing)
        self.assertEqual(rows, tickets(self.cell_b))
        self.assertEqual(len(rows), 2)
        self.assertEqual([row['days'] * row['rate'] for row in rows], [16, 15])

    def test_wrong_expected_total_fails_visibly(self):
        result = self.execute(self.listing.replace('expected = 31', 'expected = 30'))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr.splitlines()[-1], 'ValueError: fixture total changed')

    def test_direct_data_lab_pins_are_preserved_in_recorded_environment(self):
        pins = (ROOT / 'labs/data-foundations/requirements.txt').read_text().splitlines()
        evidence = dict(self.note['lab']['scenarios'][1]['evidence'])
        actual = evidence['Scratch venv pip freeze: selected exact lines'].splitlines()
        for pin in pins:
            if pin and not pin.startswith('#'):
                self.assertIn(pin, actual)
        self.assertIn('notebook==7.4.5', actual)
        self.assertIn('ipykernel==6.30.1', actual)
        self.assertIn('matplotlib==3.10.7+dfsg1',
                      evidence['Host pip freeze: selected exact lines'].splitlines())

    def test_one_file_staged_snapshot_excludes_environment_fixture(self):
        # Everything Git touches is temporary. This is a dummy ignored file,
        # not a virtual environment; no venv or pip command runs in this test.
        with TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                result = subprocess.run(['git', '-c', 'commit.gpgsign=false',
                                         '-c', 'user.name=Fixture',
                                         '-c', 'user.email=fixture@example.invalid', *args],
                                        cwd=root, text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout
            git('init', '--quiet', '--object-format=sha1')
            (root / '.gitignore').write_text('.venv/\n.env\n')
            (root / '.venv').mkdir()
            (root / '.venv' / 'ignored-fixture.txt').write_text('not a real environment')
            path = root / 'rental_summary.py'
            path.write_text(self.program.replace('expected = 31', 'expected = 30', 1) + '\n')
            git('add', '.gitignore', 'rental_summary.py')
            git('commit', '--quiet', '-m', 'fixture baseline')
            path.write_text(self.program + '\n')
            self.assertEqual(git('status', '--short'), ' M rental_summary.py\n')
            diff = git('diff', '--unified=0', '--', 'rental_summary.py')
            recorded = self.program.split('(content-identifier line omitted):\n')[1].split('\nStaged file list:')[0]
            shown = '\n'.join(line for line in diff.splitlines() if not line.startswith('index '))
            self.assertEqual(shown, recorded)
            git('add', 'rental_summary.py')
            self.assertEqual(git('diff', '--staged', '--unified=0', '--', 'rental_summary.py'), diff)
            self.assertEqual(git('diff', '--staged', '--name-only'), 'rental_summary.py\n')
            self.assertEqual(git('status', '--short'), 'M  rental_summary.py\n')
            self.assertEqual(git('status', '--short', '--ignored', '--', '.venv/'), '!! .venv/\n')
            git('commit', '--quiet', '-m', 'fixture correction')
            self.assertEqual(git('status', '--short'), '')


if __name__ == '__main__':
    unittest.main()
