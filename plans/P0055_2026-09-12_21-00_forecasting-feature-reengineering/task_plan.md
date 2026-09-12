---
pid: P0055
created: 2026-09-12 21:00:00
updated: 2026-09-12 21:00:00
status: in_progress
focus_detail: "OPTIONAL WORK WITH A GUARANTEED FALLBACK. The SRQ4 experiment is FINISHED (63 runs, schema v6-shared-composition+af04a42a478b) and its architecture is LOCKED - interface, integration, leakage boundary and prompt composition answer SRQ2/SRQ3 and are not touched here. PHASE 0 IS MANDATORY AND FIRST: commit the uncommitted v6 work to main, because that IS the fallback and it currently lives only in a working tree. Then branch. REVISED 2026-09-12 by a higher-effort re-analysis; three things the first draft got WRONG are corrected in findings.md: (1) P0051 is NOT folded into this plan - it is the EVIDENTIARY SPINE and is read FIRST. Its F2 is the key fact: 27 of 79 brands test as ALREADY STATIONARY in raw form, so the blanket d=1 OVER-DIFFERENCES them. (2) The premise "diagnostics never reached the matrix" is too broad and Ch4 would refute it - Ch4 SS4.2.2 explicitly defends uniform log1p on low ADF power at 46 observations, which is a considered argument. The narrow, citable defect is the sentence after it, which says non-stationarity is handled by differencing - FALSE for RTD, whose own Table 3 reports stationary in level. (3) REPAIRS BEFORE ADDITIONS: three provably-broken sites verified live (F8) - SARIMAX(1,1,1) with no seasonal order on a seasonal monthly panel at srq1_baselines_stat.py:283 (its docstring admits "no pmdarima"); p_diff computed and never used in the stationarity rule at step_2_eda_descriptive.py:543-553; derive_log_transform() computing a verdict then returning the config constant. A DEFENSIBLE STOPPING POINT IS REPAIRS PLUS A RETRAIN WITH NO NEW FEATURES. Also: Ch8 is a 1,384-word SKELETON with [N]-style placeholders and a weekly grain contradicting the monthly panel, Ch9 still claims the code-as-action arm never ran (it ran 63 times), and Ch7 has three stale numbers regardless of this plan. The brand-filtered-advantage claim is an ASSUMPTION; the cheapest test is one per-brand training run (Phase 4). Retraining is NOT the schedule risk (HPC: 6 stages in 18.3 min). The prose is."
---

# P0055 — Forecasting pipeline: repairs, then optional additions

> **Read `START_HERE.md`, then `FALLBACK.md`, then `findings.md`.**
> This plan is abandonable by design. `main` always ships.

---

## Goal

Repair three provably-broken sites in the forecasting pipeline, then — only if
justified by measurement — add features the literature supports, retrain, and
re-run the experiment. **Without putting the finished v6 results at risk.**

The emphasis is deliberate: an earlier draft framed this as *adding* features.
The higher-value and lower-risk work is **fixing what is already wrong**, and
Chapter 5 already admits two of the three defects, so repairing them converts
stated limitations into results.

## What this plan will NOT do

- Touch the SRQ4 experiment architecture, the tool interface, the integration
  or the leakage boundary. **SRQ2/SRQ3 are answered and locked.**
- Change the prompt schema. Any edit invalidates 63 paid runs.
- Change the pooled / per-category training grain. That is a defended design
  choice (M5 cross-learning precedent) and stays a stated limitation.

---

## Phases

### Phase 0 — Secure the fallback ⚠ MANDATORY, BEFORE ANYTHING ELSE

The entire v6 redesign and the 63-run result set are **uncommitted on `main`**.
Until they are committed, there is no fallback to fall back to.

| Step | |
|---|---|
| 0.1 | Stage the v6 work **by explicit path** — never `git add -A` |
| 0.2 | Decide on `raw_responses/` (~9 MB, embeds Nielsen history) — commit or keep local, deliberately |
| 0.3 | Commit and push to `origin/main` |
| 0.4 | Record the resulting commit hash in `FALLBACK.md` |
| 0.5 | **Then** branch: `git checkout -b data/forecasting-feature-reengineering` |

**Status:** pending. Nothing below may start until 0.4 is written down.

### Phase 1 — Establish the gap, in code not in prose

| Step | |
|---|---|
| 1.1 | Inventory what `engineer_features()` builds vs what `_features.FEATURES` admits |
| 1.2 | Run a **Ljung-Box test on current model residuals** (§5.4). Cheap, no retrain, and it answers whether the feature set is leaving signal behind |
| 1.3 | **Read P0051 findings F1-F7 first** — they are this plan's evidence base, not a subset to absorb. P0051 stays open |
| 1.4 | Write the gap list with one source section per item |

**1.2 is the gate.** If residuals are already indistinguishable from white
noise, the case for more features weakens sharply and this plan should stop
early — which would itself be a reportable result.

### Phase 2 — Implement, one feature group at a time

Each addition must clear the same three bars before it is written:

1. **Sourced** — a named section of Hyndman & Athanasopoulos, read directly
2. **Time-safe** — computed only from observations at or before `t − horizon`,
   the invariant `engineer_features()` already documents
3. **Reaches the model** — added to `_features.FEATURES`, not merely engineered

> ⚠ **Bar 3 is not hypothetical.** The holiday columns were engineered
> 2026-08-18, measured by an ablation, and **never added to any FEATURES list**,
> so the ablation reported a benefit the served model could not receive (P0049
> F31). `resolve()` intersects; it never *adds*.

### ⚠ REPAIRS BEFORE ADDITIONS (reordered 2026-09-12 by findings F8)

An earlier draft of this phase listed STL features first. **That builds on a
pipeline whose differencing is provably wrong for roughly a third of brands.**
Repair first; add second. Each repair is independently shippable.

**2.A — repairs (do these first; each is cheap and already admitted):**

| # | Fix | Site | Source |
|---|---|---|---|
| 2.A1 | Seasonal ARIMA order, or `auto_arima` order selection | `srq1/srq1_baselines_stat.py:283` | §9.9, §9.6 |
| 2.A2 | Use `p_diff` in the stationarity decision rule; allow `"diff"` and `"none"` verdicts | `step_2_eda_descriptive.py:543-553` | P0051 F7 |
| 2.A3 | Return the computed verdict, or state plainly that the constant is the design choice | `step_3_derive_params.py` | P0051 F4 |
| 2.A4 | Fix the code comment claiming the ADF csv is consumed | `pipeline_config.py:218` | P0051 F6 |
| **2.A5** | **MASE seasonal denominator: `np.diff(y)` (m=1) -> lag-12 difference** | `srq1_benchmark_cv.py:200` | 5.8, F9 |
| **2.A6** | **Lag set: 13 -> 12, and `rolling_mean_13` -> `_12`** | 20 live files, F10f | 2.7/2.8/5.2/7.4/9.9 + the repo's OWN ACF and provenance, F10a/F10d |
| **2.A7** | **Guard on `*_features.LAGS`, not a hardcoded `lag_13` literal** | the same 20 files | F10f — removes the error class |

### 2.A5 and 2.A6 are the two highest-value repairs, and 2.A5 is nearly free

**2.A5 (MASE) needs no retrain.** It rescores existing predictions and is
independently shippable. It also **explains an anomaly already in the thesis** —
seasonal naive scoring worse than naive on MASE — which converts a puzzling
result into a corrected one.

**2.A6 (lag 12) is the strongest-evidenced defect in the plan** and needs no
appeal to the textbook: the repo's own ACF measured lag 12 significant for
**20 of 20** leading brands, its EDA tables say so, and its contract provenance
says *"the lag-12 term is retained"* — while the manifests ship `13`. See
F10a/F10d. It requires a matrix rebuild and retrain.

⚠ **2.A6 crosses three tiers**, including `02_SRQ2_Tool_Interface/forecast_tool.py`
(F10f). It does **not** touch the SRQ4 harness, prompts or leakage boundary, so
the 63 paid runs stay valid — but it is not a preprocessing-only change and must
not be scheduled as one.

⚠ **Do NOT add lag 24 without measuring first.** 9.9 reads seasonal structure at
12, 24 and 36, but `warmup = max(lags)` so a 24-lag drives `min_periods` to 28 on
a 39-month panel. **Fourier terms (7.4) give the annual cycle and its harmonics
with zero warm-up cost** and are the better first move (F10b).

**2.A1 is the highest-value single change in this plan.** Chapter 5 already
admits the missing seasonal order, so fixing it converts a stated limitation
into a result with no new prose argument needed.

**2.B — additions (only after 2.A, and only if Phase 1.2 justified them):**

| # | Addition | Source | Note |
|---|---|---|---|
| 2.B1 | STL trend strength, seasonal strength | §4.3 | Formulae given explicitly: `max(0, 1 − Var(R)/Var(T+R))` |
| 2.B2 | STL remainder ACF (`stl_e_acf1`, `stl_e_acf10`), spikiness | §4.3 | Same decomposition, no extra cost |
| 2.B3 | ETS as a benchmark family | §8.6, §9.10 | Ch5 already admits the omission |
| 2.B4 | Simple-average combination baseline | §13.4 | Highest expected accuracy gain of any addition |

**2.A1, 2.B3 and 2.B4 are benchmark/model changes, not feature changes.** They
need no matrix rebuild and can ship independently of a retrain — so they survive
even if Phase 3 is abandoned.

> **A defensible stopping point is 2.A alone.** Repairs plus a retrain, with no
> new features, would answer the brief's intent and carries the least risk.

### Phase 3 — Retrain and re-run

| Step | Cost |
|---|---|
| 3.1 | Rebuild matrices, all four categories | local, minutes |
| 3.2 | Full HPC retrain (22 stages; see P0053 runbook) | 1–2 h |
| 3.3 | Re-run SRQ4, 63 runs, **unchanged prompt schema** | ~$20, ~1 h |
| 3.4 | Regenerate figures and tables (P0050) | minutes |

**Decision gate before 3.3:** if the retrained models do not improve on the
current test WMAPE, **do not spend the $20**. Report the re-engineering as a
measured negative result and keep the v6 experiment as-is. A negative result
here is publishable and costs nothing.

### Phase 4 — The grain test (high value, independent, cheaper than first estimated)

Fit models **per brand** on HARBOE, 7-UP and ØRBÆK and compare against the
pooled and per-category models on the same three. This separates *grain* from
*agency* and converts the brand-filtered-advantage claim from an assumption
into a measurement. **Runs in parallel with Phase 2**; independent of the
re-engineering.

#### ⚠ CORRECTED 2026-09-12 — "one training run" was wrong, and the truth is better

An earlier draft said this was one run of the existing pipeline. It is not:
**`srq1_pooled_perbrand.py` does NOT fit per brand.** Its docstring is explicit
that it *"refits the exact same models as `srq1_pooled.py`… then scores per
brand rather than per category"*, and its loop (line 157) iterates the **test**
frame calling `.predict()` on two already-fitted models. Pooled-vs-per-category,
scored per brand — a different question.

What actually exists, which makes this cheaper than a new subsystem:

| Half | Status | Where |
|---|---|---|
| **Statistical** | **Already per-brand. Free.** ARIMA, Prophet and Ridge are each fitted on one brand's `train+val`, guarded by `len(fit) >= 12` | `srq1_baselines_stat.py:323` |
| **ML (LightGBM/XGBoost)** | Needs a modest new loop — but no new infrastructure | reuse `_fit_tuned`, `_all_metrics`, `_load`, `FEATURES` from `srq1_pooled.py` |
| **Reporting** | Convention already set: 460 rows × 13 cols with `n_train`, `mean_test_units`, `delta_wmape` | `pooled_perbrand.csv` |
| **Stratification** | Syntetos-Boylan-Croston demand classes (p = 1.32, CV² = 0.49) | `pooled_perbrand_summary.md` |

**Extend that schema; do not invent one.** Add a `perbrand_wmape` column beside
the existing pooled and per-category columns so the three grains sit in one
table.

> ⚠ **Filter on `scorable` before averaging anything.** `pooled_perbrand.csv`
> carries WMAPE values around `4.9e+12` for brands with `mean_test_units = 0.0`.
> They are flagged `scorable = False` for exactly this reason, and any mean that
> includes them is meaningless.

**Expect per-brand fitting to fail or degrade on short series** — the
statistical arm already skips brands with fewer than 12 fit rows. That is not a
defect of the test; **it is part of the answer**, and it is the same
short-series argument (§13.7) the thesis uses elsewhere.

### Phase 5 — Prose

| Chapter | Change |
|---|---|
| Ch4 | The diagnostics now reach the matrix; state which and cite each |
| Ch5 | Benchmark families updated; remove or narrow the ETS/seasonal-ARIMA admissions if fixed |
| Ch8 | Results regenerate. **Note: Ch8 is currently a skeleton, not prose** |
| Ch9 | The §9.1.4 E2B claim is false and must go regardless of this plan |
| Ch10 | Limitations: grain stays; add the Phase 4 measurement |

**Ch6 and Ch7 are not touched** — except Ch7's three stale numbers, which are
P0048's problem either way.

---

## Decision gates, in order

| Gate | Question | If no |
|---|---|---|
| **G0** | Is the v6 work committed and pushed? | **STOP.** Do Phase 0 |
| **G1** | Do residuals show remaining autocorrelation (Ljung-Box, §5.4)? | Skip 2.B additions; do 2.A repairs anyway — they are correctness fixes, not enhancements |
| **G2** | Do retrained models beat current test WMAPE? | Don't spend the $20; keep v6 |
| **G3** | Is there time to rewrite Ch4/Ch5 prose? | Abandon; `FALLBACK.md` |

---

## Definition of done

Either:

- **Success** — new features sourced, time-safe and reaching the model;
  retrained; experiment re-run; prose updated; `main` merged.
- **Clean abandonment** — `status: cancelled`, a `cancellation_reason`, one
  `progress.md` paragraph on what was measured, and `main` untouched.

**Both are acceptable outcomes.** Only leaving `main` in a broken or
uncommitted state is not.
