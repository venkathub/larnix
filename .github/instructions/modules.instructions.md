---
applyTo: "modules/**"
---

# Content-chapter review rubric (Varsity contract + P1_REVIEW conventions)

When reviewing chapter/quiz/capstone changes under `modules/`, check each of these and
explain the *why* in your comments (tutor mode):

1. **Contract order**: hook (analogy/demo first) → plain-language explanation (one
   concept) → runnable worked example → Key Takeaways (3–6 points) → 2–4 exercises
   with hidden solutions → quiz. Front-matter complete (10 fields incl.
   `last_reviewed`), 3 `review_cards`.
2. **Exercise ladder is real**: Ex1 guided blank → **Ex2 = write-the-whole-body from a
   docstring/spec** (a second one-blank fill-in does NOT qualify) → Ex3 open-ended/
   rubric. Exception: **M0 is exempt** (learners don't know Python yet — guided
   single-call blanks only there).
3. **No syntax before its chapter**: an exercise may not require constructs a later
   module/chapter teaches; if unavoidable, the helper is given code, the blank is one
   call, and a callout says where it's taught.
4. **Quizzes/review cards test only taught content** — every answer's explanation must
   be traceable to the chapter body. **Module quizzes are transfer/application
   questions**, never verbatim reuse of chapter-quiz questions.
5. **Transitions are content**: the closing section must hand off to the *actual* next
   chapter; after any reorder, every affected transition must be re-checked.
6. **Capstone three-way agreement**: brief = rubric = walkthrough, every printed number
   reproducible from the vendored data, and the capstone must force transfer (new
   dataset or a required variation).
7. **₹0 / browser promise**: `compute: browser` chapters import only Pyodide-safe
   packages; datasets are vendored + ledgered in `docs/ASSETS.md`; no paid key is ever
   required on the learning path.
8. **Beginner truth**: every term defined at first use; analogies clarify (flag where
   an analogy would mislead and isn't scoped); difficulty badges match front-matter and
   the actual demands of the exercises.
9. **Math/data correctness**: verify derivatives, chain-rule products, probability
   arithmetic, matrix shapes, and pandas idioms (modern, copy-on-write-safe; no
   `inplace=True`, no chained assignment). Recompute spot values where feasible.
