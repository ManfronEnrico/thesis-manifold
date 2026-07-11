# Step 01 — Ingestion report
_Generated 2026-04-16T19:04:35_

## Baseline feature matrix (frozen input)
- Source: `results/phase1/feature_matrix.parquet`
- Target: `data/raw/feature_matrix_baseline.parquet`
- Size: 0.40 MB  (3,234 rows × 22 cols)
- SHA256: `30e262b9a5b731978593c98ef99988d83139e926c5ebed1f1edc81bc71434dd8`

## Nielsen raw tables
| Table | Rows | Cols | Size (MB) | SHA256 (prefix) |
|---|---:|---:|---:|:---|
| csd_clean_facts_v | 2,535,464 | 10 | 83.20 | `29fd11118d360c74…` |
| csd_clean_dim_product | 49,287 | 30 | 3.92 | `89cc257120233d14…` |
| csd_clean_dim_market | 587 | 13 | 0.05 | `4c11eaa481a3b478…` |
| csd_clean_dim_period | 152 | 16 | 0.02 | `e1386758c2fe8b17…` |

## Indeks Danmark
| File | Rows | Cols | CSV (MB) | Parquet (MB) | Ratio | SHA256 (prefix) |
|---|---:|---:|---:|---:|---:|:---|
| indeks_data | 20,134 | 6364 | 266.2 | 69.7 | 3.8x | `ad9d98fa276f3c38…` |
| indeks_metadata | 29,185 | 3 | 1.1 | 0.1 | 10.7x | `09e29b069fadd3aa…` |
| indeks_codebook | 6,364 | 11 | 1.9 | 0.3 | 6.0x | `10cf0e570386fb02…` |

## Design decisions

- Baseline FM is the frozen input for modelling. Raw Nielsen is snapshotted for audit + future FE.
- Nielsen re-aggregation deliberately NOT performed (would risk drift from baseline numbers).
- Indeks converted to Parquet via `polars` for 5–10× read speedup downstream.
- All artefacts idempotent: re-running overwrites safely.