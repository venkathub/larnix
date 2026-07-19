-- Larnix `quiz` shortcode.
--
-- Usage in a chapter:  {{< quiz quiz-chNN.yml >}}
--
-- Reads the referenced YAML quiz file at render time, converts it to JSON, and
-- embeds it in a mount <div> that the client-side engine (larnix-quiz.js) renders
-- and scores. The quiz file is validated separately in CI by infra/ci/quiz_lint.py.
--
-- YAML parsing (review 2026-07-19 / D0017): quiz files are parsed with the
-- vendored lua-tinyyaml (tinyyaml.lua, same parser quarto-live bundles) instead
-- of the previous trick of round-tripping the YAML through Pandoc *markdown
-- metadata*. The round-trip applied typographic transforms (smart quotes,
-- em-dashes) to prompts/options and flattened any markdown via stringify;
-- tinyyaml returns the strings exactly as authored and preserves ints/bools
-- (`answer:`, `shuffle:`) natively.

local tinyyaml = dofile(
  pandoc.path.join({ pandoc.path.directory(PANDOC_SCRIPT_FILE), "tinyyaml.lua" })
)

-- Read the quiz file, trying the document's directory first, then the path as given.
local function read_quiz_file(relpath)
  local candidates = {}
  local input = nil
  pcall(function() input = quarto.doc.input_file end)
  if input and input ~= "" then
    table.insert(candidates, pandoc.path.join({ pandoc.path.directory(input), relpath }))
  end
  table.insert(candidates, relpath)
  for _, p in ipairs(candidates) do
    local fh = io.open(p, "r")
    if fh then
      local content = fh:read("*a")
      fh:close()
      return content
    end
  end
  return nil
end

return {
  ["quiz"] = function(args, kwargs)
    if #args < 1 then
      error("quiz: requires a quiz file path, e.g. {{< quiz quiz-ch01.yml >}}")
    end
    local relpath = pandoc.utils.stringify(args[1])
    local content = read_quiz_file(relpath)
    if not content then
      error("quiz: could not read quiz file '" .. relpath .. "'")
    end

    local ok, data = pcall(tinyyaml.parse, content)
    if not ok or type(data) ~= "table" then
      error("quiz: could not parse '" .. relpath .. "' as YAML: " .. tostring(data))
    end
    local json = quarto.json.encode(data)

    -- Register the engine assets once (Quarto de-duplicates the dependency).
    quarto.doc.add_html_dependency({
      name = "larnix-quiz",
      version = "1.0.0",
      scripts = { "resources/larnix-quiz.js" },
      stylesheets = { "resources/larnix-quiz.css" },
    })

    local html = '<div class="larnix-quiz" data-larnix-quiz>'
      .. '<script type="application/json" class="larnix-quiz-data">'
      .. json
      .. "</script></div>"
    return pandoc.RawBlock("html", html)
  end,
}
