# P0031 — Findings

## Source of these 5 gaps

Identified during a full top-to-bottom review of `pre_processing_notebook_csd.ipynb`'s EDA
section, requested by Brian right after P0030 (notebook consolidation) completed and he'd
re-run the notebook himself. Full review context: P0030's `progress.md` / `task_plan.md`
document the migration itself; this file only covers the 5 net-new gaps found in the
already-migrated, already-working notebook.

## Gap 1 — ACF/PACF lag consensus unwired

Step 3.14 (ACF/PACF Analysis) computes per-brand significant lags (top 5 brands, outside the
+/-1.96/sqrt(n) confidence band) and a cross-brand consensus, printing suggested lags to add/
remove relative to `LAGS` (set earlier in Step 3.13 via a different method: cross-brand
correlation on ALL stable brands, |r|>0.1 in >=50% of brands). At time of last full run:
- Step 3.13's `LAGS = (1, 2, 3, 4, 8, 12, 13)`
- Step 3.14's consensus (top-5-brand ACF): suggests adding `[5, 6, 9, 11, 14, 15, 17, 18]`,
  removing `[4, 13]`
- Neither list overrides `LAGS`; only Step 3.13's value reaches Step 4.3.

## Gap 2 — CSD has zero promo signal

Step 3.11 and Step 3.16 both independently confirm CSD (at the "DVH EXCL. HD" market grain)
has `promo_units` always 0 -- "No promo activity recorded for this category at the region
grain" / mean+median promo intensity = 0.000. This means Step 4.3's `promo_intensity` feature
is constant-zero for every row in CSD's feature matrix. Not a bug; genuinely no promo data at
this grain for this category. Not yet recorded in `csd_eda_findings.json`.

## Gap 3 — Heterogeneity verdict not persisted

Step 3.12 (Cross-Brand Heterogeneity): 45/136 brands have CV > 1.0 (high volatility);
peak-month concentration 0.38 (Dec accounts for 53/140 brands' peak month). Verdict printed:
"High CV + varied peak months -> consider brand fixed effects or per-brand models." This is a
modeling-stage decision, correctly out of scope for a preprocessing notebook to *act* on, but
currently only exists as printed cell output -- lost on cell-output-clear or notebook re-run
without saving outputs. Not yet in `csd_eda_findings.json`.

## Gap 4 — sales_value / sales_liters correlation with sales_units unexamined

Step 3.17/3.18 (Correlation Heatmap) flagged 3 non-linear pairs by Pearson/Spearman gap:
- `sales_units` <-> `weighted_dist`: Delta=0.411 (Pe=0.489, Sp=0.900) -- ADDRESSED (P0030 added
  `log_weighted_dist`)
- `sales_value` <-> `weighted_dist`: Delta=0.454 (Pe=0.457, Sp=0.911) -- NOT directly relevant
  (weighted_dist side already log-transformed; this is about weighted_dist's own skew, not
  sales_value's relationship to the target)
- `sales_liters` <-> `weighted_dist`: Delta=0.445 (Pe=0.462, Sp=0.907) -- same as above

**Correction from initial framing**: my prior message described `sales_value`/`sales_liters`
as themselves having a large Pearson/Spearman gap against `sales_units` (the modeling target).
Re-checking the actual heatmap output: the flagged non-linear pairs are all against
`weighted_dist`, not against `sales_units`. The real open question for Task 4 is different and
more direct -- what is the *raw linear correlation* between `sales_units` and
`sales_value`/`sales_liters` themselves (not yet computed/printed anywhere in the notebook)?
Given these are the same underlying sales volume in different units (units vs. currency vs.
liters), a near-1.0 Pearson correlation is likely, which would make them redundant as separate
model inputs. Task 1 in the P0031 task list (task id "4") directs computing this directly
rather than relying on the heatmap's existing (differently-scoped) output.

## Gap 5 — Stale CELL-N print headers

Confirmed via grep: Step 3.12's cell prints `"CELL 11: Cross-Brand Heterogeneity Analysis"`;
Step 3.14's cell prints `"CELL 11: ACF/PACF Analysis (Autocorrelation Structure)"` -- same
"CELL 11" label, two different Steps. Leftover from an earlier ad-hoc numbering scheme that
predates the EDA/pipeline notebook merge; markdown headers are the current source of truth
(fixed to 3.01-3.19 in P0030's session, then had to be re-fixed again this session after a
mid-session save collision reverted the renumbering -- see P0030 task_plan.md's "Errors
Encountered" table for that incident). The print-header strings were never part of that
renumbering pass.
