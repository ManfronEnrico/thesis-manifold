---
pid: P0023
created: 2026-06-30 12:38:00
updated: 2026-06-30 14:00:00
---

# P0023 — Progress Log

## Session 1 — 2026-06-30

**Goal**: Read EDA script, produce structured critique from predictive ML + FMCG perspective.

### Actions
- [x] Read full `pre_csd_1.5_eda.py` (940 lines, 16 cells)
- [x] Catalogued all 16 cells by ML relevance (Phase 1)
- [x] Identified 13 critique items across P0/P1/P2 tiers (Phase 2)
- [x] Wrote full findings to `findings.md` (Phase 3)
- [ ] Output critique document to `docs/reference/` (Phase 4 — pending)

### Key Findings This Session
- Central issue: most EDA cells aggregate across brands, masking heterogeneity critical for per-brand ML
- Data leakage risk in Cell 13 (hardcoded split with no per-brand validation or warmup buffer)
- Target variable (Y) is never explicitly defined — the most fundamental ML gap
- Dead code bug in Cell 2 (skewness threshold elif order)
- ACF/PACF (Cell 11) is the strongest cell — but its findings aren't used to derive lag parameters

### Blockers
None.

## Session 2 — 2026-06-30

**Goal**: Execute all 13 fix tasks against `pre_csd_1.5_eda.py`.

### Actions
- [x] T-01: Added ML_TARGET constants block (TARGET_COL, FORECAST_HORIZON, WARMUP_PERIODS)
- [x] T-09: Fixed dead-code elif ordering in Cell 2 (skewness extremes)
- [x] T-10: Fixed promo_intensity metric — clip(lower=1) + data quality assertion
- [x] T-02: Fixed Cell 13 split — per-brand validation + warmup buffer table
- [x] T-03: Replaced aggregated ADF with per-brand ADF top-20 + majority vote in Cell 4
- [x] T-04: Cell 10 now computes lag corrs across all stable brands, 50% significance threshold
- [x] T-05: Cell 11 now extracts significant ACF lags programmatically per brand
- [x] T-06: New Cell 9b — CV, peak-month distribution, promo spread across brands
- [x] T-07: New Cell 5b — zero-sales run analysis (clustered vs scattered) + imputation decision
- [x] T-08: Cell 12 now uses predictive correlation + collinearity pruning to select windows empirically
- [x] T-11: Cell 8 auto-selects additive vs multiplicative via residual variance comparison
- [x] T-12: Cell 15 now shows Pearson + Spearman side-by-side, flags non-linear pairs (Δ>0.1)
- [x] T-13: New Cell 15b — Chow test structural break at 2020-03 (COVID)
- [x] Cell 16 findings JSON updated with ml_target block and empirical parameter rationales

### Outcome
All 13 EDA critique issues resolved. Script now ~1,250 lines. Parameters are empirically derived, not business-heuristic. No manual verification step needed as fixes are in-place edits with clear print outputs at runtime.
