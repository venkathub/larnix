# Larnix

An original AI Engineering curriculum for interview preparation and production practice.

Phase 1 defines the learning plan. Two original interactive samples are implemented for review:

- [M03-L01 — Reason with vectors](samples/vector-similarity/index.html) · [preview guide](samples/vector-similarity/README.md)
- [M17-L01 — Assemble a grounded answer pipeline](samples/rag-grounding/index.html) · [preview guide](samples/rag-grounding/README.md)

The first local platform foundation is implemented: a searchable catalogue, lesson-plan pages, prerequisite links, Learn/Interview/Production views, and browser-local progress for the two previews. The remaining 166 lesson narratives and labs are planned.

## Run the platform

```sh
python3 scripts/build_site.py
python3 -m http.server 8775 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8775/`. Rebuild after source changes, then reload the browser. No package installation, account or model API is required. Progress stays in browser local storage and is specific to the origin (including port); it does not synchronize across devices. Standalone samples keep session-only quiz progress.

See the [implementation guide](docs/IMPLEMENTATION.md) for architecture, checks, authoring and remaining milestones.

Start with the [curriculum specification](docs/curriculum/README.md), then browse the [42 module plans](docs/curriculum/INDEX.md), [primary source register](docs/curriculum/SOURCES.md), and [coverage audit](docs/curriculum/AUDIT.md).

The [teaching design](docs/curriculum/TEACHING_DESIGN.md) specifies visual explanations, interactive experiments, worked examples and inline checks, combining the user's linearalgebra.info visual reference with the adopted Varsity-inspired narrative explanation standard.

The AI Engineering Playbook supplied by the user is a background reference only. This repository does not fork it or import its code, prose, questions, diagrams, or interface.

## Maintaining the plan

The authoritative records are `docs/curriculum/curriculum.json` and `docs/curriculum/sources.json`. Human-readable module plans are generated from those records.

```sh
python3 scripts/curriculum.py render
python3 scripts/curriculum.py check
```

The check verifies identifiers, references, prerequisite cycles, lesson completeness, generated-document consistency, and planned coverage. It does not claim that future lessons, exercises, or applications have been implemented or tested.
