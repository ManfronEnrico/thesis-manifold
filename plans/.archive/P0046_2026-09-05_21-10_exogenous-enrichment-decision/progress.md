# P0047 — Progress

## Session 1 — 2026-09-05 — decision

Split out of P0043: the enrichment objection changes feature engineering, hence
training, hence every reported number, so it is not a prose fix.

Brian corrected two findings; **both weakened my case against enrichment**, and
neither was a point he had to concede.

- **F1** — I claimed the project had already tested holiday features. It had not.
  The 2026-08-18 change was a rename of a mislabelled peak-month rule.
- **F2** — The Prophet grain argument holds for holiday *windows*, not monthly
  *counts*.

**Decision: Option C, upstream of the funded runs.**
> *"exactly thats why I want to do it before we finish the experiments"*

## Session 2 — 2026-09-06 — built

### API

`nagerholidays.com/api/pro/` → 401 (commercial tier). Free tier is
`date.nager.at/api/v3/PublicHolidays/{year}/DK` (F4). Brian's BDBI exam script
used the correct host and served as the pattern for the fetch loop.

### Corrections Brian made during the build

| # | mine | correct |
|---|---|---|
| 1 | `trading_days` = weekdays − holidays | Danish retail trades weekends; `non_holiday_days = days_in_month − n_holidays` (F6) |
| 2 | Four objections to fetching during training | Three were answerable by the cache-with-timestamp I had *myself* proposed. Only the refetch-coupling point stood |
| 3 | Fetch tied to Nielsen refetch | Also needs standalone — a Nielsen pull is ~10 min minimum, ~2 h with raw |
| 4 | Asked two contract-schema questions | Not his call; decided them (F8) |

On (2) I stated the fix and then used it as an objection anyway. On (4) I asked
for a decision instead of making one after he had said to proceed.

### Built

| component | note |
|---|---|
| `_00_raw/holidays/fetch_holidays.py` | standalone + auto; per-year cache; manifest with timestamp + sha256 |
| `engineer_features.py::add_holiday_features` | `days_in_month`, `n_holidays`, `non_holiday_days` |
| `step_3_derive_params.py` | contract **v1.2**; decides + records reason |
| `step_4_engineer_features.py` | accepts v1.1 (unenriched) + v1.2; hard-fails if a promise is unmet |
| `save_all_datasets.py::_refresh_holidays` | `--force` on a Nielsen pull; never fails the Nielsen run |
| `export_holiday_appendix.py` | appendix tables 90–93 |

### Verified by running

- Fetch: 10 years cached, **15 holidays 2018–2023 → 14 from 2024** (F5)
- Features: Mar 2023 = 0 vs Mar 2024 = 3 (Easter); 2017 = NaN not 0
- Contract: covered panel → `True`; 2015-start panel → `False` with the exact fix command
- Both engineer paths: enriched emits 3 columns, unenriched emits none
- Mismatch guard raises; all 4 files compile
- **F9 bug found and fixed**: a narrow re-run shrank the manifest to 3 years while
  10 were cached — would have silently disabled enrichment

### Appendix (per P0046 provenance rules)

Tables 90–93 in `05_thesis_results/appendix/`, `.md` + `.csv` twins, all values
derived from the cache, `<!-- INTERNAL REVIEW -->` separators, output via
`PATHS.py`, root anchored on `.env.example`.

Table 92 (monthly matrix) is the anti-collinearity evidence (F7): December flat
at 4, March 0–4, April 0–5.

### Repo restructure

Mid-session the parallel session moved everything to SRQ tiers. All paths
updated; `PATHS.py` was already current. They also replaced my `parents[4]` hop
with an anchor-based root finder — a real improvement, kept.

**P-ID collision**: this plan renumbered **P0047**; the other keeps P0046
because `DEC-P0046-*` decision IDs reference it. Folder name still says P0046.

### Task 11 — pipeline re-run, complete

Steps 3 and 4, all 4 categories, both horizons. 8/8 succeeded each time.

| check | result |
|---|---|
| Contracts | 8/8 now **v1.2**, `holiday_enrichment: true`, "cache covers panel" |
| Matrices | 8/8 carry `days_in_month`, `n_holidays`, `non_holiday_days` |
| Coverage | **0 NaN** — panel 2022-10..2026-07 sits inside fetched 2018-2027 |
| Arithmetic | `non_holiday_days == days_in_month - n_holidays` verified |
| Run log | `result.has_holidays: true` on all 8 |

Baseline before the run: all 8 were v1.1 with the field absent.

**The evidence, now in live CSD training rows** — March is `peak_month=1` in
every year (a CSD quarter-end peak), yet `n_holidays` runs 0 / 3 / 0 / 0 across
2023-2026. Same peak flag, different holiday exposure: the peak rule cannot see
this, which is precisely F1's "what does a calendar add *over* the peak rule".
May 2025 shows 2 holidays against 4-5 elsewhere — Store Bededag (F5) landing in
real training data.

## Session 3 — 2026-09-06 — measured, and the scope widened

### The ablation (untuned) — mostly null

8 of 12 category x model combinations got **worse** with the holiday features.
Helps decisively in RTD (all 3 models), hurts in CSD (all 3). Two follow-ups,
both measured rather than assumed:

- **Not dimensionality.** `n_holidays` alone: mean delta +0.00pp, worse in the
  same 8 of 12.
- **Not seed luck.** RTD's LightGBM gain holds across 5 seeds (-1.19..-2.10pp).

**SHAP redistribution test: negative.** The holiday features take 1.2-2.4%
attribution while `month`/`peak_month` lose only 0.2-1.1%. They carry
information `month` structurally cannot hold — and the models still generalise
worse with them. **Attribution is not accuracy.** Both halves get reported.

### Brian's methodology challenge, and what it exposed

> *"did we do a proper feature importance, and feature correlation analysis and
> kept only information adding components?"*

**No.** Verified by search: no VIF, no correlation on the model feature set, no
feature selection, and **no cross-validation anywhere** — including in
`srq1_benchmark_cv.py`, despite the name. The feature list was hand-maintained
and its two removals were justified in code comments (F11).

Built in response:

- `srq1_feature_diagnostics.py` — VIF, exact-dependency detection, Spearman
  redundancy clusters, permutation importance on validation
- `srq1_ridge_cv.py` — rolling-origin CV (k-fold is invalid on a time series)

**First diagnostic run: only 1-3 of 15-16 features per category are below
VIF 5.** `rolling_mean_4` reaches 227-256. Every category carries one 6-7 member
lag/rolling cluster at rho >= 0.95, plus `month + quarter`.

### The two results that mattered most were both negative

1. **Naive VIF reduction makes it worse** (F13): 16->9 features gives mean WMAPE
   28.82 vs 26.44. Collinearity is a *linear-model* pathology; trees use
   correlated lags productively. The correlated lags ARE information-adding, and
   this is the measurement that proves it.
2. **Proper CV made Ridge slightly worse** (F14): mean -0.19pp vs the hard-coded
   alpha=1. The CV curve is flat; alpha barely matters on this data. Worth fixing
   for method, not for accuracy.

### Three of my own claims were wrong

All three followed the same pattern — quoting an exploratory sweep before
running it through the protocol.

| claim | reality |
|---|---|
| "The exact dependency explains RTD's Ridge instability" | Dropping it changes WMAPE by < 0.01pp in all 8 cells (F12a) |
| "RTD Ridge should be 43.6%, a 13.7pp error" | That was read **on the test set**. Honest answer: 56.3% (F12b, F14) |
| "VIF > 10 per Hair et al. (2019)" | Cited **from memory**; not in the 86-entry Zotero library (F15) |

The citation is the serious one. It is the `holiday_months` defect transposed
into the literature layer, where a reader cannot check it against data.
`writing-notes/unverified-claims-to-check.md` now exists as a standing register,
carrying four open items — two of them also mine (the Spearman 0.95 threshold and
the Lukkeloven 2012 date).

### Decision: SHIP and report honestly

> Brian: *"I am also leaning into actually shipping and honestly reporting."*

Rationale in task_plan. The short version: Option C was pre-registered, the null
is the substantive finding (Danish beverage seasonality is trade-driven, not
holiday-driven at monthly grain), and it is the strongest available answer to the
five reviewers.

Rejected — splitting the feature set by model family. The SRQ1 cross-model
ranking depends on the models seeing the same information.

### In flight

`srq1_holiday_ablation_tuned.py` — separate Optuna study per arm per model, plus
Ridge with CV-selected alpha. **These are the thesis numbers**; everything above
was measured on the untuned benchmark, which confounds a feature change with
frozen model capacity.

First launch failed instantly: `srq1_benchmark_tuned.DATASETS` keys the grain
`"brand"` where `srq1_benchmark` keys the same directory `"bymonth"`. Resolved
from the module rather than hard-coded, so a future rename cannot desync them.

## Next session starts here## Next session starts here

1. **Read the tuned ablation result** (task 6) and treat it as authoritative.
   The untuned numbers do not go in the thesis.
2. **Task 7** — appendix tables for the ablation and diagnostics, same
   conventions as 90-93.
3. **Task 19** — regenerate affected SRQ1 artefacts; update the staleness audit.
4. **Task 12** — write-up: per-category AND per-model deltas, never the mean
   alone. Include the reproducibility limitation, the `non_holiday_days` proxy
   caveat, school holidays out of scope by data availability, weather/macro as
   future work, and the sub-monthly reading of a null.
5. **Task 8** — close the five Word threads: built, measured, reported.
6. **Task 20 (Brian)** — verify the four register items before any reaches prose.

Then, and only then, P0042's funded runs.

### Open

- **Both features or one?** `non_holiday_days` is an exact linear function of
  `n_holidays` given `days_in_month`. Dropping it changed nothing measurable
  (F12a), so this is a presentation choice, not an accuracy one.
- **Should the tuned result change the ship decision?** It should not — the
  decision was made on pre-registration and on the value of the null, neither of
  which depends on the sign. But if the tuned numbers differ sharply from the
  untuned ones, that difference is itself worth a sentence in the write-up.

---

## Session 4 — 2026-09-06 (evening)

**Tasks 7 and 19.**

### Task 7 — appendix tables 94-99 (COMPLETE)

Emitted into `05_thesis_results/appendix/`, `.md`+`.csv` twins, all 10 verified present
(90-93 from the earlier session, 94-99 new).

Two defects found and fixed while doing it, both recorded as **F17**:

- **(a) Output placement.** All four scripts added this session were writing 12 loose
  CSVs to the TOP of `srq1_model_performance/`, which already had `figures/ models/
  tables/`. `PATHS.get_srq_tables_dir(1)` existed the whole time. All four repointed,
  all 12 files moved, 0 loose files remain.
- **(b) `to_markdown` dropped significant digits** — re-parses "22.20" and renders
  "22.2". `astype(object)` does NOT stop it; `disable_numparse=True` does. Trailing
  zeros state reported precision, so this mattered.
  *(`export_appendix.py` likely needs the same fix — flagged for P0046 Phase 7.)*

### Task 19 — regeneration (SUBSTANTIALLY COMPLETE, one run outstanding)

**The task's premise was false, and testing it found a real defect.**

Task 19 assumed SRQ1 artefacts were stale because the feature set changed. They were
not: every generator pins a literal 13-name `FEATURES` list that excludes the three
holiday columns, and `available_features()` intersects wanted-with-present, so extra
matrix columns are invisible. Verified: all four matrices carry the holiday columns with
zero nulls, and the overlap with `FEATURES` is empty.

Re-running `srq1_benchmark.py` should have been a no-op. It was not — **XGBoost rows
only, 4 of 4, while all 12 non-XGBoost rows were byte-identical.** That signature
isolated the cause: `n_jobs=-1` makes XGBoost's parallel gradient reduction
order-dependent, so the thread count changes the result. Measured 2.65pp of spread from
thread count alone, seed and data held constant. **See F18.**

Two conclusions were not real: RTD's best model flips XGBoost -> LightGBM
(old margin 0.43pp, smaller than the artefact), and 3 of 12 table-94 cells flip sign.

**Fixed:** `XGB_N_JOBS = 1` at every accuracy call site (8 scripts), rationale inline.
`srq1_profiling.py` deliberately left at `-1` — it measures resource cost under
realistic multi-core execution and already records the core count. Verified two
consecutive full runs are now byte-identical.

**Also fixed (F18b):** table 94's internal-review block hard-coded "3 of 8 cells" (now
4 of 8) and named RTD XGBoost as least-stable (now danskvand LightGBM, 3.81pp). Both
would have shipped wrong. Now derived from the data.

### Headline numbers changed

| | before | after |
|---|---|---|
| cells helped | 6/12 | **7/12** |
| mean delta | -0.75pp | **-1.42pp** |
| sign flips | — | 3 cells |

### Regenerated this session
`metrics.csv`/`summary.md`, `tuned_metrics.csv`/`tuned_summary.md`, all three figures,
`shap_importance`, `holiday_ablation_tuned_*`, appendix 94-99, `calibration`, `mase`,
`demand_classes`, `stat_baselines`, `pooled_*`, `ridge_pooled`, `pooled_perbrand`.

### Outstanding

**`srq1_benchmark_cv.py` — CONFIRMED COMPLETE** at 00:39. Verified whole, not truncated:
all 16 cells (4 categories x 2 models x 2 objectives) and 1601 convergence rows
(800 trials x 2 + header). The CV track is now deterministic.

**`srq1_stability.py` — running.** 5 seeds x 2 models x 4 categories = 40 Optuna studies
at 40 trials, the longest run of the set. Still holds Aug-24 pre-fix numbers until it
lands. This is the one whose *conclusion* may move, not just its digits: it measures
seed sensitivity and has been measuring seed noise with thread noise on top.


---

## Session 5 — 2026-09-07

**Snapshot regenerated** as `2026-09-07_14-29_holiday-enrichment` (30,119 words, 281
comments, 154 leaf sections).

**Task 12 rewritten with exact insertion points.** Reading the real document corrected a
wrong assumption of mine: Ch6 is *Model Benchmark*, not Discussion. Six blocks P1-P6,
each with a verbatim anchor, an action verb, and an in-text/appendix decision per asset.
P1 closes Word comment 177, which is anchored on the exact sentence it changes.

**Two pre-existing discrepancies flagged, not fixed:** "22 columns" (the matrix has 54)
and "14 modelling features" including `weighted_distribution` when the benchmark's
FEATURES has 13 and excludes it. Also a cross-reference bug: 6.6 cites 6.5.7 for a sweep
that is 6.5.9.

**Task 21 complete — see F19.** The stability verdict SURVIVES on clean evidence.
All four categories still flip. One qualification needed: RTD's model gap now exceeds
its seed spread, so 6.6's blanket claim must be narrowed to three categories.

**Skill + rule created** for reproducibility: `write-prose-from-bullets` and
`prose-insertion-discipline`. Claims folder restructured by chapter/topic per request.

**All six prose blocks are now unblocked**, with the constraint that P3 and P4 ship
together.
