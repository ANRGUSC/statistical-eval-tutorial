# Output template for `stateval-review.md`

The skill writes a single markdown file in this format. Use the
structure literally; replace the `<...>` placeholders.

```markdown
# Statistical Evaluation Review: <paper basename>

**Paper file:** `<path>`
**Paper type:** <systems / applied-ml / theory-with-experiments / hardware-or-embedded / hybrid>
**Reviewed:** <YYYY-MM-DD>
**Reference:** Krishnamachari, *How to Do Statistical Evaluations in ECE/CS Papers*

## Summary

<One paragraph: what the paper claims and what evidence it provides.>

<One paragraph: the top concern in the evaluation, and what fixing it
would buy.>

## What this paper already does well

- **<short title>** (§<tutorial section>) — <one sentence; quote the
  paper if it sharpens the point>.
- **<short title>** (§<tutorial section>) — <one sentence>.
- **<short title>** (§<tutorial section>) — <one sentence>.
<3–5 strengths total.>

## Findings

### Critical (must address)

#### 1. <short title> (Cat <N>; tutorial §<section>)

> <verbatim excerpt from the paper, ≤ 30 words>

**Symptom.** <one sentence: what is wrong>.

**Fix.** <one sentence: a concrete, actionable change>.

#### 2. ...

### Important

#### N. <short title> (Cat <N>; tutorial §<section>)

> <quote>

**Symptom.** <...>

**Fix.** <...>

### Nice to have

#### N. <short title> (Cat <N>; tutorial §<section>)

> <quote>

**Symptom.** <...>

**Fix.** <...>

## Suggested next 3 actions

The highest-leverage things to do first, in order:

1. <one sentence pointing at a specific finding above>.
2. <...>.
3. <...>.

## Pre-submission checklist results

| # | Item | Status |
|---|------|--------|
| 1 | Hypothesis stated explicitly, in falsifiable form | ✓ / ✗ / — |
| 2 | At least one strong baseline (not a strawman) | ✓ / ✗ / — |
| ... | ... | ... |

(Mirror every item from `references/checklist.md`. ✓ = the paper
addresses it; ✗ = it does not; — = not applicable.)

## Tutorial reference index

The tutorial sections most relevant to the findings above:

- §<section> — <one-line description of why this is relevant>.
- §<section> — <...>.

(One bullet per tutorial section that produced a finding. Helps the
student go straight to the right part of the tutorial.)
```

## Style rules for the produced review

- **Verbatim quotes.** Quote what the paper actually says. Paraphrasing
  in a quote block is forbidden.
- **Length cap.** ≤ 30 words per quote; ≤ 1 sentence per
  symptom/fix/strength entry.
- **No filler.** No "this is a great paper but…" preambles. Lead with
  the strengths section, then the findings.
- **No nesting beyond two levels.** Severity tier → finding. Findings
  do not contain sub-findings.
- **Categories are numbered.** Always cite the category number from
  `principles.md` so the student can look up the canonical principle.
- **Tutorial section references** are by section name (e.g.,
  "§Variability and Confidence Intervals"), not by section number,
  because section numbering may drift between tutorial revisions.
- **Severity tiers are sorted** Critical → Important → Nice-to-have.
  Within a tier, sort by category number.
