---
pid: P0035
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0035 — Findings

## Pre-existing (verified 2026-08-01)

### F1 — `group_keys` is grain-capable, not grain-committed — do NOT rip it out

`_shared_modules/engineer_features.py` parameterizes every series-aware function with
`group_keys: list[str] = ["brand"]` (see `make_calendar` :192, `filter_series` :248,
`engineer_features` :269, `apply_split` :348, and the pipeline class :401).

The default is already `["brand"]` = brand×month. Chain/region grain was invoked by
*passing* `["brand", "market_id"]`, not by a separate code path.

**Implication:** the correct cleanup is to stop *calling* with multi-key grain and confirm
defaults everywhere — not to strip the parameter. Removing `group_keys` would be a large,
risky rewrite of working, correct code for no behavioural gain. Leave the mechanism.

### F2 — the P0027 leakage bug is already FIXED

P0027 (2026-07-11) found that `engineer_features.py` grouped by `brand` only, so
region-grain lag/rolling features conflated across regions. Verified 2026-08-01: the module
now threads `group_keys` through all five functions, and the docstrings explicitly warn
about grouping by `"brand"` alone on a multi-region grain (:199-200, :254, :279, :353).

**So this bug does not need re-fixing.** It is recorded here (and in P0032) so no one
re-investigates it. Note the irony: this fix is what made the chain grain *correct* — and
DEC-GRAIN then dropped the chain grain anyway.

### F3 — data already deleted, code references remain

`02_thesis_data/_03_engineered/` contains only `bymonth/`. `bychain/` is gone from disk.
But `PATHS.py` still defines `THESIS_DATA_ENGINEERED_BYCHAIN_DIR` and
`get_category_engineered_bychain_dir()`, and ~20 live files still reference the chain grain.

Any code path still calling those helpers now resolves to a **non-existent directory** —
failing at runtime rather than at import. This half-state is the actual risk this plan removes.

### F4 — `utility_scripts/scripts/` shadows `03_thesis_modelling/`

Both trees contain near-identical `srq1_benchmark.py`, `srq1_benchmark_tuned.py`,
`srq1_figures.py`, `srq1_profiling.py`, `srq2_synthesis.py`, `srq4_experiment.py`,
`forecast_service.py`.

Per `.claude/rules/repo-tier-structure.md`, `utility_scripts/` is tooling-only and must
never hold thesis pipeline logic — so the `utility_scripts/scripts/` copies look like
P0028 leftovers. **Determine which tree is canonical before editing both** (task 2). Fixing
the wrong copy leaves the bug live.

### F5 — `phase3_region_grain_test.py` is wholly obsolete

Its docstring: *"Load the region-grain CSD feature matrix (brand×region×period, 25.1k rows)
... Compare test WMAPE against the 16.5% brand×month baseline."*

That comparison is precisely the question DEC-GRAIN closed, and it is the same test harness
task B02 was dropped for. The script has no remaining purpose. Archive rather than delete —
it is the evidence behind the grain decision.

---

## Discovered during execution

<!-- append below -->
