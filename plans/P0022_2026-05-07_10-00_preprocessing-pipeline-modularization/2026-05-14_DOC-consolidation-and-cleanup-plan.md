# Plan: CSD EDA Script Consolidation + P0022 Doc Cleanup

**Date:** 2026-05-14  
**Purpose:** Consolidate 3 near-duplicate EDA scripts into 1 canonical version; reorganize 6 planning docs into 1 reference doc + archive

---

## Executive Summary

**Problem:**
- 3 similar EDA scripts exist for CSD (superseding each other in sophistication)
- 6 planning docs with overlapping content in P0022 folder
- Latent bug in the best script (`log_necessary` NameError when statsmodels unavailable)

**Solution:**
- Adopt `pre_csd_eda_enhanced_with_visualizations_expanded.py` (most complete: 10 cells, 8 visualizations) as canonical
- Fix 1-line bug, rename to `pre_csd_eda.py`, delete other 2 scripts
- Create 1 condensed rationale doc from 2 substantive planning docs; archive all 6 originals
- Update P0022 frontmatter to Phase 5 Ready

**Outcome:**
- CSD folder: 1 canonical EDA script (clean, tested, template-ready for Phase 5)
- Plan folder: 1 active reference doc + 1 archive folder preserving originals
- Ready to replicate for Energidrikke, Danskvand, RTD (Phase 5)

---

## Script Analysis & Consolidation

### Comparison Table

| Script | Lines | Cells | Visualizations | Status |
|--------|-------|-------|----------------|--------|
| `pre_csd_eda_and_parameter_analysis.py` | 465 | 8 | 0 | **DELETE** — original, no visualizations |
| `pre_csd_eda_enhanced_with_visualizations.py` | ~770 | 9 | ~4–5 PNG | **DELETE** — intermediate version |
| `pre_csd_eda_enhanced_with_visualizations_expanded.py` | 976 | 10 | 8 PNG | **KEEP & RENAME** — canonical |

### Why `_expanded` is Canonical

The `_expanded` script includes every cell and visualization from both earlier versions, PLUS 4 additional analyses:
- **Cell 1.5:** Distribution histograms with skewness (GeeksforGeeks style)
- **Cell 4.5:** Monthly sales bar chart (highlights holiday months)
- **Cell 5:** Top 5 brands time series (individual brand trajectories)
- **Cell 8:** Promo intensity analysis (effectiveness visualization)

All original cells from both earlier scripts are present (with shifted numbering).

### Known Bug

**Location:** `pre_csd_eda_enhanced_with_visualizations_expanded.py`

**Issue:** `log_necessary` variable is defined inside the `if HAS_STATSMODELS:` block (lines ~372–383) but referenced unconditionally at:
- Line 712: `"LOG_TRANSFORM_NECESSARY": log_necessary if log_necessary is not None else "Requires stationarity test"`
- Line 934: Summary table references `log_necessary`

**Impact:** If `statsmodels` is not installed, `NameError: name 'log_necessary' is not defined`

**Fix:** Add `log_necessary = None` before the `if HAS_STATSMODELS:` block as a default value.

---

## Documentation Analysis & Organization

### Current State (6 Docs)

| Document | Lines | Purpose | Redundancy |
|----------|-------|---------|-----------|
| `2026-05-14_DOC-feature-engineering-eda-analysis-and-insights.md` | ~423 | Identify suspect patterns, what's validated vs. missing | Content reused in rationale |
| `2026-05-14_DOC-rossmann-vs-csd-eda-comparison.md` | ~374 | Feature-by-feature comparison, code snippets, priority matrix | Content reused in rationale |
| `2026-05-14_DOC-supporting-docs-index.md` | ~284 | Navigation hub (points to other 5 docs) | **Obsolete after consolidation** |
| `2026-05-14_DOC-vps-ready-eda-code-reference-comprehensive.md` | ~970 | Cell-by-cell breakdown of the `_expanded` script | **Redundant with actual script** |
| `2026-05-14_DOC-vps-ready-eda-code-reference.md` | ~393 | Reference for `_enhanced` script (non-expanded) | **References old script** |
| `2026-05-14_DOC-vps-session-checklist.md` | ~402 | VPS execution guide with setup, analysis, decision points | **Operational knowledge, not reference** |

**Key insight:** 2 docs contain substantive analysis (docs 1–2); 4 docs are operational or redundant (docs 3–6).

### Target State (1 Active Doc + Archive)

**Active folder root:**
- P0022 plan file
- `2026-05-14_DOC-eda-design-rationale.md` (new, consolidated)

**Archive folder** (preserved for reference):
- All 6 original docs (searchable, detailed backup)

---

## Implementation Steps

### Step 1 — Fix Bug in `_expanded` Script

**File:** `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_enhanced_with_visualizations_expanded.py`

**Action:** Add line after Cell 2 date analysis (around line 315, just before the `if HAS_STATSMODELS:` block for Cell 2.5):

```python
log_necessary = None  # Default; overwritten by ADF test if statsmodels available
```

**Verification:** After fix, `log_necessary` is always defined before reference in Cell 10.

---

### Step 2 — Rename to Canonical Name

```bash
cd /root/dev/thesis-manifold/thesis/data/preprocessing/nielsen/CSD

mv pre_csd_eda_enhanced_with_visualizations_expanded.py pre_csd_eda.py
```

**Update docstring in renamed file:**
- Change title from "Comprehensive Enhanced EDA with Full Visualization Suite" → "CSD EDA & Parameter Analysis"
- Update PURPOSE section to indicate: "Canonical EDA script for CSD Nielsen preprocessing. Generates all parameters (MIN_PERIODS, LAGS, ROLLING_WINDOWS, HOLIDAY_MONTHS, TRAIN_END, VAL_END) via empirical analysis. Serves as template for Phase 5 (Energidrikke, Danskvand, RTD)."

---

### Step 3 — Delete Superseded Scripts

```bash
rm pre_csd_eda_and_parameter_analysis.py
rm pre_csd_eda_enhanced_with_visualizations.py
```

**Verification:** `ls pre_csd_*.py` should return only `pre_csd_eda.py`

---

### Step 4 — Create Consolidated Reference Doc

**File to create:** `plans/03-focus_plans/P0022_2026-05-07_1000_PLAN-preprocessing-pipeline-modularization/2026-05-14_DOC-eda-design-rationale.md`

**Structure:**

```markdown
# CSD EDA Design Rationale & Visualization Reference

## Parameter Decisions & Evidence

| Parameter | Value | Validation Method | Confidence | Location |
|-----------|-------|-------------------|------------|----------|
| MIN_PERIODS | 40 | Cell 3: 62 brands ≥40 periods (43.4% quality focus) | High | `pre_csd_eda.py` Cell 3 |
| LAGS | [1,2,3,4,8,13] | Cell 5.5: ACF/PACF significance (top 5 brands) | High | `pre_csd_eda.py` Cell 5.5 |
| ROLLING_WINDOWS | [4, 13] | Cell 6: Nielsen 4-4-5 calendar alignment + quarterly | High | `pre_csd_eda.py` Cell 6 |
| HOLIDAY_MONTHS | {3,6,12} | Cell 4.6: Seasonal decomposition peaks | High | `pre_csd_eda.py` Cell 4.6 |
| LOG_TRANSFORM | Yes | Cell 2.5: ADF stationarity test | High | `pre_csd_eda.py` Cell 2.5 |
| TRAIN_END | (2024, 10) | Cell 7: 24m train (2 years for pattern stability) | High | `pre_csd_eda.py` Cell 7 |
| VAL_END | (2025, 04) | Cell 7: 6m validation window | High | `pre_csd_eda.py` Cell 7 |

## What Each Visualization Confirms

| Plot | File | Purpose | Validates |
|------|------|---------|-----------|
| Distribution Histograms | Cell 1.5 | Feature skewness | Right-skewed sales_units → log transform justified |
| ECDF Distributions | Cell 1.6 | Cumulative distribution shape | Sales distribution pattern (confirms skew) |
| Monthly Sales Bar Chart | Cell 4.5 | Seasonal peak visualization | Holiday months {3,6,12} are actual peaks (>75th percentile) |
| Seasonal Decomposition | Cell 4.6 | Trend + seasonal + residual | Confirms {3,6,12} are TRUE seasonal component peaks |
| Top Brands Time Series | Cell 5 | Individual brand trajectories | High-volume brands exhibit expected temporal patterns |
| ACF/PACF Plots | Cell 5.6 | Lag autocorrelation structure | Lags {1,2,3,4,8,13} are statistically significant |
| Promo Intensity Analysis | Cell 8 | Promo effectiveness | Promotions correlate with sales (business validation) |
| Correlation Heatmap | Cell 9 | Metric relationships | Metric interdependencies (promo↔sales, distribution↔sales) |

## Suspect Patterns Addressed (from Rossmann Analysis)

| Issue | Previous State | Current State | Resolution |
|-------|---|---|---|
| Hard-coded lag windows | Assumed {1,2,3,4,8,13} | ACF/PACF validates significance | Cell 5.6 confirms each lag is statistically significant |
| Holiday months guessed | Assumed {3,6,12} | Seasonal decomposition confirms | Cell 4.6 shows peaks in true seasonal component |
| Log transform unchecked | Applied blindly | ADF test validates necessity | Cell 2.5 confirms non-stationarity → log needed |
| Rolling window min_periods loose | max(2, w//4) | Validated via coverage | Cell 4 ensures sufficient data density |
| Promo intensity noisy | Divide + clip | Analyzed for distribution shape | Cell 8 shows promo effect on sales |

## Phase 5 Template Instructions (Energidrikke, Danskvand, RTD)

For each category, replicate `pre_csd_eda.py`:

1. **Create copy:** `pre_energidrikke_eda.py`, `pre_danskvand_eda.py`, `pre_rtd_eda.py`
2. **Change CATEGORY variable** (line ~86): `CATEGORY = "Energidrikke"` (etc.)
3. **Run the script** to extract category-specific parameters
4. **Extract findings** from JSON output (findings.json)
5. **Use extracted parameters** to update Step 4 feature engineering scripts

Expected outputs:
- JSON findings with parameters specific to each category
- 8 PNG visualizations validating each category's parameters
- Console summary tables showing parameter choices

---

## Archive Organization

All original docs moved to `archive/` subfolder within P0022 plan folder:

```
plans/03-focus_plans/P0022_.../
├── P0022_2026-05-07_1000_PLAN-...md (main plan)
├── 2026-05-14_DOC-eda-design-rationale.md (new, consolidated)
└── archive/
    ├── 2026-05-14_DOC-feature-engineering-eda-analysis-and-insights.md
    ├── 2026-05-14_DOC-rossmann-vs-csd-eda-comparison.md
    ├── 2026-05-14_DOC-supporting-docs-index.md
    ├── 2026-05-14_DOC-vps-ready-eda-code-reference-comprehensive.md
    ├── 2026-05-14_DOC-vps-ready-eda-code-reference.md
    └── 2026-05-14_DOC-vps-session-checklist.md
```

**Rationale:** Archive preserves full analysis detail (cross-referencing, code snippets, detailed implementation notes) while keeping active folder clean and focused.

---

## Files Modified Summary

| File | Action | Notes |
|------|--------|-------|
| `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_enhanced_with_visualizations_expanded.py` | Fix bug (add `log_necessary = None`) + rename to `pre_csd_eda.py` | 1-line fix; update docstring |
| `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py` | **DELETE** | Original, no visualizations |
| `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_enhanced_with_visualizations.py` | **DELETE** | Intermediate, superseded |
| `plans/.../2026-05-14_DOC-supporting-docs-index.md` | **MOVE → archive/** | Navigation hub (obsolete) |
| `plans/.../2026-05-14_DOC-vps-ready-eda-code-reference-comprehensive.md` | **MOVE → archive/** | Redundant with script |
| `plans/.../2026-05-14_DOC-vps-ready-eda-code-reference.md` | **MOVE → archive/** | References old script |
| `plans/.../2026-05-14_DOC-vps-session-checklist.md` | **MOVE → archive/** | Operational knowledge |
| `plans/.../2026-05-14_DOC-feature-engineering-eda-analysis-and-insights.md` | **MOVE → archive/** | Content merged into rationale |
| `plans/.../2026-05-14_DOC-rossmann-vs-csd-eda-comparison.md` | **MOVE → archive/** | Content merged into rationale |
| `plans/.../2026-05-14_DOC-eda-design-rationale.md` | **CREATE** | Consolidated reference (new) |
| `plans/.../P0022_2026-05-07_1000_PLAN-...md` | **UPDATE frontmatter** | `status: Phase 5 Ready (...)` |

---

## Verification Checklist

- [ ] Bug fix applied: `log_necessary = None` added before Cell 2.5 block
- [ ] Script renamed: `pre_csd_eda.py` exists, `_expanded` version deleted
- [ ] Superseded scripts deleted: `pre_csd_eda_and_parameter_analysis.py` and `_enhanced` version removed
- [ ] Consolidated doc created: `2026-05-14_DOC-eda-design-rationale.md` exists in plan folder root
- [ ] Archive folder created: `archive/` subfolder exists with all 6 original docs
- [ ] Plan frontmatter updated: `status` field reflects "Phase 5 Ready"
- [ ] Script test pass: `python pre_csd_eda.py` runs without errors (with/without statsmodels)

---

**Status:** Ready for implementation  
**Estimated time:** 30 minutes (script fix + doc consolidation + file moves)  
**Next Phase:** Phase 5 EDA Replication (Energidrikke, Danskvand, RTD using canonical template)
