# assessments — Assessment, progress & certification

## Quiz engine (P0, see DECISIONS D0006)

A zero-backend MCQ engine: a per-chapter `quiz.yml` is rendered by the `quiz`
shortcode into a client-side widget that scores in the browser and stores the
best score in `localStorage`. The quiz file is schema-validated in CI by
`infra/ci/quiz_lint.py`.

### Authoring a quiz

1. Write a `quiz.yml` next to the chapter `.qmd`:

```yaml
title: "Chapter 1 — quick check"   # optional
id: "m0-ch1"                       # optional; the localStorage key
questions:
  - id: what-is-a-model            # optional, unique within the file
    prompt: "A model is…"          # required
    options:                       # required, >= 2
      - "A spreadsheet of data"
      - "A function learned from data"
    answer: 1                      # required, 0-based index of the correct option
    explanation: "It is the learned function."   # optional, shown after scoring
```

2. Mount it in the chapter with one line:

```markdown
{{</* quiz quiz.yml */>}}
```

(The `*` form above is the literal escape — write it without the `*` to actually
mount the quiz. Note: Quarto expands shortcodes even inside backtick code spans,
so always escape literal examples.)

### How it works

- `site/_extensions/larnix/quiz/quiz.lua` — shortcode: reads `quiz.yml` at render,
  converts it to JSON (via Pandoc), embeds it in a mount `<div>`, and registers
  the engine assets once.
- `site/_extensions/larnix/quiz/resources/larnix-quiz.{js,css}` — the client-side
  engine: renders MCQs, scores on submit, shows correct/incorrect + explanations,
  persists `{best,last,total,at}` to `localStorage` under `larnix-quiz:<id>`.

A worked example is at `site/sandbox-quiz.qmd` (+ `site/quiz-sandbox.yml`).

> **Verification note.** Render confirms the YAML→JSON embed and asset bundling;
> the actual render/score/persist is confirmed in a browser (preview deploy).

## Deferred to later phases

- Spaced-repetition scheduler (P6; the card *convention* is seeded in P0 task 13 — see below).
- Certification exam config + learning-track definitions (P6).

## Spaced-repetition card seeding (P0-D3, see DECISIONS D0004)

Chapters seed review cards **inline in front-matter** as a `review_cards:` block,
derived from the chapter's Key Takeaways. The scheduler that serves them is P6;
P0 only proves the authoring convention (schema-validated by
`infra/ci/review_cards_lint.py`) so no later chapter needs retrofitting.

```yaml
review_cards:
  - id: what-is-a-model           # optional, unique within the chapter
    q: "What is a model?"         # required
    a: "A function learned from data that maps an input to a prediction."  # required
  - q: "What does accuracy measure?"
    a: "The fraction of predictions that match the true labels."
```

Convention: one card per Key Takeaway, phrased as a question the learner can
self-test. `q`/`a` are plain text.
