---
pid: P0023
created: 2026-06-22 15:00:00
updated: 2026-06-22 15:00:00
status: in_progress
focus_detail: "Audit preprocessing & EDA pipeline against academic time series standards. Verify claims by reading actual code, not comments. Identify what's production-ready vs needs improvement for CBS thesis on FMCG demand forecasting."
---

# P0023: Preprocessing Pipeline Audit — Academic Time Series Readiness

## Goal

Conduct an honest, code-verified audit of the current preprocessing and EDA pipeline for CSD Nielsen data, evaluating it against:
1. **Academic rigor** — time series statistical requirements (stationarity, autocorrelation, seasonality proofs)
2. **Domain specifics** — FMCG demand forecasting characteristics
3. **Thesis methodology** — Design Science Research framework (Hevner 2004, Peffers 2007) + CBS compliance
4. **Computational constraints** — 8 GB RAM hard limit
5. **Feature engineering readiness** — Is the data properly prepared for System A's 5 forecasting models?

**Key principle**: Every claim verified by **reading actual code**, not trusting comments or prior documentation.

---

## Phases

### Phase 1: Current State Mapping (Actual Code Audit)
**Goal**: Build a complete inventory of what actually exists by reading the scripts.

**Deliverables**:
- [ ] List all preprocessing scripts (by-step and by-category)
- [ ] Document what each script actually does (not what the docstring says)
- [ ] Extract the actual EDA analysis being performed
- [ ] List all outputs (parquets, JSON, logs, visualizations)
- [ ] Verify paths resolve correctly post-reorganization
- [ ] Check for data leakage or preprocessing errors

**Status**: Not started

---

### Phase 2: Academic Soundness Assessment
**Goal**: Evaluate against time series and FMCG-specific best practices.

**Dimensions to assess**:
1. **Data Integrity**
   - [ ] Missing value handling (is it documented and justified?)
   - [ ] Outlier detection & treatment
   - [ ] Data quality checks before feature engineering
   - [ ] Time index completeness (any gaps in the time series?)

2. **Stationarity & Transformation**
   - [ ] ADF test performed? (current EDA shows results)
   - [ ] Log transformation justified?
   - [ ] Differencing strategy clear?
   - [ ] Is this category-specific or global?

3. **Seasonality Analysis**
   - [ ] Visual + statistical proof (seasonal decomposition works now)
   - [ ] Holiday/promotional effects distinguished?
   - [ ] Is HOLIDAY_MONTHS = {3, 6, 12} justified for CSD or just data-driven?
   - [ ] Seasonal patterns stable across brands?

4. **Autocorrelation & Lag Structure**
   - [ ] ACF/PACF analysis (now works for top brands)
   - [ ] Are LAGS = (1,2,3,4,8,13) theoretically grounded or empirically chosen?
   - [ ] Rolling window sizes (4, 13) justified?
   - [ ] Different brands need different lags?

5. **Feature Engineering Quality**
   - [ ] What features are actually being created per brand?
   - [ ] Are they domain-appropriate for FMCG demand?
   - [ ] Cross-sectional features (brand, market, product) included?
   - [ ] Temporal features (trend, seasonality indicators) included?
   - [ ] Promotional features properly encoded?

6. **Train/Val/Test Split**
   - [ ] Split dates empirically justified?
   - [ ] Is 24m train / 6m val / 12m test reasonable for monthly data?
   - [ ] Forward-chaining (no look-ahead bias)?

**Status**: Not started

---

### Phase 3: Gap Analysis vs Thesis Requirements
**Goal**: Identify what's missing for CBS compliance and System A readiness.

**CBS Thesis Methodology**:
- [ ] Is this Design Science Research (building + evaluating an artefact)?
- [ ] Are preprocessing choices documented as **design decisions** or just code?
- [ ] Are parameter choices (MIN_PERIODS, LAGS, etc.) justified in writing?

**System A Readiness** (for forecasting models):
- [ ] Feature matrix dimensions match expectations?
- [ ] Missing data handled correctly for ML models?
- [ ] Feature normalization/scaling needed?
- [ ] Are there interdependencies between steps that could fail downstream?

**FMCG Domain Specifics**:
- [ ] Promotional effects accounted for?
- [ ] Regional variation (market) considered?
- [ ] Product-level differences (brand, category) isolated?
- [ ] Inventory/supply-side constraints ignored (retail data limitation)?

**Computational Constraints**:
- [ ] Current RAM usage profiled?
- [ ] Parquet caching effective?
- [ ] Can all 4 categories run in parallel or sequentially?

**Status**: Not started

---

### Phase 4: Critique & Recommendations
**Goal**: Honest assessment of what works, what's missing, what needs improvement.

**For each issue identified**:
- [ ] Priority (blocking vs nice-to-have)
- [ ] Effort estimate (quick fix vs phase 5+)
- [ ] Recommendation (implement, document, defer)
- [ ] Impact on thesis narrative

**Critical blockers to escalate**: Any issue that breaks CBS compliance or System A functionality

**Status**: Not started

---

### Phase 5: Output & Handoff
**Goal**: Create actionable document for thesis writing + System A integration.

**Deliverables**:
- [ ] Comprehensive audit report (markdown)
- [ ] Decision matrix: what to fix vs document vs defer
- [ ] Updated P0022 status (completion, blockers, phase 5 scope)
- [ ] Recommendations for thesis chapter 4 (data methodology)
- [ ] Integration readiness checklist for System A

**Status**: Not started

---

## Context & Constraints

**Thesis Deadline**: 15 May 2026 (time-sensitive)

**Thesis Scope** (from thesis-topic.md):
- Main RQ: Extend production agentic system with lightweight forecasting
- SRQ1: Model benchmarking under RAM constraint
- SRQ2: Structured tool/action interface design
- SRQ3: Integration readiness criteria
- SRQ4: Agentic vs non-agentic comparison
- Data: Nielsen CSD, 28 retailers, ~36 months, 142 brands
- Target: MAPE ≤ 15% (LightGBM expected best)
- RAM: 8 GB hard limit

**What We Know**:
- P0022 completed Phases 1–4 (architecture, bug fixes, EDA for CSD)
- 8 PNG visualizations generated (DPI=150, thesis-ready)
- 4/5 categories working (CSD, Danskvand, Energidrikke, RTD; Totalbeer skipped)
- Parquet cache reorganized (preprocessing/ → converted/)
- All step scripts tested for CSD

**What We Need**:
- Honest assessment of academic quality
- Gaps filled before thesis writing
- Clear documentation of design decisions
- System A integration readiness

---

## Known Issues to Investigate

1. **EDA scope**: Global analysis only (facts table). Star schema dimensions not used. Is this academic enough?
2. **Parameter justification**: HOLIDAY_MONTHS, LAGS, MIN_PERIODS chosen empirically. Need theoretical grounding?
3. **Feature engineering**: Steps 2–6 exist, but what features actually result? Are they FMCG-appropriate?
4. **Categorical variation**: Do parameters differ per brand, market, product category? Or one global set?
5. **Reproducibility**: Are preprocessing random seeds set? Is output deterministic?

---

## Decision Log

(Decisions made during audit will be logged here)

