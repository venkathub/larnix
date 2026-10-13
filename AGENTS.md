# AGENTS.md — Larnix

Original AI/ML Engineering curriculum: 42 modules, 192 lesson plans, 31 authored previews,
static site published to GitHub Pages. No backend, no accounts, no model calls at runtime.

## Commands

- Build: `python3 scripts/build_site.py` (writes `dist/`, git-ignored)
- Full check: `make check` (needs Node 22 on PATH and `labs/data-foundations/requirements.txt` installed)
- Curriculum only: `python3 scripts/curriculum.py check`; regenerate docs: `python3 scripts/curriculum.py render`
- Serve: `python3 -m http.server 8775 --bind 127.0.0.1 --directory dist`

## Source of truth

- `docs/curriculum/curriculum.json` and `sources.json` are authoritative. Module pages,
  INDEX, LEARNING_PATH, COVERAGE, AUDIT, SOURCES and DELIVERY are generated; edit the records
  and re-render.
- `web/lessons.json` is the only source of preview availability. Lesson `status` must agree
  with it; the checker fails otherwise.
- Authored foundation notes live in `samples/foundations/*.json`; specialist labs in
  `samples/<slug>/` with their own tests under `tests/`.

## Conventions

- Original content only. The reference playbook is background; nothing is copied from it.
- Label fixtures and results as synthetic, simulated, replayed or measured. Never present a
  demo as production evidence or a preview as a complete lesson.
- Keep lessons to the ten-minute core with optional deeper sections; follow
  `docs/curriculum/TEACHING_DESIGN.md`.
- No new runtime dependencies for the site. Python standard library for scripts; pinned
  versions for labs.
- Conventional Commits. Branch `codex/<slug>` from `main`; PR to `main`; CI must pass.

## Do not

- Hand-edit generated Markdown.
- Change a lesson status to `preview` or `complete` without the manifest entry or evidence files.
- Add analytics, external fonts, tracking or remote calls to the site.
- Claim learner validation, accessibility audits or CI results that did not run.
