---
name: 2026-08-19_srq4-experiment-handover-enrico
description: HANDOVER - SRQ4 rebuilt on OpenAI as three scenarios, first paid results in, and six defects found that changed numbers. What to read, what to decide, what to re-run.
category: reference
applies-to: [03_thesis_modelling, 04_thesis_results, 05_thesis_writing]
triggers: [handover, srq4, scenarios, enrico, what changed]
created: 2026_08_19-22_00
updated: 2026_08_19-22_00
---

# Handover — SRQ4 rebuilt and first results (2026-08-19)

**For:** Enrico
**From:** Brian
**Covers:** 25 commits, `855d418` → `30303c8`

> **Read the 2026-08-19 preprocessing handover first** if you have not — it covers
> the pipeline rebuild this sits on top of. This document assumes it.
> One correction to it up front: **the SRQ4 harness now runs on OpenAI
> `gpt-5.5-2026-04-23`, not Claude.** DEC-LLM already said gpt-5.5; the harness
> was the thing that had drifted.

---

## TL;DR

**SRQ4 ran for real and produced a result.** Scenario C (trained model as a tool)
beat Scenario B (LLM writes its own code) on every run of both brands, returned
an *identical* number every time where B varied, and cost 39x less at 22x lower
latency.

But six defects were found on the way there, and **four of them changed numbers**:

1. Hyperparameters were tuned on **pre-EDA data** with a different feature set.
   Re-tuning improved danskvand by **12.6pp**.
2. Scenario C's prediction intervals were **3.9x too narrow** — same
   calibration bug as P0037 F10, present in a second copy of the code.
3. `srq1_benchmark_tuned.py` raised `NameError` and **could not run at all**,
   which is why the stale parameters were never regenerated.
4. Ridge was scoring 446–7392% WMAPE — **not a baseline, noise**. Fixed, and it
   changed the SRQ1 model-selection story.
5. All six Scenario A runs answered in **DKK, not units** — a prompt confound.
6. Training, serving and synthesis each had **their own copy** of the training
   code, which is how (2) got fixed in one place and survived in another.

**Nothing about the preprocessing pipeline changed today.** All six sit in the
modelling and serving layers.

---

## 1. The experiment, as it now stands

### Three scenarios, not two

Renamed from "arms", and the lettering now runs weakest to strongest:

| | Data access | Mechanism | Isolates |
|---|---|---|---|
| **A_plain** | none (web search only) | its own judgement | what the LLM knows without firm data |
| **B_data** | brand history in a sandbox | writes + runs its own Python | what **data access** buys |
| **C_model** | history behind a `forecast_demand` tool | calls the tool, writes no code | what **model integration** adds |

`A → B` measures data access. `B → C` measures the thesis artefact.

**Why three.** A two-scenario B-vs-C design cannot separate "having the data"
from "having a trained model on the data", and a reviewer can then attribute the
whole effect to data access. With three, the increments are attributable —
and on HARBOE they are **+17.8pp** (A→B) and **+3.5pp** (B→C). Most of the value
is data access. That is worth stating plainly rather than burying.

### Where everything lives

```
03_thesis_modelling/
  model_training/            SRQ1 — trains and persists. Nothing else trains.
    train_and_persist.py       fits once, writes models + metadata
    training_report.py         transparency report, generated from data
    srq1/                      benchmark, tuning, calibration, SHAP, profiling
  model_serving_interface/   SRQ2 — the structured tool interface
    scenario_c_forecast/       loads persisted models, never fits
  scenario_setup/            SRQ4 — runs scenarios and logs them
    prompts.py                 every prompt, in one auditable place
    srq4_experiment.py         the harness
    verify_setup.py            free pre-flight (10 checks)
    inspect_runs.py            read back any run
```

The folders map one-to-one onto research questions. That is the test for where a
new script belongs.

---

## 2. First paid results

18 runs, $3.44. Raw logs in `04_thesis_results/srq4/`.

### B vs C — every observation

| Brand | Scenario | rep 0 | rep 1 | rep 2 | APE |
|---|---|---:|---:|---:|---|
| COCA COLA | B | 3,427,000 | 3,448,467 | 3,459,436 | 8.7 / 9.4 / 9.7% |
| COCA COLA | **C** | **3,105,464** | **3,105,464** | **3,105,464** | **1.5% ×3** |
| HARBOE | B | 3,600,000 | 3,950,000 | 3,950,000 | 24.7 / 17.3 / 17.3% |
| HARBOE | **C** | **4,117,982** | **4,117,982** | **4,117,982** | **13.8% ×3** |

C wins every run of both brands; C's *worst* beats B's *best* on both.

**Consistency is the strongest result.** C returned the identical number 6/6. On
HARBOE, B's spread (3.60M–3.95M) is **wider than C's entire error**. This needs
no confidence interval — determinism is a property, not an estimate.

**An earlier single-run comparison had B ahead.** It reversed completely at three
repeats. Worth reporting: direct evidence that single-run LLM comparisons are
unreliable.

**B is not a straw man.** 9–16 code blocks per run, ensembling seasonal-naïve,
month-of-year averages and log-trend regressions with expanding-window
backtesting. C beats a serious effort.

### Cost, and where it goes

| | prompt sent | input **billed** | ratio | output | reasoning |
|---|---:|---:|---:|---:|---:|
| B | ~547 tok | 11,568 | **21×** | 6,547 | 6,314 (**96%**) |
| C | ~97 tok | 576 | 5.9× | 134 | 21 (16%) |

The input multiplier is **the tool loop, not a long prompt**: B's conversation is
re-sent once per tool round, each round carrying the CSV plus all prior code and
output. Input grows roughly quadratically in rounds.

This is what code-as-action *costs*, not an inefficiency to apologise for. An
agent that re-derives a method per query pays for it every time; an agent calling
a trained model pays once at training and amortises across every query after.

---

## 3. The six defects, and which numbers moved

### 3.1 Hyperparameters were tuned on pre-EDA data ← **the big one**

| artefact | timestamp |
|---|---|
| `tuned_params.json` | **2026-08-11 17:55** |
| feature matrices | **2026-08-18 22:59** |

The 2026-08-11 tuning script declared `holiday_month` and
`weighted_distribution`. Neither exists in the current matrix — the first was
renamed `peak_month`, the second deliberately dropped from model inputs. Column
discovery silently skipped both, so **tuning ran on 12 features while the model
trains on 13**.

Re-tuned on current data:

| Category | stale | re-tuned | delta |
|---|---:|---:|---:|
| CSD | 17.1% | **14.9%** | −2.2pp |
| danskvand | 32.6% | **20.0%** | **−12.6pp** |
| energidrikke | 14.9% | **14.3%** | −0.6pp |
| RTD | 31.8% | 33.6% | +1.8pp |

**Any SRQ1 figure from before today should be re-derived.** The table in §3 of the
previous handover is superseded.

### 3.2 It had never been caught because the script crashed

`srq1_benchmark_tuned.py` raised `NameError: name 'fm' is not defined` on its
first call to `tune()` — the column-discovery refactor left
`available_features(fm)` inside a function that never received `fm`. Fixed.

`optuna` was also missing from `requirements.txt`, so the script could not have
run on a fresh machine regardless. Added, with `joblib`.

### 3.3 Scenario C's intervals were 3.9x too narrow

`_eval_forecast` fit on train+val and then measured residuals on **val** — rows
the model had memorised. Same defect P0037 F10 fixed in `forecast_service.py`,
alive in a second copy.

| | a 4.30M forecast |
|---|---|
| before | [3.17M … 5.84M], "Moderate" |
| **honest** | **[1.30M … 11.97M], "Low"** |

Corrected widths (3.0 / 11.6 / 5.5 / 2.8× the forecast) now match P0037 F11
independently.

### 3.4 Ridge was noise, not a baseline

446% / 7392% / 2669% / 1121% WMAPE. Volume features are in **raw units** while
the target is **log**, so a linear model must approximate a logarithm with a
straight line and extrapolates catastrophically — on danskvand it predicted
**1.9 billion units** against 3.85M actual. Trees are invariant to monotone
feature transforms, so only Ridge broke.

Fixed by log-scaling volume columns for linear models: 21.9 / 19.2 / 20.8 /
57.3%. **This changed an SRQ1 claim** — Ridge briefly beat tuned XGBoost on
danskvand, until re-tuning (3.1) restored XGBoost.

### 3.5 Scenario A answered in DKK

All six runs returned currency, not units — 145,000,000 DKK for Coca Cola
against a 3,152,932 *unit* actual, scored as a 4500% error. The model was not
hallucinating; ~145M DKK is a plausible monthly value. It answered the question
asked.

B and C were immune because they infer the unit from the data handed to them. So
an ambiguous question hit exactly the scenario with no data, making its measured
accuracy an artefact of wording.

Fixed to *"How many units of X will be sold …? Answer in units sold, not
currency."* Re-run: all runs in units, error 570% → 35.1%.

**This belongs in the methodology** as evidence that prompt equivalence across
scenarios is a real control.

### 3.6 Three copies of the training code

`forecast_service.build_service()`, `srq4_experiment._eval_forecast()` and
`srq2_synthesis.py` each trained their own models — the last of them **on
import**, so `import srq2_synthesis` silently triggered a full training pass.

That duplication is how 3.3 got fixed in one place and survived in another.
Training now happens once in `train_and_persist.py`; serving loads. Second and
later tool calls serve in **0.037 s** against ~1.1 s of retraining.

---

## 4. What I need from you

### 4.1 DEC-VENDOR — settled, please confirm

`gpt-5.5-2026-04-23` for all three scenarios. Your DEC-LLM reasoning (it is the
production model of the agent Scenario B represents) still holds; the harness had
drifted to Claude and is now aligned. Pinned to the **dated snapshot** so it
cannot silently re-point.

Deliberately not moving to GPT-5.6: changing the base model changes coding
competence and tool-use reliability, which are the mechanisms producing the
between-scenario difference.

### 4.2 The LLM judge — dropped

Every SRQ4 metric is programmatic. The judge only covered qualitative dimensions
("clarity", "actionability") that are **not in the research question**, and a
defensible judge protocol needs cross-family selection, blinding, order
randomisation and human-validated agreement statistics. That is a lot of work
defending a measurement that does not answer the question.

**Consequence**: the "judge must be another family" constraint in your
OPEN-PARAMS table no longer applies.

### 4.3 The prompt set — replaced

Your ~50-prompt / 6-archetype taxonomy is superseded for SRQ4 by **a single
prediction template across brands**. Roughly 34 of the 50 involve no forecasting
at all, and on those Scenario C's tool is irrelevant — both scenarios do
identical work, diluting the effect across two-thirds of the sample.

Your prompt CSVs are **now committed** (`.gitignore` had a blanket `*.csv` rule,
so they existed on one machine only). They are in
`03_thesis_modelling/.archive/prompts_srq2_2026-08/` with a README. Two things
to know if SRQ2/SRQ3 revisits them: the pilot is 15 *distinct* queries across 9
archetypes, and every prompt is **chain-level** — the grain DEC-GRAIN deleted.

### 4.4 Budget

$7 spent today, balance now **negative**. From measured per-run costs:

| Scenario | cost/run | latency |
|---|---:|---:|
| A_plain | $0.4243 | 100 s |
| B_data | $0.2664 | 114 s |
| C_model | **$0.0068** | **5 s** |
| **one full ladder observation** | **$0.697** | ~220 s |

**$50 buys ~71 full ladder observations (213 calls).** Recommended:
**5 brands × 10 repeats × 3 scenarios ≈ $35**. That satisfies the sizing (B's CV
is 2.67%, so n=10 gives a ±1.9% CI on its mean) and widens the cross-section
from 2 brands to 5.

Scenario C is ~1% of the total. **You are almost entirely paying for the two
comparison scenarios** — itself worth a sentence in the cost discussion.

---

## 5. Running it yourself

```bash
# free — 10 checks, no API calls
python 03_thesis_modelling/scenario_setup/verify_setup.py

# see what a run would cost before spending
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --full \
    --brands "COCA COLA" --categories CSD --scenarios A --repeats 3 --dry-run

# the real thing, with a hard spend cap
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --full \
    --repeats 3 --brands-per-cat 2 --budget 5 --out 04_thesis_results/srq4

# read back what happened
python 03_thesis_modelling/scenario_setup/inspect_runs.py --all
```

**Always pass `--budget`.** Per-run cost varies ~60x between scenarios, so a
pre-run projection is not a safeguard.

**Use `--brands` for partial re-runs.** `--brands-per-cat` counts from the
highest-volume brand down, so it repeats work already paid for — that is how
$0.90 was spent today re-running HARBOE while trying to collect Coca Cola.

Other flags: `--categories`, `--rep-offset` (extend a run without overwriting),
`--list-brands`, `--scenarios A,B,C`.

---

## 6. Open items

| Item | State |
|---|---|
| Coca Cola Scenario A | **unmeasured** — credits ran out. ~$1.27 with `--brands` |
| Scenario C re-run on the re-tuned model | ~$0.04. CSD moves 15.6→15.1%, so direction is unaffected, but the exact figures in `run_2026-08-19_dkk-confound/` are superseded |
| RTD | degrades under tuning (31.8→33.6%). **Not a bug**: val→test correlation is −0.096, so validation carries no signal there. Do not re-tune — report as a limitation |
| Ensemble | inverse-WMAPE ensemble of XGBoost/LightGBM/Ridge beats the single best model in **3 of 4** categories and recovers most of RTD's loss. Recommended as the next iteration, benchmarked in SRQ1 first — **not** bolted onto the tool before a paid run |
| `tuned_params.json` reproducibility | future runs are reproducible now that `optuna` is pinned; the pre-2026-08-19 values are not recoverable |

---

## 7. Where to read more

| What | Where |
|---|---|
| Results + what can/cannot be claimed | `04_thesis_results/srq4/RESULTS_2026-08-19.md` |
| Interpretation for the write-up | `05_thesis_writing/notes/srq4-first-results-and-interpretation.md` |
| Why the design is shaped this way | `05_thesis_writing/notes/srq4-experiment-design-rationale.md` |
| Findings F10–F21 (the audit trail) | `plans/P0039_2026-08-19_01-45_srq4-system-a-vs-b/findings.md` |
| How the models were trained | `04_thesis_results/srq1/training_report.md` (generated, re-runnable) |
| Your decisions, annotated | `user-docs/handovers/2026-07-13_harness-and-srq4-decisions-handover-brian.md` §"Brian's Decisions" |
