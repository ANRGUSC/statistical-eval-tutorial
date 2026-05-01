# Audit principles, symptoms, and fixes

For each of 24 categories, this file gives:

- **Principle** — what a credible evaluation must do, in one sentence.
- **Symptoms** — concrete things to look for in the paper that indicate
  the principle is being violated.
- **Fix** — a specific, actionable change the student should make.

Use this file in step 4 of the workflow. For each category that the
paper-type filter says applies, read its entry and scan the paper for
the symptoms. If a symptom is present, file a finding using the format
in `output-template.md`.

The categories are numbered. Always cite the number in findings so the
student can locate the canonical principle.

---

## 1. Hypothesis stated and falsifiable

**Principle.** The paper states the hypothesis its experiment is meant
to test, in a form that the experiment could in principle disprove.

**Symptoms.**
- The introduction says the paper "improves," "outperforms," or "is
  better than" without committing to a metric, condition, or direction.
- No explicit hypothesis statement anywhere; the reader must infer it
  from the results section.
- The hypothesis is unfalsifiable as written ("our system is good,"
  "the method scales").

**Fix.** Add one sentence near the end of the introduction of the form
"We hypothesize that <method> reduces <metric> by at least <amount>
under <condition>, relative to <baseline>." Tutorial: §Experimental
Design.

---

## 2. Strong baseline, and baseline distinct from ablation

**Principle.** The headline comparison is against the strongest
reasonable existing method (not a strawman), and ablations are
separate experiments that isolate component contribution.

**Symptoms.**
- The baseline is an obviously-weak method nobody would actually use
  (e.g., random scheduling, untuned defaults from a 10-year-old paper)
  and no stronger comparator is included.
- "Ablation" and "baseline comparison" are conflated; the only
  comparison is the proposed method vs. its components, with no
  comparison to existing work.
- Baseline hyperparameters are tuned on training data while the
  proposed method's are tuned on test data, or vice versa.

**Fix.** Identify the strongest method already in the literature for the
same setting, tune it on the same data the proposed method was tuned
on, and add it to the headline comparison. Keep ablations as a separate
experiment. Tutorial: §Experimental Design and §Ablation Studies.

---

## 3. Repeated trials with multiple seeds, and the count is justified

**Principle.** Each configuration is run with at least 10 random seeds
(30+ for tail metrics), and the choice of $n$ is stated and defensible.

**Symptoms.**
- Single run reported, or "averaged over <small number, e.g., 3>
  runs."
- No statement of how many seeds were used.
- "Averaged over 5 runs" with no rationale, on a stochastic system.
- Tail metrics ($p_{95}$, $p_{99}$) reported from a small number of
  short runs.

**Fix.** Run at least 30 seeds per configuration; for tail metrics,
ensure each run produces enough requests/episodes to estimate the tail
($n \cdot \text{requests per run} \gtrsim 10^4$). State the seed count
explicitly in the experimental setup paragraph. Tutorial: §Measurement
and Variability and §Sample Size and Power.

---

## 4. Unit of analysis / pseudoreplication

**Principle.** The unit of analysis matches what was independently
randomized. Treating correlated within-run measurements as independent
samples is pseudoreplication and inflates apparent precision.

**Symptoms.**
- Reported $n$ is the number of packets / queries / episodes / tokens
  / forward passes, not the number of independent runs.
- "We measured 1,000,000 latencies" used as the sample size for a
  variance estimate or test.
- Confidence intervals computed from per-event measurements within a
  single run.
- Cross-validation folds that cluster correlated data (same patient,
  same session, same time window) across train and test.

**Fix.** Define the unit of analysis as the independent run (one seed,
one workload draw). Summarize each run by a single statistic (mean,
$p_{99}$, accuracy), then compute variability and tests across runs.
For cross-validation with grouped data, use a grouped split that keeps
all members of a group on the same side. Tutorial: §Measurement and
Variability.

---

## 5. Variability reporting beyond a mean

**Principle.** Every headline number is reported with a measure of
spread, ideally a 95% confidence interval. Standard errors and
standard deviations are insufficient on their own.

**Symptoms.**
- Headline result is a single number ("47.2 ms") with no $\pm$ or CI.
- Bar charts with no error bars, or with bars that have no caption
  explaining what they represent.
- Error bars labeled "$\pm$ std" or unlabeled.
- Tables with mean only, no spread column.

**Fix.** Replace each headline mean with "<mean> (95% CI: <low>--<high>)"
computed via the bootstrap. Tutorial: §Variability and Confidence
Intervals.

---

## 6. CI of the difference, not separate error bars

**Principle.** When comparing two methods, the right uncertainty
quantity is the CI on the per-pair *difference*, not separate error
bars on each arm.

**Symptoms.**
- Two bars side by side with overlapping error bars; the paper claims
  one is better.
- Per-method error bars without a paired-difference CI, in a paired
  experimental design.
- "Method A: $5.0 \pm 0.5$, Method B: $4.7 \pm 0.4$, so A is faster"
  without a CI on $A - B$.

**Fix.** Run paired trials (same seeds), compute the per-seed
difference, bootstrap a 95% CI on the mean difference. Report
"<method A> reduces <metric> by <X>% (95% CI: <a>%--<b>%) relative to
<method B>." Tutorial: §Variability and Confidence Intervals and
§Reporting and Figure Design.

---

## 7. CI construction matches the data

**Principle.** The CI construction matches the data: bootstrap for
heavy-tailed or non-normal data, $t$-based for small-$n$
approximately-normal data, normal/Wald only when $n$ is large and
data is well-behaved.

**Symptoms.**
- Latency data summarized with $\bar{x} \pm 1.96 s/\sqrt{n}$ as if
  normal, no normality check.
- "$\pm$ standard error" for $n < 30$ on heavy-tailed data.
- Bootstrap CIs reported with no statement of $B$ (number of
  resamples) or $n$.

**Fix.** For ECE/CS data, default to the bootstrap with $B \geq 10{,}000$.
Use the $t$-based CI for small-$n$ Gaussian-like data. Use the normal CI
only for large-$n$ averages of independent quantities.
Tutorial: §Variability and Confidence Intervals.

---

## 8. Test choice: paired/unpaired, parametric/non-parametric, with assumption checks

**Principle.** Tests are paired when the design is paired; the
parametric/non-parametric choice is justified by an explicit
distributional check; ECE/CS data defaults to non-parametric tests.

**Symptoms.**
- Two-sample $t$-test on data run with the same seeds (should be
  paired).
- Student's $t$-test on visibly heavy-tailed data with no Q--Q plot or
  Shapiro--Wilk result.
- ANOVA with no Levene's test or equivalent equal-variance check.
- One-tailed test used without an a-priori directional hypothesis.
- $\chi^2$ test on a contingency table with cells $< 5$.

**Fix.** Default to paired Wilcoxon signed-rank for two-condition
comparisons and Mann--Whitney U for unpaired; report Q--Q plots in an
appendix when defending parametric choices. Use Welch's $t$-test
(unequal variance) over Student's. Use Fisher's exact for sparse
contingency tables. Tutorial: §Hypothesis Testing.

---

## 9. Effect size leads, p-value supports

**Principle.** The paper reports an effect size with units the reader
cares about (% improvement, absolute difference, with CI), and uses
the $p$-value as a screening criterion, not as the headline.

**Symptoms.**
- Headline is "$p < 0.001$" with no effect size.
- Effect sizes reported only in a relegated table; p-values in the
  abstract.
- Statistically significant results celebrated when the effect is
  practically negligible (e.g., 0.3% improvement claimed as a win).
- No CI on the difference (overlaps with Cat 6).

**Fix.** Lead with the absolute and relative effect, both with CIs;
report the test result in support. Apply Cohen's $d$ or Cliff's delta
when standardization is needed for cross-study comparison. Tutorial:
§Effect Size and Practical Significance.

---

## 10. Linear regression diagnostics

**Principle.** When a regression or correlation is reported, the
paper includes residual diagnostics and reports $R^2$ alongside the
coefficient with its CI. Pearson is reserved for verified linear
relationships; otherwise use Spearman or Kendall.

**Symptoms.**
- $R^2 = 0.92$ reported with no residual plot.
- Pearson correlation reported on data that visibly curves on a
  scatter plot.
- Multiple regression with highly correlated predictors, no mention
  of multicollinearity (VIF / condition number).
- Slope reported with no SE or CI.

**Fix.** Add a residual-vs-fitted plot to the appendix; check for
patterns (U-shape, fan, autocorrelation). Replace Pearson with
Spearman when the relationship is monotone but non-linear. Report the
slope with its 95% CI. Tutorial: §Linear Regression and Correlation.

---

## 11. Multi-factor design: OFAT screening, factorial for headlines

**Principle.** OFAT (one-factor-at-a-time) sweeps are a screening
step; the headline evaluation uses a factorial sweep over at least
the most-likely-to-interact factors and reports an interaction plot.

**Symptoms.**
- The evaluation is one OFAT sweep at "default" parameters, presented
  as the headline.
- Sweep over load with everything else fixed; sweep over size
  distribution with everything else fixed; the two are not crossed.
- Single working point (e.g., one load, one workload) reported as the
  headline.
- No interaction plot; differences across regimes summarized only as
  averages.

**Fix.** Run a $2 \times 2$ or $3 \times 3$ factorial over the two
factors most likely to interact (e.g., load $\times$ size
distribution); plot as an interaction plot; report per-cell
comparisons and the interaction effect. Tutorial: §Multi-factor
Experiments.

---

## 12. Multiple-comparisons correction

**Principle.** When many tests are reported, the paper applies an
appropriate correction (Bonferroni, Benjamini--Hochberg) and
discusses the garden of forking paths if the analysis was
data-dependent.

**Symptoms.**
- Many pairwise tests reported (e.g., proposed method vs. 8
  baselines on 5 datasets), all at $p < 0.05$, no correction.
- Subgroup or per-condition $p$-values reported individually with no
  family-wise control.
- Mention of "we found that on the subset where X..." without
  acknowledging this is post-hoc selection.

**Fix.** Apply Benjamini--Hochberg at $q = 0.05$ to control the false
discovery rate when reporting many tests; pre-register the analysis
plan in supplementary material if the choice of metric/cutoff was
made before seeing results. Tutorial: §Multiple Comparisons.

---

## 13. Out-of-sample validation; train/val/test discipline

**Principle.** The headline numbers come from data the method was not
tuned on; tuning, model selection, and reporting are done on disjoint
sets.

**Symptoms.**
- Hyperparameters tuned on the test set or on the same workloads
  used to report headline numbers.
- Single train/test split with no validation set.
- "We selected the best epoch by test loss."
- For systems papers: parameters of the proposed method tuned on the
  same workload trace used in the headline figure.

**Fix.** Use a train/val/test split: tune on val, report on test.
Touch the test set exactly once. For systems work, tune on a held-out
workload and report on the headline workload, or vice versa. Tutorial:
§Out-of-sample Validation.

---

## 14. Ablation studies

**Principle.** Multi-component methods are accompanied by ablations
that isolate each component's contribution, run with the same
statistical machinery as the main result.

**Symptoms.**
- Method has 3+ components (architecture A + loss B + augmentation C)
  with no ablation.
- Ablation table reports point estimates only, no CIs or seeds.
- Ablation done at one working point, not across the regimes used in
  the main evaluation.
- Components removed but the headline change ("we add C and gain
  20%") is reported on a different benchmark than the ablation
  ("removing C costs 2%").

**Fix.** Add a leave-one-out ablation table: full system, then full
system minus each component, with the same seeds and CIs as the
headline. If the gain attributed to a component is not recovered when
that component is removed, investigate. Tutorial: §Ablation Studies.

---

## 15. Latency-specific pitfalls

**Principle.** Latency is reported with median + tail percentiles +
the CDF, not the mean alone; warmup is discarded; coordinated
omission is corrected for in closed-loop benchmarks.

**Symptoms.**
- Latency summarized only by mean.
- No CDF plot.
- No mention of warmup discarding; or a discarded amount that is
  unjustified.
- Closed-loop benchmark with no mention of coordinated omission or
  intended dispatch time.
- Linear y-axis on a heavy-tailed quantity.

**Fix.** Replace mean-only summaries with median, $p_{95}$, $p_{99}$,
plus a CDF on log--log axes. Discard a warmup window; document its
size. For closed-loop benchmarks, measure latency relative to the
*intended* dispatch time, not the actual one. Tutorial:
§Latency-Specific Pitfalls.

---

## 16. Reporting and figure design

**Principle.** Figures use 95% CIs (not SE bars), log axes for
heavy-tailed quantities, captions that are self-contained, and the
right plot type for the data (CDF for distributions, box/violin for
distribution shape, points overlaid when $n \leq 40$).

**Symptoms.**
- Bar charts with SE error bars labeled or unlabeled.
- Linear axes on latency / inter-arrival times / energy distributions.
- Captions that say only "Performance comparison" with no $n$, no
  error-bar definition, no axis context.
- Bimodal data plotted as a bar (mean + SD) that hides both modes.
- Color-only encoding that fails greyscale or color-blindness checks.

**Fix.** Switch error bars to 95% CIs; use log axes where appropriate;
write captions that include $n$, the meaning of error bars, and the
context needed to read the figure without the body text. Use box or
violin plots when comparing distributions across few conditions; use
CDFs when distributions are heavy-tailed or the tail matters.
Tutorial: §Reporting and Figure Design.

---

## 17. Random seeds and non-determinism

**Principle.** All random sources are seeded; seeds are recorded in
the output; non-determinism that seeding cannot fix (GPU, parallel
scheduling) is acknowledged and budgeted for via more seeds.

**Symptoms.**
- No mention of random seeds anywhere.
- "We use seed 42" with $n = 1$ run.
- GPU-trained model with no acknowledgment of non-determinism, with
  cross-seed variance not reported.
- "Reproducibility is supported" claim with no released seeds or code.

**Fix.** Seed every random source, log seeds in the output, run 30+
seeds for stochastic experiments, acknowledge GPU non-determinism
where applicable. Tutorial: §Random Seeds and Determinism.

---

## 18. Sample size and power

**Principle.** The sample size ($n$ seeds, $n$ subjects, $n$ episodes)
is justified by a power calculation or rule of thumb appropriate to
the effect size and noise level.

**Symptoms.**
- "$n = 5$" with no justification on a noisy metric.
- Power "100%" claimed because all results are significant.
- Tail metrics ($p_{99}$) estimated from runs with $\leq 100$ samples
  per run.
- Effect-size-to-noise ratio not discussed; reader cannot tell whether
  $n$ is enough.

**Fix.** Run a small pilot (10 seeds), estimate per-seed standard
deviation $s$ and the smallest difference $\Delta$ you would care
about, compute $n \approx 8 / (\Delta/s)^2$ for $\alpha = 0.05$,
$\beta = 0.2$. State the calculation in the experimental setup.
Tutorial: §Sample Size and Power.

---

## 19. Time-correlated data and the block bootstrap

**Principle.** Time-series data (per-second throughput, per-packet
latency, queue occupancy) is summarized at the run level or
analyzed with a block bootstrap; standard CIs assume independence
that time-series violates.

**Symptoms.**
- Throughput sampled every second over a 1-hour run, treated as
  3,600 independent samples.
- CI computed from per-packet measurements within a single run.
- Block-bootstrap not used despite obvious autocorrelation in the
  data.

**Fix.** Summarize each run by one statistic (mean, $p_{99}$,
throughput), treat that as the unit of analysis (Cat 4); when
analyzing a within-run series, use the block bootstrap with block
length larger than the dominant autocorrelation timescale. Tutorial:
§Time-Correlated Data.

---

## 20. Simulation Verification and Validation (V&V)

**Principle.** Simulator-based papers run sanity checks (zero load
yields zero queueing), reproduce a known analytical or published
baseline, perform sensitivity analysis on parameters, verify
conservation laws, and use common random numbers across compared
policies for variance reduction.

**Symptoms.**
- Simulator-based headline numbers with no sanity check section.
- No comparison against an analytical baseline (M/M/1, simple TCP,
  etc.) where one is known.
- Parameter values not justified; no sensitivity analysis.
- Compared policies driven by *different* random sequences when
  same-seed paired comparison would be free.

**Fix.** Add a §Simulation Validation section with sanity checks,
baseline reproduction (e.g., M/M/1 mean queue length within X% of
analytical), sensitivity sweeps for the most sensitive parameters,
and conservation-law checks. Drive paired policies with common random
numbers (CRN). Tutorial: §Simulation Validation.

---

## 21. ML metrics matched to the task

**Principle.** The evaluation metric matches the task family and the
cost structure of errors. The right metric is more important than the
right test.

**Symptoms.**

By task:

- **Classification (imbalanced):** accuracy reported alone; no
  precision/recall, P--R curve, or AP.
- **Classification (rare events):** AUROC alone with no P--R AP.
- **Multi-class:** macro/micro $F_1$ unspecified; per-class
  performance hidden.
- **Regression:** $R^2$ only, no residual plot; or RMSE alone where
  MAE is more honest.
- **Probabilistic forecasts:** point-prediction metrics only, no
  scoring rule (log score, CRPS, calibration curve).
- **Language models:** BLEU on free-form generation tasks where it is
  known to correlate poorly; no perplexity on a held-out corpus; no
  contamination check.
- **Detection / segmentation:** IoU at one threshold only; no
  mAP\@[.5:.95].
- **Reinforcement learning:** mean return reported with no IQM, no
  per-seed variance, $\leq 5$ seeds.

**Fix.** For imbalanced classification add P--R curve and AP. For
regression add MAE and a residual plot. For LMs add perplexity and a
contamination check. For RL use IQM and stratified bootstrap CIs
across $\geq 30$ seeds. Tutorial: §A Note on Machine-Learning
Evaluations.

---

## 22. Reproducibility

**Principle.** A diligent reader can re-run the experiments with
reasonable effort: code, seeds, hardware, workloads, and
hyperparameters are documented or released.

**Symptoms.**
- No code release statement.
- No mention of hardware (CPU, GPU, RAM, OS).
- Hyperparameters listed as "tuned via grid search" with no grid
  specification.
- Workload generators or traces not described or not released.
- Pre-trained model used but not specified by hash or version.

**Fix.** Add a §Reproducibility paragraph stating the seeds, hardware,
hyperparameters, and code/data release. Aim for an artifact-evaluation
submission alongside the paper. Tutorial: §Reproducibility.

---

## 23. Equivalence and non-inferiority claims

**Principle.** Claims of "equivalent" or "no worse than" performance
are made via equivalence tests with a pre-specified margin, not by a
non-significant difference test. Failure to reject is not evidence of
no difference.

**Symptoms.**
- "We found no statistically significant difference, so the methods
  are equivalent."
- "Method A is no worse than Method B" with no equivalence margin.
- Non-inferiority claim made on the basis of overlapping CIs.

**Fix.** State an equivalence margin $\delta$ a-priori (e.g., "we
consider methods equivalent within 5% of mean latency"), and use a
two-one-sided-tests (TOST) procedure or check that the 90% CI on the
difference lies entirely within $[-\delta, \delta]$.

---

## 24. Primary vs. secondary metrics

**Principle.** The paper distinguishes one (or two) primary metrics
that the proposed method is expected to improve from secondary
metrics; statistical claims are concentrated on the primary; the
primary is selected before seeing results.

**Symptoms.**
- Five metrics reported; the paper highlights different ones in
  different parts of the paper depending on which favors the proposed
  method.
- Method optimizes for X; the paper's headline number is on Y, where
  the method happens to also win.
- "We additionally observe gains in <other metric>" with no a-priori
  reason that metric should improve.

**Fix.** Pre-register one primary metric and at most one or two
secondaries in the introduction. Concentrate hypothesis tests on the
primary; report secondaries descriptively. Acknowledge if the proposed
method does not improve the primary but improves a secondary.
