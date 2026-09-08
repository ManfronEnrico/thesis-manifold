---
name: p0053-start-here
description: STATE - Run the SRQ1 training suite on the VPS. Written to be read FROM the VPS with no prior conversation context.
pid: P0053
created: 2026_09_08-15_40
updated: 2026_09_08-15_40
status: in_progress
---

# P0053 — Run SRQ1 training on the VPS: START HERE

**You are probably reading this on the VPS, with no conversation history. This file
is everything you need.** Follow it top to bottom.

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
.venv/bin/pip install -r plans/P0053_2026-09-08_15-40_vps-model-training/requirements-training.txt
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
for cat,slug in (('CSD','csd'),('danskvand','danskvand'),('energidrikke','energidrikke'),('RTD','rtd')):
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

20 stages in dependency order. The order is not cosmetic: several stages guard
their reads with `is_file()` and **degrade silently** rather than failing, which is
exactly how model selection once fell through to a hardcoded default (P0049 F25).

| Tier | Stages | Notes |
|---|---|---|
| 1 | benchmark, benchmark_cv, benchmark_tuned, baselines_stat | **CV is ~52 min** — 16 Optuna studies × 100 trials × 4 folds |
| 2 | calibration, mase, demand_classes, stability | **stability ~25 min**, 5 seeds × 2 models × 4 cats |
| 3 | ridge_cv, pooled, pooled_perbrand, ridge_pooled | minutes |
| 4 | feature_diag, holiday_ablation, holiday_tuned | the holiday-enrichment result |
| 5 | train_persist, training_report, shap_figures, perf_figures, enrich_appendix | train_persist is what SRQ2 serves |

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
