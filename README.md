# Statistical Evaluation Tutorial

A practical, example-driven tutorial on doing statistical evaluations in
ECE/CS experimental papers, intended for beginning student researchers in
systems, networking, and applied machine learning. Two PDFs and a
reproducible simulator:

| | What it is | Where it lives |
|---|---|---|
| **Tutorial paper** | The 31-page tutorial. *What* a defensible evaluation is. | [`paper/stateval.pdf`](paper/stateval.pdf) |
| **Student workbook** | The 6-page hands-on companion. *How* a student plans one before touching the code. Project-type table, fragile-evaluation autopsy, fill-in worksheet (with worked example), exercises. | [`appendix/student-appendix.pdf`](appendix/student-appendix.pdf) |
| **Reproducible simulator** | Single Python script that regenerates every figure and headline number in the paper from a seeded FIFO-vs-SRPT simulation. | [`code/figures.py`](code/figures.py) |
| **Claude Code review skill** | A `/stateval-review` command that audits a student paper against the tutorial's principles and writes a prioritized review. | [`skill/stateval-review/`](skill/stateval-review/) |

**Author:** Bhaskar Krishnamachari ([bkrishna@usc.edu](mailto:bkrishna@usc.edu)),
University of Southern California.

---

## Repository layout

```
.
├── paper/                    Main tutorial paper.
│   ├── stateval.tex          LaTeX source.
│   ├── stateval.bib          Bibliography (every entry verified
│   │                          against Crossref/arXiv/publisher).
│   ├── stateval.pdf          Compiled PDF.
│   └── figs/                 Figures produced by code/figures.py.
│
├── appendix/                 Student-facing companion workbook.
│   ├── student-appendix.tex  LaTeX source. Uses xr to pull section
│   │                          numbers from ../paper/stateval.aux,
│   │                          so cross-references stay current.
│   └── student-appendix.pdf  Compiled PDF.
│
├── code/                     Reproducible simulator + figure generator.
│   └── figures.py            One script, six figures, headline numbers.
│
├── skill/                    Claude Code skill (see "Review skill" below).
│   └── stateval-review/
│
├── Makefile                  make / make figures / make paper / make workbook.
├── README.md                 This file.
└── .gitignore
```

---

## What the tutorial covers

The tutorial is organized as an evaluation **workflow**, not a stats
syllabus:

> **claim → hypothesis → unit of analysis → baselines → regimes → metrics
> → uncertainty → validation → reporting → reproducibility**

Each section closes a specific class of reviewer objection. Topics
include:

- Experimental design (hypotheses, baselines, regimes, repeated trials,
  randomization and blocking, primary vs. secondary metrics).
- The unit of analysis and pseudoreplication ("1,000,000 packets is not
  *n* = 10⁶").
- Confidence intervals: normal/Wald, Student's *t*, and the bootstrap,
  with caveats on resampling units, time-series, nested data, small *n*,
  and tail quantities.
- Hypothesis testing: parametric (one-/two-sample/paired *t*, ANOVA, χ²,
  Pearson) and non-parametric (Wilcoxon signed-rank, Mann–Whitney U,
  Kruskal–Wallis, Friedman, Kolmogorov–Smirnov), with caveats on
  symmetry, shape, ties, and McNemar for paired ML predictions.
- Effect size (Cohen's *d*, Cliff's delta, η², domain-natural
  percentages); estimation-first reporting; CI of the difference.
- Tradeoffs and Pareto fronts; equivalence and non-inferiority claims.
- Linear regression, residual diagnostics; multi-factor designs and
  interactions.
- Multiple comparisons; the garden of forking paths.
- Out-of-sample validation; ablation studies.
- Latency-specific pitfalls (heavy tails, coordinated omission, warmup).
- Reporting and figure design (CIs vs. SE bars; CI of the difference;
  log axes; box and violin plots).
- Random seeds and non-determinism; sample size and power.
- Outliers, failed runs, and exclusion rules.
- Time-correlated data and the block bootstrap.
- Simulation **verification** vs. **validation** (sanity, baseline
  reproduction, sensitivity, conservation, common random numbers).
- Machine-learning evaluations (data leakage; grouped and temporal
  splits; nested CV; metrics for classification, regression, ranking,
  language models, detection, RL).
- Reproducibility, a minimal toolkit, and an evaluation-section template.
- Appendices: pre-submission checklist and glossary.

A running example threads the document: a comparison of two
job-scheduling policies (**FIFO** vs. **SRPT**) on simulated workloads
with Poisson arrivals and **truncated** Pareto job sizes (truncation
keeps the heavy-tail lesson while keeping the mean well-defined).

The companion workbook adds:

- A **project-type translation table** (wireless, systems benchmark, ML,
  scheduler, embedded, simulation) showing unit of analysis, metrics,
  common mistakes, and recommended defaults for each.
- An **anatomy of a fragile evaluation**: a typical weak claim, the nine
  hidden problems behind it, and a defensible rewrite.
- A **fill-in evaluation-plan worksheet** (18 items, ending with "what
  result would make us weaken or abandon the claim?"), with a fully
  worked-out example for the FIFO/SRPT case so students see the level of
  specificity expected.
- **Exercises** mapped to main-paper sections, ranging from "rewrite a
  weak claim" to factorial-design budgeting and equivalence reasoning.

---

## Building from source

The repository contains everything needed to rebuild both PDFs and all
six figures from scratch.

### Quick start

```bash
git clone https://github.com/ANRGUSC/statistical-eval-tutorial.git
cd statistical-eval-tutorial
make           # builds paper/stateval.pdf and appendix/student-appendix.pdf
```

### Make targets

```
make            # build paper + workbook
make figures    # regenerate paper/figs/ from a seeded simulation
make paper      # compile paper/stateval.pdf (runs bibtex)
make workbook   # compile appendix/student-appendix.pdf (xr needs paper first)
make clean      # remove LaTeX build artifacts
make distclean  # also remove generated PDFs and figures
```

### Manual build

```bash
# (1) Regenerate figures (optional; figures are checked in).
python code/figures.py
# Writes paper/figs/{bootstrap,box_violin,error_bars,interaction,latency_cdf,power}.pdf
# and prints headline numbers used in the paper text.

# (2) Compile the paper.
cd paper
pdflatex stateval.tex
bibtex   stateval
pdflatex stateval.tex
pdflatex stateval.tex
cd ..

# (3) Compile the workbook (requires paper/stateval.aux from step 2 so
#     that cross-references via the xr package resolve).
cd appendix
pdflatex student-appendix.tex
pdflatex student-appendix.tex
```

### Requirements

- Python 3.10+ with `numpy`, `scipy`, `matplotlib`.
- A LaTeX distribution with `pdflatex`, `bibtex`, and the packages used
  in the preambles (`natbib`, `tikz`, `listings`, `framed`, `booktabs`,
  `enumitem`, `xr`).

---

## Review skill (Claude Code)

The repository ships with a Claude Code skill,
[`stateval-review`](skill/stateval-review/), that lets a student point
Claude at their own paper draft (`.tex` or `.pdf`) and get back a
structured review document grounded in the tutorial's principles. The
skill produces `stateval-review.md` in the working directory: a list of
strengths, prioritized findings (Critical / Important / Nice-to-have)
with quote-and-suggest fixes, a checklist pass/fail grid, and pointers
back to the relevant tutorial sections.

**Install:**

```bash
cp -r skill/stateval-review ~/.claude/skills/
```

**Use:**

```
/stateval-review path/to/paper.tex
```

The skill audits 24 categories: hypothesis quality, baseline strength,
seed counts, unit of analysis, variability reporting, CI construction,
test choice and assumption checking, effect size, regression
diagnostics, multi-factor design, multiple comparisons, out-of-sample
validation, ablation studies, latency pitfalls, figure design, seed
discipline, sample size, time-correlated data, simulation V&V,
ML-metric matching, reproducibility, equivalence claims, and primary
vs. secondary metric pre-registration.

The skill does **not** edit the student's paper; it writes a separate
review file the student then acts on.

---

## Suggested workflow for student research

The two-document structure is meant to be used together over the life of
a student project:

| When | Document | What to do |
|---|---|---|
| Before experiments | Workbook | Identify your project type from Table 1; fill out the Evaluation Plan Worksheet. |
| First research meeting | Workbook | Discuss only items 1–12 of the worksheet (claim, hypothesis, metrics, unit of analysis, baselines, regimes, seeds, pairing/blocking, summary, test). |
| After a pilot run | Tutorial paper | Revisit sample size, exclusion rules, plots, and validation. |
| Before paper writing | Tutorial paper | Use the pre-submission checklist (Appendix A) and the evaluation-section template. |
| Before submission | Skill | Run `/stateval-review` on the draft and act on the findings. |

---

## Citing

If you use or refer to this tutorial, please cite it as:

> Bhaskar Krishnamachari. *How to Do Statistical Evaluations in ECE/CS
> Papers: A Practical Playbook for Defensible Results.* 2026.

---

## License

The text and figures of this tutorial are released for educational and
research use; please credit the author when reusing material. The
accompanying code (`code/figures.py`) and the Claude Code skill are
released under the MIT License.
