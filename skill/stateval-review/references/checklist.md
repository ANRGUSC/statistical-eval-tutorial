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
- [ ] Variability reported via 95% CIs, preferably bootstrap. (Cat 7)
- [ ] Paired non-parametric test used where the design allows. (Cat 10)
- [ ] Effect sizes reported alongside $p$-values, with CIs on differences. (Cat 11)
- [ ] At least two regimes evaluated; results reported per regime, not averaged. (Cat 13)
- [ ] Where the method does *not* help is stated explicitly. (Cat 1, Cat 13)
- [ ] Multiple-comparison correction applied where many tests are reported. (Cat 14)
- [ ] Latency reported with median + tail percentiles + CDF; warmup discarded. (Cat 19)
- [ ] Error bars are 95% CIs, not SE or SD; captions self-contained. (Cat 20)
- [ ] Held-out workloads or conditions for out-of-sample validation. (Cat 17)
- [ ] Simulator passes sanity checks, baseline reproduction, sensitivity, conservation. (Cat 25)
- [ ] Common random numbers used to pair runs across policies. (Cat 25)
- [ ] Seeds, hardware, code, and workload generators released or described. (Cat 27)
