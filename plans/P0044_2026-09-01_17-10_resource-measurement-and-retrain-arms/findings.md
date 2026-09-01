---
pid: P0044
created: 2026-09-01 17:10:00
updated: 2026-09-01 17:40:00
---

# P0044 findings

## F1 — tracemalloc understated XGBoost by 266x. Brian's doubt was correct.

Brian: *"Granted that the training performance log of 8 MB is actually real,
something which I kind of doubt currently, because I remember from training
neural networks, that it took waaaaay more resources."*

Measured, same machine, same tuned configs, same data:

| Model | tracemalloc fit (MB) | **RSS fit (MB)** | pickled size (MB) | ratio |
|---|---|---|---|---|
| Ridge | 5.5 | 5.4 | 0.0 | 1.0x |
| LightGBM | 23.0 | **36.8** | 7.64 | 1.6x |
| XGBoost | **0.1** | **26.6** | 3.70 | **266x** |
| ARIMA | 0.3 | 2.2 | n/a | 7.3x |

The error is confined to LightGBM and XGBoost -- the two models that build their
ensembles in C++. Ridge is unchanged (5.5 -> 5.4) because scikit-learn allocates
through NumPy, which tracemalloc does see. That pattern is the signature of the
bug, not measurement noise: if this were jitter it would not respect the
Python/native boundary so exactly.

The pickled size settles it independently. XGBoost serialises to 3.7 MB, so it
cannot have trained in 0.1 MB. The old number was never small -- it was
**unmeasured**.

## F2 — the fix, and why each part of it is load-bearing

Three changes to `srq1_profiling.py`, none of them cosmetic:

1. **RSS instead of tracemalloc.** RSS is what the OS charges the process, which
   is the unit an 8 GB budget is denominated in.
2. **A poller thread at 5 ms, not a single reading.** Peak memory during a fit is
   transient -- XGBoost frees histogram buffers before returning -- so reading
   once at the end measures what survived, not what was needed.
3. **One subprocess per model.** RSS never returns to baseline in-process
   (allocators retain freed pages), so a sequential loop charges each model with
   its predecessors' retained memory. Ridge would look enormous purely for
   running after XGBoost.

Both columns are retained in the published table so the correction is auditable
rather than silent, and so Ch6 can show the native/Python gap as a finding.

## F3 — two further defects found while fixing it

- **Stale grain label.** The report title read "CSD brand×chain" while line ~92
  has loaded `bymonth` since P0035 deleted the chain grain (DEC-GRAIN). The
  published table named a grain that no longer exists. Fixed.
- **Silent untuned fallback.** `params.get("brand/CSD/LightGBM", {})` would have
  profiled an *untuned default* model had the key been missing, reporting it as
  a tuned result. The keys do resolve, so no past result is wrong, but the
  failure mode was undetectable. Changed to `params[...]` so a missing key
  raises.

## F4 — the corrected numbers STRENGTHEN the thesis, they do not weaken it

Worst case is now 36.8 MB against an 8 GB budget: ~220x headroom rather than the
~1000x the broken instrument implied. The claim survives comfortably, and now
rests on an instrument that can see what it is measuring.

It also makes Brian's [22] intuition quantitative: 8 GB *is* oversized for
serving pre-trained models. That is an argument for the retrain arms
(see F5), not against the budget.

## F5 — refit-per-query is affordable; re-tuning is not (DEC-REFIT-NOT-RETUNE)

Brian's worry: *"that hinges a lot on if that is even possible, with all the
hyperparameter tuning ... I just remember that neural networks had a quite
tedious and slow tuning process."*

The worry is right in general and does not bind here, because tuning and fitting
are separable:

- `04_thesis_results/srq1/tuned_params.json` holds tuned hyperparameters per
  category/model, found offline via **Optuna TPE** (`srq1_benchmark_tuned.py`).
- Fitting on those stored params costs **3.0 s** (LightGBM, 1192 trees) and
  **2.2 s** (XGBoost, 926 trees, depth 7).

So the viable architecture is **refit on fixed hyperparameters, not re-tune**.
Tuned params are stable across a month of new data; the coefficients are what go
stale. A per-query refit of ~3 s and ~37 MB is entirely plausible inside an 8 GB
session -- which is exactly the "always up-to-date, no human retraining step"
argument, and the only design in which the RAM budget is genuinely exercised.

## F6 — the writing surfaces: verified, not assumed

- `sections-final/` is **dead**: all 6 files frozen 2026-07-11, and 4 of 10
  chapters were never exported at all. Superseded by the OneDrive document.
- `sections-drafts/ch1-introduction.md` (3,615 w) and the snapshot (3,395 w) are
  **the same text**; the gap is the footnote plus markdown scaffolding. The
  draft is not a stale predecessor -- it is a second live copy.
- They agree today only because nobody has edited either since the export. That
  luck expires the first time comment [17] is acted on, because the Word
  comments anchor to the .docx and a fix there leaves the .md behind.

Hence DEC-ARCHIVE-NOT-DELETE-PROSE: strip prose from the drafts, archive it,
keep bullets. Two live prose copies with no authority rule is precisely the
drift P0043 exists to prevent.

## F7 — exogenous enrichment is genuinely unsupported (comments [15] [16] [17])

Live features in `_02_preprocessing/nielsen/_shared_modules/engineer_features.py`:
`lag_{1,2,3,4,8,13}`, `rolling_mean/std_{4,13}`, `month`, `quarter`,
`peak_month`, `promo_intensity`, `zero_run_flag`, `zero_run_length`,
`log_sales_units`.

All endogenous (derived from the series' own history) or calendar-derived. Every
holiday-calendar hit in the repo is under `.archive/`. Brian is correct: the
Ch1 claim to "incorporate exogenous predictors" is unsupported.

Note the Ch1 footnote already defines promotional signals and distribution
coverage as exogenous. That is defensible for `promo_intensity` -- promotion is
a decision external to the demand series. So the honest fix is to **narrow** the
claim (promotional and calendar signals) rather than delete it, and to drop the
implication that weather/macro/holiday-calendar enrichment was performed.

## F8 — [25] and [26] are factually wrong about the code

Recording these so the Ch1 rewrite does not "fix" things that are not broken:

- **[25] "memory efficiency is not actually tracked or logged"** -- it is, in
  `srq1_profiling.py` and `train_and_persist.py:214-244`. The instrument was
  wrong (F1), but the tracking exists. SRQ1 is answered on all three axes.
- **[26] "observability and traceability ... unsure whether implemented"** --
  implemented. Every SRQ4 run logs `latency_s`, `tokens_in/out/cached/reasoning`,
  `cost_usd_est`, and a `trace` carrying `tool`, `wrote_code`,
  `tool_returned_forecast`, plus `tool_outputs` and `tool_schema`
  (`srq4_experiment.py:426-534`).
  What is missing is not the logging but an *evaluation* of it: no metric scores
  whether a trace is auditable. If Ch1 promises observability as a **measured**
  property, that is the gap; as an **implemented** property, it is satisfied.

---

## F9 — CORRECTION: "tuned params are stable" was asserted, not verified — and the data argues against it

Brian: *"The pre-tuned parameters, and refitting with known params and not
re-tune, is that okay to do? I mean I am unsure whether 'Tuned params are stable
across a month of new data; the coefficients are what go stale' is true at all."*

He is right to distrust it. I asserted that premise without evidence, and the
files on disk point the other way. `cv_params.json` stores tuned params per
category, model **and metric**:

```
CSD/LightGBM/wmape    -> n_estimators 374, lr 0.032, num_leaves 120
CSD/LightGBM/medmape  -> n_estimators 350, lr 0.014, num_leaves  21
```

Same data, same model, different objective — and `num_leaves` moves 120 -> 21,
nearly 6x. `tuned_params.json` separately gives CSD/LightGBM `n_estimators=1192`
against `cv_params.json`'s 374.

Tuned params are therefore demonstrably **not** stable under small changes in
the fitting condition. Stability across a *month of new data* is a different
question, but that volatility is reason to lower confidence, not raise it.

**Do not write refit-not-retune into the thesis as a premise.** Measure it
(task 16). Either outcome is publishable: if refit tracks re-tune, the cheap
architecture is validated; if it drifts, then on-demand retraining requires
re-tuning, which changes the cost story and is a more interesting finding.

### What refitting actually means (Brian asked)

- **Hyperparameters** are set *before* training: how many trees, how deep,
  learning rate. Optuna searches for them.
- **Coefficients / tree splits** are what training *learns* from the data.

Refit keeps the hyperparameters and relearns the splits on data now including
the newest month. The premise is that hyperparameters describe the *problem*
(series length, noise, seasonality) while splits describe the *data*. Plausible,
unverified, and weakened by the metric-sensitivity above.

## F10 — CORRECTION: the retrain arms are NOT blocked on building a template

Brian: *"arent those already part of the graph engines template? Or am I trippin?"*

Not tripping — this was my error. P0040 F38 records that the engine ships
`prometheus.yaml`, which builds a template carrying the ODBC driver and the
scientific stack, registering under Brian's own E2B account as
`PROMETHEUS_TEMPLATE_ID=prometheus`.

What `measure_e2b_cost.py` probed was E2B's **default base image** (no template
id), which lacks pyodbc/sqlalchemy/statsmodels/xgboost/prophet. Those are
different artefacts and I conflated them: "the default image lacks X" does not
imply "no template provides X".

**Revised blocker:** not "build a template", but "confirm the existing template
alias resolves" — which P0040 flagged as written-but-never-run. Much smaller.

## F11 — timing also shifted, though timing was never the broken instrument

Brian: *"did this also understated the training time necessary?"*

Yes, though not for the reason the memory number was wrong. `perf_counter` was
always correct.

| Model | old fit (s) | new fit (s) |
|---|---|---|
| Ridge | 0.075 | 0.102 |
| LightGBM | 2.039 | **3.011** |
| XGBoost | 0.968 | **2.187** |
| ARIMA | 0.085 | 0.075 |

Two causes, both favouring the new numbers: `tracemalloc` hooks every allocation
and slows the process it measures, and the old run profiled all four models in
one warm process (shared imports, warm caches) where each now gets a cold
subprocess. The new figures are the honest ones.

**Refit cost is ~3 s, not ~2 s.** Still cheap, but earlier statements quoting
2.0 s were quoting the contaminated run.

## F12 — CORRECTION: the fixed measurement does not favour either architecture

Brian: *"how is that cutting toward our arms though? Having such an absurdly low
number before is whats cutting the reliability and trust into our training
process."*

Correct, and my phrasing was wrong. The broken instrument damaged trust in the
*measurement*; repairing it restores that and nothing more. Pre-trained vs.
refitted stays an open engineering decision on cost, latency and code
complexity — which is what the arms exist to settle. Claiming the fix supports
one side was reaching.

## F13 — the feature-engineering pipeline is the real feasibility risk, not RAM

Brian: *"for re-training on demand, it would need to have all the feature
engineering and EDA data cleaning pipeline applied once again, which might not
be suitable anyways with no human intervention (time within the cloud
environment & context bloat when transferring all of the code snippets)."*

This is a stronger objection than the RAM question and should be recorded as a
first-class risk. An on-demand refit needs the full preprocessing chain — load,
aggregate, calendar-fill, engineer features, split — reproduced inside the
sandbox. Two distinct costs:

1. **Wall clock**: the pipeline is many steps over the raw extract, not the
   3 s fit. The fit is the cheap tail of an expensive chain.
2. **Context**: shipping enough code for the agent to reproduce feature
   engineering faithfully is a large prompt payload, and any divergence
   silently produces a differently-featured matrix — a correctness risk, not
   just a cost one.

**Design implication:** the credible on-demand architecture ships the
*preprocessing as a callable artefact* (a pinned module or prebuilt image
layer), not as code-in-context for the agent to re-derive. Worth stating in Ch9
regardless of whether the arms run.

## F14 — Optuna is automatic, so tuning cost is measurable too

Brian: *"could we not also test and measure the resources and time necessary to
tune each model? Because I believe Optuna is a automatic algorithm to tune ML
models, am I correct?"*

Correct — Optuna TPE, `study.optimize(objective, n_trials=trials)`
(`srq1_benchmark_tuned.py:163-164`), fully automatic, no human in the loop. So a
re-tune arm needs no human either, and its cost is measurable with the same
RSS instrument.

Worth measuring precisely because it can *invalidate* refit-not-retune: if a
re-tune is a few hundred trials at ~3 s each, per-query re-tuning is
infeasible and refit becomes the only viable on-demand path. That rules the
alternative out with a number instead of ignoring it.

## F15 — the template yaml was NOT found at the engine root this session

F10 rests on P0040 F38's record that the engine ships `prometheus.yaml`. A search
of the engine tree this session (`find -maxdepth 3 -name prometheus.yaml -o -name
e2b.toml`) returned **nothing**.

This does not overturn F10 — the search was shallow (depth 3) and the engine
arrived as a zip that may have been re-extracted since P0040 — but it does mean
the template is **unconfirmed on disk right now**. Do not plan the retrain arms
on the assumption that it is present.

**Verification is cheap and free** (task 20): locate the yaml, or list the
templates registered against the E2B account, before committing to any arm that
needs the scientific stack in-sandbox. If it is genuinely absent, the fallback
in P0040 F29 stands: build from the engine's Dockerfile, or run against a local
snapshot instead.

---

## F16 — the download worry dissolves: the agent never needs the 38 GB raw extract

Brian: *"just having access to the warehouse via a live connection /= having it
available to insert engineered features, for which the agent would need to
download the dataset (perhaps I am wrong here), and that process took
significant time."*

Measured:

| Artefact | Size |
|---|---|
| `_00_raw/` (full scanner extract) | **38 GB** |
| step-1 aggregate, CSD (brand × month) | **0.81 MB** on disk |
| CSD engineered feature matrix (h3) | **1.08 MB** on disk, 2.12 MB in memory |
| shape | 4,370 rows x 51 cols, 95 brands x 46 periods |

The aggregation is a **~47,000x reduction**, and it happens *inside the
warehouse query*, not on the client. `engineer_features.py:95`
`aggregate_brand_month_from_db(category, conn, target_market)` pulls
facts x dim_product x dim_period x dim_market and returns the data already
aggregated to (brand, period_year, period_month). What crosses the wire is
~1 MB, not 38 GB.

So the premise behind the worry -- that the agent must download the dataset --
does not hold for this pipeline. Aggregation is pushed down to SQL. Measured
client-side load of the aggregate is **0.066 s / 17 MB RSS**.

**This significantly de-risks the on-demand refit.** The chain is not
38 GB -> features; it is `SELECT ... GROUP BY` -> 1 MB -> features -> 3 s fit.

## F17 — but the remaining chain is NOT just the fit, and one step is a real obstacle

The full sequence is seven steps, not two. Steps 0-1 log separately; 2-6 run
inside the orchestrator:

| Step | What it does | On-demand? |
|---|---|---|
| 0 validate cache | one-off, 23.7 s (first build only) | not needed (DB path) |
| 1 load + aggregate | **5.25 s**, 4,209 rows out | pushed to SQL |
| 2 build calendar | reindex to full brand x month grid, fill gaps | deterministic, cheap |
| 3 filter series | drop series failing coverage rules | deterministic, cheap |
| **4 engineer features** | lags, rolling, calendar, promo_intensity, zero-runs | deterministic, cheap |
| 5 apply split | train/val/test by date cutoff | deterministic, cheap |
| 6 save outputs | write parquet + manifest | trivial |

Steps 2-6 are pure deterministic transforms over a ~1 MB frame. Nothing here is
expensive. Total on-demand cost is dominated by the SQL round-trip plus the ~3 s
fit (F11), not by data movement.

**The obstacle is not cost, it is step 3 (`derive_params` / filtering).**
`engineer_features(...)` takes `peak_months` as a **required keyword-only
argument**, and `peak_months` is *derived from the data* by an earlier EDA step
(the archived `pre_csd_1.5_eda.py` computed `HOLIDAY_MONTHS` as months at or
above the 75th percentile of sales). Several pipeline parameters are empirical,
not constants.

That is the genuine reproducibility risk, and it is sharper than context bloat:
an agent re-deriving these parameters from a *different* data window can compute
*different* peak months, and then silently produce a differently-featured matrix
that is not comparable to the trained model's feature space. This is a
correctness failure that no error message announces.

## F18 — critical evaluation: guidelines-not-code is the WORSE of the two options

Brian: *"we could simply send instructions / guidelines to the AI agent in those
scenarios, with information regarding the dataset qualities, EDA steps taken in
the past, features engineered in each, and the AI agent would then re-produce the
steps with less upfront context bloat, compared to sending all code snippets as
they are."*

The instinct (reduce context) is right; the conclusion does not follow, because
it optimises the cheap axis and sacrifices the expensive one.

**Context is not the binding constraint.** `engineer_features.py` is ~800 lines;
the transform itself is a few dozen. At current pricing that is cents per call
against A_plain at $0.4277/run. Trading correctness for a context saving of that
size is a bad exchange.

**Guidelines make divergence undetectable.** If the agent is *told* "we used lags
1,2,3,4,8,13 and rolling windows 4 and 13, and a binary peak-month flag", it will
produce *a* feature matrix. Whether it produces *the same* matrix -- same column
order, same NaN handling, same `min_periods` on the rolling windows, same
zero-run definition, same peak months -- is unverifiable without comparing
against the reference implementation, which is the very thing the guidelines were
supposed to avoid shipping. And the model being served expects exactly the
reference feature space. A mismatch does not raise; it silently degrades
predictions, which is the failure mode hardest to detect in an LLM pipeline and
the one most damaging to a thesis about *reliability and traceability*.

**It also contradicts SRQ2.** The thesis argues for a structured tool interface
that preserves reliability and traceability precisely *because* free-form LLM
code generation does not. Having the agent re-derive feature engineering from
prose is the code-as-action baseline (Scenario B), which the thesis positions as
the weaker design. Adopting it for the retrain arm would argue against the
thesis's own claim.

### Recommendation

**Ship preprocessing as a pinned callable artefact, not as prose or as code.**
The sandbox image already carries the scientific stack; add the preprocessing
module to it, and expose one entry point:

```
build_feature_matrix(category, as_of_date) -> DataFrame
```

The agent calls it. It does not reimplement it. Properties this buys:

- **byte-identical features** to those the model was trained on, by construction
- **near-zero context**: one function signature instead of prose or 800 lines
- **traceable**: the call appears in the tool trace like any other, which is
  exactly what SRQ2 asks for
- **derived params are pinned**, not re-derived, so F17's silent-divergence risk
  disappears

This is the same argument the thesis already makes for `forecast_demand`: the
value of a structured tool is that the agent cannot get it subtly wrong. The
retrain arm should use a structured tool for preprocessing for the identical
reason -- and that consistency is a point in the thesis's favour rather than an
awkward exception.

**What the arms then actually compare** is a cleaner question than "can the agent
rebuild the pipeline":

- **F (pre-trained served)**: model trained offline, served. ~27-37 MB, ~0 s.
- **G (on-demand refit)**: `build_feature_matrix(as_of)` then refit on stored
  params. ~1 MB over the wire, ~3 s fit, ~37 MB peak.

That is a real architectural comparison on freshness vs. latency, which is what
Brian wanted to test, and it no longer depends on the agent reproducing
undocumented empirical parameters.

---

## F19 — MEASURED (task 16): refit-not-retune holds on accuracy, for a reason neither of us predicted

Walk-forward on CSD, 5 monthly cutoffs, LightGBM, wMAPE on held-out next month.
"refit" = stored tuned params; "retune" = fresh Optuna (30 TPE trials) at each
cutoff. `04_thesis_results/srq1/refit_vs_retune.csv`.

| cutoff | refit wMAPE | retune wMAPE | delta | retuned num_leaves |
|---|---|---|---|---|
| 2026-02 | 14.26% | 14.82% | **-0.56pp** | 35 |
| 2026-03 | 15.58% | 10.95% | +4.63pp | 16 |
| 2026-04 | 13.49% | 11.44% | +2.05pp | 93 |
| 2026-05 | 11.69% | 14.49% | **-2.80pp** | 74 |
| 2026-06 | 12.57% | 14.49% | **-1.92pp** | 128 |
| **mean** | **13.52%** | **13.24%** | **+0.28pp** | stored = 63 |

**Refit costs 0.28pp of wMAPE on average and 12x less time (7.0s vs 84.4s).**

But the mean conceals the real finding, and the real finding is the stronger
one: **re-tuning wins in only 2 of 5 cutoffs and LOSES in 3**, twice by more
than 1.9pp. If re-tuning were reliably better, the sign would be consistent.
It is not.

### Why: the hyperparameters are unstable, and that is the argument FOR refit

Re-tuned `num_leaves` across five consecutive months: **16, 35, 74, 93, 128** --
an 8x spread on essentially the same data, one month apart. The stored value
(63) sits mid-range.

Brian's doubt in F9 was therefore **correct on the premise and inverted on the
conclusion**. Tuned params are *not* stable -- confirmed, and more starkly than
cv_params.json suggested. But instability is not evidence that you must re-tune
constantly; it is evidence that the tuning objective is **noisy at this sample
size** (~3,100 rows, 46 months, one month of inner validation). Optuna is
faithfully fitting that noise, then carrying it into the test month. A stored
parameter set, chosen once over the full history, is *more* robust than a fresh
search over a short, noisy validation window.

This is a known effect (over-tuning on small validation sets) and it means the
cheap architecture is also the better-behaved one here. That is a real Ch6
finding, not a convenience.

### Caveats to state, not bury

- One category (CSD), one model (LightGBM), five cutoffs, 30 trials. Enough to
  refute "refit is clearly worse"; not enough to claim "refit is better". The
  honest claim is **equivalent within noise, at 12x lower cost**.
- 30 trials is far below the production tuning budget. A larger budget with a
  proper inner CV would likely stabilise the re-tune arm. That would *raise* the
  cost ratio well past 12x, which strengthens the same conclusion.
- The inner validation is a single month. This is the weakest part of the design
  and the most likely source of the noise diagnosed above.

**Verdict: the thesis may state refit-not-retune as a measured design choice**,
with the 12x cost ratio and the +0.28pp accuracy cost, and should report the
sign inconsistency and the num_leaves spread as the evidence. It must NOT claim
refit is more accurate.

## F20 — MEASURED (task 17): a re-tune costs ~12x a refit, and that is a floor

30 TPE trials = **16.9s median** per cutoff vs **1.06s** for a refit (the 2.65s
first refit is import/JIT warm-up, discounted).

Extrapolating to a realistic budget: 200 trials at the same per-trial cost is
~110s of pure tuning per query, against ~1s for a refit -- roughly **100x**.
Per-query re-tuning is therefore infeasible in an interactive agent regardless
of the accuracy question, which is exactly the number needed to rule the
alternative out rather than ignore it (F14).

Optuna needs no human (TPE, `n_trials`), so this is a cost argument, not an
automation one.

---

## F21 — CORRECTION to F19: "re-tuning is worse" was overstated. Brian caught the flaw.

Brian: *"What did you ACTUALLY do to 're-tune'? Did you do an updated data pull?
Because if you didnt, should the re-tuning with the same data, same seed, not
yield the exact same results?"*

The seed WAS fixed (42) at every cutoff, so the search is deterministic given
identical data. The data was not identical -- `tr = d[d.date <= cut]` grows a
month per cutoff and the inner validation month changes -- so the params moving
was not an RNG artefact. That part of F19 stands.

**But the question exposed a missing control**, and running it changes the
conclusion. Holding the cutoff FIXED (identical data) and varying only the
Optuna seed:

| optuna seed | num_leaves | n_est | val wMAPE | **test wMAPE** |
|---|---|---|---|---|
| 0 | 99 | 986 | 7.53% | **13.11%** |
| 1 | 110 | 1099 | 8.03% | **16.64%** |
| 7 | 116 | 729 | 8.71% | **17.08%** |
| 42 | 74 | 676 | 8.13% | **14.49%** |
| 2024 | 114 | 724 | 7.95% | **13.43%** |

Same data, same everything except the search seed: **num_leaves spans 74-116 and
test wMAPE spans 3.97pp**. Determinism confirmed separately (seed 42 twice ->
identical).

**So the across-month spread in F19 was NOT mostly "the data changed".** Search
randomness alone reproduces most of it. The correct diagnosis is that the tuning
objective cannot resolve these hyperparameters at this sample size (95-row
validation month), so the "re-tune" arm's per-cutoff results were substantially
seed noise -- and F19's headline that re-tuning "loses in 3 of 5 months" was
reading that noise as signal.

**Retracted:** "re-tuning is worse on accuracy". Not supported. A 5-cutoff
comparison where a single seed change moves test wMAPE by 3.97pp cannot separate
arms differing by 0.28pp on average.

**Still supported, and unaffected:**
- The **12x cost ratio** (7.0s vs 84.4s) is a timing measurement, not a noise-
  sensitive accuracy claim. ~100x at a 200-trial budget.
- Refit is **not detectably worse** than re-tune. The honest statement is that
  the two are indistinguishable at this sample size, and refit is 12x cheaper.
- Validation-set noise is real and is itself a Ch6-worthy caveat about tuning on
  short monthly panels.

**What the thesis may say:** refit-on-stored-params is chosen because re-tuning
costs 12-100x for no *measurable* accuracy gain at this data scale. NOT because
re-tuning is worse.

**What would settle it properly** (not required for the arms, but honest to
list): multi-seed runs per cutoff, a multi-month inner validation window, and
more cutoffs. That is a bigger SRQ1 study; the cost argument alone is already
sufficient to justify the architecture.

## F22 — RESOLVED (task 20): the template exists and carries the full stack

Brian: *"those credentials are saved into .env are they not? What is blocking
you?"* Nothing was. F15's "not found" came from a shallow filesystem search for
`prometheus.yaml`; the right check is to ask the E2B API what is registered.

`.env` carries `thesis_manifold_e2b_sandbox` (44 chars). Querying
`GET https://api.e2b.dev/templates` with it returns:

```
templateID=fxe7gzkqjupdhbx4uvpr  aliases=['prometheus']  cpu=1  mem=4096MB  public=False
```

Probed live (`AsyncSandbox.create("prometheus")`, 2.42s create, 37.95s total):

| package | status |
|---|---|
| pandas 2.2.3, numpy 2.3.5, sklearn 1.6.1 | OK |
| **pyodbc** | **OK** |
| sqlalchemy 2.0.52 | OK |
| statsmodels 0.14.6 | OK |
| xgboost 3.4.1, lightgbm 4.7.0 | OK |
| prophet 1.4.0 | OK |
| **optuna 4.9.0** | OK |

Every package the default base image lacked (P0042 F8) is present. **F15 is
withdrawn** and the retrain arms are unblocked: no template build, no fallback to
a local snapshot.

Two consequences:
- `PROMETHEUS_TEMPLATE_ID=prometheus` should be added to `.env`; it is currently
  absent, so any code path reading it falls back to the default base image --
  precisely the image that lacks pyodbc.
- The template is **4096 MB**, not 8 GB. The RAM ceiling actually in force for
  sandbox work is 4 GB. Ch1 should not claim 8 GB for the sandbox without
  reconciling this -- refit at ~37 MB is comfortable either way, but the stated
  budget must match the provisioned one.

## F23 — 8 GB vs 4 GB: these are two different budgets, and conflating them would be a new error

Brian: *"then lets change everything to that template number, which was supported
by the actual template that came with the production level copy of prometheus."*

Before doing a global replace: the two figures do **not** describe the same thing,
and the 8 GB claim is load-bearing in 30 files including the RQs, the gap analysis
and the project overview.

| | figure | what it bounds | evidence |
|---|---|---|---|
| **Thesis deployment budget** | ≤ 8 GB | the SME cloud instance hosting the forecasting substrate | asserted from the SME-cost argument; motivated by Ng (2017) |
| **Prometheus E2B sandbox** | **4096 MB** | one code-execution sandbox in the production engine | **measured** (`GET /templates`, F22) |

The 8 GB figure is the *deployment* envelope for the whole system. The 4 GB figure
is what Manifold actually provisions for a *single code-execution sandbox*. A
sandbox is one component inside a deployment, so 4 GB does not replace 8 GB --
it sits inside it.

**Why a global replace would be wrong.** It would rewrite the SME cloud-budget
argument (Ch1 §1.1, the delimitation, G1, the RQs) into a claim about E2B sandbox
provisioning, which is not what those passages argue and not what Ng (2017)
supports. It would also make the thesis assert a number for *its own artefact's*
deployment on the basis of *someone else's* sandbox configuration.

**Why the finding still matters.** Comment [20] is right that the 8 GB was being
justified with a wrong mechanism (hosting an LLM locally). The measured 4096 MB
is the first *hard, verifiable* RAM number in the whole project, and it is the
figure that actually constrains any code the agent runs -- including an
on-demand refit.

### Recommendation (needs Brian's call)

Keep both, and say which is which:

1. **≤ 4 GB — measured, binding on sandbox execution.** Manifold's own template,
   `fxe7gzkqjupdhbx4uvpr`, 4096 MB. Use this wherever the claim is about what the
   *agent* can execute: the refit arm, code-as-action, Ch5's architecture, Ch6's
   operational profiling. This is the number that has evidence.
2. **≤ 8 GB — the SME deployment envelope.** Keep in Ch1/Ch2/gap analysis where
   the argument is about SME cloud economics, but restate it as a *design
   assumption* rather than an empirical constraint, and drop the
   GPU-instance/LLM-hosting justification comment [20] correctly rejects.

Net effect on the results: none. Serving is 36.8 MB and refit ~37 MB, which is
~1% of 4 GB. The claim gets *stronger* under the tighter, measured bound --
which is the better rhetorical position anyway: "fits in a measured 4 GB
production sandbox" beats "fits in an assumed 8 GB budget".

**Do not global-replace until Brian confirms.** The alternative reading -- that
he wants the whole thesis re-anchored on 4 GB, retiring the SME-budget argument
entirely -- is also coherent, and is his call, not mine.

## F24 — glossary + what the refit/retune experiment can and cannot answer

Terms used loosely earlier, defined once:

- **cutoff** — a date splitting history from future, simulating "retrain today".
  Five were used: 2026-02 .. 2026-06. At cutoff 2026-04, train on everything up
  to March, predict April. Five simulated retrain events, nothing more.
- **trial** — one hyperparameter combination Optuna tests. 30 trials = 30
  combinations tried, best kept.
- **what was executed** — 30 trials x 5 cutoffs = **150 tuning runs**, plus 5
  refits. Wall clock: **84.4 s total** for all tuning (~16.9 s per cutoff,
  ~0.56 s per trial) vs **7.0 s total** for all refits (~1.06 s each).
- **the 12x ratio** — 84.4 / 7.0. Measured.
- **the ~100x figure** — arithmetic, NOT measured: 200 trials x 0.56 s ~ 110 s
  against ~1 s to refit. A projection from the measured per-trial cost. It must
  be labelled as such wherever it appears.

### How many trials would be necessary? Unknown, and this design cannot say.

30 is demonstrably too few: five seeds returned num_leaves 74, 99, 110, 114,
116 (F21). A converged search returns approximately the same optimum regardless
of seed; this one does not, so it has not converged.

But raising the trial count does not fix the underlying problem. The inner
validation set is **95 rows -- a single month**. More trials search harder
against a target too small to distinguish a genuinely better configuration from
a lucky one, so the extra compute buys precision on a noisy estimate.

**What this experiment CAN support:**
- the cost ratio (a timing measurement, noise-independent)
- that refit is not *detectably* worse at this data scale
- that hyperparameter tuning on a one-month validation window is unstable --
  itself a legitimate Ch6 caveat

**What it CANNOT support:**
- that re-tuning is worse (retracted, F21)
- an optimal trial count
- any accuracy ranking finer than ~4pp, the observed seed-only spread

**To answer the trial-count question properly** would need a multi-month rolling
inner validation, several seeds per configuration, and a convergence check
(does best-value plateau as trials increase). That is a genuine SRQ1 sub-study.
It is NOT required to justify refit-on-stored-params, which stands on cost
alone.

## F25 — the "what do we do about noisy tuning" problem was already solved by srq1_benchmark_cv.py

Brian: *"What is the alternative? just leaving trials at 30?! How many trials do
we have in our current model training that we did before we served the trained
models? Also 30?!"*

**No -- production tuning uses 100 trials with expanding-window CV.** My
refit-vs-retune test used a weaker setup than the project's own, which is a flaw
in my test, not in the pipeline.

| | my F19 test | `srq1_benchmark_cv.py` (production) |
|---|---|---|
| trials | 30 | **100** |
| validation | single 95-row month | **expanding-window time-series CV, 4 folds** |
| objectives | wMAPE only | wMAPE **and** medMAPE |
| convergence evidence | none | **`cv_convergence.csv`, 1,600 rows** |

`srq1_benchmark_cv.py`'s own docstring anticipated exactly this critique ("an
examiner asking 'how many trials, and did you cross-validate?' would get a weak
answer") and fixed it, citing Hyndman & Athanasopoulos §5.10 and Tashman (2000)
for rolling-origin evaluation, and Bergstra et al. (2011) for TPE.

### The answer to "how many trials" is empirical, and already recorded

The docstring's position is correct and worth quoting in Ch3/Ch6:

> **There is no citable "correct" number of trials.** Any source claiming one is
> being misread: the requirement depends on the search space.

So the budget is justified by **convergence evidence** instead. Trial at which
the running best comes within 1% of its final value, from `cv_convergence.csv`:

| category | model | wMAPE plateau | medMAPE plateau |
|---|---|---|---|
| CSD | LightGBM | 58 | 34 |
| CSD | XGBoost | 83 | 43 |
| RTD | LightGBM | 69 | 44 |
| RTD | XGBoost | 21 | 54 |
| danskvand | LightGBM | 52 | 82 |
| danskvand | XGBoost | 74 | 87 |
| energidrikke | LightGBM | 74 | 70 |
| energidrikke | XGBoost | 66 | 51 |

Worst case plateaus at **trial 87 of 100**. So 100 is justified by evidence --
enough for every configuration to converge, with headroom -- and this is a
stronger argument than citing a convention. **That is the answer to "what are we
supposed to do": nothing. It is already done, and done well.**

### Consequence for F19/F21

My test's instability (seeds giving num_leaves 74-116) is now explained: 30
trials against a single month is roughly a third of the budget that the
convergence curve shows is needed, evaluated on a fold design the project had
already rejected as under-powered. **The instability was an artefact of my
harness, not a property of the pipeline.** F21's retraction stands and is
reinforced -- that comparison should not be cited for anything but the cost
ratio.

## F26 — Brian's arithmetic on the re-tune cost is correct

Brian: *"realistically we could test only 1 cutoff ... and increase the number of
trials to way above 30 ... and then it would only take half the total time e.g.
40 seconds, as before you summed and did not average."*

Correct on every step. 84.4 s was 5 cutoffs summed. An on-demand retrain faces
**one** cutoff -- the month being predicted -- so the relevant figure is the
per-cutoff cost, ~16.9 s at 30 trials (~0.56 s/trial).

Scaling to a defensible budget on a single cutoff:

| trials | est. time (single cutoff) |
|---|---|
| 30 | ~17 s |
| 60 | ~34 s |
| **100** (production, convergence-justified) | **~56 s** |

Against ~1 s for a refit that is ~56x, not 12x -- but on a single cutoff the
absolute number is under a minute, which is a very different proposition from
the "84 s" figure I kept quoting without saying it was a sum.

**So per-query re-tuning is NOT obviously infeasible**, and the earlier framing
("re-tuning is dead") was wrong on the arithmetic as well as on the accuracy
(F21). A ~56 s re-tune is slow for an interactive agent but plausible for an
overnight or on-demand-with-progress workflow.

Note the estimate ignores that CV multiplies cost by fold count; the honest
figure needs measuring, not extrapolating -- see task 21.

## F27 — RED FLAG (Brian's catch): the served models use the WEAKER tuning, and cv_params.json is orphaned

Brian: *"why the fuck is it not in sync? Isnt that a red flag? The real training
sounds way more sophisticated and should propagate to the stored parameters, why
is that not the case?"*

**It is a red flag, and he is right.** Verified:

| file | written | method | consumed by |
|---|---|---|---|
| `tuned_params.json` | **2026-08-19 20:11** | 30 trials, single validation split, wMAPE only | **`train_and_persist.py:208`** -> the served models; `training_report.py`; `srq1_profiling.py` |
| `cv_params.json` | **2026-08-24 20:13** | **100 trials, 4-fold expanding-window CV, wMAPE + medMAPE** | **nothing** -- reported only |

`srq1_benchmark_cv.py` was written specifically to fix the three weaknesses of
`srq1_benchmark_tuned.py` (its docstring says so, citing P0040 F58). It ran five
days later, produced better hyperparameters with convergence evidence, and its
output was **never propagated into training**. Every served model, every SRQ4
scenario using `forecast_demand`, and the profiling table are all built on the
30-trial single-split parameters the project itself had already judged
"methodologically correct but under-powered".

Divergence on CSD/LightGBM is not cosmetic:

| param | tuned_params (served) | cv_params (better method) |
|---|---|---|
| n_estimators | 1192 | 374 |
| num_leaves | 63 | 120 |
| min_child_samples | 5 | 14 |
| colsample_bytree | 0.867 | 0.641 |

A 3x difference in tree count and a 2x difference in leaves. These are different
models, not variants.

### Why this happened (not an excuse, a mechanism)

The two scripts write to different filenames. Nothing reads `cv_params.json`, so
nothing broke, no test failed, and no error surfaced. The CV script's outputs are
named `cv_*` throughout (`cv_metrics.csv`, `cv_summary.md`, `cv_params.json`),
which reads as "an additional analysis" rather than "the replacement". The
handover note (`2026-08-19_preprocessing-pipeline-handover-enrico.md:256`) also
flags that `tuned_params.json` predated the EDA-corrected data -- a *second*
staleness problem on the same file, already known and also unresolved.

### Consequences to state plainly

1. **SRQ1's reported best-model selection may not match the served model.** Ch6
   reports CV results; the artefact uses the older params.
2. **The profiling table (F1) profiled the served config**, so its RAM/time
   figures describe what is actually deployed. That is the right choice for a
   deployment claim, but it must not be presented as profiling "the tuned model"
   without saying which tuning.
3. **My F19 refit test used `tuned_params.json`** -- so it compared a 30-trial
   stored config against a fresh 30-trial search. Both arms were under-powered.
   This further weakens F19 (already retracted in F21) but does not affect the
   cost measurements.

### Recommendation -- needs Brian's decision, do not act unilaterally

**Option A (preferred): repoint training at `cv_params.json` and re-persist.**
The CV params are better by the project's own stated criteria and carry
convergence evidence justifying the budget. Cost: re-run `train_and_persist.py`
(free, minutes) and re-run profiling. Risk: every downstream SRQ4 number was
produced against the old models, so results referencing `forecast_demand` output
would need regenerating -- which collides with the P0042 frozen design if blocks
have already run.

**Option B: keep the served params, and say so explicitly.** Document that the
served artefact uses the 30-trial config while Ch6 reports the CV study, and
justify it as "the deployed model was frozen before the CV study completed".
Honest but weak, and an examiner may well ask why the better parameters were
computed and then not used.

**Timing matters:** if blocks 1-3 have NOT yet run, Option A is nearly free and
clearly correct. Once they run against the current models, switching invalidates
them. **This should be settled before spending the API budget.**

## F28 — MEASURED (task 21): a single-cutoff re-tune at production settings costs 417 s, not 56 s

F26 accepted Brian's arithmetic and projected ~56 s for a 100-trial single-cutoff
re-tune. **Measured, that projection was 7x too low**, because it ignored that
expanding-window CV multiplies every trial by the fold count.

Single cutoff (2026-06, 3,040 train rows -> 95 predicted), CSD/LightGBM:

| operation | time | peak RSS | test wMAPE | ratio |
|---|---|---|---|---|
| **refit on stored params** | **2.93 s** | 35.0 MB | **12.57%** | 1x |
| re-tune, 30 trials x 4-fold CV | 107.9 s | 86.6 MB | 15.27% | **37x** |
| re-tune, 100 trials x 4-fold CV | **417.3 s** | 65.3 MB | 16.77% | **142x** |

`04_thesis_results/srq1/retune_single_cutoff.csv`.

**Every projection I made about re-tuning cost was wrong, in both directions.**
The 12x from F19 was too low (it compared a no-CV search); the ~100x from F20
was arithmetic that happened to land near the true 142x for the wrong reason;
the ~56 s in F26 was 7x optimistic. Only this measurement should be cited.

**On accuracy, note the direction:** the re-tuned models scored *worse* on the
held-out month (15.27% and 16.77% vs 12.57%). Per F21 this must NOT be read as
"re-tuning is worse" -- a single cutoff with ~4pp of seed noise cannot support
that. It does, however, mean there is no evidence anywhere in this project that
re-tuning per query buys accuracy.

### What this settles

**Per-query re-tuning is infeasible for an interactive agent**, now on a
measured basis: 7 minutes per query at the production tuning design, versus 3
seconds to refit. That is the number that justifies DEC-REFIT-NOT-RETUNE, and it
does not depend on any accuracy claim.

The refit arm (G) remains viable: 2.93 s and 35.0 MB, comfortably inside the
measured 4 GB sandbox (~0.9%).

**Caveat:** measured on one category, one model, one cutoff. The 142x is a
cost ratio at *this* data scale; it will grow with more data since CV cost scales
with both folds and rows.

## F29 — Option A executed, and it surfaced a second, worse defect: selection on the test set

Brian chose Option A. `train_and_persist.py` now reads `cv_params.json`
(100 trials, 4-fold expanding CV) with `tuned_params.json` retained as a
fallback so a missing entry degrades rather than crashes.

Repointing `best_model_for()` exposed a defect worse than the stale params.
The old selection was:

```python
t = pd.read_csv("tuned_metrics.csv")
r = t.sort_values("test_wmape").iloc[0]      # <-- the TEST set
```

**The served model was chosen by ranking candidates on the held-out test set** --
the same data the thesis then reports that model's performance against. That is
selection on test, and it optimistically biases every downstream number that
flows from the served model, including SRQ4's Scenario C.

`cv_metrics.csv` carries `cv_score`, the expanding-window validation score, which
never touches test. Selection now uses it, so the test set is genuinely held out.

### What changed in the artefact

| category | old (test_wmape) | new (cv_score) | model changed |
|---|---|---|---|
| CSD | XGBoost 14.87% | XGBoost 16.05% | no |
| danskvand | XGBoost 19.96% | XGBoost 17.07% | no |
| energidrikke | XGBoost 14.25% | XGBoost 10.56% | no |
| **RTD** | **XGBoost 33.63%** | **LightGBM 27.92%** | **YES** |

Re-persisted successfully; RTD is now LightGBM. Note the two score columns are
not comparable (test vs CV) -- only the *selection* is being compared.

The RTD flip matters: had selection been unbiased from the start, RTD would
always have served LightGBM. Any SRQ4 result citing RTD's served model was built
on a model chosen by peeking at test.

### Honest caveat

`cv_metrics.csv` also reports `test_wmape`, and for CSD/LightGBM it is 14.54%
against the served config's 15.59% -- so the CV params also look better on test.
That comparison is offered as corroboration only; it is not what selection uses,
and must not become a new justification for selecting on test.

## F30 — `train_and_persist.py` leaves orphaned model files when the selected model changes format

Re-persisting after the RTD flip (XGBoost -> LightGBM) left two stale artefacts:

```
orphaned (not referenced by index.json):
  RTD_model.json            <- the old XGBoost model
  danskvand_model.joblib    <- from some earlier flip
```

XGBoost persists to `.json`, LightGBM/Ridge to `.joblib`, and the writer never
removes the previous file when the format changes. `index.json` is authoritative
and pointed correctly (`RTD -> RTD_model.joblib`), so serving was never wrong --
but a stale `RTD_model.json` sitting beside the live model is a trap for anyone
globbing the directory or loading by convention rather than through the index.

Both removed. **Not fixed in code** -- the writer should prune non-referenced
`{cat}_model.*` files after writing the index, and that is a small change worth
making before the next flip silently recreates the situation.

## F31 — MEASURED (task 22): parameter drift over 7 months is INCONCLUSIVE, and honestly so

Brian: *"technically the refitting would drift eventually when we keep on using
non re-tuned parameters, lets say if we are 8 months outside of the current train
period, wouldnt the saved parameters at some point drift?"*

The right question, and nothing measured before it addressed it -- every earlier
cutoff sat within ~5 months of the tuning window, so a slow decay was invisible
by construction.

Design: tune ONCE on data through 2025-12 (2,470 rows, 20 trials x 2-fold CV,
81 s), freeze those params (`num_leaves=93, n_est=435`), then walk 7 months
forward. At each month, refit on frozen params vs refit on freshly-tuned params;
gap = frozen - fresh, so positive means the frozen params are worse.

| months out | target | frozen | fresh | gap (pp) | fresh num_leaves |
|---|---|---|---|---|---|
| 1 | 2026-01 | 15.10% | 15.10% | 0.00 | 93 |
| 2 | 2026-02 | 19.78% | 20.46% | **-0.69** | 66 |
| 3 | 2026-03 | 17.00% | 16.42% | +0.58 | 57 |
| 4 | 2026-04 | 6.83% | 10.57% | **-3.74** | 16 |
| 5 | 2026-05 | 11.44% | 11.44% | 0.00 | 93 |
| 6 | 2026-06 | 15.28% | 15.28% | 0.00 | 93 |
| 7 | 2026-07 | 17.56% | 13.96% | **+3.60** | 74 |

`04_thesis_results/srq1/param_drift.csv`.

**Mean gap -0.04pp. Correlation with distance +0.42, slope +0.414 pp/month.**

### Why this does NOT establish drift, despite the positive slope

Three reasons, and all three should be stated rather than the slope quoted alone:

1. **The mean gap is essentially zero (-0.04pp)** across 7 months. If frozen
   params decayed, the average would be positive.
2. **The slope is driven by one point.** Month 7 (+3.60pp) and month 4 (-3.74pp)
   are near-equal and opposite. Remove either and the trend reverses. A +0.42
   correlation on n=7 with two dominating outliers is not evidence.
3. **Three months show a gap of exactly 0.00pp** because re-tuning *rediscovered
   num_leaves=93* -- the frozen value. On those months the two arms are the same
   model, so they are not independent observations of anything.

The fresh `num_leaves` sequence (93, 66, 57, 16, 93, 93, 74) is the same
instability documented in F21: the search is not converging on a stable optimum
at 20 trials, so "freshly tuned" is partly a random draw. Measuring frozen-vs-
fresh when fresh is itself noisy cannot resolve a slow drift.

### What can honestly be said

- **No detectable decay over 7 months** at this data scale. The frozen params
  neither clearly degrade nor clearly hold; the experiment lacks the power to
  separate them.
- The thesis should state this as a **limitation and a future-work item**, not
  as a validated property in either direction.
- Brian's concern remains **theoretically sound and untested at the horizon that
  matters**. 46 months of data caps the probe at ~8 months of distance; a
  production system runs for years. The honest position is that per-query refit
  is validated on cost (F28: 2.93 s vs 417 s, 142x) and that a **periodic
  re-tune cadence is prudent but unquantified**.

### Recommended design consequence

Refit per query; re-tune **on a schedule** (e.g. quarterly) rather than never or
per-query. This is defensible without the drift measurement: at 417 s a
quarterly re-tune is trivially affordable, and it removes the unbounded-drift
risk that this experiment could not rule out. Ch9 should say the cadence was not
empirically optimised.

**Do not cite the +0.414 pp/month slope.** It is an artefact of two outliers on
seven points.
