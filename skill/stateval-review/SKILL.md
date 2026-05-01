---
name: stateval-review
description: Audit a student paper draft for statistical evaluation quality and produce a prioritized, quote-and-suggest review document grounded in the Krishnamachari statistical-evaluation tutorial. Use when the user asks to "review my paper from a stats perspective", "audit my evaluation", "stateval review", or invokes /stateval-review with a paper path. Covers statistical validity, experimental design, hypothesis quality, ablation studies, presentation, reporting, and reproducibility.
allowed-tools: Read Grep Glob AskUserQuestion Write Bash
---

# stateval-review

Produce a structured review of a student's experimental paper draft against
the principles of the Krishnamachari *How to Do Statistical Evaluations in
ECE/CS Papers* tutorial. Output is one markdown file the student can read
and act on.

The skill **does not edit the student's paper.** It writes a separate
review document at `stateval-review.md` in the user's current working
directory.

## Workflow

Follow these eight steps in order.

### 1. Locate the paper

Resolve the paper to audit:

- If the user passed a path argument (e.g. `/stateval-review paper.tex` or
  `/stateval-review /path/to/draft.pdf`), use it directly.
- Otherwise, glob the current directory for candidate files:
  ```
  Glob: *.tex, *.pdf
  ```
  - If exactly one match, use it.
  - If multiple matches, use `AskUserQuestion` to ask which to audit.
    Provide the candidate paths as options.
  - If zero matches, tell the user no candidate file was found and ask
    them to provide a path.

Record the resolved path; refer to the file by its basename in the output.

### 2. Read the paper

Read the file with the `Read` tool.

- For `.tex`: read the full file (LaTeX source is small).
- For `.pdf` ≤ 10 pages: read the whole PDF.
- For `.pdf` > 10 pages: read in passes prioritizing the sections most
  likely to expose statistical-evaluation issues:
  1. Pages 1–3 (abstract, intro)
  2. The evaluation/results/experiments section (search the table of
     contents or skim for it; if not findable, read the middle third)
  3. The conclusion (last 2 pages)
  4. Any explicit "Ablation" section
  Use the `pages` parameter for targeted reads. Skip related-work and
  background sections unless time permits.

For large papers, **do not** try to load every page into context at once.
Take notes on each pass.

### 3. Detect paper type

Load `references/paper-types.md`. Apply the heuristics there to classify
the paper as one of:

- `systems` — networking, OS, distributed systems, latency/throughput metrics
- `applied-ml` — training models, classification/regression/RL/LLMs
- `theory-with-experiments` — proofs plus a small numerical-results section
- `hardware-or-embedded` — circuits, sensors, energy
- `hybrid` — combinations of the above

Record the type and pull the per-type filter (which of the 24 audit
categories apply to this paper). Theory papers skip latency/seeds/correlated;
ML papers prioritize the metrics audit; pure simulator papers must hit
sim-validation.

### 4. Audit category by category

Load `references/principles.md`. For each applicable category, scan the
paper for the listed symptoms and record findings.

A finding has four parts:

```
{
  category: "<category number and name>",
  severity: "Critical" | "Important" | "Nice-to-have",
  quote: "<short verbatim excerpt from the paper, max ~30 words>",
  symptom: "<what is wrong, in one sentence>",
  fix: "<concrete, actionable suggestion, in one sentence>",
  tutorial_ref: "§<section name>"
}
```

Rules for findings:

- **Quote-and-suggest, never abstract.** Every finding must include a
  verbatim excerpt from the paper. If you cannot quote the paper, you
  cannot file the finding.
- **Specific fixes only.** Not "report variability" but "report a 95%
  bootstrap CI on the per-seed mean of the headline metric, computed via
  `scipy.stats.bootstrap`."
- **Severity:**
  - **Critical** — the paper makes a claim its evidence cannot support
    (e.g., headline number with no variability; "X is better" with one
    seed).
  - **Important** — the paper's argument is weakened but not broken
    (e.g., uses a $t$-test on heavy-tailed data without checking
    normality; missing ablation for a multi-component method).
  - **Nice-to-have** — improves polish (e.g., bar chart should be a CDF;
    captions could be more self-contained).

### 5. Prioritize and dedupe

After scanning all categories:

- Cap the findings list at **20 total**. If more, drop Nice-to-have first,
  then Important, until ≤ 20.
- Merge near-duplicate findings (e.g., two "no CI" hits become one).
- If the paper is short or already strong, fewer than 20 findings is
  expected and correct. Do not invent issues to fill the count.

### 6. Identify what the paper already does well

List 3–5 strengths. These come from the same audit categories — the
paper *does* state a falsifiable hypothesis, *does* use paired tests,
*does* report effect size, etc. Ground each strength in a specific
section reference or quote, just like findings.

This section comes **first** in the output. A review that leads with
criticism alone is correctly distrusted by students.

### 7. Cross-check against the checklist

Load `references/checklist.md`. For each checklist item, mark whether
the paper passes (`✓`), fails (`✗`), or is not applicable (`—`). The
checklist is the second-pass safety net: it catches things the
category audit missed.

If a checklist item failed but produced no finding in step 4, add a
finding for it at Important severity.

### 8. Write the review and report

Load `references/output-template.md` for the exact format. Write the
review to `stateval-review.md` in the user's cwd (use `Write`). The
file structure is:

1. Title and metadata (paper file, paper type, date)
2. Two-paragraph summary (what the paper claims; the top concern)
3. **What this paper already does well** (3–5 strengths)
4. **Findings** by severity tier
5. **Suggested next 3 actions** (the highest-leverage fixes)
6. **Checklist results** (the pass/fail/NA grid from step 7)
7. **Tutorial reference index** (links to the relevant tutorial sections)

Then print a **5-line summary in chat**:

```
Reviewed: <basename>
Paper type: <type>
Top strength: <one line>
Top concern: <one line>
Findings: <N> Critical, <N> Important, <N> Nice-to-have
Written to: stateval-review.md
```

Do not paste the full review into chat. The student reads it from the
file.

## Behavioral guidance

- **Lead with what to do, not what is wrong.** Each finding's `fix` is
  the most important field. The `symptom` exists to motivate the fix.
- **Quote sparingly.** Excerpts ≤ 30 words. Long quotes obscure the
  point.
- **Stay in scope.** This skill audits statistical evaluation,
  experimental design, presentation, hypothesis quality, ablation, and
  reproducibility. It does **not** review writing style, claims of
  novelty, theoretical contribution, or related-work coverage. If asked,
  point the user to other tools.
- **No hedging.** Once a finding is logged, state the symptom and fix
  directly. Do not pad with "you might want to consider" — the student
  invoked the skill to get an opinion.
- **Tutorial pointers, not lectures.** The fix points to the tutorial
  section that explains the technique. The skill itself does not teach
  the technique; the tutorial does that.
- **One finding per problem.** If the paper has no CIs anywhere, file
  one finding ("no variability reporting") rather than one per arm.

## When the audit cannot proceed

Return a clear error and stop:

- The candidate file is not readable or is binary in an unexpected
  format (e.g., `.docx`).
- The PDF is encrypted or has no extractable text.
- The paper is clearly not an experimental paper (e.g., a survey, a
  position paper, a magazine article). The skill does not apply to
  these; report the type and decline.

## Files

- `references/principles.md` — the 24-category audit knowledge base.
  Loaded in step 4. Contains principle / symptoms / fix for each.
- `references/paper-types.md` — type-detection heuristics and per-type
  category filters. Loaded in step 3.
- `references/output-template.md` — exact markdown format for
  `stateval-review.md`. Loaded in step 8.
- `references/checklist.md` — flat pre-submission checklist mirroring
  the tutorial's Appendix A. Loaded in step 7.
