"""Tie the persistence preview's counts and errors to the read-only lab."""
from contextlib import closing, redirect_stdout
import importlib.util
from io import StringIO
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes

SPEC = importlib.util.spec_from_file_location('persistence_reference_lab', ROOT / 'labs/service-foundations/lab.py')
LAB = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LAB
SPEC.loader.exec_module(LAB)


class PersistenceLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L04']
        cls.ticket = json.loads(LAB.FIXTURE.read_text())[0]
        cls.report = LAB.persistence_cases(cls.ticket)
        cls.starter = {'__name__': 'persistence_starter'}
        exec(compile(cls.note['practice']['starter'], 'M02-L04 starter', 'exec'), cls.starter)

    def test_case_row_counts_and_failures_match_executed_operations(self):
        baseline = self.starter['separate_writes'](LAB, self.ticket)
        counts = [baseline['counts'], self.report['after_crash'], self.report['after_lost_response']]
        errors = [baseline['failure'], self.report['rejected_failures']['crash_between_writes'],
                  self.report['lost_response']]
        for case, actual, error in zip(self.note['lab']['scenarios'], counts, errors):
            with self.subTest(case=case['label']):
                evidence = dict(case['evidence'])
                row_pairs = re.findall(r'tickets=(\d+); audit=(\d+)', case['evidence'][0][1])
                self.assertEqual(tuple(map(int, row_pairs[0])), (actual['tickets'], actual['audit']))
                self.assertEqual([bar['value'] for bar in case['bars']], [actual['tickets'], actual['audit']])
                self.assertTrue(all(bar['max'] == 3 for bar in case['bars']))
                self.assertIn(f"{error['type']}: {error['message']}", evidence.values())
                self.assertIn('SYNTHETIC', case['label'])
        final = self.note['lab']['scenarios'][2]
        self.assertEqual(dict(final['evidence'])['Replay result'], str(self.report['replay']))
        final_pair = re.findall(r'tickets=(\d+); audit=(\d+)', final['evidence'][0][1])[-1]
        self.assertEqual(tuple(map(int, final_pair)), tuple(self.report['after_replay_and_rejections'].values()))
        visible = ' '.join(self.note['mechanism'] + [case['why'] for case in self.note['lab']['scenarios']])
        for key in ('duplicate_key', 'conflicting_replay', 'join_as_ticket_count'):
            error = self.report['rejected_failures'][key]
            self.assertIn(f"{error['type']}: {error['message']}", visible)
        self.assertEqual((self.report['joined_rows'], self.report['distinct_tickets']), (3, 1))

    def test_companion_ledger_replay_and_unique_index(self):
        output = StringIO()
        with redirect_stdout(output):
            actual = self.starter['probe'](LAB)
        self.assertEqual(actual['lab'], self.report)
        self.assertEqual(actual['replay'], {'ticket_id': 1, 'replayed': True})
        self.assertTrue(actual['unique_key_index'])
        expected = [(1, 0), (0, 0), (1, 3), (1, 3), (1, 3), (1, 3)]
        self.assertEqual([(row['tickets'], row['audit']) for _, row in actual['ledger']], expected)
        self.assertIn('stage                              | tickets | audits', output.getvalue())
        for stage, row in actual['ledger']:
            self.assertIn(f"{stage:34} | {row['tickets']:7} | {row['audit']:6}", output.getvalue())
        # The worked prose adds the initial empty state to this same ledger.
        quoted = re.findall(r'\((\d+),(\d+)\)', self.note['example'])
        self.assertEqual([tuple(map(int, pair)) for pair in quoted], [(0, 0)] + expected)

    def test_transfer_join_and_rollback_preserve_the_correct_unit(self):
        with closing(LAB.open_store()) as connection:
            LAB.store_ticket(connection, self.ticket)
            with self.assertRaises(LAB.InjectedCrash):
                LAB.store_ticket(connection, {**self.ticket, 'request_key': 'rent-new'}, crash=True)
            self.assertEqual(LAB.store_counts(connection), {'tickets': 1, 'audit': 3})
            events = connection.execute('SELECT event FROM audit ORDER BY id').fetchall()
            self.assertEqual(events, [('accepted',), ('validated',), ('recorded',)])
            # A committed but unaudited ticket is invisible to the inner join.
            with connection:
                connection.execute('INSERT INTO tickets(request_key,equipment,days) VALUES (?,?,?)',
                                   ('rent-no-audit', 'saw', 1))
            inner = connection.execute('SELECT COUNT(*), COUNT(DISTINCT tickets.id) FROM tickets '
                                       'JOIN audit ON tickets.id = audit.ticket_id').fetchone()
            left = connection.execute('SELECT COUNT(DISTINCT tickets.id) FROM tickets '
                                      'LEFT JOIN audit ON tickets.id = audit.ticket_id').fetchone()[0]
            self.assertEqual(inner, (3, 1))
            self.assertEqual(left, 2)
            self.assertEqual(LAB.store_counts(connection), {'tickets': 2, 'audit': 3})
        self.assertIn('inner join omits tickets', self.note['transfer'][1]['answer'])


if __name__ == '__main__':
    unittest.main()
