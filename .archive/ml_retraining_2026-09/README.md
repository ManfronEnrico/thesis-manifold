# `ml_retraining/` — archived 2026-09-06

An 11-step April-2026 pipeline (`00_setup.py` .. `10_publication_figures.py`),
superseded by `01_SRQ1_Model_Training/`.

## Why archived rather than repointed at PATHS.py

Every script sets `PROJECT_ROOT = Path(__file__).resolve().parents[2]` and then
reads/writes paths that do not exist in this repo and have not for months:

- `PROJECT_ROOT / "results" / "phase1" / "feature_matrix.parquet"`
- `PROJECT_ROOT / "data" / "raw"`, `data/clean`, `data/features`
- `PROJECT_ROOT / "Thesis" / "indeksdanmark"` — the `Thesis/` folder segment was
  removed by the P0028 restructure on 2026-07-11

There is no live directory for these to point at. Repointing them through
`PATHS.py` would produce constants for folders nobody maintains, which is the
failure mode P0046 exists to remove — the same reason the
`THESIS_MODELLING_SERVING_*` constants were deleted rather than repointed.

It also ingested the Indeks Danmark dataset, dropped on 2026-09-06
(see `.archive/spss_indeksdanmark_2026-09/`).

Recoverable from git history if a step is ever needed again.
