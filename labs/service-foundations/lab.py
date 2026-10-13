#!/usr/bin/env python3
"""Original SYNTHETIC rental-desk contract, concurrency and transaction lab."""
import argparse
import asyncio
from contextlib import closing
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import platform
import sqlite3

FIXTURE = Path(__file__).parent / 'fixtures' / 'tickets.json'
VERSION_HEADER = 'X-Larnix-Version'
VERSION = '1'


class ContractError(ValueError):
    pass


class CapacityExceeded(ValueError):
    pass


class InjectedCrash(RuntimeError):
    pass


class LostResponse(RuntimeError):
    pass


class DuplicateRequest(ValueError):
    pass


class JoinCardinalityError(ValueError):
    pass


@dataclass
class Response:
    status: int
    headers: dict
    body: str


def validate_ticket(ticket):
    if not isinstance(ticket, dict) or set(ticket) != {'request_key', 'equipment', 'days'}:
        raise ContractError('ticket must contain exactly request_key, equipment, days')
    for field in ('request_key', 'equipment'):
        if not isinstance(ticket[field], str) or not ticket[field].strip():
            raise ContractError(f'{field} must be a nonempty string')
    # bool is an int subclass; True is not a rental duration.
    if type(ticket['days']) is not int or ticket['days'] < 1:
        raise ContractError('days must be a positive integer')
    return dict(ticket)


def response(status, data):
    return Response(status, {VERSION_HEADER: VERSION}, json.dumps(data, sort_keys=True))


def handle(body, headers):
    """HTTP-shaped boundary called in-process, with no transport or database writes."""
    try:
        ticket = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {'error': 'malformed JSON'})
    try:
        ticket = validate_ticket(ticket)
    except ContractError as exc:
        return response(422, {'error': str(exc)})
    version = next((v for k, v in headers.items() if k.lower() == VERSION_HEADER.lower()), None)
    if version != VERSION:
        return response(426, {'error': 'unsupported contract version; expected 1'})
    return response(200, {'accepted': True, 'ticket': ticket})


def accept_response(reply):
    """A success status is necessary, but does not establish a valid payload."""
    if reply.headers.get(VERSION_HEADER) != VERSION:
        raise ContractError('unsupported response version; expected 1')
    try:
        data = json.loads(reply.body)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ContractError('response must be valid JSON') from exc
    if reply.status != 200:
        reason = data.get('error', 'invalid error body') if isinstance(data, dict) else 'invalid error body'
        raise ContractError(f'HTTP {reply.status}: {reason}')
    if not isinstance(data, dict) or set(data) != {'accepted', 'ticket'} or data['accepted'] is not True:
        raise ContractError('200 response must contain accepted=true and ticket')
    try:
        return validate_ticket(data['ticket'])
    except ContractError as exc:
        raise ContractError(f'invalid 200 ticket: {exc}') from exc


class MockProvider:
    """Cooperative waits model a slow provider; no throughput is measured."""
    def __init__(self, gate=None):
        self.active = 0
        self.max_active = 0
        self.gate = gate
        self.entered = asyncio.Queue()

    async def request(self, ticket):
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        self.entered.put_nowait(ticket['request_key'])
        try:
            if self.gate is None:
                await asyncio.sleep(0)
                await asyncio.sleep(0)
            else:
                await self.gate.wait()
            return accept_response(handle(json.dumps(ticket), {VERSION_HEADER: VERSION}))
        finally:
            self.active -= 1


def check_capacity(observed, capacity):
    if observed > capacity:
        raise CapacityExceeded(f'provider capacity exceeded: observed {observed} > {capacity}')


async def limited_request(provider, semaphore, ticket):
    async with semaphore:
        return await provider.request(ticket)


async def bounded_client(tickets, capacity, provider):
    if type(capacity) is not int or capacity < 1:
        raise ValueError('capacity must be a positive integer')
    queue = asyncio.Queue(maxsize=capacity)
    semaphore = asyncio.Semaphore(capacity)
    results = [None] * len(tickets)
    # One extra worker makes the semaphore (rather than worker count) limit requests.
    workers = capacity + 1
    max_queued = 0

    async def worker():
        while True:
            item = await queue.get()
            try:
                if item is None:
                    return
                index, ticket = item
                results[index] = await limited_request(provider, semaphore, ticket)
            finally:
                queue.task_done()

    # TaskGroup cancels siblings and the producer if a worker fails.
    async with asyncio.TaskGroup() as group:
        for _ in range(workers):
            group.create_task(worker())
        for index, ticket in enumerate(tickets):
            await queue.put((index, ticket))
            max_queued = max(max_queued, queue.qsize())
        for _ in range(workers):
            await queue.put(None)
        await queue.join()
    check_capacity(provider.max_active, capacity)
    return {'request_keys': [t['request_key'] for t in results],
            'capacity': capacity, 'worker_tasks': workers, 'queue_capacity': capacity,
            'max_queued': max_queued, 'max_active': provider.max_active,
            'active_after': provider.active}


async def cancellation_case(tickets):
    gate = asyncio.Event()
    provider = MockProvider(gate)
    semaphore = asyncio.Semaphore(1)
    tasks = []
    try:
        first = asyncio.create_task(limited_request(provider, semaphore, tickets[0]))
        tasks.append(first)
        await asyncio.wait_for(provider.entered.get(), 2)
        waiting = asyncio.Event()

        async def follower():
            waiting.set()
            return await limited_request(provider, semaphore, tickets[1])

        second = asyncio.create_task(follower())
        tasks.append(second)
        await waiting.wait()  # Follower now waits at the occupied semaphore.
        first.cancel()
        try:
            await first
        except asyncio.CancelledError:
            cancelled = True
        else:
            raise AssertionError('injected cancellation was not propagated')
        entered = await asyncio.wait_for(provider.entered.get(), 2)
        gate.set()
        completed = await second
        return {'cancelled': cancelled, 'error': 'CancelledError', 'capacity': 1,
                'next_entered': entered, 'completed': completed['request_key'],
                'max_active': provider.max_active, 'active_after': provider.active}
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


def rejection(expected_type, operation):
    try:
        operation()
    except expected_type as exc:
        return {'type': type(exc).__name__, 'message': str(exc)}
    raise AssertionError(f'injected failure did not raise {expected_type.__name__}')


async def concurrency_cases(tickets):
    bounded = await bounded_client(tickets, 2, MockProvider())
    unlimited = MockProvider()
    # Deliberately broken: one immediately started task per input, without a limit.
    await asyncio.gather(*(unlimited.request(ticket) for ticket in tickets))
    failure = rejection(CapacityExceeded, lambda: check_capacity(unlimited.max_active, 2))
    return {'bounded': bounded, 'unlimited': {'max_active': unlimited.max_active,
            'active_after': unlimited.active, 'rejection': failure},
            'cancellation': await cancellation_case(tickets)}


def open_store():
    connection = sqlite3.connect(':memory:')
    connection.execute('PRAGMA foreign_keys = ON')
    connection.executescript('''
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY,
            request_key TEXT NOT NULL UNIQUE,
            equipment TEXT NOT NULL,
            days INTEGER NOT NULL CHECK (days > 0)
        );
        CREATE TABLE audit (
            id INTEGER PRIMARY KEY,
            ticket_id INTEGER NOT NULL REFERENCES tickets(id),
            event TEXT NOT NULL
        );
    ''')
    return connection


def store_ticket(connection, ticket, crash=False):
    ticket = validate_ticket(ticket)
    try:
        with connection:
            cursor = connection.execute(
                'INSERT INTO tickets(request_key, equipment, days) VALUES (?, ?, ?)',
                (ticket['request_key'], ticket['equipment'], ticket['days']))
            ticket_id = cursor.lastrowid
            if crash:
                raise InjectedCrash('crash after ticket insert, before audit insert')
            connection.executemany('INSERT INTO audit(ticket_id, event) VALUES (?, ?)',
                                   [(ticket_id, event) for event in ('accepted', 'validated', 'recorded')])
    except sqlite3.IntegrityError as exc:
        if connection.execute('SELECT 1 FROM tickets WHERE request_key = ?',
                              (ticket['request_key'],)).fetchone():
            raise DuplicateRequest(f"duplicate request key: {ticket['request_key']}") from exc
        raise
    return ticket_id


def ingest(connection, ticket, lose_response=False):
    ticket = validate_ticket(ticket)
    previous = connection.execute('SELECT id, equipment, days FROM tickets WHERE request_key = ?',
                                  (ticket['request_key'],)).fetchone()
    if previous:
        if previous[1:] != (ticket['equipment'], ticket['days']):
            raise DuplicateRequest(f"request key reused with different ticket: {ticket['request_key']}")
        return {'ticket_id': previous[0], 'replayed': True}
    ticket_id = store_ticket(connection, ticket)
    if lose_response:
        raise LostResponse('response lost after commit; outcome unknown to client')
    return {'ticket_id': ticket_id, 'replayed': False}


def store_counts(connection):
    return {'tickets': connection.execute('SELECT COUNT(*) FROM tickets').fetchone()[0],
            'audit': connection.execute('SELECT COUNT(*) FROM audit').fetchone()[0]}


def check_join_count(joined_rows, tickets):
    if joined_rows != tickets:
        raise JoinCardinalityError(f'joined rows are not ticket count: {joined_rows} != {tickets}')


def persistence_cases(ticket):
    with closing(open_store()) as connection:
        crash = rejection(InjectedCrash, lambda: store_ticket(connection, ticket, crash=True))
        after_crash = store_counts(connection)
        lost = rejection(LostResponse, lambda: ingest(connection, ticket, lose_response=True))
        after_lost = store_counts(connection)
        replay = ingest(connection, ticket)
        duplicate = rejection(DuplicateRequest, lambda: store_ticket(connection, ticket))
        conflict = rejection(DuplicateRequest, lambda: ingest(connection, {**ticket, 'days': 9}))
        joined, distinct = connection.execute('''SELECT COUNT(*), COUNT(DISTINCT tickets.id)
            FROM tickets JOIN audit ON tickets.id = audit.ticket_id''').fetchone()
        wrong_count = rejection(JoinCardinalityError, lambda: check_join_count(joined, distinct))
        return {'after_crash': after_crash, 'after_lost_response': after_lost,
                'replay': replay, 'after_replay_and_rejections': store_counts(connection),
                'joined_rows': joined, 'distinct_tickets': distinct,
                'rejected_failures': {'crash_between_writes': crash, 'duplicate_key': duplicate,
                                      'conflicting_replay': conflict, 'join_as_ticket_count': wrong_count},
                'lost_response': lost}


def contract_cases(ticket):
    good_body = json.dumps(ticket)
    cases = {'malformed_json': handle('{', {VERSION_HEADER: VERSION}),
             'wrong_field_type': handle(json.dumps({**ticket, 'days': '2'}), {VERSION_HEADER: VERSION}),
             'incompatible_version': handle(good_body, {VERSION_HEADER: '2'})}
    failures = {key: rejection(ContractError, lambda reply=reply: accept_response(reply))
                for key, reply in cases.items()}
    invalid = response(200, {'accepted': True, 'ticket': {**ticket, 'days': '2'}})
    failures['invalid_200'] = rejection(ContractError, lambda: accept_response(invalid))
    valid = handle(good_body, {VERSION_HEADER: VERSION})
    return {'statuses': {**{key: reply.status for key, reply in cases.items()}, 'valid': valid.status},
            'accepted_ticket': accept_response(valid), 'rejected_failures': failures}


def run(output):
    raw = FIXTURE.read_bytes()
    tickets = [validate_ticket(ticket) for ticket in json.loads(raw)]
    report = {'label': 'SYNTHETIC: in-process teaching fixture, not a benchmark',
              'versions': {'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version},
              'fixture_sha256': hashlib.sha256(raw).hexdigest(),
              'contract': contract_cases(tickets[0]),
              'concurrency': asyncio.run(concurrency_cases(tickets)),
              'persistence': persistence_cases(tickets[0])}
    destination = Path(output)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    run(parser.parse_args().output)
