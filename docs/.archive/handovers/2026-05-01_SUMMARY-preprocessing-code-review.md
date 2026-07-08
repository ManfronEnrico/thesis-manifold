# Summary: Preprocessing Code Review (2026-05-01)

**Status**: Code review complete. Handover prepared for Enrico. Awaiting responses on design rationale.

---

## What Was Done

1. **Line-by-line code review** of `engineer_features.py` (actual Python implementation, not docstrings/comments)
2. **Verified**: No data leakage, deterministic feature engineering, robust implementation
3. **Identified**: 7 design choices lacking documented justification
4. **Created**: Detailed handover document for Enrico with specific code references + answerable questions
5. **Updated**: P0017 plan with correct folder structure

---

## Key Findings

### ✅ Technical Implementation (Sound)
- No data leakage in feature engineering (lags use shift, rolling uses shift(1), calendar/promo/log are deterministic)
- Robust error handling (CSV validation, market existence check)
- Pure functions, deterministic, reproducible

### ❌ Design Choices (Need Justification)
1. **Lag selection (1,2,3,4,8,13)** — ACF analysis? Domain knowledge? Arbitrary?
2. **Rolling windows (4,13)** — Why these? Why rolling_std only for w=4?
3. **Holiday months {1,4,6,10,12}** — Why exclude Jul–Aug (summer peak)?
4. **min_periods=30** — Data-driven or rule of thumb?
5. **Train/val/test split (2025-02, 2025-08)** — Do all categories have 2019–2025 data?
6. **Promo intensity denominator** — Clipped to lower=1; intentional or bug?
7. **Feature schema per category** — Do all have sales_units_any_promo?

---

## Folder Structure (Corrected)

**Output folders should match notebook folder names**:

```
parquet_nielsen/
  specialized_CSD/
    specialized_CSD_feature_matrix.parquet
    series_index.csv
    split_dates.json
    preprocessing_report.md
  specialized_danskvand/
    specialized_danskvand_feature_matrix.parquet
    series_index.csv
    split_dates.json
    preprocessing_report.md
  specialized_energidrikke/
    ...
  specialized_rtd/
    ...
  specialized_totalbeer/
    ...
```

---

## Next Steps

**Blocked Until Enrico Responds**:
- Answer the 7 questions in the handover document
- Provide rationale for each design choice
- Clarify any per-category variations needed

**Once Cleared** (future session):
1. Restructure parquet_nielsen/ folders
2. Update preprocessing_csd.py to write to per-category subfolders
3. Create preprocessing scripts for remaining categories
4. Test all 5 scripts end-to-end

---

## Documents Created

1. **`docs/handovers/2026-05-01_HANDOVER-enrico-preprocessing-code-review.md`**
   - Detailed code review with line references
   - 7 specific questions requiring answers
   - Action items per priority
   - Ready to send to Enrico

2. **P0017 Plan Updated**
   - Phase 2B: Preprocessing refactoring documented
   - Correct folder structure specified
   - Blocking items clearly marked
   - Next steps outlined

---

## Summary

**Code is technically sound, but design rationale is undocumented.** 
The handover provides a structured list of questions for Enrico to address before scaling to other categories.
