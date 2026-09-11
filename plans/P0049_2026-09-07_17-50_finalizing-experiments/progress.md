---
name: p0049-progress
description: STATE - Session log for P0049. What was delivered, what was tried and rejected, and exactly where the two-horizon run stopped.
pid: P0049
created: 2026_09_07-20_45
updated: 2026_09_07-20_45
---

# P0049 — Progress

## Session 2026-09-07 (evening)

### Delivered

**The horizon fix, all three layers** (F23). Implemented, verified, committed.
`engineer_features()` now takes a required `horizon`; `srq4_experiment.py` scores
`test.iloc[HORIZON-1]`; the forecast tool is passed the scored month explicitly
and reports `months_ahead`. All 8 feature matrices rebuilt.

**Both horizons made runnable** (F24). `srq1/_horizon.py` resolves ONE value per
run (`SRQ1_HORIZON`, default 3) into both the input matrix and the output
directory. 21 SRQ1 scripts routed through it. H=3 keeps the unsuffixed paths;
H=1 writes to `h1/`, so **an H=1 run cannot overwrite an H=3 result**.

**`run_both_horizons.py`** — 8 ordered stages x 2 horizons, with `--dry-run`,
`--horizon`, `--only` and `--resume`.

### Where the two-horizon run actually stopped

| Stage | H=3 | H=1 |
|---|---|---|
| benchmark | done 18:51 | done 18:25 |
| benchmark_cv | **done 19:47** (56 min) | not started |
| benchmark_tuned | **done 19:51** (3 min) | not started |
| baselines_stat | not started | not started |
| calibration | not started | not started |
| train_persist | not started | not started |
| shap / perf figures | not started | not started |

**Resume tomorrow with one command:**

```bash
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/run_both_horizons.py --resume
```

`--resume` skips only stages whose artefact was written *after the current run
began*, so a stale table never counts as done.

### Two defects found, neither of which was the task

- **F25** — `train_and_persist.py` read its five model-selection inputs from the
  results tier ROOT; they live in `tables/` and `models/`. Every read is guarded
  by `is_file()`, so selection silently fell through to a hardcoded `"XGBoost"`
  default and never consulted the CV study — beneath a long comment explaining
  why selecting on `cv_score` matters. The default was wrong for all four
  categories.
- Third instance of one pattern (F21, F22's scoring default, F25): **a
  soft-failing read of a misplaced path degrades into a weaker result rather than
  an error.** Worth a lint rule.

### Tried and rejected — do not revisit without new information

**Moving training to a VPS, and committing the feature matrices** (F27). Both were
proposed to escape memory kills. Both were wrong:

- The suite uses **282 MB** (CV) / **247 MB** (tuned). Measured while running, not
  estimated. It was never memory-hungry — `XGB_N_JOBS=1` keeps per-fit memory low.
- The kills came from **two suites running concurrently**: a `nohup` launch whose
  wrapper had returned (so it looked finished) was still alive when a second run
  started. Six orphaned processes terminated.
- Freeing them recovered ~0.1 GB. The pressure was **other applications** — Word
  424 MB, VS Code 527 MB, `MemCompression` 1.27 GB.
- The matrices are **4.5 MB total**, so GitHub limits were never the obstacle. They
  stay gitignored because of the **Nielsen confidentiality agreement with Manifold
  AI** — brand-level monthly sales for named Danish brands is the confidential
  data itself, merely transformed.

### Near-misses

- **My "RTD improves because of survivorship" hypothesis was wrong**, and I only
  found out by testing it. The 10 brands H=3 drops carry **0.3 % of test volume**,
  and WMAPE is volume-weighted. Restricting H=1 to the surviving brands moved the
  baseline 0.1 pp. Corrected in F26 rather than left standing.
- **Two files had their horizon import inserted AFTER first use** by a regex whose
  continuation pattern over-matched. Compiled fine; would have raised `NameError`
  at runtime. Caught by an explicit import-before-use scan across all files, not
  by `py_compile`.
- **`training_report.py` had its import spliced into the middle of an existing
  comment**, and referenced a `_here` variable that file does not define. Also
  compiled fine.

### State at close

- Training stopped cleanly; no half-written artefacts.
- `verify_setup.py`: **10/10, no warnings** — re-checked after the restructure.
- Horizon fix re-verified post-restructure: `h3.lag_1 == h1.lag_3` in all 4
  categories.
- The parallel session restructured `05_thesis_results/` into chapter-keyed
  folders mid-run (`srq1_model_performance` -> `06_model_benchmark`). All outputs
  survived; `PATHS.py` was updated, so the horizon helper follows automatically.

### Note on the commit history

The parallel session's commit `362fe1f` (20:34) **swept in this session's code
changes** — `engineer_features.py`, `srq4_experiment.py`, `forecast_tool.py`,
`_horizon.py`, `run_both_horizons.py` and the 21 routed scripts are all already
committed under a message about the results restructure. Nothing was lost, but
the horizon fix is not findable by its commit message. This is what selective
staging is meant to prevent.

---

## Session 2026-09-09 — experiment-side work, training moved off this machine

Training now runs on the HPC (P0053). This session deliberately covered only what
is **decoupled from training**, so results plug in when they land.

### Delivered

**F31 — the feature set.** Brian asked why training used 13 features from a
54-column matrix. Most of that gap is correct (~28 columns are contemporaneous
Nielsen measures that would leak). Two parts were not:

- holiday enrichment reached NO model, so the ablation measured a benefit the
  served model could not receive
- `FEATURES` existed as a literal in 11 live files and had already drifted

Now `srq1/_features.py`, one definition, **13 -> 18 features**. `srq1_pooled.py`
computes the cross-category intersection (17) rather than carrying a literal.

**F32 — casing sweep.** The HPC's `CATS` fix covered SRQ1; three experiment-side
files still had lowercase keys. `srq4_experiment.CAT_FILE` raised `KeyError` on
two of four categories: **scorable brands 120 -> 168**, so the funded-run sample
was missing 40 % of its population. Added `_cat_key()` (case-folded join) and
`canonical_category()` (normalises caller input, which matters because Scenario
C's caller is an LLM).

Also: the harness logged `tool_output` but never checked it. Scenario C could
have run every repeat with no `historical_*` fields, each logged `outcome: ok`.
Added `_payload_complete()`, per call and in the run trace.

**F33/F34 — traceability and the smoke test.** Read ch2 §2.5 from snapshot
`2026-09-09_16-05_prose-pass` to derive requirements rather than choosing them.
Dong et al. (2024) name four auditable artefacts; three were present, the
**prompt registry was not** — `prompts.schema_id()` existed and was never
called. Now in every trace.

`scenario_setup/smoke_test.py`: one run per scenario, ~$0.81, nine checks each
tied to a stated requirement.

### Corrected mid-session

**Brian's diagnosis of the holiday features was half right.** He proposed that
retraining on the HPC would pick them up. It would not: `available_features()`
intersects a hardcoded list with the matrix and never *adds* a column the list
omits. The HPC run would have produced a holiday-free model and needed doing
twice. Verified before accepting.

**My blanket edit of `srq1_pooled.py` was wrong.** Replacing its literal with the
full 18-item list would have made it hard-fail on Danskvand/RTD, which lack
`promo_intensity`. Pooling needs the intersection, not the union. Caught by
reading how the file used `FEATURES` rather than assuming.

### Near-misses

- Three figures (`ch6_model_selection_v2` and two siblings) existed ONLY in the
  stale `06_model_benchmark/` tree I deleted earlier. Restored from git and moved
  into the live tree. The mistake was inspecting a sample of four files, not the
  full set, before an irreversible delete.
- `requirements.txt` pins the laptop's SYSTEM python versions (xgboost 3.4.1) not
  the venv's (3.2.0). A VPS built from it would produce incomparable numbers,
  silently. Hence `P0053/requirements-training.txt`.

### State at close

- 4 commits, all pushed: `3f8b0a9`, `67a5474`, `a7002ea`, `ae4c290`
- `verify_setup.py` 10/10; all four categories resolve; 168 scorable brands;
  18 features; every payload complete at `months_ahead=3`
- Working tree holds only the parallel prose session's files

### Open, in order

1. **DEC-VENDOR** — pure writing, blocks the funded runs
2. **Scenarios D/E** — `SCENARIOS` holds A/B/C only. **Not implemented at all**,
   and the E2B template is unbuilt. B->C and D->E are the same intervention on
   two orchestrators; only one half exists
3. **Run the smoke test** once HPC results land, then the funded set

---

## Session 2026-09-10 — scenario inputs shipped, then D and E built

Two deliverables. Both are code; neither has been run against a paid endpoint.

### 1. Scenario inputs materialised (`127bbdf`)

12 per-brand CSVs to `05_thesis_results/08_experimental_evaluation/scenario_inputs/`,
3 per category at max / median / min volume, plus `index.csv` and a README.

Written by `export_scenario_inputs.py`, which calls the harness's own
`_brand_history()` rather than rebuilding the series — so it cannot drift from
what the scenarios actually run on. Two checks passed: all 12 byte-identical to
the string pasted into Scenario B's prompt, and 0 of 12 contain their own scored
month.

DEC-SHARE-CSV is what makes this shippable: the series are already filtered to
one brand and aggregated to monthly, so they disclose no more than the thesis
tables, and they are what lets an assessor re-run A–C with their own key.

### 2. Scenarios D and E written (`a941927`, plan update `b462885`)

`SCENARIOS` now holds all five. `--scenarios D,E` selects them like any other.

Everything vendor-shaped lives in one new file, `prometheus_bridge.py`, and
importing it is allowed to fail — an assessor with A–C, the shipped CSVs and an
OpenAI key must still be able to run the harness.

**Verified free:** `verify_setup.py` 13/13 with the engine; 11 passed + 2 skipped
without it; the full five-scenario ladder dry-runs to 60 runs / ~$17 at 3
stratified brands per category.

### What the build corrected — read F44 to F47

Three of these were beliefs this plan held in writing, not oversights:

| | Was recorded as | Actually |
|---|---|---|
| **F45** | "register the project WITHOUT the SQL tools" | Prometheus is a **two-agent delegation**; the tools are hardcoded in the nested coder. DEC-D-SNAPSHOT is **measured, not enforced** — a warehouse query is detected and excluded |
| **F46** | one interpreter assumed | the venvs are **disjoint**; D/E cross a process boundary, and E works because the **parent** evaluates the model and injects the payload |
| **F44** | not considered | adding D/E moved `schema_id()` to **v4**, so this had to land **before** the funded set or every paid row would be re-sent |
| **F47** | `_classify` had 5 classes | engine failures need their **own** classes; `engine_unavailable` as `code_error` would let an unplugged machine read as evidence about Prometheus |

### Near-misses

- **The graph ends at `interrupt()`**, so it needs a checkpointer. Compiling it
  bare — as the vendor's own module-level handle does — fails at *invoke*, not at
  compile. Caught by reading the vendor before running it.
- **The sandbox leaks `df` between observations.** The engine reuses
  `code_interpreter_id` and the coder's kernel keeps DataFrames alive, so one
  brand's data would be visible while forecasting another — and it would look
  like unusually good performance, not like a bug. Now killed after every run
  including failures.
- **A shell heredoc silently collapsed `\n` escapes** in the prompt strings,
  producing unterminated literals. Reverted and redone by writing the patch to a
  file. Lesson: prompt text with escapes never goes through a heredoc.
- I nearly wrote a blunt regex to repair those strings in place; it could have
  corrupted unrelated literals. Reverting to a known-good file was cheaper and
  safer than a clever fix.

### State at close

- 4 commits pushed: `127bbdf`, `a941927`, `b462885`, plus this log
- `verify_setup.py` 13/13; five scenarios registered; schema `v4-five-scenarios`
- **Nothing has been spent.** D and E have never been run
- Working tree otherwise holds only P0050's figure session

### Open, in order

1. **Smoke D and E** — `python smoke_test.py --scenarios D,E`, ~$0.90 estimated.
   This is the step that replaces both placeholder cost estimates with
   measurements. A defect here costs $1; the same defect in the funded set costs
   $40. **Needs Brian's go-ahead: it spends money.**
2. **The three OPEN QUESTIONS** in `findings.md` — Q-A (the brand sample for D/E,
   now partly answered: the full ladder at 3/category is 60 runs / ~$17), Q-B
   (how the reduced dataset is declared in BOTH design and limitations), Q-C
   (whether the 39-row aggregate is the right shared input)
3. **The funded set** — gated on 1 and 2
4. **HPC-side (P0053)** — the 4 patched scripts are still unverified; re-run
   `enrich_appendix`; check appendix table 97's VIF against the 18-feature set

---

# Session 2026-09-11 — first paid runs, seven arms, ready to fund

The longest session on this plan. **Every open item from the previous entry is
closed or superseded.**

## Delivered

| | |
|---|---|
| **First paid executions** | three runs, ~$4.86 estimated across the day |
| **Scenarios F and G** | the combined arm, on both orchestrators — five rungs became seven |
| **Arm rename** | `<letter>_<orchestrator>_<inputs>`, 39 occurrences, 6 scripts |
| **Volume floor** | `MIN_SCORED_UNITS = 1000` on the stratification pool |
| **Web-search pricing** | the one genuinely unpriced component |
| **Funded run** | specified, dry-run verified, waiting only on credit |

## What the seven-arm smoke measured

CSD/HARBOE, target 2026-03, actual 6,365,900. All 8 checks pass.

**The headline: `deviates_from_model=True` on BOTH F and G.** Neither returned
the model's 4,969,050, and both cited its low confidence tier and wide interval
as the reason to weigh it rather than adopt it. DEC-COMBINED-INPUT measured
integration rather than deference, which is what it was written to do. That is a
result for SRQ2 independent of accuracy.

`sql_calls: []` on D, E and G. `usage_reported: true` on all three engine arms.

## Defects found and fixed

Seven, of which **five would have silently corrupted the funded set**:

1. **F49a** — smoke_test built its command without `--full`, so it took the demo
   branch and persisted nothing. Five paid runs existed only in scrollback.
2. **F49b** — Scenario E classified `no_evidence` while behaving correctly; it is
   handed its forecast and is *supposed* to make no tool calls.
3. **F51** — the one-month check read a non-existent column; the horizon check
   passed vacuously over an all-`None` list. Both now fail on absent evidence.
4. **F55** — two checks compared this run against an *accumulated* runs.csv.
   Neither was a real defect, which is the problem: a check that cries wolf gets
   explained away.
5. **F56** — the summary generator **relettered the arms under the old reversed
   scheme**, so the table contradicted its own caption and mixed two lettering
   systems in one header row. The appendix had it right, so the artefacts
   disagreed with *each other*.
6. **F58** — stratifying CSD returned **VOELKEL at 9 units/month**, where one
   unit of error is 11.1% APE.
7. **F59** — `--brand-strategy stratified` silently selected **four** brands.

## Tried and rejected

- **Size-bucketed conformal calibration (F52).** I proposed a ±1.35x band from 28
  rows covering 4 brands, then measured it properly: only 0–4 brands per category
  exceed 1M units/month (RTD has **zero**), so every large bucket falls back to
  pooled. No scheme won more than 2 of 4 categories. **F50 options 2 and 3
  withdrawn.** Saved an HPC night.
- **A 1.77x cost multiplier for funding.** See the correction below.

## MY OWN ERROR, corrected same session

**I told Brian the cost estimate under-reports by up to 1.77x while he was
deciding how much money to load.** It does not. The costs endpoint buckets by
whole **day**, so I was comparing one run against the whole organisation's daily
spend. Summing every run on 2026-09-11 gives **$4.86 estimated vs $4.03 billed —
the estimate is CONSERVATIVE by ~17%**.

The tell was visible and I walked past it: `tokens_cached_in = 0` on every run
against a non-zero cached-input charge. A billed line item with no matching
activity means **the window is wrong, not the estimate**.

`fetch_billed_cost` now documents the day-bucket behaviour and forbids that
division. F57 carries the full correction.

## Near-miss

The dry run for the funded command selected **four** brands including CARIBIA and
LØGISMOSE, because `--brands-per-cat` defaulted to `[4,4,4,3]` and the count came
from a different flag than the strategy. Nothing errored. It would have cost ~33%
more and measured a different sample than the writing notes justify. Caught one
step before launch (F59), and fixed structurally rather than by remembering to
pass two flags.

## State at close

- **On `main`**, working tree clean but for the smoke results (untracked,
  deliberately — 9 MB with Nielsen history embedded in every cached prompt)
- `verify_setup.py` **13/13**; seven scenarios; schema `v5-seven-scenarios+d22fe7cdc30e`
- A–E prompt strings **byte-identical to v4**, so earlier paid runs stay poolable
- **Prometheus reachable** as of 20:30
- Spent today: **~$4.86 estimated**, org-wide day billed $4.03

## Open, in order

1. **The funded run.** Brian is loading **$50**; it estimates **$19.33** and takes
   **80–100 minutes**. Deferred to tomorrow — the office window was 71 minutes.
   Command and pre-launch checks: **`LAUNCH_THE_FUNDED_RUN.md`** in this folder.
2. **Chapter 6 prose** — unblocked; the parallel session left
   `ch6-CONSOLIDATED-pass.md` ready, with three small decisions pending in its
   part 4.3.
3. **HPC-side (P0053)** — 4 patched scripts still unverified; re-run
   `enrich_appendix`; check appendix table 97's VIF against the 18-feature set.
4. **`unverified-claims-to-check.md` is MISSING** — see the flag below.

## ⚠ Found during the end-of-day sweep, NOT from this session

`06_thesis_writing/writing-notes/unverified-claims-to-check.md` **does not exist
on disk.** It was deleted in commit `202f75a` *"Messy Handover: All combined 2"*,
while every verification brief it indexes is still present under
`notebookLM/04-Claims_Verification/`.

`START_HERE.md:174` still cites it as the register for CV-01…CV-05, and
`prose-insertion-discipline.md` names it as **the single queue** for unverified
claims — "a claim named in a writing note but absent from the register will not
be verified".

**Not restored**, because it predates this session and the right content is a
judgement call. Recoverable with `git show 202f75a^:06_thesis_writing/writing-notes/unverified-claims-to-check.md`.
