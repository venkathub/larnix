# fonts

Self-hosted [Inter](https://rsms.me/inter/) (latin subset, weights 400/500/600/700)
from [@fontsource/inter](https://www.npmjs.com/package/@fontsource/inter).

Self-hosted (not loaded from a third-party CDN) to keep the site ₹0, private, and
offline-friendly. Inter is licensed under the SIL Open Font License 1.1 — see
`LICENSE`. The `@font-face` declarations live in `theme/_larnix-components.scss`
with a `url("fonts/…")` relative to the project root; Quarto bundles the files
next to the compiled theme CSS automatically.
