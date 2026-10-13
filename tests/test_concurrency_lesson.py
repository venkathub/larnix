"""Verify the concurrency preview against the read-only runnable lab."""
import asyncio
from contextlib import redirect_stdout
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

SPEC = importlib.util.spec_from_file_location('concurrency_reference_lab', ROOT / 'labs/service-foundations/lab.py')
LAB = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LAB
SPEC.loader.exec_module(LAB)


class ConcurrencyLessonTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.note = load_notes()['M02-L03']
        self.tickets = json.loads(LAB.FIXTURE.read_text())

    async def test_case_counters_match_instrumented_lab_results(self):
        actual = await asyncio.wait_for(LAB.concurrency_cases(self.tickets), 2)
        for case, key, capacity in zip(self.note['lab']['scenarios'],
                                       ['bounded', 'unlimited', 'cancellation'], [2, 2, 1]):
            with self.subTest(case=key):
                result = actual[key]
                evidence = dict(case['evidence'])
                quoted = dict(re.findall(r'(\w+)=(\d+)', ' '.join(evidence.values())))
                for field in ('max_active', 'active_after'):
                    self.assertEqual(int(quoted[field]), result[field])
                self.assertEqual(int(quoted['capacity']), capacity)
                self.assertEqual([bar['value'] for bar in case['bars']],
                                 [result['max_active'], capacity, result['active_after']])
                self.assertTrue(all(bar['max'] == len(self.tickets) for bar in case['bars']))
                self.assertIn('SYNTHETIC', case['label'])
                if key == 'bounded':
                    for field in ('worker_tasks', 'queue_capacity', 'max_queued'):
                        self.assertEqual(int(quoted[field]), result[field])
                    self.assertEqual(evidence['Returned request keys'].removesuffix(' (input order)').split(', '),
                                     result['request_keys'])
                    self.assertEqual(result['request_keys'], [t['request_key'] for t in self.tickets])
                elif key == 'unlimited':
                    rejection = result['rejection']
                    self.assertEqual(evidence['Rejected audit'], f"{rejection['type']}: {rejection['message']}")
                else:
                    self.assertTrue(result['cancelled'])
                    self.assertIn('cancelled=true; error=' + result['error'], evidence['Probe / cancellation'])
                    self.assertEqual(evidence['Slot reuse'],
                                     f"next_entered={result['next_entered']}; completed={result['completed']}")

    def test_five_ticket_paper_timeline_conserves_requests(self):
        worked = self.note['example']
        self.assertIn('SYNTHETIC paper timeline', worked)
        self.assertIn('not measured scheduling times', worked)
        counts = [tuple(map(int, row)) for row in re.findall(r'\((\d+),(\d+),(\d+),(\d+)\)', worked)]
        self.assertEqual(len(counts), 8)
        for active, waiting, cancelled, completed in counts:
            self.assertEqual(active + waiting + cancelled + completed, 5)
            self.assertLessEqual(active, 2)
        self.assertEqual(counts[1], counts[2])  # cancel request has not cleaned up yet
        self.assertEqual(counts[3], (1, 3, 1, 0))
        self.assertEqual(counts[-1], (0, 0, 1, 4))

    async def test_companion_timeout_and_stream_cleanup_and_permit_reuse(self):
        starter = {'__name__': 'concurrency_starter'}
        exec(compile(self.note['practice']['starter'], 'M02-L03 starter', 'exec'), starter)
        output = StringIO()
        with redirect_stdout(output):
            report = await asyncio.wait_for(starter['probe'](LAB), 3)
        self.assertEqual(json.loads(output.getvalue()), report)
        self.assertEqual(report['lab'], await LAB.concurrency_cases(self.tickets))
        self.assertEqual(report['extensions'], {
            'timeout': {'error': 'TimeoutError', 'active_after': 0},
            'interrupted_stream': {'error': 'CancelledError', 'partial': 1, 'completed': 0, 'active_after': 0},
            'normal_stream': {'partial': 1, 'completed': 1}})
        # Success after two cancellations shares the same semaphore in extensions;
        # test the actual completed chunk too, rather than trusting its summary.
        provider = LAB.MockProvider()
        chunks = [chunk async for chunk in starter['stream_ticket'](
            LAB, provider, asyncio.Semaphore(1), self.tickets[0])]
        self.assertEqual(chunks, [{'kind': 'partial', 'text': 'Checking drill'},
                                 {'kind': 'complete', 'ticket': self.tickets[0]}])
        self.assertEqual((provider.max_active, provider.active), (1, 0))


if __name__ == '__main__':
    unittest.main()
