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
