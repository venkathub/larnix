# Sample lesson: An answer needs evidence

Original **M17-L01 — Assemble a grounded answer pipeline**, using the adopted narrative and interactive teaching standard. This is a standalone lesson prototype, not the full platform or a live RAG service.

## Preview

From the repository root:

```sh
python3 -m http.server 8774 --bind 127.0.0.1 --directory samples
```

Open `http://127.0.0.1:8774/rag-grounding/`. Keep the parent `samples` directory as the server root: this lesson shares the vector sample's base stylesheet. Opening `index.html` directly also works. All computations are local; only the two further-reading links are external.

## Teaching and interaction

A fictional camera-rental policy change carries through the story, evidence pipeline, worked trace, failure diagnosis, interview guide and production exercise. The lesson includes prerequisites, a policy-folder analogy with its limits, three explanatory checks, five takeaways and a glossary.

The interactive fixture contains five versioned passages, three questions and six scenarios. Change source availability, retrieval K, context capacity and date filtering. Inspect candidate exclusions, included passages, claim citations, abstention and conflicting evidence. Citation links highlight their context passage. Controls support keyboard input; the static narrative explains the baseline without JavaScript.

All dates use the fixed reference date **2026-10-12**. Dates are inclusive. Candidate order is fixed per question. Filtering happens after retrieval and does not backfill. Packing uses whole-passage slots, not tokens. The mock answers from known fields; it does not parse arbitrary documents, retrieve embeddings, call a language model or measure performance. It can only detect contradictions in supplied context. The expired-but-cited scenario deliberately demonstrates an incorrect current-policy answer even though the claim maps to a source.

The answer policy withholds a complete answer when a required fact is absent; known fragments are shown separately. Conflicts withhold all claims. These are teaching choices, not universal RAG requirements. Progress and theme are page-session only.

## Practice files

- `fixtures.json`: versioned fictional policies, question order, six independent expected cases.
- `exercise.py`: learner TODO scaffold and fixture report runner. It intentionally raises `NotImplementedError` until implemented.
- `rag-engine.js`: working browser rules, also importable by Node tests.
- `lesson.js`: browser controls, trace rendering, citations and quiz definitions.
- `../shared/lesson-ui.js`: reusable quiz feedback, reset and theme controls.
- `rag.css`: responsive evidence-lab layout, layered on the existing sample styles.

## Verification

```sh
node samples/rag-grounding/tests/rag-engine.test.cjs
node --check samples/rag-grounding/lesson.js
python3 scripts/curriculum.py check
```

Tests cover baseline facts/citations, retrieval versus context failures, stale-source applicability, visible/unseen contradictions, unsupported queries, empty sources, valid citation targets and invalid configuration. The downloadable expected cases are also checked against the browser engine. Browser QA covers scenarios, controls, citation navigation, quiz/reset, themes and mobile/desktop layout. This is not a full accessibility audit or learner study.

Research sources are linked in the lesson. The reference projects informed teaching direction only; no external lesson content, interface assets or implementation was copied.
