# Phase 1 validation report

Generated from the authoritative JSON records after content validation. Run `python3 scripts/curriculum.py check` from the repository root to verify the current files match the records.

| Check | Result |
| --- | --- |
| Approved modules | 42 / 42 |
| Lessons with all required fields | 188 / 188 |
| Unique interview questions and answer guidance | 188 |
| Unique exercise briefs with acceptance criteria | 188 |
| Source records | 99 |
| Direct prerequisite edges | 259 |
| Unknown prerequisites / dependency cycles | 0 / 0 |
| Unknown source IDs / invalid source URL syntax | 0 / 0 |
| Learning path | All modules once; every dependency precedes its dependent lesson |
| Lesson status | 161 planned; 27 previews; 0 full-contract complete |

## Effort assumptions

Guided study totals approximately 320–534 learner hours. Exercises add 581–959 hours if all are completed. These broad estimates describe learner effort, not an implementation commitment; prior knowledge and compute choices materially affect them.

## What was reviewed

The author reviewed the module-to-lesson mapping for conceptual gaps and repeated exercises, separated metrics from infrastructure health, added early security/evaluation gates, and provided resource alternatives for compute-heavy topics. Every lesson has an original scenario or engineering artifact and explicit review evidence.

## Limits of this report

The checker validates IDs, field completeness, unique questions/exercises, source references, dependency cycles, learning order, local Markdown targets, explicit anchors and generated-file consistency. It does not prove conceptual correctness, universal AI coverage, external link availability, legal compliance or working production systems. Exercise fixtures, solutions, measured benchmarks, learner pilots and independent technical review belong to later phases.

## Source and delivery audit

Lessons with one source: 27. EVAL references: 24; NIST references: 20. A focused specification can legitimately be a single source; source count alone is not evidence quality.

Hour ranges differ by lesson but remain low-confidence editorial estimates, not measured learner timings. They assume stated prerequisites and small local fixtures or labeled replays, excluding large training runs and cloud provisioning. Repeated estimate-basis prose was removed after post-review; calibrate the ranges through learner trials.

[Per-lesson delivery inventory](DELIVERY.md)
