"""Offline failure and recovery checks for the synthetic rental desk."""
import asyncio
from contextlib import closing
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from lab import (FIXTURE, VERSION_HEADER, ContractError, DuplicateRequest, InjectedCrash,
                 LostResponse, MockProvider, accept_response, bounded_client,
                 concurrency_cases, contract_cases, handle, ingest, open_store, persistence_cases,
                 response, store_counts, store_ticket, validate_ticket)


class ContractTest(unittest.TestCase):
    def setUp(self):
        self.ticket = json.loads(FIXTURE.read_text())[0]

    def test_status_and_body_contract_for_each_request_failure(self):
        report = contract_cases(self.ticket)
        self.assertEqual(report['statuses'], {'malformed_json': 400, 'wrong_field_type': 422,
                                             'incompatible_version': 426, 'valid': 200})
        self.assertEqual(report['accepted_ticket'], self.ticket)
        self.assertEqual(report['rejected_failures']['invalid_200']['message'],
                         'invalid 200 ticket: days must be a positive integer')
        self.assertEqual(handle(json.dumps(self.ticket), {}).status, 426)
        self.assertEqual(handle(json.dumps(self.ticket), {'x-larnix-version': '1'}).status, 200)

    def test_field_validation_rejects_bool_null_missing_and_extra(self):
        for days in (True, None, 0, -1, 1.5, '2'):
            with self.subTest(days=days), self.assertRaisesRegex(ContractError, 'positive integer'):
                validate_ticket({**self.ticket, 'days': days})
        for ticket in ([], None, {}, {**self.ticket, 'extra': 1}):
            with self.subTest(ticket=ticket), self.assertRaises(ContractError):
                validate_ticket(ticket)
        for key in ('request_key', 'equipment'):
            for value in ('', ' ', None, 3):
                with self.subTest(key=key, value=value), self.assertRaises(ContractError):
                    validate_ticket({**self.ticket, key: value})

    def test_client_rejects_success_with_invalid_json_schema_or_version(self):
        for body in ([], {}, {'accepted': 1, 'ticket': self.ticket},
                     {'accepted': True, 'ticket': {'days': 2}}):
            with self.subTest(body=body), self.assertRaises(ContractError):
                accept_response(response(200, body))
        bad = response(200, {'accepted': True, 'ticket': self.ticket})
        bad.body = '{'
        with self.assertRaisesRegex(ContractError, 'response must be valid JSON'):
            accept_response(bad)
        bad.headers[VERSION_HEADER] = '2'
        with self.assertRaisesRegex(ContractError, 'unsupported response version'):
            accept_response(bad)


class ConcurrencyTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tickets = json.loads(FIXTURE.read_text())

    async def test_bounded_queue_and_semaphore_preserve_all_tickets(self):
        for capacity in (1, 2, 3):
            with self.subTest(capacity=capacity):
                provider = MockProvider()
                result = await asyncio.wait_for(bounded_client(self.tickets, capacity, provider), 2)
                self.assertEqual(result['request_keys'], [t['request_key'] for t in self.tickets])
                self.assertEqual(result['max_active'], capacity)
                self.assertLessEqual(result['max_queued'], capacity)
                self.assertEqual(result['active_after'], 0)
        self.assertEqual((await bounded_client([], 2, MockProvider()))['request_keys'], [])
        for capacity in (0, -1, True):
            with self.assertRaisesRegex(ValueError, 'capacity must be a positive integer'):
                await bounded_client(self.tickets, capacity, MockProvider())

    async def test_unlimited_creation_is_detected_and_cancelled_slot_is_reused(self):
        result = await asyncio.wait_for(concurrency_cases(self.tickets), 2)
        self.assertEqual(result['unlimited']['max_active'], 4)
        self.assertEqual(result['unlimited']['active_after'], 0)
        self.assertEqual(result['unlimited']['rejection'], {
            'type': 'CapacityExceeded', 'message': 'provider capacity exceeded: observed 4 > 2'})
        self.assertEqual(result['cancellation'], {
            'cancelled': True, 'error': 'CancelledError', 'capacity': 1,
            'next_entered': 'rent-002', 'completed': 'rent-002', 'max_active': 1, 'active_after': 0})

    async def test_worker_failure_and_pipeline_cancellation_leave_no_active_requests(self):
        provider = MockProvider()
        with self.assertRaises(ExceptionGroup) as caught:
            await asyncio.wait_for(bounded_client([{'request_key': 'invalid'}] + self.tickets, 2, provider), 2)
        self.assertTrue(any(isinstance(exc, ContractError) for exc in caught.exception.exceptions))
        self.assertEqual(provider.active, 0)
        blocked = MockProvider(asyncio.Event())
        task = asyncio.create_task(bounded_client(self.tickets * 4, 2, blocked))
        await asyncio.wait_for(blocked.entered.get(), 2)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(blocked.active, 0)


class PersistenceTest(unittest.TestCase):
    def setUp(self):
        self.ticket = json.loads(FIXTURE.read_text())[0]

    def test_crash_rolls_back_both_writes_without_losing_existing_ticket(self):
        with closing(open_store()) as connection:
            store_ticket(connection, self.ticket)
            with self.assertRaisesRegex(InjectedCrash, 'crash after ticket insert, before audit insert'):
                store_ticket(connection, {**self.ticket, 'request_key': 'rent-new'}, crash=True)
            self.assertEqual(store_counts(connection), {'tickets': 1, 'audit': 3})
            self.assertIsNone(connection.execute("SELECT id FROM tickets WHERE request_key='rent-new'").fetchone())

    def test_lost_response_replays_same_record_and_conflicting_key_is_rejected(self):
        with closing(open_store()) as connection:
            with self.assertRaisesRegex(LostResponse, 'response lost after commit'):
                ingest(connection, self.ticket, lose_response=True)
            self.assertEqual(store_counts(connection), {'tickets': 1, 'audit': 3})
            for _ in range(2):
                self.assertEqual(ingest(connection, self.ticket), {'ticket_id': 1, 'replayed': True})
            with self.assertRaisesRegex(DuplicateRequest, 'duplicate request key: rent-001'):
                store_ticket(connection, self.ticket)
            with self.assertRaisesRegex(DuplicateRequest, 'request key reused with different ticket: rent-001'):
                ingest(connection, {**self.ticket, 'days': 9})
            self.assertEqual(store_counts(connection), {'tickets': 1, 'audit': 3})
            new = {**self.ticket, 'request_key': "desk's-next"}
            self.assertEqual(ingest(connection, new), {'ticket_id': 2, 'replayed': False})
            self.assertEqual(store_counts(connection), {'tickets': 2, 'audit': 6})

    def test_three_audits_multiply_join_rows_but_not_distinct_ticket_count(self):
        report = persistence_cases(self.ticket)
        self.assertEqual(report['after_crash'], {'tickets': 0, 'audit': 0})
        self.assertEqual(report['after_replay_and_rejections'], {'tickets': 1, 'audit': 3})
        self.assertEqual((report['joined_rows'], report['distinct_tickets']), (3, 1))
        self.assertEqual(report['rejected_failures']['join_as_ticket_count'], {
            'type': 'JoinCardinalityError', 'message': 'joined rows are not ticket count: 3 != 1'})


class ReproductionTest(unittest.TestCase):
    def test_two_isolated_processes_write_identical_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('first', 'second'):
                subprocess.run([sys.executable, '-I', str(FIXTURE.parents[1] / 'lab.py'),
                                '--output', str(root / name)], check=True, timeout=10)
            self.assertEqual((root / 'first/report.json').read_bytes(), (root / 'second/report.json').read_bytes())
            report = json.loads((root / 'first/report.json').read_text())
            self.assertEqual(report['concurrency']['bounded']['max_active'], 2)
            self.assertEqual(report['persistence']['after_replay_and_rejections'], {'tickets': 1, 'audit': 3})

    def test_demonstrations_open_no_network_connections(self):
        from lab import run
        with tempfile.TemporaryDirectory() as directory, \
                patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
                patch('socket.socket.connect', side_effect=AssertionError('network forbidden')):
            run(directory)


if __name__ == '__main__':
    unittest.main()
