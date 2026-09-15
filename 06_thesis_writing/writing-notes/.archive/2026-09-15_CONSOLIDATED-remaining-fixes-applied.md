---
name: 2026-09-15_BRANCH_A_CONSOLIDATED-remaining-fixes
description: CONSOLIDATED - Every outstanding fix from seventeen audited writing notes, in one document. Each verified against the current snapshot. Fifteen chapter fixes, six of them one-word, plus the style sweep and three optional additions.
category: workflow
applies-to: [ch1_introduction, ch2_literature_review, ch3_methodology, ch6_architecture, all chapters]
triggers: [remaining fixes, consolidated, what is left, submission]
created: 2026_09_15-11_40
updated: 2026_09_15-11_40
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Everything still to apply, in one document

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`
— 46,465 words, 8 comment threads. Zotero: 92 items.

**Seventeen notes audited end to end against this snapshot.** Nine were already
applied or are reference material. **This document carries everything that
remains.**

⚠ **Every fix below was re-verified by me against the snapshot**, not taken on
report. Where a line number is given it is the snapshot's, and the quoted text is
verbatim.

---

# Read this first — six one-word fixes, fifteen minutes

**These are the highest-value edits in the document, because each is a
self-contradiction an assessor can catch on one page.**

| # | Site | Change | Why it matters |
|---|---|---|---|
| **1** | Ch1 §1.4 | `8 gigabytes` → **`4 gigabytes`** | ⚠ **§1.1 of the same chapter already says four** |
| **2** | Ch1 §1.4 | `five-category` → **`four-category`** | ⚠ **§1.4, eight lines above, excludes beer explicitly** |
| **3** | Ch1 §1.5 | `nine chapters` → **`ten chapters`** | the list beneath it has ten entries |
| **4** | Ch2 §2.3 | `Chapter 6` → **`Chapter 5`** | Ch5/Ch6 swapped on 2026-09-08 |
| **5** | Ch2 §2.5 | `Chapter 6` → **`Chapter 5`** | same |
| **6** | Ch3 §3.6 | `all five forecasting models` → **`all six forecasting models`** | ⚠ **§3.5.1 enumerates six, and Ch5 has six subsections** |

---

# F1 — Ch1 §1.4, the RAM budget

### Anchor

**Chapter 1, Section 1.4**, the paragraph beginning **"Computational
constraint."** Verbatim:

> "**Computational constraint.** The framework is constrained to a maximum of 8 gigabytes of total RAM across all simultaneously active components."

### Action

REWORD — `8` → `4`. Nothing else changes.

**After:**
> "**Computational constraint.** The framework is constrained to a maximum of 4
> gigabytes of total RAM across all simultaneously active components."

### Note — this is the last holdout

✅ **Verified: every other site says four.** Ch1 §1.1 (*"a ceiling of
approximately four gigabytes"*), Ch2, Ch3 §3.6 and §3.7, Ch5, Ch6, Ch9, Ch10, and
the abstract (*"a four-gigabyte ceiling"*).

⚠ **Chapter 1 currently contradicts itself within one chapter** — §1.1 says four,
§1.4 says eight. This was S32 and C1 in the cross-chapter note.

---

# F2 — Ch1 §1.4, the category count

### Anchor

**Chapter 1, Section 1.4**, the paragraph beginning **"Generalisability."**
Verbatim:

> "While the five-category benchmark provides evidence on whether the modelling findings hold across heterogeneous beverage categories"

### Action

REWORD — `five-category` → `four-category`.

### Note

⚠ **§1.4 already excludes beer explicitly, eight lines above this sentence.** The
thesis ships four categories: CSD, Danskvand, Energidrikke, RTD.

---

# F3 — Ch1 §1.5, the chapter count

### Anchor

**Chapter 1, Section 1.5**, the opening sentence. Verbatim:

> "The remainder of this thesis is organised into nine chapters, each corresponding to a phase of the Design Science Research process (Peffers et al., 2007)."

### Action

REWORD — `nine` → `ten`.

### Note

✅ **The per-chapter entries beneath it are already correct** (Ch5 benchmark, Ch6
architecture, Ch7 interface). Only the count is stale.

---

# F4 and F5 — Ch2's two stale chapter references

⚠ **I initially doubted these and was wrong.** My first spot-check truncated the
lines before reaching the reference; a full read confirms both. **Both are real.**

## F4 — §2.3

### Anchor

**Chapter 2, Section 2.3.** The sentence containing:

> "Chapter 6 encounters and documents the same problem on the Nielsen panel."

### Action

REWORD — `Chapter 6` → `Chapter 5`.

## F5 — §2.5

### Anchor

**Chapter 2, Section 2.5**, in the conformal-prediction paragraph:

> "Chapter 6 accordingly measures coverage empirically on a held-out test period"

### Action

REWORD — `Chapter 6` → `Chapter 5`.

### Note — do not touch the others

✅ **Verified correct, leave alone:** Ch2's references to Chapter 4, Chapter 5 and
Chapter 3 all point where they should. Only these two are stale from the
2026-09-08 swap.

---

# F6 — Ch3 §3.6, five versus six models ⚠ NEW FINDING

**No note predicted this. It surfaced during the audit.**

### Anchor

**Chapter 3, Section 3.6 Validity and Reliability**, the paragraph beginning
**"Internal validity is maintained through three design choices."** Verbatim:

> "First, a common percentual  train-test split is applied identically across all five forecasting models, ensuring that performance differences reflect model characteristics rather than differences in the data each model observes."

⚠ **Note the double space in "percentual  train-test"** — it is in the document
and makes the string findable.

### Action

REWORD — `all five forecasting models` → `all six forecasting models`.

### Note — six is correct, verified twice

✅ **Ch3 §3.5.1 enumerates six:** *"Six model families are evaluated… ARIMA and
Prophet as classical statistical methods, LightGBM and XGBoost as gradient-boosted
ensembles, Ridge regression as a regularised linear baseline, and a set of
parameter-free benchmarks."*

✅ **Ch5 §5.2 has six subsections:** simple benchmarks, ARIMA, Prophet, LightGBM,
XGBoost, Ridge.

**The "five" is the error.** Fixing the other direction would contradict both.

---

# F7 — Ch6 §6.2, a cross-reference pointing at the wrong chapter ⚠ NEW

**The audit flagged this as unverifiable. I verified it: it is wrong.**

### Anchor

**Chapter 6, Section 6.2 Architectural Overview.** Verbatim:

> "that production substrate is the object of the integration-readiness assessment (SRQ3, Section 5.6), not the evaluated implementation"

### Action

REWORD — `Section 5.6` → `Section 6.6`.

### Note

✅ **SRQ3 integration readiness is §6.6 — in the same chapter.** Ch5 §5.6 is part
of the model benchmark and has nothing to do with integration readiness. Another
casualty of the Ch5/Ch6 swap.

---

# F8 — Ch2 §2.8, the hedging lead-in

### Anchor

**Chapter 2, Section 2.8 Contributions**, the sentence introducing the four
contributions. Verbatim:

> "This thesis addresses that intersection through four contributions, stated at the level of the system class rather than any single product, and distinguishing what is designed from what is planned for evaluation or left to future work:"

### Action

REWORD — delete the final clause.

**After:**
> "This thesis addresses that intersection through four contributions, stated at
> the level of the system class rather than any single product:"

### Note

✅ **The four `designed; pending` status labels beneath this sentence are already
gone.** This lead-in is the last survivor, and it now promises a distinction the
list no longer makes.

⚠ **Related, and yours to judge — §2.8's closing sentence:** *"Empirical
calibration of uncertainty and full-scale evaluation are identified as directions
for further work rather than completed results."* **Partly overtaken**: the
evaluation landed (63 funded runs), the calibration result is reported in Ch5 and
Ch7 as a negative finding, but neither was *full-scale*. **NEEDS-BRIAN** — I would
reword to *"Full-scale evaluation across organisations remains a direction for
further work"*, but the call is yours.

---

# F9 — Ch3 §3.6, the temperature contradiction

**Written up in full as its own note** —
`ch3_methodology/2026-09-15_BRANCH_A_ch3-temperature-contradiction.md`. Summarised
here so nothing is missed.

⚠ **§3.6 says *"outputs at temperature zero are highly reproducible"*, ten lines
after §3.5.4 correctly states decoding is not adjustable on this model.** Same
false claim I removed from `export_appendix.py` this session.

**One sentence reworded; the surrounding argument gets stronger.** See that note
for the before/after.

---

# The style sweep — not run

`2026-09-14_BRANCH_A_watermark-patterns-to-remove.md` is **reference material, and
its sweep has not been run.** Both sentences it was written to fix are still
verbatim in the document.

| Pattern | State |
|---|---|
| **P1** colon-led elaboration | ⚠ present throughout. The note's own exemplar survives at Ch3 §3.1: *"This stance has practical methodological implications: it motivates careful data quality assessment"* |
| **P2** not-X-but-Y | ⚠ **3 instances.** The note's exemplar survives at Ch3 §3.1: *"is not incidental; it reflects the deliberate choice"*. Also Ch4: *"The retention threshold is not chosen; it is derived."* |
| **P4** hedge stack | ✅ **clean — zero instances** |
| **P5** summarising restatement | 1 candidate, Ch5: *"This is precisely the outcome the benchmark rung exists to detect."* |
| **P6** em-dash density | ⚠ **not measurable in the snapshot** — it renders em dashes as hyphens. **Count in Word.** |

⚠ **A raw count of colon-led sentences is an upper bound, not a defect count** —
legitimate list and quotation colons match the same pattern. **Do not batch-replace.**
Word threads 67 and 68 (Ch3) are the two the note was written from.

**This is a read-through task on a locked document, best done last.**

---

# Three optional additions — none is a defect

**Each is content a reference note recommends that never reached the prose. All
are additions, not corrections.** ⚠ **With the deadline at 14:00, treat these as
optional.**

### A — the leakage boundary (Ch3 §3.5.4) — **the strongest of the three**

`ch3_methodology/srq4-data-input-is-a-constructed-choice.md` records that §3.5.4
says nothing about what data the scenarios receive, or how the held-out period was
protected.

⚠ **A methodology chapter silent on leakage protection invites the question
immediately — and here the answer is good.** If you add one thing from this
section, add this:

> "Each scenario receives the brand's monthly series as it leaves the warehouse
> after joining and aggregation, and nothing further: cleaning, imputation and
> feature construction are withheld deliberately, because they are the pipeline
> under evaluation. The visible window ends at the same origin the served model is
> fitted to, and the cut is applied when the file is written rather than when it
> is read, so that no downstream consumer can reintroduce what it removes."

### B — harness verification (Ch3 §3.6)

`ch3_methodology/verification-of-the-experimental-harness.md` recommends stating
that the harness has pre-flight checks, a smoke run and a printed dry run, and
that **there is no test coverage over the experiment harness** — *"a weaker
guarantee than unit tests and a stronger one than nothing."*

✅ **Honest, and it is a rigour argument currently unclaimed.** Optional.

### C — the SKU-to-brand aggregation limitation

`ch8_experiment/the-agent-input-contract.md` flags that the aggregation from SKU
to brand level is never stated as a limitation. One sentence in Ch3 §3.7 or Ch9
§9.4. Optional.

---

# What the audit found already applied — nine notes

**No action needed on any of these. Recorded so nobody re-derives them.**

| Note | State |
|---|---|
| `ch5-profiling-rerun.md` | ✅ **fully applied** — Ch5 §5.5.6 carries 31.9/14.9/2.0/1.6 MB and the eighteen-feature disclaimer |
| `ch4-followup-02-exogenous-consistency.md` | ✅ **fully applied** — §4.1.3 verbatim as specified; the stale footnote deleted, not relocated |
| `cross-chapter-flow…md` | 5 of 9 applied — the rest are F1–F5 and F8 above |
| **7 × `ch8_experiment/*.md`** | ✅ **reference material — no anchors, no actions, nothing to apply.** Their content reached the prose |
| `verification-of-the-experimental-harness.md` | reference — see optional B |
| `srq4-data-input-is-a-constructed-choice.md` | reference — see optional A |

⚠ **Hazard if you reuse `ch8_experiment/srq4-experiment-design-rationale.md`:** its
arm lettering runs **backwards** (A = trained model). The thesis runs **A = no firm
data, B = data and code, C = dedicated model**. Re-map before reading.

⚠ **Standing trap from `ch5-profiling-rerun.md`:** four stale artefacts —
`param_drift.csv`, `refit_vs_retune.csv`, `retune_single_cutoff.csv`,
`sandbox_profiling.csv`. **Do not cite these without regenerating.**

---

# The order I would work in

| | Item | Time |
|---|---|---|
| **1** | **F1–F8**, the eight chapter fixes above | ~20 min |
| **2** | **F9**, the temperature reword | 2 min |
| **3** | The eight comment threads — `2026-09-15_BRANCH_A_final-eight-threads.md` | ~15 min |
| **4** | Appendix regeneration (in flight) | — |
| **5** | In-text citations → Zotero fields, **then** the dynamic list | long pole |
| **6** | The style sweep, on a locked document | last |
| **7** | `/submission-export` | last |

**Items 1, 2 and 3 are forty minutes of work and close every self-contradiction in
the document.**
