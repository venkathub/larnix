# Larnix e2e smoke tests

Browser-level smoke tests for the two paths a learner actually depends on —
paths no Python unit test can cover (review 2026-07-19, finding E1):

1. **Quiz engine** (`_extensions/larnix/quiz/resources/larnix-quiz.js`) —
   renders, scores, persists best score to `localStorage`, locks a graded
   attempt, offers *Try again*.
2. **Chapter progress** (`theme/_after-body.html`) — *Mark chapter complete*
   persists; the module landing page's progress bar and sidebar ticks reflect it.
3. **Live Pyodide cell** — a worked cell on M0 Ch1 really executes Python in
   the browser (the ₹0 promise). This test hits the Pyodide CDN and is the
   slow one (~20 s warm, minutes cold).

## Run locally

The tests run against an already-rendered `_site/`:

```bash
# 1. render the site (repo root; Docker per infra/docker-compose.yml)
# 2. then:
cd infra/e2e
npm ci
npx playwright install --with-deps chromium
npm test                     # uses ../../_site
SITE_DIR=/path/to/_site npm test   # or any rendered copy
```

In CI these run in the `Checks → render` job, immediately after `quarto render`
and the rendered-site link check (`.github/workflows/checks.yml`).

Versions are exact-pinned in `package.json` + `package-lock.json` (repo
convention: bump deliberately, log the bump).
