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

## What a reviewer is also seeing

- The same chapter has a CI **twin** notebook that runs the worked example and the
  exercise solutions under CPython in CI, so the code is guaranteed to work.
- Every page passed the CI gates (front-matter/quiz/review-card schemas;
  R1/R3/R6/R10; prose/spell/link; WCAG-AA a11y) before it could merge.
