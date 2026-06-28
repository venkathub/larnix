-- Larnix `quiz` shortcode.
--
-- Usage in a chapter:  {{< quiz quiz.yml >}}
--
-- Reads the referenced YAML quiz file at render time, converts it to JSON, and
-- embeds it in a mount <div> that the client-side engine (larnix-quiz.js) renders
-- and scores. The quiz file is validated separately in CI by infra/ci/quiz_lint.py.

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

-- Recursively convert a Pandoc Meta value into plain Lua tables/strings/bools.
local function meta_convert(v)
  local lt = type(v)
  if lt == "boolean" or lt == "number" or lt == "string" then
    return v
  end
  if lt ~= "table" then
    return tostring(v)
  end
  local pt = pandoc.utils.type(v)
  if pt == "Inlines" or pt == "Blocks" then
    return pandoc.utils.stringify(v)
  end
  -- Decide list vs. map.
  local is_array = (pt == "List")
  if not is_array then
    is_array = true
    for k in pairs(v) do
      if type(k) ~= "number" then
        is_array = false
        break
      end
    end
    if next(v) == nil then
      is_array = false
    end
  end
  local out = {}
  if is_array then
    for i, x in ipairs(v) do
      out[i] = meta_convert(x)
    end
  else
    for k, x in pairs(v) do
      out[tostring(k)] = meta_convert(x)
    end
  end
  return out
end

return {
  ["quiz"] = function(args, kwargs)
    if #args < 1 then
      error("quiz: requires a quiz file path, e.g. {{< quiz quiz.yml >}}")
    end
    local relpath = pandoc.utils.stringify(args[1])
    local content = read_quiz_file(relpath)
    if not content then
      error("quiz: could not read quiz file '" .. relpath .. "'")
    end

    -- Parse the YAML by reading it as Pandoc markdown metadata.
    local parsed = pandoc.read("---\n" .. content .. "\n---\n", "markdown")
    local data = meta_convert(parsed.meta)
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
