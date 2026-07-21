# ASSETS — dataset & media license ledger

> Every file under `modules/**/data/` (and any other vendored asset) is recorded
> here with its source and license (R11). CI (`infra/ci/assets_check.py`) fails if
> a `data/` file is not ledgered below. Keep entries in sync when you add data.

## Datasets

| File | Used in | Source | License | Rows | Size |
|------|---------|--------|---------|------|------|
| `modules/03-data/data/penguins.csv` | M3 — Data & Tooling (running example + EDA) | [allisonhorst/palmerpenguins](https://github.com/allisonhorst/palmerpenguins) `inst/extdata/penguins.csv` (vendored 2026-06-28) | CC0-1.0 (Creative Commons Zero v1.0 Universal) — verified via GitHub API `license.spdx_id = CC0-1.0` | 344 | ~15 KB |
| `modules/01-python/data/habits.csv` | M1 — Python for AI (running example; progressive data-cleaning) | Synthetic — authored by Larnix (no real persons; deliberately "messy" for teaching) | CC0-1.0 — dedicated to the public domain by Larnix | 35 | ~1 KB |
| `modules/04-classical-ml/data/penguins.csv` | M4 — Classical ML (classification thread, Ch5+) | Byte-identical copy of `modules/03-data/data/penguins.csv` (P2-D2: "penguins return"; copied because `lib/data.py` loads relative to the module dir; `cmp`-verified 2026-07-21) | CC0-1.0 (same file/licence as the M3 entry above) | 344 | ~15 KB |
| `modules/04-classical-ml/data/california-housing-sample.csv` | M4 — Classical ML (regression running thread, "apprentice appraiser") | scikit-learn `fetch_california_housing` (1990 U.S. Census block groups via StatLib); seeded 800-row sample by `infra/datasets/make_california_sample.py` (seed 0, 4-dp rounding; vendored 2026-07-19) | Public domain (1990 U.S. Census derivative; distributed by scikit-learn itself, BSD-licensed loader) | 800 (of 20,640) | ~50 KB |
| `modules/06-vision-sequences/data/glove-50d-sample.csv` | M6 — Vision & Sequences Ch13 (in-browser semantic search / embeddings) | Stanford NLP GloVe `glove.6B.50d.txt` (Wikipedia 2014 + Gigaword 5, uncased); curated 135-word subset by `infra/datasets/make_glove_sample.py` (3-dp; official HF/Stanford mirrors; vendored 2026-07-19) | PDDL (Open Data Commons Public Domain Dedication and License) — "Pre-trained word vectors are made available under the Public Domain Dedication and License" (stanfordnlp/GloVe README, re-verified 2026-07-19) | 135 words × 50d (of 400K vocab) | ~44 KB |

## Runtime-fetched datasets & pretrained weights (not vendored)

These P2 assets are downloaded at runtime on Colab (torchvision / direct fetch)
or vendored later with their owning task; nothing is redistributed by this
repo, but R11 requires their licences recorded **before** any chapter uses
them. All licences re-verified 2026-07-19 (`P2_SPEC.md §9` + this build).

| Asset | Used in | Fetched via | License / attribution |
|-------|---------|-------------|------------------------|
| MNIST | M5 Ch11–18 + capstone (digits thread at full scale) | `torchvision.datasets.MNIST` at runtime on Colab | CC BY-SA 3.0 — © Yann LeCun & Corinna Cortes; attribution required in the chapter |
| Fashion-MNIST | M6 Ch4–5 (CNN training) | `torchvision.datasets.FashionMNIST` | MIT — Zalando Research (GitHub API `license.spdx_id = MIT`, verified 2026-07-19) |
| Oxford-IIIT Pets (2-class subset) | M6 Ch6–7 + capstone (transfer learning) | `torchvision.datasets.OxfordIIITPet` | CC BY-SA 4.0 — Parkhi et al., VGG Oxford |
| SSA baby names | M6 Ch8–14 (char-level name generator, makemore lineage) | direct fetch of `ssa.gov/oact/babynames/names.zip` in the companion (US-gov data.gov catalog entry) | US-government public domain |
| UCI Bank Marketing | M4 capstone ("will this customer subscribe?", imbalanced) | sample **to be vendored with the M4 capstone task** (P2 §6.B task 28); row added then | CC BY 4.0 — Moro, Laureano & Cortez (2011), UCI ML Repository ID 222; citation required |
| ResNet-18/50 pretrained weights | M6 Ch5–6 + capstone (transfer learning) | `torchvision.models` weights download at runtime | BSD-3-Clause (torchvision), weights trained on ImageNet — ImageNet's own terms restrict the *images*, not these derived weights; the chapter uses weights only. First **model** asset in this ledger. |

## Notes

- **Palmer Penguins** is collected by Dr. Kristen Gorman and the Palmer Station LTER
  (part of the US Long Term Ecological Research Network). The `palmerpenguins`
  package and its data are released under CC0-1.0. We vendor the CSV (rather than
  fetch at runtime) so chapters load offline and CI twins stay deterministic (P1-D8).
- **`habits.csv`** is fully synthetic. Its messiness — missing values, stray units
  (`8h`, `7,500`), inconsistent mood labels (`Good`/`good`/`GOOD`/` ok `), duplicate
  rows, mixed date formats, and impossible values — is intentional teaching material
  for M1's cleaning thread. As our own work we dedicate it to the public domain (CC0-1.0).
- **California-Housing sample**: derived samples are produced by committed, seeded
  scripts in `infra/datasets/` (P2-D2) so they can be regenerated byte-for-byte.
  Pace & Barry (1997), *Sparse Spatial Autoregressions*; the full 20,640-row set is
  noted in M4 as a Colab aside, the vendored sample keeps the browser tier at ₹0.
- **GloVe subset**: Pennington, Socher & Manning (2014), *GloVe: Global Vectors for
  Word Representation*. The 135-word vocabulary is curated for teaching (analogy
  families, country↔capital pairs, semantic clusters); the sampling script fetches
  only the needed zip member via HTTP range requests (~8 MB, not the 822 MB archive)
  from Stanford's official mirrors. Vendored-subset sanity check at build: `king −
  man + woman → queen`; `dog → cat`; `paris → france`.
- **MNIST licence note**: CC BY-SA 3.0 is share-alike, which is fine because we vendor
  nothing — torchvision downloads it in the learner's own session; chapters carry the
  LeCun & Cortes attribution.

## License texts

- CC0-1.0: <https://creativecommons.org/publicdomain/zero/1.0/>
- PDDL-1.0: <https://opendatacommons.org/licenses/pddl/>
- CC BY 4.0: <https://creativecommons.org/licenses/by/4.0/>
- CC BY-SA 3.0 / 4.0: <https://creativecommons.org/licenses/by-sa/3.0/> ·
  <https://creativecommons.org/licenses/by-sa/4.0/>
- MIT: <https://opensource.org/license/mit/>
- BSD-3-Clause: <https://opensource.org/license/bsd-3-clause/>
