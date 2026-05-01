# Pre-submission checklist

Mirror of the tutorial's Appendix A, formatted as a flat list. Used in
step 7 of the workflow as a second-pass safety net. Each item maps to
one of the 24 categories in `principles.md`; the category number is
in parentheses for cross-reference.

When using: for each item, mark whether the paper passes (`✓`),
fails (`✗`), or is not applicable (`—`). Failed items that did **not**
already produce a finding in step 4 should be added as findings at
Important severity.

- [ ] Hypothesis stated explicitly, in falsifiable form. (Cat 1)
- [ ] At least one strong baseline (not a strawman). (Cat 2)
- [ ] $\geq 10$ seeds per configuration; $\geq 30$ if the effect is small. (Cat 3)
- [ ] Unit of analysis matches what was independently randomized; no pseudoreplication. (Cat 4)
- [ ] Variability reported via 95% CIs, preferably bootstrap. (Cat 5)
- [ ] CI on the per-pair difference reported for paired comparisons. (Cat 6)
- [ ] CI construction matches the data (bootstrap / $t$ / normal). (Cat 7)
- [ ] Paired non-parametric test used where the design allows; assumptions checked when parametric. (Cat 8)
- [ ] Effect sizes reported alongside $p$-values, with CIs on differences. (Cat 9)
- [ ] Regression results include residual diagnostics and CI on the slope. (Cat 10)
- [ ] At least two regimes evaluated; results reported per regime, not averaged. (Cat 11)
- [ ] Multiple-comparison correction applied where many tests are reported. (Cat 12)
- [ ] Out-of-sample / held-out conditions used for headline numbers. (Cat 13)
- [ ] Ablation table for multi-component methods, with CIs. (Cat 14)
- [ ] Latency reported with median + tail percentiles + CDF; warmup discarded; coordinated omission addressed. (Cat 15)
- [ ] Error bars are 95% CIs, not SE or SD; captions self-contained; log axes for heavy tails; box/violin where appropriate. (Cat 16)
- [ ] Seeds, hardware, code, and workload generators released or described. (Cat 17, 22)
- [ ] Sample size and power justified, not assumed. (Cat 18)
- [ ] Time-correlated data summarized at run level or analyzed with block bootstrap. (Cat 19)
- [ ] Simulator passes sanity checks, baseline reproduction, sensitivity, conservation; common random numbers used. (Cat 20)
- [ ] ML metrics matched to task family (P--R/AP for imbalanced classification; perplexity for LMs; IQM for RL; etc.). (Cat 21)
- [ ] Equivalence claims use a pre-specified margin and TOST or equivalent; non-significant difference is not equivalence. (Cat 23)
- [ ] One primary metric named a-priori; secondaries reported descriptively. (Cat 24)
- [ ] Where the method does *not* help is stated explicitly. (Cat 1, Cat 11)
