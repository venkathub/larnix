-- Larnix chapter-meta filter (review 2026-07-19, finding U8).
--
-- Chapters carry CI-validated front-matter (est_minutes, prereqs, difficulty…)
-- that was never SHOWN to the learner — a Varsity-style reader wants "⏱ ~20 min
-- · Needs: M0 Ch1" before committing to a chapter. This filter renders that
-- strip automatically from front-matter on every page that declares `compute:`
-- (the chapter marker used across the CI gates), so authors add nothing and the
-- strip can never drift from the validated metadata.
--
-- Registered project-wide in `_quarto.yml` (`filters:`), so it applies to both
-- the plain `html` pages (which skip it — no `compute:`) and the `live-html`
-- chapters.
--
-- Extending the strip (maintainer note, per PR #5 AI review): to surface a new
-- front-matter field, (1) make sure it is validated first in
-- `infra/ci/frontmatter_lint.py` (the strip renders only CI-validated
-- metadata — that is the whole point), (2) append a `table.insert(parts, …)`
-- below with the same "label: value" shape, (3) style stays automatic — the
-- output is one `<div class="lx-chapter-meta">` (see theme/_larnix-components
-- .scss), (4) the e2e smoke test asserts the strip renders (`.lx-chapter-meta`
-- in infra/e2e/tests/smoke.spec.js), so a broken filter fails CI.

local function stringify(v)
  return pandoc.utils.stringify(v)
end

function Pandoc(doc)
  local meta = doc.meta
  -- Only chapters (same marker the CI gates use).
  if not meta.compute or not meta.est_minutes then
    return doc
  end

  local parts = {}
  table.insert(parts, "⏱ ~" .. stringify(meta.est_minutes) .. " min, reading + running the code")

  if meta.prereqs then
    local names = {}
    local pt = pandoc.utils.type(meta.prereqs)
    if pt == "List" then
      for _, p in ipairs(meta.prereqs) do
        table.insert(names, stringify(p))
      end
    else
      table.insert(names, stringify(meta.prereqs))
    end
    if #names > 0 then
      table.insert(parts, "Needs: " .. table.concat(names, " · "))
    end
  end

  local strip = pandoc.Div(
    { pandoc.Para({ pandoc.Str(table.concat(parts, "  ·  ")) }) },
    pandoc.Attr("", { "lx-chapter-meta" })
  )
  doc.blocks:insert(1, strip)
  return doc
end
