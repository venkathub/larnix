"""Learner starter: implement mock recovery, then extend it to durable SQLite stores.

Download fixtures.json beside this file and run python3 exercise.py.
No payment service, model, API key or third-party package is needed.
This starter intentionally has no working recovery implementation.
"""
import json
from pathlib import Path


def recover_case(config):
    """Simulate one authorized INR 500 refund for rental R-104.

    Defaults: crash='commit', policy='safe', lookupOnline=True,
    payloadChanged=False. Use key refund-R104-01 and receipt-1.

    Crash points: before (no dispatch); commit (effect recorded, no reply);
    receipt (reply in memory, not saved); saved (receipt checkpointed).
    A crash drops process memory but preserves intent and provider ledger.

    Recovery: if already done, return saved receipt without calling again.
    Otherwise safe policy blocks changed intent (500 -> 700), holds when
    lookup is unavailable, and reconciles the original operation receipt.
    If authoritative lookup finds no receipt, submit with the original key.
    Bind receipt to operation ID, amount, currency and rental before saving.
    Blind policy ignores lookup and submits with a fresh key, possibly 700
    if payloadChanged. The mock permits duplicates to expose the failure.

    Return status, effectCount, total, calls, checkpointStatus, receiptId.
    'incorrect' means one effect with the wrong amount (blind changed retry
    before dispatch). Duplicates take precedence when there are two effects.
    'calls' counts effect submissions, not receipt reads. 'done' can hide
    duplicates in the intentionally broken blind baseline.

    Extension: two SQLite stores, atomic provider deduplication, injected
    process termination, concurrent attempts, schema migration, retention
    boundary and repeated crashes. Capture evidence from fresh processes.
    """
    raise NotImplementedError('Implement recovery and run the fixture report.')


def main():
    fixture = json.loads(Path(__file__).with_name('fixtures.json').read_text())
    failures = 0
    for case in fixture['cases']:
        actual = recover_case(case['config'])
        differences = {key: {'expected': value, 'actual': actual.get(key)}
                       for key, value in case['expected'].items()
                       if actual.get(key) != value}
        print(case['name'], 'FAIL' if differences else 'PASS')
        if differences:
            failures += 1
            print(json.dumps(differences, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
