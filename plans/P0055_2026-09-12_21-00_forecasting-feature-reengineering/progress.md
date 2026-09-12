---
name: p0055-progress
description: STATE - Session log for P0055.
pid: P0055
created: 2026_09_12-21_00
updated: 2026_09_12-21_00
---

# P0055 — Progress

## Session 2026-09-12 — plan created

**Context.** An in-person session (Brian, Enrico, Rico) reviewed the state after
the v6 experiment finished. Rico implemented Chapter 7 changes against the
pre-v6 plan state. The decision taken was to attempt forecasting-feature
re-engineering on a **branch**, with the current results preserved as a
guaranteed fallback.

### Delivered

- Plan folder created with `START_HERE.md`, `FALLBACK.md`, `findings.md`,
  `task_plan.md`, this file.
- Fallback recorded **before** any branch work: commit, schema id, the seven
  headline result rows, and the exact uncommitted file list.

### Four corrections to the session brief, all evidenced in `findings.md`

1. **F1 — the premise was too strong.** Chapter 4 already performs log
   transformation with skewness evidence, ADF tests, differencing and ACF
   analysis, all cited. The accurate claim is that those diagnostics **never
   reached the feature matrix** — the model sees 18 columns with no STL, no
   ACF-derived feature, no Box-Cox and no seasonal term beyond three calendar
   integers. Sharper, checkable, and a better thesis sentence.
2. **F4 — Chapter 8 does not document this, because Chapter 8 is a skeleton.**
   1,384 words, `[N] SKUs × 28 retailers × [T] weeks` placeholders, a weekly
   grain contradicting the monthly panel, and pre-v6 WMAPE figures. Chapter 9
   still states the code-as-action baseline "was not executed… E2B is not
   configured" — it ran 63 times. The real admissions live in **Chapter 5**.
3. **F5 — P0051 already owns half of this**, opened 2026-09-08 on exactly the
   computed-but-unconsumed-diagnostics defect. Fold, do not duplicate.
4. **F7 — the brand-filtered-advantage claim is an assumption.** The cheapest
   test in the project is fitting the pipeline per brand on the same three
   brands. One training run. It separates grain from agency.

### Challenged, with the reasoning

- **Retraining is not the schedule risk.** HPC measured 6 stages in 18.3 minutes
  (`j-12387709`). The prose is the risk: Ch4, Ch5 and Ch8 all describe the
  feature set, and Ch8/Ch9 are unwritten regardless.
- **Chapter 7 is not fully locked.** Its latency, token and cost figures pin to
  `smoke/runs.csv` from 2026-09-11, superseded by the 63-run set. The argument
  holds; three numbers are stale either way.
- **A Ljung-Box residual test should gate Phase 2.** It costs nothing, needs no
  retrain, and either justifies the whole plan or ends it early with a
  reportable result.

### State at close

- **On `main`, v6 work UNCOMMITTED.** Phase 0 is mandatory and unstarted.
- SRQ4 experiment complete: 63 runs, schema `v6-shared-composition+af04a42a478b`.
- No branch created yet — deliberately, because the fallback is not yet a commit.

### Open, in order

1. **Phase 0** — commit the v6 work to `main`, push, record the hash, then
   branch. Nothing else may start first.
2. Phase 1.2 — the Ljung-Box gate.
3. Phase 4 — the grain test, which can run in parallel.

---

## Session 2026-09-12, later — higher-effort re-analysis, three self-corrections

The plan was re-derived from scratch at higher reasoning effort. **Three things
the first draft got wrong**, all corrected in place:

### 1. The P0051 relationship was inverted

The first draft said *"fold P0051 into this plan."* P0051 was then read in full,
and it is **the better-evidenced document** — seven findings with line numbers,
verified by exhaustive grep across three pipeline generations. Its F2 is the
strongest fact in the whole area: **27 of 79 brands test as already stationary
in raw form, so the blanket `d=1` over-differences them.**

Retracted. P0051 stays open, is read first, and P0055 cites it. The
`superseded_by` marker and fold banner were removed; the index row was corrected.

### 2. The premise was still too broad

The first draft narrowed *"forecasting features were not incorporated"* to
*"the diagnostics never reached the matrix."* **Still too broad.** Ch4 §4.2.2
explicitly defends uniform `log1p` on low ADF power at 46 observations and on
feature-semantic consistency — a considered argument the plan must not attack.

The real defect is one sentence later and much sharper: §4.2.2 claims
non-stationarity "is handled by differencing for the statistical baselines,"
which is **false for RTD**, whose own Table 3 in the same chapter reports
`p = 0.000, stationary in level`.

### 3. Phase 2 was ordered backwards

The first draft added STL and ACF features before fixing anything. That builds
on a pipeline whose differencing is wrong for a third of brands. Phase 2 is now
**2.A repairs, then 2.B additions**, and a defensible stopping point is repairs
alone.

### Verified live during the re-analysis

| Claim | Evidence |
|---|---|
| `p_diff` computed, never used | `step_2_eda_descriptive.py:543` computes it; rule at `:549-553` ignores it |
| ARIMA fixed, non-seasonal | `srq1/srq1_baselines_stat.py:283` — `order=(1,1,1)`, no seasonal order; docstring line 26 says *"no pmdarima"* |
| Transform verdict discarded | `derive_log_transform()` now records `adf_stationary_at_5pct` but still returns `LOG_TRANSFORM_TARGET` |
| No consumer surface exists | The engineered dir holds only `*_manifest_h*.json` and `*_split_dates_h*.json` — no contract exposing ADF |
| Feature count | 54 matrix columns, 18 in the `FEATURES` literal, `resolve()` returns 18 on CSD — **no literal-vs-matrix drift** |

### Unchanged from the first draft, and still correct

- Phase 0 remains mandatory: the v6 work is **uncommitted on `main`** and is the
  fallback.
- Ch8 is a skeleton; Ch9's E2B claim is false; Ch7 has three stale numbers.
- The brand-filtered-advantage claim is an assumption, testable by one per-brand
  training run.
- Retraining is not the schedule risk; the prose is.


---

## Session 2026-09-13 — the book scan, and four defects found in code

**Method, approved by Brian before starting:** read all 41 Hyndman &
Athanasopoulos (2021) section PDFs **first, end to end**, derive the standard
from them, and only then diff against the code — because the earlier analysis
anchored on the code and mistook post-hoc justification for methodology.

### Scan outcome: 39 of 41 sections read

| | |
|---|---|
| PDFs on disk | 41 |
| Read end-to-end | **39** |
| §5.5 | **0 bytes on disk** — verified, the only empty file |
| §6.7 | **file contains §6.6 instead** — headers and source URL both confirm |
| Bonus | §6.6 gained, was not on the original list |

Both gaps recorded in `book-scan/SCAN_LOG.md` with the URL to re-obtain.
Neither blocks the feature conclusions; they bear on interval reporting (§5.5)
and judgmental adjustment (§6.7) respectively.

### Four findings, each verified in live code — see findings F9–F12

| ID | Finding | Retrain? |
|---|---|---|
| **F9** | **MASE uses the non-seasonal (m=1) denominator** on a seasonal monthly panel. `np.diff(y)` at `srq1_benchmark_cv.py:200`. §5.8 requires m=12. **This explains the unexplained anomaly that seasonal naive scored worse than naive on MASE** | **No** — metric only |
| **F10** | **The lag set contains no multiple of 12.** `DEFAULT_LAGS = (1,2,3,4,8,13)` | Yes |
| **F11** | ARIMA `SARIMAX(order=(1,1,1))`, no seasonal order, `enforce_stationarity=False` (restates F8, now with §9.7's full algorithm attached). **Prophet checked and CLEARED** | Yes (ARIMA) |
| **F12** | **RETRACTED** — I claimed prose drift the draft had already corrected 14 lines above what I read | — |

### F10 is the strongest finding, and it needs no appeal to the textbook

The chain is entirely internal:

1. The ACF **measured lag 12 significant for 20 of 20 leading brands**, all four
   categories. Lag 13: 10 of 20, and **never without 12 also significant**.
2. The shipped EDA tables state *"Significance at lag 12 indicates annual
   seasonality."*
3. The contract **provenance field** — whose stated job is to answer "why this
   value" — reads *"the lag-12 term is retained because the autocorrelation
   analysis finds it significant."*
4. All four manifests ship `lags: [1, 2, 3, 4, 8, 13]`.

**The one lag that was measured is the one lag that did not reach the matrix.**
`run_seasonal_naive` uses `hist[-12]`; `training_report.py:180` describes
`lag_13` as *"same month last year"*, which is 12. The book's five confirmations
only explain **why** 12 is right.

**HARBOE — one of the three SRQ4 brands — is `[1,2,3,9,12,15]`: 12 yes, 13 no.**

### Scope, corrected twice during the session

- F10e listed 7 fix sites and implied SRQ1 containment. **F10f corrects this:**
  20 live files, including **`02_SRQ2_Tool_Interface/forecast_tool.py:488`**.
- The real fix is not 13 -> 12 in 20 places. It is
  `dropna(subset=["log_sales_units", *_features.LAGS])` — removing the class of
  error rather than relocating it.
- **The SRQ4 experiment is untouched.** `forecast_tool.py` is hit at a row-filter
  literal, not its interface or payload. The 63 paid runs stay valid.

### Highest-value additions the scan identified

| Source | Addition |
|---|---|
| §7.4, reinforced by §12.2 | **Fourier terms** — Prophet already uses them internally (order 10 annual) while the ML models get three calendar integers. They capture the annual cycle **and its harmonics** with **no warm-up cost**, which matters given F10b |
| §9.1, §9.7 | **KPSS not ADF**, via `unitroot_ndiffs` / `unitroot_nsdiffs`; AICc for p,q,P,Q |
| §5.9 | **The Winkler score** — resolves the coverage/width trade-off the thesis reports as unresolved |
| §10.6 | **AICc selects the number of promotional lags** (k), which the repo has never justified |
| §7.6 | **ex-ante / ex-post** — the vocabulary for the leakage boundary, and it explicitly licenses calendar/holiday/Fourier predictors as known in advance |

### Unexpected: §6.1 and §6.2 speak to SRQ4's framing, not its models

§6.2's judgmental-forecasting principles independently justify **prompt
consistency as a methodological control**, and §6.1 names **anchoring** —
"it is common to take the last observed value as a reference point" — which is a
**directly testable hypothesis against the 63 logged runs**: does the agent's
forecast sit suspiciously close to the last observed month? Either result is
reportable.

### State at close

- **Phase 0 still not started.** The v6 work remains uncommitted on `main`.
  Nothing in this session changed that, and it remains the gate.
- No code was modified. The session was read-only apart from plan files.
- Next: write the derived standard, then diff prose (Phase 5 list is in F10c).
