-- Larnix `badge` shortcode.
--
-- Usage in a chapter:
--   {{< badge difficulty=beginner >}}
--   {{< badge compute=browser >}}
--   {{< badge status=stable >}}
--
-- Emits an inline <span> whose VISIBLE LABEL carries the meaning (so meaning is
-- never colour-only); the coloured dot is decorative CSS. An aria-label gives
-- screen readers the dimension + value (e.g. "difficulty: Beginner").

local LABELS = {
  difficulty = { beginner = "Beginner", intermediate = "Intermediate", advanced = "Advanced" },
  compute    = { browser = "Browser", colab = "Colab", gpu = "GPU" },
  status     = { stable = "Stable", frontier = "Frontier" },
}

-- Read a kwarg as a trimmed string, or nil if absent/empty.
local function kwarg(kwargs, key)
  local v = kwargs[key]
  if v == nil then return nil end
  local s = pandoc.utils.stringify(v)
  if s == nil or s == "" then return nil end
  return s
end

local function escape(s)
  return s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;")
end

return {
  ["badge"] = function(args, kwargs)
    for _, dim in ipairs({ "difficulty", "compute", "status" }) do
      local value = kwarg(kwargs, dim)
      if value ~= nil then
        local label = LABELS[dim][value]
        if label == nil then
          error("badge: unknown " .. dim .. " value '" .. value
            .. "'. Allowed: " .. table.concat((function()
              local ks = {} ; for k in pairs(LABELS[dim]) do ks[#ks + 1] = k end ; return ks
            end)(), ", "))
        end
        local cls = "larnix-badge badge-" .. dim .. " badge-" .. value
        local aria = dim .. ": " .. label
        local html = '<span class="' .. cls .. '" role="img" aria-label="'
          .. escape(aria) .. '">' .. escape(label) .. "</span>"
        return pandoc.RawInline("html", html)
      end
    end
    error("badge: requires one of difficulty=, compute=, status=")
  end,
}
