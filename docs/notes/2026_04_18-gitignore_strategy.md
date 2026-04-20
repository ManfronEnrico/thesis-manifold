---
title: Git-Ignore Strategy for Feature Matrix
type: note
status: active
created: 2026-04-18
---

# Git-Ignore Strategy: Should `feature_matrix.parquet` Be Tracked?

## The Problem

**Status quo**:
- `.gitignore` line 19 ignores ALL `*.parquet` files
- `feature_matrix.parquet` does NOT exist in the repo (git-ignored)
- SRQ1 and SRQ2/3 notebooks depend on this file to run
- Enrico generated outputs from it, but the input snapshot itself is lost

**Consequence**:
- Brian downloads the repo → missing data file
- Brian runs SRQ1 notebook → fails (no input data)
- Brian must regenerate `feature_matrix.parquet` from scratch
- Different machines may produce slightly different outputs (floating-point, RNG, library versions)

**Your question**: Should we git-ignore only *raw* data, but track *derived analysis checkpoints* like `feature_matrix.parquet`?

## Answer: YES

### Analysis: What Should Be Tracked vs. Ignored?

| File Type | Example | Should Track? | Reason |
|-----------|---------|---------------|--------|
| **Raw source data** | `datasets/indeksdanmark_data.csv` | ❌ NO | Large, source of truth is external, CSV version is definitive |
| **Raw parquet versions** | `datasets/data_raw_*.parquet` | ❌ NO | Regenerable from CSV; just a cache |
| **Preprocessing intermediate** | `results/preprocessing/tier_*.parquet` | ❌ NO | Intermediate step; can be regenerated |
| **Analysis checkpoint** | `results/phase1/feature_matrix.parquet` | ✅ YES | Exact input snapshot SRQ1/2/3 depend on; changed rarely; non-sensitive |
| **Analysis outputs** | `outputs/*.csv` | ✅ YES | Already tracked (exceptions in .gitignore) |
| **Model checkpoints** | `outputs/*.pkl` | ❌ NO | Regenerable from feature matrix + code |

### Why Track `feature_matrix.parquet`?

1. **Reproducibility**: Enrico ran notebooks with specific data snapshot. Tracking it preserves that state.

2. **Efficiency**: Brian doesn't wait 30+ minutes for preprocessing. Fixed feature_matrix version → instant SRQ1/2/3 runs.

3. **Consistency**: Floating-point aggregations and random seeds can vary across machines. Tracking ensures exact input.

4. **Low risk**: 
   - Size: ~50–150 MB (acceptable for GitHub)
   - Sensitivity: Aggregated features, not raw survey respondents
   - Frequency: Changed rarely (only when feature engineering is updated)

5. **Alignment**: Already tracking `outputs/*.csv` (metrics); treating the *input* the same way is consistent.

### Why NOT Track Raw Data?

1. **Size**: Raw Nielsen + Indeks can be gigabytes.
2. **Sensitivity**: Contains individual respondent records.
3. **External source**: Truth lives in the original CSV/database, not the parquet snapshot.
4. **Regeneration**: CSV → parquet is deterministic (pandas.read_csv + pd.to_parquet).

---

## Proposed `.gitignore` Update

**Current** (line 19):
```
*.parquet
```

**Proposed**:
```
*.parquet
!results/phase1/*.parquet      # Track analysis checkpoints (feature_matrix.parquet)
```

This creates an exception: all `.parquet` files are ignored *except* those in `results/phase1/`.

### Rationale

- ✅ Raw data in `datasets/` stays ignored (can regenerate from CSV)
- ✅ Intermediate preprocessing ignored (intermediate/*.parquet)
- ✅ Analysis checkpoint tracked (results/phase1/feature_matrix.parquet)
- ✅ Simple rule, easy to maintain

---

## Indeks Danmark Data: Now Available

**New files** (just downloaded):
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv` (20,134 respondents, 6,364 columns)
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_metadata.csv` (variable definitions)
- `datasets/data_spss_indeksdanmark/.csv/official_codebook.csv` (column reference)

**Key demographics in data**:
- `KOEN` (gender)
- `ALDER_ALL` (age group)
- `POST` (postal code / region)
- `ALDERB_*` (age bracket indicators for children)
- `ANTPERS`, `ANTVOKS`, `ANTBOERN` (household size info)
- Media and consumer behavior columns (6,300+ variables)

**Status for SRQ3**:
- System C (real Indeks demographic integration) now has actual source data
- Can validate that System C outputs match the agentic notebook metrics (9.9 Indeks mentions)

---

## Action Plan (Prioritized)

### Immediate (blockers for reproducibility)

1. **Restore or regenerate `feature_matrix.parquet`**
   - Option A: Find backup/archive of original file from Enrico
   - Option B: Locate raw Nielsen CSV files and run preprocessing script
   - Option C: Enrico sends you the file directly (fastest)

2. **Update `.gitignore` to track analysis checkpoints**
   ```bash
   # Edit .gitignore line 19
   *.parquet
   !results/phase1/*.parquet
   
   # Then add the file
   git add results/phase1/feature_matrix.parquet
   git commit -m "feat: track feature_matrix.parquet for SRQ1/2/3 reproducibility"
   ```

### Short-term (validation)

3. **Validate SRQ1 notebook reproducibility**
   - Run `docs/thesis/analysis/thesis_notebook.ipynb` end-to-end
   - Confirm outputs match `outputs/final_comparison.csv` metrics
   - Document any environment differences (library versions, OS)

4. **Validate SRQ3 Indeks integration**
   - Run `docs/thesis/analysis/thesis_agentic_notebook.ipynb` section 10 (System C)
   - Confirm outputs match `outputs_agentic/abc_summary.csv` (9.9 Indeks mentions)

### Documentation

5. **Add README to `results/phase1/`**
   ```markdown
   # Feature Matrix Checkpoint
   
   **File**: `feature_matrix.parquet`
   **Size**: ~100 MB
   **Created**: [date]
   **Source**: Nielsen + Indeks aggregated features
   
   ## To regenerate:
   - Run `datasets/combined_scripts/preprocessing.py`
   - Requires: raw Nielsen CSV + Indeks CSV
   - Time: ~30 minutes
   
   ## When to regenerate:
   - Feature engineering logic changed
   - New/updated source data available
   - Want to verify preprocessing output
   
   ## When to use tracked version:
   - Running SRQ1/2/3 notebooks (default)
   - Ensuring reproducibility across machines
   - Thesis evaluation (fixed inputs)
   ```

---

## Summary Table

| Question | Answer | Implication |
|----------|--------|-------------|
| Should `feature_matrix.parquet` be tracked? | ✅ YES | Unblock SRQ1/2/3 reproduction |
| Should raw data CSVs be tracked? | ❌ NO | Keep git-ignored; source is external |
| Update `.gitignore` line 19? | ✅ YES | Add exception for `!results/phase1/*.parquet` |
| Indeks data ready to use? | ✅ YES | Validate System C in SRQ3 |
| Preprocessing regeneration needed now? | ⚠️ TBD | Depends on if Enrico backup exists |

---

## Decision Required from Brian

1. **Do you have a backup of `feature_matrix.parquet` from Enrico?**
   - If YES → restore it, commit with .gitignore update
   - If NO → ask Enrico to send it, or regenerate from raw Nielsen data

2. **Approve `.gitignore` change?**
   - Accept proposal: `!results/phase1/*.parquet`
   - Alternative approach?

Once you decide, we'll implement the changes in the next session.
