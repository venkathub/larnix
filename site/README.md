# site — Build & Publish System

The Larnix learner-facing website: a [Quarto](https://quarto.org) static site.

## Layout

| Path | Purpose |
|------|---------|
| `_quarto.yml` | Website project config: nav, search, theme slots, execution (`freeze`). |
| `index.qmd` | Landing page. |
| `about.qmd` | Project goals + build status. |
| `styleguide.qmd` | Internal design-system styleguide (renders every component; not learner content; excluded from search). |
| `sandbox.qmd` | Internal scratch page proving the in-browser runtime runs Python + scikit-learn (`format: live-html`, `{pyodide}` cells). |
| `sandbox-colab.qmd` | Internal scratch page proving the `colab` "Open in Colab" button shortcode. |
| `theme/larnix.scss` | Light theme (on `cosmo`) — brand tokens + imports the shared component partial. |
| `theme/larnix-dark.scss` | Dark theme (on `darkly`) — imports the partial, then dark colour overrides. |
| `theme/_larnix-components.scss` | Shared component structure: Key Takeaways box + badges (imported by both themes). |
| `_extensions/larnix/badges/` | The `badge` Quarto shortcode (Lua). |
| `_site/` | Generated output (git-ignored). |

## Design system (see DECISIONS D0008)

**Badges** — author with the shortcode, one dimension per call:

```markdown
{{< badge difficulty=beginner >}}    <!-- beginner | intermediate | advanced -->
{{< badge compute=browser >}}        <!-- browser | colab | gpu -->
{{< badge status=stable >}}          <!-- stable | frontier -->
```

The label carries the meaning (colour is reinforcement, never the only signal);
an `aria-label` is emitted for screen readers.

**Key Takeaways box** — author as a fenced div:

```markdown
::: {.key-takeaways}
### Key Takeaways
1. ...
:::
```

**Themes** — light/dark via the navbar toggle (native Quarto). A **sepia**
reading mode is a tracked follow-up (D0008); component colours are
contrast-checked to WCAG AA. See `styleguide.qmd` rendered to eyeball both modes.

## In-browser runtime (quarto-live + Pyodide)

Beginner `compute: browser` chapters run Python **client-side** via the vendored
`quarto-live` extension (Pyodide), so learners need zero install (₹0). Author a
runnable cell with the `{pyodide}` block in a `format: live-html` document:

````markdown
---
format: live-html
execute:
  enabled: false   # {pyodide} cells run in the browser, never at render time
---

```{pyodide}
print("hello from your browser")
```
````

`site/sandbox.qmd` is the proof page (imports scikit-learn, trains Iris, prints
accuracy). **Important:** `{pyodide}` cells execute in the visitor's browser, not
during `quarto render` — so a local/CI render only confirms the runtime assets +
cell markup are emitted; actual execution is confirmed by opening the page in a
browser (or the preview deploy). Render with `execute.enabled: false` so the
build needs no Python/Jupyter kernel.

The design system (Key Takeaways box, 🟢/🟡/🔴 difficulty badges, `browser|colab|gpu`
compute badge, `stable|frontier` status badge) is in place. The in-browser
runtime, auto-grader, quiz engine, and the first chapter are layered on in later
P0 tasks (see `docs/phases/P0_SPEC.md §6`).

## Version pins

| Tool | Pin | Notes |
|------|-----|-------|
| Quarto CLI | **1.8.27** | Latest confirmed stable patch on the 1.8 line (2026-01-16). The 1.9 line is the current release; bump deliberately and log it. |
| `quarto-live` extension | **v0.2.0** (internal ext version 0.1.3) | Pyodide in-browser runtime. **Vendored** at `site/_extensions/r-wasm/live/` so a fresh clone builds without a network `quarto add`. Re-add with `quarto add r-wasm/quarto-live@v0.2.0`. |

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
