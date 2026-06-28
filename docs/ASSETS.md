# ASSETS — dataset & media license ledger

> Every file under `modules/**/data/` (and any other vendored asset) is recorded
> here with its source and license (R11). CI (`infra/ci/assets_check.py`) fails if
> a `data/` file is not ledgered below. Keep entries in sync when you add data.

## Datasets

| File | Used in | Source | License | Rows | Size |
|------|---------|--------|---------|------|------|
| `modules/03-data/data/penguins.csv` | M3 — Data & Tooling (running example + EDA) | [allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins) `inst/extdata/penguins.csv` (vendored 2026-06-28) | CC0-1.0 (Creative Commons Zero v1.0 Universal) — verified via GitHub API `license.spdx_id = CC0-1.0` | 344 | ~15 KB |
| `modules/01-python/data/habits.csv` | M1 — Python for AI (running example; progressive data-cleaning) | Synthetic — authored by Larnix (no real persons; deliberately "messy" for teaching) | CC0-1.0 — dedicated to the public domain by Larnix | 35 | ~1 KB |

## Notes

- **Palmer Penguins** is collected by Dr. Kristen Gorman and the Palmer Station LTER
  (part of the US Long Term Ecological Research Network). The `palmerpenguins`
  package and its data are released under CC0-1.0. We vendor the CSV (rather than
  fetch at runtime) so chapters load offline and CI twins stay deterministic (P1-D8).
- **`habits.csv`** is fully synthetic. Its messiness — missing values, stray units
  (`8h`, `7,500`), inconsistent mood labels (`Good`/`good`/`GOOD`/` ok `), duplicate
  rows, mixed date formats, and impossible values — is intentional teaching material
  for M1's cleaning thread. As our own work we dedicate it to the public domain (CC0-1.0).

## License texts

- CC0-1.0: <https://creativecommons.org/publicdomain/zero/1.0/>
