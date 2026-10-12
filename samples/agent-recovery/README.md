# Agent recovery lesson · M21-L02

Original narrative and interactive simulation: **The refund that happened twice**. Follows the approved explanation style and M21-L02 curriculum plan. The reference project was not forked or imported.

Use the integrated platform at `/lessons/M21-L02/` after `python3 scripts/build_site.py`. For standalone use, serve the entire `samples` directory, then open `/agent-recovery/`; the shared stylesheet and quiz component live in sibling directories.

## What is implemented

- Seven scenario presets; four crash boundaries; blind versus reconciled recovery.
- Step controls reveal durable intent, volatile receipt and separate provider ledger.
- Three explanatory checks, original worked trace, failure cases, glossary, interview discussion and downloadable Python starter with ten fixture cases.
- Shared platform theme, quiz persistence, navigation and self-reported progress.

The engine is pure JavaScript. It precomputes frames; no durable workflow runtime, concurrency, real payment service, network request or model inference runs. The provider retains keys indefinitely and atomically associates each effect with its key and receipt. Lookup is authoritative when available. A failed lookup causes a conservative hold; other valid provider contracts may permit a same-key retry. A completed checkpoint resumes its saved outcome regardless of pending-retry controls.

## Verification

Run `make check` from the repository root. Engine tests compare ten independent fixtures, crash-state separation, stable receipt binding, deliberate duplicate effects, repeated recovery, outage recovery, mismatched receipts, invalid inputs and immutable snapshots. Browser review covers step controls, failure presets, persisted checks and desktop/mobile layouts.

The Python starter is intentionally unfinished. Learners must implement it and extend it to two SQLite stores with process termination, racing attempts, delayed replies and migration tests. Browser results do not establish those production guarantees.

Sources reviewed October 12, 2026: [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [Temporal workflow execution](https://docs.temporal.io/workflow-execution), [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests). The mock lookup contract and rental story are original teaching fixtures, not a vendor API tutorial.
