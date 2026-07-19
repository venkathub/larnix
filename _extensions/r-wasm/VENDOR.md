# Vendored extension provenance

## `live/` — quarto-live (r-wasm)

- **Upstream:** <https://github.com/r-wasm/quarto-live>
- **Upstream commit:** `d1459f7968efca5ccdb3cb8a993a399ec6d3e102`
  (2026-05-22, "Update webR to v0.6.0")
- **Extension version:** `0.1.3-dev` · **Pyodide pinned inside:** v0.28.1
- **Verification (2026-07-19):** the commit was not recorded at vendor time;
  it was reconstructed by hashing the vendored tree against upstream history —
  `diff -r` of `_extensions/live/` at that commit vs this directory = **0 lines**
  (byte-identical; neighbouring commits differ by 42–60 lines). See
  `docs/DECISIONS.md D0017`.
- **Local modifications:** none. Larnix customizations (Setting-up/Running
  indicator split, runtime watchdog) live in `theme/_after-body.html` and patch
  at runtime — this directory stays pristine so future upstream diffs are clean.
- **Policy:** any future vendor update must record the new upstream commit here
  and in `DECISIONS.md`, and re-verify `theme/_after-body.html`'s patches
  against the new internals.

Note: `_extensions/larnix/quiz/tinyyaml.lua` is copied from this extension's
`resources/tinyyaml.lua` (lua-tinyyaml, MIT) — same upstream commit.
