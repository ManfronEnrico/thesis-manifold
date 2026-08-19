---
pid: P0039
created: 2026-08-19 01:45:00
updated: 2026-08-19 02:05:00
---

# P0039 Findings

## F1 — the harness is further along than the plan files implied

`03_thesis_modelling/scenario_setup/srq4_experiment.py` already implements the full
experiment. Read before assuming anything needs building:

- `run_system_a()` — Claude calls `forecast_demand`, backed by the trained XGBoost
- `run_system_b()` — Claude gets `df` in an E2B sandbox and must write its own code
- Both record forecast, input/output tokens, latency
- Both loop up to 8 tool-use rounds
- System B parses a `FORECAST=<number>` sentinel from stdout

The design is clean and single-variable. **What it lacks is execution, not
conception.**

## F2 — the only blocker is credentials

`srq4_experiment.py` line 28 reads `ROOT/.env` for `ANTHROPIC_API_KEY` and
`E2B_API_KEY`. The file is gitignored and absent, so the module raises
`FileNotFoundError` on import.

`forecast_service.py` imports cleanly and `build_service()` runs, so System A's backing
is in place. Nothing else about SRQ4 can be verified until `.env` exists.

## F3 — what E2B is, and what drives its cost

E2B is a disposable cloud sandbox. System B's answer only exists if the model's
self-written code actually *runs*; E2B is where it runs without touching a real
machine. System A does not need it, and **that asymmetry is the experiment**.

Billing is by sandbox uptime (per-second while alive), not per call, with a free tier
that likely covers this workload.

Cost drivers visible in `run_system_b()`:

| Step | Note |
|------|------|
| `Sandbox.create()` | per-run container |
| `pip install statsmodels` | **re-downloaded every single run** — likely the largest fixed cost |
| data load + up to 8 tool rounds | the variable part |
| `sbx.kill()` | ends billing |

If the run count reaches the hundreds, an E2B template with packages pre-installed
removes the repeated install. Not worth doing below that.

## F4 — the vendor choice has no recorded justification

Searched `01_thesis_research/research-questions/` and `00_thesis_context/`. The model
is a hardcoded constant (`MODEL = "claude-sonnet-4-6"`, line 36) with a price comment
and **no argued basis anywhere**.

This is a genuine gap: a reviewer asking "why this model?" currently has no answer in
the thesis.

See DEC-VENDOR in `task_plan.md` for the options. The short version: decide on
**ecological validity** ("this is what firms deploy"), which is both defensible and
reportable. Budget is a real constraint but governs *sample size*, not vendor choice —
see F7, which measures it and corrects the framing here.

## F5 — terminology: traceability vs transparency vs determinism

Brian asked whether "traceability" was the right word, wondering if his colleague meant
something else. **The word is correct** — SRQ2 defines it precisely as *"a recorded
mapping from tool call → forecast value → recommendation"*.

What Brian described (deterministic, non-black-box) is a different property. All three
are separate and worth keeping distinct in the write-up:

| Term | Question | Status here |
|------|----------|-------------|
| **traceability** | where did this number come from? | **implemented** 2026-08-19 (P0037 F12) |
| **transparency / interpretability** | *why* this number? | XGBoost is a black box; SHAP approximates it |
| **determinism** | same input → same output? | already true: fixed seed, temperature 0 |

Only traceability is claimed by SRQ2, and it is now the one that is built.

## F6 — the honest intervals reshape what System A can claim

From P0037 F10/F11: once conformal calibration was moved off test residuals, all 230
served forecasts report `Low` confidence and the median 90% interval spans **3× the
forecast** (Danskvand 11.6×, Energidrikke 5.5×, CSD 3.0×, RTD 2.8×).

**Consequence for this experiment**: "System A is more accurate" is a weak thesis, and
possibly a losing one. The strong version is that System A returns a number *with*
calibrated uncertainty *and* provenance, neither of which self-written code can
produce.

This also makes the comparison fairer — System B is no longer competing against a
precision System A does not actually have.

## F7 — API cost is not the deciding factor at this scale (corrects F4's framing)

Brian clarified (2026-08-19) that the cost point was an **internal budget constraint**,
not a reported argument — the API is paid out of pocket, and ~50 prompts are planned
per system to get a stable estimate from non-deterministic responses.

That is a legitimate constraint and normal to disclose. It is also a different claim
from "pick a weaker model so the result looks better", which was never the intent.
F4's framing conflated the two.

**Measured, the constraint turns out to be small.** Order-of-magnitude from the
harness' own token structure, 50 runs per system (100 conversations):

| Model | System A | System B | Total |
|-------|---------:|---------:|------:|
| claude-sonnet-4-6 | $1.05 | $6.38 | **~$7** |
| GPT-5.x class | $0.59 | $3.50 | **~$4** |
| GPT-5-mini class | $0.12 | $0.70 | **~$1** |

Even at 10x, the vendor difference is tens of euros. **So cost should not decide
DEC-VENDOR** — ecological validity should. Cost governs a different question: how many
runs are affordable, which is a sample-size decision and belongs in the methodology as
a stated limit.

**Where the money actually goes**: System B costs ~6x System A per run. It loops
through several tool-use rounds carrying the brand's history in context and re-installs
statsmodels per sandbox, where System A makes a single tool call. If the design grows,
System B is the line item to watch — and an E2B template with packages pre-installed
is the first optimisation.

Real per-run figures come from `--demo` (task 1). The harness already computes cost
per run via `PRICE_IN_PER_M` / `PRICE_OUT_PER_M`, so if the vendor changes, **update
those constants** or every reported cost will be wrong.


## F8 — the blocker was three problems, not one; two are now fixed

F2 said "the only blocker is credentials". That was true of the *symptom* but not
the cause: the `FileNotFoundError` on import masked two further defects that only
became visible once it was cleared. Fixed 2026-08-19 (commit `63c8a6c`):

| # | Defect | Why it was invisible |
|---|--------|----------------------|
| 1 | `.env` read was unguarded and hard-failed on import | it *was* the visible error |
| 2 | `forecast_service.py` path stale since the P0028 train-vs-serve split — the file lives in `model_serving/`, the harness looked beside itself | masked by #1 |
| 3 | `anthropic` and `e2b-code-interpreter` absent from `requirements.txt` **and** from the environment | both imported lazily *inside* the run functions, so they fail mid-run, not at import |

Defect 3 is the same failure mode as the ML block fixed 2026-08-18: a dependency the
code needs, missing from the manifest, hidden behind a lazy import. Worth treating as
a pattern in this repo rather than three coincidences.

**Now verified without any credentials**: the module imports, and
`_eval_forecast("CSD", "HARBOE")` returns
`forecast_units=4,326,970` with a 90% interval of `[3,259,384 – 5,744,233]`.
System A's forecasting core is sound; the remaining blocker is genuinely
credentials alone.

**Caveat on that number**: the interval is roughly ±30%, far tighter than the
median 3x reported in F6/P0037 F11. HARBOE is a large, stable brand. Do **not**
quote it as representative — F6's median is the honest headline figure.

## F9 — the ANTHROPIC_API_KEY in the repo-root .env is an empty placeholder

The root `.env` contains the literal line `ANTHROPIC_API_KEY=` with no value. A
`grep` for the key name finds it and looks like a working credential; it is not.

Two consequences:

1. **The env loader now skips empty values.** Otherwise `setdefault` locks in the
   empty string and a genuinely exported key can never override it, turning a clear
   auth failure into a confusing one.
2. **The handover's claim needs qualifying.** It tells Enrico he "probably already
   has" an Anthropic key because he built System B. If his `.env` carries the same
   placeholder, that is optimistic. He should check for a *value*, not a key name.

`E2B_API_KEY` is absent entirely from both files.

## F10 — Scenario A cannot retrieve the answer, tested adversarially

The held-out months are historical, so Scenario A could in principle look up the
figure instead of estimating it. Tested directly rather than assumed: the model
was asked point-blank to *find* the Nielsen-reported January 2026 unit sales for
a named brand, with web search enabled.

It searched and returned **NOT FOUND**. What it surfaced instead were
annual-report aggregates citing NIQ ("Danish soft drinks +2.6%, FMCG incl. HD,
W16 2026") — category-level growth rates, not brand-level monthly units.

**Why**: Nielsen scanner data is a paid commercial product. Brand x month unit
sales are not published anywhere the model can reach.

**Consequence for the design**: the "do NOT search for a published figure"
instruction was removed from Scenario A's prompt. It was doing no work, and it
made A's prompt structurally different from B's and C's, which is a confound.
`used_web`, the search queries and `retrieval_suspected` are still logged every
run, so the claim rests on evidence rather than on the model obeying an
instruction.

State this in the limitations as a *tested* control, not an assumed one.

## F11 — the prompts were not equivalent; now they are

Found by reading the logged prompts rather than the code. The three scenarios
were receiving materially different instructions:

- A: the question + a paragraph forbidding search
- B: the question + method guidance + the CSV
- C: one bare sentence

Any measured accuracy difference therefore partly reflected **prompt wording**,
not the mechanism under test — which is precisely what the single-variable
design exists to exclude.

Rewritten so all three receive the **same user question verbatim**:

> What will {brand} sell in the {category} category in Danish retail in
> {target}? Give the number, a range, and how confident you are.

Only the capability note differs, and that note *is* the treatment: A is told it
has no internal data, B is given the history and told to run code, C is told a
`forecast_demand` tool exists and not to compute the number itself.

"Do not compute it yourself" is retained for C and must be disclosed: without
it the model may ignore the tool and hand-compute, collapsing C into B.

## F12 — Scenario B's advantage did not replicate; its inconsistency is the finding

Three runs, identical prompt and brand (CSD/HARBOE, target 2026-01):

| Run | B forecast | B's chosen method | B APE | C APE |
|-----|-----------:|-------------------|------:|------:|
| 1 | 4,009,826 | inverse-RMSE ensemble of ETS + regression | 16.1% | 17.5% |
| 2 | 4,143,790 | rolling-origin ensemble, ETS + month/trend | 13.3% | 17.5% |
| 3 | 3,931,319 | log-linear OLS with monthly seasonality | 17.7% | 17.5% |

**Scenario C returned 3,943,859.8 every single time.**

The logs show B genuinely tries hard — ExponentialSmoothing, SARIMAX, ARIMA, OLS
and Ridge appear across its generated code, with rolling-origin backtesting and
inverse-RMSE ensembling. It is not doing something naive.

But it **selects a different model on each run**, and the spread (3.93M–4.14M,
~5%) is comparable to the accuracy gap being measured. The earlier "B beats C"
reading was run-to-run variance in an n=1 sample, not a better method.

This is the consistency metric appearing early, and it favours C on grounds that
survive B occasionally winning on accuracy:

| | Scenario B | Scenario C |
|---|---|---|
| Same answer twice? | no | yes, identical |
| Method | varies per run | fixed, recorded |
| Cost per run | ~$0.27 | ~$0.007 (~40x cheaper) |
| Latency | ~143 s | ~6.6 s (~22x faster) |
| Provenance | none | model, training cutoff, calibration split |

**Do not over-read n=3.** The point is that the design now measures the right
thing; the scaled run settles the magnitude.

## F13 — compute cost is measured in the serving path, not only offline

The thesis claims these models run in a compute-limited environment (~8 GB per
query), so `_eval_forecast` now records peak RAM and wall-clock for the code path
actually used at serve time: **~3-4 MB and ~1.1 s** per forecast, against an 8 GB
budget — about 0.05%.

Offline profiling (`srq1_profiling.py`) independently reports peak fit RAM of
5.5 MB (Ridge), 8.0 MB (LightGBM), 0.1 MB (XGBoost), 0.3 MB (ARIMA).

`tracemalloc` measures Python allocations only, so both figures are lower bounds
on the Python side; they are directly comparable to each other because they
measure the same quantity the same way. Say so rather than implying a total
process footprint.

**Scenarios A and B log no RAM, correctly**: their computation happens on
OpenAI's infrastructure and is already priced into the token and container
charges. There is no local process to measure, and inventing one would be
guesswork. The honest cross-scenario compute comparison is therefore
**cost and latency**, both of which are measured — with the asymmetry itself
being a finding, since C's compute is ours to control and B's is not.

## F14 — the served models are correct; verified independently

Prompted by a fair concern: two portability bugs (an unpicklable Ridge pipeline,
a loader that assumed every model was an XGBoost booster) raised the question of
whether the models were ever trained or served correctly at all.

**They are.** Scored the *loaded, served* model against the full held-out test
split and compared with what SRQ1 reported:

| Category | served | SRQ1 | delta |
|----------|-------:|-----:|------:|
| CSD | 15.6% | 17.1% | -1.5pp |
| danskvand | 18.2% | 19.2% | -1.0pp |
| energidrikke | 15.7% | 14.9% | +0.7pp |
| RTD | 36.7% | 31.8% | **+4.9pp** |

The two are *expected* to differ: `srq1_benchmark.py` fits **train only with
default hyperparameters** (it is a model-ranking ladder), while
`train_and_persist.py` fits **train+val with tuned hyperparameters** (it is the
deployed model). Decomposing both factors:

| Category | default/train | default/train+val | tuned/train | tuned/train+val |
|----------|-------------:|------------------:|------------:|----------------:|
| CSD | 17.1% | 15.5% | 16.8% | **15.3%** |
| danskvand | 32.6% | 20.4% | 29.5% | **17.7%** |
| energidrikke | 14.9% | 15.2% | 19.8% | **14.6%** |
| RTD | 31.8% | 33.4% | 32.5% | **38.1%** |

Three categories behave as designed: more data and tuning both help, and the
served configuration is the best of the four.

## F15 — RTD degrades under tuning and extra data

RTD is the exception and it is not a bug. Going from default/train (31.8%) to
tuned/train+val (38.1%) makes it **6.3pp worse**, and both factors hurt
independently (+1.6pp from extra data, +0.7pp from tuning, +4.0pp interacting).

The likely mechanism, consistent with the other evidence: RTD has the shortest
validation window and the widest spread of small volatile brands. Optuna tuned
against a 372-row validation set that does not represent the test period, so the
configuration it chose is fitted to a window that has passed.

**Consequences:**

1. **Do not report RTD's served accuracy as SRQ1's number.** They measure
   different configurations and differ by 4.9pp.
2. **Scenario C serves the worse model for RTD.** Defensible only if the
   selection rule is stated *in advance* -- "we serve the tuned model refit on
   train+val" -- and the RTD outcome is reported as a limitation. Switching RTD
   to the default configuration *after seeing* the test result would be fitting
   the selection rule to the evaluation set, which is the same error as tuning
   on test.
3. **Worth stating positively**: tuning that helps three categories and hurts a
   fourth is an honest result about hyperparameter transfer under short
   histories, and it belongs in the limitations rather than being smoothed away.

RTD is not in the SRQ4 scenario set (CSD is primary), so this does not affect the
experiment -- but it must not be misquoted in the SRQ1 chapter.

## F16 — an ensemble beats the single best model in 3 of 4 categories

The ensemble idea from the archived `srq2_synthesis.py` was dismissed too
quickly on cost grounds. Tested directly, all three models fitted on train+val
and scored on the held-out test split:

| Category | XGBoost | LightGBM | Ridge | ensemble (equal) | ensemble (inv-WMAPE) |
|----------|--------:|---------:|------:|-----------------:|---------------------:|
| CSD | 15.3% | 15.2% | 19.4% | **14.2%** | **14.2%** |
| danskvand | 17.7% | 21.4% | 18.2% | 16.0% | **15.6%** |
| energidrikke | **14.6%** | 33.4% | 20.0% | 15.3% | 16.8% |
| RTD | 38.1% | 33.6% | 56.2% | 33.3% | **33.2%** |

The weighted ensemble wins in three categories, and on RTD it recovers most of
the degradation recorded in F15 (38.1% -> 33.2%). Only energidrikke prefers the
single model, and there LightGBM is so poor (33.4%) that averaging drags the
result down.

**Cost is not the objection.** Weights come from validation WMAPE, which is
computed once at training time; serving three persisted models is three
`predict()` calls on one row -- microseconds, no extra API cost, and no retraining
at serve time. The original objection was to `srq2_synthesis.py` *retraining on
import*, which is a separate defect and is now fixed by persistence.

**What it would change:**

- Scenario C's payload gains an **inter-model agreement** signal
  (`1 - std/mean` across the three forecasts), which is a genuinely different
  trust dimension from interval width: two models disagreeing is evidence a
  single model's tight interval is overconfident. That is squarely SRQ2's
  "reliability and uncertainty".
- The confidence formula could then legitimately use agreement, which is what
  the archived 30/40/30 formula was doing. It was not arbitrary; it was
  unaffordable only because it retrained.

**What it costs the thesis:** SRQ1's story becomes "we selected a model *and*
found the ensemble better", which is more honest but needs the ensemble
benchmarked properly rather than bolted on.

**Recommendation**: keep the single-model tool for the first paid SRQ4 run so the
pipeline is validated against a simple, already-verified path. Treat the ensemble
as the next iteration, benchmarked in SRQ1 first. Do not bolt it on before the
run -- an untested change to the tool is exactly what a first paid run should not
be testing.

## F17 — how many repeats the consistency claim actually needs

Measured from the three real Scenario B runs (same prompt, same brand):
mean 4,028,312, sd 107,435, **CV 2.67%**.

95% CI half-width on B's mean forecast, by number of repeats:

| n | half-width | as % of mean |
|--:|-----------:|-------------:|
| 3 | +/- 266,883 | 6.63% |
| 5 | +/- 133,398 | 3.31% |
| 10 | +/- 76,854 | 1.91% |
| 20 | +/- 50,281 | 1.25% |
| 30 | +/- 40,117 | 1.00% |
| 50 | +/- 30,533 | 0.76% |

Smallest B-vs-C gap detectable at 80% power, alpha 0.05:

| n | detectable gap |
|--:|---------------:|
| 3 | 8.26% |
| 5 | 4.43% |
| 10 | **2.65%** |
| 20 | 1.76% |
| 30 | 1.41% |

**n=10 is a defensible stopping point, and the answer to "wouldn't we need
hundreds?" is no.** Precision improves as sqrt(n): going 10 -> 40 costs four
times the money to halve the interval. At n=10 the CI is +/-1.9%, which is
comfortably tighter than the effect being discussed.

**The more important point**: the headline consistency claim does not need a CI
at all. Scenario C returned *the identical number* on every run -- that is not a
statistical estimate, it is a property of a deterministic model, and one run
demonstrates it. What the repeats measure is B's spread, and n=10 x 3 brands = 30
observations per scenario is ample for that.

State the design as: **n chosen so the CI on B's mean is under 2%**, which is
n=10, not "as many as we could afford".

## F18 — the tuning procedure is sound; RTD's validation split is the problem

Audited because the tuned hyperparameters were inherited from a colleague's
environment and had never been reproduced here.

**Procedure (`srq1_benchmark_tuned.py`) — correct.** Optuna TPE, seed 42, 30
trials, objective = **validation** WMAPE, best config refit on train+val,
evaluated **once** on test. That is the textbook arrangement: the test split is
touched exactly once, at the end, and never informs a choice.

**Search space — appropriate for gradient boosting.** Six parameters covering the
three things that matter for a small tabular dataset: capacity
(`n_estimators` 200-1200, `max_depth` 3-10, `num_leaves` 15-128 for LightGBM),
step size (`learning_rate` 0.01-0.15, log scale — correct, since learning rate is
multiplicative), and regularisation (`min_child_weight` / `min_child_samples`,
`subsample`, `colsample_bytree` 0.6-1.0).

Two defensible omissions worth stating rather than hiding: no explicit L1/L2
(`reg_alpha`, `reg_lambda`), and no early stopping. Both are partly covered by
the capacity and subsampling ranges. Adding `reg_lambda` would be the first
extension if tuning were revisited.

**The real diagnostic — does validation predict test?** Ran 20 fresh trials per
category and correlated each trial's validation WMAPE against its test WMAPE:

| Category | val rows | corr(val, test) | test of val-best | best test seen |
|----------|---------:|----------------:|-----------------:|---------------:|
| CSD | 665 | **0.918** | 17.2% | 16.6% |
| danskvand | 174 | **0.836** | 32.4% | 29.9% |
| energidrikke | 264 | **0.902** | 14.6% | 13.6% |
| RTD | 372 | **-0.096** | 32.9% | 29.7% |

Three categories show strong positive correlation: choosing on validation
reliably improves test, and the val-best config lands within ~1pp of the best
configuration seen. **The tuning is doing its job.**

RTD's correlation is **-0.096** — statistically indistinguishable from zero.
Validation performance there carries no information about test performance, so
Optuna is optimising a target that does not transfer. This is not a coding error
and not a wrong search space; it is a property of RTD's data.

**Note it is not a sample-size effect**: RTD has 372 validation rows, more than
danskvand's 174, which correlates at 0.836. The likelier cause is a regime change
between RTD's validation window (2025-08..2026-01) and its test window
(2026-02..2026-07) — RTD is the most seasonal category and those windows sit on
opposite sides of the year.

**Consequences:**

1. The tuned parameters are **not** the reason RTD degrades. Even the best
   configuration observed only reaches 29.7% against the default's 31.8% — the
   ceiling is low regardless of tuning.
2. **Do not re-tune RTD hoping for a better number.** With zero val-test
   correlation, any improvement found that way is selection noise.
3. Report RTD as a limitation: short history, strong seasonality, and a
   validation window that does not represent the test period. The ensemble
   (F16) recovers more of it (33.2%) than any tuning did.
4. RTD is not in the SRQ4 scenario set, so this does not affect the experiment.

**Reproducibility gap closed**: `optuna` was never in `requirements.txt`, so
`srq1_benchmark_tuned.py` could not run on a fresh machine and the tuned values
could not be regenerated. Added, with `joblib` (now a hard dependency, since
danskvand serves a Ridge pipeline persisted via joblib).

## F19 — `tuned_params.json` does not reproduce, but the numbers are sound

Tested directly after installing optuna: re-ran CSD/XGBoost tuning with the same
seed (42), the same 30 trials and the same search space.

| | n_estimators | learning_rate | max_depth | min_child_weight | subsample | colsample |
|---|---:|---:|---:|---:|---:|---:|
| stored | 314 | 0.0513 | 9 | 6.53 | 0.644 | 0.923 |
| reproduced | 926 | 0.0888 | 7 | 2.91 | 0.899 | 0.925 |

**Completely different parameters.** Something in the generating environment
differed — a different optuna or xgboost version, a different trial count, or a
different search space at the time. Not recoverable from the artefact.

**But accuracy is nearly identical**: stored 15.32% test WMAPE vs reproduced
14.80%. The loss surface is flat across the plausible region, which is why the
val->test correlation is 0.918 (F18) yet the argmin moves.

**So the choice is narrow, and it is a documentation choice, not a correctness
one:**

- The stored parameters are **not wrong**. They produce a model within 0.5pp of a
  freshly tuned one, and every SRQ4 result so far used them.
- The thesis **cannot claim** these parameters are reproducible from the recorded
  seed, because they are not.

**Recommendation: do not re-tune before submission.** Re-tuning would invalidate
every SRQ4 number collected today for a 0.5pp accuracy change, and the parameters
would still not match the originals. Instead:

1. Keep the stored parameters and state in the methodology that they were
   produced by a documented procedure (Optuna TPE, seed 42, 30 trials, objective
   = validation WMAPE) whose exact environment was not captured.
2. Record the measured evidence that the choice is insensitive: a fresh tuning
   run lands within 0.5pp.
3. `optuna==4.7.0` and `joblib==1.5.2` are now pinned in requirements.txt, so
   **future** tuning is reproducible even though the historical run is not.

If time allows after the writing is done, a clean re-tune plus a full SRQ4 re-run
would close this properly. It is not worth doing with a month left and \$50 of
API budget.

## F20 — where Scenario B's tokens actually go

Asked because B bills ~20x C's input tokens on the same question. Measured on
one run (CSD/HARBOE):

| | prompt sent | input billed | ratio | output | reasoning | code written |
|---|---:|---:|---:|---:|---:|---:|
| B_data | ~547 tok | 11,568 | **21.1x** | 6,547 | 6,314 (96%) | 11 blocks, ~2,600 tok |
| C_model | ~97 tok | 576 | 5.9x | 134 | 21 (16%) | none |

**The input multiplier is the tool loop, not a long prompt.** B's prompt is sent
once but billed once per *tool round*: each of its 11 code executions re-sends the
whole conversation — the CSV, every prior code block, and every prior execution
output. Input tokens therefore grow roughly quadratically in the number of rounds.

**The output is long because the model writes the code.** 6,547 output tokens of
which 6,314 are reasoning: comparing candidate models, backtesting, weighing
ensembles. The ~2,600 tokens of Python are a small part; the thinking dominates.
C's 134 output tokens are one tool call plus a sentence of prose.

**For the write-up**: this is not an implementation inefficiency to apologise for.
It is what code-as-action *costs*. An agent that re-derives a forecasting method
per query pays for that derivation every time, while an agent calling a trained
model pays once at training time and amortises it across every subsequent query.

## F21 — F19 was wrong: the parameters were stale, not irreproducible

**Brian's hypothesis was correct and my F19 explanation was not.** F19 attributed
the non-reproducing hyperparameters to "some environment difference not
recoverable from the artefact". The actual cause is simpler and worse:

| artefact | timestamp |
|----------|-----------|
| `tuned_params.json` | **2026-08-11 17:55** |
| feature matrices | **2026-08-18 22:59** |

Seven days apart, spanning the entire preprocessing rebuild.

**The feature set differed.** The tuning script on 2026-08-11 declared:

```
[..., "holiday_month", "promo_intensity", "weighted_distribution"]
```

Neither `holiday_month` (since renamed `peak_month`) nor `weighted_distribution`
exists in the current matrix. Open-world selection silently dropped both, so the
**tuning ran on 12 features while the served model trains on 13** — and one of
those 12 was a column later removed from model inputs on purpose (P0036 task 7).

So the hyperparameters were optimised for a different dataset *and* a different
feature set than the models they were being applied to.

### Why it had never been caught

`srq1_benchmark_tuned.py` raised `NameError: name 'fm' is not defined` on its
first call to `tune()`. The open-world refactor left `available_features(fm)`
inside a function that never received `fm`. **The script could not run at all**,
which is why `tuned_params.json` was never regenerated — not an environment
quirk, a crash. Fixed: `_load()` now returns the feature list alongside the
split parts.

### Effect of re-tuning on the current data

| Category | stale params | re-tuned | delta |
|----------|-------------:|---------:|------:|
| CSD | 17.1% | **14.9%** | -2.2pp |
| danskvand | 32.6% | **20.0%** | **-12.6pp** |
| energidrikke | 14.9% | **14.3%** | -0.6pp |
| RTD | 31.8% | 33.6% | +1.8pp |

**Danskvand improves by 12.6pp.** F19's claim that re-tuning was not worth doing
because the effect was ~0.5pp was based on CSD alone and does not generalise.

Served-model accuracy, measured independently after retraining:

| Category | now | before | delta |
|----------|----:|-------:|------:|
| CSD | **15.1%** | 15.6% | -0.5pp |
| danskvand | 19.9% | 18.2% | +1.7pp |
| energidrikke | **13.9%** | 15.7% | -1.8pp |
| RTD | **34.6%** | 36.7% | -2.1pp |

### A second defect this exposed: incomparable results files

`metrics.csv` (train-only, **default** params) and `tuned_metrics.csv`
(train+val, **tuned** params) measure different regimes. `best_model_for()` read
only the first, so on danskvand it selected Ridge at 19.2% (untuned, train-only)
over XGBoost at 20.0% (tuned, train+val) — **not the same measurement**.

Selection now reads `tuned_metrics.csv`, with untuned baselines from
`metrics.csv` admitted only on a >10% relative margin, since a narrow win by a
model that never had the benefit of tuning is likely noise. All four categories
now serve tuned XGBoost.

### Consequence for the SRQ4 results collected today

Every SRQ4 number from 2026-08-19 used a Scenario C model built on the stale
parameters. CSD (the experiment category) moves 15.6% -> 15.1%, so the direction
of the B-vs-C comparison is unaffected — but **the exact Scenario C figures in
`run_2026-08-19_dkk-confound/` are superseded** and must be regenerated before
being quoted. The consistency, cost and latency findings are unaffected, since
none of them depends on the model's parameters.

## F22 — the split is applied before warm-up rows are dropped (OPEN decision)

Brian asked whether the 13 warm-up months should be dropped *before* the split is
assigned, so the 70/15/15 holds over the rows that are actually modelled.

**Current behaviour**: `resolve_split_cutoffs()` cuts on the distinct periods
present in the frame, which includes the first 13 months where `lag_13` is null.
Those months are entirely in train, so the split boundary dates are correct as
dates — but the *usable* proportion is not 70/15/15:

| Category | months | usable | current (usable) | if cut on usable only |
|----------|-------:|-------:|------------------|----------------------|
| CSD | 46 | 33 | 19/7/7 = **58/21/21** | 23/5/5 = 70/15/15 |
| danskvand | 41 | 28 | 16/6/6 = 57/21/21 | 20/4/4 = 71/14/14 |
| energidrikke | 43 | 30 | 17/6/7 = 57/20/23 | 21/4/5 = 70/13/17 |
| RTD | 41 | 28 | 16/6/6 = 57/21/21 | 20/4/4 = 71/14/14 |

**Brian's reading is methodologically standard**: feature engineering is part of
preprocessing, and the split is normally struck over the data that survives it.
On that reading the proportion should be measured after the drop.

**The counter-argument, which is why it is not a one-line change:**

1. **Cutting on usable months shrinks val and test to 4-5 months.** At n=4, a
   validation window is one seasonal quarter, and the conformal calibration (F18)
   already showed RTD's val->test correlation collapsing when the windows sit on
   opposite sides of the year. Shorter windows make that worse, not better.
2. **The current split gives MORE evaluation data**, not less: 7 test months
   instead of 5. The "wrong" proportion errs toward a larger held-out set, which
   is conservative with respect to every accuracy claim.
3. **Every number in the thesis so far uses the current split**, including all
   SRQ4 results and the re-tuned hyperparameters. Changing it invalidates them.

**Recommendation: keep the current split and state it precisely.** Say the split
is 70/15/15 **over available months**, note that 13 warm-up months carry no
`lag_13` and fall entirely in train, and give both proportions. That is honest,
costs nothing, and avoids trading 7 test months for 5 in exchange for a rounder
number.

**If it is changed**, it must be changed before any further paid runs, and every
SRQ1 and SRQ4 figure regenerated. It is not worth doing with a month left unless
a supervisor asks for it.
