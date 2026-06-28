# Runbook

> Operational procedures for building, previewing, and deploying Larnix.

## Local preview

The builder laptop runs Docker but not a system Quarto install, so render/preview
through the pinned image (see `docs/SITE.md` for detail):

```bash
# Live preview with reload at http://localhost:4848
docker compose -f infra/docker-compose.yml run --rm --service-ports preview

# One-shot static render into _site/
docker compose -f infra/docker-compose.yml run --rm render
```

With a native Quarto install: `quarto preview` / `quarto render`.

> **Snap-confined Docker note.** The snap `docker` can only bind-mount paths under
> `$HOME`. If the repo lives outside `$HOME` (e.g. `/data/...`), the volume mount
> resolves empty. Work around it by rendering from a copy under `$HOME` (e.g.
> `rsync -a --exclude .git --exclude _site ./ ~/larnix-render/ && docker run --rm
> -v "$HOME/larnix-render":/work -w /work ghcr.io/quarto-dev/quarto:1.8.27 quarto
> render <path>`), or move the clone under `$HOME`.

## Authoring chapters

### Loading the auto-grader (single source — P1-D9 / DECISIONS D0016)

Do **not** paste the grader. Each browser chapter loads `lib/grader.py` from the
Pyodide VFS:

1. In the chapter front-matter, declare the resource (path relative to the chapter):

   ```yaml
   resources:
     - ../../lib/grader.py
   ```

2. Give **every** `#| exercise:` a one-line setup cell (each exercise runs in its
   own environment, so a single global import does not reach it):

   ````markdown
   ```{pyodide}
   #| setup: true
   #| exercise: ex_name
   from lib.grader import run_tests
   ```
   ````

The exercise and its solution then call `run_tests([...])`. Verified in-browser on
M0 Ch1; full pattern + rationale in `lib/README.md` and DECISIONS D0016.

## CI / deploy

Two GitHub Actions workflows (see `infra/README.md` for the deploy model):

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `.github/workflows/publish.yml` | push to `main`, or manual **Run workflow** (`workflow_dispatch`) | Renders the site and deploys to the `gh-pages` branch **root** → production Pages. |
| `.github/workflows/pr-preview.yml` | `pull_request` (opened/updated/reopened/closed) | Renders the site and deploys a preview to `gh-pages/pr-preview/pr-<N>/`; comments the URL; cleans up on close. |

### First-time enablement

Set **Settings → Pages → Source → Deploy from a branch → `gh-pages` / (root)**.
No secrets needed (`GITHUB_TOKEN` is automatic).

### Branch protection & merge policy (`main`)

`main` is protected — all work lands via pull request and **every check must pass
before merge** (no direct pushes, even for admins):

- **Required status checks** (strict / branch must be up to date): `Schema, a11y &
  unit tests`, `Notebook execution (R10)`, `Prose, spelling & links`, `preview`.
- **Pull request required** (0 approvals — solo maintainer); conversations must be
  resolved; **force-pushes and branch deletion are blocked**; **admins are not
  exempt** (`enforce_admins`).
- Repo hygiene: **head branches auto-delete on merge**, **auto-merge enabled** (a
  PR merges itself once checks go green), and "update branch" is allowed.

Manage at **Settings → Branches**. In a genuine emergency an admin can temporarily
relax protection, fix, then restore it.

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
