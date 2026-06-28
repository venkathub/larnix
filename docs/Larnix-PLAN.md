# Larnix — PLAN: Building a Zerodha Varsity-Style Learning Platform for AI/ML

## TL;DR
- A free, open-access, **newbie-to-frontier** AI school modeled on Zerodha Varsity's pedagogy (plain language, analogies, short sequenced chapters, Key Takeaways, end-of-module quizzes + certification), now expanded to **17 modules** so coverage runs all the way from "what is AI" to **reinforcement learning + reasoning models** and **building your own custom LLM end-to-end** (data → tokenizer → pretraining → distributed training → post-training → quantize → serve).
- Two new outcome-defining tracks were added per your asks: a **"Build Your Own LLM" module** (so a graduate can actually train and serve a custom model, not just call an API or fine-tune), and a **Career & Job-Readiness module** (portfolio, ML/LLM system-design interviews, role map) so a finisher is genuinely hireable as an ML/AI/LLM engineer.
- A full **Prerequisites & Infrastructure section** now specifies exactly what accounts, API keys, and compute each module needs — **free-tier-first** (browser + Colab/Kaggle + Ollama on a laptop costs ₹0), escalating to API keys (OpenAI/Anthropic/Gemini, or free local Ollama) and rented cloud GPUs (RunPod/Lambda/Modal) only when a module genuinely requires them.
- Same build approach as before: **docs-as-code** (Git + Jupyter/Markdown + Quarto + CI), runnable code in every chapter (JupyterLite in-browser for beginners, Colab for GPU work), shipped to Claude Code phase by phase.

---

## What changed in this revision (your three asks)
1. **"Ensure all topics covered, foundation → advanced → till now."** Added/expanded: **Reinforcement Learning & Reasoning Models** (RLHF/DPO/GRPO, test-time compute, o1/R1-style reasoning), a dedicated **Build-Your-Own-LLM / distributed-training** module, **Model Context Protocol (MCP) and multi-agent systems** in the AI-engineering module, and an **Applied ML electives** module (time series, recommenders, speech). The map below is now genuinely end-to-end.
2. **"What prerequisites are needed (OpenAI key, Ollama/vLLM, cloud)."** New **Section B0 — Prerequisites & Infrastructure**: a module-by-module table of required accounts, keys, local tools, and cloud GPUs, with a free alternative for every paid item and cost-guardrail guidance.
3. **"Graduate should land AI jobs and build custom LLMs."** New **Module 16 — Career & Job-Readiness** and a new **Outcomes & Job-Readiness** section mapping the curriculum to concrete roles, portfolio expectations, and interview prep; the custom-LLM capability is now an explicit capstone.

---

## Key Findings — what makes Varsity work, and how to port it to AI

Zerodha Varsity describes itself as "an extensive and in-depth collection of stock market and financial lessons… one of the largest financial education resources on the web. No signup, no pay-wall, no ads." That free, frictionless, editorially-driven model is the thing to copy. Its effectiveness comes from a few repeatable choices we lift directly:

1. **Module → chapter hierarchy with steady progression** (Varsity has 12 modules; its intro module is 15 chapters, Technical Analysis 22, Options 25), ordered foundations-first.
2. **Short, single-topic chapters in plain language**, each opening by assuming the reader "knows nothing," in a conversational first-person tone.
3. **Real-world analogies and running narratives** (IPOs via a t-shirt entrepreneur; time-value-of-money via a friend borrowing money).
4. **"Key Takeaways" at the end of every chapter** — a numbered 3–6 point recap.
5. **Visual aids and downloadables** embedded in the flow.
6. **Three difficulty tiers + end-of-module quizzes → certification.** Varsity Certified is "100 multiple-choice online questions in 100 minutes… minimum of 65%" for a nominal fee.
7. **Free + multi-format** (exhaustive text primary, video as aid, bite-size mobile app).

**The crucial adaptation for AI:** finance is read-and-understand; AI is *do*. Karpathy's "Zero to Hero," fast.ai, and Hugging Face all converge on the same lesson — **you learn AI by writing and running code.** So every Varsity principle is kept, but each chapter gains a runnable notebook, and each module gains graded exercises and a build-something project.

**Sequencing philosophy (blended):** fast.ai's **top-down** "show a working model first, then dig down" (grounded in David Perkins' *Making Learning Whole*, 2009 — teach the "whole game") + Karpathy's **bottom-up** "build from first principles" (micrograd → makemore → GPT). We use **"taste then theory"**: each major section opens with a working demo, then builds foundations bottom-up.

---

## PART A — THE FULL AI CURRICULUM (newbie → frontier → custom LLM)

**The "Varsity contract" applied to every chapter:** ~1,500–3,000 words OR a 15–25 min notebook · one concept each · analogy/demo → plain explanation → worked example → **Key Takeaways** → 2–4 exercises · difficulty badge 🟢 Beginner / 🟡 Intermediate / 🔴 Advanced · every module has objectives, prereqs, a quiz, and a capstone.

Sources blended: fast.ai *Practical Deep Learning*, Andrew Ng's ML & Deep Learning Specializations (DeepLearning.AI/Stanford), Stanford CS229/CS231n/CS224n, Karpathy "Neural Networks: Zero to Hero," Hugging Face LLM/Agents courses, Chip Huyen *AI Engineering* (O'Reilly 2025), Sebastian Raschka *Build a Large Language Model (From Scratch)* (Manning), and the OWASP Top 10 for LLM Applications (2025).

### Module map (the spine) — now end-to-end

| # | Module | Difficulty | Prereqs | ~Ch | Capstone |
|---|--------|-----------|---------|-----|----------|
| 0 | How to Use This School / What is AI? | 🟢 | none | 6 | Run your first pretrained model |
| 1 | Python for AI | 🟢 | none | 14 | Data-cleaning CLI/notebook |
| 2 | Math You Actually Need (intuition-first) | 🟢→🟡 | M1 | 16 | "Math of one neuron" notebook |
| 3 | Data & Tooling (NumPy/Pandas/viz/envs) | 🟢→🟡 | M1 | 14 | EDA on a real dataset |
| 4 | Classical Machine Learning | 🟡 | M2,M3 | 20 | End-to-end tabular predictor |
| 5 | Deep Learning Foundations | 🟡 | M4 | 18 | Neural net from scratch → PyTorch |
| 6 | Specialized DL: Vision & Sequences | 🟡→🔴 | M5 | 14 | Image classifier + sequence model |
| 7 | NLP & the Transformer | 🔴 | M5,M6 | 14 | Build a small GPT from scratch |
| 8 | Large Language Models (adapt + evaluate) | 🔴 | M7 | 16 | Fine-tune + eval a small LLM |
| 9 | **Reinforcement Learning & Reasoning Models** ✨ | 🔴 | M5,M8 | 14 | Post-train a model to reason better |
| 10 | Generative AI (diffusion, multimodal, audio) | 🔴 | M7 | 12 | Text-to-image + multimodal app |
| 11 | **Build Your Own LLM End-to-End** ✨ | 🔴 | M7,M8,M9 | 18 | **Train + serve a custom LLM** |
| 12 | AI Engineering: RAG, Agents & MCP | 🟡→🔴 | M8 | 20 | Production RAG + agent assistant |
| 13 | Production AI: MLOps & LLMOps | 🔴 | M12 | 16 | Deploy + monitor + cost-optimize |
| 14 | Responsible AI: Safety, Security, Ethics | 🟡→🔴 | M8,M12 | 12 | Red-team & harden your app |
| 15 | **Applied ML Electives** ✨ (optional) | 🟡→🔴 | M4,M6 | 12 | Pick one: forecast / recommend / speech |
| 16 | **Career & Job-Readiness** ✨ | 🟢→🔴 | any | 12 | Portfolio + mock interview loop |

✨ = new in this revision. Modules 0–3 are gentle and analogy-heavy for non-technical/junior learners; Modules 7–14 carry the senior-engineer "prototype-to-production" rigor.

---

### Module 0 — How to Use This School / What is AI? 🟢
**Objectives:** demystify AI/ML/DL/GenAI; get every learner running code on day one.
**Chapters:** What is AI, really? · AI vs ML vs DL vs GenAI (a family tree) · 10-minute history (perceptron → deep learning → transformers → foundation models → reasoning models) · How this school works · Your toolkit (notebooks, Colab, in-browser sandbox) · Run your first model (5 lines).
**Hands-on:** Hugging Face `pipeline()` for sentiment + image classification with zero theory.

### Module 1 — Python for AI 🟢
**Objectives:** enough Python for data and ML; clarity over cleverness.
**Chapters:** types · control flow · functions · data structures · comprehensions · files (CSV/JSON) · errors & debugging · venvs & pip · just-enough OOP · NumPy preview · clean readable code · IDE/Colab · reading tracebacks · Pythonic data idioms.
**Hands-on:** auto-graded mini-exercises; capstone data-cleaning script. *Includes "Python for Java developers" side-notes (dynamic typing, indentation-as-syntax, duck typing) for the creator's own onboarding.*

### Module 2 — Math You Actually Need 🟢→🟡
**Objectives:** intuition-first linear algebra, calculus, probability/statistics (picture before symbols).
**Chapters:** why math for AI · vectors & geometry · matrices as transformations · matmul intuition · dot products & similarity · derivatives = sensitivity · gradients (downhill picture) · the chain rule (engine of backprop) · probability basics · distributions · mean/variance/std · Bayes intuition · correlation vs causation · sampling & uncertainty · linear algebra in NumPy · the math of one neuron.
**Hands-on:** visualize gradient descent; code dot-product similarity; capstone neuron forward+backward pass.

### Module 3 — Data & Tooling 🟢→🟡
**Objectives:** load, clean, explore, visualize; reproducible environments.
**Chapters:** NumPy & vectorization · Pandas Series/DataFrame · indexing · cleaning (missing/types/dupes) · joins & groupby · reshaping · Matplotlib · Seaborn · the EDA workflow · scaling/encoding preview · notebooks vs scripts · environments & reproducibility · data ethics preview · messy real-world data.
**Hands-on:** full EDA on a public dataset. Mantra: "manual inspection of data has the highest value-to-prestige ratio in ML."

### Module 4 — Classical Machine Learning 🟡
**Objectives:** the CS229/Ng core — supervised & unsupervised learning, evaluation, bias-variance.
**Chapters:** what is learning? · linear regression · cost functions & gradient descent · logistic regression · KNN · decision trees · random forests & ensembles · gradient boosting (XGBoost) · SVMs · naive Bayes · k-means · hierarchical clustering · PCA & dimensionality reduction · feature engineering · train/val/test & cross-validation · overfitting & regularization · bias-variance · metrics (precision/recall/F1/ROC-AUC) · imbalanced data · the scikit-learn workflow.
**Hands-on:** build each algorithm in scikit-learn + "from scratch" exercises. **Capstone:** end-to-end tabular prediction, Kaggle-style.

### Module 5 — Deep Learning Foundations 🟡
**Objectives:** understand neural nets by building one from scratch (micrograd style), then PyTorch.
**Chapters:** from logistic regression to a neuron · activations · layers & networks · forward pass · loss functions · backprop spelled out · GD variants (SGD/momentum/Adam) · build micrograd · build an MLP from scratch · enter PyTorch (tensors/autograd) · `nn.Module` & training loops · dropout/batchnorm · initialization & LR tuning · diagnosing training · GPUs & why they matter · saving/loading · a reproducible training harness.
**Hands-on:** implement backprop by hand. **Capstone:** digit classifier from scratch, then re-implemented in PyTorch.

### Module 6 — Specialized DL: Vision & Sequences 🟡→🔴
**Objectives:** CNNs, RNN/LSTM, embeddings as the bridge to NLP.
**Chapters:** images as tensors · convolution intuition · pooling/padding/strides · CNN from scratch · LeNet→ResNet · transfer learning & fine-tuning vision models · data augmentation · sequences & memory · RNNs · LSTM/GRU · vanishing gradients · word embeddings (word2vec) · embeddings for search/similarity · limits of RNNs (motivating attention).
**Hands-on:** fine-tune a pretrained ResNet; train an LSTM generator. **Capstone:** image-classifier app + char-level sequence model.

### Module 7 — NLP & the Transformer 🔴
**Objectives:** master attention and the transformer; build a small GPT.
**Chapters:** the NLP task zoo · tokenization & BPE (build a tokenizer) · attention intuitively · self-attention math · multi-head attention · positional encodings · the full transformer block · encoder/decoder/encoder-decoder · build a small GPT (nanoGPT style) · training dynamics · Hugging Face Transformers · pretraining vs fine-tuning.
**Hands-on:** implement self-attention. **Capstone:** "Let's build GPT" — a working char-level transformer.

### Module 8 — Large Language Models 🔴
**Objectives:** how LLMs are built, adapted, and evaluated. Anchored on Huyen *AI Engineering* Ch. 2–3.
**Chapters:** language models → foundation models · pre-training & next-token prediction · the data behind LLMs · scaling laws & emergent abilities · sampling/decoding (temperature, top-k/p) · structured outputs · SFT · preference tuning & RLHF/DPO (intro) · PEFT (LoRA/QLoRA) · quantization & memory math · why eval is hard · eval metrics (perplexity, functional correctness) · AI-as-a-judge · benchmarks & leaderboards · hallucination & its causes · open vs proprietary (build-vs-buy).
**Hands-on:** fine-tune a small model with LoRA; build an eval harness. **Capstone:** fine-tune + rigorously evaluate a small LLM.

### Module 9 — Reinforcement Learning & Reasoning Models 🔴 ✨
**Objectives:** RL from fundamentals through the techniques behind modern reasoning models (o1/o3, DeepSeek-R1) — the "till now" frontier.
**Chapters:** what is RL (agent/environment/reward) · Markov Decision Processes intuition · value vs policy methods · Q-learning · policy gradients · PPO intuition · reward models · RLHF, deeply (the alignment pipeline) · DPO & preference optimization · RLAIF & Constitutional AI · GRPO and reasoning-model training · test-time compute & chain-of-thought · self-consistency & verifiers · distillation of reasoning · RL for agents (motivating Module 12).
**Hands-on:** implement a policy-gradient agent on a toy environment; train a tiny reward model; run a small preference-optimization (DPO) loop. **Capstone:** post-train a small model so it reasons/behaves measurably better, with before/after evals.

### Module 10 — Generative AI: Diffusion, Multimodal, Audio 🔴
**Objectives:** generative models beyond text.
**Chapters:** the generative landscape (GAN→VAE→diffusion) · diffusion intuition (add noise, learn to reverse) — diffusion models work by destroying training data through the successive addition of Gaussian noise, then learning to recover it by reversing that noising process · the forward/reverse process · DDPM essentials · latent diffusion & Stable Diffusion · text-to-image conditioning (CLIP/text encoders) · sampling & guidance · image fine-tuning (LoRA, DreamBooth, textual inversion) · multimodal (vision-language) models · audio & speech generation · video generation overview · ethics of synthetic media & deepfakes.
**Hands-on:** run and steer a Diffusers pipeline. **Capstone:** text-to-image mini-app + a multimodal "describe this image" feature.

### Module 11 — Build Your Own LLM End-to-End 🔴 ✨ (the "custom LLM" you asked for)
**Objectives:** take a model from **raw data to a trained, aligned, served custom LLM** — the full pipeline at small-but-real scale (Raschka's *Build an LLM From Scratch* + Karpathy nanoGPT/llm.c). This module is what makes a graduate able to *develop custom LLMs*, not just consume them.
**Chapters:** the LLM build pipeline (the whole map) · sourcing & licensing training data · large-scale cleaning, dedup & quality filtering · training a tokenizer (BPE) at scale · dataset packing & sharding · architecture choices (params, context length, attention variants, RoPE) · the pretraining loop at scale · **distributed training: data / tensor / pipeline parallelism** · **FSDP, DeepSpeed & ZeRO, mixed precision** · scaling laws & compute budgeting · checkpointing & resuming · continued pretraining & domain adaptation · **post-training (SFT + preference tuning) to make it useful** · evaluating your custom model · **quantizing & exporting (GGUF)** · **serving with vLLM and Ollama** · the hardware/cost reality (rent vs own GPUs).
**Hands-on:** pretrain a small (~100M–1B param) model from scratch on a curated corpus using rented cloud GPUs; run a multi-GPU job. **Capstone:** **a custom, domain-specialized LLM** — data → tokenizer → pretrain → fine-tune → evaluate → quantize → serve locally via Ollama and over an API with vLLM. *This is the headline "you can build an LLM" deliverable.*

### Module 12 — AI Engineering: RAG, Agents & MCP 🟡→🔴
**Objectives:** build real applications on foundation models — the highest-demand skillset. Anchored on Huyen Ch. 5–6 + Hugging Face Agents course.
**Chapters:** the AI engineering stack (vs ML engineering) · prompting fundamentals (zero/few-shot, system vs user) · prompt-engineering best practices · prompts under version control · embeddings in practice · vector databases (Pinecone/Weaviate/Milvus/Qdrant/Chroma/pgvector) · chunking strategies · RAG architecture (retriever + generator) · hybrid search & reranking · advanced RAG (GraphRAG, agentic RAG, HyDE, self-RAG) · evaluating RAG · tool use & function calling · structured outputs · **Model Context Protocol (MCP) & tool/connector standards** ✨ · agents & planning · **multi-agent systems & orchestration** ✨ · agent failure modes & memory · frameworks (LangChain, LlamaIndex, LangGraph, smolagents) · "RAG is for facts, fine-tuning is for form."
**Hands-on:** build a RAG pipeline over your own docs; add function-calling tools; wire up an MCP server/client. **Capstone:** a production-style RAG + agent assistant with retrieval, tools, MCP, and evaluation.

### Module 13 — Production AI: MLOps & LLMOps 🔴
**Objectives:** prototype → reliable production (your signature theme). Anchored on Huyen Ch. 9–10 + DeepLearning.AI MLOps.
**Chapters:** the ML/AI lifecycle · experiment tracking (MLflow/W&B) · data & model versioning (DVC) · reproducible pipelines · serving (FastAPI, Triton, BentoML, vLLM) · batch vs real-time inference · inference optimization (KV cache, batching, quantization) · cost & latency optimization · semantic caching · model routing & gateways · CI/CD for ML · monitoring & observability · data & concept drift · online eval & feedback · guardrails & fallback patterns · scaling & infra · the AI engineering architecture (context → guardrails → router → cache → agents → monitoring).
**Hands-on:** containerize & deploy the Module 12 app; add monitoring + drift detection. **Capstone:** a deployed, monitored, cost-instrumented AI service with CI/CD.

### Module 14 — Responsible AI: Safety, Security, Ethics 🟡→🔴
**Objectives:** ethics, bias, alignment, security as engineering practice.
**Chapters:** why responsible AI matters · sources of bias & fairness · dataset documentation & transparency · privacy & data protection · the **OWASP Top 10 for LLM Applications (2025)** · prompt injection (direct & indirect — the #1 OWASP LLM risk) · jailbreaking · sensitive-info disclosure & system-prompt leakage · insecure output handling & excessive agency · guardrails & I/O filtering · red-teaming & adversarial testing · alignment & RLHF revisited · governance, regulation & the road ahead.
**Hands-on:** craft and defend against prompt-injection attacks. **Capstone:** red-team and harden your Module 12/13 app against the OWASP LLM Top 10.

### Module 15 — Applied ML Electives 🟡→🔴 ✨ (optional breadth, pick what your target job needs)
**Objectives:** job-relevant breadth beyond LLMs.
**Chapters (modular, pick-and-choose):** time-series forecasting (classical + deep) · recommender systems · speech: ASR & TTS (Whisper, etc.) · tabular deep learning · anomaly detection · graph neural networks (intro).
**Hands-on / Capstone:** ship one elective end-to-end (e.g., a demand forecaster, a recommender, or a voice-to-text app).

### Module 16 — Career & Job-Readiness 🟢→🔴 ✨ (so you actually get hired)
**Objectives:** convert skills into offers; make the portfolio and interviews land.
**Chapters:** the roles map (ML Engineer vs AI Engineer vs LLM/Applied Scientist vs MLOps vs Data Scientist — what each does and screens for) · building a portfolio (GitHub, deployed demos, a technical blog) · Kaggle & competitions · contributing to open source · the AI/ML resume · coding/DSA for ML interviews · ML-theory & ML-breadth interviews · **ML system-design interviews** · **LLM/RAG/agent system-design interviews** · take-home projects & how to ace them · the job search, referrals & networking · staying current (papers, newsletters, communities).
**Hands-on:** ship a portfolio; run mock interviews. **Capstone:** a polished portfolio of 3–4 deployed projects (incl. the custom LLM from M11 and the production RAG app from M12–13) + a passed mock interview loop.

---

## PART B — PLATFORM & CONTENT-PRODUCTION PLAN

### B0. Prerequisites & Infrastructure (free-tier-first) ✨ — your second ask

**Guiding rule:** *nothing paid until a module truly needs it, and every paid step has a free or local alternative.* A learner can complete Modules 0–10 for **₹0** using a browser, a Google account (Colab), a free Kaggle account, a free Hugging Face account, and **Ollama on their own laptop**. Paid API keys and rented GPUs only become necessary in the LLM-app, custom-training, and production modules — and even there, free local paths exist.

| Tier | Needed from (modules) | What you need | Free / local option | Paid option (only for scale/convenience) |
|------|----------------------|---------------|---------------------|--------------------------------------------------|
| **0 — Just a browser** | M0–M4 | Browser; optional Google account | **JupyterLite in-page**, Google **Colab** (free), local Python (optional) | — |
| **1 — Free GPU notebooks** | M5–M10 | Google account; **Kaggle** account (free GPU/TPU quota); **Hugging Face** account + access token (free) | Colab free T4 GPU; Kaggle weekly GPU hours; HF Hub for datasets/models | Colab Pro/Pro+ for longer/bigger GPUs |
| **2 — Hosted LLM APIs** | M8, M12, M14 (using frontier models) | An LLM **API key** | **Local Ollama** (no key, runs Llama/Mistral/Qwen/Phi on a laptop CPU/GPU); free tiers on **Groq / OpenRouter / Google AI Studio (Gemini)** | **OpenAI**, **Anthropic (Claude)**, **Google Gemini**, Mistral, Together — pay-per-token |
| **3 — Local/self-hosted inference** | M11, M13 | A way to run models locally | **Ollama**, **llama.cpp**, **LM Studio** (CPU/consumer GPU); **GGUF** quantized models | A consumer GPU (e.g., RTX 4090) for faster local serving |
| **4 — Training a custom LLM** | M11 (pretraining), M9 (RL) | **Cloud GPUs** + HF Hub | Small models (~100M–1B) train on a single Colab/Kaggle T4 or a cheap spot GPU; **vLLM** to serve | Rent A100/H100 by the hour from **RunPod / Lambda / Vast.ai / Modal**, or AWS/GCP/Azure; serve with **vLLM** |
| **5 — Production / MLOps** | M12–M13 | Git/GitHub, **Docker**, a vector DB, experiment tracking | **Chroma / pgvector** (local), **Qdrant / Pinecone** free tiers; **MLflow / Weights & Biases** free tiers; GitHub free | Managed vector DB, cloud hosting, paid observability |

**Practical setup notes**
- **Ollama** is the recommended default for "run an LLM yourself" from Module 8 onward — one install, no API key, works offline on a laptop; perfect for a broad, cost-sensitive audience. **vLLM** is introduced later (M11/M13) as the *throughput-oriented server* for when you deploy your own model on a GPU.
- **API keys:** teach learners to create keys, **set hard spend limits**, never commit keys to Git (use `.env`/secrets), and prefer the cheapest small model that demonstrates the concept. Always show a **free fallback** (Ollama/Groq/Gemini free tier) alongside any paid-API example.
- **Cloud GPUs:** for the custom-LLM capstone, recommend **RunPod / Lambda / Modal / Vast.ai** spot instances billed by the minute; emphasize that *learning to pretrain* needs only a small model on a single modern GPU — frontier-scale compute is explicitly out of scope, and that's fine.
- **A "Prerequisites & Setup" chapter ships inside Module 0** (accounts, Colab, Ollama, HF token) and a **"Cloud GPU & training setup" chapter ships inside Module 11** (renting a GPU, moving data, running a distributed job) so infra is taught just-in-time, never front-loaded.

### B1. Content structure & format
- **Hierarchy:** Module → Chapter → (sections + runnable notebook + Key Takeaways + Exercises).
- **Chapter length:** ~1,500–3,000 words or a 15–25 min notebook, **one concept per chapter**. Heavier modules (7–14) budget ~6–8 hours/week of learner effort.
- **Theory vs hands-on:** M0–2 ≈ 70/30; M3–10 ≈ 40/60; M11–14 ≈ 30/70.
- **Every chapter ends in a "Key Takeaways" box + 2–4 graded exercises.** Visual-first (diagrams for every architecture; animations for gradient descent, attention, diffusion). Downloadable notebooks/datasets.
- **Tone:** conversational, "assume the reader knows nothing," recurring analogies, a running example/project per module.

### B2. Designing hands-on exercises for a broad audience
- **Two-tier compute (the key decision):** **JupyterLite/Pyodide in-browser** for M0–4 and all quick "try it" cells (zero install, runs client-side); **Colab/Kaggle free GPU** for M5–14 ("Open in Colab" button per chapter); **local setup** taught as an optional M3 chapter; **rented GPU** only in M11.
- **Scaffolding:** fill-in-the-blank → "implement this function" → open-ended mini-project; hidden solution walkthroughs revealed after an attempt.
- **Auto-grading:** `assert`-based unit-test graders runnable in-browser; MCQ auto-grading for concept checks.

### B3. Assessment, practice & certification
- **Per-chapter:** 2–4 exercises + a 3–5 question concept check.
- **Per-module:** a Varsity-style MCQ quiz + a capstone (auto/peer-reviewed).
- **Spaced repetition & retrieval practice:** Dunlosky et al. (2013) rate **practice testing and distributed practice** as the two most effective study techniques — surface "review" cards from prior modules at spaced intervals.
- **Certification & tracks:** mirror Varsity Certified (proctored MCQ + project, ~65% pass). Offer named tracks: **Absolute Beginner → ML Practitioner → AI Engineer (LLMs) → LLM Builder (custom training) → MLOps/Production**, plus a final **"AI Engineer Certified"** gated on the custom-LLM and production-RAG capstones.

### B4. Platform & tech (Claude-Code-friendly)
- **Authoring:** Jupyter `.ipynb` for code-heavy chapters + Markdown/`.qmd` for prose (diffable, AI-editable).
- **Publishing:** **Quarto** → one static site (what fast.ai uses; supports code-fold, callouts, LaTeX, multi-format). Alternatives: Jupyter Book, Docusaurus/MDX.
- **Interactivity:** embed JupyterLite (Quarto live/Pyodide, e.g. `quarto-live`); "Open in Colab" for GPU chapters.
- **Hosting:** static site on GitHub Pages / Netlify / Vercel, CI/CD auto-deploy on merge.
- **Repo as product (docs-as-code):** everything in Git; chapters under `/modules/<n>/`; PR review for every change; CI runs notebook execution, link-checks, Markdown lint, spell-check — ideal for **phase-by-phase Claude Code development** (each phase = PRs against a clear spec).

### B5. Content-production workflow
- **Per-chapter template:** front-matter (title, module, difficulty, prereqs, objectives) → hook → explanation → runnable worked example → Key Takeaways → exercises → solution → further reading.
- **Loop:** draft → CI runs all cells → PR review → merge → auto-deploy.
- **Keeping AI content current (critical):** separate **stable core** (math, classical ML, backprop, transformers — write to last years) from **fast-moving frontier** (specific models, frameworks, vector DBs — isolated, version-pinned, "last reviewed" dated, swappable). Quarterly review cycle with per-chapter owners + a "What changed in AI" changelog; community PRs via forum/Discord.

---

## RECOMMENDED PHASED ROADMAP (hand each phase to Claude Code)

**Phase 0 — Platform MVP & conventions.** Git repo + folder convention; Quarto skeleton; per-chapter template; CI (execute notebooks, lint, link-check, deploy); JupyterLite embed + "Open in Colab" proven on one sample chapter; design system (Key Takeaways box, difficulty badges). **Exit:** one fully working sample chapter end-to-end.

**Phase 1 — Foundations track (M0–3).** What-is-AI, Python, Math, Data & Tooling, fully in-browser. **Includes the M0 "Prerequisites & Setup" chapter** (accounts, Colab, Ollama, HF token). **Exit:** a non-technical learner goes zero → EDA capstone entirely in-browser, ₹0 spend.

**Phase 2 — Core ML & DL (M4–6).** Classical ML, DL foundations (scratch + PyTorch), Vision & Sequences; Colab/Kaggle GPU integration; auto-graders. **Exit:** learner builds/evaluates tabular models and trains a neural net from scratch and in PyTorch.

**Phase 3 — Transformers, LLMs, RL & GenAI (M7–10).** Build-a-GPT, LLMs (fine-tune + eval), **RL & reasoning models**, Generative AI. Introduces Ollama + free LLM-API fallbacks. **Exit:** learner builds a small GPT, fine-tunes + evaluates an LLM, runs a preference-optimization loop, and runs a diffusion pipeline.

**Phase 4 — Build Your Own LLM (M11).** ✨ The custom-LLM module: data → tokenizer → pretraining → distributed training → post-training → quantize → serve (Ollama + vLLM). **Includes the "Cloud GPU & training setup" chapter.** **Exit:** learner trains a small custom LLM from scratch and serves it locally and via API — the headline capability.

**Phase 5 — AI Engineering & Production (M12–13).** RAG, Agents & MCP; MLOps/LLMOps; deployable capstones; observability/cost. **Exit:** learner ships a deployed, monitored RAG+agent app — the prototype-to-production proof.

**Phase 6 — Responsible AI, Electives, Career & Certification (M14–16 + platform).** OWASP/Responsible-AI module; applied electives; **Career & Job-Readiness module**; certification exams + proctoring; spaced-repetition review; learning paths; community forum. **Exit:** a complete newbie→frontier school where a graduate is job-ready and certified.

**Phase 7 (ongoing) — Maintenance & currency.** Quarterly review cadence, per-chapter owners, frontier refresh, changelog/newsletter, community PR pipeline.

---

## OUTCOMES & JOB-READINESS — what a graduate can do ✨ (your third ask)

By finishing the curriculum and its capstones, a learner can credibly claim — and *demonstrate via portfolio* — the following:

**Can build & ship**
- Train classical ML and deep-learning models from scratch and with PyTorch (M4–6).
- Build a transformer/GPT from first principles and fine-tune LLMs with LoRA/QLoRA, with rigorous evaluation (M7–8).
- Apply RL/preference methods (RLHF/DPO/GRPO) to post-train and improve model behavior and reasoning (M9).
- **Build a custom LLM end-to-end** — curate data, train a tokenizer, pretrain, post-train, quantize, and **serve it with Ollama/vLLM** (M11). *This directly answers "develop custom LLM and all the things."*
- Build production-grade **RAG + agent applications** (incl. MCP, tools, multi-agent) (M12).
- **Deploy, monitor, secure and cost-optimize** AI services with proper MLOps/LLMOps and OWASP-aligned guardrails (M13–14).

**Roles this prepares you for** (covered explicitly in M16): **AI/LLM Engineer** (strongest fit and hottest market — RAG, agents, fine-tuning, serving), **ML Engineer** (training + production pipelines), **MLOps Engineer** (deployment, monitoring, scale), **Applied Scientist / Research Engineer** (with the from-scratch + RL depth), and **Data Scientist** (via classical ML + electives).

**Job-readiness deliverables baked in:** a public **GitHub portfolio of 3–4 deployed projects** (custom LLM, production RAG/agent app, a fine-tuned + evaluated model, one elective), a **technical blog**, preparation for **coding, ML-theory, and ML/LLM system-design interviews**, and a passed **mock interview loop** — plus the platform's own **"AI Engineer Certified"** credential gated on the M11 + M12–13 capstones.

---

## Recommendations (decision-ready)
1. **Two outcomes define success:** (a) a learner can train and serve a custom LLM (M11), and (b) a learner is interview-ready with a deployed portfolio (M16). Sequence the build so these are reachable and prove them with real capstones, not slideware.
2. **Free-tier-first, taught just-in-time.** Keep M0–10 at ₹0 (browser + Colab/Kaggle + Ollama). Introduce optional paid API keys (always with a free Ollama/Groq/Gemini fallback) from M8, and a rented GPU only in M11 — with hard spend caps and a free local fallback for every paid example.
3. **Commit to "runnable-everything"** (JupyterLite for beginners + Colab/GPU for heavy work); prove it in Phase 0 before authoring at scale.
4. **Adopt docs-as-code from day one** (Git + Quarto + CI) — cheap to host, correct, and ideal for phased Claude Code development.
5. **Write foundations to last, isolate the frontier** (version-pinned, "last reviewed" dated, swappable chapters; standing quarterly refresh).
6. **Keep Varsity's soul:** plain language, one idea per chapter, analogies, Key Takeaways, free/no-signup, three tiers, quizzes → certification. The power is editorial, not technical — don't over-engineer.

## Caveats
- **Frontier specifics date fast.** Vector-DB rankings, "best" models, GRPO/reasoning techniques, and framework APIs here are late-2025/2026 snapshots — examples, not commitments. The maintenance plan exists precisely for this.
- **Custom-LLM training is scoped to *small* models.** Learners pretrain ~100M–1B-param models to *understand the full pipeline*; frontier-scale pretraining (billions of params, large clusters) is intentionally out of scope on cost grounds, and the curriculum says so plainly.
- **In-browser compute has real limits** (memory, package availability, no GPU); the JupyterLite + Colab dual strategy mitigates but doesn't eliminate this.
- **Auto-grading open-ended work is hard** (RAG quality, generated images, a custom model's outputs need rubrics/peer review/AI-as-a-judge — itself imperfect).
- **"Job-ready" ≠ guaranteed offer.** The curriculum builds the demonstrable skills and portfolio employers screen for; outcomes still depend on the market, the learner's prior background, and interview performance.
- **Accounts/keys carry obligations:** managing API spend, data-protection rules (EU/India), and certification proctoring add operational complexity not fully scoped here.