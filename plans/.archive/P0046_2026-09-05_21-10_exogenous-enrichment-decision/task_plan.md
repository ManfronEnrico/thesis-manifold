---
pid: P0047
created: 2026-09-05 21:10:00
updated: 2026-09-07 18:30:00
status: complete
focus_detail: "NUMBERS LOCKED 2026-09-07 -- see LOCKED_STATE.md, which is the one-page entry point for any new session. All SRQ1 accuracy artefacts regenerated deterministically under XGB_N_JOBS=1 (F18); stability re-run confirmed the model-equivalence verdict SURVIVES with one qualification on RTD (F19); the five remaining pre-fix files are efficiency measurements F18 cannot reach (F20). Holiday-enrichment PROSE moved to a separate session. Remaining here: nothing blocking -- task 8 (Word threads) and 22 (claims verification) are Brian's. P0042 funded runs are unblocked."
completed: 2026-09-07 18:30:00
outcome_summary: "ARCHIVED -- open work absorbed into P0048 tasks 9-10. Experiments finished and numbers locked: holiday enrichment shipped, 7/12 cells helped, mean -1.42 pp, reported as a per-model/per-category split rather than a mean. 19 of 22 tasks complete; the 3 remaining were Brian's writing-side items (five Word threads, NotebookLM claims verification) and moved to P0048/INHERITED_CONTEXT.md Part A. The durable output is the determinism contract in LOCKED_STATE.md (accuracy at XGB_N_JOBS=1, resource profiling at -1), which P0049 depends on."
---

# P0047 — Exogenous enrichment: holiday calendar

> **P-ID NOTE.** Created as P0046, colliding with
> `P0046_..._figure-table-provenance-centralisation`. Renumbered **P0047**;
> folder name still says P0046. The other plan keeps P0046 — its `DEC-P0046-*`
> decision IDs are referenced elsewhere.

## Why this is not part of P0043

Five Word threads object that the thesis **claims** exogenous enrichment it does
not **have**: ch1 15/18/20, ch2 66/69, ch3 127, ch4 177, ch5 207.

P0043 closes threads by editing prose. These five cannot be, because the honest
fix has two branches and only one is writing:

- **Withdraw** the claim → prose fix → P0043's job
- **Deliver** the enrichment → new feature → retrain → every WMAPE changes

The second touches SRQ1 results and the funded SRQ4 runs, so it lives here.

## Decisions

| # | decision | date |
|---|---|---|
| 1 | **Option C**: build it, report the delta whatever it is | 2026-09-05 |
| 2 | Enrichment is **upstream** of P0042's ~111 funded runs (~$40) — spending credit against a feature set the thesis then abandons is the outcome to avoid | 2026-09-05 |
| 3 | **SHIP and report honestly**, rather than withdraw or split by model family | 2026-09-06 |

**Why ship (decision 3), given the result is mostly null:**

- Option C was **pre-registered** before the answer was known. Changing the
  reporting rule once the result is unfavourable is a researcher degree of
  freedom, and the plan documents the commitment.
- The null is the substantive finding: seasonal structure in Danish beverage
  demand is **trade-driven, not holiday-driven** at monthly grain. `peak_month`
  already pointed there (CSD peaks at quarter-ends); an independent calendar
  corroborates it. Unpublished for this panel.
- It is the strongest answer to the reviewers: not "you're right, we withdrew it"
  but "we built it, measured it properly, here is what it bought".
- **Rejected — split by model family** (holiday features for Ridge only): the
  SRQ1 cross-model ranking depends on the models seeing the same information.
  Step 6 already warns that categories differ in feature space; a second axis of
  that would make the comparison uninterpretable.

## What was built

| component | location |
|---|---|
| Fetch + cache + manifest | `_00_raw/holidays/fetch_holidays.py` |
| Features | `engineer_features.py::add_holiday_features` |
| Decision point (contract v1.2) | `step_3_derive_params.py::derive_holiday_enrichment` |
| Application | `step_4_engineer_features.py` (accepts v1.1 + v1.2) |
| Auto-refresh on Nielsen pull | `save_all_datasets.py::_refresh_holidays` |
| Appendix tables 90–93 | `_00_raw/holidays/export_holiday_appendix.py` |
| **Collinearity + importance** | `srq1_feature_diagnostics.py` (**new capability**) |
| **Rolling-origin CV for Ridge** | `srq1_ridge_cv.py` (**new capability**) |
| Ablation, untuned | `srq1_holiday_ablation.py` |
| **Ablation, tuned — thesis numbers** | `srq1_holiday_ablation_tuned.py` |

Features: `days_in_month`, `n_holidays`, `non_holiday_days`.

## Scope widened 2026-09-06 — the methodology gap

Brian asked whether the pipeline did proper feature-importance and correlation
analysis and kept only information-adding components. **It did not** (F11):

| capability | before | after |
|---|---|---|
| Correlation on the **model** feature set | absent | `srq1_feature_diagnostics.py` |
| VIF / multicollinearity | absent | same |
| Permutation importance (on validation) | absent | same |
| Cross-validation, any model | **absent everywhere** | `srq1_ridge_cv.py` (rolling-origin) |
| Feature selection | absent | measured, and **rejected** (F13) |

The feature list was hand-maintained; its two removals were justified in code
comments. That is a habit, not a method. It is now measured.

## Tasks

| # | task | blocked by | status |
|---|---|---|---|
| 1 | Ground truth: what IS exogenous today | — | complete |
| 2 | Size Option C against the P0042 schedule | 1 | complete |
| 3 | DECISION GATE → Option C | 2 | complete |
| 5 | Build feature + fetch + contract wiring | 3 | complete |
| 9 | Corrected F1/F2 reasoning → `writing-notes/` | — | complete |
| 10 | Appendix tables per DEC-P0046-PATHS/-ROUTING | 5 | complete |
| 11 | Steps 3–6 × 4 categories × 2 horizons | 5 | complete |
| 13 | Untuned ablation + SHAP + seed/single-feature checks | 11 | complete |
| 14 | **Feature diagnostics**: VIF, clusters, permutation importance | 11 | complete |
| 15 | **Rolling-origin CV for Ridge** | 11 | complete |
| 16 | Validate naive VIF reduction → **rejected**, recorded | 14 | complete |
| 17 | Unverified-claims register | — | complete |
| 6 | **Tuned ablation — the thesis numbers** | 13,15 | **running** |
| 18 | DECISION: ship (confirmed by Brian) | 6 | complete |
| 7 | Appendix tables for the ablation + diagnostics | 6 | pending |
| 19 | Regenerate affected SRQ1 figures/tables; staleness audit | 7 | pending |
| 12 | Writing notes: result, limitations, future work | 6 | pending |
| 8 | Close the five Word threads with the outcome | 12 | pending |
| 20 | Verify the 4 open items in the unverified-claims register | — | **Brian** |
| 4 | *(fallback, not taken)* Withdraw the claim | — | n/a |

## Reporting requirements

**Report per-category AND per-model. Never the mean alone** — it averages over
model families that respond differently, which is itself a finding.

Must appear in the write-up:

1. The delta table, all cells, whatever the signs
2. SHAP before/after — establishes the features are *not* month re-encoded (F10)
3. Appendix table 92 — the structural argument (Easter moves; Store Bededag)
4. The robustness checks: 5 seeds, single-feature variant, widened alpha grid
5. The **rejected** VIF reduction (F13) — trees use correlated lags productively
6. Both of Claude's over-claims (F12, F14), since they are corrected in the record

## Non-goals

- **Weather / macro data.** Future work (task 12), not scope now.
- **School holidays.** No free API found (Brian). Out of scope by data
  availability — state it, don't leave it silent.
- **Re-opening the grain.** Brand × month is locked (DEC-GRAIN). The plausible
  reading of a null at monthly grain is that the effect is sub-monthly; that is
  a future-work sentence, not a re-scope.
- **Retro-fitting.** The claim is narrowed to what the pipeline has, not softened.
- **Arguing from the 2026-08-18 rename.** A naming fix, not a negative result (F1).
- **Citing a source not in the Zotero library.** F15. Register it instead.

## Related

- `plans/P0048_2026-09-07_13-51_remaining-prose-and-results-citations/` — inherits this
  plan's holiday-enrichment note as a paste-ready input. **Two constraints flow across:**
  (1) P0048 F3 establishes the feature base is **13, not 14**, so this note's "14 → 17"
  becomes **16** — apply P0048's P2 first; (2) P0048's re-run (task 5) must honour the
  `XGB_N_JOBS=1` contract in `LOCKED_STATE.md`, or the regenerated numbers are no more
  reproducible than the ones that contract was written to fix.

- `plans/P0043_.../` — writing-side plan; the five threads (F47)
- `plans/P0042_.../` — funded runs; this plan is upstream
- `plans/P0046_..._figure-table-provenance-centralisation/` — DEC-P0046-* govern
  the appendix generators
- `06_thesis_writing/writing-notes/exogenous-enrichment-and-the-holiday-question.md`
- `06_thesis_writing/writing-notes/unverified-claims-to-check.md`


---

## Session 4 addendum (2026-09-06) — the determinism finding

Task 19 was scoped as "regenerate what the feature change made stale". **That premise
was false**: no SRQ1 generator reads the holiday columns, because each pins a literal
`FEATURES` list and `available_features()` intersects wanted-with-present.

Testing the premise rather than assuming it found a defect that had been present the
whole time. `srq1_benchmark.py` re-ran with **XGBoost-only drift** — 4 of 4 XGBoost rows
moved, 0 of 12 others. Cause: `n_jobs=-1` leaves XGBoost's parallel gradient reduction
order-dependent, so thread count changes the tree. `random_state` does not fix this.

**2.65pp of spread from thread count alone** — larger than most of the holiday effects
this plan set out to measure. Two conclusions were not real: RTD's best model
(XGBoost -> LightGBM, old margin 0.43pp) and 3 of 12 ablation sign flips.

### Corrected headline

| | superseded | **reported** |
|---|---|---|
| cells helped | 6/12 | **7/12** |
| mean delta | -0.75pp | **-1.42pp** |

The superseded pair must not survive anywhere in prose.

### Decision — DEC-P0047-DETERMINISM

**Accuracy numbers use `XGB_N_JOBS = 1`. Resource measurements do not.**

`srq1_profiling.py` keeps `n_jobs=-1`: it measures memory and latency under realistic
multi-core execution, where all-cores IS the measured quantity, and it already records
the core count and states the machine-dependence in its output. Flattening that would
have destroyed a valid measurement to satisfy a rule aimed at a different problem.

The reproducibility cost is wall-clock on a single fit — seconds, and not a reported
quantity.

### Remaining

`srq1_benchmark_cv.py` **completed** (verified whole: 16 cells, 1601 convergence rows).

Only `srq1_stability.py` remains — **task 21**, and it is not a refresh. Its headline is
that LightGBM and XGBoost are *statistically indistinguishable*, resting on a per-seed
winner that **FLIPS in 4 of 4 categories** and on "between-seed spread exceeding the
between-model difference". That spread was measured with thread noise folded into
XGBoost's seed variation, and quantifying seed sensitivity is the table's entire
purpose — so F18 reaches the conclusion here, not just the digits.

LightGBM is the control (F18 does not touch it). Pre-fix baseline preserved at
`prefix_stability_baseline/`. Criteria in task 21; **either outcome is publishable and
neither is preferred.**


---

## Final state — 2026-09-07

**The experiments are finished and the numbers are locked.** `LOCKED_STATE.md` is the
single page a new session should read first; this file is the history behind it.

### What this plan ultimately delivered

It began as a decision about whether to add a holiday calendar. It delivered that — and
three things that were not in scope when it started, each found by testing an assumption
rather than accepting it:

| Finding | What it was | How it was found |
|---|---|---|
| **F18** | XGBoost was never reproducible; `n_jobs=-1` gave a 2.65 pp thread-count spread | Task 19's premise (artefacts stale from the feature change) was false; testing it produced XGBoost-only drift |
| **F19** | The model-equivalence verdict survives, but RTD needs a qualification | Re-running stability against a preserved pre-fix baseline |
| **F20** | Five pre-fix files are efficiency measurements, untouched by F18 | Checking what each file actually contains before regenerating it |

The enrichment result itself (7/12, mean −1.42 pp, with the model-family split as the
real finding) is smaller than F18, which corrected two conclusions that were never real:
RTD's best model, and 3 of 12 ablation signs.

### The durable output

Not the numbers — those will be superseded. The durable output is the **determinism
contract**: accuracy at `n_jobs=1`, resource profiling at `-1`, the rationale inline at
the definition, and the measurement that justifies it preserved in F18. Any future
XGBoost call site inherits it by importing `XGB_N_JOBS` rather than writing a literal.
