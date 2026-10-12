"""Learner starter, not a completed RAG implementation.

Place fixtures.json beside this file. Implement run_pipeline(), then run:
    python3 exercise.py
No model API or third-party packages required.
"""
import json
from pathlib import Path


def run_pipeline(documents, questions, as_of, config):
    """Return status, context (IDs), claimCitations, missing, conflicts, stale.

    1. Follow the question's fixed order, keep available IDs, take topK.
    2. If currentOnly, filter by inclusive from/to dates before packing.
    3. Keep the first `slots` eligible passages. Do not backfill retrieval.
    4. Check each required field for absence or conflicting values.
    5. Withhold claims if there is a conflict; otherwise trace each
       supported field to all matching context IDs. Incomplete answers
       abstain, but can report supported fragments separately.
    6. Run a separate date audit even when currentOnly is disabled.

    Add a per-stage trace and plain-language answer as your own extension.
    The expected status 'answer' is the mock's status, not a correctness
    verdict: the expired-but-cited case intentionally answers incorrectly
    for the reference date. Its stale list must catch the problem.
    """
    raise NotImplementedError('Implement the pipeline before running the fixture report.')


def main():
    fixture = json.loads(Path(__file__).with_name('fixtures.json').read_text())
    failures = 0
    for case in fixture['cases']:
        actual = run_pipeline(fixture['documents'], fixture['questions'],
                              fixture['asOf'], case['config'])
        differences = {key: {'expected': expected, 'actual': actual.get(key)}
                       for key, expected in case['expected'].items()
                       if actual.get(key) != expected}
        print(case['name'], 'FAIL' if differences else 'PASS')
        if differences:
            failures += 1
            print(json.dumps(differences, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
