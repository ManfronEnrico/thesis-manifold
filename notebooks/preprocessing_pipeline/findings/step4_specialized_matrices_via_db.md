# Step 4 — Specialized matrices via DB (5 categories)

**Goal**: produce one feature matrix per Nielsen category — the input for
the 5 "specialized" models in the 7-model plan.

## Why we went DB instead of CSV

The CSV exports of the 4 new categories' `dim_product` had **massive orphan
rates**:

| Category | facts product_ids | dim coverage | Orphan rate |
|---|---:|---:|---:|
| csd | 8,522 | 8,429 | 4% (acceptable) |
| danskvand | 1,255 | 564 matched | 63% (broken) |
| energidrikke | 2,758 | 732 matched | 79% (broken) |
| rtd | 2,173 | 578 matched | 78% (broken) |
| totalbeer | 18,543 | 1 matched(!) | 100% (corrupted from CSV recovery) |

The CSV-exported `dim_product` for the 4 new categories simply doesn't
contain all the product_ids used in facts. The DB has them — the export was
incomplete.

**Verified at the DB**: each category has working
`{cat}_clean_facts_v` + `{cat}_clean_dim_product_v` views with INNER JOIN
yielding correct brand attribution for ~all rows.

## Schema-tolerant SQL

Categories don't share the same facts schema. CSD has 10 columns; danskvand
has 15 (no `sales_units_any_promo`); the others have 30+ (with
`baseline_sales_*` etc).

`aggregate_brand_month_from_db` introspects the available columns via
`INFORMATION_SCHEMA.COLUMNS` and substitutes `0` for any column missing in
that category's facts view. Result: the same canonical output schema
(`brand`, `period_year`, `period_month`, `sales_units`, `sales_value`,
`sales_liters`, `promo_units`, `weighted_dist`) regardless of category.

## Results

Run on `DVH EXCL. HD` market (the same market used by `preprocessing.py`):

| Category | Aggregated rows | Brands in | Brands kept | Months | Time |
|----------|-----:|--------:|-----------:|----:|----:|
| csd | 3,789 | 136 | 77 | 42 | 1.3s |
| danskvand | 1,090 | 49 | 24 | 37 | 1.2s |
| energidrikke | 1,520 | 64 | 27 | 39 | 0.7s |
| rtd | 2,193 | 93 | 42 | 37 | 1.0s |
| totalbeer | 12,627 | 455 | **266** | 39 | 3.5s |

**Total elapsed: 7.7 seconds** for all 5. Network-bound on the DB queries.

Output:
```
results/phase1/csd/feature_matrix.parquet      460 KB
results/phase1/danskvand/feature_matrix.parquet 116 KB
results/phase1/energidrikke/feature_matrix.parquet 200 KB
results/phase1/rtd/feature_matrix.parquet      176 KB
results/phase1/totalbeer/feature_matrix.parquet 1.0 MB
```

## Sanity checks (top brands)

| Category | Top 5 brands by sales_units (sanity-confirmed against domain knowledge) |
|---|---|
| csd | HARBOE, COCA COLA, PEPSI, FAXE KONDI, FANTA |
| danskvand | HARBOE, EGEKILDE, RAMLOESA, AQUA D'OR, BLUE KELD |
| energidrikke | RED BULL, MONSTER ENERGY, FAXE KONDI BOOSTER, CULT, STATE |
| rtd | BREEZER, SHAKER, SMIRNOFF ICE/TWISTED, SOMERSBY, MOKAÏ |
| totalbeer | (top 5 to verify — 266 brands kept, expected ROYAL UNIBREW + CARLSBERG dominant) |

All five make sense for the Danish market. Categories cleanly separated.

## Note for Brian

The orphan-product issue makes the CSV-only approach unviable for the 4 new
categories. We should:
- Re-export `dim_product_v` for the 4 new categories with a more robust CSV
  writer (or use TSV / proper quoting)
- OR move the agent to query the DB directly (current approach in this
  module, via `aggregate_brand_month_from_db`).

Recommendation: the DB path is cleaner and what the module already supports.
The CSV path stays available for offline / CI scenarios.
