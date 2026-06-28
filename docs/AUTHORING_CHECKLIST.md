# Authoring checklist — every Larnix chapter

> Copy this into each chapter PR and tick every box. It instantiates the **Varsity
> contract** (`STYLE_GUIDE §2`), the **beginner-scaffolding kit** (P1-D4), and the
> **correctness review** (`P1_SPEC §5.5`). The structural pillars are enforced by
> `infra/ci/chapter_structure_lint.py`; the rest is human review — this list keeps
> chapter #1 and chapter #50 reading as one course.

## The Varsity contract (in this order)

- [ ] **Hook** — a real-world analogy or a working demo first (taste before theory).
- [ ] **Plain explanation** — one concept, ~1,500–3,000 words or a 15–25 min notebook.
- [ ] **Runnable worked example** — at least one `{pyodide}` cell that actually executes.
- [ ] **Key Takeaways** box — `::: {.key-takeaways}`, 3–6 numbered points.
- [ ] **2–4 graded exercises** — each with a working `run_tests` auto-grader (or a
      labelled rubric for stretch) and a hidden `<details>` solution walkthrough.

## Beginner-scaffolding kit (P1-D4 — apply to every chapter)

- [ ] **"You'll need from before"** — a one-line recap at the top naming the prior
      chapters/ideas this one builds on (mirror the front-matter `prereqs`).
- [ ] **Exercises scaffold guided → implement → stretch** —
      🟢 *Guided* (fill one line) → 🟡 *Implement* (write a function, asserts) →
      🔴/optional *Stretch* (open-ended, **rubric-graded**, labelled as such).
- [ ] **"If you're stuck"** hint — one nudge *before* the hidden solution in each
      non-trivial exercise (a `> 💡` line or a hint sentence), so a stuck learner
      gets unstuck without the full answer.
- [ ] **`🧱 For Java developers`** callouts — in M1 only, as collapsible asides that a
      non-Java beginner can skip (dynamic typing, indentation-as-syntax, duck typing).
- [ ] Tone is encouraging, never condescending; no banned words
      (`simply`, `just`, `obviously`, `trivially`, hype).

## Grader, data & compute wiring

- [ ] Grader is **single-sourced**: `resources: [ ../../lib/grader.py ]` in front-matter
      + a `#| setup: true` / `#| exercise: <id>` cell per exercise (`from lib.grader
      import run_tests`). No pasted grader. (P1-D9)
- [ ] Any dataset is **vendored** at `data/<name>.csv`, declared in `resources:`, loaded
      via `lib/data.py`, and **ledgered** in `docs/ASSETS.md` with a license (R11). A
      data chapter declares `pyodide: packages: [pandas]`. (P1-D8)
- [ ] `compute: browser`; imports are Pyodide-safe (R3) — a runtime micropip install is
      annotated `# micropip: <name>`.
- [ ] The CI **twin** is generated, not hand-written: run `python infra/ci/make_twin.py
      --write <chapter.qmd>` and commit it; the hidden solution is a runnable cell given
      the cells above it. (P1-D10)

## Assessment

- [ ] A per-chapter **quick check** `quiz.yml` (2–3 MCQ) mounted with `{{< quiz quiz.yml >}}`;
      each MCQ has an `answer` and a one-line `explanation`. (P1-D11)
- [ ] **3 spaced-repetition cards** in the front-matter `review_cards:` block, drawn from
      the Key Takeaways.

## Correctness & accessibility review (P1_SPEC §5.5)

- [ ] Every code cell executed in CI (twin) **and** previewed in-browser; outputs shown.
- [ ] Every term defined on first use; reads for a true beginner (the house test).
- [ ] Numbers/claims verified; primary sources cited; no invented citations. Mark
      fast-moving content `status: frontier` rather than guessing.
- [ ] Front-matter complete + accurate (all 10 fields); `last_reviewed` set;
      `review_cards` present.
- [ ] ₹0 / `browser` path confirmed; R3 import lint clean.
- [ ] Plots/diagrams have meaningful alt-text (the takeaway, not "a chart"); no
      colour-only meaning.
