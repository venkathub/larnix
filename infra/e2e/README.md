# Larnix e2e smoke tests

Browser-level tests for what no Python unit test can cover (review 2026-07-19,
finding E1 + the D0017 deferred items):

1. **Quiz engine** (`smoke.spec.js`) — renders, scores, persists best score to
   `localStorage`, locks a graded attempt, offers *Try again*.
2. **Chapter progress** (`smoke.spec.js`) — *Mark chapter complete* persists;
   the module landing page's progress bar and sidebar ticks reflect it.
3. **Live Pyodide cell** (`smoke.spec.js`) — a worked cell on M0 Ch1 really
   executes Python in the browser (the ₹0 promise). Hits the Pyodide CDN;
   the slow one (~20 s warm, minutes cold).
4. **axe DOM audit** (`a11y.spec.js`) — WCAG A/AA scan of the five key page
   types; **serious + critical violations fail the build**, lesser findings are
   logged as advisories. Live editors (third-party CodeMirror internals) are
   excluded with rationale in the spec.
5. **Mobile viewport** (`mobile.spec.js`) — 375 px: no horizontal overflow on
   landing/chapter/module/curriculum, and the quiz + mark-complete controls
   stay usable.

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

## Dependency layout (why "playwright" appears more than once)

Only **one** Playwright is depended on directly. The similar names are two
different things:

- **`@playwright/test`** — the Playwright test runner (our one direct
  Playwright dependency; drives all three spec files).
- **`@axe-core/playwright`** — Deque's **axe accessibility engine** adapter
  *for* Playwright (used by `a11y.spec.js`). It is named after what it plugs
  into, not a second copy of Playwright.

In `package-lock.json` you'll additionally see `playwright` and
`playwright-core` — that's Playwright's own upstream package layering
(runner → library → driver core), all resolving to the **same version** as
`@playwright/test`; npm dedupes `playwright-core` so the axe adapter and the
runner share one copy (`npm ls playwright-core` shows a single deduped entry).
To upgrade, bump `@playwright/test` — the transitive pair follows in lockstep.
