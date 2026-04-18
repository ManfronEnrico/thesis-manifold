# Future Work — Thesis Extensions Parked for Later

## System D — Feature-layer Indeks integration

**Status**: not implemented. Parked as future work / thesis extension.

**Motivation**: SRQ3 phrasing covers "predictive and decision-support capabilities". The
current work (System B + C) addresses the decision-support dimension via context
injection at the recommendation agent layer. An alternative path integrates Indeks
context at the **feature layer** of the predictive model itself, answering whether
heterogeneous contextual data improves forecast accuracy (not just recommendation
quality).

**Proposed implementation**:
1. Pre-compute regional demographic aggregates from Indeks (mean age, urban %, income
   tier) for the 7 retail regions.
2. Use the hardcoded brand → target region mapping (same as System C) to attach a
   demographic feature vector to each (brand, channel, month) row in the feature
   matrix.
3. Retrain LightGBM with walk-forward CV on the augmented feature set.
4. Measure TEST per-brand DVH MAPE; compare to the baseline 23.54% from SRQ1.

**Expected outcome range**: marginal to small improvement (0–2 pp on MAPE). Reasons:
- The LightGBM already captures heavy brand × channel heterogeneity via SHAP-confirmed
  drivers (lag_1, weighted_dist, rolling_mean_*, brand_mean_sales).
- Indeks is cross-sectional (survey snapshot), so the signal added to a time-series
  forecast is weak unless region changes materially over the 42-month window.
- The brand → region mapping is a proxy; real brand-specific demographic signal
  would require Indeks brand-awareness data that is sparse in the available extract
  (only PEPSI and FAXE KONDI have direct references).

**Thesis value regardless of outcome**:
- *Positive result (≥1 pp MAPE reduction)*: strengthens SRQ3 to cover both
  decision-support AND predictive accuracy dimensions.
- *Null result (<0.5 pp change)*: defensible as methodological rigor — confirms that
  the recommendation-layer integration was the correct architectural decision for
  the given data constraints.
- *Negative result (MAPE rises)*: rare but would document a caveat about
  cross-sectional-to-time-series feature fusion with weak spatial mapping.

**Estimated effort**: ~2 hours (feature pre-computation, pipeline update, retrain,
test eval, commit).

**Owner decision (2026-04-18)**: deferred. Keep as backlog for post-defence
iteration if time permits. Do NOT block the thesis timeline on this.

## Other possible extensions

- **SRQ4 — comparison vs traditional descriptive BI**: not yet addressed. Would
  require identifying a baseline descriptive-analytics tool and running a
  side-by-side evaluation on the same query set.
- **Statistical significance testing**: Wilcoxon signed-rank on the 20-query A/B/C
  panel would strengthen the quantitative claims (currently descriptive only).
- **LLM-as-judge evaluation**: richer recommendation quality scoring beyond the
  regex-based heuristics used in §8 and §10b.
- **Indeks brand-specific columns**: the current System C uses only demographic
  aggregates. The codebook contains 12 brand-specific references (PEPSI 4, FAXE
  KONDI 8). A targeted extraction could provide brand-direct Indeks signals for
  the subset of brands covered.
- **Full regional forecast model**: retrain the pipeline at (brand × region × month)
  granularity if Nielsen ever exposes regional sub-markets with real fact data.
