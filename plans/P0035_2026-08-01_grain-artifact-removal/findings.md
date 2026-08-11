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

### F6 — Task 2 RESOLVED: `03_thesis_modelling/` is canonical; `utility_scripts/scripts/` is a stale P0028 leftover

Decision: **clean `03_thesis_modelling/` only; archive the shadow copies in
`utility_scripts/scripts/` wholesale.** Evidence, in order of strength:

1. **Git history diverges — `03_thesis_modelling/` is strictly ahead.**
   Both trees landed together in `8329881` ("Refactor: Flattening the repo structure").
   Since then `03_thesis_modelling/model_training/srq1_benchmark.py` received
   `5b64c40` ("Chore: Slight Restructuring…", +46/-10) and the tree also gained
   `d892af8` (`phase3_region_grain_test.py`, +198). `utility_scripts/scripts/`
   received **no commits after `8329881`**.

2. **The diff is a real feature refactor, not a whitespace drift.**
   `03_thesis_modelling/`'s copy is grain-aware: it adds `argparse` with
   `--grain/--grains`, `DEFAULT_GRAINS = ["bymonth"]`, graceful skip when a
   grain's matrix is absent, and fixes the feature name
   `weighted_distribution` → `weighted_dist`. It also renames the brand grain
   key `"brand"` → `"bymonth"` in `DATASETS`/`KEYS`. The `utility_scripts/`
   copy still has the pre-DEC-GRAIN shape ("Runs on BOTH granularities … _04
   brand×chain (primary)").

3. **Nothing imports or invokes the `utility_scripts/` copies.** A repo-wide
   grep for `utility_scripts/scripts` referencing any `srq*`/`forecast_service`
   returns zero hits outside `PLANS_INDEX.md`'s description of this very plan.
   By contrast `README.md`, `repository_map.md`, `PATHS.py` (via
   `THESIS_MODELLING_TRAINING_DIR`) and `harness/reviews/` all point at
   `03_thesis_modelling/model_training/`.

4. **Repo rule agrees.** `.claude/rules/repo-tier-structure.md` states
   `utility_scripts/` is tooling-only and must never hold thesis pipeline logic.

**Risk if this call is wrong:** low — the archived copies remain on disk under
`utility_scripts/.archive/scripts_p0028_shadow/`, recoverable.

### F7 — plan is stale on `PATHS.get_category_engineered_dir()`

Task 3 says the deprecated `get_category_engineered_dir()` alias "currently
redirects to bymonth". Verified in code: correct, it returns
`THESIS_DATA_ENGINEERED_BYMONTH_DIR / category`. No live caller uses it (grep:
zero non-archive hits), so it was removed outright rather than re-pointed.

### F8 — `preprocessing_csd.py` / notebook already guard the chain grain

Contrary to the plan's framing of these as things to "clean", both already
implement `GRAIN_CONFIG` with `bymonth` implemented and `bychain`/`byregion`
raising `NotImplementedError`. The only live defect was the notebook importing
`get_category_engineered_bychain_dir` from PATHS — which would become an
`ImportError` the moment task 3 removed that symbol. That import and the
`"bychain"` config entry were removed; the explanatory GRAIN HISTORY comment
was kept (it is documentation of DEC-GRAIN, not an artifact).

### F9 — `market_id` hits are NOT grain artifacts

The initial inventory grep included `market_id`, which produced many hits in
`_00_raw/` scripts and `pre_*_1_load_and_aggregate.py`. These are references to
a **raw Nielsen source column**, not to the chain/region modelling grain. Left
untouched deliberately.

### F10 — `srq1_figures.py` was chain-grain-only, not chain-grain-optional

Unlike the other consumers, `srq1_figures.py` had no bymonth path at all: Fig 1
filtered `m[m.dataset == "bychain"]` and Fig 2 computed `best_chain` from
`bychain` rows. Repointing it to `bymonth` is a behavioural change, not a
deletion — the figures it emits will now describe the brand×month grain. Flagged
for human review (it affects Ch6 figures, which is P0034 territory).

Related: `fig2_granularity.png` was a brand×month **vs** brand×chain comparison.
With the chain grain gone the comparison has no second term, so the figure is no
longer generated. The **stale PNG was deliberately left on disk** because
`05_thesis_writing/sections-drafts/ch6-model-benchmark.md:137` still cites it,
and Ch6 prose is explicitly out of P0035's scope (P0034 owns it).

### F11 — task 8 could NOT be run end-to-end: no data in the worktree

`*.parquet` and `.env` are **gitignored**, so a fresh worktree contains none of
the pipeline's inputs — they exist only in the main working folder, which this
session was forbidden to touch. Confirmed:

- `git check-ignore` -> `.gitignore:21:*.parquet`, `.gitignore:14:.env`
- `02_thesis_data/_01_converted/` holds **0** parquet files
- `02_thesis_data/_03_engineered/bymonth/CSD/` holds only
  `csd_split_dates.json` + `csd_preprocessing_report.md`; no feature matrix
- Running `python preprocessing_csd.py --run-step 4` exits 1 with
  *"ERROR: Stage 1 Parquet cache not found!"*

So task 8's regression gate was satisfied by **static verification only** — see
progress.md for the exact checks. A human must re-run the gate from the main
folder after merge.

### F12 — plan cites `apply_split :348`; the function at that line is `build_series_index`

Minor staleness in F1's line references. The substance holds: `group_keys`
defaults to `["brand"]` at all five sites (`make_calendar`, `filter_series`,
`engineer_features`, `build_series_index`, and the pipeline dataclass, which uses
the tuple form `("brand",)`). Verified by runtime signature inspection, not by
reading. `engineer_features.py` was **not modified** by this plan.

### F13 — two consumers disagree with each other on the brand-grain tag name

`srq1_benchmark.py` calls the brand×month grain `"bymonth"`; `srq1_benchmark_tuned.py`,
`srq1_figures.py`, `srq1_profiling.py` and the committed
`04_thesis_results/srq1/tuned_params.json` call it `"brand"`. This split predates
P0035 (it came from the grain-aware refactor in `5b64c40` landing in only one
script). P0035 **preserved each file's existing tag** rather than unifying them,
because renaming keys in `tuned_params.json` would silently rewrite recorded
experimental output, and renaming in the scripts would orphan those keys.

**This is a latent trap and a human should decide it.** Concretely:
`srq1_profiling.py` reads `params.get("brand/CSD/XGBoost", {})` — P0035 repointed
it from `bychain/...`, and `brand/...` keys do exist, so it works today. But if
anyone regenerates `tuned_params.json` with the current `srq1_benchmark.py`, the
keys become `bymonth/...` and every `brand/...` lookup silently falls back to
`{}` (untuned defaults) **without raising**. Recommend unifying on `bymonth` in
one deliberate pass, scripts and results together.
