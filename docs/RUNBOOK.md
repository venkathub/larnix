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

_(Added in P0 task 12: the manual Colab-run record procedure for `colab`/`gpu`
chapters.)_
