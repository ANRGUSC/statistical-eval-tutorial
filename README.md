# Statistical Evaluation Tutorial

A practical, example-driven tutorial on doing statistical evaluations in
ECE/CS experimental papers, intended for beginning student researchers in
systems, networking, and applied machine learning.

**Author:** Bhaskar Krishnamachari
([bkrishna@usc.edu](mailto:bkrishna@usc.edu)),
University of Southern California.

## What this covers

The tutorial is comprehensive at a beginner level. Topics include:

- Experimental design (hypotheses, baselines, regimes, repeated trials).
- Descriptive statistics, the central limit theorem, and three flavors of
  confidence interval (normal/Wald, Student's *t*, and the bootstrap).
- Hypothesis testing fundamentals (null/alternative, *p*-value, Type I/II,
  power); parametric tests (one-sample, paired, and two-sample *t*; one-way
  ANOVA; chi-squared; Pearson correlation); checking parametric assumptions
  (Q–Q plots, Shapiro–Wilk, Levene); non-parametric alternatives (Wilcoxon
  signed-rank, Mann–Whitney U, Kruskal–Wallis, Friedman, Kolmogorov–Smirnov).
- Effect size (Cohen's *d*, Cliff's delta, η²) and practical significance.
- Linear regression and correlation (OLS, *R*², residual diagnostics).
- Multi-factor experiments (one-factor-at-a-time screening, full and
  fractional factorial designs, interaction plots).
- Multiple comparisons (Bonferroni, Benjamini–Hochberg, the garden of
  forking paths).
- Out-of-sample validation and ablation studies.
- Latency-specific pitfalls (heavy tails, coordinated omission, warmup).
- Reporting and figure design (CIs vs. SE bars, log axes, box plots,
  violin plots).
- Random seeds and non-determinism.
- Sample size and power analysis.
- Time-correlated data and the block bootstrap.
- Simulation validation (sanity checks, baseline reproduction, sensitivity,
  conservation, common random numbers for variance reduction).
- Machine-learning evaluations (data leakage; metrics for classification,
  regression, ranking, language models, detection, and reinforcement
  learning).
- Reproducibility, a minimal toolkit, and an evaluation-section template.
- Appendices: pre-submission checklist and a glossary.

A running example threads through the document: a comparison of two
job-scheduling policies (FIFO vs. SRPT) on simulated workloads with
Poisson arrivals and Pareto job sizes.

## Repository layout

| File | Purpose |
|---|---|
| `stateval.tex` | LaTeX source of the tutorial. |
| `stateval.bib` | Bibliography (every entry verified against Crossref/arXiv). |
| `stateval.pdf` | Compiled tutorial. |
| `figures.py` | Single Python script that regenerates every figure and the headline numbers from a seeded simulation. |
| `figs/` | Generated PDF figures. |
| `skill/stateval-review/` | A Claude Code skill that audits a paper draft against the tutorial's principles and writes a prioritized review. |

The tutorial is itself reproducible: rerunning `figures.py` regenerates
every figure used in the paper, and recompiling the LaTeX source produces
the PDF.

## Companion Claude Code skill

The repository ships with a Claude Code skill called **`stateval-review`**
that lets a student point Claude at their own paper draft (`.tex` or
`.pdf`) and get back a structured review document grounded in the
tutorial's principles. The skill produces `stateval-review.md` in the
working directory: a list of strengths, prioritized findings (Critical /
Important / Nice-to-have) with quote-and-suggest fixes, a checklist
pass/fail grid, and pointers back to the relevant tutorial sections.

Install:

```bash
git clone https://github.com/ANRGUSC/statistical-eval-tutorial.git
cp -r statistical-eval-tutorial/skill/stateval-review ~/.claude/skills/
```

Use:

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

## Building from source

```bash
# Regenerate figures (optional; figures are checked in).
python figures.py

# Compile the PDF.
pdflatex stateval.tex
bibtex   stateval
pdflatex stateval.tex
pdflatex stateval.tex
```

Requires:
- Python 3.10+ with `numpy`, `scipy`, `matplotlib`.
- A LaTeX distribution with `pdflatex`, `bibtex`, and the packages used in
  the preamble (`natbib`, `tikz`, `listings`, `framed`, `booktabs`).

## Citing

If you use or refer to this tutorial, please cite it as:

> Bhaskar Krishnamachari. *How to Do Statistical Evaluations in ECE/CS
> Papers: A Practical Playbook for Defensible Results.* 2026.

## License

The text and figures of this tutorial are released for educational and
research use; please credit the author when reusing material. The
accompanying code (`figures.py`) is released under the MIT License.
