-- Larnix `colab` shortcode — an "Open in Colab" button for a GPU/colab notebook.
--
-- Usage in a chapter:  {{< colab infra/fixtures/colab-fixture.ipynb >}}
--   (the path is the notebook's path within the repository)
--
-- The repo + branch are NOT hardcoded (CLAUDE.md): they come from document/project
-- metadata, with an env-var fallback, so they are set once at publish time:
--   _quarto.yml:  larnix-colab-repo: "OWNER/REPO"
--                 larnix-colab-branch: "main"
--   or env:       LARNIX_COLAB_REPO, LARNIX_COLAB_BRANCH

local function meta_or_env(meta, key, env, default)
  local v = meta[key]
  if v ~= nil then
    local s = pandoc.utils.stringify(v)
    if s ~= "" then return s end
  end
  local e = os.getenv(env)
  if e ~= nil and e ~= "" then return e end
  return default
end

return {
  ["colab"] = function(args, kwargs, meta)
    if #args < 1 then
      error("colab: requires a notebook path, e.g. {{< colab path/to.ipynb >}}")
    end
    local path = pandoc.utils.stringify(args[1])
    local repo = meta_or_env(meta, "larnix-colab-repo", "LARNIX_COLAB_REPO", "OWNER/REPO")
    local branch = meta_or_env(meta, "larnix-colab-branch", "LARNIX_COLAB_BRANCH", "main")

    local url = "https://colab.research.google.com/github/"
      .. repo .. "/blob/" .. branch .. "/" .. path
    local badge = "https://colab.research.google.com/assets/colab-badge.svg"
    local html = '<a class="larnix-colab" target="_blank" rel="noopener" href="'
      .. url .. '"><img src="' .. badge .. '" alt="Open in Colab"></a>'
    return pandoc.RawInline("html", html)
  end,
}
