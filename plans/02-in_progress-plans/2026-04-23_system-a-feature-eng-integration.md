---
created: 2026-04-23
updated: 2026-04-23
branch: session/thesis-agents-review
status: DRAFT — awaiting human approval
---

# Plan: Wire Feature Engineering Into System A + Sync Thesis State

## Context

**Why this plan:** Brian ran the smoke tests proposed in session `thesis-agents-setup-verification` against System A (`ai_research_framework`), System B (`thesis_production_system`), and the standalone preprocessing script. The results expose three concrete, scoped gaps that block System A from running end-to-end, and a documentation drift in `docs/tasks/thesis_state.json`. This plan consolidates those findings, pairs each with an executable fix, and defines the parallel-worktree execution strategy for the next session.

**What prompted it:**
- `test_agents.py` → ✅ passes (Nielsen 2.5M rows + Indeks 20K × 6.3K load cleanly).
- `test_langgraph_pipeline.py` → builds the LangGraph correctly but halts with `DataAssessmentAgent failed: Feature engineering: pending data access`.
- System B import check → ✅ `OK`.
- `python thesis/data/preprocessing/combined_scripts/preprocessing.py` → `ModuleNotFoundError: No module named 'thesis'` (packaging / sys.path bug; `ROOT = parents[2]` resolves to `thesis/data/`, not the repo root).

**Intended outcome:** System A's LangGraph pipeline executes through at least the feature-engineering phase using real Nielsen data, the preprocessing script runs standalone, and `thesis_state.json` reflects the actual 2026-04-23 thesis state (not the 2026-03-15 snapshot currently pinned).

**Non-goals:**
- No modifications to System A's agent logic beyond the single `_engineer_features()` stub. System A is marked FROZEN for research-artefact reasons; wiring an existing module into a stub is an integration fix, not a redesign. Flag to supervisor if tighter scope needed.
- No implementation of forecasting/validation stubs in this plan. Those come after feature engineering works.
- No edits to System B agents. Phase 1 state extension is already complete (verified: `toggles`, `material_gaps`, `chapter_states`, `style_profile` present in `thesis_state.py:120-135`; outcome at `.claude/plans/outcome_files/2026-04-15_integration-phase1-execution.md`). The earlier parallel audit marking it "open" was wrong.

---

## Findings summary (from Brian's test results)

| Component | Entry point | Result | Blocker |
|---|---|---|---|
| System A config + data loading | `test_agents.py` | ✅ PASS | — |
| System A LangGraph pipeline | `test_langgraph_pipeline.py` | ⚠️ HALTS at feature engineering | `DataAssessmentAgent._engineer_features()` raises `NotImplementedError("Feature engineering: pending data access")` |
| System B imports | `python -c "from ... import ThesisCoordinator"` | ✅ PASS | — |
| Standalone preprocessing | `python thesis/data/preprocessing/combined_scripts/preprocessing.py` | ❌ FAIL | `ModuleNotFoundError: No module named 'thesis'` — `ROOT = parents[2]` wrong |
| `docs/tasks/thesis_state.json` | — | ⚠️ Stale | `last_scraped: 2026-03-15`; `session_id: 20260315-000000`; claims ch1–ch4 are `prose_draft` with `word_count_estimate` values that look like character counts (e.g. 50500 for ch2 = ~50kb markdown, not 50k words) |

**The good news:** Feature engineering itself is fully implemented at `thesis/data/preprocessing/combined_scripts/preprocessing.py` (lags 1–13, rolling stats, Danish-calendar holiday flags, promo intensity, log target). It's just not wired in and not runnable from its current location. This is a 2-fix problem, not a missing-feature problem.

---

## Scope of work

Three independent workstreams. They touch disjoint file sets and can run in parallel across isolated worktrees.

### Workstream A — Fix preprocessing standalone runnability
**Branch:** `chore/preprocessing-packaging-fix`
**Root cause:** `thesis/data/preprocessing/combined_scripts/preprocessing.py:24` sets `ROOT = Path(__file__).resolve().parents[2]` which resolves to `C:\dev\thesis-manifold\thesis\data\` — missing the repo root by one level. The `sys.path.insert(0, str(ROOT))` then can't find the top-level `thesis` package.
**Fix (investigate both options, then pick — per Brian's decision):**
The worktree agent first checks which `__init__.py` files exist along `thesis/ → thesis/data/ → thesis/data/preprocessing/ → thesis/data/preprocessing/combined_scripts/`, whether `pyproject.toml` declares `thesis` as a package, and whether other modules in the repo use `python -m` invocation. Then picks:
1. **Option A (minimal):** Change `parents[2]` → `parents[3]` so `ROOT` = repo root. Ships in 5 min.
2. **Option B (clean):** Add missing `__init__.py` files, drop the `sys.path.insert`, invoke as `python -m thesis.data.preprocessing.combined_scripts.preprocessing`. Cleaner but larger diff.

Pick B only if it's <30 min of work AND the rest of the repo already uses `python -m` style. Otherwise pick A. Document the choice and reasoning in the outcome file.
**Acceptance:** `python thesis/data/preprocessing/combined_scripts/preprocessing.py` (from repo root) runs without `ModuleNotFoundError`. If it then fails for a different reason (missing DB credentials, etc.), log separately — that's out of scope for this workstream.
**Files touched:** `thesis/data/preprocessing/combined_scripts/preprocessing.py` (one line) OR `__init__.py` files under `thesis/`.

### Workstream B — Build the real feature-engineering integration into System A
**Branch:** `chore/feature-eng-wire-system-a`

**Context update (after Brian's feedback):** The `NotImplementedError` in `DataAssessmentAgent._engineer_features()` is a stub left by a colleague. This is NOT a "frozen artefact — don't touch" situation. Brian wants a **proper integration**, not a minimal wire-up.

**Reference assets in the repo:**
- Existing implementation: `thesis/data/preprocessing/combined_scripts/preprocessing.py::engineer_features()` — handles domain-specific temporal features (lags 1–13, rolling mean/std 4/13, Danish calendar, promo intensity, log target).
- Project skill: `.claude/skills/feature-engineering/SKILL.md` — generic sklearn-based patterns (encoding, scaling, polynomial, interactions, binning, imputation, leakage-safe `ColumnTransformer` pipelines). Use this as the methodology reference when designing the integration.
- Project skill: `.claude/skills/forecasting-time-series-data/SKILL.md` — generic ARIMA/Prophet-style forecasting guidance (trend/seasonality analysis, model selection, confidence intervals, evaluation metrics MAE/RMSE). Use when designing the feature set with the downstream forecasting phase in mind.
- Project skill: `.claude/skills/aeon/SKILL.md` (with references for `forecasting.md`, `regression.md`, `transformations.md`, `similarity_search.md`, `segmentation.md`, `anomaly_detection.md`, etc.) — aeon is a scikit-learn-compatible time-series library. The `transformations.md` and `regression.md` references are directly relevant to this workstream; `forecasting.md` informs the downstream step. Prefer aeon-style scikit-compatible transformer classes over bespoke DataFrame-in/DataFrame-out functions, because they compose cleanly with `ColumnTransformer` and the leakage-safe `fit`/`transform` pattern.

**Gap analysis between what exists and what a proper integration needs:**

| Dimension | In `preprocessing.py` today | In feature-engineering skill | Needed for System A |
|---|---|---|---|
| Temporal (lags, rolling, calendar) | ✅ Nielsen-specific | Generic patterns | ✅ Keep existing |
| Log / power transforms | ✅ `log_sales_units` | ✅ `np.log1p`, `sqrt` | Keep, possibly extend |
| Encoding (categorical → numeric) | ❌ None | ✅ OneHot / Ordinal / Label | ⚠️ Needed for brand/market if modelled as features |
| Scaling | ❌ None | ✅ Standard / MinMax / Robust | ⚠️ Required for gradient-based models in forecasting phase |
| Interactions | ❌ None | ✅ Patterns provided | Optional; add only if domain-justified |
| Polynomial features | ❌ None | ✅ `PolynomialFeatures` | Optional |
| Leakage-safe pipeline | ⚠️ Train/val/test split is locked but transforms fit on full data | ✅ `ColumnTransformer` + `Pipeline` | ⚠️ Must fit scalers/encoders on train only |
| Missing-value imputation | ❌ None visible | ✅ Mean/median/ffill | ⚠️ Confirm with data EDA |
| Time-series-specific transformers (seasonal decomp, detrending, Fourier, wavelet, PAA) | ❌ None | Partial (log only) | Consider via aeon `transformations` — justify before adding |
| Stationarity checks (ADF, KPSS) | ❌ None | ❌ None | ⚠️ Required before ARIMA-family models per forecasting skill |
| Forecasting-phase compatibility (feature set must be consumable by ARIMA / Prophet / tree-based / deep) | Implicit | Handled in forecasting skill | ⚠️ Design feature output so all 5 forecasting models listed in System A config can consume it |

**Integration approach (three sub-steps):**

1. **Audit the existing `engineer_features()`** — confirm its outputs, inputs, assumptions, and any data-leakage paths (does it fit transforms on the full frame before splitting? If so, that's a leakage bug that blocks SRQ1 credibility).

2. **Extend it into a proper feature-engineering module** — new file likely at `thesis/thesis_agents/ai_research_framework/features/` (or similar; worktree agent decides based on repo conventions). Structure:
   - `engineer_features.py` — the full pipeline, refactored from `combined_scripts/preprocessing.py`.
   - Split into `fit()` / `transform()` (scikit-learn compatible) so scalers/encoders can be fit on train only and applied to val/test without leakage.
   - Return both the feature matrix AND a fitted transformer object (System A can serialise it per the locked split in `preprocessing.py:37-39`).
   - Cover the gaps in the table above that are domain-justified; document gaps intentionally NOT filled (e.g. "no interactions added — no theoretical basis in the demand-forecasting literature for this dataset").

3. **Wire it into `DataAssessmentAgent._engineer_features()`** — import the new module, call `fit` on train portion, `transform` on full frame, persist the fitted transformer + feature matrix to `thesis/analysis/outputs/phase1/`, update LangGraph state so `ForecastingAgent` can consume it.

**Acceptance:**
- `python thesis/thesis_agents/test_langgraph_pipeline.py` advances past `data_assessment` without the feature-engineering error.
- Feature matrix written to `thesis/analysis/outputs/phase1/feature_matrix.parquet` (matching the existing preprocessing.py output contract).
- Fitted transformer persisted alongside so inference-time use is possible.
- A short design note at `docs/dev/feature_engineering_design.md` explaining what's in/out and why (for supervisor + Enrico traceability).
- Unit-test-level sanity: feature matrix has no NaNs in numeric columns, no scaler was fit on val/test rows.

**Files likely touched:**
- NEW: `thesis/thesis_agents/ai_research_framework/features/engineer_features.py` (primary module).
- MODIFIED: `thesis/thesis_agents/ai_research_framework/agents/data_assessment_agent.py` (the `_engineer_features` stub).
- MODIFIED (possibly): `thesis/data/preprocessing/combined_scripts/preprocessing.py` — deduplicate if logic fully moves into the new module. Decision point: keep as standalone batch script that imports from the new module, or retire it.
- NEW: `docs/dev/feature_engineering_design.md`.

**Risk:**
- Pre-commit hook blocks direct `.py` edits on OneDrive paths — must use the safe temp-script pattern documented in `docs/tooling/tooling-issues.md`.
- Leakage audit may surface that `preprocessing.py` is already leaking (transforms fit on full frame). If so, that's a methodological finding for the thesis itself, not just an engineering fix. Surface to Brian immediately; do not silently fix and move on.

**Scope boundary:** This plan covers feature *engineering*. Feature *selection* (picking which of the engineered features to keep) is a modelling decision for Chapter 6, not this workstream.

### Workstream C — Sync `docs/tasks/thesis_state.json` with reality
**Branch:** `chore/thesis-state-json-sync`
**Root cause:** JSON snapshot reflects 2026-03-15 state; today is 2026-04-23. Specifically:
- `last_scraped: 2026-03-15` → should reflect the most recent literature scraping run (need to confirm actual date).
- `session_id: 20260315-000000` → replace with current date or remove if not needed for workflows.
- `word_count_estimate` values for ch1 (21400), ch2 (50500), ch3 (27300), ch4 (22700) — per Brian: unclear whether these are word counts or character counts. **Investigate first:** worktree agent runs `wc -w` and `wc -m` on each section file (`thesis/thesis-writing/sections-drafts/ch1-introduction.md` etc.), compares to the JSON values. Three outcomes:
  - Match on `wc -w`: field name correct, values just stale → recompute and update.
  - Match on `wc -m`: field name wrong → rename to `character_count_estimate` OR recompute actual word counts.
  - Match neither: values are arbitrary and need full recomputation.
  Report findings and pause for Brian's call on naming before committing.
- `compliance_note` fields reference dates from 2026-04-12 — verify these checks are still the latest.
- `literature_state.papers` lists 23 papers; `literature.confirmed_papers` lists 11 more with `run: 3`; `total_confirmed: 37`. Reconcile the two structures or document why both exist.
- `rq_version: v2`, `gap_analysis_version: v3` — confirm these match current repo state.
**Acceptance:** JSON reflects what's actually on disk as of 2026-04-23. Diff reviewed by Brian before merge. Enrico can read the updated file and understand current state without asking.
**Files touched:** `docs/tasks/thesis_state.json` only.
**Risk:** Low. This is a data/documentation file, no code executes from it directly — but downstream agents (System B) do load it, so schema must remain valid. Run `ThesisState.load("docs/tasks/thesis_state.json")` after the edit to confirm.

---

## Execution strategy

### Parallel worktree setup

Each workstream gets its own isolated worktree so file writes don't collide. Parent session stays on `session/thesis-agents-review`.

| Worktree | Branch | Agent type | Duration estimate |
|---|---|---|---|
| `.cc/worktrees/preprocessing-packaging-fix/` | `chore/preprocessing-packaging-fix` | general-purpose, `isolation: "worktree"` | 15–30 min |
| `.cc/worktrees/feature-eng-wire-system-a/` | `chore/feature-eng-wire-system-a` | general-purpose, `isolation: "worktree"` | 30–60 min (includes hook workaround) |
| `.cc/worktrees/thesis-state-json-sync/` | `chore/thesis-state-json-sync` | general-purpose, `isolation: "worktree"` | 45–60 min (lots of manual cross-check) |

Each agent receives a self-contained prompt including:
- Project-specific context pointers (`CLAUDE.md`, `docs/dev/repository_map.md`, System A frozen marker).
- The specific workstream section above, verbatim.
- Tooling-issue reminders (CRLF, OneDrive `.py` hook, `Read` over `cat`, etc.).
- Instruction to draft an outcome file at `.claude/plans/outcome_files/2026-04-23_<slug>.md` upon completion.

### Ordering

A, B, C can start simultaneously. B is the one most likely to need human input (frozen-system policy), so surface questions early.

### Integration

After all three complete:
1. Review each worktree's diff (`git diff main..<branch>` from inside each worktree).
2. Merge in order: C → A → B (lowest to highest risk).
3. Re-run the smoke test suite (`test_agents.py` → `test_langgraph_pipeline.py` → preprocessing script) to confirm nothing regressed.
4. Draft a combined commit message referencing this plan.
5. Push to origin; open draft PR for Enrico's review.

---

## Critical files

| Path | Purpose in this plan |
|---|---|
| `thesis/data/preprocessing/combined_scripts/preprocessing.py` | Workstream A — fix `parents[2]`; source of `engineer_features()` used by Workstream B |
| `thesis/thesis_agents/ai_research_framework/agents/data_assessment_agent.py` | Workstream B — replace `NotImplementedError` stub with call into preprocessing module |
| `thesis/thesis_agents/ai_research_framework/core/coordinator.py` | Workstream B — verify state passing from `data_assessment` → `forecasting` still works after wiring |
| `docs/tasks/thesis_state.json` | Workstream C — full sync target |
| `thesis/thesis-writing/sections-drafts/ch1-introduction.md` (etc.) | Workstream C — source of truth for word counts |
| `.system_a_frozen.md` | Governance — read before Workstream B |
| `docs/tooling/tooling-issues.md` | Workstream B — OneDrive `.py` safe-edit pattern |

## Functions / utilities to reuse (don't rewrite)

- `engineer_features(df: pd.DataFrame) -> pd.DataFrame` — `thesis/data/preprocessing/combined_scripts/preprocessing.py`. Complete, tested implementation. Workstream B imports this, doesn't duplicate it.
- `ThesisState.load(path)` — `thesis/thesis_agents/thesis_production_system/state/thesis_state.py`. Workstream C uses this for schema validation of the edited JSON.
- `NielsenConfig`, `IndeksDanmarkConfig` — already used by `test_agents.py`; no changes needed.

---

## Verification

**End-to-end test sequence (run from repo root, in order, after all workstreams merged):**

```bash
# A — preprocessing standalone
python thesis/data/preprocessing/combined_scripts/preprocessing.py
# Expect: runs past the import error. May still fail later on DB creds — log separately.

# B — full System A pipeline
python thesis/thesis_agents/test_agents.py              # sanity: already passes
python thesis/thesis_agents/test_langgraph_pipeline.py  # expect: advances past data_assessment

# C — JSON schema validity
python -c "from thesis.thesis_agents.thesis_production_system.state.thesis_state import ThesisState; s = ThesisState.load('docs/tasks/thesis_state.json'); print(f'OK: {len(s.sections)} sections, {len(s.literature_state.papers)} papers')"
```

**Pass criteria:**
- Preprocessing script no longer throws `ModuleNotFoundError`.
- LangGraph pipeline advances beyond `data_assessment` (it may still fail at forecasting — that's out of scope).
- `ThesisState.load()` returns a valid state object without raising.
- Every workstream has an outcome file under `.claude/plans/outcome_files/2026-04-23_*.md`.

---

## Decisions recorded from Brian (2026-04-23)

1. **System A stub:** Not a frozen-artefact concern. The `NotImplementedError` is an inherited stub from a colleague. Build a proper integration, not a minimal wire-up. Methodology references: `feature-engineering`, `forecasting-time-series-data`, and `aeon` skills (all three in `.claude/skills/`).
2. **Preprocessing fix (A):** Investigate both options, then pick — preferring minimal fix unless clean refactor is <30 min AND matches repo conventions.
3. **NotebookLM plan:** Delete `.claude/plans/plan_files/2026-04-13_notebooklm-integration-plan.md` outright. (Brian's call, taken literally.)
4. **Word-count/character-count (C):** Investigate first using `wc -w` and `wc -m` against actual section files, then surface findings before committing.

## Open question

**Push strategy:** Draft PR for Enrico after all three merge, or individual PRs per workstream? (Recommend: single combined PR. Three related fixes, one review cycle, easier for Enrico to see the full picture. Flag if you prefer otherwise.)

---

## Out of scope (future plans)

- Implementing `ForecastingAgent.run()` — separate plan once feature engineering is wired. The `forecasting-time-series-data` and `aeon` skills will be the primary methodology references.
- Feature 2–6 System B implementations (anti-leakage, Semantic Scholar, quality check, style calibration, integrity gates) — queued after Phase 1 state extension (already done, despite the earlier audit marking it open).
- NotebookLM Phase 1 execution — superseded; original plan deleted per Brian's instruction. A fresh plan can be drafted later if still needed.

## Cleanup actions executed as part of Workstream C

- Delete `.claude/plans/plan_files/2026-04-13_notebooklm-integration-plan.md` (Brian's explicit instruction, 2026-04-23).
