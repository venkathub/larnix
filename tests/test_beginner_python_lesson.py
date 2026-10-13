"""Check the beginner's predictions and trace against isolated Python execution."""
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes

# The probe observes the unchanged downloaded starter, including its deliberate error.
PROBE = '''
import contextlib, io, json, runpy, sys
path = sys.argv[1]
events = []
names = ('daily_rate', 'discount', 'days', 'predicted', 'observed', 'total')
def trace(frame, event, arg):
    if frame.f_code.co_filename == path and event in ('line', 'return', 'exception'):
        row = {'event': event, 'line': frame.f_lineno, 'function': frame.f_code.co_name,
               'values': {k: frame.f_locals[k] for k in names if k in frame.f_locals}}
        if event == 'return':
            row['result'] = arg
        if event == 'exception':
            row['error'] = type(arg[1]).__name__ + ': ' + str(arg[1])
        events.append(row)
    return trace
output = io.StringIO()
sys.settrace(trace)
try:
    with contextlib.redirect_stdout(output):
        runpy.run_path(path, run_name='__main__')
except TypeError:
    pass
finally:
    sys.settrace(None)
print(json.dumps({'events': events, 'stdout': output.getvalue()}))
'''


class BeginnerPythonLessonTest(unittest.TestCase):
    def setUp(self):
        self.note = load_notes()['M02-L08']

    def test_core_listing_matches_the_first_fifteen_practice_lines(self):
        self.assertEqual(self.note['listing']['language'], 'python')
        self.assertEqual(len(self.note['listing']['lines']), 15)
        self.assertEqual(self.note['listing']['lines'], self.note['practice']['starter'].splitlines()[:15])

    def execute(self, starter, probe=False):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'rental_price.py'
            path.write_text(starter + '\n')
            command = [sys.executable, '-I']
            command += ['-c', PROBE, str(path)] if probe else [str(path)]
            return subprocess.run(command, text=True, capture_output=True, timeout=10)

    def test_isolated_starter_prints_predictions_then_raises_named_type_error(self):
        run = self.execute(self.note['practice']['starter'])
        self.assertNotEqual(run.returncode, 0)
        cases = self.note['lab']['scenarios']
        expected = [dict(case['evidence'])['Exact printed output'] for case in cases[:2]]
        self.assertEqual(run.stdout.splitlines(), expected)
        for line in expected:
            self.assertIn(line, self.note['example'])
        failure = dict(cases[2]['evidence'])['Exception (final traceback line)']
        self.assertEqual(run.stderr.splitlines()[-1], failure)
        self.assertNotIn('text-day observed:', run.stdout)
        self.assertEqual([case['bars'][0]['value'] for case in cases], [1, 1, 0])

    def test_worked_trace_values_and_execution_order_match_isolated_starter(self):
        run = self.execute(self.note['practice']['starter'], probe=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        events = json.loads(run.stdout)['events']
        module = {e['line']: e['values'] for e in events
                  if e['event'] == 'line' and e['function'] == '<module>'}
        worked = self.note['example']
        assignments = re.findall(r'L(\d+): (\w+) = (\d+)', worked)
        self.assertEqual(len(assignments), 6)
        for line, name, value in assignments:
            self.assertEqual(module[int(line) + 1][name], int(value))
        for line, value in re.findall(r'Back at L(\d+), observed = (\d+)', worked):
            self.assertEqual(module[int(line) + 1]['observed'], int(value))
        calls = [e for e in events if e['function'] == 'rental_price']
        totals = [e['values']['total'] for e in calls if e['event'] == 'line' and e['line'] == 5]
        self.assertEqual(totals[:2], [int(v) for v in re.findall(r'L4 sets total = (\d+)', worked)])
        self.assertEqual(totals[2], '3' * 20)
        self.assertIn('"' + totals[2] + '"', dict(self.note['lab']['scenarios'][2]['evidence'])['Input / intermediate value'])
        discounted = next(e['values']['total'] for e in calls
                          if e['event'] == 'line' and e['line'] == 7 and e['values']['days'] == 3)
        self.assertEqual(discounted, int(re.search(r'L6 changes total = (\d+)', worked)[1]))
        returns = [e['result'] for e in calls if e['event'] == 'return' and e['result'] is not None]
        self.assertEqual(returns, [int(v) for v in re.findall(r'L7 returns total = (\d+)', worked)])
        # Exact sequence independently checks skipped body-at-definition and skipped discount.
        self.assertEqual([e['line'] for e in events if e['event'] == 'line' and e['line'] <= 15],
                         [1, 2, 3, 8, 9, 10, 4, 5, 7, 11, 12, 13, 14, 4, 5, 6, 7, 15, 4, 5])
        for line in (12, 13):
            self.assertEqual(module[line]['predicted'], 20)
            self.assertEqual(module[line]['observed'], 20)
        for values in module.values():
            if 'discount' in values:
                self.assertEqual((values['daily_rate'], values['discount']), (20, 5))

    def test_fixing_only_the_text_fixture_completes_the_starter(self):
        original = self.note['practice']['starter']
        self.assertEqual(original.count('days = "3"'), 1)
        run = self.execute(original.replace('days = "3"', 'days = 3'))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, '')
        self.assertEqual(run.stdout.splitlines(), [
            'one-day predicted: 20 observed: 20',
            'multi-day predicted: 55 observed: 55',
            'text-day observed: 55'])

    def test_transfer_input_and_definition_only_have_the_claimed_behavior(self):
        lines = self.note['practice']['starter'].splitlines()
        self.assertEqual(lines[2], 'def rental_price(days):')
        definition = '\n'.join(lines[:7])
        run = self.execute(definition)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, '', ''))
        run = self.execute(definition + '\nprint(rental_price(2))')
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, '40\n', ''))
        self.assertIn('40 fictional currency units', self.note['transfer'][0]['answer'])


if __name__ == '__main__':
    unittest.main()
