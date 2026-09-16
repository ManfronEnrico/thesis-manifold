---
name: 2026-09-14_BRANCH_A_ch5-consolidated-book-citations-and-flow
description: NOTE - Chapter 5 consolidated pass. Five free Hyndman citations that endorse choices the chapter already made, plus the flow items landing here. The 7.5 citation is rerouted to Ch4; 5.9's seasonal half stays out because MASE uses m=1.
category: workflow
applies-to: [ch5_model_benchmark]
triggers: [ch5 prose pass, defending the benchmark design, answering why this metric, book citations]
created: 2026_09_14-09_30
updated: 2026_09_14-09_30
snapshot: 2026-09-13_21-30_book-citations-pass
status: prose ready to paste, awaiting human review
---

# Chapter 5 — consolidated pass

Verified against snapshot `2026-09-13_21-30_book-citations-pass` (Ch5 at 7,732
words — up 196 from the previous snapshot, which is Fix 8's calibration table
landing), repository at `9746b44`, fetch clean. Zotero: **89 items**. Hyndman &
Athanasopoulos (2021) is key `5NFQRRXS`, already cited in this chapter.

**Notes swept:**
- `2026-09-13_21-15_BRANCH_A_book-citations-that-strengthen.md` — not applied,
  **superseded by this file** and archived with it. One of its six citations is
  rerouted and one is withheld; see the corrections.
- `ch5-profiling-rerun.md` — **left in place, not applied.** It is a measurement
  task, not a prose task, and nothing here touches it.

**Already applied and verified this session**, so not re-proposed:
- the tested-alternatives calibration table in 5.5.7 (Fix 8 of the Ch10 note) ✓
- 72.4 → **73.6** in 5.5.7 (Fix 9) ✓ — `calibration.csv` agrees, and Table 13
  ten lines above now agrees with the prose

---

# Three corrections to the note this supersedes

## Correction 1 — the 7.5 weighted-distribution citation does NOT belong here

The superseded note routes it to Ch5. **Chapter 5 never mentions the
weighted-distribution feature.** The rejection prose lives in Ch4 §4.3, in two
places, and I verified both against this snapshot.

**Moved to the Ch4 consolidated note as its Fix 4.** Do not look for a home for
it here.

## Correction 2 — 5.9's seasonal sentence must stay OUT

The superseded note already carried this warning and it is confirmed:
`mase_denominator()` at `srq1_benchmark_cv.py:184` computes
`np.mean(np.abs(np.diff(y)))` — a **one-step** naive denominator, m=1, on a
seasonal monthly panel.

The book says that where data are seasonal the benchmark should be the
**seasonal** naive method. **The thesis violates that**, so citing 5.9's seasonal
half would have the chapter cite a rule it breaks, in the same chapter that
reports a seasonal-naive comparison.

**Fix 4 below claims only the safe half of 5.9** — the preference for scaled over
percentage errors, which the chapter already satisfies.

## Correction 3 — the §13.3/§5.6 bounding citation is a STRENGTHENING, not a gap

The superseded note implies Ch5's upper bound needs sourcing. **It is already
sourced.** Section 5.5.2, the Ridge paragraph:

> "Hyndman and Athanasopoulos (2021) prefer bounds imposed through the
> transformation itself over constraints applied to a finished forecast, and this
> is a departure from that preference..."

The chapter already names the source, the preference, and its own departure from
it. **That is exemplary and needs nothing.** Fix 5 adds only the mechanism that
makes the departure defensible.

---

# The fixes

Five fixes, each a **free citation**: a choice the chapter already made
correctly, which the source independently endorses, and which the prose
currently justifies from first principles or not at all.

---

## Fix 1 — 5.3.1, the single-month-at-fixed-horizon design is a strength presented as a convention

### Anchor

**Section 5.3.1 Grain and data split.** The paragraph beginning *"The panel is
split temporally into training, validation and test partitions with no
shuffling"*.

It ends: *"...665 rows for CSD, 372 for RTD, 308 for energidrikke and 174 for
danskvand."*

### Action

INSERT AFTER — one sentence, appended to that paragraph.

#### Replace with

> Scoring at a single fixed horizon rather than averaging across several also
> avoids a known defect of test-set comparison, since forecast variance grows
> with the horizon and averaging errors drawn from different horizons combines
> quantities of unequal variance (Hyndman & Athanasopoulos, 2021).

### Note — what this converts

The chapter justifies the three-month horizon on **decision relevance** (*"a
quarter is the period over which the promotional and range decisions this
forecast supports are taken"*), which is a good business justification and not a
methodological one.

The design — `test.iloc[HORIZON-1]`, exactly one month at exactly H=3 —
sidesteps the variance-mixing problem **entirely**. That is currently invisible
to the reader, who sees only a convention.

⚠ **This citation also creates a standing rule worth knowing: an H=3 result must
never be compared against an H=1 figure.** If any table in the thesis does that,
it is a defect, and this sentence makes it a self-inflicted one. I found no such
comparison in Ch5, but the H=1 subtree exists and the rule should be honoured
wherever the two horizons meet.

---

## Fix 2 — 5.5.1, comparing model families on a test set is the correct instrument, not a convenience

### Anchor

**Section 5.5.1 Tabular-model benchmark.** The paragraph beginning *"Both
gradient-boosted models were tuned with Optuna (TPE, 100 trials) against an
expanding-window cross-validation objective, then scored once on the untouched
test split."*

### Action

INSERT AFTER — one sentence.

#### Replace with

> Comparing across model families on a held-out split rather than by an
> information criterion is a requirement rather than a preference: information
> criteria are comparable only within a model class and cannot be used to rank,
> for instance, an exponential-smoothing model against an ARIMA one, whereas a
> test-set comparison is valid across families and across differencing regimes
> alike (Hyndman & Athanasopoulos, 2021).

### Note — this is a direct endorsement of SRQ1's core design

Section 9.10 states the two-level procedure explicitly: AICc **within** a family,
test set or cross-validation **across** families. SRQ1 compares classical,
gradient-boosted and regularised-linear families — three classes — so the
held-out test split is the book's prescribed instrument and an information
criterion would have been the wrong one.

It pairs with §9.9, which adds that test-set comparisons *"are always valid"*
even between models fitted under different differencing regimes. That matters
here specifically, because ARIMA differences and the tree models do not, and a
reader could otherwise wonder whether the comparison is apples to apples.

⚠ This is also the citation that makes the **absence of an information criterion**
defensible rather than an oversight — the chapter needs none for the comparison
it actually performs. Do not overclaim it into covering feature selection, which
is where the repo genuinely lacks one.

---

## Fix 3 — 5.4.1, the deviation from the book's named recommendation is deliberate and unexplained

### Anchor

**Section 5.4.1 Why WMAPE is the primary metric.** The paragraph beginning *"The
choice is not conventional but theoretical."*

⚠ **That paragraph opens with a duplicated sentence** in the current snapshot:
*"The choice is not conventional but theoretical. The choice is theoretical
rather than conventional."* Delete one of the two while you are in there — it is
not part of this fix, but it is two words from where you will be typing.

The paragraph ends: *"...The stability analysis later in this chapter explains
why."*

### Action

INSERT AFTER — one sentence, appended to that paragraph.

#### Replace with

> Selecting on weighted MAPE rather than on root mean squared error is a
> considered departure from the standard recommendation, which names the latter
> (Hyndman & Athanasopoulos, 2021): because absolute-error loss and squared-error
> loss are minimised by different functionals, a single objective cannot serve
> two reported metrics, and tuning once per objective is the response that
> follows from the same theory the recommendation rests on.

### Note — why this is worth a sentence rather than silence

The book gives exactly one named recommendation for choosing a forecasting model:
*"find the model with the smallest RMSE computed using time series
cross-validation."* This thesis tunes on **WMAPE**. An unexplained deviation from
a single named recommendation in the standard reference is precisely the thing an
examiner circles.

And the thesis's position is **stronger than the book's here**, which is the
reason to say it out loud rather than hope nobody checks. §5.8 establishes that
MAE is minimised by the median and RMSE by the mean; §5.4.1 already builds its
whole argument on Gneiting's consistency result, which is the same fact stated
more generally. Having two reported metrics targeting two functionals, the
methodologically correct response is to tune twice — which is what
`tuned_for` in `cv_metrics.csv` records, and what Table 11 already shows.

**The chapter has already done the harder thing. It just does not say that it
knows it is departing from the convention.**

---

## Fix 4 — 5.5.3, the choice to report MASE has a source

### Anchor

**Section 5.5.3 Scaled error (MASE).** The opening paragraph:

> "WMAPE compares models within a category but says nothing about whether a
> category is forecastable at all. MASE answers that directly: below 1 beats the
> in-sample naive forecast."

### Action

INSERT AFTER — one sentence, before the table.

#### Replace with

> Reporting a scaled error alongside the percentage measures follows the standard
> recommendation, which prefers scaled errors to percentage errors where the
> evaluation sample is small enough that the percentage denominator is itself
> unreliable (Hyndman & Athanasopoulos, 2021) — a condition this panel meets, at
> between 174 and 665 test rows per category.

### Note — the half that is claimed, and the half that is not

**Claimed:** the preference for MASE/RMSSE over MAPE when the test set is small
*"especially in the denominator"*. The chapter satisfies this and the row counts
make the condition concrete rather than generic.

⚠ **NOT claimed, and must not be:** the book's accompanying rule that *"when the
data are seasonal, the benchmark used is the seasonal naive method."* The MASE
denominator here is `np.mean(np.abs(np.diff(y)))` — a **one-step** naive, m=1,
on a monthly seasonal panel. The thesis breaks this rule.

**Do not add the seasonal sentence.** Citing it would have the chapter quote a
rule it violates, three lines above a table that reports a seasonal-naive MASE
for comparison — which is where a careful reader would catch it.

This is a permanent exclusion for Branch A, not a hold. Changing the MASE
denominator to m=12 would alter a reported metric across every category and
every model, so it is not a late edit — it is a re-scoring. The chapter reports
MASE honestly on the denominator it used; it simply must not claim the source's
endorsement for a rule it does not follow.

**Ch5 already handles this honestly**, at line 254: it reports that seasonal
naive scores worse than naive on MASE while winning on WMAPE for RTD, and says
the disagreement is *"surfaced rather than resolved by picking one."* That is the
right posture and needs no citation.

---

## Fix 5 — 5.5.7, the log-space conformal interval is sourced, not improvised

### Anchor

**Section 5.5.7 Prediction-interval calibration.** The sentence introducing the
table:

> "A split-conformal wrapper on the tuned model, calibrated on validation
> residuals in log space, gives the following on the untouched test split."

### Action

REWORD.

**Before:**
> "A split-conformal wrapper on the tuned model, calibrated on validation
> residuals in log space, gives the following on the untouched test split."

**After:**
> "A split-conformal wrapper on the tuned model, calibrated on validation
> residuals in log space, gives the following on the untouched test split.
> Calibrating on the transformed scale and back-transforming the bounds
> preserves the interval's coverage, because quantiles are unchanged by a
> monotonically increasing transformation (Hyndman & Athanasopoulos, 2021)."

### Note — the small thing this closes

A reader who has followed §4.3's log transform arrives here and may reasonably
ask whether an interval computed in log space still covers at the stated rate
once exponentiated. The answer is yes, for a reason that takes one clause, and
the chapter currently leaves the reader to supply it.

This also **pairs with the bounding argument in 5.5.2**, which already cites the
same source for preferring transformation-imposed bounds over post-hoc clipping
and already names its own departure. Fix 5 supplies the mechanism —
quantile preservation — that makes the *interval* half of that argument work even
though the *point-forecast* half departs from it. Together they read as one
coherent treatment rather than two unrelated mentions.

---

# Cross-chapter flow items landing in Chapter 5

From `2026-09-13_18-40_BRANCH_A_cross-chapter-flow-and-connectedness.md`.

| Item | Status |
|---|---|
| **C8** — 5.5.7's 72.4 exists in no artefact | ✅ **DONE** — verified 73.6 in this snapshot |
| **C1** — the 8 GB / 4 GB split | Ch5 is **already correct** ("four-gigabyte sequential budget", §5.1 and §5.5.6). No edit |
| **C5** — stale chapter cross-reference | **One site: §5.7**, "integration readiness is argued in Chapter 7" → **Chapter 6**. See below |

## The one C5 site in this chapter

### Anchor

**Section 5.7**, the sentence containing *"integration readiness is argued in
Chapter 7"*.

### Action

REWORD — change **Chapter 7** to **Chapter 6**. Nothing else changes.

### Note

Ch5 and Ch6 swapped on 2026-09-08. Integration readiness is argued in the
architecture chapter, which is now Chapter 6. This is one of eight stale
cross-references across the document; the other seven are in Ch1, Ch2, Ch3 and
Ch6 and are listed in the flow note's C5 table.

⚠ **Chapter 4 shows the durable fix**: it uses Word's broken-link placeholder
rather than a typed number, so Word owns the value and a reorder cannot stale it.
Ugly in the snapshot, correct in the document. Worth considering for these eight
if there is any chance of another reorder.

---

# Citations register rows

All five fixes cite one source, already in the library, already cited in this
chapter. No verification debt.

| | |
|---|---|
| Source | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice*, 3rd ed. |
| Zotero key | `5NFQRRXS` |
| Status | **IN-ZOTERO** ✓ — verified against the 89-item pull |

| Fix | Lands in | Supports the sentence |
|---|---|---|
| 1 | 5.3.1 | "...forecast variance grows with the horizon and averaging errors drawn from different horizons combines quantities of unequal variance" |
| 2 | 5.5.1 | "...information criteria are comparable only within a model class and cannot be used to rank... whereas a test-set comparison is valid across families" |
| 3 | 5.4.1 | "...a considered departure from the standard recommendation, which names the latter" |
| 4 | 5.5.3 | "...prefers scaled errors to percentage errors where the evaluation sample is small enough that the percentage denominator is itself unreliable" |
| 5 | 5.5.7 | "...quantiles are unchanged by a monotonically increasing transformation" |

---

# One thing to notice about this chapter

Four of these five fixes say the same thing in different sections: **Chapter 5
keeps making the methodologically correct choice and then justifying it from
first principles, or not at all.**

That is a good problem. It means the chapter was written by someone reasoning
from the mathematics rather than from a textbook, which is why §5.4.1's
Gneiting argument is the strongest passage in the thesis. But it leaves free
defensive ground unoccupied, and an examiner who reaches for the standard
reference will find it agrees with the thesis in five places the thesis never
claims.

**Each fix is one sentence. None changes a number, a table or an argument.**
