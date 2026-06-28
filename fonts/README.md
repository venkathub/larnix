# fonts

Self-hosted display + body typefaces (latin subset), from
[Fontsource](https://fontsource.org):

- **Fredoka** (weights 500/600/700) — rounded display font for headings.
- **Nunito** (weights 400/600/700/800) — friendly, readable body font.

Self-hosted (not a third-party CDN) to keep the site ₹0, private, and
offline-friendly. Both are licensed under the SIL Open Font License 1.1
(`LICENSE-Fredoka`, `LICENSE-Nunito`). The `@font-face` declarations live in
`theme/_larnix-components.scss` with `url("fonts/…")` relative to the project
root; Quarto bundles the files next to the compiled theme CSS automatically.
