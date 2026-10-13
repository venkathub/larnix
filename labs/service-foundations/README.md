# Service foundations: original runnable lab

A SYNTHETIC equipment-rental desk receives four booking tickets. Follow one ticket through a JSON contract, a bounded asynchronous client and a transactional SQLite store. These are three independently exercised parts of the same story, not a deployed service or an end-to-end HTTP server. The artifact supports M02-L02–L04; it does not complete their nine-part lesson contracts.

## Reproduce

Target: Python 3.12. Tested locally with Python 3.12.13 and 3.14.4. Standard library only; no installation or network access is needed. From this directory:

```sh
python3 -I -m unittest discover -s . -p 'test_*.py'
python3 -I lab.py --output /tmp/larnix-service-first
python3 -I lab.py --output /tmp/larnix-service-second
cmp /tmp/larnix-service-first/report.json /tmp/larnix-service-second/report.json
```

Use the same Python executable for both runs. `report.json` is the only output. It records actual Python and SQLite versions, the SHA-256 of `fixtures/tickets.json`, contract responses, active-request counts, rollback/replay counts and exact rejected errors. It contains no timestamp or elapsed-time measurement. Different Python/SQLite versions intentionally change the version fields; byte-identical output is promised for repeated runs in the same environment, not across environments. The database is in memory and is closed after each demonstration.

## Predict before running

1. The four tickets are `rent-001` through `rent-004`, for drill/saw/pump/drill, with day counts `[2, 1, 3, 2]`. What status should a malformed JSON body, string duration `"2"`, unsupported version `2`, and valid version `1` receive? Should a status 200 with a string duration pass the client?
2. With capacity **2**, queue size **2**, and **3 fixed workers**, how many provider requests can be active together? Compare starting all four tasks immediately. With capacity **1**, cancel the first ticket while the second waits: does the second get the slot?
3. A ticket insert crashes before its audit insert. How many rows remain? A later request commits, but its response is lost; retry the same request key. How many tickets and audit rows exist after replay? What does joining one ticket to its three audit rows count?

Expected values:

- Statuses are **400**, **422**, **400**, **200** respectively. The invalid 200 is rejected. A JSON number `2` is accepted; a string `"2"` or boolean `true` is not.
- The bounded run completes **4** tickets in input order, reaches **2** active requests and at most **2** queued items, then returns to **0** active. There are **3** worker tasks regardless of input size; the semaphore limits in-flight provider calls. The deliberately unlimited run reaches **4 > 2** active requests and fails the capacity audit.
- Cancellation propagates `CancelledError`, releases the semaphore, lets `rent-002` enter and finish, and leaves **0** active. Its maximum is **1**.
- The crash leaves **0 tickets / 0 audits**. After the committed response is lost: **1 / 3**. Replay returns ticket ID **1**, `replayed=true`, and leaves **1 / 3**. Direct duplicate insertion and a changed payload using the same key are rejected. The join has **3 rows**, but **1 distinct ticket**.

## Inspect and explain

### Contract: parse, validate, then check the version

`handle()` accepts a JSON body plus the `X-Larnix-Version` header and returns a small HTTP-shaped response. It is called in-process: no socket, DNS lookup or external provider. Request header names are case-insensitive. Its response helper emits one canonical header spelling, used by the in-process client. An unsupported or missing contract version is a 400 bad request with its own error reason; it is not an HTTP protocol upgrade. The versioned ticket schema has exactly three fields: nonempty string `request_key`, nonempty string `equipment`, and positive integer `days`.

`accept_response()` checks the response version, parses the body and validates the envelope and ticket even for status 200. Parsing JSON alone proves neither field types nor compatibility. The contract handler does not store a ticket; the separate persistence case owns that boundary.

### Concurrency: limit waiting work and active calls

`bounded_client()` puts tickets into a bounded `asyncio.Queue`; a fixed set of workers acquires an `asyncio.Semaphore` before entering the mock provider. The extra worker makes the semaphore's effect observable. `TaskGroup` cancels sibling workers if one fails, and `finally` releases queue bookkeeping and the provider counter. `limited_request()` uses the semaphore context manager so cancellation also releases the slot.

The slow provider cooperatively yields control; the cancellation case uses an event gate to hold a request until it is cancelled. These controlled waits establish interleaving without wall-clock timing. Counters measure active calls in this simulation, not requests per second. The broken path intentionally bypasses both limits; the capacity audit then raises an explicit error. It illustrates overload detection, not an overload prevention mechanism. Inputs, ordered results and diagnostic events remain in memory: this is not a constant-memory streaming client.

### Persistence: a transaction and a stable request key

`store_ticket()` parameterizes SQL and uses one connection transaction for a ticket plus three audit events (`accepted`, `validated`, `recorded`). An injected exception between writes rolls back the ticket. The database uniqueness constraint protects `request_key`; `ingest()` also checks that a replay has the same equipment and days before returning the existing ID. A different payload must use a new key.

The lost response is injected **after commit**. The client cannot infer rollback from silence. Retrying the stable key finds the existing ticket without adding audit rows. The pre-read followed by insert is a single-client teaching example: concurrent independent connections could race, and the uniqueness constraint would reject one insert rather than magically turn it into a successful replay.

A one-to-many audit join repeats the ticket three times. `COUNT(DISTINCT tickets.id)` answers the ticket-count question; `COUNT(*)` answers the joined-row question. The report rejects interpreting the latter as the former.

## Injected failures and exact errors

| Injection | Observed rejection |
| --- | --- |
| Malformed JSON | `ContractError: HTTP 400: malformed JSON` |
| String duration | `ContractError: HTTP 422: days must be a positive integer` |
| Incompatible version | `ContractError: HTTP 400: unsupported contract version; expected 1` |
| Invalid data in a 200 | `ContractError: invalid 200 ticket: days must be a positive integer` |
| Unlimited tasks | `CapacityExceeded: provider capacity exceeded: observed 4 > 2` |
| Crash between writes | `InjectedCrash: crash after ticket insert, before audit insert` |
| Direct duplicate key | `DuplicateRequest: duplicate request key: rent-001` |
| Changed payload on replay | `DuplicateRequest: request key reused with different ticket: rent-001` |
| Joined rows treated as ticket count | `JoinCardinalityError: joined rows are not ticket count: 3 != 1` |

The recovery demonstrations also observe `CancelledError` (with no message) and `LostResponse: response lost after commit; outcome unknown to client`. Neither is swallowed as success: the cancelled request stays cancelled, and only an explicit replay establishes the committed record. Tests additionally cover blank/missing fields, boolean durations, invalid response JSON/version, worker failure and cancellation of the whole pipeline, and rollback while preserving an earlier committed ticket.

## What this does not show

- No real provider, HTTP transport, authentication, TLS, network timeout policy or retry/backoff policy. Network scope is loopback only if a transport is added; this implementation opens no sockets and uses in-process handler calls.
- SQLite is not PostgreSQL. This does not demonstrate PostgreSQL isolation levels, connection pools, concurrent server failures or cross-process transaction races.
- The crash is a Python exception in an in-memory SQLite transaction, not a power failure, disk durability test or distributed exactly-once delivery guarantee.
- Controlled synthetic waits and four invented tickets are not a performance benchmark, production capacity estimate or fairness result.
- Not learner-validated. This runnable artifact does not establish the complete lesson contract or production readiness.

Extend the fixture only after predicting the new counts. Try a conflicting replay and explain why a stable key identifies an operation, not just a successful HTTP exchange.

Primary readings: Python 3.12 [semaphores](https://docs.python.org/3.12/library/asyncio-sync.html#asyncio.Semaphore), [queues](https://docs.python.org/3.12/library/asyncio-queue.html), and [SQLite connection transactions](https://docs.python.org/3.12/library/sqlite3.html#how-to-use-the-connection-context-manager). The scenario, fixture and implementation here are original.
