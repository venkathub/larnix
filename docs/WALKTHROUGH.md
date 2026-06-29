# 5-minute learner walkthrough

A click-and-run path through the P0 sample chapter, so a reviewer can experience
the whole platform in five minutes. Two ways to do it.

## Option A — local preview (one command)

```bash
docker compose -f infra/docker-compose.yml run --rm --service-ports preview
```

Open <http://localhost:4848>, then follow the steps below.
(With a native Quarto install: `quarto preview`.)

## Option B — the deployed site

Open the published site (GitHub Pages) or a PR preview link, then follow the
steps below. No install, ₹0.

## The path (≈5 minutes)

1. **Land on Home.** From the navbar, click **Start learning** → *Train your
   first model — in your browser*. Note the badges under the title:
   🟢 Beginner · `browser` · stable.
2. **Run the worked example.** Press **Run** on each `{pyodide}` block in order
   (the first run downloads Pyodide; a few seconds). Watch it load the Iris data,
   split it, train a classifier, predict, and print a **test accuracy** — all in
   the browser, nothing installed.
3. **Do Exercise 1 (guided).** Replace the blank with `model.fit(X_train, y_train)`
   and press **Run** — the grader prints `All tests passed ✅`. Click **Show
   solution** to check your reasoning.
4. **Do Exercise 2 (implement).** Complete `accuracy()` with `a == b`; the grader
   runs three asserts and confirms a pass.
5. **Read the Key Takeaways** box, then **take the quiz** at the end: pick answers,
   press **Check answers**, see your score and per-question explanations. Reload
   the page — your best score is remembered (browser `localStorage`).

That is the full learner loop: hook → explanation → runnable example → graded
practice → quiz, at ₹0.

---

## P1 — the four-module journey (≈10 minutes)

P1 turns the proven sample chapter into a real beginning-to-frontier start:
**50 chapters across 4 modules**, each ending in a cumulative quiz and a
build-something capstone. A reviewer can taste the whole arc by opening one
landing page per module from the sidebar.

1. **M0 — Orientation** → `modules/00-orientation/`. Start at *Train your first
   model* (the P0 chapter), then *What you need & what it costs* (the ₹0 path
   stated up front). Finish at the **module landing** and take the 10-question
   module quiz — it scores client-side and remembers your best score.
2. **M1 — Python for AI** → *Variables & types* through *Notebooks, the IDE &
   Colab* (14 chapters). The module threads one deliberately messy `habits.csv`,
   cleaned a little more each chapter; the **capstone** turns 35 messy rows into 30
   clean ones with your own functions.
3. **M2 — Math You Actually Need** → *Why math for AI* through **Ch16 — The math of
   one neuron** (16 chapters). Picture-first vectors, derivatives, and probability
   build to the culmination: open Ch16, press **Run** on the gradient-check cell,
   and watch the hand-derived gradient match a numeric estimate to
   `max error = 3.27e-11`. That is backpropagation, by hand.
4. **M3 — Data & Tooling** → *NumPy & vectorization* through *Messy real-world
   data* (14 chapters). Open *Pandas Series & DataFrame*, press **Run**, and the
   real **Palmer Penguins** dataset (344×8, CC0) loads offline in your browser;
   later chapters clean, group, plot, and reason about it. The **capstone** is a
   full EDA on a *new* dataset, to test transfer.

Each module landing mounts a cumulative **module quiz** (M0: 10 Q, M1: 11 Q, M2:
12 Q, M3: 12 Q); all score in-browser and persist to `localStorage`.

## What a reviewer is also seeing

- Every one of the **50 chapters** ships a CI **twin** notebook executed under
  CPython (`nbclient`) — so every worked example and every hidden solution is
  guaranteed to run. All 50 execute cleanly.
- Browser chapters load a **single-source grader** (`lib/grader.py`) and offline
  **datasets** (`lib/data.py`) into the Pyodide filesystem — no network, ₹0.
- Every page passed the CI gates (front-matter/quiz/review-card schemas;
  R1/R3/R6/R10; render-safety; prose/spell/link; WCAG-AA a11y) before it could
  merge. Backed by **111 unit tests**.
- The whole site (61 documents) renders cleanly with `quarto render`, and the
  project builds from a fresh clone.
