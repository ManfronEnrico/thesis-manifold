---
name: findings-feature-reduction
pid: P0051
created: 2026_09_08-19_20
updated: 2026_09_08-19_20
status: investigation-complete
---

# Why the matrix has 54 columns and training uses 13

Traced 2026-09-08 in the code, not from comments. Written to answer one question:
**was the reduction from ~54 columns to 13 a method, or a guess?**

**Answer: it was a method, applied in three stages, each with a stated and mostly
measured rationale. But the stages are not written down in one place, two of them
were never re-examined after the data changed, and the appendix table reports a
number that contradicts the training code.**

---

## 1. What "contemporaneous" means, and why it excludes a column

A forecast made at origin *t* predicts *t+H*. A column is **contemporaneous** if its
value describes the same month being predicted.

`sales_value` for October is October's revenue. If the model is predicting October's
units, handing it October's revenue means handing it the answer — those two quantities
are the same trading month measured in different units. At forecast time in July, nobody
knows October's revenue. The column exists in the matrix only because the data was
recorded historically.

**This is not a statistical preference; it is a timing fact.** The project measured what
it buys:

```
CSD H=3, LightGBM 300 trees:
  base features                      WMAPE 17.20%
  base + sales_value + sales_liters  WMAPE 15.02%
```

A 2.2pp "improvement" bought entirely by letting the model read the month it forecasts.
That number is the evidence for the exclusion — it is what leakage looks like when
measured. (`step_6_save_outputs.py`, above `CONTEMPORANEOUS_COLS`.)

The fix for a useful contemporaneous measure is to **lag it**, not to admit it.
`promo_intensity` is exactly that: built from `promo_units` but `.shift(1 + horizon)`,
so at *t* it describes *t−1*, which a forecaster genuinely knows.

---

## 2. The three stages of the reduction

| Stage | Where | 54 → | Basis |
|---|---|---:|---|
| A. Contemporaneous exclusion | `step_6_save_outputs.py` `CONTEMPORANEOUS_COLS` | 34 | Timing + measured leakage (2.2pp) |
| B. Structural/unlagged exclusion | `srq1_benchmark.py` `FEATURES` | 13 | Measured accuracy test, 1 of 21 documented |
| C. Redundancy reduction | `srq1_feature_diagnostics.py` | rejected | Tested 16→9, WMAPE 26.44 → 28.82 |

### Stage A — 54 → 34 (documented, measured, sound)

12 named columns are dropped: same-month sales in kroner/litres/units, the promoted-unit
count, and Nielsen's baseline estimates. Rationale and the 17.20/15.02 measurement are in
the code. **This stage is defensible as-is.**

Note the *rule shape*: the manifest is built as
`everything NOT in NON_FEATURE_COLS and NOT in CONTEMPORANEOUS_COLS`. It is a
**denylist** — any column not explicitly named falls through and is labelled a feature.
That is why the manifest says 34.

### Stage B — 34 → 13 (this is the weak link)

`srq1_benchmark.FEATURES` is a hardcoded list of 13. The 21-column gap breaks down as:

| Group | n | Documented? | Time-safe? |
|---|---:|---|---|
| Distribution + promotional structural measures | **16** | **only `weighted_dist`** | No — unlagged, contemporaneous |
| Holiday calendar (`days_in_month`, `n_holidays`, `non_holiday_days`) | 3 | as an ablation | **Yes** |
| `zero_run_flag`, `zero_run_length` | 2 | **no** | **Yes** — shifted |

**`weighted_dist` is the one that was done properly** (P0036 task 7, 2026-08-19). It was
tested with/without/lagged across 4 categories and 3 seeds:

```
category       without    with    lagged
CSD             17.20%   18.24%   18.32%
Danskvand       33.39%   34.36%   32.89%
Energidrikke    17.40%   16.94%   16.86%
RTD             31.83%   32.54%   31.26%
```

Worse in 3 of 4 → excluded. That is a measured decision with an audit trail.

**The other 15 distribution/promotional columns were never individually tested.** They
share `weighted_dist`'s defect — unlagged, contemporaneous, describing the forecast month
— so excluding them is *correct by the same timing argument as Stage A*. But that argument
lives in a comment about a different column. **They are excluded by a rule that was never
written down.**

⚠ **This is the honest gap.** The exclusion is right; the justification is inherited
rather than stated.

### Stage C — the reduction that was tested and rejected

`srq1_feature_diagnostics.py` (2026-09-06) computes VIF, Spearman redundancy clusters and
permutation importance on the validation split, then proposes a reduced set. Result:
16 → 9 features raised mean test WMAPE from **26.44 to 28.82**. Rejected.

This is the strongest methodological artefact in the whole chain — a data-driven
reduction, evaluated honestly, and declined on evidence.

---

## 3. Two defects to fix

### D1 — the appendix table states a false number

`05_thesis_results/04_data_assessment/tables/04_feature_matrix.md` caption:

> "…in 54 columns, of which **34 are model inputs**."

**False.** 34 is the manifest's denylist count (Stage A). Models consume 13. The table's
generator (`export_appendix.py::table_feature_matrix`) reads `manifest["features"]` and
never reads `srq1_benchmark.FEATURES`, so it cannot see the Stage-B reduction.

Consequence: the table labels 16 distribution/promotional columns "Feature – distribution"
and "Feature – promotional" when no model has ever seen them. An assessor reading this
appendix would conclude the model uses same-period distribution data — the exact
misreading the generator's own docstring says it exists to prevent.

The generator's docstring even records the drift — *"13, then 14, then 16, now 34"* — and
resolved it by counting the manifest. It counted carefully, but counted the wrong list.

**Fix:** have the table read the trained list and add a role distinguishing *built but not
trained* from *excluded — contemporaneous*.

### D2 — holiday features are built but not trained

`days_in_month`, `n_holidays`, `non_holiday_days` are time-safe (calendar facts, known
years ahead) and populated 100%. They are **not** in `srq1_benchmark.FEATURES`. They enter
only `srq1_holiday_ablation_tuned.py`, which appends them for the with-holiday arm.

**"Ablation" = train the model twice, with and without a feature group, and report the
difference.** It is how you measure whether a feature earns its place. Here it is used as
a *side experiment* rather than as the gate on the main model — so the headline benchmark
never sees the holiday features, whatever the ablation concludes.

⚠ **This matters for the VPS run.** Stage 4 of `run_both_horizons.py` runs
`holiday_ablation` and `holiday_tuned`. Those will report the holiday effect. But
`srq1_benchmark`, `srq1_benchmark_tuned` and everything downstream — including
`train_persist`, which is what SRQ2 serves — train on the 13 without them.

**If the ablation shows holiday features help, the headline models still will not use
them unless `FEATURES` is edited.** Decide before the run finishes, not after.

`zero_run_flag`/`zero_run_length` are in the same position: time-safe, built, never
trained, never tested. Lower stakes — they are sparse-series diagnostics — but the
omission is equally undocumented.

---

## 4. What should have been done, and what to do now

**Textbook order:** eligibility filter (leakage) → redundancy/collinearity → importance →
validated reduction → final set. Every exclusion recorded against a rule or a measurement.

**What exists:** all four stages exist. Stage A is measured. Stage C is measured and is
genuinely strong. **Stage B is a hand-maintained list in which 1 of 21 exclusions was
tested and the rest inherit an unstated rule.**

Given the timeline, in priority order:

| # | Action | Cost | Why |
|---|---|---|---|
| 1 | Fix the `04_feature_matrix.md` caption + roles | ~30 min | An assessor reads this table; it currently says something false |
| 2 | Write the three-stage rule into Ch4 | prose | Turns an apparent guess into a stated method |
| 3 | Decide the holiday question before the VPS run lands | decision | Determines whether the ablation changes the headline set |
| 4 | *(optional)* Replace `FEATURES` with a derived eligibility filter | ~1 h | Makes the rule executable; changes no results |

**No retraining is required for 1, 2 or 4.** Item 3 is a genuine decision, not a cleanup.

**Do not** attempt a fresh data-driven selection over all 34 in the time remaining. Stage C
already tested reduction and it made results worse; re-opening selection now would
invalidate every committed number for no expected gain.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

**Verified in code, not comments:** `CONTEMPORANEOUS_COLS` and the manifest comprehension
(`step_6_save_outputs.py:111-183`); `FEATURES` parsed from `srq1_benchmark.py:171`;
`_arm_features` in `srq1_holiday_ablation_tuned.py`; `_fm_role` +
`table_feature_matrix` in `export_appendix.py:1186-1265`; manifest/trained diff computed
against `csd_manifest_h3.json`.

**The 17.20/15.02 and weighted_dist numbers are quoted from code comments** and were NOT
independently re-measured. They are internally consistent (17.20% appears as the base in
both) but should be re-verified before either enters prose as a cited figure.

**Not checked:** whether the other three categories' manifests contain the same 34, or
whether the promo-zero categories (danskvand, RTD) shift the counts. CSD only.

---

# Part 2 — the methodology, reviewed against the thesis's actual proposition

Added 2026-09-08 after Brian restated the research framing. Part 1 above was written
assuming the holiday work needed defending as a finding. **It does not, and that changes
the recommendation.**

## The proposition this thesis actually tests

> Whether **trained models help an LLM forecast** — not whether exogenous variables
> improve models.

SRQ1 exists to produce a *defensible, literature-consistent* forecasting artefact. It is
the instrument, not the result. SRQ2 exposes it through a tool interface; SRQ4 compares
plain LLM (A) vs LLM + data & code (B) vs LLM + trained models (C).

**Consequence: feature-level effect sizes are not thesis claims.** They are build
decisions. This reframes three things in Part 1.

## R1 — The ablation should not be a reported result

An ablation answers "does this feature group earn its place?" That is a question about
*feature contribution*, which is not an SRQ. Reporting it invites an examiner to evaluate
the thesis on a claim it never set out to make, and it competes for space with SRQ4.

**The literature motivates the *direction*, not the specific feature.** M4 and M5 identify
explanatory (exogenous) variables as the open frontier in forecasting practice — that is a
claim about exogenous inputs generally, **not** a prescription for holiday calendars, which
neither competition specifies for this setting. The holiday calendar is *one instance* of
that direction, chosen because it was constructible at monthly grain from a free source.

So the defensible framing is: the thesis takes up M4/M5's explanatory-variable direction at
the scale it actually did — **one calendar source, monthly grain**. Adopting an exogenous
input on that basis is a design choice consistent with the cited direction; it is not a
claim that the literature prescribed this feature, and it must not be written as one.

**Recommendation:** holiday features belong in the feature matrix **by design, from the
start**, justified by citation. The ablation scripts (`srq1_holiday_ablation_tuned.py`,
`srq1_holiday_ablation.py`) should not produce a reported table.

⚠ **This means `FEATURES` should include the three holiday columns**, so the headline
benchmark trains on the enriched set — which is the design the thesis intends and what
the data chapter will describe. Currently it does not, which is the D2 defect in Part 1.

**On "we added it too late":** the *code* handles this correctly. `derive_holiday_enrichment()`
in `step_3_derive_params.py` is a contract-level decision point with an explicit flag and a
stated reason, and step 4 reads the flag rather than deciding for itself. A run can always
say whether its numbers came from an enriched matrix. So the late addition is a
**sequencing regret, not a validity problem** — the matrices carry the features, populated
100%, and a rerun with them in `FEATURES` produces exactly the literature-consistent
artefact intended from the start.

## R2 — Brian's stated EDA order is correct, and is close to what exists

The proposed order, checked against standard practice:

| Step | Brian's framing | Correct? | State in repo |
|---|---|---|---|
| 1 | Engineer features (lags, rollings, calendar) | ✔ | `engineer_features.py` |
| 2 | Enrich with exogenous data (holiday API) | ✔ | built, **not in `FEATURES`** |
| 3 | Correlation matrix → drop one of each correlated pair | **partly** — see below | measured, reduction rejected |
| 4 | Split train/val/test | ✔ | chronological, correct |
| 5 | Train; assess feature importance | ✔ | permutation importance on validation |

**One correction to step 3.** Dropping one member of every correlated pair is a
*linear-model* convention. It is right for Ridge, where collinearity inflates coefficient
variance. It is **not** right for gradient-boosted trees, which split on whichever
correlated feature is locally most informative and lose real signal when the others are
removed.

The project measured exactly this and the measurement should be trusted over the
convention: the redundancy-based reduction (16 → 9) **raised** mean test WMAPE from
**26.44 to 28.82**. Adopting the textbook rule would have made every reported number worse.

**So the correct methodological statement is:** correlation was measured, a reduction was
derived from it, the reduction was evaluated against held-out performance, and it was
rejected on evidence. That is *stronger* than applying the rule, and it is a defensible
answer to "why didn't you drop correlated features?".

## R3 — What the reduction chain should say in Chapter 4

Three stages, all defensible once written down:

1. **Eligibility (leakage).** A column is admissible only if knowable at forecast time.
   Excludes same-month sales, baselines, and the unlagged distribution/promotional block.
   Measured cost of violating it: WMAPE 17.20% → 15.02%, a gain bought by leakage.
2. **Literature-driven construction.** Lags, rolling statistics, calendar position and
   holiday enrichment as one instance of M4/M5's explanatory-variable direction.
3. **Validated redundancy check.** Correlation and importance measured; the implied
   reduction tested and rejected on held-out error.

That chain is honest, complete, and requires **no new experiments**.

## R4 — What is genuinely under-justified

Being straight about the remaining gap, since the point is to know where you stand:

- **15 of the 16 distribution/promotional exclusions were never individually tested.** They
  are excluded correctly (unlagged, contemporaneous — stage 1 covers them), but only
  `weighted_dist` has a measurement. Stating the *rule* in Ch4 closes this; testing 15
  columns individually is not needed and there is no time for it.
- **`zero_run_flag` / `zero_run_length`** are time-safe, built, never trained, never
  discussed. Lowest stakes on the list. Either include them or say they are diagnostics.

## R5 — On the wider architecture

The SRQ1 → SRQ2 → SRQ4 chain is coherent as described, and the scope discipline is right:
*"not the best FMCG model, but which lightweight models perform well enough to be worth
serving."* Light tuning via CV, pooled vs per-category, one selected model — that is
proportionate to a thesis whose contribution is architectural.

The main risk is **not** methodological. It is that SRQ1's supporting detail (ablations,
feature-effect tables, diagnostics nobody consumes) grows until it reads as the
contribution, and SRQ4 — the actual claim — gets the thinner treatment. Cutting the
ablation from the reported results serves the thesis twice: it removes a claim you are not
making, and it returns space to the one you are.

## Actions, revised

| # | Action | Cost | Blocking? |
|---|---|---|---|
| 1 | Add the 3 holiday columns to `srq1_benchmark.FEATURES` | 1 line | **Yes — before the VPS run** |
| 2 | Drop the holiday ablation from reported results | prose/table | No |
| 3 | Fix `04_feature_matrix.md` — caption says 34 inputs, truth is 13 (16 with holidays) | ~30 min | No |
| 4 | Write the three-stage chain into Ch4 | prose | No |

**Item 1 is time-critical.** If the VPS run completes with the current `FEATURES`, the
headline benchmark, `train_persist` (what SRQ2 serves) and every downstream table describe
a model without the enrichment the data chapter will claim it has.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

**Verified:** `derive_holiday_enrichment()` at `step_3_derive_params.py:386`;
`add_holiday_features()` at `engineer_features.py:379`; holiday columns present and 100%
populated in all four h1/h3 matrices dated 2026-09-07 17:59.

**Corrected 2026-09-08.** An earlier revision of this note claimed M4/M5 "establish
calendar/holiday enrichment as standard practice for retail demand forecasting". **They do
not, and Brian never said they did** — he said they discuss exogenous variables helping.
The narrower true claim is above. See
`06_thesis_writing/writing-notes/ch4_data_assessment/.archive/2026-09-08_exogenous-enrichment-and-the-holiday-question-folded-in.md`,
which had already worked out this exact boundary and which this note initially ignored.

**Judgement, not measurement:** R1 and R5 are editorial recommendations about scope, not
findings. Brian's call.
