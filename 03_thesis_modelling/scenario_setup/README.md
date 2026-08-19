---
name: scenario_setup-readme
description: RULE - What lives in scenario_setup, how the three SRQ4 scenarios are configured and run, where every prompt is defined, and what is logged per run.
category: reference
applies-to: [03_thesis_modelling, srq4]
triggers: [running the SRQ4 experiment, inspecting scenario logs, auditing prompts, checking leakage controls]
created: 2026_08_19-16_00
updated: 2026_08_19-16_00
---

# `scenario_setup/` — SRQ4 scenario testing and logging

This folder holds **everything concerned with running the three-scenario SRQ4
comparison and recording what happened.** It is deliberately separate from its
two neighbours:

| Folder | Concern |
|--------|---------|
| `model_training/` | training the ML/statistical models (SRQ1 benchmarks, tuning, calibration, SHAP) |
| `model_serving/` | making a trained model reachable — the forecast service behind Scenario C's tool |
| `scenario_setup/` | **this folder** — running scenarios against those models and logging the results |

---

## Files

| File | Purpose |
|------|---------|
| `prompts.py` | **Every prompt, in one auditable place.** Templates + the tool schema. No prompt text is defined anywhere else. |
| `srq4_experiment.py` | The experiment harness: three scenarios, failure taxonomy, cost logging, budget cap |
| `inspect_runs.py` | Read back what a run did — prompts, generated code, tool calls, leakage flags |
| `verify_setup.py` | Pre-flight check: credentials, model access, data integrity, leakage guards |
| `srq4_tier2.py` | Tier-2 prompt work (pre-existing, not yet revised for the 2026-08-19 design) |

---

## The three scenarios

One variable under test: **how the agent produces a forecast.** The scenarios form an
*information ladder*, so two increments can be attributed separately:

| Scenario | Data access | Mechanism | Isolates |
|-----|-------------|-----------|----------|
| `A_plain` | open web only | the LLM's own judgement | what the LLM knows without firm data |
| `B_data` | brand history in a sandbox | writes + runs its own Python | what **data access** buys |
| `C_model` | history behind a tool | calls `forecast_demand` | what **model integration** adds |

`A -> B` measures data access. `B -> C` measures the thesis artefact.

---

## How Scenario C actually reaches the trained model

This is the part worth being precise about, because it is easy to assume the LLM
"has" the model. It does not.

```
  prompt  ->  LLM  ->  emits {"category": "CSD", "brand": "HARBOE"}
                            |
                            v
              OUR CODE intercepts the call
                            |
                            v
              _eval_forecast() loads the H=3 feature matrix,
              fits tuned XGBoost on train+val, predicts the test row
                            |
                            v
              JSON handed back  ->  LLM interprets it in prose
```

The LLM sees **only** the function name, a two-string schema, and a description.
It never loads a model, never sees a feature, never runs code. Its arguments are
its own choice — which is why they are logged and checked against what was
requested (`args_match_request`).

**The scored number is the tool's, not the LLM's prose.** `tool_forecast` is
authoritative, so a model that misquotes the figure in its answer is still
credited with the model's output. Accuracy measures the forecasting model;
prose fidelity is a separate question.

---

## Running it

```bash
# Pre-flight: credentials, model reachability, data + leakage checks. Free.
python 03_thesis_modelling/scenario_setup/verify_setup.py

# Smoke test: one brand through all three scenarios, no repeats (~$0.30)
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --demo

# One scenario only
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --demo --scenarios A

# The full experiment, with a hard spend cap
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --full \
    --repeats 5 --budget 40
```

**Always pass `--budget`.** Per-run cost varies ~45x between scenarios (Scenario C ~$0.006,
Scenario B ~$0.25), so a pre-run projection is not a safeguard. The cap stops
mid-run; partial results are already on disk from the per-brand checkpoint.

---

## What is logged, and where

Per run, `04_thesis_results/srq4/raw_responses/{scenario}__{category}_{brand}__rep{n}.json`:

| Field | Why it is kept |
|-------|----------------|
| `prompt` | the exact text sent — reproducibility |
| `detail.tool_schema` | what the LLM was offered |
| `detail.tool_calls` | **the arguments the LLM chose**, with `args_match_request` |
| `detail.tool_outputs` | what the model returned, including confidence tier and training cutoff |
| `detail.code_blocks` | **every block of code Scenario B wrote** — qualitative evidence |
| `detail.reasoning` | reasoning summaries where the API exposes them |
| `detail.web_queries` | what Scenario A searched for |
| `tokens_*`, `cost_usd_est` | cost, with reasoning tokens broken out |
| `trace` | model, decoding, reasoning effort, target month, scenario-specific flags |

Plus `runs.csv` (one row per run) and `summary.md` (aggregates + cost
reconciliation against the billing endpoint).

**Why this matters:** paid, non-deterministic runs cannot be reproduced. The
same prompt will not return the same reasoning or the same generated code.
Anything not written down at run time is gone.

---

## Leakage controls

The held-out period is **2026-01 to 2026-07 — in the past** relative to the run
date. Two risks a forward-looking design would not have:

**Scenario B** receives `train`+`val` only. `_assert_no_leakage()` hard-fails if the
target month ever appears in the history handed to a scenario, or if that history
runs to or past the target. A silent leak would not raise an error — it would
produce an impressively accurate Scenario B, which is the exact quantity being
measured.

**Scenario A** could in principle retrieve a published figure for a past month. It is
instructed to estimate rather than retrieve, and every run records
`retrieval_suspected` (does the answer cite the target month?) and `used_web`.
**A mitigation, not a guarantee** — documented as a limitation. The residual bias
is conservative: retrieval would make Scenario A look better, shrinking the measured
value of data access.

**All scenarios are scored on the same named month**, derived from the data and
passed in explicitly. Scenario A previously received "next month", which it anchored
on the wall-clock date — scoring a different month than B and C.

---

## Configuration

Frozen constants at the top of `srq4_experiment.py`:

| Constant | Value | Note |
|----------|-------|------|
| `MODEL` | `gpt-5.5-2026-04-23` | dated snapshot, not the floating alias |
| `REASONING_EFFORT` | `medium` | API default, stated explicitly |
| `TEMPERATURE` | `None` | **not settable** — the model rejects it, see below |
| `PRICE_IN/OUT_PER_M` | 5.00 / 30.00 | verified against actual billing |

**Decoding cannot be controlled.** `gpt-5.5` rejects both `temperature` and
`top_p` with HTTP 400. All scenarios are equally uncontrolled, so the comparison
holds, but the write-up must not claim temperature 0 — consistency is a purely
measured outcome.

Credentials come from `03_thesis_modelling/.env`, falling back to the repo-root
`.env`. Two disjoint scopes, both needed:

- `OPENAI_API_KEY` — project key, runs the experiment
- `OPENAI_ADMIN_KEY` — admin key, reads actual billed cost

---

## Related

- `05_thesis_writing/notes/srq4-experiment-design-rationale.md` — why each design decision was taken, and the challenge it must survive
- `plans/P0039_2026-08-19_01-45_srq4-system-a-vs-b/` — execution plan
- `03_thesis_modelling/model_serving/system_a_forecast/forecast_service.py` — the serving layer Scenario C's tool mirrors
