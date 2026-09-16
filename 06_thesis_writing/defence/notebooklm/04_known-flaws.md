# Known flaws, and the answer to each

> **Source file for NotebookLM.** Written for quiz and multiple-choice
> generation, so each flaw is stated as a defect, a cause, and an answer.
>
> ⚠ **Every item here is either already conceded in the submitted thesis or is
> immaterial to its conclusions.** Nothing in this file is a discovery that
> changes a finding. That distinction is the point: a thesis that knows its own
> defects is in a stronger position than one that does not.

## Why this file exists

CBS states that the oral defence is an opportunity to "correct (significant)
flaws". The thesis already states most of these in its limitations. The purpose
of rehearsing them is to be able to answer in twenty seconds, from memory,
without the defensiveness that comes from being surprised.

---

## 1. The lag set contains no multiple of twelve

**The defect.** On monthly data, "the same month last year" is twelve months
back. The feature matrix ships `lag_13` and `rolling_mean_13`. No element of the
lag set `(1, 2, 3, 4, 8, 13)` is a multiple of 12.

**Why it is the strongest item on this list.** The project measured 12,
documented 12, benchmarks with 12 — and engineered 13:

| Layer | What it says |
|---|---|
| ACF analysis, 20 leading brands across 4 categories | lag 12 significant for **20 of 20**; lag 13 for 10 of 20, and **never without 12 also significant** |
| The EDA table's own note | "significance at lag 12 indicates annual seasonality" |
| The parameter contract's provenance field | "the lag-12 term is retained because the autocorrelation analysis finds it significant" |
| The seasonal-naive baseline | reads `hist[-12]` — twelve months back |
| A code comment in the training report | describes `lag_13` as "same month last year" — which is 12 |
| **The shipped feature matrix** | **`lag_13`** |

One of the three brands in the experiment, HARBOE, has significant lags
`[1, 2, 3, 9, 12, 15]` — lag 12 significant, lag 13 **not**.

**The cause.** A provenance failure between pipeline stages. No contract existed
between the analysis layer and the engineering layer: the exploratory analysis
wrote reports for human readers, and the feature builder read a hardcoded
configuration. Nothing connected them, so a correct diagnostic and an
inconsistent feature could coexist without either being revised.

**The answer.** This is a recognised class of defect rather than unfamiliarity
with forecasting methodology — and it demonstrates the thesis's own SRQ2
argument from the negative case: a forecast is auditable only if its features
carry their justification.

**Concede the narrower point immediately.** No contract was *needed* to notice
that 13 is not a multiple of 12. If the lag set was inherited from an earlier
weekly-grain prototype and never re-derived when the grain became monthly, say
so plainly — but say "most likely", because that has not been confirmed.

**The fix is strictly favourable, which is worth knowing.** Because the
eligibility threshold is derived as `warmup + horizon + 1`, changing 13 to 12
lowers the history requirement by one month, so it **admits more brands** rather
than fewer. It corrects the phase error and improves sample size at once. It
also strengthens the thesis's existing Prophet argument, which claims the
tabular models already capture annual seasonality.

**Where the thesis says it:** Chapter 9, Section 9.4, limitations.

---

## 2. MASE uses a non-seasonal denominator on a seasonal panel

**The defect.** MASE scales forecast error against a naive benchmark's error.
The source defines that denominator with the seasonal period *m* for a seasonal
series — 12 for monthly data. The implementation computes a first difference,
i.e. *m* = 1.

**The visible symptom.** Seasonal naive scores *worse* than naive on MASE in
every category. With an *m* = 1 denominator, that is the expected outcome, not a
finding about the data. Every model is scaled against the one-step naive error,
which flatters naive-1 by construction and penalises any method whose skill is
seasonal.

**The internal contradiction that proves it.** The same script scores a lag-12
benchmark with a lag-1 denominator: `run_seasonal_naive` correctly reads twelve
months back, while the MASE denominator takes a first difference.

**The answer, and concede it as permanent.** The choice of MASE over MAPE is the
source's own — percentage errors need a test set large enough "especially in the
denominator". The implementation of the denominator is wrong. It is **not under
repair**, because changing it would re-score every category and every model,
which is not a late edit. The thesis reports MASE honestly on the denominator it
used.

**What this costs, and it is bounded.** Chapter 5 must not cite the source's
seasonal sentence, because that would quote a rule the chapter breaks three
lines above a table reporting a seasonal-naive MASE. The safe half of the
source — the preference for scaled over percentage errors on a small test set —
*is* cited and is correct. Chapter 5 handles the disagreement well, reporting it
as "surfaced rather than resolved by picking one".

---

## 3. The fitted ARIMA carries no seasonal order

**The defect.** `SARIMAX(order=(1,1,1))` with no seasonal component, on a panel
the repository's own docstring describes as "monthly beverage demand with strong
annual seasonality". The orders are fixed rather than selected, no information
criterion is computed anywhere, and `enforce_stationarity=False` disables a
guard the source says should always apply.

**The cause, stated plainly.** The statistical baselines were implemented
without `pmdarima` available, so the order was fixed rather than selected. The
module's own docstring records "no pmdarima".

**Demonstrated, not merely admitted.** A Ljung-Box test on the ARIMA residuals
rejects white noise for a substantial share of series, and the remaining
autocorrelation is concentrated at the **seasonal lag**: median ACF(12) of
**+0.361** among rejecting brands against **+0.064** among non-rejecting.
Overall rejection rate 22.2% over 230 series. That is the seasonal-order
limitation measured rather than asserted.

**The mitigating sentence is the source's own:** "it is not possible to find a
model that passes all of the residual tests… we would normally use the best
model we could find, even if it did not pass all of the tests."

**One honest caveat about the test itself.** The gate runs on **in-sample**
residuals where the source prefers cross-validation residuals. In-sample
residuals are optimistically clean, because the fitted parameters have already
absorbed some of the structure the test looks for — so the rejection rates are
**lower bounds**, and structure detected under an optimistic test is genuinely
there. The seasonal localisation is unaffected, because it is a contrast rather
than a level and both halves are computed identically, so the optimism cancels.
This limitation is stated on the emitted results table itself.

**Where the thesis says it:** Chapter 5 admits it; Chapter 9 §9.4 and §9.5 make
adding a seasonal term explicit future work.

---

## 4. The confidence index discriminates nothing

**The defect.** Two independent faults. The forecast value cancels out of the
relative interval width, leaving a function of the per-category quantile alone.
And the second term assumes a quantile bounded near one, when the measured
values are 1.89 to 2.69 — so that term is **identically zero**. Four attainable
values exist across all brands, and all tier "Low".

**Why it is not repairable by recalibration.** The problem is not where the
thresholds sit; it is that the quantity being thresholded does not vary within a
category. Re-tiering four constants yields a category label wearing a number.

**Why it shipped.** Published experiment runs are scored against it.

**The answer.** The thesis reports this as a finding rather than hiding it as an
omission, and the reporting is what makes the chapter's real claim: the interval
does not carry the reliability of a forecast — the measured track record
travelling in the same payload does.

**An unexpected defence, worth having ready.** In the combined scenarios both
agents departed from the model's forecast and cited its confidence tier and
interval width as the reason. A constant "low" was, on that brand, the honest
signal — and it changed behaviour. That is the uncertainty channel working even
through a broken index.

---

## 5. Two different peak-memory figures appear in the submitted thesis

**The defect.** Chapter 9 reports XGBoost at 34.5 MB and LightGBM at 17.9 MB.
Chapter 6's per-component budget table reports 31.9 and 14.9, and Chapter 7
follows Chapter 6.

**The cause.** Two profiling runs at different dates, never reconciled. The
results artefact on disk agrees with Chapter 9.

**Why it changes nothing.** The argument is a hundredfold margin against a
4096 MB ceiling. 34.5 MB is 0.84% of budget; 31.9 MB is 0.78%. Either figure
supports the same conclusion by three orders of magnitude.

**The answer.** Name it as two measurement runs, say which one the results
artefact carries, and do not claim the difference is meaningful. Do **not** claim
it was noticed before submission.

---

## 6. Prediction intervals attain coverage and are too wide to use

**Not a defect — a designed negative result.** Listed here because it is the
most likely line of attack on SRQ2.

At 90 per cent the interval spans 8 to 34 times the quantity forecast, and no
category yields an actionable interval. At 80 per cent it narrows to 3 to 4
times for three of four categories, at the cost of coverage that is measured
rather than guaranteed. Energidrikke has no operating point at either level.

**The honest framing.** The marginal guarantee holds — 83.9 to 91.7 per cent
against a 90 per cent target. The width is the cost of one pooled quantile over
brands spanning six orders of magnitude with few validation months each. Three
alternative schemes were implemented and measured; none improved coverage and
width together in more than two of four categories, which is the signature of a
sample-size limit rather than a modelling choice.

**A tested negative result is a contribution.** The answer is stronger for
naming what was tried and failed than for defending the width.

**Danskvand's shortfall has a named cause:** the guarantee assumes
exchangeability, monthly demand violates it, and Danskvand is where the
violation shows.

---

## 7. Two of four categories are beaten by a parameter-free benchmark

**Not a defect — a reported qualification.** Seasonal naive wins CSD (19.2) and
RTD (27.3); Prophet wins Danskvand (19.4). Both gradient boosters nonetheless
beat Ridge and ARIMA in every category, and those differences exceed the seed
noise.

**The answer.** That a benchmark costing nothing to compute beats the substrate
in two of four categories is the most important qualification the thesis places
on its own work, and it is reported rather than absorbed. It is also why the
thesis does not claim a general accuracy result.

---

## 8. The two gradient boosters are statistically indistinguishable

**Not a defect — the finding.** A five-seed sweep changes the selected model in
all four categories. The gap between families is 0.3 to 1.2 percentage points;
the between-seed standard deviation reaches 2.81.

**The answer.** The defensible claim is that they are indistinguishable on this
data, which is weaker than naming a winner and more useful: a practitioner may
choose on training time, memory footprint or tooling maturity without forfeiting
accuracy.

---

## 9. Model selection uses cross-validation where test performance disagrees

**Looks like an error until explained.** On test, XGBoost wins everywhere; on
cross-validation, Energidrikke and RTD select LightGBM.

**The answer.** Selecting on the test split is selection on the evaluation set,
which biases every number downstream of it. Cross-validation selection is the
defensible choice even though it picks a different model in two categories.

---

## 10. The panel is hierarchical and nothing is reconciled

**Stated in the limitations.** Brands sit within categories and categories
within markets, so the data is a mixed hierarchical and grouped structure.
Forecasts produced independently at brand level are not guaranteed to sum to a
category-level forecast, and the thesis reconciles nothing.

**Two consequences, both stated.** Established reconciliation methods would very
likely improve accuracy at every level by borrowing strength across the
hierarchy. And the back-transformed point forecasts are **medians rather than
means** — so summing brand forecasts to a category total would be biased even
before reconciliation, because medians do not add.

---

## 11. Post-hoc clipping where the source prescribes a transformation

**A departure the thesis already names as one.** The substrate constrains
implausible forecasts *after* back-transformation. The principled alternative is
to impose the constraint through the transformation itself, which applies the
bias adjustment automatically and preserves interval coverage.

---

## 12. Design principles are derived, not validated

**Stated in Chapter 10's limitations.** The thesis completes **one** design
science cycle.

**The answer.** One cycle is what a thesis-scale DSR study delivers. The
principles are stated at the level of a problem class and each carries an
evidence column, which is what makes them falsifiable rather than asserted —
each is claimed because something in the evaluation would have come out
differently had it not held. Validation across contexts is named as further
work, not implied.

---

## What is NOT wrong, recorded so it is not conceded by accident

| Item | Status |
|---|---|
| Uniform `log1p` transformation | **A defended design choice**, not an oversight. The tests that would drive per-series selection have limited power at 46 observations, and uneven transformation would make feature semantics inconsistent across the panel. Do not concede this. |
| Prophet's configuration | **Checked and correct.** Annual seasonality on by name, weekly and daily off by name. Nothing relies on a daily-tuned default. |
| Comparing ARIMA against gradient boosting on a test set | **The correct method.** Information criteria cannot compare across model classes; the source prescribes exactly this. |
| Tuning on WMAPE rather than RMSE | **Principled.** MAE and RMSE are minimised by different functionals, so the pipeline tunes once per objective. |
| Scoring a single month at exactly the horizon | **A deliberate strength** the prose does not claim: averaging across horizons would combine unequal variances. |
| The pooled/per-category training grain | **A defended choice** with precedent — a large competition found cross-learning superior to series-by-series training at scale. One model per brand is also not a small-business memory budget, and could not serve a brand with no history. |
