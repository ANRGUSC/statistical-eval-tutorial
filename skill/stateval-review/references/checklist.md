# Pre-submission checklist

Mirror of the tutorial's Appendix A (Pre-submission Checklist),
formatted as a flat list. Used in step 7 of the workflow as a
second-pass safety net. Each item maps to one or more categories in
`principles.md`; the category number is in parentheses for
cross-reference.

When using: for each item, mark whether the paper passes (`✓`),
fails (`✗`), or is not applicable (`—`). Failed items that did **not**
already produce a finding in step 4 should be added as findings at
Important severity.

- [ ] Hypothesis stated explicitly, in falsifiable form. (Cat 1)
- [ ] At least one strong baseline (not a strawman). (Cat 2)
- [ ] $\geq 10$ seeds per configuration; $\geq 30$ if the effect is small. (Cat 3)
- [ ] Trial order randomized; runs blocked on known confounders (machine, topology, time of day, channel, day). (Cat 4)
- [ ] One primary metric named a-priori; secondaries reported descriptively, including unfavorable ones. (Cat 5)
- [ ] Unit of analysis matches what was independently randomized; no pseudoreplication. (Cat 6)
- [ ] Variability reported via 95\% CIs, preferably bootstrap. (Cat 7)
- [ ] CI construction (bootstrap / $t$ / normal) matches the data. (Cat 8)
- [ ] CI on the per-pair difference reported for paired comparisons. (Cat 9)
- [ ] Paired non-parametric test used where the design allows; assumptions checked when parametric. (Cat 10)
- [ ] Effect sizes lead, with CIs on differences; $p$-value reported in support. (Cat 11)
- [ ] Regression results include residual diagnostics and CI on the slope. (Cat 12)
- [ ] At least two regimes evaluated; results reported per regime, not averaged; factorial sweep where interactions are plausible. (Cat 13)
- [ ] Multiple-comparison correction applied where many tests are reported. (Cat 14)
- [ ] Tradeoffs (cost, energy, memory, complexity) reported and Pareto fronts compared where the proposed method does not dominate everywhere. (Cat 15)
- [ ] Equivalence claims use a pre-specified margin and 90\%/95\% CI inclusion (or TOST); non-significant difference is not equivalence. (Cat 16)
- [ ] Held-out workloads or conditions used for headline numbers; test set touched once. (Cat 17)
- [ ] Ablation table for multi-component methods, with same seeds and CIs as the headline. (Cat 18)
- [ ] Latency reported with median + tail percentiles + CDF; warmup discarded; coordinated omission addressed. (Cat 19)
- [ ] Error bars are 95\% CIs, not SE or SD; captions self-contained; log axes for heavy tails; box/violin where appropriate. (Cat 20)
- [ ] Seeds, hardware, code, and workload generators released or described. (Cat 21, 27)
- [ ] Sample size and power justified, not assumed. (Cat 22)
- [ ] Exclusion criteria pre-declared, counts reported, with-and-without comparison shown if exclusions move the headline. (Cat 23)
- [ ] Time-correlated data summarized at run level or analyzed with block bootstrap. (Cat 24)
- [ ] Simulator passes both verification (sanity, conservation) and validation (baseline reproduction, sensitivity, scope statement) checks; common random numbers used safely. (Cat 25)
- [ ] ML splits respect the unit of analysis (grouped, temporal, nested CV); metrics matched to task family (P--R/AP for imbalanced classification; perplexity for LMs; IQM for RL; etc.). (Cat 26)
- [ ] Where the method does *not* help is stated explicitly. (Cat 1, Cat 13)
