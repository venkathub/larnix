# Runbook

> Operational procedures for building, previewing, and deploying Larnix.

## Local preview

The builder laptop runs Docker but not a system Quarto install, so render/preview
through the pinned image (see `site/README.md` for detail):

```bash
# Live preview with reload at http://localhost:4848
docker compose -f infra/docker-compose.yml run --rm --service-ports preview

# One-shot static render into site/_site/
docker compose -f infra/docker-compose.yml run --rm render
```

With a native Quarto install: `quarto preview site/` / `quarto render site/`.

## CI / deploy

Two GitHub Actions workflows (see `infra/README.md` for the deploy model):

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `.github/workflows/publish.yml` | push to `main`, or manual **Run workflow** (`workflow_dispatch`) | Renders `site/` and deploys to the `gh-pages` branch **root** → production Pages. |
| `.github/workflows/pr-preview.yml` | `pull_request` (opened/updated/reopened/closed) | Renders `site/` and deploys a preview to `gh-pages/pr-preview/pr-<N>/`; comments the URL; cleans up on close. |

### First-time enablement

Set **Settings → Pages → Source → Deploy from a branch → `gh-pages` / (root)**.
No secrets needed (`GITHUB_TOKEN` is automatic).

### Reading a failed run

1. **Actions** tab → open the failed run → expand the failed step.
2. Most failures at this stage are render errors — reproduce locally with
   `docker compose -f infra/docker-compose.yml run --rm render` and read the same
   Quarto error.
3. Re-run a flaky deploy from the run page (**Re-run jobs**), or trigger a fresh
   production deploy via **publish.yml → Run workflow**.

### Manual production deploy

Actions → **Publish site** → **Run workflow** → branch `main`.

## GPU notebook policy

GPU work never runs on the builder's laptop and **never runs in CI** (there is no
GPU runner). `colab`/`gpu` notebooks are executed manually on a free Colab/Kaggle
GPU and the run is **recorded in the PR**. CI's R10 gate (`run_notebooks.py`)
**skips** any notebook marked GPU/`colab` and runs only browser-twin + CPU
notebooks.

### How a notebook is marked "do not run in CI"

R10 skips a notebook if either is true:

- its Quarto front-matter has `compute: colab` or `compute: gpu`; or
- its notebook metadata has `"larnix": {"compute": "colab"}` (or `"ci": false`).

The non-content example is `infra/fixtures/colab-fixture.ipynb`.

### Adding an "Open in Colab" button

In the chapter `.qmd`, use the shortcode with the notebook's repo-relative path:

```markdown
{{</* colab modules/NN-slug/chapter.ipynb */>}}
```

The repo + branch come from `_quarto.yml` (`larnix-colab-repo`,
`larnix-colab-branch`) or the `LARNIX_COLAB_REPO` / `LARNIX_COLAB_BRANCH` env
vars — never hardcoded. Set them once the repo is published.

### Manual Colab-run record (required in the PR)

For every `colab`/`gpu` notebook changed in a PR, paste into the PR description:

1. The Colab link used (from the button).
2. The Colab runtime type (e.g. **T4 GPU**) and a one-line **cost** statement
   (free tier, or the rented-GPU rate for M11).
3. Confirmation it ran top-to-bottom, with the final cell's output (a screenshot
   or pasted text) and the run date.

A reviewer treats a missing record as a failing check for that notebook.
