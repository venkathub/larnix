# site — Build & Publish System

The Larnix learner-facing website: a [Quarto](https://quarto.org) static site.

## Layout

| Path | Purpose |
|------|---------|
| `_quarto.yml` | Website project config: nav, search, theme slots, execution (`freeze`). |
| `index.qmd` | Landing page. |
| `about.qmd` | Project goals + build status. |
| `_site/` | Generated output (git-ignored). |

The design system (Key Takeaways box, 🟢/🟡/🔴 difficulty badges, `browser|colab|gpu`
compute badge, `stable|frontier` status badge, dark/sepia toggle), the in-browser
runtime, auto-grader, quiz engine, and the first chapter are layered on in later
P0 tasks (see `docs/phases/P0_SPEC.md §6`).

## Version pins

| Tool | Pin | Notes |
|------|-----|-------|
| Quarto CLI | **1.8.27** | Latest confirmed stable patch on the 1.8 line (2026-01-16). The 1.9 line is the current release; bump deliberately and log it. |
| `quarto-live` extension | **0.2.0** (planned) | Pyodide in-browser runtime; **added in P0 task 5**, not yet installed. |

## Build & preview locally

This repo's builder laptop has Docker but **not** a system Quarto install, so we
render through the pinned official image. CI installs Quarto natively and is the
authoritative render.

**Live preview** (reloads on save) at <http://localhost:4848>:

```bash
docker compose -f infra/docker-compose.yml run --rm --service-ports preview
```

**One-shot static render** into `site/_site/`:

```bash
docker compose -f infra/docker-compose.yml run --rm render
```

If you *do* have Quarto installed natively, the equivalents are
`quarto preview site/` and `quarto render site/`.

## Output

Rendered HTML lands in `site/_site/`. Hosting/deploy (GitHub Pages + PR preview)
is wired in P0 task 2.
