---
name: ch4-feature-eligibility
snapshot: 2026-09-07_16-53_numbered-headings
category: workflow
applies-to: [chapter 4, data assessment, feature engineering]
created: 2026_09_08-16_10
updated: 2026_09_08-16_45
status: draft
---

# Chapter 4 — feature eligibility

**Three paragraphs to paste into §4.3. Nothing else in this file needs action.**

Everything below the divider is checking material. Skip it unless a number looks wrong.

---

# PASTE 1 — new paragraph, opens §4.3

**Where:** §4.3 Feature Engineering. This becomes the **first paragraph of the section**,
placed **immediately before** the sentence that currently opens it:

> "The feature matrix contains 22 columns…"

**Action:** INSERT BEFORE. Nothing is deleted.

---

Feature selection is governed by a single constraint: a column is admissible as a model
input only if its value is known at the moment the forecast is issued. The feature matrix
retains every Nielsen measure at its contemporaneous value, because those measures describe
the data and belong in the assessment; but a measure recorded for the month being predicted
cannot inform a prediction of it. Sales value in a given month correlates with sales units
in that same month at 0.90, and admitting it would produce a model reporting near-perfect
accuracy while forecasting nothing. The admissible columns are therefore those constructed
to describe the past or the calendar: lagged realisations of the target, rolling summaries
of the same window, calendar position, and promotional intensity carried forward from the
preceding period. This rule, rather than a judgement about which measures are most
interesting, determines the input set.

---

# PASTE 2 — new paragraph, follows PASTE 1

**Where:** §4.3, **immediately after** PASTE 1.

**Action:** INSERT AFTER.

---

Within that admissible set, two further questions were put to the data. The first is
collinearity: the lag and rolling features are correlated by construction, since each is
computed from the same series, and variance inflation factors confirm this directly. The
second is whether the redundancy warrants reduction. Grouping features by correlation and
retaining the most important member of each group yields a smaller set, and that reduced set
was evaluated against the benchmark rather than adopted on principle. It performed worse,
raising mean test error from 26.4 to 28.8 per cent. The correlated features are therefore
retained: collinearity is a pathology of linear estimation, whereas a gradient-boosted tree
splits on whichever correlated feature is locally most informative and loses genuine
information when the others are removed. The reduction is reported because the negative
result is the evidence for the decision.

---

# PASTE 3 — replaces one sentence in §4.2

**Where:** §4.2, the sentence introducing the log transformation.

⚠ **Find the exact sentence in the snapshot before pasting** — I could not fix its wording
from the snapshot I had. It is the sentence in §4.2 that first says the target is
log-transformed.

**Action:** REWORD — replace that one sentence with the paragraph below.

---

The logarithmic transformation is applied uniformly to the target and to the volume-valued
inputs of the linear model, rather than selected per brand. The distributional evidence
supports it without qualification: across all four categories the volume-valued features
carry raw skewness between 3.7 and 10.4, and fall to below 0.5 in absolute value under the
transformation, while the calendar and intensity features remain close to symmetric and are
left untransformed. Uniform treatment is preferred to per-series selection because the tests
that would drive such a selection have limited power at the available series length, and
because a transformation applied unevenly across brands would make the feature semantics
inconsistent within the panel.

---
---

# Below here: checking material only

## ⚠ Two numbers to fix elsewhere in the chapter

**1. The input count is 13, not 16.** If any sentence in §4.3 says the model uses sixteen
features including the holiday calendar, that is wrong. `srq1_benchmark.py::FEATURES` is:

```
lag_1, lag_2, lag_3, lag_4, lag_8, lag_13,
rolling_mean_4, rolling_std_4, rolling_mean_13,
month, quarter, peak_month, promo_intensity
```

`days_in_month`, `n_holidays` and `non_holiday_days` are in the matrix but **not trained
on**. They enter only the with-holiday arm of the ablation
(`srq1_holiday_ablation_tuned.py`). Describe the holiday enrichment as an ablation, not as
part of the standard input set.

Also: `promo_intensity` does not exist for danskvand and RTD (Nielsen reports no promotion
for them), so those two categories train on **12**. Safest phrasing: *"thirteen inputs where
the category supports promotional measurement, twelve otherwise."*

**2. Brand counts may have moved again.** The current h1 matrices hold **CSD 106,
danskvand 30, energidrikke 50, RTD 72** brands (files dated 2026-09-07 17:59). If the
chapter still says 95/29/44/62, it is one regeneration behind. I have not traced which
number belongs in which table — flagging, not fixing.

## Where the claims-register rows go

Two thresholds in this area have **no source in the library**. Both are handled by *not
citing them*, so neither PASTE block above carries citation debt:

- **The 0.95 correlation threshold** used to group redundant features. PASTE 2 deliberately
  says "grouping features by correlation" without naming a number.
- **VIF bands of 5 and 10.** PASTE 2 states no threshold at all.

If you later want either number in prose, add a row to
`06_thesis_writing/notebookLM/04-Claims_Verification/Chapter 4 - Data Assessment/` — that is
where Chapter 4's verification packs live (there is a `Holiday Enrichment/claims.md` there
already to copy the format from). Until then there is nothing to file.

**Kim (2013)** for the |skew| > 2 rule is already cited in the EDA table artefact. PASTE 3
avoids restating the threshold, so it does not depend on that citation.

## Evidence behind the three paste blocks

All measured 2026-09-08 against the shipped h1 matrices in
`_03_engineered/bymonth/*/`, all four dated 2026-09-07 17:59 — i.e. **after** the holiday
enrichment, which is present and fully populated (4,876/4,876 non-null on CSD).

**PASTE 1 — the eligibility rule.** The matrix has 54 columns; 13 are trained on. The other
41 are contemporaneous with the target: `corr(sales_units, sales_value) = 0.897` in the same
row. The trained columns are time-safe by construction — `lag_1` at *t* equals `sales_units`
at *t−1* (verified by printing consecutive rows); `promo_intensity`, `zero_run_flag` and
`zero_run_length` are `.shift(1 + horizon)`; calendar features are known ahead. Read from
`engineer_features.py`, not from comments.

**PASTE 2 — the rejected reduction.** From
`05_thesis_results/05_model_benchmark/tables/98_feature_redundancy_reduction.md`: 16→9
features, WMAPE 26.44 → 28.82, rejected. VIF table is `97_feature_collinearity_vif.md`.

**PASTE 3 — skewness, all four categories.** Volume features (the nine lag/rolling columns),
raw vs `log1p`:

| Category | raw skew range | logged skew range |
|---|---|---|
| CSD | 4.96 – 7.98 | −0.16 – 0.04 |
| Danskvand | 3.87 – 10.39 | −0.39 – −0.19 |
| Energidrikke | 3.65 – 8.88 | −0.44 – −0.08 |
| RTD | 4.48 – 7.07 | 0.01 – 0.39 |

Non-volume features, all categories: `month` 0.07–0.17, `quarter` 0.05–0.17, `peak_month`
0.67–1.12, `promo_intensity` 0.30–0.67 — all below 2, none transformed.

This **confirms the existing implementation exactly**: the nine volume features are the ones
`LOG_SCALE_FEATURES` log-scales for Ridge, and the four others are the ones it leaves alone.
The hand-written tuple and the measured partition are the same set.

> Note on the existing skewness tables: `step_2_02_skewness.md` reports skewness for all four
> categories, but only for **raw Nielsen measures** — `sales_value`, `weighted_dist` and so
> on. No `lag_*` or `rolling_*` column appears in it. The figures above are for the features
> actually modelled, which had never been measured anywhere.

## What the EDA diagnostics drive

| Diagnostic | Consumed? | What happens |
|---|---|---|
| Target skewness | **Yes** | skew 5.00 → every model trains on `log_sales_units` |
| Collinearity (VIF) | **Reported** | measured per category; nothing dropped on it, deliberately |
| Redundancy + permutation importance | **Yes, and rejected** | 16→9 tested, WMAPE worsened, retained |
| Per-brand ADF recommendation | No | `recommendation` column read by nothing |
| Per-measure skewness interpretation | No | issued for ~30 columns, 29 of them ineligible |
| Raw-measure correlation pairs | No | every pair is between ineligible columns |
| ACF consensus lags | No | lag set comes from `derive_lag_structure(horizon)` |
| Structural breaks | No | `break_detected` written, never read |

Five of these report on the raw Nielsen measures — columns that were never eligible, so
their recommendations were never live. The defect is that the EDA **issues imperatives for
columns it has already excluded**, which is what makes the chapter look as though it ignored
its own evidence. The two diagnostics that bear on the modelled features were computed, and
the reduction they implied was tested and rejected on measured evidence.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

**Not traced.** Which brand-count number belongs in which Chapter 4 table. The matrices say
106/30/50/72; earlier notes say 95/29/44/62. Flagged above, not fixed.

**Not fixed, code hygiene only.** `pipeline_config.py:218` claims structural-break and
ADF-per-brand outputs "feed data-handling decisions". Both halves are false. One line, no
dependencies, tracked in P0051. Does not affect any prose above.

**Optional, changes no results.** Replacing the literal `FEATURES` list with a filter that
derives the eligible set and asserts it reproduces the same 13 would make the rule
executable rather than merely documented. Not needed for submission.
