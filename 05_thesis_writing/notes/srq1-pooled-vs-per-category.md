---
name: srq1-pooled-vs-per-category
description: RULE - Report-writing notes on the SRQ1 pooled-vs-per-category result, the metric disagreement it exposes, and how to state the finding without overclaiming.
category: reference
applies-to: [srq1, methodology, ch6, ch8]
triggers: [writing the SRQ1 results, describing category specialization, defending the pooling comparison]
created: 2026_08_22-10_00
updated: 2026_08_22-11_00
---

# SRQ1 — pooled vs per-category

Closes the third leg of SRQ1's headline question. Written for the results and
methodology chapters.

**Source artifacts:** `04_thesis_results/srq1/pooled_metrics.csv`,
`pooled_summary.md`, `pooled_params.json`. Script:
`03_thesis_modelling/model_training/srq1/srq1_pooled.py`. Findings: P0040 F44,
F48–F50.

## Why this exists at all

SRQ1 names a **three-way** trade-off — accuracy, memory efficiency, and *category
specialization* — and `srq1-models-efficiency.md:32` glosses the third as
*"does a per-category model beat a single pooled model?"*

Until 2026-08-21 the results answered the first two only: `tuned_metrics.csv` held
4 categories × 2 models and **no pooled row**. The thesis asked a question in its own
section heading that its results did not answer. Say nothing about this in the prose;
just make sure the gap is closed before submission, because it is the kind of thing
an examiner finds by reading the heading and then the table.

## The headline result

Delta = pooled WMAPE − per-category WMAPE. **Positive means the specialised model
wins.** Sorted by training rows:

| Category | train rows | LightGBM | XGBoost | Winner |
|----------|-----------:|---------:|--------:|--------|
| CSD | 1805 | +1.2pp | +1.3pp | per-category |
| RTD | 992 | +0.7pp | +1.5pp | per-category |
| energidrikke | 748 | −1.6pp | −1.4pp | **pooled** |
| danskvand | 464 | −2.2pp | −2.5pp | **pooled** |

### What makes this defensible

**The sign flips exactly once, in the same place, for both model families.** Two
independently tuned gradient-boosting implementations agree on all four categories
and agree on magnitude to within 0.8pp. An artifact of one algorithm's inductive
bias would not replicate that way. Lead with this when defending the result —
cross-algorithm replication is the strongest thing the comparison has.

### The claim to make

Not "pooled wins" and not "per-category wins", but a **conditional**:

> Neither strategy dominates. Specialisation pays only where a category has enough
> history to support it; below that threshold a pooled model borrowing
> cross-category structure is more accurate. On this dataset the crossover sits
> between roughly 750 and 1000 brand-month training observations.

This is more useful to a practitioner than either absolute, because it converts a
modelling choice into a **measurable precondition** — count your rows, then decide.

### ATTRIBUTION RULE — verified 2026-08-23, do not break this when drafting

**The 750–1000 threshold is ours. It does not appear in Montero-Manso & Hyndman
(2021) or anywhere else in the literature.** A source-level verification checked
that paper specifically for it and found nothing, warning that attributing the
number to them would be *"a misattribution and a severe factual overstatement"*.

The split to hold when writing:

| Cite Montero-Manso & Hyndman (2021) for | Report as OUR finding |
|---|---|
| *why* a crossover should exist at all — local models cannot estimate parameters from short series (p. 1633); global models pool to avoid overfitting | **the location of the crossover** on this dataset |
| the local/global definitions (p. 1634) | that the sign flips **once**, and replicates across two algorithms |
| that global models need no homogeneity assumption (Prop. 1) | the ~750–1000 brand-month figure |

**This makes the result stronger, not weaker.** The theory predicts a crossover
exists but supplies no threshold; measuring one on an FMCG brand-month panel is
a contribution rather than an application.

### Two qualifications the same verification attached

1. **The generalisation bound assumes cross-series independence.** Proposition 2's
   complexity argument applies Hoeffding across series, which requires them to be
   independent. **Brands within one beverage category plainly are not** — they
   compete for the same shelf and the same occasion. The bound is therefore
   suggestive here, not binding. Saying so is cheap and is the kind of thing an
   examiner rewards.

2. **Global models may need longer memory than local ones**, per Proposition 1 —
   a shared function must distinguish series that a per-series model never has to
   tell apart. **Our pooled and per-category runs use an identical lag set**
   (lag_1..lag_13 plus rollings), so the pooled arm may be handicapped by exactly
   the memory constraint the theory flags. **This is a possible confound and
   belongs in the limitations**: the measured crossover may sit at a different
   row count for a pooled model given longer lags. Not a reason to withhold the
   result — a reason to state its scope.

It also sharpens the memory-efficiency leg: one pooled model is a quarter of the
artifacts, and for two of four categories it is *also more accurate*, so for those
categories the accuracy/memory trade-off **is not a trade-off at all.** That is a
genuinely useful sentence for the deployment argument.

## The caveat that must not be omitted

**WMAPE and median MAPE disagree in 2 of 8 cells, and the disagreements are far
larger than any WMAPE effect.**

| Model | Category | WMAPE winner | medMAPE winner |
|-------|----------|--------------|----------------|
| XGBoost | CSD | per-cat (15.3 vs 16.6) | **pooled** (34.8 vs 35.5) |
| XGBoost | energidrikke | pooled (12.5 vs 13.9) | **per-cat by 11.2pp** (39.7 vs 50.9) |
| LightGBM | RTD | per-cat (35.1 vs 35.8) | per-cat by 11.6pp (43.4 vs 55.0) |

Every WMAPE delta in the entire table is ≤ 2.5pp. Median-MAPE deltas reach 11.6pp.

**Why, mechanically:** WMAPE divides summed absolute error by summed actuals, so
high-volume brands dominate it. Median MAPE weights every brand-month equally, so it
reflects the typical brand. The natural reading is that pooling helps small series
and hurts large ones *within* a category — the same "borrow from the data-rich"
mechanism as the cross-category result, one level down.

**That reading was tested per-brand, and it only half holds.** See the section below
before writing it as the explanation.

### How to frame it

Report **WMAPE as the headline** (it is the operational metric: the business cares
about total units mis-forecast), then state the median-MAPE disagreement explicitly
and interpret it as evidence about *who* pooling helps.

Stated openly this is an **additional finding**. Found unaided by a reviewer, it
reads as a cherry-picked metric. There is no version of this where omitting it is
the better choice.

### Arguably the most useful sentence in the comparison

> The pooled-vs-per-category choice is nearly irrelevant for total-volume accuracy
> (≤2.5pp) and quite consequential for typical-brand accuracy (up to 11.6pp).

This is invisible if only WMAPE is reported, and it is the version a practitioner
can act on.

## The per-brand test — the mechanism only half holds

`srq1_pooled_perbrand.py` scored all 213 brands individually and related each
brand's pooled-minus-per-category delta to its own volume, to test the explanation
above rather than assert it. **The result is split by model family**, and the note
that follows is deliberately less tidy than the section above, because that is what
the data supports.

| | small brands | medium | large |
|---|---|---|---|
| **XGBoost** win-rate for pooling | 68% | 59% | 54% |
| **LightGBM** win-rate for pooling | 46% | 45% | 46% |

**XGBoost supports it cleanly** — monotone across terciles on win-rate and on median
delta (−6.9 → −1.0 → −0.3pp), and negative in the small tercile of all four
categories. **LightGBM shows nothing**: a flat 46/45/46 win-rate and a correlation
against training rows of −0.014.

Judge this on win-rate, not correlation. Medians and means diverge sharply
(LightGBM small: median +2.0pp, mean −3.9pp), so outlier brands move the mean and
with it any correlation coefficient. Win-rate asks only *for how many brands did
pooling win*, which is both the question of interest and immune to outlier
magnitude. An earlier version of the analysis script judged by correlation and
reported "supports" for both models; that verdict was wrong and the script has been
corrected.

### How to phrase it

> A per-brand breakdown supports this mechanism for XGBoost — pooling wins for 68%
> of small-volume brands against 54% of large ones, declining monotonically — but not
> for LightGBM, where the effect is flat across the volume range. The metric
> disagreement is therefore real, but its cause is not uniform across model families.

**Note the contrast with the category-level result**, and make it explicitly: the
*category-level* crossover replicates across both algorithms, which is what makes it
trustworthy; the *brand-level* mechanism does not. Reporting the first as robust and
the second as model-dependent is the honest split, and it demonstrates the
replication logic being applied consistently rather than only where it flatters the
result.

**Exclusion to state:** 124 of 460 brand-model rows (27%) were unscorable — zero
actuals in the test window, where APE is undefined rather than merely large. These
statistics describe the continuously-selling subset only. The figure is consistent
with the ~40% unscorable rate found during SRQ4 brand selection, so it is a property
of the data, not of this analysis.

**If the brand-level mechanism becomes load-bearing in the prose**, a seed sweep
would establish whether LightGBM's null is stable or a one-seed artifact. Cheap, no
API spend. The category-level result does not depend on it.

## Methodological choices worth defending in prose

Three, each of which removes a confound. Worth a short methods paragraph because
each one is a place the comparison could have been made uninterpretable.

**1. Scored per-category, never pooled-in-aggregate.** A single pooled WMAPE across
all four categories would be dominated by CSD's volume, and comparing it against four
separate per-category numbers compares different populations. Instead one pooled
model is trained, then **scored separately on each category's test rows**, against a
per-category model on those *same* rows. Only the training rows differ.

**2. The per-category arm was re-trained, not read from `tuned_metrics.csv`.** That
file's models used 13 features including `promo_intensity`; the pooled model can only
use the 12-feature intersection. Reusing the old numbers would have confounded
*pooling* with *one fewer feature*. Both arms here use the same 12.

**3. The series key is `(category, brand)`, never `brand`.** Measured: **16 brand
names span more than one category** (AQUA D'OR, EASIS, FEVER TREE, FREM, HANCOCK,
HARBOE, …), and `OTHER BRAND` is a per-category residual bucket with different
contents each time. Pooling on name alone would have silently merged unrelated
series. The script audits and prints this before training.

## The feature-intersection framing needs correcting

`prometheus-scenarios-design-rationale.md` argues the intersection is "a finding, not
a limitation" on the basis of **33 of 51 matrix columns** being common. That number
is true of the *feature matrices* but **not of the models**, which consume only 13
columns. The real intersection is **12 of 13** — the sole casualty is
`promo_intensity`, ranked 11th of 13 by SHAP in CSD (0.041).

Correct that section. The underlying point survives and is arguably stronger: pooling
costs almost nothing in features, so the measured accuracy differences are
attributable to pooling itself rather than to a crippled feature set. That is what
makes the comparison worth reporting.

The construct-validity argument in that same note — that union-with-NaN would let a
tree split on *is-NaN* and rebuild a category indicator — remains **valid as
reasoning** but no longer describes a live risk, since dropping `promo_intensity`
leaves no NaNs to split on. Keep it as justification for the design choice, not as a
description of a hazard avoided at runtime.

## Caveats to state plainly

1. **Effect sizes are small** (0.7–2.5pp on WMAPE). Directional, not decisive.
2. **No confidence intervals.** Single split, single seed. A seed sweep is cheap
   (no API spend) and is the obvious response if a reviewer presses.
3. **The crossover is interpolated from four points.** "Between roughly 750 and 1000
   rows" is the honest phrasing; a precise threshold is not supported.
4. **RTD sits near 35% WMAPE in both arms.** For that category the pooling question
   is secondary to the fact that neither model forecasts it well — worth saying so
   rather than reporting a +0.7pp delta as if it were the interesting number.
5. **The per-brand breakdown excluded 27% of brands until 2026-08-23.** A
   scorability filter (zero actual in the test window) was applied to **WMAPE**
   statistics, which do not need it — WMAPE puts the sum in the denominator and is
   defined at zero. The excluded brands were the intermittent, low-volume ones,
   i.e. precisely the population the pooling question concerns, and restoring them
   **flipped the sign of the XGBoost size correlation** (+0.252 → −0.095). Any
   per-brand number predating that fix is unusable. Hyndman & Koehler (2006,
   p. 683) also criticise the exclusion practice generally.

   **Superseded 2026-08-23 — nothing is excluded from the WMAPE tables at all.**
   An intermediate fix applied a 1 unit/month volume floor, because readmitting
   every brand let in ones averaging under one unit across the test window, where
   a delta of −3179pp is division by an almost-empty denominator. That worked but
   was a judgement call, and measuring it showed it was a **poor proxy for the
   thing it targeted**:

   | | brands |
   |---|---:|
   | Below the floor (<1 unit/month) | 38 |
   | — of which **smooth** (well-behaved, merely small) | **8** |
   | **Above** the floor yet lumpy/intermittent | **21** |

   It removed well-behaved small brands while leaving irregular ones in, because
   **volume and regularity are different properties**.

   Replaced by the **Syntetos–Boylan–Croston categorisation** (2005, *JORS* 56(5),
   495–503, p. 495), whose cut-offs are *derived* rather than tuned: average
   inter-demand interval **p = 1.32** and squared CV of non-zero demand sizes
   **CV² = 0.49**, partitioning into smooth / erratic / intermittent / lumpy.

   **Results are now reported per demand class, with no exclusion.** A weak result
   on lumpy series is a stated limitation rather than an absence — which is what
   both Hyndman & Koehler (p. 683) and Syntetos & Boylan actually recommend, since
   both object to discarding difficult series rather than modelling them.

   *One caveat to state:* the cut-offs were derived for Croston-type estimators
   (α = 0.15, lead time 1), not for gradient boosting on a brand-month panel. They
   are used as a **principled, citable partition of demand patterns**, not as a
   claim that the same accuracy ordering transfers — which the per-class results
   can themselves examine.

7. **The size correlation is not robust, and should not be reported as a number.**
   Across three defensible variants of the same analysis — scorable-only (the old
   bug), all brands, and all brands above the volume floor — XGBoost's
   correlation between delta and log volume reads **+0.252, −0.095 and +0.176**.
   It changes sign on inclusion choices alone. **Report the win-rate pattern
   instead**, which is stable: pooling wins most often on small brands (56–68%)
   and is near a coin-flip on large ones (46–57%), with no monotone trend. The
   instability of r is itself worth one sentence, because it is the same lesson
   as F63/F67 — a diagnostic that looks quantitative but is outlier-driven.
6. **Under-tuning inflates apparent gains.** At 2 trials the per-category danskvand
   result read 41.6%/22.0%; at 30 trials it read 23.7%/21.5%. The pilot's dramatic
   −20.9pp was a tuning artifact roughly ten times the true effect. Worth one
   methodology sentence, because the direction of that bias favours whichever arm
   happens to converge faster — a trap, not a curiosity.

## Related

- `srq1-models-efficiency.md` — the SRQ1 question this closes
- `prometheus-scenarios-design-rationale.md` — contains the 33/51 framing that needs
  the correction above
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md` — F44, F48–F51
- `04_thesis_results/srq1/pooled_perbrand_summary.md` — the per-brand tables
