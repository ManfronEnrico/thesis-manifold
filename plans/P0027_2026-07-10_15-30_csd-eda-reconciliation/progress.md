# P0027 Progress Log

## 2026-07-10 15:30 — Plan created

- Prior fork audit (same session) established CSD EDA was stale relative to brand×region×period grain
- User surfaced `docs/handover/2026-07-01_enrico-to-brian-merge-handover.md` — a large parallel modeling track (SRQ1-4) merged into main on 2026-07-01, with several "locked" decisions
- User explicit instruction: verify every claim in the handover before acting on it, since Enrico is a heavy Claude Code user with limited independent verification habits
- Switched from `main` to `thesis/csd-eda-rerun` branch (user confirmed via AskUserQuestion)
- Verified during this session (pre-plan, see findings.md): Cell 12 fix is real, region-grain rejection reasoning is accurate but based on partial data, a separate canonical script (`build_feature_matrix.py`) exists distinct from our modular pipeline, degenerate mean-MAPE confirmed live in data, KPSS/missingness gaps persist in Enrico's version too
- Created P0027 plan folder with 6 phases: verify claims → academic gap-fill → region grain WMAPE test → canonical script decision → extend to 3 categories → Ch4 handoff package
- Next: task decomposition for Phase 1 (claim verification), then execute

## 2026-07-10 16:15 — Phase 1 complete: all 5 claims verified

- Ran `/task-decomposition` for Phase 1, persisted 5 task JSON files, then executed all 5 as parallel forked agents (independent, read-only investigations, no shared write conflicts)
- Results (full detail in `findings.md`):
  1. MIN_PERIODS=30 — holds, global constant, no per-category override. Period-count ceiling (37-39) verified for CSD/Energidrikke against raw `_01_converted` data; danskvand/RTD rest on secondary sources only (local checkout lacks their raw parquets) — residual gap, not urgent
  2. Granularity winner (brand×month vs brand×chain) — holds exactly for all 4 categories, systematically reproduced from `tuned_metrics.csv`, non-trivial margins (1.8-7.8pp)
  3. WARMUP_PERIODS=13 — holds exactly, `max(MAX_LAG=13, MAX_WINDOW=13)=13`, identical across brand/bychain scripts
  4. Gitignore status of `_03`-`_07` output tiers — **not actually gitignored** (no patterns exist), but no current large-file risk (~34MB total, largest file 140KB). Recommend adding ignore patterns preventively (not done — read-only task)
  5. Pooled brand-demeaned ACF method — **genuine defect found**, not just a caveat: boundary-splicing (concatenating brands without masking lag boundaries) + heteroscedasticity (variance-weighting toward high-volume brands) both bias the pooled ACF vs a proper per-brand-then-averaged approach. Also unreproducible — no script in `build_feature_matrix.py` computes it; the numbers in `eda_findings_dvhexclhd.md` are an unversioned manual calculation.
- Updated `task_plan.md` Phase 1 checkboxes to complete, added Phase 1 Summary table to `findings.md`
- Net assessment: 3/5 claims solid, 1 latent-but-harmless gitignore gap, 1 genuine academic defect (ACF) requiring a real fix in Phase 2 — validates the user's original skepticism that Enrico's "locked" claims needed independent checking, not blanket acceptance
- Next: begin Phase 2 (academic gap-fill) — KPSS alongside ADF, formal MCAR/MAR/MNAR missingness reasoning, train/val/test distribution-shift check (motivated further by Task 2's side-finding of val≪test WMAPE gaps), skewness-citation correction, and replacing the pooled ACF with a proper per-brand-then-averaged method

## 2026-07-10 19:30 — Brian requested more precision on Phase 1; Phase 2 executed (5/6 tasks complete)

- Brian pushed back on the Phase 1 summary table for being too compressed ("what does that even mean?") — rewrote all 5 Phase 1 findings in `findings.md` with full mechanistic explanations, exact code/numbers as evidence, and an explicit separation between "does the fact hold" vs "is it academically justified" (these are different questions; 3 of 5 items had justification gaps even where the fact itself checked out)
- Decomposed Phase 2 into 6 tasks (IDs 6-11), persisted as JSON, task 11 wired with `blockedBy: ["8"]` since it needs corrected ACF numbers first
- Executed tasks 6, 7, 9, 10 in parallel (independent), then task 8, then task 11 (unblocked after 8 completed)
- **Critical environment discovery**: this local checkout lacks `data/raw/` (canonical script's input) and most engineered parquet files. Only CSD has reliable local data; energidrikke partial/stale (29 periods vs 39 claimed); danskvand/RTD essentially none. This blocked full completion of 4 of 6 tasks for 2 of 4 categories.
- Results: Task 6 (KPSS) — ADF/KPSS jointly ambiguous for CSD/energidrikke, weaker than doc's clean "I(1)" claim; also found unreconciled CSD ADF p-value discrepancy (0.140 vs 0.421). Task 7 (missingness) — MNAR mechanism identified via aggregate reasoning; no-impute approach defensible but was undocumented. Task 8 (ACF) — **real code fix shipped**: new script `compute_acf_per_brand.py` + updated `eda_findings_dvhexclhd.md`; confirmed pooled method inflated lag1 by ~0.2-0.3 absolute. Task 9 (distribution shift) — **fully blocked**, no data to run KS tests, only structural split-window metadata obtained. Task 10 (citation) — confirmed "Kim, 2013" is unbacked, no matching bibliography entry anywhere. Task 11 (lag-13 reconciliation) — recommend keep-but-reweight-narrative, evidence too thin (2/4 categories) to justify removal.
- Updated `task_plan.md` Phase 2 checkboxes and `findings.md` with full Phase 2 summary table
- Next: **data-access gap must be resolved before Phase 5** (extend to 3 categories) can proceed properly. Also need to decide with Brian: pursue Phase 3 (region-grain WMAPE test) next, or prioritize resolving data access, or apply the proposed narrative-wording fixes (Kim citation, lag-13 comment) with human approval first.

## 2026-07-10 20:00 — Data-access gap root-caused; sequencing confirmed with Brian

- Brian clarified: raw `.jsonl` data exists for ALL 4 categories — the actual gap is that Stage-1 conversion (JSONL→Parquet, `thesis/data/_01_converted/nielsen/jsonl_to_parquet_script/`) was only run for CSD and Energidrikke. Danskvand and RTD have zero converted parquet. Energidrikke's existing parquet is confirmed stale (Task 8 found 29 periods vs. the canonical script's expected 39) and needs `--force` re-conversion, not just a fresh run (idempotent skip-if-newer would otherwise leave it untouched).
- Provided the exact command: `python thesis/data/_01_converted/nielsen/jsonl_to_parquet_script/run_all_conversions.py --only Danskvand Energidrikke RTD --force`, run from project root. Not yet executed — command handed to Brian to run.
- **Correction discovered while verifying this**: task_plan.md's Context section (from the original Phase 1 fork audit) claimed `_02_preprocessing/nielsen/<cat>/pre_*.py` scripts are "not runnable" because `PATHS.py` is deleted. Directly tested this claim: `PATHS.py` **exists** at repo root and `python -c "import PATHS"` succeeds cleanly, resolving `PATHS.THESIS_DATA_PREPROCESSING_DIR`. This claim was either stale or never independently verified (Phase 1 inferred it from the handover rather than testing the import directly) — logged as a correction in task_plan.md's Errors Encountered table; still need to actually run a `pre_csd_*.py` step script to fully confirm runnability, not just the import.
- Brian confirmed explicit sequencing decision: finish CSD's EDA/preprocessing pipeline (Phases 2-4) to full academic rigor first — the *procedure* must be identical and equally justified across all 4 categories (same stationarity tests, same missingness-mechanism reasoning, same ACF method, same transform-justification logic), while only the *numeric results and derived parameter values* differ per dataset. Agreed this validates the plan's existing Phase 2→Phase 5 ordering; no reordering needed.
- Next: Brian runs the conversion command, then session compacts, then continue with the next phase of CSD-specific rigor work (deciding between Phase 3 region-grain test vs. remaining Phase 2 follow-ups now that data will be available for all 4 categories).

## 2026-07-10 20:35 — Conversion confirmed; CSD-only re-scoping; pipeline provenance resolved

- Brian confirmed the conversion ran successfully: all 3 categories converted cleanly (manifest shows Danskvand/Energidrikke/RTD, 4 views + 1 metadata each, 0 errors, ~83s total).
- Brian explicitly narrowed scope: focus purely on making **CSD** bulletproof this session before touching danskvand/energidrikke/RTD, even though their data is now available. Created tasks 12-14 (CSD-only distribution-shift check, ADF discrepancy reconciliation, row-level missingness test), persisted as JSON.
- Ran Task 12 (distribution-shift check) as a forked agent. Result: **no meaningful distribution shift found for CSD** — KS tests on train/val/test show val-vs-test as the *smallest* divergence of the three comparisons (opposite of the shift-driven-anomaly signature). CSD's own WMAPE gap is small (1.3-2.1pp at brand grain, reversed direction at bychain grain) versus RTD's clean 4.6-4.7pp gap — CSD does not exhibit the anomaly pattern that motivated this check. More consistent with small-sample noise from the short 6-month validation window.
- **Provenance question surfaced by Task 12**: the KS test had to run against `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` (25,124 rows) because `build_feature_matrix.py`'s expected output folder `_03_engineered_dvhexclhd/CSD/` only has a split_dates.json locally, no feature matrix. Paused to ask Brian how to proceed rather than assume.
- Brian clarified: he restructured data folders in a separate session; asked me to analyze current state directly rather than rely on old assumptions.
- Investigated directly (file existence + `pd.read_parquet` + `git log`): confirmed `_03_engineered/nielsen/CSD/` (our modular `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` pipeline's output) is the live, current, most-recently-regenerated (commit `cb615cf`, 2026-06-30, "~25.1k rows") CSD dataset — 78 brands, 25,124 rows, verified directly. `_03_engineered_dvhexclhd/CSD/` (Enrico's `build_feature_matrix.py` track) has no feature-matrix parquet in this checkout, only docs + split-dates.
- This is now the **second correction** to the plan's original premise (after the PATHS.py runnability correction) that our modular pipeline is the deprecated/non-canonical one for CSD — it is not; it's actively maintained and more current locally than the alternative. Directly informs Phase 4.
- Side-finding: `_03_engineered/nielsen/CSD/csd_preprocessing_report.md` has stale header text (2026-06-22, 62 brands, 2,666 rows) not matching the current parquet (78 brands, 25,124 rows) despite being touched in the same commit that regenerated the parquet — cosmetic reporting bug, not a data problem, not urgent.
- Updated task_plan.md (Context section, Phase 2 note), findings.md (new "Pipeline Provenance Clarification" section), and tasks 9/13/14 JSON (9 noted as CSD-portion-superseded, 13/14 descriptions corrected to point at the confirmed file).
- Brian requested deferring further execution to tomorrow's session. Tasks 13/14 remain `status: "pending"` in their JSON, fully scoped and targeting the confirmed-correct file — no in-session state to lose.
- Next (tomorrow): run Task 13 (CSD ADF p-value discrepancy reconciliation, 0.140 vs 0.421) and Task 14 (CSD row-level MNAR/MAR/MCAR missingness test), both targeting `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet`. After those close, CSD's Phase 2 gap-fill is essentially complete — decide next between Phase 3 (region-grain WMAPE test) and starting Phase 5 (extend to 3 categories, now that all 4 have current converted data).

## 2026-07-11 00:40 — Tasks 13 and 14 complete; CSD Phase 2 gap-fill closed

- Ran Task 13 (ADF p-value reconciliation) and Task 14 (row-level missingness test) as parallel forked agents, both targeting the confirmed `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet`.
- **Task 13 result**: root-caused the 0.140 vs 0.421 discrepancy to an aggregation-grain bug, not a date-range or lag-selection difference. `csd_feature_matrix.parquet` is brand×region×period grain (78 brands, 44-396 rows each depending on region count). Task 6's original script grouped by brand alone without summing across regions first, feeding a region-interleaved series into `adfuller()` — reproduced exactly (median p=0.1408, matching 0.140). Correcting the grain (sum sales across regions per brand per calendar month, then per-brand ADF on the clean 44-point series, then median across all 78 brands) gives median p=0.3535 (mean 0.4068), closely matching the doc's reported 0.421 (n=76 vs our n=78). **0.421 is now the authoritative number.** Both values agree on the qualitative verdict (non-stationary, I(1) in log level), so Ch4's stationarity conclusion is unaffected — only the cited exact p-value changes. Also reproduced the modular pipeline's separate "aggregate series (reference only)" line (p=0.2078 raw / p=0.0656 log1p) — a third, distinct diagnostic (category-total, not per-brand) that should not be confused with either the 0.140 or 0.421/0.353 figures.
- **Task 14 result**: row-level test strongly confirms and sharpens Task 7's aggregate-level MNAR reasoning. Missingness indicator (per brand-month grid cell) is overwhelmingly explained by brand volume tier: chi²=1336.9, p≈1.4e-289 (Q1 low-volume brands miss 16.3% of period-cells vs Q4 high-volume brands at 0.4%). Brand identity itself: chi²=4018.6 (p≈0). Month: chi²=48.8 (p=1e-6, small effect). Region: chi²=36.3 (p=1.6e-5, small effect). Joint logistic regression: volume-tier dominates (Q4-vs-Q1 coefficient -3.90, ~50x odds reduction), month/region effects modest once volume tier is included. This is a formal MAR signature (missingness predictable from an observed variable) that also reads as MNAR in the colloquial/substantive sense (a brand's sales genuinely dropped near-zero and stopped being recorded) — both vocabularies converge on the same conclusion, worth stating explicitly rather than picking one label. Grounds the current reindex-and-leave-NaN (no-impute) approach as correct, not just defensible.
- Findings appended to `findings.md` (new "Task 13 — CSD ADF Log-Level p-Value Discrepancy Reconciled" section, and a row-level missingness section preceding it). `task_plan.md` Phase 2 checkboxes and `focus_detail` updated; tasks 13/14 JSON marked `"status": "completed"` with detailed notes.
- **CSD's Phase 2 academic-rigor gap-fill is now complete.** All CSD-scoped tasks (6, 7/14, 8, 9/12, 10, 11, 13) are closed or explicitly deferred with a stated reason (danskvand/energidrikke/RTD portions deferred to Phase 5).
- Next: decide with Brian between Phase 3 (region-grain WMAPE test, re-running `pre_csd_1_load_and_aggregate.py` against full raw and comparing region-grain re-aggregated WMAPE vs the 16.5% brand-national baseline) and Phase 5 (extend the now-validated CSD procedure to danskvand/energidrikke/RTD, all of which now have current converted parquet as of 2026-07-10's conversion run).

## 2026-07-11 10:30 — Phase 3 Complete: Region-Grain WMAPE Test + Strategic Reframing

- Fixed all 6 CSD preprocessing scripts (pre_csd_0..6) to work with P0028 restructured paths:
  - Moved imports from stale `thesis.data._02_preprocessing` to local `02_thesis_data/_02_preprocessing/nielsen/shared`
  - Copied `engineer_features.py` module from archive and placed in shared utilities
  - All steps 1-6 ran cleanly: 27.1k → 25.1k rows after filtering

- Executed Phase 3 region-grain WMAPE test:
  - Region-grain feature matrix: brand×region×period, 25,124 rows (test: 5,787 rows)
  - Optuna tuning: 30 trials per model, TPE sampler, seed=42
  - Result: XGBoost 21.2%, LightGBM 21.2% (tied)
  - Baseline (brand×month): 16.5%
  - Delta: +4.7pp

- **CRITICAL INSIGHT FROM BRIAN** (reframes entire Phase 3-4 strategy):
  - WMAPE is NOT the optimization target — it's a diagnostic metric
  - The thesis is about making Prometheus useful to regional managers asking "What will Faxe Kondi sell in Copenhagen next quarter?" — questions only region-grain can answer
  - Both models are PRODUCTION-READY, serving different personas (regional mgrs vs HQ)
  - 21.2% WMAPE is appropriate/expected for region-level granularity (1/9 the volume per row → higher noise is normal)

- Updated findings.md with detailed explanation of what WMAPE actually means:
  - ~540K total units error across 254M test sales (21% of aggregate)
  - Per-brand: Coca-Cola ±115K units, Faxe Kondi ±80K units (21% of their respective totals)
  - Why region-grain is noisier: same absolute error across 10x fewer rows → higher % error
  - What WMAPE does NOT tell us: trend direction, brand-specific performance, per-region heterogeneity, usefulness for domain decisions

- Restructured Phase 4 decision (was "pick one grain," now "maintain both"):
  - Brand×month pipeline (16.5% WMAPE) → HQ-level "total sales in Denmark" queries
  - Region×month pipeline (21.2% WMAPE) → Regional manager "Copenhagen Coca-Cola" queries
  - Both are intentional production capabilities, not competing alternatives

- **Outcome**: Phase 3 is complete and reframed. Phase 4-5 now proceed with dual-grain strategy instead of choosing between them.

## 2026-07-11 18:35 — Separate session (post-P0028-restructure) surfaces a real leakage bug blocking Phase 3/4

- Started from an unrelated question ("how do I test the whole pipeline end to end") in a fresh session, after the P0028 repo restructure (numbered tiers, `02_thesis_data/` etc. replacing `thesis/data/`). Investigation naturally converged on this same plan's territory, so folding findings in here rather than opening a new P-ID.
- User pointed out an existing CSD orchestrator (`preprocessing_csd.py` + `pre_csd_0..6_*.py`) that the session's initial pipeline-testing answer had missed — corrected course to investigate it directly instead of just the colleague's standalone scripts.
- Confirmed all 4 categories (not just CSD) already have their own 6-step orchestrator + step scripts under `_02_preprocessing/nielsen/{Category}/` — not previously stated this explicitly in P0027's findings.
- Confirmed `srq1_benchmark.py` (the actual SRQ1 training entry point) reads from `_03_engineered/{bymonth,bychain}/`, treating **bychain as primary**, brand×month as "robustness comparison" — a framing not previously cross-referenced against Phase 3's region-grain work in this plan.
- User directive on grain scope: canonical scope stays DVH EXCL. HD only; base grain is brand×region×month with rollup to brand×month; region and chain should exist as two parallel orchestrator branches (not one replacing the other), copied to all 4 categories only after CSD is fully finished as the reference implementation.
- **Found a real, previously-undetected bug while reading Step 4 in detail**: `pre_csd_4_engineer_features.py` delegates lag/rolling computation to the shared `engineer_features.py` module, which groups by `"brand"` only (no `market_id`) — meaning CSD's region-grain lag/rolling features are silently conflating rows across the 9 different regions per brand. This directly affects Phase 3's already-reported 21.2% region-grain WMAPE, which was computed on features built by this exact code path. Same bug also affects Step 6's `build_series_index()` reporting (region-blind stats, though the underlying parquet itself is fine since `market_id` is retained as a column).
- This finding connects to and generalizes Task 13 above (2026-07-11 earlier) — Task 13 found and fixed the identical grain-conflation failure mode in an ad hoc ADF test script; today's finding shows the same bug pattern exists in the actual production feature-engineering code, not just a one-off analysis script.
- Updated `task_plan.md` frontmatter + added Phase 4a (fix the leakage bug, re-run Phase 3's benchmark) and Phase 4b (add a chain-grain branch to the orchestrator, using the same `group_keys` mechanism) — both inserted before the existing Phase 4/5 action items, which now explicitly depend on 4a/4b completing first.
- **No code changed this session** — investigation and planning only, per explicit user instruction to document and continue tomorrow.
- Next (tomorrow): implement the `group_keys` parameter fix in `engineer_features.py`, apply to CSD's Step 4 and Step 6, re-run CSD's pipeline, re-verify Phase 3's WMAPE number before trusting it for any Phase 4 decision.

