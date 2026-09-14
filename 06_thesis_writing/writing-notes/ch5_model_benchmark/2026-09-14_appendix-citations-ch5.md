---
name: 2026-09-14_appendix-citations-ch5
description: NOTE - Which generated artefacts Chapter 5 can cite. Twenty-six tables and six figures sit behind a chapter that already carries thirteen body tables; the question here is which of the unused ones close an evidence gap rather than add bulk.
category: workflow
applies-to: [ch5_model_benchmark]
triggers: [ch5 prose pass, appendix placement, benchmark tables, SHAP figures, figure placement]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written
---

# Chapter 5 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**This chapter is already table-heavy.** It carries Tables 5 through 17 in the
body — thirteen of the document's twenty-three. So the bar here is higher than
elsewhere: an artefact earns a citation only if it closes an evidence gap, not
because it exists.

**The chapter itself is current.** Its benchmark table matches `cv_summary.md`
row for row, including the energidrikke 11.5 / 16.2 pair and RTD's n = 372. No
repair needed.

---

# What this chapter owns

Twenty-six tables and six figures. The ones already reflected in body tables are
omitted below; these are the **unused** artefacts.

| Artefact | Last regenerated | Notes |
|---|---|---|
| `residual_diagnostics.md` | **2026-09-14** | newest artefact in the repo, uncited |
| `97_feature_collinearity_vif.md` | 2026-09-10 | unindexed |
| `98_feature_redundancy_reduction.md` | 2026-09-10 | unindexed |
| `99_ridge_alpha_cross_validation.md` | 2026-09-10 | unindexed |
| `94_holiday_ablation_tuned.md` | 2026-09-10 | unindexed |
| `95_holiday_ablation_tuning_sensitivity.md` | 2026-09-10 | unindexed |
| `96_holiday_shap_attribution.md` | 2026-09-10 | unindexed |
| `01_metric_dictionary.md` | 2026-09-11 | indexed |
| `06_retraining_cost.md` | 2026-09-11 | indexed |
| `08_parameter_drift.md` | 2026-09-11 | indexed |
| `training_report.md` | 2026-09-10 | unindexed |
| `demand_classes.md`, `mase.md`, `pooled_*.md`, `ridge_pooled.md`, `stability.md`, `calibration.md`, `profiling.md` | 09-09 → 09-11 | mostly reflected in body tables |
| `ch5_model_selection_v2.svg` | 2026-09-10 | current, correct winners, uncited |
| `ch5_resource_profile_v2.svg` | 2026-09-10 | uncited |
| `ch5_modelling_pipeline_v1.svg` | 2026-09-10 | uncited |
| `fig1_model_ladder.svg` | 2026-09-10 | uncited |
| `fig3_forecast_overlay.svg` | 2026-09-10 | uncited |
| `shap_importance.svg` | 2026-09-10 | uncited |

---

# R1 — The residual diagnostics table closes a limitation the chapter states

**The artefact.** `residual_diagnostics.md`, written this morning. Ljung-Box on
ARIMA residuals at lag 24, with the Hyndman & Athanasopoulos degrees-of-freedom
correction (`K = p + q = 2`), applied in log space, rejection rates per category.

**Recommendation: appendix, cited from §5.5 Results where the statistical
baselines are discussed.**

**Why this is the top item.** It is a diagnostic an examiner familiar with
forecasting will expect and will not find. The table is careful in exactly the
way that earns credit: it explains why the correction matters, why the test is
applied to ARIMA rather than to the boosted models, and why the first residual is
dropped. The reasoning is already written.

**It is also the newest artefact in the repository and cited nowhere.** No chapter
mentions Ljung-Box or a portmanteau test. If it is not cited it was work done for
nothing.

**One caveat to carry into the sentence.** The test is on **in-sample** residuals,
which the table states. Say so in prose too, or an assessor will.

---

# R2 — The feature-reduction trio answers "why 18 features and not fewer"

**The artefacts.** VIF by feature and category, the redundancy-based reduction
that was tested and rejected, and the ridge alpha cross-validation.

**Recommendation: appendix, as one block, cited once from §5.3 Experimental
setup.**

**Why.** A reader looking at a wide matrix and a short panel asks whether the
feature set was pruned and on what basis. These three tables answer it with
measurement: collinearity was quantified, a reduced set was constructed and
tested, and it performed worse.

**Table 98 is the valuable one** precisely because it records a **negative
result** — a reduction that was tried and did not work. Negative results are
cheap to report and expensive to leave out, because their absence reads as
something not attempted.

---

# R3 — The holiday ablation belongs here, not in Chapter 4

**The artefacts.** Tuned ablation, tuning sensitivity, SHAP attribution of the
calendar features.

**Recommendation: appendix, cited from §5.5.**

**Why here and not Chapter 4.** Chapter 4 documents where the calendar came from
and what was derived (see the Ch4 note, R2). Whether those features *helped* is a
benchmark result and belongs with the benchmark.

**Read the two ablations carefully before citing.** They answer different
questions: one is untuned and one is independently tuned, and they disagree in
direction. Cite the tuned one, and if both are referenced say explicitly which
question each answers. A reader who finds the other one unaided will read the
discrepancy as an error.

---

# R4 — Figures: two earn the body, four do not

| Figure | Recommendation | Reasoning |
|---|---|---|
| `ch5_model_selection_v2.svg` | **in text, §5.6** | §5.6 is the model-selection decision; this figure *is* that decision, and it reads its winners live from the deployed metadata. Verified correct: XGBoost for CSD and water, LightGBM for energy drinks and RTD |
| `ch5_resource_profile_v2.svg` | **in text, §5.4 or Ch6 §6.8** | peak fit memory per model against the envelope. The memory constraint is load-bearing for the whole thesis and is currently carried entirely by numbers in prose |
| `shap_importance.svg` | appendix | interpretability evidence, supports §5.5 but does not carry it |
| `fig1_model_ladder.svg` | appendix or drop | duplicates Table 10's content as bars |
| `fig3_forecast_overlay.svg` | appendix | one brand, one window — illustrative rather than evidential |
| `ch5_modelling_pipeline_v1.svg` | appendix or drop | overlaps Chapter 4's pipeline figures |

**On the resource-profile figure.** Chapter 6 §6.8 also has a claim on it. Decide
once; my view is Chapter 5, because the measurement is a benchmark output and
Chapter 6 can reference it.

**Provenance note on `fig1_model_ladder`.** Its model ladder is typed as
`["SeasonalNaive", "Ridge", "LightGBM", "XGBoost"]` rather than read from the
metrics file. Its title and verdict *are* computed — it correctly reports that
Ridge loses to SeasonalNaive on RTD. If a fifth model is ever added to the
benchmark, this figure will silently omit it.

---

# R5 — The metric dictionary should be referenced, not restated

**Recommendation: appendix, referenced from §5.4 Evaluation metrics.**

§5.4 defines metrics in prose and carries Table 6. The generated dictionary is
written by the same run that computes the numbers, so it cannot drift.

The Chapter 3 note makes the same recommendation for §3.5. **One appendix entry,
two references** — that is the right outcome, and it removes a place where the
same definitions are written twice and can disagree.

---

# R6 — Leave these uncited

`training_report.md` duplicates content already in body tables.
`06_retraining_cost.md` and `08_parameter_drift.md` are operational rather than
evidential — they belong to the Chapter 6 deployment argument if anywhere.
`demand_classes.md`, `mase.md` and the pooled tables are already reflected in
Tables 7, 8, 11 and 12.

---

# Summary of what I would apply

| # | Artefact | Placement | Confidence |
|---|---|---|---|
| R1 | residual diagnostics | appendix | high |
| R2 | VIF + redundancy + ridge alpha | appendix, one block | high |
| R3 | holiday ablation (tuned) | appendix | medium, read the caveat |
| R4a | model selection figure | **in text §5.6** | high |
| R4b | resource profile figure | in text, chapter TBD | medium |
| R5 | metric dictionary | appendix, shared with Ch3 | high |
