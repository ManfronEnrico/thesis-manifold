---
name: ch7-verification-pass
description: NOTE - The single Chapter 7 document. Section-by-section verification against the code and the regenerated artefacts, with the confidence-index decision and the payload-behaviour evidence folded in. Ten fixes, six comment verdicts, one table-numbering collision affecting every chapter from 8 onward.
category: workflow
applies-to: [chapter 7]
snapshot: 2026-09-12_16-21_ch7-verification-pass
created: 2026_09_12-16_45
updated: 2026_09_12-16_45
status: open
---

# Chapter 7 — verification pass

Verified at `693c5e1`, fetch clean, 0 ahead / 0 behind. Zotero re-pulled
2026-09-12 16:22: **89 items**, up from 86 at the last pull. Snapshot
`2026-09-12_16-21_ch7-verification-pass`. Chapter 7 is **unchanged at 5,184
words** since the previous snapshot, so every anchor below is current.

**This is the single Chapter 7 document.** Two earlier notes are folded in
whole and archived, so nothing in this folder contradicts anything else:

| Folded in | State when folded | Where it now lives |
|---|---|---|
| `ch7-confidence-index-decision.md` | not applied; three coverage figures stale; one whole section obsolete | Fix 4, and **Part 2** below |
| `the-payload-changed-behaviour.md` | not applied, correctly — nothing is funded | **Part 3** below, re-verified |

⚠ **Both were re-verified against the current artefacts before folding, not
copied.** What changed is recorded in each part.

**Artefact recency.** Every number cited below comes from an artefact written
**after** the 2026-09-09 21:10 training cutoff:

| Artefact | Written | Used for |
|---|---|---|
| `calibration.csv` / `.md` | 2026-09-11 17:16 | Table 18, and the 7.4 prose |
| `profiling.csv` | 2026-09-11 18:37 | the memory claim in 7.6 |
| `smoke/runs.csv` | 2026-09-11 21:07 | latency, tokens and cost in 7.6 |
| `models/index.json` | 2026-09-09 21:10 | the confidence index values |

---

# What the chapter already gets right

Stated first because most of the chapter verifies clean, and a note that lists
only defects misrepresents it.

- **Both substantive citations resolve and point the right way.** Goodwin, Önkal
  and Thomson (2010) is in the library, and its abstract states the intervals
  "did not improve the quality of the decisions and also reduced the propensity
  of the decision makers to respond appropriately to the asymmetry in the loss
  function". The chapter uses it in two places and both are faithful. Lei et al.
  (2018) and Barber et al. (2023) also resolve.
- **The confidence-index diagnosis in 7.4 is exactly right**, and I recomputed it
  independently from the served metadata: CSD 5.9, Danskvand 5.8, Energidrikke
  3.2, RTD 6.7, against a Low/Moderate cut at 40. "Between three and seven" and
  "the index distinguishes nothing" are both correct.
- **The four scoring criteria in 7.3 match the scorer exactly** — states an
  interval, bounds match within five per cent, states confidence, gives a
  recommendation.
- **The prompt-hash claim verifies.** SHA-256 over every string that reaches the
  model.
- **The refit-per-call figure verifies.** The tool's own header records ~1.1 s,
  which the chapter renders as "approximately one second".

---

# The fixes

## Fix 1 — Section 7.6 is not prose, and every number in it is falsified

The section is four raw bullets plus a paragraph from a superseded protocol.
Brian's two comments on it (VERIFY, PROSE, OUTDATED, INTERNALREFERENCES) are
both correct, and the measurements are now available to replace it.

**Every claim in the bullets is wrong against measurement:**

| The bullet says | Measured | Source |
|---|---|---|
| ~1–3 s per request | **7.2 s** mean | `smoke/runs.csv`, arm C, two runs |
| ~500–1000 input tokens | **1,034** | same |
| ~100–200 output tokens | 130 | same |
| synthesis step RAM <50 MB | **0.03–0.47 MB** peak predict RSS | `profiling.csv` |
| `claude-sonnet-4-6` | **`gpt-5.5-2026-04-23`** | `srq4_experiment.py:168` |
| GPT-4o judge | **no judge** | `score_interval_communication.py:38` |
| temp 0 | **not settable** | `srq4_experiment.py:177` |
| N=50 | not the design | — |

⚠ **The 50 MB figure is the one traced last night**: it is a July
pre-measurement estimate, roughly 9x too high even for the largest model's fit,
and about 100x too high for the prediction path the interface actually runs.

### Anchor

**Section 7.6 Operating within bounded cost, latency and memory.** The whole
section, from the bulleted line beginning *"LLM API call: ~1–3 seconds per
synthesis request"* through to the end of the paragraph ending *"...trade-off
are in Ch8 §8.3.4."*

### Action

REPLACE the entire section body.

#### Replace with

> The interface was designed against a memory ceiling rather than a latency or
> cost target, because the deployment it extends runs on a small-business cloud
> instance. That constraint is met by a wide margin, and the margin is worth
> stating precisely: serving a forecast loads a persisted model and calls
> predict, and the peak resident memory of that path is under half a megabyte
> for every model family benchmarked. The fitting path, which the serving
> interface never executes, peaks between 1.6 and 31.9 megabytes. No language
> model is loaded locally at any point, so the generative component contributes
> no resident memory of its own.
>
> Latency and cost are properties of the exchange rather than of the interface,
> and both are dominated by the language model rather than by the forecast. A
> tool-backed answer completes in roughly seven seconds and consumes on the
> order of one thousand input and one hundred and thirty output tokens, at a cost
> of under one cent. These figures are measured on the pilot runs and are
> reported here to establish the order of magnitude; the comparison across
> scenarios, where the differences are substantial, belongs to Chapter 8.
>
> The relationship between the three quantities is the point rather than any one
> of them. The memory ceiling that motivated the whole substrate is not the
> binding constraint on the delivered system, because the expensive component is
> the one that runs elsewhere and is billed by the token.

### Note — why the old paragraph cannot be repaired

It describes a **five-dimension LLM-judged comparison against a rule-based
baseline** that no longer exists in the design. The judge was removed, the model
changed, and temperature 0 is rejected by the current model with HTTP 400. There
is nothing to update; the study it reports was not run in the form described.

⚠ The cross-reference *"Ch8 §8.3.4"* also uses the section symbol, which the
project does not use, and points at a numbered subsection that may not survive.

---

## Fix 2 — Table numbering collides with Chapter 6, and shifts everything from Chapter 8 on

⚠ **This is the largest finding in the pass and it is not confined to Chapter 7.**

Chapter 6 and Chapter 7 both number their tables **17, 18 and 19**. Chapter 8
resumes at 20.

| Chapter | Table numbers used |
|---|---|
| Ch5 | 5–16 |
| Ch6 | **17, 18, 19** |
| **Ch7** | **17, 18, 19** ← collision |
| Ch8 | 20, 21, 22 |
| Ch9 | 23 |

Chapter 7's three tables are therefore **absent from the global sequence**, and
every table number from Chapter 8 onward is understated by three.

**The cause is mechanical.** Chapters 5, 6 and 8 carry their numbers as Word
field references, which renumber automatically. Chapter 7's are **typed as plain
text**, so they did not move when Chapter 6 gained its seventh-arm table.

### Action

NEEDS-BRIAN, and it is a Word operation rather than a paste. Chapter 7's three
captions and their in-text callouts must become field references like the
surrounding chapters', after which Word renumbers Chapters 8 and 9 on its own.

⚠ **Do this before any further table is added anywhere**, because each new table
widens the offset.

### Note — a second, smaller numbering defect inside Chapter 7

Independent of the collision, **the chapter contradicts itself**. Section 7.2.2
says the payload groups are *"summarised in Table 18"*, and the caption directly
beneath that table reads ***Table 17***. One of the two is wrong regardless of
how the global sequence resolves.

---

## Fix 3 — The synthesis engine described in 7.2.2 no longer exists

Section 7.2.2 states, in the present tense, that a second composite confidence
score *"exists in this work, produced by the deterministic synthesis engine
described below"*.

⚠ **Two problems, and the second is worse than the first.**

1. **Nothing is described below.** No later section describes a synthesis engine,
   so the forward reference has no referent.
2. **The engine is archived.** `srq2_synthesis.py` exists only under two
   `.archive/` folders, both retired 2026-08-19. `PATHS.py:368` states plainly
   that it "no longer exists as live code". Nothing in the live tool or the
   experiment harness imports it. The only live mentions are in two module
   headers, both listing it as one of three **defects that motivated the
   train/serve boundary**.

The 30/40/30 weights the chapter quotes are accurate to the archived file. But
its first term is **inter-model agreement**, computed as the relative spread
across several models' forecasts — and Chapter 5 settles selection to **one model
per category**, so there is nothing left to disagree. The engine is not merely
unused; its central input no longer exists.

### Anchor

**Section 7.2.2 What the interface returns.** The paragraph in full:

> "A second and different composite confidence score exists in this work,
> produced by the deterministic synthesis engine described below, which combines
> inter-model agreement, interval tightness and model accuracy under weights of
> thirty, forty and thirty per cent. The two indices address the same question by
> different means and are not interchangeable. Both are documented here."

**The preceding paragraph ends:** *"...while the claim about how far a forecast
may be relied upon is carried by the track record instead."*

**The following paragraph begins:** *"The track record is what distinguishes this
interface from one reporting a forecast and its interval alone."*

### Action

REPLACE — the paragraph becomes a statement about the design's history rather
than its contents.

#### Replace with

> An earlier design carried a second composite score, combining inter-model
> agreement with interval tightness and measured accuracy. It was removed with
> the component that produced it. Its leading term was the relative spread across
> several models' forecasts, which presupposes that several models are served for
> a category; Chapter 5 settles that question in favour of one, leaving the term
> undefined rather than merely small. The interface therefore carries a single
> confidence field, and Section 7.4 establishes what that field is worth.

### Note — why not simply delete it

Deleting leaves a reader who has seen the archived code wondering whether it was
overlooked. **Naming the removal and its reason converts an apparent omission
into a design decision**, which is the same move Fix 4 makes for the index. It
also costs three lines and forward-references 7.4, which is where the surviving
index is dismantled.

---

## Fix 4 — The repairable-index sentence (carried forward, still not applied)

**Raised by Enrico 2026-09-11; its single correction has not reached the
document.** The full diagnosis is **Part 2** below; this is the one edit the
chapter needs.

The chapter says the index *"could be repaired by recalibrating the bands against
the widths actually observed"*. ⚠ **It could not.** The chapter's own preceding
sentence says the index is constant within a category. Re-tiering a quantity that
takes exactly four values assigns every brand in a category the same band, so the
band becomes the category name.

### Anchor

**Section 7.4 Preserving uncertainty**, the final paragraph. Starts:

> "That is a property of the weights and the cut-offs rather than of the
> forecasts, and it could be repaired by recalibrating the bands against the
> widths actually observed."

**It continues** *"Reported as it stands, however, it settles a question..."* and
the paragraph ends *"...is not by itself what makes that forecast usable."*

### Action

REWORD the first sentence only. The rest of the paragraph stands.

**Before:**

> "That is a property of the weights and the cut-offs rather than of the
> forecasts, and it could be repaired by recalibrating the bands against the
> widths actually observed."

**After:**

> "That is a property of the construction rather than of the forecasts, and it is
> not repairable by choosing different weights or different band boundaries:
> both terms are functions of a quantile that is fixed within a category, so any
> reweighting or re-thresholding yields one value per category and assigns every
> brand in that category the same band."

### Note

The current wording **offers a repair that does not exist**, and an examiner who
takes it at face value will ask why it was not done. The honest answer is that it
would not have worked.

---

## Fix 5 — Table 18 is empty, and the hold that emptied it is resolved

Enrico's comment on 7.4 (10 Sep) holds the calibration table because
`srq1_calibration.py` fitted XGBoost for every category while Energidrikke and
RTD serve LightGBM.

✓ **That is fixed.** `srq1_calibration.py:178` now has a `served_model()` helper
reading the served metadata, and its docstring records the defect explicitly:
*"Until 2026-09-11 this script fitted XGBRegressor unconditionally, so half the
published calibration table described a model that is not served."* The table was
regenerated 2026-09-11 17:16, after the training cutoff.

### Anchor

**Section 7.4**, the empty eight-row table above the caption ***Table 18*** *-
Calibration of the prediction interval at two nominal levels*.

### Action

EDIT-THEN-INSERT — fill the table, then apply Fix 6 to the two paragraphs that
read it.

#### Replace with

| **Category** | **Nominal** | **Empirical coverage** | **Median rel. width** | **n** |
|---|---|---|---|---|
| CSD | 80% | 80.5% | 3.40 | 665 |
| CSD | 90% | 91.7% | 8.99 | 665 |
| Danskvand | 80% | 73.6% | 3.03 | 174 |
| Danskvand | 90% | 83.9% | 11.77 | 174 |
| Energidrikke | 80% | 77.3% | 10.54 | 308 |
| Energidrikke | 90% | 86.7% | 34.44 | 308 |
| RTD | 80% | 83.3% | 3.92 | 372 |
| RTD | 90% | 91.4% | 8.52 | 372 |

⚠ **The column header must read "Median rel. width", not "Mean"** — see Fix 7.

---

## Fix 6 — Two numbers in the 7.4 prose no longer match the regenerated table

Both were correct against the pre-fix table and are wrong against the current
one. This is exactly the failure the artefact-recency rule exists to catch: the
prose was verified once, the artefact moved beneath it.

| The prose says | Measured now |
|---|---|
| Energidrikke at 80% "remains above twelve" | **10.54** |
| Danskvand "roughly eight points below" nominal at 80% | **6.4 points** (73.6 against 80) |

### Anchor

**Section 7.4**, the paragraph beginning *"At eighty per cent the picture
changes."* It is the second paragraph after Table 18.

### Action

REWORD — two clauses inside one paragraph, applied in one pass.

**Before:**

> "The interval narrows to around three to four times the actual for CSD,
> Danskvand and RTD, which is a range a planner can work with, while Energidrikke
> remains above twelve. Coverage at this level is close to nominal for CSD, RTD
> and Energidrikke, and roughly eight points below it for Danskvand."

**After:**

> "The interval narrows to around three to four times the actual for CSD,
> Danskvand and RTD, which is a range a planner can work with, while Energidrikke
> remains above ten. Coverage at this level is close to nominal for CSD, RTD and
> Energidrikke, and roughly six points below it for Danskvand."

### Note — the surrounding claims all still hold

The 90% paragraph's "between roughly eight and thirty-four times" is correct
(8.52 to 34.44). "Three of the four" at 80% is correct. Danskvand as the
exchangeability failure is correct and is the largest shortfall at both levels.

---

## Fix 7 — The width column is a median labelled as a mean

Enrico flagged this on the CSV. ⚠ **It is worse than recorded: the rendered
markdown label is wrong too**, so the defect reaches the reader rather than
stopping at the column name.

`srq1_calibration.py:251` computes `np.median(...)`. The CSV column is
`mean_rel_width` and `calibration.md` prints the header **"Mean rel. width"**.

### Action

A **code fix**, not a paste — rename the column and the printed header to
`median_rel_width` / "Median rel. width", then regenerate. It changes no value.

⚠ Until it is done, **Table 18's header in the thesis must say "Median"**, which
Fix 5 already does. A thesis table and its source artefact disagreeing on what a
column measures is the kind of thing an assessor checks.

---

## Fix 8 — The duplicated chapter title

The chapter opens with its title twice, on consecutive lines, before the
subtitle. Almost certainly an artefact of the 2026-09-08 rename.

### Action

Delete the second occurrence. Verify in Word that one of the two is not a
heading carrying the numbering.

---

## Fix 9 — "Preserving uncertaint" is missing its final letter

Section 7.4's heading reads **"7.4 Preserving uncertaint"**. It appears in the
table of contents and every cross-reference.

### Action

REWORD the heading to **"7.4 Preserving uncertainty"**.

---

## Fix 10 — "Outstanding decisions" is a planning section inside submission prose

The chapter ends with four bullets that are notes to the authors: whether to add
a fourth confidence component, whether to flag low-confidence recommendations for
human review, an API cost ceiling, and whether to log to SQLite. Brian's comment
tags it METACOMMENT, VERIFY, correctly.

⚠ **Its cost figure is also wrong**: it estimates "N=50 × ~$0.005/call ≈ $0.25".
Measured cost is **$0.0091** for a tool-backed answer, so fifty calls are $0.46,
and the costly arms are twenty-five times that again.

### Action

DELETE the section from the chapter.

### Note — where the content goes

Two of the four are real and belong on the deferred list rather than in the bin:

- **A human-review flag for low-confidence recommendations.** Currently
  meaningless, because every forecast tiers Low (Fix 4) — it would flag
  everything. Worth stating as future work *conditional on* a discriminating
  index.
- **A fourth confidence component tracking accuracy drift.** Same dependency.

The SQLite question is **already answered** in 7.5: the log is one JSON object
per line, and the reasoning for that choice is given. The cost ceiling is
answered by Fix 1.

---

# Comment ledger

| Thread | Section | Verdict |
|---|---|---|
| Brian, chapter naming (resolved) | title | **VERIFIED-OK.** Enrico renamed it to SRQ2's own predicate and renamed 6.4 to avoid collision. Already applied. |
| Enrico, the two placeholders | 7.1 | **VERIFIED-OK.** Replaced by Goodwin et al. (2010), confirmed in Zotero and pointing the right way. |
| Enrico, 7.4 IN REVIEW / table held | 7.4 | **ADDRESSED** by Fixes 5, 6, 7. The blocking defect is fixed in code and the table regenerated. |
| Brian, PROSE VERIFY | 7.6 | **ADDRESSED** by Fix 1. Every bullet falsified by measurement. |
| Brian, no judge / temp 0 / N wrong | 7.6 | **ADDRESSED** by Fix 1. All three confirmed in code. |
| Brian, METACOMMENT VERIFY | Outstanding decisions | **ADDRESSED** by Fix 10. |

---

# Part 2 — The confidence index, in full

**Folded in from `ch7-confidence-index-decision.md` (Enrico raised it 2026-09-11),
re-verified 2026-09-12.** Fix 4 above is the one edit the chapter needs. This part
is the evidence behind it, kept because an examiner will ask and because the
argument is a contribution rather than an apology.

## What changed on re-verification

| Claim in the original note | Now |
|---|---|
| coverage 91.0 / 90.9 / 86.0 / 83.9 at nominal 90 | ⚠ **three of four stale.** Current: CSD 91.7, Danskvand 83.9, Energidrikke 86.7, RTD 91.4 |
| "a score returning four values across 230 brands" | the brand count is not verifiable from any current artefact — **drop the number**, the argument does not need it |
| final section: the calibration table describes a model two categories do not serve (S17) | ✅ **closed.** Fixed in code 2026-09-11, table regenerated. Removed here; see Fix 5 |
| the four index values, the formula, the three SRQ4 consumers | ✅ **all re-verified unchanged** |

⚠ **The stale coverage figures do not weaken the argument** — they were quoted to
show the intervals are correctly calibrated *while the index built on them is
not*, and the current figures make that point equally well.

## The formula, and why it cannot be repaired

`forecast_tool.py:531`:

```python
conf = 100 * (0.5 * (1 / (1 + rel)) + 0.5 * (1 - min(q90, 1)))
```

**Two independent defects, either of which alone would flatten the score.**

**Defect 1 — the forecast cancels out of the width.** The interval is built
multiplicatively in log space, so the width is proportional to the forecast and
dividing by it cancels:

> rel = (hi − lo) / y ≈ e^q90 − e^−q90 = 2·sinh(q90)

Since the quantile is **one number per category**, the relative width is a
per-category constant. Nothing brand-specific enters it.

⚠ **This is a property of the design, not of the data.** Any multiplicative
interval with a shared quantile behaves identically.

**Defect 2 — the second term is off by a unit.** The expression treats the
quantile as though bounded near 1. It is a log-space residual quantile, which
reaches 1.0 as soon as the band is wider than roughly a factor of 2.7 either way.

| q90 (log) | the 90% band it implies | term 2 |
|---|---|---|
| 0.25 | x0.78 to x1.28 | 0.75 |
| 0.50 | x0.61 to x1.65 | 0.50 |
| **1.00** | **x0.37 to x2.72** | **0.00** |
| 1.89 (RTD) | x0.15 to x6.6 | 0.00 |
| 2.69 (Energidrikke) | x0.07 to x14.7 | 0.00 |

**Every category sits between 1.89 and 2.69**, so half the index is dead by
construction.

## What it returns, recomputed 2026-09-12

From `models/index.json`, written 2026-09-09 21:10:

| Category | Served | q90 (log) | rel. width | term 1 | term 2 | **conf** | tier |
|---|---|---|---|---|---|---|---|
| CSD | XGBoost | 2.027 | 7.46 | 5.9 | **0.00** | **5.9** | Low |
| Danskvand | XGBoost | 2.040 | 7.56 | 5.8 | **0.00** | **5.8** | Low |
| Energidrikke | LightGBM | 2.691 | 14.69 | 3.2 | **0.00** | **3.2** | Low |
| RTD | LightGBM | 1.890 | 6.47 | 6.7 | **0.00** | **6.7** | Low |

**Four attainable values across the entire product range, all tiering Low.**

## What went wrong, and why it is worth one sentence

1. **The formula was never checked against the range its inputs take.** A single
   print of the four quantiles would have caught it.
2. **The two terms are not independent.** Both derive from the same quantile, so
   an equal weighting combines one quantity with itself.
3. **Nothing asserted that the output varied.** A one-line check catches this.

⚠ **It is not caused by sparse data or the small panel.** Those explain why the
*intervals* are wide, which is an honest finding at this data scale. The
intervals are correctly calibrated. **It is the index built on top of them that
is not**, and Chapter 7 should keep those two statements apart.

## The decision, and the code consequence

| Option | Verdict |
|---|---|
| **Keep the field, stop presenting it as a confidence signal** | ✅ **recommended** |
| Recalibrate the tier cut-offs | ❌ re-tiering a per-category constant yields a category label wearing a number |
| Fix defect 2 only | ❌ defect 1 still leaves it constant within a category |
| Rebuild on a per-forecast quantity | ⚠ real work, out of scope for the time available |

⚠ **Deleting the key is not a local change.** Re-verified 2026-09-12 — three SRQ4
consumers depend on it, and one is an already-scored result:

| Consumer | What it does | If deleted |
|---|---|---|
| `verify_setup.py:215` | asserts the field is in the payload | **pre-flight fails**, blocking every run |
| `score_interval_communication.py` | scores one of four criteria | a scored criterion disappears |
| `inspect_runs.py:133` | prints the tier | cosmetic |
| `interval_communication.csv` | **already holds scored runs** | existing results stop being reproducible |

**Keeping the key costs nothing and is honest, not a fudge.** The SRQ4 criterion
asks whether an agent *communicates* the uncertainty it was given, which is a
question about the agent and is unaffected by whether the index is informative.
Chapter 7's claim is about what the payload should be *trusted* for. Both are
true at once.

### Note — the one code change this implies

The tool's docstring says the index "varies little within a category". ⚠ **It does
not vary at all.** Worth strengthening, and it is a comment-only edit.

---

# Part 3 — The payload changed what the agent did

**Folded in from `the-payload-changed-behaviour.md`, re-verified 2026-09-12
against the committed smoke traces.** ✓ **Every figure and both quotations
verified exactly.** Nothing changed.

⚠ **Not for the chapter yet.** One brand-month, one run per combined arm. This is
recorded so the claim is ready when the funded set lands, and so the evidence is
not re-derived.

## What happened

Both combined arms were given the model's forecast alongside the history and an
execution sandbox. **Neither returned the model's number.**

| Arm | Given | Returned | Error |
|---|---|---|---|
| combined | 4,969,050 | **6,200,000** | 2.6% |
| combined, in production | 4,969,050 | **5,604,800** | 12.0% |
| tool-only, both orchestrators | 4,969,050 | 4,969,050 | 21.9% |

The two tool-only arms relayed the figure **identically, to the decimal, on every
run and on both orchestrators**.

## The part that matters: they said why, unprompted

Neither arm was asked to justify departing. Both did, and both named **the
model's own reported uncertainty**. Verbatim from the traces:

> "...the history is short, 2025 was volatile, and the dedicated model's own
> confidence is low with a very wide interval."

> "...the dedicated model is low-confidence with a wide interval; March history
> supports the midpoint, but recent sales are volatile and likely
> promotion-sensitive."

**The payload carried decision-relevant information rather than a bare number,
and that information changed the decision.** That is what Chapter 7 claims the
interface is for.

## Why this is the strongest SRQ2 evidence available

⚠ **It does not depend on sample size the way an accuracy ranking does.** It is a
claim about *mechanism*, and a single clean instance demonstrates a mechanism
exists. More runs establish how often, not whether.

- **Both arms did it independently**, on two different orchestrators.
- **Neither was prompted to.** The reasoning is unelicited.
- **They cited the specific fields the interface supplies** — the confidence tier
  and the interval width — not vague hedging.

## The uncomfortable part, which makes it stronger

⚠ **The index is degenerate (Part 2), and it still worked here.** On this brand
"low confidence with a wide interval" was the *correct* signal.

| Do NOT conclude | Do conclude |
|---|---|
| the index works, so the defect does not matter | the **uncertainty channel** works; the index is one degenerate input to it |
| the index should be kept as it is | a constant "low" is right by accident here and would be wrong wherever confidence should vary |

**The honest formulation:** the interval width did the work, and the tier agreed
with it because both derive from the same quantile. **That is not a defence of the
index.**

## What to write, and when

When the funded set lands, the claim this supports is:

> The interface's uncertainty channel is consumed rather than ignored: agents
> given a forecast with its interval and a confidence qualifier weigh it against
> other evidence instead of adopting it, and cite the qualifier when they do.

**What must be measured first:** how often the combined arms depart, and whether
they cite the uncertainty fields when they do. Both are already recorded on every
run, so the funded set answers this with no additional instrumentation.

⚠ **Do not claim the agents were *right* to depart.** On this brand they were —
both landed closer than the model. That is an accuracy claim needing the funded
set. The SRQ2 claim is about the channel being used, which is separable and much
better supported.

### Note — one design decision this validates

The combined arms supply the forecast as **one input among several**, never as a
figure to revise. Had the framing been "here is the forecast, revise if needed",
the near-certain outcome was both arms returning it unchanged and the arm
establishing nothing. **Measured: both departed.** This belongs in Chapter 3 or
Chapter 8's design description — it says the instrument measures what it was
built to measure.

---

# One finding for a different chapter

**`export_appendix.py` carries a stale note that contradicts Chapter 7, and the
chapter is the correct one.** Its `review=` block says the "gives a
recommendation" criterion was **DROPPED** because the shared prompt never asked
for one.

✓ **The prompt was amended.** `prompts.py` records *"v3 2026-09-03 adds the
recommendation request (Goodwin...)"*, and all seven scenario prompts were
rendered to confirm: **every arm receives the recommendation request**,
identically.

So the chapter's account in 7.3 is right and the exporter's note is eight days
stale. ⚠ **It must be corrected before the appendix is regenerated**, or the
appendix will tell an assessor a criterion was dropped that the chapter says was
kept. Filed for the Chapter 8 pass.

---

# Related

- Both former notes in this folder are **folded into Parts 2 and 3** and archived
  under `.archive/`. Nothing else in this folder is live.
- `ch10_limitations/interval-width-a-tested-negative-result.md` — the three
  alternative calibration schemes, which is what 7.4's "left to future work"
  should eventually cite
