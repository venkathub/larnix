"""Keep the service-contract preview's authored traces tied to the read-only lab."""
from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_foundations import load_notes

SPEC = importlib.util.spec_from_file_location('contract_reference_lab', ROOT / 'labs/service-foundations/lab.py')
LAB = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LAB
SPEC.loader.exec_module(LAB)


class ContractLessonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.note = load_notes()['M02-L02']
        cls.ticket = json.loads(LAB.FIXTURE.read_text())[0]
        cls.starter = {'__name__': 'contract_starter'}
        exec(compile(cls.note['practice']['starter'], 'M02-L02 starter', 'exec'), cls.starter)

    def test_three_case_request_response_pairs_match_the_lab(self):
        for case, passed, status in zip(self.note['lab']['scenarios'], [0, 1, 3], [400, 422, 200]):
            with self.subTest(case=case['label']):
                evidence = dict(case['evidence'])
                header, body = evidence['Request'].split('\n', 1)
                name, value = header.split(': ', 1)
                actual = LAB.handle(body, {name: value})
                quoted_status, quoted_body = evidence['Response'].split('\n', 1)
                self.assertEqual(int(quoted_status), actual.status)
                self.assertEqual(actual.status, status)
                self.assertEqual(json.loads(quoted_body), json.loads(actual.body))
                self.assertEqual(quoted_body, json.dumps(json.loads(quoted_body), indent=2))
                if status == 400:
                    self.assertEqual(body, '{')  # Deliberately malformed, not repaired for display.
                else:
                    self.assertEqual(body, json.dumps(json.loads(body), indent=2))
                self.assertEqual(actual.headers, {'X-Larnix-Version': '1'})
                self.assertEqual([bar['value'] for bar in case['bars']], [passed, 3 - passed])
                self.assertTrue(all(bar['max'] == 3 for bar in case['bars']))
                self.assertIn(f'{passed} / 3 passed; {3 - passed} remaining', evidence['Checks / accepted tickets'])
                self.assertIn('SYNTHETIC', case['label'])
                if status == 200:
                    self.assertEqual(LAB.accept_response(actual), self.ticket)
                else:
                    with self.assertRaises(LAB.ContractError):
                        LAB.accept_response(actual)

    def test_worked_version_and_invalid_success_traces_match_the_lab(self):
        raw = json.dumps(self.ticket)
        compact = lambda value: json.dumps(value, separators=(',', ':'))
        worked = self.note['example']
        for headers in ({}, {'X-Larnix-Version': '2'}):
            reply = LAB.handle(raw, headers)
            self.assertEqual(reply.status, 400)
            reason = json.loads(reply.body)['error']
            self.assertEqual(reason, 'unsupported contract version; expected 1')
            self.assertIn(f'{reply.status} and {reason}', worked)
            self.assertIn(reason, self.note['lab']['scenarios'][2]['why'])
            self.assertIn(f'400 with {compact(json.loads(reply.body))}', self.note['transfer'][1]['answer'])
        invalid = LAB.response(200, {'accepted': True, 'ticket': {**self.ticket, 'days': '2'}})
        with self.assertRaises(LAB.ContractError) as caught:
            LAB.accept_response(invalid)
        self.assertIn(f'ContractError: {caught.exception}', worked)
        self.assertIn(str(caught.exception), self.note['checks'][1]['explanation'])

    def test_listing_matches_all_three_pretty_exchanges_and_fits_the_column(self):
        expected = []
        for index, case in enumerate(self.note['lab']['scenarios']):
            rows = dict(case['evidence'])
            header, body = rows['Request'].split('\n', 1)
            status, response = rows['Response'].split('\n', 1)
            if expected:
                expected.append('')
            expected.extend([
                case['label'], 'Request', header,
                'Body (deliberately malformed):' if index == 0 else 'Body:',
                *body.splitlines(), 'Response', 'Status: ' + status,
                'X-Larnix-Version: 1', 'Body:', *response.splitlines()])
        self.assertEqual(self.note['listing']['language'], 'text')
        self.assertEqual(self.note['listing']['lines'], expected)
        self.assertTrue(all(len(line) < 60 for line in expected))

    def test_typed_starter_executes_all_five_cases_and_rejects_invalid_200(self):
        output = StringIO()
        with redirect_stdout(output):
            rows = self.starter['probe'](LAB)
        self.assertEqual([row[1] for row in rows], [400, 422, 400, 400, 200])
        self.assertEqual([row[2].get('error') for row in rows], [
            'malformed JSON', 'days must be a positive integer',
            'unsupported contract version; expected 1', 'unsupported contract version; expected 1', None])
        self.assertEqual(rows[-1][2], {'accepted': True, 'ticket': self.ticket})
        self.assertEqual(rows[-1][3], 'accepted rent-001')
        self.assertIn('invalid 200 rejected: invalid 200 ticket: days must be a positive integer', output.getvalue())
        for ticket in ({'days': 2}, {**self.ticket, 'days': True}):
            with self.assertRaises(LAB.ContractError):
                self.starter['checked_ticket'](LAB, LAB.handle(json.dumps(ticket), {'X-Larnix-Version': '1'}))
        reply = LAB.response(200, {'accepted': True, 'ticket': self.ticket})
        reply.headers['X-Larnix-Version'] = '2'
        with self.assertRaisesRegex(LAB.ContractError, 'unsupported response version; expected 1'):
            self.starter['checked_ticket'](LAB, reply)


if __name__ == '__main__':
    unittest.main()
