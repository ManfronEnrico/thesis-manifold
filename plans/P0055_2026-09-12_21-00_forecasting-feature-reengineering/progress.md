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


---

## Session 2026-09-13 (afternoon) — Branch B opened; tasks 1 and 3 done

**G0 SATISFIED.** `git rev-list --left-right --count origin/main...HEAD` returns
`0 0`. The Branch A fallback (`58243f3`) is pushed. An earlier report in this
plan said it was not — that was true when written; Brian pushed since.

### Decisions taken

**Branch B runs on `main`, in parallel with Branch A — deliberately.** Enrico
needs Ch9/Ch10 pushed and only one branch can be open. Isolation is therefore by
FILE SURFACE, not by branch. Contract: `BRANCH_B_FILES.md`.

Brian's correction, applied: `05_thesis_results/05_model_benchmark/` is not
cleanly Branch B's, because Branch B generates numbers the thesis will cite. So
the contract carries an **announcement rule** — every regeneration under
`05_thesis_results/` is logged here, naming which numbers moved and which
chapter cites them.

### Task 1 — DONE. `BRANCH_B_FILES.md` written

Green (01_SRQ1, 05_model_benchmark, plans/P0055) / Red (04_SRQ4 esp.
`prompts.py`, 07_*, 08_*, 06_thesis_writing) / Amber (`forecast_tool.py:488`,
the citable SRQ1 tables).

### Task 3 — DONE. Scan closed 41/41

All three outstanding PDFs verified readable at
`C:/Users/brian/Downloads/Hyndman Book (2021)/`.

⚠ **§9.7 was never missing** — on disk since 2026-09-10, merely unread. An
earlier claim in this session that it was a gap was wrong: "not yet read" was
conflated with "not obtainable".

Deleted the stale "Sections still to read" list from `SCAN_LOG.md`; every
section it named already had a recorded entry, and it contradicted the
document's own summary.

### Three findings recorded

1. **§9.7 changes task 4's design.** A portmanteau test on ARIMA residuals needs
   `dof = p + q`. Omitting it OVERSTATES significance — i.e. it would report
   remaining autocorrelation that is an artefact, biasing G1 toward "do more
   work". Recorded against task 4 before it is written.
2. **§5.5 lands on BRANCH A, not B.** *"Point forecasts can be of almost no value
   without the accompanying prediction intervals."* Ch7 can cite 5.5 for why the
   interval-communication criterion exists. **Hand to the Ch9/Ch10 session.**
3. **§5.5 hardens task 2.** Seasonal-naive interval is `sigma*sqrt(k+1)`,
   k = floor((h-1)/m) — parameterised by m, so lag-13 seasonal naive contradicts
   its own interval arithmetic.

### Task 2 re-sequenced — it is NOT the standalone quick win it was offered as

Brian approved jumping the queue on the seasonal-naive contradiction. On
scoping: **`csd_manifest_h3.json` carries lag_1,2,3,4,8,13 — there is no lag_12
column to point at.** So task 2 is now `blockedBy: [1, 5]`, behind the matrix
rebuild. Computing a lag-12 inline was rejected: it would put a second,
divergent lag definition in the codebase, which is the error class task 6 exists
to remove.

### Verified, not transcribed

- All three repair sites still live, untouched by Branch A's commits:
  `srq1_benchmark_cv.py:200` (MASE m=1), `srq1_baselines_stat.py:283`
  (SARIMAX no seasonal order), 19 live lag-13 files (**19, not 22** — the
  earlier count wrongly included two `.archive/` copies)
- `mase_denominator` is defined ONCE at `srq1_benchmark_cv.py:184` and imported
  by `srq1_mase.py`. Task 7 is a single-site fix
- No Ljung-Box code exists anywhere in the repo. Task 4 writes it from scratch
- The 5 pre-existing modified files (`prompts.py`, `srq4_experiment.py`,
  `export_appendix.py`, `score_interval_communication.py`,
  `train_and_persist.py`) are **Branch A comment corrections**, "three
  scenarios" -> "seven". Diffed: NO prompt string changed, `SCHEMA_VERSION =
  "v6-shared-composition"` intact, 63 paid runs valid. **Left uncommitted —
  they are not Branch B's to commit.**

### Next

**Task 4** — write and run the Ljung-Box gate, with `dof = p+q`. Free, no
retrain, no spend. Its verdict decides whether the 2.B feature additions happen
at all.

---

## Session 2026-09-13 (later) — task 4 COMPLETE, gate G1 PASSED

### Task 4's own definition was self-contradictory, and was corrected before coding

The task said: read the four persisted models, run Ljung-Box, pass `dof = p+q`.
**Those two halves describe different models.** `p` and `q` are ARIMA orders;
the four persisted artefacts are XGBoost (CSD, danskvand) and LightGBM
(energidrikke, RTD), which have neither. `dof = p+q` is undefined for exactly
the files the task named. The `dof` requirement came from §9.7's ARIMA section,
the "read the persisted models" instruction from the benchmark folder; they
were written into one task without noticing they did not compose.

**Brian chose ARIMA-only.** That resolves it cleanly and dissolves a second
worry: the persisted models are dated 2026-09-09 and every one still carries
`lag_13`, so their residuals would have been residuals of the specification
Branch B has already judged wrong. Testing ARIMA instead means **no persisted
model is read, no model is retrained, and no Branch A artefact is touched** —
SARIMAX has no saved artefact and refits from the matrix in seconds.

### The gate, and its verdict

New file, GREEN zone, purely additive:
`01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_residual_diagnostics.py`

Fits the same `SARIMAX(1,1,1)` the reported baseline uses, on the same series
under the same retention rule (`len(fit) >= 12 and len(test) > 0`), keeps the
residuals instead of discarding them, and tests at lag 24 (2m, m=12) with
`dof = p+q = 2`. `DOF` is **derived from `ARIMA_ORDER`**, never typed, so
changing the order cannot leave a stale correction behind.

| Category | rejects H0 | rate | median ACF(12) |
|---|---|---|---|
| CSD | 24/95 | 25.3% | +0.131 |
| Danskvand | 6/29 | 20.7% | +0.115 |
| Energidrikke | 5/44 | 11.4% | +0.022 |
| RTD | 16/62 | 25.8% | +0.112 |
| **Overall** | **51/230** | **22.2%** | **+0.109** |

**G1 PASSED: autocorrelation remains. The 2.B additions are justified.**

22.2% against a ~5% null is 4.4x chance, *with* the §9.7 correction applied —
so it is not the overstated-significance artefact the plan warned about.

### The structure is annual — which makes this task 8's evidence too

Splitting by verdict: rejecting brands have median ACF(12) **+0.361**, versus
**+0.064** for non-rejecting. A 5.6x separation at exactly lag 12, positive in
both groups rather than scattered. 29 of the 35 brands whose lag-12 ACF exceeds
their own `2/sqrt(n)` band are also the ones rejecting Ljung-Box.

So the test is not finding diffuse noise; it is finding **seasonality the
non-seasonal ARIMA did not model**. That is repair 2.A1 (task 8) demonstrated
rather than asserted — §9.7 step 6's *"if they do not look like white noise, try
a modified model"* is now a measured result in this repo.

### Checked rather than assumed

- **Convergence**: 5 of 230 SARIMAX fits (2.2%) failed to converge. Far too few
  to explain a 22.2% rejection rate; the finding does not rest on bad fits
- **Power**: residual series are short (34-38 against lag 24), so per-brand
  power is modest. This cuts *toward* the finding — a weak test still rejecting
  22% means the structure is not subtle
- Every figure in `residual_diagnostics.md` is interpolated from a value
  computed that run; nothing transcribed

### ANNOUNCEMENT — three new files under `05_thesis_results/`

Per `BRANCH_B_FILES.md`. **All three are NEW; no existing table was
regenerated, and no number any chapter currently cites has moved.**

| File | Status |
|---|---|
| `tables/residual_diagnostics.md` | new |
| `tables/residual_diagnostics.csv` | new |
| `tables/residual_diagnostics_per_brand.csv` | new |

Nothing for the Ch9/Ch10 session to re-check. If Ch9's limitations section
wants it, the ARIMA residual result is *available* to cite as evidence the
non-seasonal order is a real limitation — but it is not yet cited anywhere.

### Next

**Task 8** (seasonal ARIMA order) now has its evidence and is unblocked —
`blockedBy: [3]`, and 3 is complete. Task 5 (lag 13->12, 19 files) is also
unblocked and is the wider edit. Neither costs money; gate G2's retrain does.


---

## Session 2026-09-13 (third) -- the conversion gap, a defect in my own gate, and the folder-split decision

### 1. I found a defect in the gate I had just run (F13)

`srq1_residual_diagnostics.py` ran on **in-sample** residuals. 5.3 requires
**cross-validation** residuals: fitted values *"are often not true forecasts
because any parameters involved are estimated using all available observations,
including future observations."*

The other two requirements were met correctly and deliberately -- `dof = p+q`
per 9.7, and residuals in log space per 5.3's transformed-scale rule. Only the
CV half is wrong. The script's own docstring says "in-sample" at line 99.

**G1 downgraded PASSED -> PROVISIONAL in `task_plan.md`.** The direction of the
verdict is probably safe (in-sample residuals are optimistically clean, so the
true rejection rate is likely higher than 22.2%, not lower) and the +0.361 vs
+0.064 seasonal-ACF split is a like-for-like comparison that survives. But the
number must not be cited until task 12 re-runs it.

This was caught by a subagent reading the SCAN_LOG for unconverted findings --
not by me re-reading my own work, which is worth noting.

### 2. The findings-to-tasks conversion was incomplete -- 25 findings (F15)

I closed the book scan at 41/41 yesterday and reported it as done. **Coverage of
the book is not conversion into tasks.** A diff of SCAN_LOG against the 2.A/2.B
tables found 25 actionable findings no task picked up. Tasks 12-26 now carry
them.

The substance of Branch B, in one line: four rebuild-class items --- **Fourier
terms (7.4), ACF/differenced features (4.2), KPSS differencing (9.1),
intervention variables (7.4)** --- on top of the 2.A repairs. Plus two FREE
items that produce new reportable results with no retrain and no spend:
**Winkler score (5.9)** and the **anchoring test (6.1)** over the 63 paid runs.

One structural discovery: **13.9's STL gap policy blocks 2.B1, 2.B2 and 12.5
bagging, and no 2.B row named it.** Now task 18.

### 3. A correction to something I told Brian (F14)

I said 10.6 *"supersedes 7.4 on how many lags to carry"* and *"bears directly on
task 5"*, and advised reading it before touching 19 files. **Wrong.** 10.6 is
about lags of an EXOGENOUS predictor, selected by AICc. It says nothing about
target lags or the seasonal period.

Task 5 was never blocked on it. The lag-12 authority is five-fold already --
2.8, 2.7, 5.2, 9.9, 5.5 Table 5.2 -- plus the repo's own ACF (F10d). 10.6 opens
a separate task instead: `promo_intensity` carries exactly one shift and has
never justified that number. Now task 20.

### 4. THE FOLDER SPLIT -- Brian decided, against my recommendation

I argued for one tree with file-level separation. **Brian's counter-arguments
were better and I withdrew the objection.**

| My objection | Why it failed |
|---|---|
| "The 2.A repairs are correctness fixes, wrong in Branch A too" | Branch A will not be retrained or re-experimented -- money spent, 63 runs locked. Fixing its code makes it **look like it produced numbers it did not produce**. Leaving it wrong-as-shipped is **provenance, not debt** |
| "PATHS.py forks and that broke the repo four times" | Solved by naming: `PATHS_branch_A.py` / `PATHS_branch_B.py`, one repo-wide import rename. Measured 1123 lines, 48 importers |
| "git revert is the same work as deleting a folder" | Not with 1.5 working days left. **Deleting a folder is verifiable by looking; reverting interleaved commits is not.** That is a correctness argument about the endgame, not a comfort one |

**The flaw in my reasoning:** I assumed long-run duplicate maintenance. There is
none -- one branch gets deleted.

Recorded as task 26, and in START_HERE.md section 1.

### 5. Brian's standing requirement, recorded because it governs what comes next

> *"we would need to hold our project code faithful to the outputs of our
> pipeline and mold the thesis around those. If an assessor actually checks the
> repo (with AI assistance for instance), these inconsistencies would surface as
> quickly as you identified them."*

This is why task 12 re-runs the gate **inside Branch B's tree** rather than
patching the number in place, and it is the reason F13 was downgraded rather
than quietly corrected.

### Files updated this session

| File | Change |
|---|---|
| `findings.md` | +F13 (gate defect), +F14 (10.6 retraction), +F15 (25 findings). 22 F-sections total |
| `task_plan.md` | G1 row PASSED -> PROVISIONAL with the 5.3 reason |
| `START_HERE.md` | section 1 rewritten for the folder split + its three reasons; section 4 now points at task 26 then 12, and carries the G1 defect |
| `tasks/12-26.json` | 15 new tasks |

### Next

**Task 26** (build the split), then **task 12** (re-run the gate on CV residuals
inside Branch B's tree).
