---
name: Quality Audit Action Items
date: 2026-04-18
timestamp: 2026-04-18T17:00:00Z
priority: CRITICAL (blocks thesis reproducibility)
---

# Action Items: Notebook Quality Audit Follow-Up

**Session**: 2026-04-18 Notebook Audit  
**Key Finding**: Code is real (not hallucinations), but data pipeline is incomplete  
**Blocker**: `feature_matrix.parquet` missing → SRQ1/2/3 cannot run

---

## Critical Path (Blocks Thesis Defense)

### ⚠️ CRITICAL: Restore `feature_matrix.parquet`

**Status**: ❌ NOT FOUND (git-ignored)  
**Why it matters**: SRQ1, SRQ2, SRQ3 notebooks depend on this  
**Action**:

Choose ONE:

**Option A** (fastest):
```
Contact Enrico → ask for feature_matrix.parquet backup
```

**Option B** (self-serve):
```
1. Locate raw Nielsen CSV files (if archived)
2. Run datasets/combined_scripts/preprocessing.py
3. Should generate results/phase1/feature_matrix.parquet
4. Time: ~30–60 minutes
```

**Option C** (fallback):
```
Recover from backup system (OneDrive, local drive, archive)
```

**Deadline**: Before next SRQ1/2/3 analysis run  
**Owner**: Brian (decide which option) + Enrico (if Option A)

---

### ✅ Update `.gitignore` to Track Analysis Checkpoints

**Status**: ⏳ DECISION PENDING  
**Change**: Allow tracking of `results/phase1/*.parquet` (analysis checkpoint)

**Action**:
```bash
# 1. Edit .gitignore line 19
# FROM: *.parquet
# TO:   *.parquet
#       !results/phase1/*.parquet

# 2. Stage and commit the feature_matrix.parquet file
git add results/phase1/feature_matrix.parquet
git commit -m "feat: track feature_matrix.parquet checkpoint for SRQ1/2/3 reproducibility

This parquet file is the final feature engineering output that SRQ1/2/3 depend on.
Tracking it ensures reproducibility across machines and prevents unnecessary
preprocessing recomputation. Raw data remains git-ignored per compliance."
```

**Rationale**: See `docs/GITIGNORE_STRATEGY_2026-04-18.md`  
**Owner**: Brian (approval) + Claude (implementation)  
**Timeline**: Same session as restoring feature_matrix.parquet

---

### ✅ Validate SRQ1 Notebook End-to-End

**Status**: ❌ BLOCKED (waiting for feature_matrix.parquet)  
**What to check**:
- [ ] Notebook runs without errors
- [ ] `outputs/final_comparison.csv` matches expected metrics (LightGBM test MAPE = 27.67%)
- [ ] All figures generate correctly
- [ ] SHAP explanations produce output

**Action**:
```bash
cd docs/thesis/analysis
jupyter notebook thesis_notebook.ipynb
# Run all cells
# Verify outputs/final_comparison.csv
```

**Expected output**:
```
Model             Test MAPE    Comment
SeasonalNaive     49.92%       Baseline
Ridge             77.43%       Overfits
LightGBM_global   27.67%       ← Best
XGBoost_global    27.04%       Close 2nd
```

**Owner**: Brian  
**Timeline**: Day 1 after restoring feature_matrix.parquet

---

### ✅ Validate SRQ3 Indeks Integration

**Status**: ⏳ DATA AVAILABLE, INTEGRATION PENDING  
**What to do**:
1. Update agentic notebook System C with real Indeks demographic computation
2. Replace hardcoded region stats with actual computation from Indeks CSV
3. Re-run 3-way A/B/C ablation (20 queries)
4. Verify metrics match commit message expectations

**Action steps**:
```
1. Load indeksdanmark_data.csv
2. Aggregate by postal code region (7 regions)
3. Compute: mean_age, pct_male, n_respondents per region
4. Update notebook cell 12 (System C context provider)
5. Run cell 13 (3-way ablation)
6. Check outputs_agentic/abc_summary.csv for System C metrics:
   - mean_indeks_mentions: 9.9 (verify)
   - mean_word_count: 241.3
   - mean_latency_s: 13.0
```

**Files involved**:
- `datasets/data_spss_indeksdanmark/.csv/indeksdanmark_data.csv` ← SOURCE
- `docs/thesis/analysis/thesis_agentic_notebook.ipynb` ← UPDATE
- `docs/thesis/analysis/outputs_agentic/abc_summary.csv` ← VERIFY

**Owner**: Brian + Claude (implementation detail)  
**Timeline**: Day 2 after SRQ1 validation  
**Blocking issue**: May need postal code → region mapping defined

---

## Documentation & Cleanup

### ✅ Add README to `results/phase1/`

**Purpose**: Explain what `feature_matrix.parquet` is and when to regenerate

**File**: `results/phase1/README.md`

**Content** (template):
```markdown
# Feature Matrix Checkpoint

## What is this?

`feature_matrix.parquet` is the final feature engineering output for SRQ1/2/3.

Columns: [list key features]
Rows: 20,134 (respondents × months in forecast period)
Size: ~100 MB

## Source Data

- Nielsen: CSD raw data (dim_period, dim_market, dim_product, facts_v)
- Indeks: Consumer survey demographics (postal code → regions)

## When to Regenerate

Run `datasets/combined_scripts/preprocessing.py` if:
- Feature engineering logic changed
- New/updated source data available
- Output doesn't match expected shape

## When to Use Tracked Version

(Default) Running SRQ1/2/3 notebooks
- No action needed; notebook will load this file

## Preprocessing Steps

[Link to preprocessing.py with step-by-step explanation]
```

**Owner**: Brian (write with Enrico's input)  
**Timeline**: After SRQ1 validation

---

### ✅ Document Indeks Integration

**Purpose**: Record how System C was implemented with real demographic data

**File**: `docs/INDEKS_INTEGRATION_SUMMARY.md` (create after Phase 1-3 complete)

**Content**: 
- Data source and extraction logic
- Postal code → region mapping used
- Regional demographic statistics computed
- Results: A/B/C comparison metrics

**Owner**: Brian + Claude  
**Timeline**: After SRQ3 validation

---

## Optional (Nice to Have)

### Create Data Pipeline Diagram

**Purpose**: Visual reference for preprocessing → SRQ1/2/3 flow

**File**: `docs/data_pipeline_diagram.md` or `.png`

**Shows**:
```
Nielsen Raw CSV
    ↓ [preprocessing.py]
    ↓
Feature Matrix Parquet (tracked in git)
    ↓ [SRQ1: thesis_notebook.ipynb]
    ↓
Model metrics + SHAP figures
    ↓ [SRQ2/3: thesis_agentic_notebook.ipynb]
    ↓
A/B/C ablation results
```

**Owner**: Claude (can generate)  
**Timeline**: After all validations complete

---

## Summary Table

| Task | Blocker? | Owner | Status | Deadline |
|------|----------|-------|--------|----------|
| Restore feature_matrix.parquet | ✅ YES | Brian + Enrico | ⏳ PENDING | Before next analysis |
| Update .gitignore | ✅ YES | Brian (approve) | ⏳ PENDING | Same session |
| Validate SRQ1 | ✅ YES | Brian | ⏳ BLOCKED | Day 1 post-restore |
| Validate SRQ3 Indeks | ⚠️ SRQ1 done | Brian + Claude | ⏳ BLOCKED | Day 2 |
| Add results/phase1/README | ❌ NO | Brian | ⏳ TODO | Day 3 |
| Document Indeks integration | ❌ NO | Brian + Claude | ⏳ TODO | Day 4 |
| Data pipeline diagram | ❌ NO | Claude | ⏳ TODO | Day 5 |

---

## Quick Reference: What Was Verified

✅ **Code quality**: All real (no hallucinations)
✅ **Model training**: Legitimate (LightGBM, XGBoost, agents)
✅ **Output files**: Exist and match commit messages
✅ **Indeks data**: Now available (ready for integration)

❌ **Source data**: Missing (feature_matrix.parquet)
⚠️ **Reproducibility**: Blocked (waiting for source data)

---

## Next Steps (for Brian)

1. **Decide**: How to restore feature_matrix.parquet (A/B/C)?
2. **Approve**: .gitignore strategy?
3. **Schedule**: When to run validations?

**Then escalate to**: Claude Code with decision → implementation will follow.
