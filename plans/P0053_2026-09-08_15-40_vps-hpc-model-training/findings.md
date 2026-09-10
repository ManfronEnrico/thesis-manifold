---
name: p0053-findings
description: STATE - VPS/HPC training session findings. F1 casing bug, F2 HPC migration, F3 the 5 FEATURES-fix scripts (RE-RUN & VERIFIED), F4 thesis-prose checklist, F5 --parallel (won't be reported, timing not measured), F6 training_report.py casing (FIXED), F7 redundancy tables predate 18 features, F8 table 98's WMAPE now computed not hardcoded (FIXED), F9 training_report.py's three stale refs (FIXED), F10 hardcoded-number audit + two new Correctness-tier rules.
pid: P0053
created: 2026_09_09-21_15
updated: 2026_09_10-15_00
---

# P0053 — Findings

## Next-session checklist (read this first)

- [x] ~~Fix the 5 scripts F3 names~~ — patched 2026-09-09 in `4b38c53`
- [x] ~~RUN those stages~~ — **2026-09-10, HPC job `j-12387709`: 6/6 passed
      in 18.3 min** (`pooled` 320s, `pooled_perbrand` 309s, `ridge_pooled` 1.3s,
      `feature_diag` 4.2s, `holiday_ablation` 12.3s, `holiday_tuned` 450s).
      Results committed `0614766`. The 4b38c53 fix is verified.
- [x] ~~Re-run `enrich_appendix`~~ — 2026-09-10, appendix tables 94-99 refreshed
      on the 18-feature set (`cf5fdbe`). **But see F8** — table 98's WMAPE
      figures are hardcoded and did NOT refresh.
- [x] ~~Re-run `training_report`~~ — 2026-09-10. F6 fixed (`b1dfd3c`), section-6
      path fixed (`b9e41ca`), report regenerated (`b89f2c2`).
- [x] ~~Check appendix table 97's VIF~~ — done. All three holiday columns show
      VIF = inf in all four categories on the 18-feature set. Trees ignore it;
      Ridge's L2 penalty regularizes through it, so no model result is affected
      — only table 97 carries three `inf` rows. **DECIDED 2026-09-10 (Brian):
      keep all three, add one thesis sentence noting the exact identity is a
      harmless descriptive redundancy. No retrain.** → laptop, ch4 prose.
- [x] ~~F8 — table 98's WMAPE figures~~ — **FIXED, not fallback.**
      `feature_diagnostics.py` now computes the reduced-vs-full comparison every
      run (`feature_reduction_eval.csv`); table 98 reads it. See F8 + F10.
- [ ] Work through the F4 thesis-prose checklist against the OneDrive `.docx`
      (laptop) — now has fully current, fully computed numbers.
- [x] ~~F5 — measure `--parallel` at 100 trials~~ — **not doing it.** Brian:
      won't be reported either way, it's only for our own efficiency. The code
      is on `main`, opt-in via `--parallel`, unused by default. Expected
      faster-or-marginally-slower at 100 trials; not worth proving.
- [x] ~~Hardcoded-number audit (F10)~~ — every generator swept. Submitted-output
      literals all converted to computed values (F8's 26.44/28.82,
      calibration.md's 70.7%/9-17x, stability.md's 4.7%/13x). Two rules added.
      One open item: `export_appendix.py`'s `review=` blocks — see F10.
- [ ] **Optional follow-up:** convert `export_appendix.py`'s ~6 `review=`-block
      numbers to `see F28`-style pointers (F10). Not submitted, low priority.
- [ ] **Optional:** `training_report.py` §6 sample payload shows `months_ahead:
      1`; pass H=3 or annotate if that section is published (F9).
- [x] ~~UCloud job~~ — new 4h job `j-12387709` launched 2026-09-10 ~13:31,
      port 2165. Git push works from it now (SSH key added to Brian's GitHub
      account, remote switched to `git@github.com:...`).

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

### RESOLVED in code 2026-09-09, NOT YET RE-RUN (laptop session, commit `4b38c53`)

**Read this before touching the five scripts — four of them are already patched.**

The inferred diagnosis above was correct, and it was **two distinct bugs**, not one:

| Script | Actual cause | Fix |
|---|---|---|
| `srq1_ridge_pooled.py` | — | **none needed** |
| `srq1_pooled_perbrand.py` | — | **none needed** |
| `srq1_pooled.py` | `FEATURES` was set to `[]` at module level and filled inside `main()`. Both scripts above do `from srq1_pooled import FEATURES`, so importers got an **empty list** | resolved at import instead |
| `srq1_holiday_ablation.py` | `list(FEATURES) + HOLIDAY_FEATURES` duplicates 3 columns now that FEATURES is 18 | arms derived by **subtraction** |
| `srq1_holiday_ablation_tuned.py` | same, inside `_arm_features()` | same |
| `srq1_feature_diagnostics.py` | same; duplicate column NAMES make `X[col]` return a DataFrame, which is the real source of "truth value of a Series is ambiguous" in `compute_vif()` | same |

**The empty-list bug was mine**, introduced by the same commit that caused the
duplicates — `srq1_pooled.py` needs the cross-category *intersection* (17,
excluding `promo_intensity`), so I made it computed rather than literal, and made
it computed too late. `ridge_pooled` and `pooled_perbrand` were never broken in
themselves; they were downstream of that.

**Verified:** `from srq1_pooled import FEATURES` now yields 17. All four patched
files compile.

**NOT verified: none of the five has been RUN since the fix.** The laptop session
was stopped before that. Treat these as proposed, not proven — the next machine to
pick this up should run all five before trusting any table they produce:

```bash
python run_both_horizons.py --horizon 3 --only pooled,pooled_perbrand,ridge_pooled,feature_diag,holiday_ablation,holiday_tuned
```

Note `pooled` is included and must run **first** — the other two import from it.

**Then re-run `enrich_appendix`**, per the note below: it reads tables these
scripts produce, so its output stays stale until they land.

**Still open regardless of the fix:** §0 of `START_HERE.md` recommends admitting
only two of the three holiday columns, because `non_holiday_days = days_in_month −
n_holidays` exactly and appendix table 97 reports VIF as `inf`. The centralized
`FEATURES` admits all three. `srq1_feature_diagnostics.py` is the script that
would settle whether that harms the Ridge baseline, and it is one of the five —
so check table 97 against the 18-feature set once it runs.

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

---

## F6 — `training_report.py` carried the F1 casing bug — FIXED 2026-09-10 (`b1dfd3c`)

**Found by the Chapter 4 closing prose pass**, which read
`05_thesis_results/05_model_benchmark/tables/training_report.md` as an appendix
candidate and found it contradicting the thesis. **Fixed and re-run 2026-09-10 —
see F9 for the full set of three stale references in this file.**

### The symptom

The report's per-category feature table marks **every** feature — not only the
holiday and intermittency columns — as present for CSD and RTD and dashed for
danskvand and energidrikke. Its dataset table is blunter still:

```
| danskvand    | _matrix missing_ | | | | | | |
| energidrikke | _matrix missing_ | | | | | | |
```

### The cause is F1, in a tenth script

`training_report.py:66` still reads:

```python
CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}
```

Those **keys** are passed to `matrix_path(cat, slug)`, which builds
`<engineered>/<cat>/<slug>_feature_matrix_h3.parquet`. On disk the folders are
`CSD`, `Danskvand`, `Energidrikke`, `RTD`. On Linux the two lowercase keys
resolve to nothing, `is_file()` returns False, and `_matrix()` returns `None` —
which the report renders as "matrix missing" rather than raising.

**This is exactly the bug F1 documents**, and the fix is the same one: capitalize
the keys, leave the lowercase filename slugs alone. F1 patched nine scripts;
this one was not among them, which is worth noting because the same dict
literal appears in it verbatim.

### ⚠ It does NOT mean the training must be re-run

Checked before recommending anything:

| Evidence | Says |
|---|---|
| `summary.md` | all four categories, WMAPE for each |
| `stat_baselines.md`, `tuned_summary.md` | all four |
| the eight feature matrices | 18 features resolve for CSD and energidrikke, 17 for danskvand and RTD |

**The HPC run is sound.** The four-category gate in
`writing-notes/post-hpc-validation.md` passes on the results themselves. Only
the *report about* the run is wrong, and it is generated from the matrices at
read time rather than written during training.

**So the fix is to patch one dict and re-run one script** — seconds, on any
machine, with no GPU and no training. Not a retrain.

### Why it still matters for the thesis

`training_report.md` is a candidate for the appendix. Published as it stands it
would tell an examiner that two of four categories have no feature matrix, while
Chapter 4 states feature counts for all four. That is a self-contradiction
inside the submitted document, from a table whose own header says every number
is "computed from the feature matrices and results files at run time, not
transcribed" — which is true, and is precisely why it is wrong.

### Action

1. Capitalize the two keys in `training_report.py:66`.
2. Re-run it. Confirm all four categories populate and the feature table shows
   `yes` for the holiday and intermittency rows in all four.
3. Fill the empty `what it is` column for `days_in_month`, `n_holidays`,
   `non_holiday_days`, `zero_run_flag` and `zero_run_length` — they are the only
   five rows with no description, which is the same half-populated state.
4. Grep for the remaining copies of the literal before closing F1:
   `grep -rn 'CATS\|CATEGORIES' --include=*.py | grep '"danskvand"'`

---

## F7 — The redundancy-reduction appendix tables predate the 18-feature set (2026-09-10)

**Also found by the Chapter 4 pass.** Chapter 4 §4.3 states that a feature
reduction "raised mean test error from 26.4 to 28.8 per cent". Both figures come
from `98_feature_redundancy_reduction.md`.

### The dependency, precisely

| Artefact | Written | Feature set it describes |
|---|---|---|
| `feature_redundancy_clusters.csv` | **2026-09-06 22:00** | 16 features |
| `97_feature_collinearity_vif.md` | 2026-09-08 18:51 | 16 features |
| `98_feature_redundancy_reduction.md` | 2026-09-08 18:51 | 16 features |
| `_features.py` (18 features) | **2026-09-09**, commit `3f8b0a9` | — |

The cluster file is the upstream input and is three days older than the feature
set it is supposed to describe. Its contents confirm it: the clusters name
`lag_1 … rolling_std_4` and `month + quarter` only, with **no holiday and no
intermittency columns anywhere**.

### This is not blocked on anything

`srq1_feature_diagnostics.py` imports `FEATURES` from `srq1_benchmark`, which
now re-exports the shared `_features.py` list. **It will pick up all 18
automatically** — no edit required. It was simply not re-run after `3f8b0a9`,
because the retrain was the priority and this is a diagnostics script rather
than part of the training path.

It is also **not affected by F6's casing bug**: it takes its category list from
`srq1_benchmark.CATS`, which F1 already fixed.

### What re-running changes

The reduced-set size and both WMAPE figures. The *direction* is expected to
hold — dropping correlated features from a tree model lost information at 16 and
should still lose it at 18 — but adding five features to the pool changes which
clusters form and therefore what survives reduction.

**Sequence:** run `srq1_feature_diagnostics.py`, then
`srq1_export_enrichment_appendix.py` to regenerate tables 97 and 98 from the new
cluster file.

### Thesis fallback if it is not re-run

Chapter 4 keeps the sentence but drops both decimals: *"a reduced feature set
was evaluated against the benchmark and performed worse"*. A directional claim
from a superseded feature set is defensible; a decimal from one is not. The
0.95 grouping threshold also has no cited source, so avoiding the numbers avoids
that debt too.

Tracked as H5 and H6 in `06_thesis_writing/writing-notes/post-hpc-validation.md`.

### 2026-09-10 — re-run done, and F7 is worse than stated (see F8)

Ran `feature_diag` + `enrich_appendix` on the 18-feature set. Table 98's
*structure* updated — "18 (17) features available", "9-10 after reduction", "3
clusters" (the new third cluster is `zero_run_flag + zero_run_length`). **The
"26.44 → 28.82" WMAPE comparison did not.** It is a hardcoded constant, not a
computed value — F8.

The VIF table (97) also regenerated: `days_in_month`, `n_holidays`,
`non_holiday_days` = `inf` in all four categories, confirming §0's collinearity
concern on the 18-feature set. `rolling_mean_4` is the next-highest at ~220-270.

---

## F8 — Table 98's redundancy-reduction WMAPE figures are hardcoded, not computed (2026-09-10)

**A re-run of `feature_diagnostics.py` + `enrich_appendix.py` does NOT refresh
the "26.44 → 28.82" comparison in appendix table 98.** F7 assumed it would.

The string lives in three places, all as a literal:

| File | Line | Text |
|---|---|---|
| `srq1_feature_diagnostics.py` | 240 | docstring: `WMAPE 28.82 reduced vs 26.44 unreduced` |
| `srq1_feature_diagnostics.py` | 374 | printed NOTE: `mean test WMAPE 28.82 reduced vs 26.44 unreduced` |
| `srq1_export_enrichment_appendix.py` | 313 | table 98 body: `raised mean test WMAPE from 26.44 to 28.82` |

`feature_diagnostics.py` *proposes* a reduced set (`feature_proposed_set.csv`)
but never fits models on it — the WMAPE comparison was a **manual validation run
on 2026-09-06**, on the 16-feature set, and its result was written into the code
as a cited constant. The `propose_reduced_set()` docstring says so: "VALIDATED
on 2026-09-06 and REJECTED".

### What this means

The reduced sets are now different (9-10 features from 17-18, and they now
include the holiday columns), so the 2026-09-06 numbers describe a reduction
that no longer exists. Table 98 currently pairs a **fresh structure** with a
**stale outcome**.

### Two ways to close it

1. **Run the mini re-evaluation.** For each category, fit LightGBM + XGBoost +
   Ridge on (a) the full 18/17 set and (b) `feature_proposed_set.csv`'s
   reduced set, compare mean test WMAPE, update the three hardcoded strings.
   ~10-15 min of compute. This is the only way to keep decimals in Chapter 4.
2. **Prose fallback (already drafted).** Chapter 4 drops both decimals and
   keeps *"a reduced feature set was evaluated against the benchmark and
   performed worse"*. Direction is defensible from first principles (tree
   models lose information when correlated features are removed); the specific
   numbers from a superseded feature set are not. Also sidesteps the uncited
   0.95 threshold debt.

Recommend (2): the reduction is a rejected negative result, not a headline, and
is not worth a bespoke experiment this late.

---

## F9 — `training_report.py` carried THREE stale references, all fixed 2026-09-10

Found while re-running it after F6. The file is generated into
`training_report.md`, an appendix candidate, so each of these would have
reached an examiner.

| # | Problem | Symptom in the report | Fix |
|---|---|---|---|
| 1 | `CATEGORIES` dict used lowercase keys (F1, in a tenth script F1's sweep missed) | Section 2 feature table: `_matrix missing_` for Danskvand and Energidrikke; every feature dashed for those two | `b1dfd3c` — capitalize the two keys |
| 2 | `desc` dict had no entry for the 5 columns the FEATURES centralization added | Section 2: blank "what it is" cell for `days_in_month`, `n_holidays`, `non_holiday_days`, `zero_run_flag`, `zero_run_length` | `b1dfd3c` — add the five descriptions |
| 3 | Section 6 built the `scenario_setup` path with `parents[1]`, pointing at the pre-2026-08-rename location | Section 6: `_could not call the tool: FileNotFoundError_` instead of the sample payload | `b9e41ca` — resolve from the repo root, `04_SRQ4_Scenario_Experiment/scenario_setup/` |

**Verified 2026-09-10** on the HPC: all four categories populate, the holiday
and intermittency rows show `yes` in all four, and section 6 renders a real
`forecast_demand` JSON payload.

**One thing left in section 6:** the sample payload shows `"months_ahead": 1`
because `_eval_forecast("CSD", "HARBOE")` uses its default horizon. The thesis
reports H=3. Section 6 is illustrative (it shows the payload *shape*), so this
is cosmetic, but if the section is published, either pass a horizon or add a
line noting the example is H=1.

**Also swept 2026-09-10:** full-repo `grep` for `CATS`/`CATEGORIES` dicts with
lowercase `"danskvand"` — the only live hit outside `.archive/` was
`05_thesis_results/generate_architecture_diagrams.py:103`, fixed in `97b5ecc`
(laptop-only script; its `_step4_logs()` would drop two categories on a
case-sensitive FS). F1's casing bug should now be fully closed.

---

## F10 — Hardcoded-number audit of the artefact generators (2026-09-10)

Prompted by F8. Brian: *"All of the cited numbers for any of the tables,
reports, or appendices must under no circumstances be hard coded."* Two rules
now enforce this — `.claude/rules/generated-artefact-provenance.md` and
`path-handling.md`, both in the Correctness tier.

Audited every script that writes a `.md`/`.csv`/`.svg` thesis artefact
(`grep -nE '"[^"]*[0-9]+\.[0-9]+'` per file, then classified each hit).

### Fixed — now computed every run

| Where | Was | Now |
|---|---|---|
| `enrich_appendix.py` table 98 caption | literal `"26.44 to 28.82"` (a 2026-09-06 run on 16 features) | `feature_diagnostics.py::evaluate_reduction()` fits full vs reduced per category×model, writes `feature_reduction_eval.csv`; the caption reads its means. First real run: 29.31 → 32.13 over 12 cells. Commits `1b0de33`, `b5634e97`, `0206402` |
| `enrich_appendix.py` table 98 threshold | literal `0.95` | read from `feature_proposed_set.csv`'s new `rho` column |
| `enrich_appendix.py` table 97 review | `"< 0.01pp in all eight cells"` (uncomputed) | mechanism argument, no number |
| `feature_diagnostics.py` docstring + NOTE | `"28.82 reduced vs 26.44"` | points at the CSV; the run prints the computed table |
| `calibration.py` → `calibration.md` | `"danskvand row (70.7% against a nominal 80%)"`, `"spanning 9-17x"` | interpolated from `calibration.csv` — current values 72.4% and 12-34x, and the framing adapts to whether a category under-covers. Commit `eedf3df` |
| `stability.py` → `stability.md` | `"~4.7% of its own level"`, `"~13%"`, `"three times more"` | computed from `stability.csv` rows (mean `wmape_std/wmape_mean`, mean `median_cv`, their ratio). **`stability.md` won't show the change until the next ~90-min stability re-run** — the code is fixed, the artefact lags |

### Acceptable as-is (rule carve-outs)

- **`training_report.py` §5** — `"gave q90 = 0.305 against an honest 1.194:
  intervals 3.9x too narrow"`. Historical narrative about a *fixed* bug
  (P0037 F10), explaining why calibration is done correctly now. The rule
  explicitly allows past-tense descriptions of corrected mistakes.
- **`export_appendix.py` `metric_dictionary`** — `"a weighted MAPE of 19.4
  denotes 19.4%"`. Illustrative of the notation, not a cited result.

### Open — catalogued, not yet converted

**`04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py`** — ~6 numbers
in `review=` blocks — **DONE 2026-09-10** (`a381272`, `71fe47b`). Each was an
editorial cross-reference to a finding (F21, F28, F31, P0044 F1-F2); replaced
with the finding pointer and a "read it off the table" note, numbers removed.

---

## F11 — `export_appendix.py` is not in the orchestrator, so its tables go stale on every retrain (2026-09-10)

`run_both_horizons.py`'s stage list runs `srq1_export_enrichment_appendix.py`
(tables 94-99) but **not** `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py`,
which owns appendix tables **04-15** — `04_feature_matrix`,
`05_substrate_resource_profile`, `06_retraining_cost`, `08_parameter_drift`,
`09_statistical_baselines`, `10_seed_stability`, plus the SRQ4 scenario tables.

Consequence: after yesterday's 18-feature retrain, tables 94-99 refreshed (they
were a stage) but **04-15 kept their pre-retrain numbers and lowercase category
labels**. Caught 2026-09-10 when a manual `export_appendix.py` run produced a
large diff — e.g. `10_seed_stability` CSD median CV `11.24 -> 18.16`,
`09_statistical_baselines` Prophet energidrikke `972.4 -> 975.0`, all four
categories relabelled `danskvand -> Danskvand`.

Regenerated and committed (`fbc67a3`). But the structural gap remains:

**Recommended fix (not done):** either add `export_appendix.py` to
`run_both_horizons.py`'s tier-5 stage list (it is offline and reads only result
CSVs for tables 04-10; the 11-15 scenario tables skip cleanly when SRQ4 run data
is absent), or add a one-line reminder to `START_HERE.md` §5 that it must be run
by hand after every training run. The first is better — the orchestrator is the
place that knows a run happened.

The SRQ4 scenario tables (11-15) genuinely need the scenario-experiment run data
and cannot be produced from a training run alone — those staying separate is
correct.
