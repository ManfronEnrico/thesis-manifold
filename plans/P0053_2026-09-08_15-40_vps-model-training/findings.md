---
name: p0053-findings
description: STATE - VPS/HPC training session findings. F1 category-casing bug, F2 HPC migration, F3 the 5 scripts still broken by the FEATURES fix, F4 what changed in the retrain (thesis-prose checklist), F5 unfinished parallelism work.
pid: P0053
created: 2026_09_09-21_15
updated: 2026_09_09-21_15
---

# P0053 — Findings

## Next-session checklist (read this first)

- [ ] Fix the 5 scripts F3 names — `pooled_perbrand.py`, `ridge_pooled.py`,
      `feature_diagnostics.py`, `holiday_ablation.py`, `holiday_ablation_tuned.py`
- [ ] Re-run just those 5 stages once fixed (`--only pooled_perbrand,ridge_pooled,feature_diag,holiday_ablation,holiday_tuned`)
      — cheap, none needs the CV search redone
- [ ] Work through the F4 thesis-prose checklist against the OneDrive `.docx`
- [ ] Decide what to do with the UCloud job — user extended it +1h tonight
      (9-Sep) after the run had already finished; it may since have been
      auto-terminated by the platform, or may still be sitting idle burning
      budget. Check before assuming either way.
- [ ] Decide whether to commit to `--parallel` for the next real CV run, or
      leave it unused until timing is actually measured at 100 trials (see F5)

---

## F1 — Category-name casing silently dropped Danskvand/Energidrikke on Linux (2026-09-09)

**Commit:** `9745bf3` (VPS session, before the HPC move)

9 scripts hardcoded a `CATS = {"CSD": "csd", "danskvand": "danskvand", ...}`
dict whose **keys** are used to resolve `get_category_engineered_bymonth_dir()`.
On Windows (laptop, case-insensitive NTFS) `"danskvand"` happily resolves the
folder actually named `Danskvand`. This VPS, and later the UCloud box, are
Linux — case-sensitive — so it resolved to nothing, and each stage's
`is_file()` guard silently treated that as "no feature matrix yet" and
skipped the category, with no error anywhere. Visible in the first VPS run's
log: `danskvand skipped — no feature matrix at grain='bymonth' yet`.

**Hit `train_and_persist.py` itself** — the script that persists the served
models — so an unnoticed run would have shipped CSD and RTD only, silently
missing two of four categories. Same failure shape as the project's own
documented P0049 F25/F28.

Fixed by capitalizing the dict *keys* to match on-disk folder names (`CSD`,
`Danskvand`, `Energidrikke`, `RTD`) while leaving the *values* (lowercase
slugs used in filenames, which really are lowercase) unchanged, across:
`srq1_benchmark.py`, `srq1_benchmark_cv.py`, `srq1_benchmark_tuned.py`,
`srq1_baselines_stat.py`, `srq1_calibration.py`, `srq1_pooled.py`,
`srq1_generate_performance_figures.py`, `srq1_generate_shap_figures.py`,
`train_and_persist.py`.

**The same bug class exists elsewhere too** — `verify_setup.py` under
`04_SRQ4_Scenario_Experiment/scenario_setup/` hardcodes lowercase category
folder paths directly (bypassing `PATHS.py`'s helper entirely) and fails the
same way. Out of scope for SRQ1 training, flagged to the laptop side; fixed
independently there in `a7002ea` the same night.

---

## F2 — Training moved from the VPS to a CBS UCloud HPC job (2026-09-09)

The VPS is a shared box (Docker-hosted "Plane" project-management stack,
n8n, Qdrant, Ollama, other tmux sessions) with periods of heavy, unrelated
CPU contention — `benchmark_cv` (16 Optuna studies, ~6,400 fits) ran **20+
hours without finishing** there against a documented ~52-minute uncontended
estimate, confirmed via cgroup CPU-throttling stats and a crash-looping
Docker service competing for the same cores.

**Moved to UCloud** (`ssh.cloud.sdu.dk`, DeiC Interactive HPC / SDU K8s
backend, workspace `BrianRohde#4971` with the 5,000 core-hour grant — there
are two identically-named workspaces, the OTHER one is a decoy with a
different, much smaller allocation). Job type: `coder-python` (browser VS
Code), machine `cpu-amd-zen5-16-vcpu` (16 cores / 48GB, confirmed via
`/sys/fs/cgroup/cpu.max` = 16 and `memory.max` ≈ 48GB — `nproc`/`free -h`
inside the container report the shared host's totals, not the cgroup quota;
don't trust them for sizing). Drive `/Master Thesis (12386697)/` mounted at
`/work/Master Thesis`. GPU (`gpu-nvidia-b200`, 200h budget) was considered
and rejected — nothing in this pipeline uses GPU-accelerated code paths, and
the datasets (a few thousand rows/category) are too small for GPU tree
building to win over CPU even if it were wired up.

SSH access: dedicated key `~/.ssh/cbs_hpc_ed25519` on the VPS, registered as
an SSH key on the UCloud job. **UCloud is job/App-based, not a persistent
login-node cluster** — SSH connects to a specific running job's container,
not a shared always-on host.

**Time allocation is a hard platform-enforced limit, independent of browser/
SSH state.** First job: 4h, started 17:10:17 CEST. The *training process*
itself is fully detached (`setsid`/`nohup`/`disown`, no controlling
terminal) and survives closing the browser or dropping SSH — but the whole
job container gets killed by the platform when its allocated time runs out,
regardless. User extended it +1h partway through. Check current job state at
the start of the next session before assuming it's still up.

**Cost measured, not estimated:** the full run used ~16 cores × 190 minutes
≈ 51 core-hours, against the 5,000-hour grant. Budget was never the binding
constraint on any of tonight's work.

**One incident:** `tmux` server died mid-run from an accidental Ctrl-C
during a botched detach (should be `Ctrl-B` then release then `D`). Root
process wasn't touched, but the whole session — including the training
subprocess as its child — went down. Fixed by decoupling the training
process from tmux entirely (`setsid nohup ... & disown`, PID tracked
separately) so a terminal mistake can no longer take it down; a disposable
`tail -f`-only tmux session is used for convenience viewing instead. A
**second incident**, mid-testing: I ran a manual timing comparison on an
isolated clone on the SAME job while the live run's `stability` stage was
still active, and the two contended for the same 16-core quota (confirmed:
~1740% combined CPU demand against a 1600% quota) — likely responsible for
part of `stability`'s 93-minute runtime against a ~25-minute plan estimate.
Caught only because the user asked what the live run was doing. **Lesson:
never run anything else on a job with a live training run in progress,
including in a separate clone — they share the same cgroup.**

---

## F3 — Five scripts still broken by the FEATURES centralization fix (2026-09-09)

**This is what "fix the 5 scripts" refers to** — not a casing issue (that's
F1, already fixed). This is a *second, independent* gap from the FEATURES
centralization the laptop side did in `3f8b0a9`/`67a5474` the same night
(see P0049 findings.md F31 for the original bug: holiday and intermittency
columns were engineered into every matrix but named in no `FEATURES` list,
so no model ever received them — 13 features shipped where 18 should have).

That fix touched 11 scripts (`srq1_benchmark.py`, `srq1_benchmark_cv.py`,
`srq1_benchmark_tuned.py`, `srq1_calibration.py`, `srq1_pooled.py`,
`srq1_profiling.py`, `srq1_generate_shap_figures.py`,
`srq1_generate_performance_figures.py`, `train_and_persist.py`,
`training_report.py`, `srq4_experiment.py`) to import the feature list from
the new single source, `srq1/_features.py`, instead of hardcoding it.

**Five sibling scripts were not on that list and still hardcode their own
feature-list logic**, specifically around the holiday columns. Confirmed
failing on the full 18-feature retrain, all with the same shape of error —
a duplicate or empty feature set reaching the model:

| Script | Error observed tonight |
|---|---|
| `srq1_pooled_perbrand.py` | `LightGBMError('Forced splits file includes feature index 0, but maximum feature index in dataset is -1')` — empty feature set |
| `srq1_ridge_pooled.py` | `ValueError: Found array with 0 feature(s) (shape=(1615, 0))` — empty feature set |
| `srq1_feature_diagnostics.py` | `ValueError: The truth value of a Series is ambiguous` inside `compute_vif()` — likely a downstream symptom of the same empty/malformed set |
| `srq1_holiday_ablation.py` | `LightGBMError: Feature (days_in_month) appears more than one time.` |
| `srq1_holiday_ablation_tuned.py` | Same duplicate-feature error, in the Optuna objective |

**Likely root cause:** these scripts' own "with holiday features" arm
probably still manually appends `days_in_month`/`n_holidays`/
`non_holiday_days` onto a base list, on the assumption that the base list
(the old 13) didn't already include them. Now that the centralized 18-item
`FEATURES` already includes those three columns, the "with" arm ends up
with duplicates, and something in the "without" arm's subtraction logic
probably nets out to zero columns instead of 15. **Not yet read in detail —
this is the shape of the bug inferred from the tracebacks, not a confirmed
diagnosis.** Read each script's own feature-list construction before
patching; the fix is almost certainly "import from `_features.py`, drop the
manual append/subtract," mirroring the treatment the other 11 got, but each
script's exact "with/without holiday" mechanics need to be understood first
so the ablation still tests what it's supposed to test.

**Not on `train_persist`'s dependency path** (confirmed by reading its
source: it reads only `metrics.csv`, `tuned_metrics.csv`, `cv_metrics.csv`,
`cv_params.json`, `tuned_params.json`) — so none of this blocked the
servable models. The irony: `holiday_ablation`/`holiday_ablation_tuned` is
the exact study that motivated the original FEATURES fix ("the holiday
ablation was reporting a benefit the production model could not obtain"),
and it's now the one still producing nothing rather than a wrong number —
loud failure instead of a silent one, at least.

A sixth stage, `enrich_appendix`, also failed tonight (`ModuleNotFoundError:
tabulate`) — unrelated to the above, just a missing pin in
`requirements-training.txt`, fixed in `318b4cf`. Verified locally that it
now runs to completion — **but it reads `94_holiday_ablation_tuned` and
similar tables that F3's broken scripts didn't regenerate tonight**, so
until those are fixed and re-run, `enrich_appendix`'s own output will be
built from stale (pre-this-run) holiday-ablation numbers even though the
script itself no longer crashes.

---

## F4 — What the retrain changed (thesis-prose verification checklist)

Full run: commit `0e95850`, 190.3 minutes on UCloud, 14/20 stages succeeded
(the 6 failures are F3). All four categories now train on **18 features**
(was 13) — this is the number that matters for any prose stating a feature
count.

**Check every one of these against the current OneDrive `.docx` before
trusting old prose:**

| What changed | Detail | Where to check in the thesis |
|---|---|---|
| **Feature count** | 13 → 18. Holiday columns (`days_in_month`, `n_holidays`, `non_holiday_days`) and intermittency columns (`zero_run_flag`, `zero_run_length`) now reach every model. | Any sentence stating "13 features" or listing the feature set explicitly — likely ch4 (data assessment) and ch6 (model benchmark). The laptop side already folded some of this into `06_thesis_writing/writing-notes/ch4_data_assessment/` (see `.archive/2026-09-09_why-thirteen-features-folded-in.md` and `ch4-prose-pass.md`) — check whether that pass already covers this run's numbers or predates it. |
| **CSD best-model selection changed** | Untuned benchmark: CSD's best model is now **Ridge** (19.1% WMAPE), was **XGBoost** on the old 13-feature set. The other three categories kept their prior winner. | Any prose naming XGBoost as CSD's best/selected model. |
| **Served models per category** | `train_persist`'s final selection (reads the *tuned*/*CV* tables, not the plain benchmark): CSD → XGBoost, Danskvand → XGBoost, Energidrikke → LightGBM, RTD → LightGBM. (Note this differs from the untuned-benchmark table above by design — `train_and_persist.py`'s own docstring explains why: tuned/CV selection, not the plain ranking ladder.) | Whatever chapter states which model is actually deployed per category. |
| **Untuned benchmark WMAPE, all 4 categories** | CSD 19.1% (was ~20.1%), Danskvand 30.2% (was ~30.4%), Energidrikke 17.8% (was ~17.3%), RTD 27.7% (was ~28.4%). Three of four improved; source: `tables/metrics.csv`/`summary.md`. | Any cited WMAPE figure in the results/benchmark chapter. |
| **CV-tuned numbers (the rigorous result)** | Fresh in `tables/cv_metrics.csv`/`cv_summary.md`/`cv_params.json` — 16 studies, 100 trials × 4 folds each, first time this has been run to completion on the 18-feature set at all. | This is likely the PRIMARY number chapter 6 cites — verify against whatever's currently written, since this may be the first time a real 18-feature CV result exists to compare against at all. |
| **SHAP feature importance** | Regenerated (`shap_importance.csv`/`.png`) — now includes the 5 previously-invisible columns as candidates. | Any SHAP figure/table reference, and any prose claiming a specific feature ranks highest/lowest. |
| **Stability (seed variance)** | Fresh (`stability.csv`/`.md`/`stability_by_cell.csv`) — first run on 18 features. | Any prose citing seed-stability numbers. |
| **Statistical baselines (ARIMA/Prophet/Naive/Ridge)** | Fresh (`stat_baselines.csv`/`.md`). These don't consume `FEATURES` the same way (ARIMA is univariate, Prophet fits its own model) so are unaffected by the feature-count change itself, but ARE freshly regenerated numbers. | Any cited ARIMA/Prophet WMAPE. |
| **Demand classification, MASE, calibration** | All fresh, all straightforward re-derivations (`demand_classes.*`, `mase.*`, `calibration.*`). | Low risk of prose drift, but re-derived nonetheless — check if specific numbers are quoted. |
| **NOT regenerated — still describes the OLD (13-feature or earlier) state** | `pooled_perbrand`, `ridge_pooled`, `feature_diag` (VIF/permutation importance/redundancy), `holiday_ablation`, `holiday_ablation_tuned`, and by extension `enrich_appendix`'s appendix tables 94-99. **Any prose citing these is describing stale data until F3 is fixed and re-run.** | Chapter 4's feature-selection/VIF discussion, the holiday-enrichment finding specifically (the one that motivated this whole fix), and the pooled-vs-per-category comparison discussion. |

**Category-label casing note (cosmetic, not a correctness bug):** rows
written by the *pre-fix* laptop code label the `category` column lowercase
(`danskvand`), rows written *after* F1's fix label it `Danskvand`
(capitalized, matching the real name). If any downstream analysis groups or
joins on that column as a literal string, old and new rows won't merge
cleanly. Not observed to cause a problem yet, but worth knowing if a
prose-verification pass finds a table that looks like it's missing rows for
one category.

---

## F5 — benchmark_cv --parallel: built and correctness-verified, speed NOT verified at scale (2026-09-09)

**Commits:** `183adce1` (code), landed on `main`, not yet used for a real run.

Two changes to `srq1_benchmark_cv.py` / `run_both_horizons.py`:

1. **`PYTHONUNBUFFERED=1`** in every stage's subprocess env (orchestrator
   fix). Root cause: each stage's stdout is a pipe (`... | tee logfile`),
   not a TTY, so Python fully block-buffered every child process — prints
   existed in the code (one line per completed study, 16 per
   `benchmark_cv` run) but never reached the log until the process exited.
   Confirmed this explains the total silence observed during the whole
   87-minute uncontended `benchmark_cv` run tonight. This part is a pure
   visibility fix with no interaction with correctness or speed.

2. **`--study CAT/MODEL/METRIC`, `--parallel`, `--merge-partials`** on
   `srq1_benchmark_cv.py`. `--parallel` runs the 8 XGBoost studies as
   concurrent subprocesses (safe: `XGB_N_JOBS=1` is already pinned for
   determinism, so N processes = N cores, no nested oversubscription) and
   the 8 LightGBM studies sequentially, unchanged (its `n_jobs` is unset —
   pinning and measuring that, the way `XGB_N_JOBS` was measured, is a
   separate decision, deliberately not made tonight). Each study writes a
   uniquely-named partial file; `--merge-partials` aggregates them through
   the same `_write_outputs()` the sequential path uses, so the two paths
   can't drift into writing different output shapes. Fails loudly (not
   silently) if any of the 16 expected partials is missing.

**Correctness: verified.** Side-by-side test on isolated UCloud clones,
identical trial count and seed: `--parallel`'s XGBoost studies reproduced
sequential mode's numbers bit-for-bit (CSD/XGBoost/wmape: 19.4% WMAPE,
41.8% medMAPE, cv=18.9 in both — matching to the decimal).

**Timing: NOT verified at production scale (100 trials).** Every test used
10-40 trials for turnaround time, and at that range a fixed per-process
overhead (~1.5-2s: Python cold-import + re-reading the category's parquet
file, paid once per subprocess) is a large enough fraction of the total
that neither the fold-level nor the study-level parallel version measured
faster than sequential in isolation:

| Test | Trials | Sequential | Parallel | Delta |
|---|---|---|---|---|
| Fold-level (first attempt, fresh thread pool per trial) | 10, 1 cat | 2m04.9s | 2m16.3s | **9% slower** |
| Fold-level (fixed: pool reused per study) | 10, 1 cat | 2m04.9s | 1m53.1s | 9.4% faster |
| Study-level `--parallel` | 10, 2 cats | 1m37.5s | 1m44.5s | **7% slower** |
| Study-level `--parallel` | 40, 2 cats | 14m48.0s (888s) | *not cleanly measured — contended with the live `stability` run, see F2* | inconclusive |

The overhead is flat per process, not per trial, so it should dilute as
trials increase toward 100 — expected to win clearly at production scale,
but that is an expectation from the shape of the cost, **not a
measurement**. The one attempt to measure it cleanly at 40 trials was
contaminated by running on the same job as the live training run (F2's
second incident) and was abandoned rather than reported as a number.

**Before trusting this for a real result:** run `--parallel` once, cleanly,
alone on a job with no other work happening, at the real 100-trial count,
and compare wall-clock against a sequential run at the same trial count.
Only then is the speed claim actually verified rather than inferred.

---

## Related

- `plans/P0049_2026-09-07_17-50_finalizing-experiments/findings.md` F31 —
  the original FEATURES-list gap this whole session traces back to
- `06_thesis_writing/writing-notes/ch4_data_assessment/` — the laptop
  side's own prose-adaptation pass; check dates against this run before
  assuming it already covers tonight's numbers
- `START_HERE.md` (this folder) — the original run-it-on-a-VPS playbook;
  still accurate for setup, now superseded on *where* to run it (F2)
