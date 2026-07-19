# modules

Curriculum content. Each module lives in `/modules/<NN>-<slug>/` and contains:

- chapters authored as `.qmd` / `.ipynb`
- a module `README.md` (objectives, prereqs, chapter list, capstone)
- per-chapter `quiz-chNN.yml` + one cumulative `module-quiz.yml`
- `capstone.md` with a rubric (front-matter `title:` — it renders as a site page)

Modules are built one per session, in dependency order. See `docs/ROADMAP.md`.
