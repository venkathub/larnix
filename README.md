# Larnix

An original AI Engineering curriculum for interview preparation and production practice.

Phase 1 defines the learning plan. One original interactive sample, [M03-L01 — Reason with vectors](samples/vector-similarity/index.html), is now implemented for review. See the [sample guide](samples/vector-similarity/README.md) for local preview and checks; the full learning platform remains planned.

Start with the [curriculum specification](docs/curriculum/README.md), then browse the [42 module plans](docs/curriculum/INDEX.md), [primary source register](docs/curriculum/SOURCES.md), and [coverage audit](docs/curriculum/AUDIT.md).

The [teaching design](docs/curriculum/TEACHING_DESIGN.md) specifies visual explanations, interactive experiments, worked examples and inline checks, informed by the user's linearalgebra.info reference.

The AI Engineering Playbook supplied by the user is a background reference only. This repository does not fork it or import its code, prose, questions, diagrams, or interface.

## Maintaining the plan

The authoritative records are `docs/curriculum/curriculum.json` and `docs/curriculum/sources.json`. Human-readable module plans are generated from those records.

```sh
python3 scripts/curriculum.py render
python3 scripts/curriculum.py check
```

The check verifies identifiers, references, prerequisite cycles, lesson completeness, generated-document consistency, and planned coverage. It does not claim that future lessons, exercises, or applications have been implemented or tested.
