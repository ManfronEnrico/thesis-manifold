---
created: 2026-04-16
updated: 2026-04-16 (v2 — full canonical ML pipeline + skill mapping)
status: APPROVED structure — awaiting operational decisions before code
---

# Plan: ML Retraining with New Skills (SRQ1) — v2

> **Goal**: Re-run SRQ1 forecasting end-to-end using the canonical ML pipeline
> (clean → EDA → FE → split → preprocess → baseline → advanced → explain → publish)
> with the 22 new academic skills imported by Brian on 2026-04-15.
>
> **Why v2**: v1 skipped data cleaning, EDA, feature engineering, splits, and
> preprocessing pipeline — assumed `feature_matrix.parquet` from 2026-04-13 already
> encoded all of that. Enrico flagged the omission. v2 redoes everything visibly.

## Context

- **Previous run** (2026-04-13): 7 models benchmarked, Global LightGBM v2 best at 22.5% MAPE
- **Outputs preserved**: [thesis/analysis/outputs/phase1/](../../thesis/analysis/outputs/phase1/) — baseline to beat
- **Data verified accessible** (Step 1 of session): Nielsen warehouse (53 tables, 2.5M rows on csd_clean_facts_v) + Indeks (266 MB, 6,364 cols) + feature_matrix.parquet (3,234 × 22)

## Scope

SRQ1 only: DVH EXCL. HD market, 77 brands, time series Oct 2022 → Mar 2026.
Indeks data **considered** for cross-source feature engineering at Step 04, NOT
for separate research questions (those would be SRQ2/SRQ3, separate plan).

---

## 11-Step canonical pipeline

| # | Step | Primary skills | Support skills | Output artefact |
|---|---|---|---|---|
| 00 | Setup & manifest | — | — | `MANIFEST.json` (versions, hashes, seed) |
| 01 | Data ingestion (raw) | `polars` | — | `data/raw/{nielsen_csd, indeks}.parquet` |
| 02 | Data Cleaning | `polars`, `statistical-analysis` | `scientific-critical-thinking` | `data/clean/*.parquet` + `cleaning_report.md` |
| 03 | EDA | `exploratory-data-analysis`, `seaborn` | `matplotlib` | `reports/eda/*.html` + plots |
| 04 | Feature Engineering | `statsmodels`, `polars` | `hypothesis-generation` | `data/features/feature_matrix_v3.parquet` |
| 05 | Dataset split | `scikit-learn` | `statsmodels` | `data/splits/{train,val,test}.parquet` + `split_strategy.md` |
| 06 | Preprocessing pipeline | `scikit-learn` | — | `pipelines/preprocessor.pkl` |
| 07 | Baseline models (simple) | `statsmodels`, `scikit-learn` | `statistical-analysis` | SeasonalNaive, OLS, Ridge, ARIMA |
| 08 | Advanced models | `aeon`, `pymc` | `scikit-learn` (LightGBM/XGBoost) | LightGBM, XGBoost, PyMC, aeon DL |
| 09 | Explainability | `shap` | `seaborn` | `thesis/analysis/outputs/.../shap_plots/*.png` |
| 10 | Publication figures + comparison | `scientific-visualization` | `matplotlib`, `seaborn` | PDF for thesis Ch. 4 + `COMPARISON.md` |

---

## Where the code will live

```
scripts/ml_retraining/
├── 00_setup.py
├── 01_ingest_raw.py
├── 02_data_cleaning.py
├── 03_eda.py
├── 04_feature_engineering.py
├── 05_split.py
├── 06_preprocessing_pipeline.py
├── 07_baselines.py
├── 08_advanced_models.py
├── 09_shap_explain.py
├── 10_publication_figures.py
├── run_all.py              ← optional orchestrator with --skip flag
└── README.md               ← run order + what each outputs
```

**Why `scripts/ml_retraining/`**:
- `ai_research_framework/` is System A frozen (per `.system_a_frozen.md` boundary marker)
- Keeps retraining isolated from baseline (`thesis/analysis/outputs/phase1/` untouched)

## Outputs Enrico can inspect

```
data/
├── raw/                    ← snapshots of original data
├── clean/                  ← post-cleaning
├── features/               ← post feature engineering
└── splits/                 ← train/val/test parquet

pipelines/
└── preprocessor.pkl        ← reusable sklearn pipeline

reports/
└── eda/                    ← auto-generated HTML + plots

thesis/analysis/outputs/ml_retrain_2026-04-16/
├── classical_results.csv
├── advanced_results.csv
├── pymc_intervals.csv
├── shap_plots/*.png
├── models/*.pkl            ← saved models for later inspection
├── run_log.txt
├── MANIFEST.json
└── COMPARISON.md           ← summary table for thesis Ch. 4

docs/thesis/figures/
├── fig_model_comparison.pdf
├── fig_brand_winners.pdf
└── fig_shap_summary.pdf
```

## Dependencies status (verified 2026-04-16)

```
✅ sklearn 1.6.1     ✅ lightgbm 4.6.0    ✅ xgboost 3.0.2
✅ statsmodels 0.14.6 ✅ pandas 2.2.3       ✅ numpy 2.2.5
✅ shap 0.48.0        ✅ seaborn 0.13.2     ✅ matplotlib 3.10.3
✅ prophet 1.3.0
❌ aeon       — needed for Step 08 (deep learning)
❌ pymc       — needed for Step 08 (Bayesian)
❌ polars     — needed for Steps 01, 02, 04 (large data)
```

## Estimated runtime

~3 hours total on Mac (no GPU):
- Steps 00–06: ~45 min (ingestion, cleaning, EDA, FE, split, preprocess)
- Step 07: ~20 min (baselines)
- Step 08: ~90 min (LightGBM + XGBoost + PyMC top-10 brands + aeon DL)
- Steps 09–10: ~25 min (SHAP + figures)

## Gates (no run alla cieca)

| Gate | Check | If fails |
|---|---|---|
| G1 — Pre-flight | Packages present, data accessible, output dir not existing | Stop, ask Enrico |
| G2 — Sanity (Step 07) | SeasonalNaive reproduces ~49.4% MAPE from 2026-04-13 | Stop — data drift |
| G3 — Per-step | Each script returns exit 0 | Stop on failure |
| G4 — Comparison (Step 10) | Generate report before any "use new results" decision | Report only |

## What I will NOT do without asking

- ❌ Touch `ai_research_framework/` (System A frozen)
- ❌ Modify `thesis/analysis/outputs/phase1/` (baseline untouched)
- ❌ `pip install` anything without explicit go-ahead
- ❌ Push commits to GitHub
- ❌ Train deep learning models > 100k params (overfit risk on 35-period data)

## Skills NOT used in this pipeline (and why)

- `networkx` — for network analysis, not forecasting
- `prophet` (package, not skill) — already tested 2026-04-13, mediocre (58.6% MAPE)
- `literature-review` / `scholar-evaluation` / `scientific-writing` — for thesis writing phase, not ML
- `apa-citation` / `pyzotero` / `notebooklm` — citation/bibliography, out of ML scope
- `academic-paper` / `academic-pipeline` / `deep-research` — full academic writing pipeline, used later for Ch. 4

## Workflow skills (run in parallel during/after)

- `update_plan` — updates `outcome_files/` after each completed step
- `log_standup` — auto-log to standup draft at session end
- `draft_commit` — when Enrico wants to commit
- `update_all_docs` — sync all docs at end of pipeline
- `test-codebase-integrity` — verify nothing broke System A before commit

---

## Operational decisions still pending

1. **Package manager**: `pip install` global (fast, dirty) vs install `uv` and use `uv.lock` (clean, +5 min setup)
2. **Missing packages**: install all 3 (aeon + pymc + polars, ~600 MB) or skip aeon/pymc?
3. **Honest expectation on aeon DL**: 35 obs/brand → likely overfits → will NOT beat LightGBM. Run anyway for thesis completeness?

Awaiting Enrico's answer on these 3 before writing any Python file.
