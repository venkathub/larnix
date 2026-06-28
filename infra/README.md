# infra — Operations & CI

CI workflows, local-preview tooling, and deploy configuration.

## Contents

| Path | Purpose |
|------|---------|
| `docker-compose.yml` | Version-pinned Quarto image for local render/preview (no system Quarto needed). See `site/README.md`. |
| `ci/` | Python CI gate scripts + their unit tests (front-matter lint now; R-gates later). See `ci/README.md`. |
| `../.vale.ini` + `../styles/Larnix/` | Vale prose style — STYLE_GUIDE §3 tone gate (banned words + no hype) on `.qmd`. |
| `../.markdownlint-cli2.yaml` | Markdown structural lint config. |
| `../.codespellrc` | Spell-check skips + allow-list. |
| `../lychee.toml` | Link-checker config (excludes generated/vendored + not-yet-live URLs). |
| `../.github/workflows/publish.yml` | Build + deploy the site to GitHub Pages (production) on push to `main`. |
| `../.github/workflows/pr-preview.yml` | Build + deploy a per-PR preview; comments the URL on the PR. |
| `../.github/workflows/checks.yml` | Quality gates: `schema` (front-matter + quiz + unit tests), `notebooks` (R10), `prose` (Vale, markdownlint, codespell, lychee). |

Later P0 tasks add more CI: notebook-execution gate (R10, task 8), prose/link/spell
(task 9), a11y (task 10), and the R1/R3/R6 gates (task 11) — as separate
workflows/jobs alongside the two above.

## Deploy model (GitHub Pages, gh-pages branch)

Per **DECISIONS.md D0007**, both production and PR previews publish to the
**`gh-pages`** branch:

- **Production** → branch root (`publish.yml`, push to `main`).
- **PR preview** → `gh-pages/pr-preview/pr-<N>/` (`pr-preview.yml`), via
  [`rossjrw/pr-preview-action`](https://github.com/rossjrw/pr-preview-action),
  which posts/updates a comment with the preview URL and deletes the subfolder
  when the PR closes.

### One-time repo setup (required for deploys to go live)

1. **Settings → Pages → Build and deployment → Source: _Deploy from a branch_**,
   branch **`gh-pages`**, folder **`/ (root)`**.
2. No secrets to add — the workflows use the automatic `GITHUB_TOKEN`.

The production URL is `https://<owner>.github.io/<repo>/`; a PR preview is
`https://<owner>.github.io/<repo>/pr-preview/pr-<N>/`.

> The live deploy + preview URL are verified on the first push/PR to GitHub
> (they need Pages enabled on the repo); they cannot run in the local sandbox.

## Pinned versions

| Thing | Pin |
|-------|-----|
| Quarto (CI + Docker) | `1.8.27` |
| `quarto-dev/quarto-actions/*` | `@v2` |
| `JamesIves/github-pages-deploy-action` | `@v4` |
| `rossjrw/pr-preview-action` | `@v1` |
