# P2_SPEC — Core ML & Deep Learning (M4–M6)

> **Phase:** P2 — *Core ML & Deep Learning* (per `ROADMAP.md §3 P2`).
> **Status:** ✅ **APPROVED (2026-07-19).** Spec groomed, researched, and confirmed: **all P2
> decisions confirmed at their recommended option** — the pedagogical set (P2-D1…D5) logged as
> **`DECISIONS.md` D0019**, the technical set (P2-D6…D11, incl. the research-driven P2-D6
> reversal: XGBoost is a Pyodide 0.28.1 built-in and stays in-browser) as **D0020**. Q-7
> confirmed at ≥3 calibration runs. Load-bearing claims web/codebase-validated 2026-07-19 (§9).
> Build proceeds with §6.A Task 1; no chapter is authored before its one-paragraph plan is
> approved (`CLAUDE.md`).
> **Authoritative parents:** `CLAUDE.md` (operating agreement, generic DoD), `ROADMAP.md §3 P2`
> (phase goal + exit criteria), `Larnix-PLAN.md` (canonical M4–M6 chapter lists), `STYLE_GUIDE.md`
> (Varsity contract + the D0017 content conventions), `CHAPTER_TEMPLATE.md` (front-matter schema),
> `RISKS.md` (R1/R3/R4/R6/R9/R10/R11/R12/R13 live in this phase), `docs/phases/P0_SPEC.md` (Colab
> shortcode + GPU-notebook CI policy, D0012), `docs/phases/P1_SPEC.md` (the at-scale conventions
> this phase inherits: generated twins, single-sourced grader, quiz structure, dataset ledger).
> **Entry criteria:** P1 DoD met ✅ (closed 2026-06-29; re-verified by the 2026-07-19 review,
> D0017 — render/e2e/a11y gates now standing).
> **Last updated:** 2026-07-19

P2 is the phase where the learner **stops exploring data and starts training models** — and where
the platform crosses its two hardest technical bridges: (1) **auto-grading model training**, whose
outputs are stochastic, and (2) the **browser → free-GPU handoff**, the first time a chapter
cannot run in Pyodide. P1's bet was "scale without regression"; P2's bet is *"the pedagogy and the
gates survive nondeterminism and a second compute tier."* Everything else — the Varsity contract,
generated twins, the quiz engine, the six-plus-gates CI — is inherited, not rebuilt.

---

## 1. Scope

### 1.1 In scope — modules + chapters

Three modules, authored to the full Varsity contract. **All chapters `status: stable`** (this is
the stable core — classical ML, backprop, CNNs/RNNs are written to last; nothing frontier ships
in P2).

| Module | Title | ~Ch | Tier | Dominant compute | Capstone |
|--------|-------|-----|------|------------------|----------|
| **M4** | Classical Machine Learning | 20 | 🟡 | **browser** (fully — incl. XGBoost, see P2-D6) | End-to-end tabular predictor + **model card** |
| **M5** | Deep Learning Foundations | 18 | 🟡 | **browser Ch1–10 → colab Ch11–18** (P2-D4) | Digit classifier from scratch → re-implemented in PyTorch |
| **M6** | Specialized DL: Vision & Sequences | 14 | 🟡→🔴 | **mixed** (browser for intuition/NumPy chapters, colab for training) | Image-classifier app + char-level sequence model |

**Total: ~52 chapters**, 3 module quizzes, 3 rubric-graded capstones, 3 module landings/READMEs,
plus the shared tooling in §6.A (stochastic-grader extensions, the Colab companion-notebook
pipeline, the CPU-scaled CI tier).

Subsystems exercised (`CLAUDE.md` → Architecture): **Content** (M4–M6), **Interactive Compute**
(the first real `colab` chapters: Colab/Kaggle templates, the handoff UX), **Auto-Grading**
(seeded/tolerance + property asserts for stochastic training — the load-bearing new capability),
**Assessment** (quizzes + the first 🟡-tier capstones; SR cards seeded per chapter), **Currency &
Ops** (GPU-notebook CI policy exercised for real; new colab-policy gate; dataset/weights ledger).

New learner-visible capabilities this phase must prove:

1. **The free-GPU workflow**: a learner clicks "Open in Colab", runs a training notebook on a free
   T4, and their exercise grades itself inside Colab.
2. **Stochastic auto-grading**: exercises that *train* something still grade deterministically
   (seeded) in the browser, and by property thresholds ("loss fell ≥ 80%", "test accuracy ≥ 0.95")
   on GPU.
3. **Evaluation as a habit**: the ROADMAP's eval spine starts here — train/val/test, metrics, CV
   arrive *early* in M4 (P2-D1), and every capstone must report a measured number and (for M4) a
   **model card**.

### 1.2 Non-goals (explicit — to prevent scope creep)

- **No attention, no transformers, no NLP-task depth.** M6 Ch14 ("limits of RNNs") *motivates*
  attention and stops there. Tokenization, self-attention, GPTs are **M7 (P3)**.
- **No LLMs, no GenAI, no API keys, no Ollama.** Nothing in P2 calls a hosted model. The R6 gate
  stays green by construction. The Ollama/free-API fallback pattern is **P3**.
- **No `status: frontier` chapters.** All of M4–M6 is stable core. Named architectures
  (LeNet→ResNet) are taught as history/design lineage, version-light. The quarterly-refresh
  machinery is exercised in **P3**.
- **No rented GPU, ever, in P2.** Free Colab/Kaggle T4-class only. **No M11 specifics** —
  tokenizer choice, model size, GPU provider are **P4** decisions and stay undecided here.
- **No second DL framework.** PyTorch only (PLAN's standing choice; reaffirmed, not reopened).
  No TensorFlow/Keras/JAX, no Lightning/fastai wrappers — M5 teaches raw `nn.Module` + a
  hand-rolled training loop precisely because the abstraction is the lesson.
- **No deployment/serving/MLOps.** The M6 "image-classifier app" is a notebook (+ optional
  in-Colab Gradio cell as a 🔬 aside); Docker/FastAPI/monitoring are **M13 (P5)**.
- **No AutoML / tuning frameworks.** Hyperparameter search stays at `GridSearchCV`/manual LR
  sweeps; Optuna/W&B sweeps are out (W&B free tier first appears M13).
- **No new assessment subsystems.** SR cards are *seeded* (P6 scheduler consumes them);
  no certification, accounts, or server-side anything (R7).
- **No re-teaching M3.** Pandas/EDA are prerequisites; M4 uses them without re-explaining.
- **Chapter-count discipline:** PLAN's 20/18/14 held, with ≤3 documented merges allowed (P2-D5).

---

## 2. Content design (per module)

Conventions: difficulty 🟢/🟡/🔴; compute per chapter as shown; `status: stable` everywhere. Each
module threads **one running example** (`STYLE_GUIDE §4`) — confirmed in **P2-D2**. All browser
chapters keep the P1 machinery (generated twins, VFS grader, quick-check quiz, 3 SR cards);
colab chapters use the new §3 P2-D8/P2-D9 machinery.

### M4 — Classical Machine Learning 🟡 · browser

- **Learning objectives.** A learner can: (1) frame a problem as supervised/unsupervised learning;
  (2) train, tune, and **honestly evaluate** models with scikit-learn (split/CV, the right metric,
  leakage awareness); (3) explain *why* models fail (overfitting, bias–variance, imbalance);
  (4) run the full tabular workflow end-to-end and write a **model card**.
- **Running thread.** *"The apprentice appraiser."* An intern learns to price houses from examples
  — and is graded only on houses they've never seen (generalization = the module's spine).
  **Regression thread:** a vendored ~1,000-row sample of **California Housing** (P2-D2).
  **Classification thread:** **Palmer Penguins returns** — the learner already knows this data
  from M3, so every new algorithm lands on familiar ground. Capstone transfers to a *new* dataset.
- **Ordering note.** Evaluation moves **early** (Ch4–8) instead of PLAN's late block — see P2-D1.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | What is learning? | Rules-by-hand vs rules-from-examples; the appraiser-intern framing. | 🟢 | browser |
| 2 | Linear regression | Fit the first line; predictions from one then many features. | 🟡 | browser |
| 3 | Cost functions & gradient descent | "How wrong am I?" as a number; walking downhill (reuses M2 Ch7). | 🟡 | browser |
| 4 | Generalization: train/val/test & cross-validation | The exam the intern hasn't seen; MAE/RMSE; the cardinal sin of leakage. | 🟡 | browser |
| 5 | Logistic regression | From "how much" to "which one"; probabilities, thresholds. | 🟡 | browser |
| 6 | Classification metrics | Accuracy lies; precision/recall/F1/ROC-AUC with a confusion matrix you read. | 🟡 | browser |
| 7 | Overfitting & regularization | Memorizing vs learning; L1/L2 as a leash. | 🟡 | browser |
| 8 | Bias–variance | Underfit vs overfit as one picture; the tradeoff curve, plotted live. | 🟡 | browser |
| 9 | K-nearest neighbours | The "ask your neighbours" model; distance, k, scaling matters. | 🟡 | browser |
| 10 | Decision trees | 20-questions as a model; splits, purity, depth. | 🟡 | browser |
| 11 | Random forests & ensembles | Ask a crowd of trees; bagging & feature randomness. | 🟡 | browser |
| 12 | Gradient boosting (+ XGBoost) | Each tree fixes the last one's mistakes; sklearn's `HistGradientBoosting` then real XGBoost — both in-browser (P2-D6: xgboost is a Pyodide 0.28.1 built-in). | 🟡 | browser |
| 13 | Support vector machines | The widest-street boundary; kernels in one picture. | 🟡 | browser |
| 14 | Naive Bayes | Bayes from M2 Ch12 becomes a classifier; why "naive" still works. | 🟡 | browser |
| 15 | Imbalanced data | When 99% accuracy is useless; resampling, class weights, the right metric. | 🟡 | browser |
| 16 | Feature engineering | Making the data easier to learn from; encoding, scaling, leakage traps. | 🟡 | browser |
| 17 | k-means clustering | Finding groups with no labels; inertia & the elbow. | 🟡 | browser |
| 18 | Hierarchical clustering | Grouping by merging; dendrograms (merge candidate — P2-D5). | 🟡 | browser |
| 19 | PCA & dimensionality reduction | Squashing dimensions while keeping the story. | 🟡 | browser |
| 20 | The scikit-learn workflow + your first model card | Pipelines end-to-end; documenting what you built, for whom, and where it fails. | 🟡 | browser |

### M5 — Deep Learning Foundations 🟡 · browser → colab

- **Learning objectives.** A learner can: (1) build a neural net **from scratch** — neuron →
  autograd engine (micrograd) → MLP — and explain every line of backprop; (2) translate that
  understanding into idiomatic PyTorch (`tensor`/`autograd`/`nn.Module`/training loop); (3) run
  the free-GPU workflow (Colab/Kaggle) confidently; (4) train reproducibly — seeds, checkpoints,
  diagnosing loss curves.
- **Running thread.** *"Teach the machine to read your handwriting."* One goal for 18 chapters:
  a digit classifier. First half builds it **by hand in the browser** on sklearn's built-in 8×8
  `digits` (Pyodide-safe, ₹0); second half rebuilds it **properly in PyTorch on MNIST** on a free
  Colab GPU. Backprop's recurring analogy: **the blame game** — every knob learns how much it
  contributed to the error (extends M2's "one neuron" thread; M2 Ch16 is the stated prereq).
- **The compute split is the pedagogy** (P2-D4): Ch1–10 `browser` (pure Python/NumPy — micrograd
  is dependency-free), Ch11 is the **handoff chapter**, Ch11–18 `colab`.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | From logistic regression to a neuron | The M4 model you know *is* a one-neuron network. | 🟡 | browser |
| 2 | Activation functions | Why stacking straight lines needs a bend; sigmoid/tanh/ReLU. | 🟡 | browser |
| 3 | Layers & networks | Neurons in rows; what "hidden layer" actually holds. | 🟡 | browser |
| 4 | The forward pass | Data flows through: matrices from M2 doing the work, by hand. | 🟡 | browser |
| 5 | Loss functions | MSE vs cross-entropy; picking the score to descend on. | 🟡 | browser |
| 6 | Backpropagation, spelled out | The blame game: chain rule (M2 Ch8) walked end-to-end on paper + code. | 🟡 | browser |
| 7 | Gradient-descent variants | SGD, momentum, Adam — same downhill walk, smarter steps. | 🟡 | browser |
| 8 | Build micrograd I: the autograd engine | A `Value` that remembers its history and back-propagates itself. | 🟡 | browser |
| 9 | Build micrograd II: backward through a graph | Topological order, `backward()`, gradient-check vs finite differences. | 🟡 | browser |
| 10 | An MLP from scratch | Assemble micrograd neurons into a net; train on 8×8 digits, in-browser. | 🟡 | browser |
| 11 | GPUs & your first Colab notebook | Why training needs parallel hardware; the ₹0 Colab/Kaggle workflow, step by step (the handoff — P2-D4). | 🟡 | colab |
| 12 | Enter PyTorch: tensors & autograd | Micrograd, industrial-strength; `.backward()` you already understand. | 🟡 | colab |
| 13 | `nn.Module` & the training loop | The five-line loop you'll write for the rest of the school. | 🟡 | colab |
| 14 | Dropout & batch norm | Making nets trainable and less overfit; what each actually does. | 🟡 | colab |
| 15 | Initialization & learning-rate tuning | Why bad starts kill training; LR too high/low, seen on real curves. | 🟡 | colab |
| 16 | Diagnosing training | Read loss curves like an engineer: overfit, underfit, bugs. | 🟡 | colab |
| 17 | Saving, loading & checkpoints | `state_dict`, resuming, not losing an hour of GPU time. | 🟡 | colab |
| 18 | A reproducible training harness | Seeds, configs, logged metrics — the template every later module reuses. | 🟡 | colab |

### M6 — Specialized DL: Vision & Sequences 🟡→🔴 · mixed

- **Learning objectives.** A learner can: (1) explain convolution/pooling and build + train CNNs;
  (2) **fine-tune a pretrained vision model** (transfer learning — the working practitioner's
  default); (3) build RNN/LSTM models and explain *why* they struggle with long sequences;
  (4) use **embeddings** for similarity/search — the conceptual bridge to M7.
- **Running thread.** *"Teach the machine to see, then to read."* Two acts, one arc. **Vision
  act:** Fashion-MNIST (train a CNN) → a small real-image dataset via transfer learning.
  **Sequence act:** a char-level **name generator** (makemore-style, public-domain SSA names —
  P2-D2) that ends by *failing* on long-range structure — the cliffhanger that motivates M7's
  attention. Intuition chapters stay in the browser (NumPy convolution on real image arrays);
  training chapters are colab.

| # | Chapter | One-line | Tier | Compute |
|---|---------|----------|------|---------|
| 1 | Images as tensors | A photo is a number grid; channels, shapes, slicing pixels live. | 🟡 | browser |
| 2 | Convolution, intuitively | A sliding stencil that detects patterns; build one in NumPy. | 🟡 | browser |
| 3 | Pooling, padding & strides | Shrinking maps without losing the plot; the arithmetic of shapes. | 🟡 | browser |
| 4 | A CNN in PyTorch | Assemble conv→pool→dense; train on Fashion-MNIST with the M5 harness. | 🟡 | colab |
| 5 | LeNet → ResNet: how CNNs grew up | Depth, skip connections; why deeper finally worked. | 🟡 | colab |
| 6 | Transfer learning & fine-tuning | Stand on a pretrained ResNet; retrain the head on your images. | 🟡 | colab |
| 7 | Data augmentation | More data for free: flips, crops, and when augmentation lies. | 🟡 | colab |
| 8 | Sequences & memory | Order matters: text, time series; why a fixed-size net can't read. | 🟡 | browser |
| 9 | RNNs | A loop with a memory; unroll it and it's an MLP through time. | 🔴 | colab |
| 10 | Vanishing gradients | Why plain RNNs forget: the blame signal fades — shown numerically. | 🔴 | browser |
| 11 | LSTM & GRU | Gates that decide what to keep; the fix that carried NLP for a decade. | 🔴 | colab |
| 12 | Word embeddings (word2vec) | Words as vectors; king − man + woman, trained small and for real. | 🔴 | colab |
| 13 | Embeddings for search & similarity | Nearest-neighbour meaning: semantic search on vendored vectors, in-browser. | 🔴 | browser |
| 14 | The limits of RNNs | Watch the name generator fail long-range; the cliffhanger: *attention* (M7). | 🔴 | browser |

---

## 3. Decisions to make now

Provisional IDs `P2-Dn`; **all confirmed at the recommended option (2026-07-19)** and logged in
`DECISIONS.md`: the pedagogical set (**P2-D1…P2-D5**) as **D0019**, the technical set
(**P2-D6…P2-D11**) as **D0020** — following the P1 D0015/D0016 pattern. **The confirmed option
is listed first.** Pedagogical first, then technical.

### Pedagogical

**P2-D1 — M4 chapter ordering: evaluation early or late?** PLAN lists train/val/test, metrics,
overfitting, bias–variance as Ch15–18, *after* all algorithms.

- **(A, rec.) Evaluation-early (the §2 order):** first model (Ch2–3) → immediately *how to judge
  it honestly* (Ch4 split/CV, Ch6 metrics, Ch7–8 overfitting/bias–variance) → the algorithm tour.
  Every later chapter then *practices* evaluation ("fit forest → cross-validate → compare"),
  which is exactly the ROADMAP eval-spine ("first real evaluation practice" is a named P2 skill).
  *Con:* diverges from PLAN's listed order (counts unchanged; logged).
- (B) Hold PLAN's order (algorithms first, eval block late). Familiar textbook shape. *Con:* the
  learner trains nine models before learning that judging them on training data is a sin — the
  worst habit in ML taught by omission for 12 chapters.
- (C) Full eval-first block (all four eval chapters before *any* model). *Con:* violates
  taste-before-theory — evaluating models you've never trained is abstract; weakest hook.

**P2-D2 — Running examples & datasets (one bundle decision, like P1-D2).**

- **(A, rec.)** **M4:** "apprentice appraiser" thread; regression = a **vendored ~1,000-row
  sample of California Housing** (1990 US Census–derived, public domain; sampled to respect the
  ≤~50 KB vendoring rule, full set noted as a Colab aside); classification = **Palmer Penguins
  reused from M3** (already vendored CC0; zero new context cost); capstone on **UCI Bank
  Marketing** (CC BY 4.0) — new domain, naturally *imbalanced* so Ch15 gets real practice, and
  "will this customer subscribe?" is a relatable business problem. **M5:** digits thread —
  sklearn built-in `load_digits` (8×8, browser-safe) → **MNIST** via torchvision on Colab.
  **M6:** **Fashion-MNIST** (MIT licence) for CNN training, a small real-image set for transfer
  learning (e.g. a ~2-class subset of Oxford-IIIT Pets, CC BY-SA), and **SSA baby names**
  (US-gov public domain, makemore lineage) for the char-level thread; a **vendored small GloVe
  subset** (PDDL/Apache-friendly; verify at build) for the browser similarity chapter. All
  ledgered in `docs/ASSETS.md` (R11). *Con:* several new assets to ledger; the housing sample
  needs a documented sampling script.
- (B) One dataset (e.g. penguins) threaded through all three modules. *Con:* penguins can't carry
  regression, imbalance, images, or sequences — the thread would fake it; M5/M6 need
  tensors/text by nature.
- (C) Kaggle competition data throughout (Titanic/House Prices). *Con:* licence/redistribution
  frictions (R11), requires Kaggle account in `browser` chapters, Titanic framing already
  rejected in P1-D2.

**P2-D3 — How deep does "from scratch" go in M5?**

- **(A, rec.) Full scalar micrograd across two chapters (Ch8–9), then an MLP on it (Ch10).**
  Karpathy-lineage, ~150 lines of dependency-free Python — runs beautifully in Pyodide; the
  learner *owns* backprop before PyTorch hides it; gradient-check vs finite differences reuses
  the M2 capstone skill. *Con:* two chapters of pure plumbing before any "real" dataset win —
  mitigated by the Ch10 in-browser digits payoff.
- (B) NumPy-matrix backprop only (hand-derived layer gradients, no autograd engine). Shorter.
  *Con:* the learner never sees *how autograd works*, which is the single best transfer into
  PyTorch (`.backward()` stops being magic); loses the school's signature build-it moment.
- (C) Skip scratch, go straight to PyTorch (fast.ai-style top-down only). *Con:* contradicts
  PLAN's stated M5 objective ("micrograd style") and the mission's build-from-first-principles
  spine; backprop becomes incantation.

**P2-D4 — Where and how the browser→Colab handoff happens.**

- **(A, rec.) A dedicated handoff chapter (M5 Ch11, "GPUs & your first Colab notebook") at the
  scratch→PyTorch seam; everything before it `browser`, everything after `colab`.** Teaches the
  *why* (parallel hardware) and the *how* (account, notebook UX, GPU runtime, session limits,
  Kaggle as the alternate — R13) just-in-time, exactly once; M6+ then assumes it. Moves PLAN's
  "GPUs & why they matter" from slot 15 to the seam — a chapter *about* GPUs belongs where the
  learner first needs one. *Con:* reorders PLAN within-module (logged).
- (B) No dedicated chapter — a "setup" callout in the first PyTorch chapter. *Con:* the single
  biggest drop-off cliff in the whole school (R12) handled in a sidebar; account setup + a new
  concept in one sitting overloads beginners.
- (C) Put the handoff at the start of M5 and do everything (incl. micrograd) on Colab. *Con:*
  surrenders ten ₹0 browser chapters that run fine in Pyodide; violates "browser where feasible"
  (ROADMAP P2 exit criterion).

**P2-D5 — Chapter granularity (scope control on ~52 chapters).**

- **(A, rec.) Hold §2's counts (20/18/14) with ≤3 documented merges allowed** (candidates: M4
  Ch17+18 k-means + hierarchical; M6 Ch3 folding into Ch2 if thin; M5 Ch17 folding into Ch18).
  M5's count reaches PLAN's 18 by splitting micrograd (P2-D3) and adding the handoff chapter
  (P2-D4) while PLAN's "GPUs" chapter is absorbed into the handoff — net counts match PLAN.
  *Con:* mid-phase merges drift counts by ≤3 (each logged, as P1 did — which used 0 of 3).
- (B) Hold PLAN's exact lists/counts verbatim. *Con:* forces thin chapters and keeps the eval
  block late (conflicts with P2-D1/P2-D4 recommendations).
- (C) Consolidate aggressively (~40 chapters). *Con:* breaks one-concept-per-chapter exactly
  where beginners hit the school's steepest grade.

### Technical

**P2-D6 — The gradient-boosting chapter's compute (the "XGBoost problem" — resolved by research,
2026-07-19).** The spec's first draft assumed `xgboost` had no Pyodide build and proposed a Colab
companion. **Web-verified: that premise is stale.** Pyodide **0.28.1** — the exact version our
vendored quarto-live pins (`_extensions/r-wasm/live/live.lua:531` →
`cdn.jsdelivr.net/pyodide/v0.28.1/full/`) — ships **`xgboost 2.1.4` and `lightgbm 4.6.0` as
built-in packages** (pyodide.org 0.28.1 package list). Our own R3 lint's `KNOWN_UNSAFE` entry for
xgboost/lightgbm is therefore factually outdated and must be corrected either way.

- **(A, rec. — revised) Ch12 fully in-browser: concept via sklearn `HistGradientBoosting*`, tool
  via real `xgboost` loaded with `loadPackage`/`micropip` in the same chapter.** M4 becomes 100%
  browser/₹0 — better than ROADMAP's own expectation ("heavier M4 chapters ship a free Colab
  fallback" becomes unnecessary). Implementation notes: (a) move `xgboost`/`lightgbm` from
  `KNOWN_UNSAFE` to the built-in allow-list in `browser_import_lint.py` (with tests); (b) the
  package arrives from the Pyodide CDN on first use — a network download (~a few MB), so the
  chapter carries a "needs internet for this cell" note (the same honesty rule P1-D7 applied to
  Seaborn; acceptable because it's built-in-CDN, not PyPI); (c) CI twin installs the pinned
  `xgboost==2.1.4` wheel under CPython so the twin executes identically. *Con:* first M4 cell
  with a runtime package download; a future quarto-live/Pyodide bump could move the version
  (covered by the vendor policy in D0017 §quarto-live).
- (B) The first draft's split: sklearn in-browser + XGBoost Colab companion. *Con:* now
  unnecessary complexity — two artifacts for a chapter whose tool runs in the browser; would
  also put the first Colab touchpoint in M4, before M5 Ch11 teaches it.
- (C) Skip XGBoost; sklearn boosting only. *Con:* XGBoost is named in PLAN and is the tabular
  workhorse employers expect; omitting it dents the "job-relevant" promise — and now there's no
  technical reason to.

**P2-D7 — Stochastic auto-grader design (the load-bearing P2 tooling; extends `lib/grader.py`).**
Training is random: identical code gives different weights per run. P1's exact/`tol` asserts
can't grade "train a model".

- **(A, rec.) Two explicit modes, chosen by chapter compute.** (1) **Seeded-deterministic** for
  `browser`/CPU twins: the exercise pins every seed (`random`/`numpy`/`torch`, plus documented
  determinism flags); grader asserts with the existing `tol` — same-seed-same-result holds on a
  pinned runtime, and the CI twin proves it. (2) **Property-based** for `colab`/GPU: assert
  *properties of a successful training run*, not values — final loss ≤ X (or fell ≥ N% from
  recorded initial), held-out accuracy ≥ threshold-with-margin, weights actually changed,
  gradient-check within tolerance. Add `run_tests` helpers (e.g. `assert_between`,
  `assert_decreased`) so exercises stay one-liners. Thresholds set with generous margin and
  calibrated on ≥3 recorded Colab runs (logged in the PR). *Con:* property thresholds can pass
  weak-but-lucky solutions — accepted: they grade "did you build a thing that trains", and the
  rubric layer covers quality (R4's match-grader-to-type rule).
- (B) Seeded-deterministic everywhere, incl. GPU. *Con:* GPU nondeterminism (cuDNN kernels,
  atomics) makes bit-exactness a lie on Colab; `torch.use_deterministic_algorithms(True)` slows
  runs and still varies across driver/image versions we don't control (R13). Grading would flake.
- (C) Property-based everywhere. *Con:* throws away the browser tier's genuine determinism, where
  exact expected outputs are the clearest feedback a beginner can get.

**P2-D8 — Colab chapter authoring: how the notebook, grader, and chapter stay in sync.** A
`colab` chapter is a rendered `.qmd` (prose + code with recorded outputs) + a notebook the
learner opens via the P0 `{{< colab >}}` button. Two artifacts = drift risk (the exact class
P1-D10 killed for twins); and Colab has no quarto-live VFS, so the grader can't arrive via
`resources:`.

- **(A, rec.) Generate the companion notebook from the `.qmd`** — extend `make_twin.py` (or a
  sibling `make_colab.py`): tagged cells → companion `.ipynb` with a standard header (title/badge
  cell, pinned-setup cell, **an embedded grader-bootstrap cell** that fetches `lib/grader.py`
  from the repo raw URL with an inlined fallback copy), exercise cells + hidden solutions in the
  P1 pattern. CI `--check` fails on drift, same as twins. Grader logic stays single-sourced;
  Colab is by definition online, so the URL fetch is acceptable there (never in `browser`
  chapters). *Con:* generator work up front; the raw-URL pin must follow the deploy branch.
- (B) Hand-author notebook + `.qmd` separately, paste the grader per notebook. *Con:* re-creates
  the P1-D10 drift problem ×~20 colab chapters; a grader fix means ~20 edits (R9).
- (C) Author `colab` chapters as `.ipynb`-only, render the notebook itself via Quarto. *Con:*
  loses the chapter template/front-matter/lint pipeline that all 51 existing chapters share;
  two authoring formats to maintain; worse diffs.

**P2-D9 — CI execution policy for `colab` chapters (extends D0012).** D0012 says GPU notebooks
are manually Colab-verified, recorded in the PR. But most M5/M6 training code *can* run small on
CPU.

- **(A, rec.) CPU-scaled twin execution in CI + manual Colab verification for the GPU
  experience.** Every colab chapter's companion notebook carries a parameters cell
  (`LARNIX_CI` env → tiny epochs/subset, e.g. MNIST 2k samples × 1 epoch); CI installs
  **CPU-only torch/torchvision (exact-pinned in `requirements-notebooks.txt`)** and executes the
  scaled notebook (budget: ≤ ~90 s/notebook, ~5–8 min added wall-clock). "Everything runs" stays
  *automated* for the code path; the manual recorded Colab run (per D0012) remains required per
  chapter for the real-GPU/full-scale path and calibrates P2-D7 thresholds. *Con:* CI gets
  heavier (torch wheel ~200 MB, cacheable); scaled runs don't prove GPU-specific lines (`.to(
  device)` covered by a device-agnostic pattern, asserted present by lint).
- (B) Manual-only Colab verification (D0012 as-written). *Con:* ~20 chapters whose code CI never
  executes — a regression of the "everything runs" gate (R10) for a third of the phase; drift
  found only at quarterly refresh.
- (C) GPU runners in CI (paid/self-hosted). *Con:* violates ₹0 build discipline; infra overkill
  for content whose CPU-scaled behaviour catches the error classes that matter.

**P2-D10 — Colab vs Kaggle: default and template surface.**

- **(A, rec.) Colab is the default one-click button (P0 shortcode as-is); Kaggle documented once**
  in M5 Ch11 as the named alternate (upload the same `.ipynb`; where the GPU switch lives), per
  R13's "don't hard-couple to one provider". *Con:* Kaggle path is documented-but-not-buttoned;
  acceptable while Colab free tier holds (R13 trigger covers the swap).
- (B) Dual buttons on every chapter. *Con:* 2× verification burden per chapter (~40 manual runs);
  Kaggle's notebook import UX makes deep-links brittle.
- (C) Kaggle default (more generous free GPU quota). *Con:* heavier onboarding (account +
  phone verification), clunkier one-click open from GitHub; Colab is the ecosystem default a
  beginner will meet everywhere else.

**P2-D11 — PyTorch version policy on Colab.** Colab preinstalls torch and rolls its image
forward; exact-pinning `pip install torch==X` there means a big reinstall every session and
fights the platform.

- **(A, rec.) Use Colab's preinstalled torch + a guard cell; exact-pin only in CI.** Companion
  notebooks assert `torch.__version__ >= <floor>` (fail fast with a friendly message), print the
  running version, and the PR records the verified version/date; CI's CPU twins exact-pin (P2-D9)
  so the automated gate is reproducible even when Colab moves. Quarterly refresh (existing R1
  machinery, even though chapters are `stable`) re-verifies floors. *Con:* learner runs float
  within a verified range rather than one bit-exact version — accepted; that's Colab's nature
  (R13) and stable-API code should tolerate it.
- (B) Exact-pin in the notebook (`pip install torch==X.Y.Z`). *Con:* multi-GB reinstall +
  restart-runtime friction *every session* for every learner; CUDA wheel/driver mismatch risk on
  an image we don't control.
- (C) No policy; use whatever's there. *Con:* un-diagnosable learner breakage when Colab bumps;
  no floor to test against.

> **Inherited, not reopened:** quiz format (P1-D11 quick-check + module quiz), scaffolding kit
> (P1-D4, minus `🧱 Java` asides which stay M1-only), twin generation for browser chapters
> (P1-D10), grader VFS loading (P1-D9), dataset vendoring ≤~50 KB + `ASSETS.md` ledger (P1-D8).
> **Deferred (so they are *not* decided in P2):** Ollama/free-API fallback + frontier cadence
> (P3); **all M11 choices — tokenizer, model size, GPU provider (P4)**; SR scheduler, cert,
> tracks (P6).

---

## 4. Exercise & assessment plan

Every chapter ships **2–4 exercises**, guided → genuine implement-from-spec → stretch
(`STYLE_GUIDE §6` incl. the D0017 Ex2 rule), graded by `run_tests` under the P2-D7 mode matching
its compute tier; stretch/open-ended tasks are rubric-graded and labelled (R4). Each chapter
seeds **3 SR cards** (`review_cards:`, linted) → ~52 × 3 ≈ **156 cards**.

### 4.1 Per-module exercise pattern (representative; authored per chapter)

| Module | Ex 1 (guided 🟢) | Ex 2 (implement, auto-graded) | Ex 3 (stretch, rubric) |
|--------|------------------|-------------------------------|------------------------|
| **M4** | Complete one sklearn call (`fit`/`predict`/`cross_val_score`) | Implement the concept small from spec: `mse(y, ŷ)`, `precision_recall(cm)`, gini impurity, one k-means step — asserted on fixed arrays (seeded, exact/`tol`) | "Beat the baseline honestly": improve CV score without leaking; defend with a number |
| **M5 (browser half)** | Fill one line of a forward pass / `Value` op | Implement `Value.__mul__` + backward, `relu`, one SGD step, `mlp_forward` — seeded asserts + finite-difference gradient checks | Extend micrograd (a new op with correct backward); verified by gradient check + rubric |
| **M5 (colab half)** | Complete a training-loop line (`loss.backward()`, `optimizer.step()`) | Implement the loop/module from spec — property asserts: loss fell ≥ N%, test acc ≥ threshold, params changed | Tune LR/architecture to beat a stated target; report curves (rubric) |
| **M6** | Compute an output shape / complete a transform | Implement `conv2d_single_channel` (NumPy, exact), an LSTM gate from equations, `cosine_similarity` search — mode per compute tier | Fine-tune on your own 2-class image set / steer the name generator; measured + rubric |

### 4.2 Quizzes

Inherited P1-D11 structure unchanged: per-chapter `quiz-chNN.yml` (3–4 MCQ, `id:` required) +
one `module-quiz.yml` (~8–12 MCQ) per module on `modules/<NN>/index.qmd`. Module quizzes are
**transfer questions only** (D0017) — e.g. M4's presents a novel scenario ("your fraud model
shows 99.2% accuracy — what do you check first?"); no verbatim chapter-quiz reuse. Quizzes test
only taught content.

### 4.3 Capstones + rubrics (0–2 per criterion; every capstone must report a measured number)

- **M4 — End-to-end tabular predictor + model card** (browser). *Brief:* full workflow on **Bank
  Marketing** (new data, imbalanced): EDA-lite → split *first* → baseline → ≥3 model families
  compared via CV → tuned final model → held-out evaluation → **model card** (intended use, data,
  metrics incl. per-class, limitations). *Auto-check:* leakage tripwire (test rows never seen in
  fit — grader-verifiable), ROC-AUC ≥ floor on the held-out split. *Rubric:* Runs · Honest
  evaluation (split/CV correct, no leakage) · Model comparison (justified choice) · Measurement
  (numbers for every claim) · Model card completeness.
- **M5 — Digits from scratch → PyTorch** (browser + colab, two graded parts). *Brief:* (1) train
  your micrograd/NumPy MLP on 8×8 digits in-browser — auto-check: seeded test accuracy ≥ 0.90 +
  gradient check passes; (2) re-implement in PyTorch on MNIST on Colab with the Ch18 harness —
  auto-check (property): test accuracy ≥ 0.97, loss-curve logged; *transfer twist (D0017):* one
  stated change (e.g. a different hidden size/activation) re-run and compared. *Rubric:* Runs
  (both) · Correct scratch backprop (gradient check) · Idiomatic PyTorch port · Measurement
  (before/after, curves) · Reproducibility (seeded, config-driven).
- **M6 — Image-classifier app + char-level sequence model** (colab). *Brief:* (1) transfer-learn
  a pretrained CNN on a small real-image dataset (goal ≥ 0.90 val accuracy; optional 🔬 Gradio
  cell); (2) train the char-level name generator; sample before/after training; document one
  clear long-range failure (the M7 hook). *Auto-check (property):* val-accuracy floor;
  generator loss fell ≥ N% and samples differ from untrained. *Rubric:* Runs · Transfer-learning
  correctness (frozen vs trained layers explained) · Sequence-model understanding (failure
  analysis) · Measurement · Honesty about limits.

### 4.4 Where SR cards are seeded

Per chapter (3 from Key Takeaways) as in P1; capstone pages seed none (unchanged convention).
The P6 scheduler remains the consumer; P2 only guarantees corpus + lint.

---

## 5. Quality plan

### 5.1 Runs in CI vs Colab-verified

- **Browser chapters (M4 ≈ 20, M5 Ch1–10, M6 Ch1–3/8/10/13/14 ≈ 37 total):** generated CPython
  twins execute in CI (R10, blocking) — unchanged P1 machinery; every one also passes the R3
  Pyodide-import lint and the e2e smoke path (D0017).
- **Colab chapters (~15):** **CPU-scaled companion-notebook
  execution in CI (blocking, P2-D9)** with exact-pinned CPU torch; **plus one recorded manual
  Colab run per chapter** (D0012: link/summary in the PR — GPU runtime, torch version, wall
  time, final metrics) before merge. Threshold calibration runs (≥3) recorded for each
  auto-graded training exercise (P2-D7).
- **Phase-close sweep (mirrors P1 Task 66):** every colab chapter's button clicked from the
  rendered preview and the notebook run end-to-end on a *free* Colab account (quota-realistic),
  results tabled in this spec at close; every browser chapter spot-run on Pyodide via the
  standing e2e smoke + a sampled manual sweep.

### 5.2 Lint / link / spell gates (all inherited, blocking)

Vale + banned-word list, markdownlint-cli2, codespell (extend allow-list: ML vocabulary — e.g.
"perceptron", "softmax", "cuDNN"), lychee (source) + lychee-site (rendered, D0017), render job +
e2e smoke + axe/mobile checks (D0017), `frontmatter_lint`, `chapter_structure_lint` (badge
drift), `quiz_lint`, `review_cards_lint`, `a11y_check` (every loss curve/decision boundary/
architecture diagram needs takeaway-bearing alt text).

### 5.3 R-gates + new P2 checks

- **R3 browser-import lint** — still load-bearing for the ~37 browser chapters (`torch` must
  fail there; `KNOWN_UNSAFE` covers it). **Change (P2-D6):** move `xgboost`/`lightgbm` out of
  `KNOWN_UNSAFE` into the built-in allow-list — they are Pyodide 0.28.1 built-ins (verified
  2026-07-19); tests updated. Colab chapters' companion notebooks stay **excluded** from the
  browser allow-list path (they're a different tier).
- **New — colab-policy check (`infra/ci/colab_check.py`):** every `compute: colab` chapter must
  have (a) a `{{< colab >}}` button resolving to an existing companion notebook, (b) a
  generated-companion drift check pass (P2-D8), (c) a parameters cell honouring `LARNIX_CI`
  (P2-D9), (d) a torch version-floor guard cell (P2-D11). Fails closed.
- **R11 assets ledger** — new entries: California-Housing sample (+ sampling script committed),
  Bank Marketing, Fashion-MNIST, MNIST, pets subset, SSA names, GloVe subset, **pretrained
  weights** (ResNet weights licence recorded — first time *model* assets enter the ledger).
  `assets_check.py` extended to cover `data/` in the three new modules.
- **R6 free-fallback** — green by construction (no keys anywhere in P2); gate still runs.
- **R1 currency** — no frontier chapters; mechanism runs (floors re-checked quarterly anyway via
  the P2-D11 guard).

### 5.4 Correctness-review checklist (per-chapter PR gate; P1 §5.5 plus P2 additions)

All P1 items, plus:

- [ ] Stochasticity handled honestly: seeded where claimed; any "your numbers will differ" cases
      say so in prose; no assert that can flake on a compliant learner run.
- [ ] Colab chapters: recorded manual run linked in the PR (GPU type, torch version, wall time,
      metrics); thresholds calibrated with margin (≥3 runs); CPU-scaled twin executes in CI.
- [ ] No leakage in any worked example (fit on train only; transforms inside pipelines/CV) —
      the M4 cardinal-sin rule applied to our own code.
- [ ] Math verified: every hand-derived gradient (M5 Ch6/8/9, M6 Ch10–11) checked numerically in
      the twin; every metric formula cross-checked against sklearn on the same inputs.
- [ ] Device-agnostic pattern (`device = "cuda" if available else "cpu"`) in every torch chapter;
      no silent CPU-only or GPU-only code.
- [ ] GPU cost/quota honesty: each colab chapter states expected free-tier runtime; nothing in
      the required path exceeds a free session.

### 5.5 Phase-specific risks

- **R3 (compute limits):** first phase with real pressure — mitigated by the per-chapter compute
  table (§2) decided *now*, the fail-closed lint, and the reshape-don't-promote rule.
- **R4 (grading reliability):** property thresholds are the new surface — mitigated by
  calibration-with-margin + rubric layering (P2-D7).
- **R12 (drop-off):** the Colab handoff is the school's steepest cliff — mitigated by the
  dedicated handoff chapter (P2-D4), ten browser chapters of M5 momentum first, and the digits→
  MNIST continuity ("same problem, bigger data").
- **R13 (free tiers change):** Colab default + Kaggle documented alternate (P2-D10); torch floor
  policy (P2-D11); provider specifics concentrated in M5 Ch11 (one swappable chapter).
- **R9 (maintenance):** single-sourced companions (P2-D8), one running thread per module, stable
  status everywhere.

---

## 6. Task breakdown (ordered, independently committable)

One task ≈ one commit/PR. §6.A lands before any content ("evals before features", as P1 did).
Every non-trivial chapter gets a one-paragraph plan approved before authoring (CLAUDE.md).

### 6.A — Shared tooling first

1. **Stochastic grader extensions (P2-D7)** — `assert_between`/`assert_decreased`/gradient-check
   helpers in `lib/grader.py`; seeded-mode conventions documented in `lib/README.md`; CPython
   unit tests.
2. **Colab companion generator (P2-D8)** — extend `make_twin.py`/add `make_colab.py`: tagged
   cells → companion `.ipynb` (header, setup, grader-bootstrap with inlined fallback, exercises +
   hidden solutions); `--check` drift gate; unit tests.
3. **CPU-scaled CI tier (P2-D9)** — `LARNIX_CI` parameters convention; exact-pinned CPU
   torch/torchvision in `requirements-notebooks.txt`; `run_notebooks.py` executes companions
   within budget; CI workflow wiring + cache.
4. **Colab-policy gate (§5.3)** — `infra/ci/colab_check.py` (button ↔ notebook ↔ params ↔ guard
   cell) + tests; RUNBOOK "recorded Colab run" template updated (metrics/threshold-calibration
   fields).
5. **Datasets + ledger (P2-D2, R11)** — vendor California-Housing sample (+ committed sampling
   script) and GloVe subset; ledger entries for all §5.3 assets incl. pretrained weights;
   `assets_check.py` coverage for M4–M6.
6. **Module scaffolding** — `modules/04-classical-ml/`, `05-deep-learning/`,
   `06-vision-sequences/` skeletons (README, `index.qmd` landing, capstone template); nav
   placeholders hidden until live.

### 6.B — M4 Classical ML (20 chapters + assessment)

7–26. One task per chapter (M4 Ch1…Ch20 in §2 order; Ch12 includes the R3 allow-list change for
xgboost/lightgbm — P2-D6). Each: `.qmd` + twin + exercises + quick-check + SR cards.
27. M4 — module quiz (transfer questions).
28. M4 — capstone (Bank Marketing + model card) + rubric + leakage/AUC auto-checks +
walkthrough; README/landing finalize.

### 6.C — M5 Deep Learning Foundations (18 chapters + assessment)

29–38. M5 Ch1–10 (browser half; micrograd arc). *(Apply P2-D5 merge only if a chapter is thin.)*
39. **M5 Ch11 — the handoff chapter** (Colab + Kaggle-alternate walkthrough; first learner-facing
colab chapter; extra care per R12).
40–46. M5 Ch12–18 (colab half; each with companion, CPU-scaled twin, recorded Colab run).
47. M5 — module quiz.
48. M5 — capstone (scratch digits → PyTorch MNIST) + rubric + both auto-checks + walkthrough;
README/landing finalize.

### 6.D — M6 Vision & Sequences (14 chapters + assessment)

49–62. One task per chapter (M6 Ch1…Ch14; browser/colab per §2 table).
63. M6 — module quiz.
64. M6 — capstone (transfer-learning app + name generator) + rubric + property checks +
walkthrough; README/landing finalize.

### 6.E — Phase integration + DoD

65. Nav/landing update: M4–M6 live in `_quarto.yml` sidebar + `index.qmd` catalog; cross-module
prereq links verified on the rendered preview.
66. Full fresh-clone build + green CI across all ~52 chapters (twins + CPU-scaled companions);
cross-chapter link/lint sweep.
67. **Free-tier confirmation sweep:** all browser chapters via e2e/Pyodide; **every colab chapter
run end-to-end on a free Colab account** from the rendered button; results tabled here.
68. Docs: `D0019+` logged; `PORTFOLIO.md` quantified P2 bullet; `RUNBOOK.md` GPU-verification
additions; `WALKTHROUGH.md` extended ("EDA graduate → trains a CNN on a free GPU").

---

## 7. Definition of Done (P2)

Instantiates `ROADMAP §3 P2` exit criteria against the `CLAUDE.md` generic DoD:

- [ ] **M4–M6 complete (~52 chapters); every chapter passes the Varsity contract** with complete
      10-field front-matter + `review_cards`; all D0017 content conventions hold (genuine Ex2,
      transfer module-quizzes, correct next-chapter handoffs, no untaught syntax).
- [ ] **Classical ML stays in-browser:** all 20 M4 chapters `compute: browser` and running on
      Pyodide (₹0) — incl. XGBoost via the Pyodide built-in (P2-D6); no Colab surface in M4.
- [ ] **Every `colab` chapter has a working "Open in Colab" button** (rendered-preview-clicked),
      a generated, drift-checked companion notebook, **and a recorded manual Colab run** in its
      PR (D0012); the Kaggle alternate is documented in M5 Ch11.
- [ ] **Auto-graders handle stochastic training:** seeded/tolerance asserts on browser chapters,
      calibrated property asserts on colab chapters (P2-D7); no flaking assert on a compliant
      run; exercises state which mode grades them.
- [ ] **CI green across the phase:** browser twins + CPU-scaled companion notebooks execute
      (R10); render + rendered-link + e2e + axe/mobile jobs pass; Vale/markdownlint/codespell/
      lychee clean; R1/R3/R6 + colab-policy + assets gates green.
- [ ] **Free-tier path confirmed end-to-end:** the §6.E sweep shows every chapter completable at
      ₹0 on browser or free Colab/Kaggle within a free session's limits; every stated runtime
      honest.
- [ ] **Each module has a quiz + a rubric'd capstone**; every capstone reports a measured number;
      M4's includes a model card; auto-check + rubric split follows R4.
- [ ] **All new datasets and pretrained weights ledgered** in `docs/ASSETS.md` with licences
      (R11); no un-ledgered `data/` file or weights reference.
- [ ] **Builds cleanly from a fresh clone**; preview deploy renders M4–M6 with working
      nav/search/progress; **every learner-facing link on the rendered preview
      clicked/verified** (D0017).
- [ ] **A "5-minute learner walkthrough"** through the new content (EDA graduate → first CV score
      → first GPU epoch) recorded in `WALKTHROUGH.md`.
- [ ] **`DECISIONS.md` updated** (D0019+ incl. any merges used); **`PORTFOLIO.md`** carries a
      quantified P2 bullet (e.g. "authored ~52 auto-graded chapters incl. a stochastic-training
      grader and a browser→free-GPU pipeline; ~70% of the phase still runs at ₹0 in-browser").

---

## 8. Open questions — researched 2026-07-19; status per question

> A web/codebase research pass (see §9 validation log) answered everything answerable without
> you. **Resolved-by-research** items now carry evidence and need only a nod with the spec;
> **needs your call** items are genuine preference/taste decisions research cannot settle.

### Resolved by research (approve with the spec)

- **Q-4 — XGBoost (→ P2-D6). RESOLVED — and the draft recommendation was overturned.**
  `xgboost 2.1.4` + `lightgbm 4.6.0` are **built-in packages of Pyodide 0.28.1**, the exact
  version our vendored quarto-live pins (`live.lua:531`). Ch12 therefore teaches real XGBoost
  **in the browser**; no Colab companion; M4 goes 100% browser. Our R3 lint's `KNOWN_UNSAFE`
  entry for xgboost/lightgbm is stale and will be corrected (§5.3). *Caveat noted in P2-D6:*
  the wheel downloads from the Pyodide CDN on first use (a "needs internet for this cell" note,
  same honesty rule as P1's Seaborn).
- **Q-2 (licences half) — Dataset bundle legality (→ P2-D2). RESOLVED.** Every proposed asset
  verified licence-clean (§9): California Housing = 1990 US Census derivative, public domain
  (sklearn's own docs); Bank Marketing = **CC BY 4.0** (UCI); Adult/Census Income = CC BY 4.0
  (UCI, if chosen); Fashion-MNIST = **MIT**; MNIST = **CC BY-SA 3.0** (LeCun/Cortes — share-alike
  is fine since we vendor nothing, torchvision downloads it; ledger records the licence);
  Oxford-IIIT Pets = **CC BY-SA 4.0**; SSA baby names = US-gov public domain (data.gov); GloVe
  pretrained vectors = **PDDL (Open Data Commons)** per Stanford NLP. All go into `ASSETS.md`.
- **Q-6 — Missing-topic check. RESOLVED (codebase audit).** PLAN's M4 (20), M5 (17 listed → 18
  via the micrograd split absorbing the GPU chapter into the handoff), M6 (14) item lists were
  diffed against §2 line-by-line: **every PLAN topic is covered; nothing dropped.** Deltas are
  reorders only: M4 eval-early (Q-1), M5 "GPUs & why they matter" → the Ch11 handoff, M6
  vanishing-gradients moved *before* LSTM (it motivates the gates; PLAN listed it after). Model
  cards (no PLAN chapter) live in M4 Ch20 + capstone. All deltas logged with the decisions.
- **Q-3 (feasibility half) — CPU-scaled CI (→ P2-D9). FEASIBLE, cost verified.** CPU-only torch
  wheels from the official `download.pytorch.org/whl/cpu` index are ~200 MB-class (vs ~800 MB+
  CUDA default) and cacheable in Actions; free-Colab facts for the runbook confirmed (T4,
  ~12 GB VRAM, ≤12 h best-case sessions, availability-dependent — Google FAQ). Remaining
  approval is the wall-clock trade only (below).

### Needs your call (the genuinely yours-to-make residue)

- **Q-1 — Eval-early reorder (→ P2-D1).** Pedagogical taste. Research adds precedent: Kaggle's
  own Intro-to-ML teaches model validation + under/overfitting immediately after the first
  model, before more models — matching option A. PLAN's order matches older textbook
  sequencing. **My recommendation stands: A (eval-early).** Confirm or hold PLAN's order.
- **Q-2 (choice half) — Capstone dataset + M6 image domain.** (a) **Bank Marketing** (rec.: a
  clean business problem, natively imbalanced) vs **Adult income** (richer fairness/model-card
  discussion, heavier framing for a first solo capstone) — both CC BY 4.0, both viable.
  (b) M6 transfer-learning images: default = a small **Oxford-IIIT Pets subset** (cats vs dogs,
  CC BY-SA 4.0) unless you want a domain you'd rather showcase in the portfolio.
- **Q-3 (trade half) — Approve ~5–8 min extra CI wall-clock** + a cached ~200 MB CPU-torch
  dependency to keep "everything runs" automated for colab chapters? (Rec.: yes — it guards a
  third of the phase against silent drift.)
- **Q-5 — M5 shape (→ P2-D3/D4/D5).** Micrograd across two chapters; the dedicated Ch11 handoff
  chapter; ≤3-merge allowance; counts 20/18/14. Pure pedagogy-shape preference — confirm or
  adjust.
- **Q-7 — Threshold calibration burden (→ P2-D7).** ≥3 recorded Colab runs per auto-graded
  training exercise (rec.) vs 2 runs + wider margins. Authoring-cost tolerance is yours.

*All five confirmed at the recommended option (2026-07-19) and logged with the resolved items in
`DECISIONS.md` D0019–D0020. §6.A Task 1 is the next unit of work.*

---

## 9. Validation log (web + codebase research, 2026-07-19)

Load-bearing claims checked before decisions are finalized. **One draft recommendation was
overturned (P2-D6); no other claim failed.**

| Claim | Verdict | Evidence |
|---|---|---|
| `xgboost` cannot run in a `browser` chapter (P2-D6 draft premise) | ❌ **Overturned** | pyodide.org **0.28.1** built-in package list: `xgboost 2.1.4`, `lightgbm 4.6.0`. Our vendored quarto-live pins exactly `cdn.jsdelivr.net/pyodide/v0.28.1/full/` (`_extensions/r-wasm/live/live.lua:531`). Current Pyodide (314.0.2) also ships both. |
| Our R3 lint treats xgboost/lightgbm as un-runnable | ✅ Confirmed stale | `infra/ci/browser_import_lint.py:50` lists both in `KNOWN_UNSAFE` — must move to the allow-list (§5.3, M4 Ch12 task). |
| torch/torchvision are **not** Pyodide packages (M5+ colab split stands) | ✅ Confirmed | Neither appears in the 0.28.1 or 314.0.2 built-in lists; `KNOWN_UNSAFE` torch entry stays. |
| California Housing is public-domain-safe to sample + vendor | ✅ Confirmed | Derived from the 1990 U.S. Census (public domain); dataset shipped/fetched by scikit-learn itself (BSD-licensed loader, `fetch_california_housing` docs + sklearn descr file). |
| Bank Marketing licence | ✅ CC BY 4.0 | UCI dataset page (ID 222) states CC BY 4.0; citation: Moro, Laureano & Cortez (2011). |
| Adult / Census Income licence (Q-2 alternative) | ✅ CC BY 4.0 | UCI dataset page states CC BY 4.0. |
| Fashion-MNIST licence | ✅ MIT | `zalandoresearch/fashion-mnist` LICENSE file (MIT). |
| MNIST licence | ✅ CC BY-SA 3.0 | LeCun & Cortes hold copyright; "made available under CC BY-SA 3.0" (Keras docs + mirrors). We vendor nothing — torchvision downloads at runtime; ledger records licence + attribution. |
| Oxford-IIIT Pets licence | ✅ CC BY-SA 4.0 | HF `timm/oxford-iiit-pet` dataset card (`license: cc-by-sa-4.0`); VGG Oxford source page. |
| SSA baby names is public-domain US-gov data | ✅ Confirmed | data.gov catalog entry for `ssa.gov/oact/babynames/names.zip` (federal dataset). |
| GloVe pretrained vectors licence | ✅ PDDL | stanfordnlp/GloVe README: "Pre-trained word vectors are made available under the Public Domain Dedication and License." |
| CPU-only torch is a slim, pinnable CI dependency | ✅ Confirmed | Official `download.pytorch.org/whl/cpu` index exists; CPU wheels are ~200 MB-class vs ~800 MB+ CUDA (community + packaging guides); cacheable in Actions. |
| Free-Colab session facts for M5 Ch11 honesty | ✅ Confirmed | Google Colab FAQ: free notebooks run "at most 12 hours" availability-dependent; free tier = T4 (~12 GB VRAM justification for small-model scoping). Exact preinstalled-torch version floats — which is precisely why P2-D11 uses a version-floor guard, verified per refresh, not a pin. |
| Eval-early has pedagogy precedent (P2-D1) | ✅ Supportive | Kaggle Learn *Intro to ML* lesson order: first model → **model validation** → **under/overfitting** → random forests → competitions. |

*Sources fetched 2026-07-19: pyodide.org (0.28.1 + 314.0.2 package lists), scikit-learn docs +
repo descr, archive.ics.uci.edu (Bank Marketing, Census Income), github.com/zalandoresearch/
fashion-mnist, keras.io/api/datasets/mnist, huggingface.co/datasets/timm/oxford-iiit-pet +
robots.ox.ac.uk/~vgg/data/pets, catalog.data.gov (SSA names), github.com/stanfordnlp/GloVe,
download.pytorch.org/whl/cpu, research.google.com/colaboratory/faq, kaggle.com/learn.*
