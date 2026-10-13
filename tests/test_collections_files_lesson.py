"""Execute the authored file round-trip and retain evidence of its deliberate failure."""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes


class CollectionsFilesLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L09']
        cls.execution, cls.files = cls.execute(cls.note['practice']['starter'])

    @staticmethod
    def execute(program):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'rental_files.py'
            path.write_text(program + '\n', encoding='utf-8')
            run = subprocess.run([sys.executable, '-I', str(path)], cwd=directory,
                                 text=True, capture_output=True, timeout=10)
            files = {name: (Path(directory) / name).read_bytes()
                     for name in ('tickets.csv', 'tickets.json')
                     if (Path(directory) / name).exists()}
            return run, files

    def test_listing_is_the_first_thirty_four_program_lines(self):
        self.assertEqual(self.note['listing']['language'], 'python')
        self.assertEqual(len(self.note['listing']['lines']), 34)
        self.assertTrue(all(len(line) < 60 for line in self.note['listing']['lines']))
        self.assertEqual(self.note['listing']['lines'], self.note['practice']['starter'].splitlines()[:34])
        run, files = self.execute('\n'.join(self.note['listing']['lines']))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(files, self.files)
        self.assertEqual(run.stdout.splitlines(), self.execution.stdout.splitlines()[:6])

    def test_exact_file_bytes_counts_fields_and_converted_totals(self):
        evidence = dict(self.note['lab']['scenarios'][0]['evidence'])
        # Parse the authored quoted CSV text, not another copy of the fixture.
        csv_text, _ = json.JSONDecoder().raw_decode(evidence['Exact CSV text (UTF-8)'])
        json_text = evidence['Exact JSON text (UTF-8)'].removesuffix(' (one line; no final newline)')
        self.assertEqual(self.files['tickets.csv'], csv_text.encode('utf-8'))
        self.assertEqual(self.files['tickets.json'], json_text.encode('utf-8'))
        csv_rows = list(csv.DictReader(io.StringIO(csv_text)))
        json_rows = json.loads(json_text)
        self.assertEqual(len(csv_rows), 3)
        self.assertEqual(len(json_rows), 3)
        self.assertEqual([list(row) for row in csv_rows], [['id', 'days']] * 3)
        self.assertEqual([list(row) for row in json_rows], [['id', 'days']] * 3)
        self.assertEqual([int(row['days']) for row in csv_rows], [1, 3, 2])
        self.assertEqual([row['days'] for row in json_rows], [1, 3, 2])
        self.assertEqual([row['id'] for row in json_rows if row['days'] >= 2], ['r2', 'r3'])
        self.assertEqual(sum(int(row['days']) for row in csv_rows), 6)
        self.assertEqual(sum(row['days'] for row in json_rows), 6)
        for line in evidence['Exact count / filter / total output'].splitlines():
            self.assertIn(line, self.execution.stdout.splitlines())
            self.assertIn(line, self.note['example'])

    def test_reloaded_types_multiplication_and_named_record_match_the_core(self):
        csv_rows = list(csv.DictReader(io.StringIO(self.files['tickets.csv'].decode())))
        json_rows = json.loads(self.files['tickets.json'])
        self.assertIs(type(csv_rows[1]['days']), str)
        self.assertIs(type(json_rows[1]['days']), int)
        self.assertEqual(csv_rows[1]['days'] * 2, '33')
        self.assertEqual(int(csv_rows[1]['days']) * 2, 6)
        for _, line in self.note['lab']['scenarios'][1]['evidence']:
            self.assertIn(line, self.execution.stdout.splitlines())
            self.assertIn(line, self.note['example'])
        comparison = 'named / tuple / dict: 3 3 3'
        self.assertIn(comparison, self.execution.stdout.splitlines())
        self.assertIn(comparison, self.note['topics'][3]['explanation'])

    def test_invalid_numeric_field_stops_without_silent_row_drop(self):
        evidence = dict(self.note['lab']['scenarios'][2]['evidence'])
        self.assertNotEqual(self.execution.returncode, 0)
        self.assertEqual(self.execution.stderr.splitlines()[-1], evidence['Exception (final traceback line)'])
        self.assertEqual(self.execution.stdout.splitlines()[-1], evidence['Exact output before failure'])
        self.assertNotIn('invalid total:', self.execution.stdout)
        # Repair just the deliberately injected value; the total includes all three rows.
        original = self.note['practice']['starter']
        self.assertEqual(original.count('csv_rows[1]["days"] = "three"'), 1)
        fixed = original.replace('csv_rows[1]["days"] = "three"', 'csv_rows[1]["days"] = "3"')
        run, files = self.execute(fixed)
        self.assertEqual((run.returncode, run.stderr), (0, ''))
        self.assertEqual(run.stdout.splitlines()[-1], 'invalid total: 6')
        self.assertEqual(files, self.files)

    def test_missing_key_and_list_transfer_have_the_claimed_behavior(self):
        broken = self.note['practice']['starter'].replace('{"id": "r2", "days": 3}', '{"id": "r2"}')
        run, files = self.execute(broken)
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(run.stderr.splitlines()[-1], "KeyError: 'days'")
        self.assertEqual(files, {})
        run, _ = self.execute('print([1, 3, 2] * 2)')
        self.assertEqual((run.returncode, run.stdout), (0, '[1, 3, 2, 1, 3, 2]\n'))
        self.assertIn(run.stdout.strip(), self.note['transfer'][0]['answer'])


if __name__ == '__main__':
    unittest.main()
