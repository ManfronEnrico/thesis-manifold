---
name: p0053-start-here
description: STATE - Run the SRQ1 training suite on the VPS. Written to be read FROM the VPS with no prior conversation context.
pid: P0053
created: 2026_09_08-15_40
updated: 2026_09_10-14_15
status: in_progress
---

# P0053 — Run SRQ1 training on the VPS: START HERE

**You are probably reading this on the VPS, with no conversation history. This file
is everything you need.** Follow it top to bottom.

> **⚠ Read `findings.md` in this folder before anything else.** Training has moved
> off the VPS onto a CBS UCloud HPC job (still runnable from here per §3-4 below,
> but the VPS is now the fallback, not the primary path — see findings.md F2). A
> full 18-feature retrain completed there on 2026-09-09; 14/20 stages succeeded and
> the servable models are current, but 5 stages are still broken (findings.md F3)
> and there's a thesis-prose verification checklist waiting (findings.md F4).

---

---

## ⚠ 0. READ FIRST — the feature-set decision below is RESOLVED, differently than it recommends

**Added 2026-09-08, resolved 2026-09-09 — kept for its reasoning, but do not follow its
"only two of three" recommendation. Read the note at the bottom of this section first.**

`srq1_benchmark.py::FEATURES` used to hold **13** columns and did **not** include the
holiday enrichment (`days_in_month`, `n_holidays`, `non_holiday_days`), even though those
columns are built, time-safe, and 100% populated in every matrix.

That was deliberate under an earlier framing: holidays were held out so a *holiday
ablation* had something to measure against. **That framing was dropped on 2026-09-08.**

The thesis proposition is *whether trained models help an LLM forecast* — not whether
exogenous variables improve models. Feature contribution is not an SRQ. M4 and M5 identify
explanatory (exogenous) variables as the open frontier — a claim about exogenous inputs in
general, **not** a prescription for holiday calendars. The holiday feature is *one instance*
of that direction, adopted as a **design choice**, so no in-thesis ablation is needed.

### What this means for this run

If the suite runs with `FEATURES` unchanged, then the headline benchmark,
`srq1_benchmark_tuned`, `train_persist` (**what SRQ2 actually serves**) and every
downstream table describe a model **without** the enrichment Chapter 4 will say it has.

**Decide before launching:**

| Option | Do this | Consequence |
|---|---|---|
| **A — enriched (intended)** | add `days_in_month` and `n_holidays` to `FEATURES`, then run | Matches the literature-consistent design the chapter describes |
| **B — as-is** | run unchanged | Ch4 must state the models exclude the calendar enrichment |

**Only two of the three holiday columns may be added.** `non_holiday_days = days_in_month −
n_holidays` by construction, so all three together are exactly linearly dependent — appendix
table 97 reports their VIF as `inf` in all four categories. Trees tolerate that; the Ridge
baseline does not. Add `days_in_month` and `n_holidays`; leave `non_holiday_days` out.

**Also under option A:** stages 4's `holiday_ablation` / `holiday_tuned` become redundant as
*reported* results. They are cheap and harmless to run — but do not put their table in the
thesis; it answers a question the thesis does not ask.

**Full reasoning:** `plans/P0051_2026-09-08_00-00_eda-diagnostics-provenance/findings-feature-reduction.md`
(Part 2, R1). Chapter framing: `06_thesis_writing/writing-notes/ch4_data_assessment/why-thirteen-features.md`.

> **2026-09-09 update — what actually happened:** the FEATURES centralization fix
> (`3f8b0a9`/`67a5474`, see P0049 findings.md F31) shipped Option A but added **all
> three** holiday columns, not the two this section recommends — the canonical
> `FEATURES` list is 18 items, including `non_holiday_days`. Whether that reintroduces
> the exact `VIF = inf` collinearity problem this section warns about is **currently
> unverified**: `srq1_feature_diagnostics.py` (the script that computes VIF) is one of
> the 5 scripts broken by this same fix — see `findings.md` F3. Check appendix table
> 97 against the new 18-feature set once that script is fixed and re-run, before
> assuming this is fine for the Ridge baseline.

---

## 1. Why training moved here

The laptop has 16 GB shared with Word, VS Code, browsers and two Claude sessions —
about **1.2–1.5 GB free**. The SRQ1 suite was killed three times by the OS, twice
in the middle of `srq1_stability.py`, which writes nothing until all ~6,400 model
fits finish. Each kill cost 22 minutes and produced no output.

An individual stage only needs ~250–400 MB. The problem is not the peak, it is
**holding that for 20–60 minutes on a machine with no headroom**. The VPS has
memory and runs 24/7.

## 2. What has to be on the VPS — and what does not

**Training reads exactly one kind of data file:** the engineered feature matrix.
Verified — no SRQ1 script reads anything else at train time. Every matrix is
self-contained: features, target, and the `split` column (train/val/test) in one
file.

```
01_SRQ1_Model_Training/01_thesis_data/_03_engineered/bymonth/
  CSD/csd_feature_matrix_h1.parquet          ← 4 categories × 2 horizons
  CSD/csd_feature_matrix_h3.parquet
  ... Danskvand, Energidrikke, RTD           32 files, 4.5 MB total
```

These are **tracked in git as of P0053** (they were previously covered by the
blanket `*.parquet` / `*.csv` ignore rules). So a `git pull` is the whole data
transfer.

**Not needed on the VPS:** raw Nielsen extracts, the preprocessing pipeline, the
`_00_raw` .. `_02_preprocessing` tiers, the OneDrive `.docx`, or any API key.
Training is offline and reads no network.

> ⚠ **These files contain Nielsen data** — brand-level monthly sales for 95 named
> Danish brands, under the confidentiality agreement with Manifold AI. Brian
> decided on 2026-09-08 to track them, with the repository's public visibility
> stated at the time. Do not copy them anywhere else, and do not widen the
> `.gitignore` exception — the raw extracts and every intermediate step are still
> excluded on purpose.

## 3. Set up (once)

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold

python3 -m venv .venv
.venv/bin/pip install -r plans/P0053_2026-09-08_15-40_vps-hpc-model-training/requirements-training.txt
```

**Install that file, NOT the repo-root `requirements.txt`.** The two disagree, and
the root one is wrong for this purpose: it pins xgboost 3.4.1 / lightgbm 4.7.0 /
sklearn 1.9.0, which are the laptop's *system* python versions. Every committed
SRQ1 result was produced by the laptop **venv** — xgboost 3.2.0 / lightgbm 4.6.0 /
sklearn 1.8.0 — and `requirements-training.txt` is a freeze of exactly that.

This is not pedantry. Gradient-boosting output is version-sensitive (histogram
binning, defaults, tie-breaking all shift between minor releases), so the wrong
versions give numbers that cannot be compared with the existing results — and do
it **silently**, because both sets import cleanly and run to completion. That
already happened once on the laptop (P0049 F29).

**The venv is not optional either.** `run_both_horizons.py` resolves
`.venv/bin/python` itself and warns loudly if it is missing.

### Confirm the versions took

```bash
.venv/bin/python -c "
import xgboost,lightgbm,sklearn
assert xgboost.__version__.startswith('3.2'), xgboost.__version__
assert lightgbm.__version__.startswith('4.6'), lightgbm.__version__
assert sklearn.__version__.startswith('1.8'), sklearn.__version__
print('versions match the committed results')"
```

### Verify before running anything

```bash
.venv/bin/python -c "
import sys; sys.path.insert(0,'.')
from PATHS import get_category_engineered_bymonth_dir as D
import pandas as pd
# Category keys are the on-disk folder names -- CAPITALIZED. Lowercase here
# resolves to nothing on a case-sensitive FS (F1). Slug values stay lowercase.
for cat,slug in (('CSD','csd'),('Danskvand','danskvand'),('Energidrikke','energidrikke'),('RTD','rtd')):
    a=pd.read_parquet(D(cat)/f'{slug}_feature_matrix_h1.parquet')
    b=pd.read_parquet(D(cat)/f'{slug}_feature_matrix_h3.parquet')
    k=['brand','period_year','period_month']
    m=a[k+['lag_1','lag_3']].merge(b[k+['lag_1']],on=k,suffixes=('_h1','_h3'))
    ok=(m.lag_1_h3.fillna(-9e9)==m.lag_3.fillna(-9e9)).all()
    print(f'{cat:14s} horizon-correct={bool(ok)}  rows={len(b)}')
"
```

**All four must print `True`.** If any prints `False` the matrices predate the
horizon fix (P0049 F23) and training would reproduce the defect the whole fix
exists to remove — stop and regenerate them on the laptop instead.

## 4. Run it

```bash
cd 01_SRQ1_Model_Training/02_thesis_modelling/model_training

# in tmux/screen -- this takes 1-2 hours and must survive your ssh session
tmux new -s srq1
../../../.venv/bin/python -u run_both_horizons.py --horizon 3 2>&1 | tee /tmp/srq1_h3.log
```

`--horizon 3` only. **H=3 is the horizon the thesis reports** — a quarter is when
marketing budgets are authorised, so it is the first horizon at which a campaign
decision is actually taken (DEC-HORIZON-BOTH, narrowed 2026-09-08). H=1 exists and
works (`--horizon 1`, writes to `h1/`) but is a robustness check, not a
deliverable; running it costs another ~1–2 h for a table nobody has asked for.

**If it dies, resume — do not start over:**

```bash
../../../.venv/bin/python -u run_both_horizons.py --horizon 3 --resume
```

`--resume` skips only stages whose artefact was written *after the current run
began*, so a stale table from an earlier run never counts as done.

### What it runs

21 stages in dependency order. The order is not cosmetic: several stages guard
their reads with `is_file()` and **degrade silently** rather than failing, which is
exactly how model selection once fell through to a hardcoded default (P0049 F25).

| Tier | Stages | Notes |
|---|---|---|
| 1 | benchmark, benchmark_cv, benchmark_tuned, baselines_stat | **CV is ~52 min** — 16 Optuna studies × 100 trials × 4 folds |
| 2 | calibration, mase, demand_classes, stability | **stability ~25 min**, 5 seeds × 2 models × 4 cats |
| 3 | ridge_cv, pooled, pooled_perbrand, ridge_pooled | minutes |
| 4 | feature_diag, holiday_ablation, holiday_tuned | the holiday-enrichment result |
| 5 | train_persist, training_report, shap_figures, perf_figures, enrich_appendix, export_appendix | train_persist is what SRQ2 serves; export_appendix owns appendix tables 04-15 (added to the suite 2026-09-10, P0053 F11) |

`srq1_profiling.py` is deliberately excluded: it measures resource cost at
`n_jobs=-1` and is horizon-insensitive (DEC-DETERMINISM). **Do not add it** — its
numbers would describe VPS hardware, not the machine the thesis reports.

## 5. When it finishes

```bash
git add 05_thesis_results/05_model_benchmark/tables 05_thesis_results/05_model_benchmark/models \
        05_thesis_results/05_model_benchmark/figures
git status --short          # READ THIS BACK before committing
git commit -m "results: SRQ1 suite at H=3, run on VPS"
git push origin main
```

**Stage by explicit path. Never `git add -A`** — it would sweep in whatever else
the working tree holds.

Then on the laptop: `git pull`, and the results are back for the thesis.

## 5b. Prophet: the one dependency likely to fail on a fresh box

`prophet` compiles a Stan backend via `cmdstanpy` and is the usual install failure
on a clean Linux VM. **It fails silently in this suite**, so check it explicitly.

`srq1_baselines_stat.py` imports Prophet *inside* `run_prophet()`, and the model
loop wraps every baseline in `try: ... except Exception: continue`. So a broken
Prophet does not raise — the stage exits 0 and writes `stat_baselines.csv` with
Prophet's row present but `n_series = 0`. Same failure shape as P0049 F21/F25:
**a weaker result, not an error.**

Before the run:

```bash
.venv/bin/python -c "
from prophet import Prophet
import pandas as pd, numpy as np
d = pd.DataFrame({'ds': pd.date_range('2022-01-01', periods=36, freq='MS'),
                  'y': np.log1p(np.arange(36)*100.0)})
m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m.fit(d)
print('prophet OK ->', float(m.predict(pd.DataFrame({'ds':[pd.Timestamp(\"2025-01-01\")]}))['yhat'][0]))"
```

If it errors: `pip install --upgrade cmdstanpy && python -c "import cmdstanpy; cmdstanpy.install_cmdstan()"`,
then re-test. A build needs a C++ toolchain (`apt install build-essential`).

After the run, confirm it actually contributed:

```bash
.venv/bin/python -c "
import pandas as pd
d = pd.read_csv('05_thesis_results/05_model_benchmark/tables/stat_baselines.csv')
print(d[['category','model','n_series','wmape']].to_string(index=False))"
```

**Every model must show `n_series > 0` for every category.** A zero means that
baseline silently contributed nothing, and the statistical-baselines table in the
thesis would be missing a comparator without saying so.

## 6. Checks that must pass before the results are trusted

```bash
# 1. every stage exited 0
grep -E "exit=|FAIL" /tmp/srq1_h3.log

# 2. no artefact older than the matrices it derives from
.venv/bin/python -c "
import datetime, pathlib
mats=pathlib.Path('01_SRQ1_Model_Training/01_thesis_data/_03_engineered/bymonth')
cut=max(f.stat().st_mtime for f in mats.rglob('*.parquet'))
b=pathlib.Path('05_thesis_results/05_model_benchmark')
stale=[f for sub in ('tables','models') for f in (b/sub).glob('*') if f.stat().st_mtime<cut]
print(f'{len(stale)} artefact(s) older than the feature matrices')
for f in stale[:15]: print('  STALE', f.name)
"
```

Check 2 is the one that matters and it is cheap. It caught **46 stale artefacts**
on the laptop that reading the code had missed (P0049 F28). Anything it names was
built from different data than the run just produced.

## 7. Do not do these

- **Do not regenerate the feature matrices on the VPS.** The preprocessing pipeline
  needs the raw Nielsen extracts, which are not here and must not be copied here.
  Matrices are built on the laptop and arrive by `git pull`.
- **Do not run with a bare `python`.** See §3 — different library versions,
  silently different numbers.
- **Do not run `--horizon 1` unless asked.** ~1–2 h for a robustness table.
- **Do not add `srq1_profiling.py`.** Its numbers would describe the VPS.
- **Do not widen the `.gitignore` exception.** Only the engineered tier is tracked;
  raw and intermediate data stay out.

## 8. Related

- `plans/P0049_2026-09-07_17-50_finalizing-experiments/findings.md` — F23 (the
  horizon fix), F25 (silent selection default), F28 (46 stale artefacts), F29
  (wrong interpreter), F30 (what the CV budget costs)
- `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/_horizon.py` —
  one value drives both the input matrix and the output directory
- `.claude/rules/repo-tier-structure.md` — where scripts belong

---

## Post-HPC-run items (status as of 2026-09-10 14:15)

All surfaced by the Chapter 4 closing prose pass. **None needs a retrain.**

- **F3** — the five FEATURES-fix scripts: **RE-RUN & VERIFIED**, 6/6 passed on
  the HPC in 18.3 min. Results on `main`.
- **F6** — `training_report.py` casing bug (a tenth script): **FIXED** (`b1dfd3c`)
  and re-run. See F9 for the two other stale references in that file, also fixed.
- **F7 / F8** — the redundancy tables (97, 98): re-run refreshed table 97 (VIF)
  and table 98's *structure*, but **table 98's "26.44 → 28.82" WMAPE figures are
  hardcoded** (F8) and did not update. **Decision pending**: run a ~15-min
  mini re-evaluation, or take the ch4 prose fallback (drop both decimals).
- **VIF = inf** — confirmed for all three holiday columns, all four categories,
  on the 18-feature set (§0 above). No model result affected; table 97 carries
  three `inf` rows. **Decision pending**: keep all three + a thesis sentence, or
  drop `non_holiday_days` from `_features.py` and retrain.
- **F5** — `--parallel` timing at 100 trials still unmeasured. HPC job is up
  and idle if you want it settled.
