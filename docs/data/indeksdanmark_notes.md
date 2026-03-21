# Indeks Danmark Dataset Notes
> Source: Thesis/indeksdanmark_data_model-1.md
> Last updated: 2026-03-14

---

## Dataset Overview

| File | Rows | Columns | Description |
|---|---|---|---|
| `indeksdanmark_data.csv` | 20,134 | 6,364 | Main survey data (all respondents) |
| `official_codebook.csv` | 6,364 | 11 | Variable documentation + survey weights |
| `indeksdanmark.metadata.csv` | 29,185 | 3 | Value label mappings (numeric → readable) |

**Data type**: All variables in main dataset are float64.

---

## File Details

### indeksdanmark_data.csv
- 20,134 respondents × 6,364 variables
- Contains demographic, behavioral, attitudinal, and preference variables
- All survey sections covered

### official_codebook.csv (6,364 rows × 11 cols)
- One row per variable in the main dataset
- Includes **survey weight column** — required for weighted analysis
- Use for population-representative results

### indeksdanmark.metadata.csv (29,185 rows × 3 cols)
- Columns: `Variable`, `Value`, `Label`
- Maps numeric codes to human-readable labels
- Example: `STEMT_HH23` value `1.0` → "A: the Danish Social Democrats"
- Essential for interpreting categorical variables

---

## Access Status

⚠️ The 3 CSV files are currently stored as `.webloc` shortcuts pointing to Google Drive — they are NOT yet downloaded locally.

**Action required**: Download the 3 CSVs from Google Drive and place them in `Thesis/` or a `data/` subfolder to satisfy the "no data outside local environment" rule.

---

## Data Security Note

- Indeks Danmark contains consumer survey data with personal/behavioral attributes
- Must remain local — no external uploads
- Survey weights must be applied for population-representative analysis (see codebook)

---

## Preliminary Assessment

- **Size estimate**: 20,134 × 6,364 float64 ≈ ~970 MB in memory → fits within 8GB constraint
- **Usability**: Wide format (many variables) — feature selection/dimensionality reduction likely needed
- **Linkage to Nielsen**: No direct key — linkage would be via demographic/behavioral segments, not row-level join
