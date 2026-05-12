# Stage 1 — JSONL → Parquet Cache

This folder owns the conversion of raw Nielsen JSONL files into Parquet.
It is **Stage 1** of a two-stage preprocessing pipeline.

```
Stage 1 (this folder)              Stage 2 (../preprocessing_*.py)
───────────────────                ───────────────────────────────
JSONL  ─────────────► Parquet ─────────────► Engineered features
(raw_nielsen/                  (parquet_nielsen/                (parquet_nielsen/
 data_jsonl/<cat>/              <cat>/views/                     <cat>/engineered/
 {views,metadata}/)             <cat>/metadata/)                  *.parquet)
```

## Why split into two stages?

- **JSONL is slow.** Pandas reads JSONL line-by-line; Parquet is columnar, compressed, ~5–10× faster, and lower memory.
- **Re-running feature engineering is cheap once Parquet exists.** Stage 2 reads Parquet only — iterating on feature logic does not re-pay the JSONL parse cost.
- **Bottleneck isolation.** Stage 1 is purely I/O; Stage 2 is computation. They have different failure modes (disk vs RAM) and different cadences (Stage 1 only re-runs when the upstream Fabric warehouse is re-downloaded).

## Files

| File | Purpose |
|---|---|
| `convert_category.py` | Convert a single category (parametric `--category`). |
| `run_all_conversions.py` | Loop over all 5 categories. |
| `__init__.py` | Package marker. |

## Usage

Run from the project root.

```bash
# Convert one category
python thesis/data/preprocessing/jsonl_to_parquet/convert_category.py --category CSD

# Convert all 5 categories (idempotent — skips up-to-date files)
python thesis/data/preprocessing/jsonl_to_parquet/run_all_conversions.py

# Force re-convert (ignore mtime check)
python thesis/data/preprocessing/jsonl_to_parquet/run_all_conversions.py --force

# Restrict to a subset
python thesis/data/preprocessing/jsonl_to_parquet/run_all_conversions.py --only CSD Energidrikke
```

## Idempotence

For each JSONL file, the destination Parquet is rewritten **only if missing or older than the source**. Re-running on an unchanged dataset is fast (mtime check only).

`--force` overrides this and re-converts every file.

## Output layout

```
thesis/data/preprocessing/parquet_nielsen/
  CSD/
    views/
      csd_clean_facts_v.parquet
      csd_clean_dim_product_v.parquet
      csd_clean_dim_period_v.parquet
      csd_clean_dim_market_v.parquet
    metadata/
      metadata_csd_clean_facts.parquet
      metadata_csd_clean_dim_product.parquet
      metadata_csd_clean_dim_period.parquet
      metadata_csd_clean_dim_market.parquet
      metadata_csd_columns.parquet
  Energidrikke/
    views/
      energidrikke_clean_facts_v.parquet
      ... (same pattern)
    metadata/
      metadata_energidrikke_columns.parquet
  Danskvand/  …
  RTD/        …
  Totalbeer/  …
```

Note: only **CSD** ships with per-table metadata files (5 files). The other four categories ship a single `metadata_<cat>_columns.jsonl`. The conversion script auto-discovers files via glob.

There is no `raw/` subfolder — Nielsen does not export raw tables as JSONL, only views.

## Manifest

`run_all_conversions.py` writes `thesis/data/preprocessing/jsonl_to_parquet_manifest.json` with per-category file counts and elapsed time, so Stage 2 (or downstream tooling) can assert that Stage 1 completed before running.

## Stage 2 dependency

The `preprocessing_*.py` scripts in the parent folder **read only Parquet**, not JSONL. If the Parquet cache is missing they hard-fail with instructions to run this folder's scripts first. There is intentionally no JSONL fallback in Stage 2.
