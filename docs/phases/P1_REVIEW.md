# P1_REVIEW — P0/P1 post-completion review: findings → fixes ledger

> **Date:** 2026-07-19 · **Reviewed:** everything P0_SPEC + P1_SPEC claim shipped
> (platform, gates, and all 50 chapters), from an AI-engineer/educator lens, with
> independent re-verification (live-site checks, recomputing content numbers,
> re-running gates). **Decision record:** `DECISIONS.md D0017`.
> **Branch:** `fix/p0-p1-review-findings`.
>
> **Purpose of this file:** (1) the honest record of what the review found and
> what was done about each finding; (2) the checklist of review-born conventions
> **every later phase (P2+) must adopt** — they are also folded into
> `STYLE_GUIDE.md`, `AUTHORING_CHECKLIST.md`, and the CLAUDE.md DoD.

## What held up under review (keep doing this)

- **Content correctness.** Every recomputed number in M2/M3 checked out — including
  the ch16 gradient-check error (3.27e-11, reproduced exactly), Bayes worked
  examples, and all vendored-dataset counts. Pandas usage is modern (CoW-safe, no
  deprecated APIs). All sampled quiz answer keys were correct.
- **Gate discipline.** 11 CI gate scripts, each unit-tested; exact version pinning
  throughout; twin-drift derivation instead of hand-maintained twins.
- **Honest docs.** Specs flagged their own verification limits ("manual sweep",
  "not independently re-derived") — which is exactly how the review could target
  the thin spots.

## Findings → fixes (all landed on this branch)

| # | Finding (severity) | Fix |
|---|---|---|
| 1 | **Capstones served as raw markdown** on the deployed site (404-class; verified live) — P1's headline deliverable unreachable as a page | `render:` includes `modules/**/capstone.md`; front-matter titles; sidebar entries; **CI now renders on every PR + offline-lychee checks every internal link in `_site/`** |
| 2 | **M0 exercises required M1 Python** (generator expressions, `while`+`dict.get`) before Python is taught — top dropout risk | ch02–ch05 blanks reduced to single calls on given helpers, with "taught in Module 1" callouts; ch01 Ex1 failure now a friendly grader ❌, not a raw `NotFittedError` |
| 3 | **Pyodide failure was silent** (offline/blocked CDN = dead Run buttons, no message) | 45 s watchdog → dismissible alert with Reload-and-retry / Keep-waiting; honest download-size note; self-removes on success |
| 4 | **No progress model** (`.lx-progress` was dead demo CSS at a hard-coded 22%) | Mark-complete toggle on every chapter/capstone, sidebar ✓ ticks, real module progress bars; device-locality stated in the UI |
| 5 | **Validated metadata never shown** (est_minutes/prereqs); hand-written badges could drift from front-matter | `larnix/chapter-meta` filter renders the strip on all 50 chapters; badge↔front-matter drift is now a CI failure |
| 6 | **Quiz UX**: `shuffle:` validated but unimplemented; silent re-scoring of a revealed key; optional `id` = fragile storage keys | shuffle implemented (answer-index remapped); attempts lock + explicit Try-again; focus to first wrong answer; `id:` required by lint |
| 7 | **Zero browser-level tests** behind the "runs in the browser" claims | Playwright smoke gate in `Checks`: quiz persist/lock, progress, one real Pyodide execution (3/3 verified locally) |
| 8 | **M3 transitions broken by a reorder** (ch09/ch13 "closed" the module early; ch14 pointed backwards) | All four closings rewritten for the real order (ch09→ch10, ch10→ch11, ch13→ch14, ch14 = module close → capstone/M4) |
| 9 | **M1 capstone brief ⊃ rubric ⊃ walkthrough** (mixed dates + impossible values in the brief and the CSV, absent from both others) | Walkthrough handles the full brief; rubric requires it; every printed number recomputed against the vendored CSV (35→29, removed 6) |
| 10 | **M2 capstone copyable from ch16** (zero transfer) | Required variation (tanh, self-derived `da/dz = 1−a²`, or ½-MSE, `dL/da = a−y`); rubric + hidden answer key updated; stated numbers computed |
| 11 | **M2 "one neuron" thread invisible in ch02–ch15**; README overclaimed the running examples | One honest linking sentence per chapter (indirect links stay explicitly indirect); README claims scoped to reality |
| 12 | **M0 ch04/ch05 currency + honesty**: "generative-adjacent" label on a classifier demo; timeline ended 2022; quiz/review-card taught an un-narrated second AI winter | Demo relabeled honestly (+ Markov-toy nesting footnote); timeline → 2023 (GPT-4/multimodal) + 2024 (o1-class reasoning); second winter narrated in the body |
| 13 | **Module quiz ≈ chapter quizzes verbatim** (M0: ~6/10) — measured recognition, not integration | All 10 M0 module-quiz questions rewritten as transfer/application scenarios |
| 14 | Ex2 "Implement" was a second one-blank across the fleet | Convention changed (STYLE_GUIDE §6) + exemplar rewrites (M1 ch01, ch12); fleet-wide pass tracked below |
| 15 | Thin chapters (M1 ch04 = ~750 prose words for four data structures) | ch04 fattened to ~1,112 words (decision guide, dict-vs-scan example, common mistakes); notebook word-floor clarified in STYLE_GUIDE |
| 16 | Stale copy: About page pre-P1; hero "journey" link → GitHub markdown; "2–3 MCQ" claims (actual 3–4); ch07 "34 fine rows" (false); ch09 dtypes sentence | About rewritten; on-site `curriculum.qmd` + navbar entry; all README/doc counts fixed; prose honesty fixes |
| 17 | Internal fixtures (sandbox/styleguide) publicly indexed | robots `noindex` (they stay rendered — they are platform proofs) |
| 18 | Ops nits: Vale double-scanned `modules/`; 3 dead avatar contrast pairs; dead testimonial CSS | All removed/fixed |

## Conventions every future phase MUST adopt (now in the standing docs)

1. **The rendered product is part of the gate.** Render on every PR; link-check
   the rendered site; click every learner-facing link on the preview before
   closing a phase (now a CLAUDE.md DoD item).
2. **Exercise ladder is real:** Ex1 guided blank → **Ex2 write-the-body from a
   spec** → Ex3 open-ended/rubric. A second one-blank is not "Implement".
3. **No syntax before its chapter.** An exercise may not require constructs a
   later module teaches; if unavoidable, the helper is given code and the blank
   is a single call, with an explicit "taught in Module N" callout.
4. **Module quizzes are transfer quizzes.** Never verbatim reuse of chapter-quiz
   questions.
5. **Transitions are content.** Closing sections hand off to the *actual* next
   chapter; re-verify every transition after any reorder.
6. **Capstone three-way agreement.** Brief = rubric = walkthrough, and every
   number printed in a walkthrough is recomputed against the vendored data.
   Capstones must force transfer (new data, or a required variation).
7. **Assessment/review cards teach only taught content.** A quiz answer or SR
   card may not rely on facts the body never narrates.
8. **Failure states are visible.** Any runtime/network dependency a learner hits
   needs an honest, actionable failure UX (and a test that the success path
   stays quiet).
9. **What CI validates, learners see.** Metadata that is schema-enforced should
   be rendered (or consciously excluded); anything hand-duplicated from
   front-matter gets a drift lint.

## Deferred (tracked, not forgotten — see D0017 for rationale)

- [ ] E5: per-module `_metadata.yml` for the shared `live-html` block (blocked by
      directory-metadata leaking live-runtime assets onto index/capstone pages).
- [ ] Fleet-wide Ex2 rewrite beyond the exemplar chapters (apply convention #2
      opportunistically as chapters are touched; required for all new P2+ chapters).
- [ ] quarto-live vendor hash unknown for the current snapshot; record on next
      vendor update.
- [ ] `a11y_check` pairs auto-parsed from SCSS; axe/pa11y DOM audit; mobile
      viewport check.
- [ ] quiz.lua YAML via vendored tinyyaml (drop the Pandoc-metadata round-trip
      and its smart-quote transforms).
- [ ] Module-quiz transfer rewrite for M1–M3 (M0 done; M1–M3 quizzes are less
      duplicative but should be audited against convention #4).
