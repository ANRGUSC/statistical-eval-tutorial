# Paper-type detection and per-type audit filters

Use the heuristics below to classify the paper, then use the per-type
filter to decide which of the 27 audit categories in `principles.md`
apply to this paper.

## Detection heuristics

Scan the abstract, intro, and section headings for the signals below.
Match the paper against the most specific type that fits; if multiple
match strongly, classify as `hybrid`.

### `systems`

Signals (any 2+):

- Metrics: latency, throughput, p95/p99/tail, jitter, queue length,
  goodput, packet loss, energy per request.
- Section names: "Implementation," "Testbed," "Evaluation,"
  "Architecture," "Protocol."
- Domain words: scheduler, network, kernel, distributed, cache, queue,
  load, request, server, RPC, CDN, datacenter.
- Mentions a real or simulated workload trace, an SUT, or a deployment.

### `applied-ml`

Signals (any 2+):

- Section names: "Training," "Architecture" (in the neural sense),
  "Datasets," "Hyperparameters," "Loss."
- Vocabulary: training set, validation set, test set, epoch,
  batch size, learning rate, gradient, embedding, transformer,
  fine-tune, perplexity, accuracy, F1, AUROC, BLEU, IoU.
- Mentions specific frameworks: PyTorch, JAX, TensorFlow, HuggingFace.
- Uses benchmark datasets: ImageNet, CIFAR, GLUE, SQuAD, MS-COCO,
  Atari, MuJoCo, etc.

### `theory-with-experiments`

Signals (any 2+):

- Heavy use of theorem/lemma/proof environments.
- Section names: "Analysis," "Proof," "Numerical Results,"
  "Simulation Validation."
- Numerical results section is short relative to analysis (typically
  <30% of the paper).
- Experiments mostly validate analytical predictions, rather than
  establishing new empirical findings.

### `hardware-or-embedded`

Signals (any 2+):

- Vocabulary: circuit, FPGA, ASIC, MCU, sensor, IoT device, voltage,
  current, dB, energy harvesting, sleep state.
- Reports power, energy, area, frequency, lifetime.
- Mentions hardware platforms (Raspberry Pi, Arduino, specific SoCs,
  FPGAs).

### `hybrid`

Two or more of the above match strongly. Examples:

- A scheduler paper that trains an RL agent: `systems` + `applied-ml`.
- A paper proving regret bounds *and* running large-scale RL
  experiments: `theory-with-experiments` + `applied-ml`.
- An on-device ML paper: `applied-ml` + `hardware-or-embedded`.

For hybrids, take the union of the per-type filters.

### Out of scope (decline)

Decline the audit and report the type if the paper is:

- A **survey** (organizes existing literature, no new experiments).
- A **position or vision** paper (argues a viewpoint, no experiments).
- A **magazine article or editorial** (tutorial register, no
  contribution).
- A **theory-only** paper with no numerical results section.

These are not experimental papers; the audit categories do not apply.

## Per-type audit filter

The 27 categories from `principles.md`, with which apply per type.
`Y` = audit; `N` = skip; `*` = audit only if relevant signals are
present in the paper.

| # | Category | systems | applied-ml | theory+exp | hardware |
|---|----------|---------|-----------|------------|----------|
| 1 | Hypothesis stated and falsifiable | Y | Y | Y | Y |
| 2 | Strong baseline; baseline ≠ ablation | Y | Y | Y | Y |
| 3 | Repeated trials, seed count, rationale | Y | Y | Y | Y |
| 4 | Randomization, blocking, order effects | Y | * | * | Y |
| 5 | Primary and secondary metrics named in advance | Y | Y | Y | Y |
| 6 | Unit of analysis / pseudoreplication | Y | Y | Y | Y |
| 7 | Variability reporting (mean alone is not enough) | Y | Y | Y | Y |
| 8 | CI construction matches the data | Y | Y | Y | Y |
| 9 | CI of the difference for paired comparisons | Y | Y | Y | Y |
| 10 | Test choice: paired/unpaired, parametric/non-param, assumptions | Y | Y | Y | Y |
| 11 | Effect size leads, p-value supports (estimation-first) | Y | Y | Y | Y |
| 12 | Linear regression diagnostics | * | * | * | * |
| 13 | Multi-factor design: OFAT, factorial, interactions | Y | Y | * | Y |
| 14 | Multiple comparisons correction | Y | Y | Y | Y |
| 15 | Tradeoffs and Pareto fronts | Y | Y | * | Y |
| 16 | Equivalence and non-inferiority claims | * | * | * | * |
| 17 | Out-of-sample validation; train/val/test | * | Y | * | * |
| 18 | Ablation studies | Y | Y | * | Y |
| 19 | Latency-specific pitfalls | * | * | N | * |
| 20 | Reporting and figure design | Y | Y | Y | Y |
| 21 | Random seeds and non-determinism | Y | Y | * | * |
| 22 | Sample size and power | Y | Y | Y | Y |
| 23 | Outliers, failed runs, exclusion rules | Y | Y | * | Y |
| 24 | Time-correlated data and block bootstrap | * | * | * | * |
| 25 | Simulation V&V | * | * | Y | * |
| 26 | ML evaluation: leakage, splits, metrics | N | Y | * | * |
| 27 | Reproducibility | Y | Y | Y | Y |

`*` triggers if the paper contains relevant signals:

- Cat 4 (applied-ml / theory+exp): paper runs experiments on a
  physical machine or testbed where order/thermal/contention
  confounders are plausible.
- Cat 12: paper reports a regression or correlation.
- Cat 13 (theory+exp): the experimental section sweeps multiple
  knobs.
- Cat 15 (theory+exp): paper reports cost/overhead alongside its
  primary metric.
- Cat 16: paper claims a tie, "no worse than," or "same X with less
  Y" comparison.
- Cat 17 (non-ML types): paper reports tuning + headline numbers.
- Cat 18 (theory+exp): paper proposes a multi-component method.
- Cat 19: paper measures latency or response time.
- Cat 21 (theory+exp / hardware): paper reports stochastic
  experiments with seeds or stochastic platforms.
- Cat 23 (theory+exp): paper might exclude failed runs.
- Cat 24: paper reports time-series measurements (per-second
  throughput, per-packet inter-arrival times, etc.).
- Cat 25 (non-theory): the paper relies on a simulator for its
  headline numbers.
- Cat 26 (non-ML): paper computes ML-style metrics (e.g., a systems
  paper with a classifier sub-component).

Always audit the un-starred (Y) categories for the matched type.
