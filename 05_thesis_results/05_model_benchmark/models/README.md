# Served forecasting models

**The model files in this directory are not in git. Regenerate them.**

```powershell
python 03_thesis_modelling/model_training/train_and_persist.py
```

Takes ~30 seconds and writes all four categories.

## What is tracked and what is not

| file | tracked | why |
|------|---------|-----|
| `{cat}_metadata.json` | **yes** | small, diffable provenance: which model was served, its features, train boundary, `q90_log` |
| `index.json` | **yes** | maps each category to its model file |
| `{cat}_model.json` (XGBoost) | no | regenerable |
| `{cat}_model.joblib` (LightGBM / Ridge) | no | regenerable, and an opaque binary |

Together the model files are ~24 MB, and git rewrites them wholesale on every
re-persist because they are binaries. A re-persist happens whenever tuning or
selection changes, so tracking them would grow history by ~24 MB each time for
artefacts that a free 30-second command reproduces exactly. The same reasoning
keeps `thesis_full.docx` out of the repo.

The metadata stays tracked because it is the provenance the thesis relies on —
it records *which* model was served for a category and under what conditions,
which is a claim that needs history. The weights themselves are a derived
product of `cv_params.json` plus the feature matrices, both of which are tracked.

## If serving raises FileNotFoundError

`forecast_tool.py` already tells you what to do:

```
No persisted model for {category}. Run model_training/train_and_persist.py first.
```

That is the expected state of a fresh clone, not a fault.

## Reproducibility

Training is seeded (`SEED = 42`), so a regenerated model is identical to the one
that produced the recorded results, provided `cv_params.json` and the feature
matrices are unchanged. Both are tracked, so the regeneration is deterministic.

Hyperparameters come from `04_thesis_results/srq1/cv_params.json`
(100 trials, 4-fold expanding-window CV). Model *selection* per category comes
from `cv_metrics.csv`, ranked on `cv_score` — never on `test_wmape`, which would
be selection on the held-out set (see P0044 F29).
