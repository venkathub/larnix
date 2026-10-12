# Phase 1 validation report

Generated from the authoritative JSON records after content validation. Run `python3 scripts/curriculum.py check` from the repository root to verify the current files match the records.

| Check | Result |
| --- | --- |
| Approved modules | 42 / 42 |
| Lessons with all required fields | 168 / 168 |
| Unique interview questions and answer guidance | 168 |
| Unique exercise briefs with acceptance criteria | 168 |
| Source records | 59 |
| Direct prerequisite edges | 225 |
| Unknown prerequisites / dependency cycles | 0 / 0 |
| Unknown source IDs / invalid source URL syntax | 0 / 0 |
| Learning path | All modules once; every dependency precedes its dependent lesson |
| Lesson status | 168 planned; 0 implemented |

## Effort assumptions

Guided study totals approximately 168–336 learner hours. Exercises add 344–688 hours if all are completed. These broad estimates describe learner effort, not an implementation commitment; prior knowledge and compute choices materially affect them.

## What was reviewed

The author reviewed the module-to-lesson mapping for conceptual gaps and repeated exercises, separated metrics from infrastructure health, added early security/evaluation gates, and provided resource alternatives for compute-heavy topics. Every lesson has an original scenario or engineering artifact and explicit review evidence.

## Limits of this report

The checker validates IDs, field completeness, unique questions/exercises, source references, dependency cycles, learning order, local Markdown targets, explicit anchors and generated-file consistency. It does not prove conceptual correctness, universal AI coverage, external link availability, legal compliance or working production systems. Exercise fixtures, solutions, measured benchmarks, learner pilots and independent technical review belong to later phases.
