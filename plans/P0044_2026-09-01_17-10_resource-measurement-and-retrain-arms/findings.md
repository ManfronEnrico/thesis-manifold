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
