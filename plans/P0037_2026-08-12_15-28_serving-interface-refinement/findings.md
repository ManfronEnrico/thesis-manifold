---
pid: P0037
created: 2026-08-12 15:28:00
updated: 2026-08-12 15:28:00
status: in_progress
---

# Findings — Serving Interface Refinement

Investigation of `03_thesis_modelling/model_serving/` against (a) the ChatGPT
serving analysis pasted by Brian, and (b) the thesis's own SRQ2 scope and the
Ch5/Ch7 rationale note.

---

## F1 — `model_serving/` is nearly empty; the real serving code lives in `model_training/`

`03_thesis_modelling/model_serving/` contains exactly two Python files:

| Path | Lines | What it is |
|---|---|---|
| `system_a_forecast/forecast_service.py` | 135 | The dedicated-model layer (trains + writes a forecast lookup) |
| `system_b_conversational/generate_systemB_diagram.py` | ~13 KB | **A diagram generator, not a service.** System B has no serving code at all |

Meanwhile the *actual* agent/tool-interface code — the thing SRQ2 is about — sits in
`03_thesis_modelling/model_training/`:

- `srq2_agent.py` — synthesis agent + LLM-as-judge
- `srq2_synthesis.py` — deterministic multi-model synthesis core
- `srq4_experiment.py` — **contains the only real `forecast_demand` tool schema and
  the Claude function-calling loop** (System A vs System B code-as-action)

Per `.claude/rules/repo-tier-structure.md`, the split is meant to be train-vs-serve:
"does this train something, or does it run something already trained?" By that test
`srq4_experiment.py`'s `run_system_a` / `run_system_b` and the tool schema are
**serving** code sitting in the training folder. `generate_systemB_diagram.py` is a
figure generator and is neither — it belongs with the Ch5/Ch7 figure tooling.

**Consequence:** the folder a reader (or examiner) opens to find "the SRQ2 artefact"
is the one folder that does not contain it.

---

## F2 — `srq4_experiment.py` has a broken import of `forecast_service.py`

```python
_spec = importlib.util.spec_from_file_location(
    "fs", Path(__file__).resolve().parent / "forecast_service.py")
```

`Path(__file__).parent` is `model_training/`. `forecast_service.py` does **not** exist
there — verified, `ls` returns "No such file or directory". It lives in
`model_serving/system_a_forecast/`. This is P0035 restructure fallout: the file moved,
the importer did not follow.

The module-level `exec_module` call means `srq4_experiment.py` raises on **import**,
not at first use. **The SRQ4 experiment harness cannot currently run at all.**

Mitigating detail: `run_system_a` does not actually call `fs.*` — it calls the local
`_eval_forecast()`. So the import is *both* broken and unused. Two options (see
task_plan): repoint it, or drop it.

---

## F3 — The `fs` import being unused reveals a real duplication

`srq4_experiment.py` defines its own `_eval_forecast()` which re-implements
`forecast_service.build_service()`'s modelling: same FEATURES list, same tuned-params
load, same XGBoost, same log-space conformal interval. Three files now carry a
byte-similar copy of the 14-element `FEATURES` list and the `SELECTED`/`CAT_FILE`
category map:

- `model_serving/system_a_forecast/forecast_service.py`
- `model_training/srq4_experiment.py`
- `model_training/srq2_synthesis.py`

The divergence is not cosmetic — the two conformal calibrations differ (see F5).

**However** — the duplication is not purely accidental. `_eval_forecast` trains on
train+val and predicts the held-out test month (evaluation mode, for a fair comparison
against System B), whereas `build_service` trains on *all* observed data and predicts
one step beyond the data (deployment mode). That is a legitimate distinction. What is
wrong is that it is implemented by copy-paste rather than by one function with a
`fit_scope` parameter.

---

## F4 — `forecasts.csv` has never been built

`build_service()` writes `model_serving/system_a_forecast/forecasts.csv`, and
`forecast_demand()` reads it. The file is absent from disk. So the *one* function in
`model_serving/` that matches the SRQ2 artefact description — the typed callable the
agent tool wraps — has never been executed end-to-end, and `forecast_demand()` would
raise `FileNotFoundError` on any call.

Note this is *not* on the SRQ4 path (which uses `_eval_forecast`), which is why it has
gone unnoticed: nothing that currently runs consumes it.

---

## F5 — Two different conformal calibrations, neither documented as a choice

| Function | Residuals used for the 90% quantile |
|---|---|
| `forecast_service.build_service` | **test** split residuals |
| `srq4_experiment._eval_forecast` | **val** split residuals |

`build_service` calibrating on the test split is the more serious of the two: the
interval width is derived from the same held-out data the model's accuracy is reported
on. For a deployment-mode service that predicts beyond all data there is no "test" in
the honest sense — but the pipeline still labels a split `test`, and using it for
calibration is a form of contamination that an examiner reading Ch7 will flag,
especially given the thesis already claims leakage discipline as a strength (rationale
note §7).

`_eval_forecast`'s use of val residuals is correct and should be the pattern.

---

## F6 — The horizon is hard-coded to one month; the thesis's own worked example uses six

This is the single largest gap between the code and the thesis intent.

**Code (all three paths):**
- `forecast_service.forecast_demand` returns `"horizon": "next month"` — a string literal
- The `forecast_demand` tool schema in `srq4_experiment.py` accepts **only**
  `{category, brand}`. There is no horizon parameter
- Tool description: *"Return next-month demand forecast"*
- The feature builder constructs exactly one future row (`nm = lm % 12 + 1`)

**Thesis (rationale note §6), the canonical worked example:**
```
User: "What will Faxe Kondi sales be in 4 months?"
{"tool": "forecast_demand", "brand": "FAXE KONDI", "horizon_months": 4}
```

**Brian's session question** asks about a 6-month horizon.

So the documented SRQ2 artefact has a `horizon_months` parameter that the implemented
tool does not have. Anyone reading §6 and then the code finds a contract mismatch.

This is also where the ChatGPT analysis is most right and most load-bearing (see F8).

---

## F7 — Tool output is missing the traceability fields SRQ2 explicitly requires

SRQ2 scope names the artefact as *"a typed tool call carrying point forecast,
calibrated 90% interval, confidence score, source attribution and traceability
metadata."* Against `forecast_demand`'s actual return:

| SRQ2-required field | Present? |
|---|---|
| point forecast | ✅ `forecast_units` |
| calibrated 90% interval | ✅ `interval_90` |
| confidence score | ✅ `confidence` + `tier` |
| source attribution | ⚠️ partial — `model: "XGBoost(tuned)"`, no version/run id |
| **traceability metadata** | ❌ **absent** |
| **data cutoff / window** | ❌ **absent** |
| **target period (absolute)** | ❌ absent — only the relative string `"next month"` |

The rationale note's own example return carries `"data_window": "2022-04..2025-11"`.
The code returns nothing equivalent. Since SRQ2's three named design properties are
reliability, uncertainty, and **traceability**, and traceability is the one with zero
implementation, this is the highest-value gap for the thesis contribution itself —
independent of the horizon question.

---

## F8 — Verification of the ChatGPT analysis

Assessed claim by claim against this repo. Broadly correct, with two errors and one
under-specification.

### Correct, and matches existing thesis intent

| Claim | Verdict |
|---|---|
| Model needs all 12 (here: **14**) features at serving time; the *user* need not supply them | ✅ Correct, and already the thesis's §6 position |
| LLM extracts intent/identifiers only; backend builds the feature vector | ✅ Correct — this *is* the SRQ2 contribution, already written |
| Three feature categories (known-in-advance / derived-from-past / unknown-future) | ✅ Sound framing, and useful — the repo has no equivalent taxonomy written down |
| Return should carry interval, data cutoff, assumptions | ✅ Correct, and F7 shows it is missing |
| Target date should anchor to last Nielsen observation, not `today` | ✅ **Correct and important.** Code currently derives the next month from the data (`lm % 12 + 1`), which is the right anchor, but never *reports* it, so the caller cannot tell |
| LLM should not invent missing numerical variables | ✅ Correct |

### Errors

1. **"12 features"** — the actual count is **14**, and the list is fixed in three
   places (`FEATURES`, F3). Minor, but the thesis must state the real number.

2. **The feature taxonomy is wrong for *this* model.** ChatGPT lists "Future-known:
   planned promotion or price" and "Future-unknown: competitor sales/price" as separate
   sources. In this pipeline `promo_intensity` is neither — it is `shift(1)`-lagged
   precisely *because* using contemporaneous promo was found to be target leakage
   (rationale note §7, defect V3). So at serving time promo is a **derived-from-past**
   feature, not a future-known one. Adopting ChatGPT's taxonomy uncritically would
   reintroduce the exact leakage the thesis claims credit for fixing.

### Under-specified — the real difficulty ChatGPT skips

ChatGPT says the horizon question is one of *interpreting* "6 months" (Feb 2027 vs Nov
2026). That is the easy half. The hard half it does not mention:

**The model is trained one-step-ahead. It cannot do h=6 in one call.** `lag_1` for
month t+6 is the *unobserved* value at t+5. Producing a 6-month forecast requires one
of:

| Strategy | Cost |
|---|---|
| **Recursive** — feed each prediction back as the next `lag_1` | Error compounds; the conformal interval calibrated for h=1 is **invalid** for h=6 |
| **Direct multi-horizon** — train a separate model per h | Retraining; ~44-month panel gets shorter per horizon |
| **Restrict** — cap the tool at short horizons and say so | Cheapest, honest, but narrows the demo |

The rationale note §9 already flags exactly this for `n_skus_active` ("at a 6-month
horizon the auto-derived value is the last observed SKU count carried forward six
months, and its accuracy degrades with horizon"), so the project has *seen* the problem
for one feature without generalising it to the horizon design as a whole.

**This is the decision the session must actually make.** Everything else is
implementation.

---

## F9 — What is genuinely good and should not be disturbed

To keep the plan honest — the existing design gets several things right that the
ChatGPT analysis proposes as if new:

- Server-side feature construction with the LLM never touching feature vectors is
  already the documented and implemented position
- The System A tool description already instructs *"do not compute yourself"* — a
  correct reliability guard
- SRQ4's comparison is well-constructed: same model, same temp, same prompts, only the
  forecast-production mechanism varies; `_eval_forecast` deliberately matches System B's
  train+val/test split for fairness
- `_tar()` implements a cited total-agreement-rate consistency metric (Atil et al. 2025)
- Deployment mode vs evaluation mode is a real and correct distinction (F3)

---

## F10 — conformal intervals were 4.4x too narrow (task 7 FIXED)

Worse than the plan recorded. `build_service` fitted on **all** of `d`
(train+val+test) and then measured residuals on the **test** rows. Both halves were
wrong and they compounded: the residuals were **in-sample**, because the model had
already seen those rows while fitting.

So the interval measured how well the model recalled its own training data, not how
well it generalises — and it did so on the split reserved for reporting accuracy.

**Fixed**: fit a calibration model on **train**, take the 90th percentile of
|residual| on **val**, leave test untouched. The served model still trains on
everything (withholding data from the deployed model would waste it for no gain);
only the calibration is out-of-sample.

**Measured effect on CSD:**

| | q90 (log units) | a 10,000-unit forecast becomes |
|--|---:|---|
| old (fit-all, calib-test) | 0.2739 | [7,604 .. 13,151] |
| **new (fit-train, calib-val)** | **1.2032** | **[3,002 .. 33,309]** |

**4.4x wider.** Anyone acting on the old interval was badly overconfident.

## F11 — the honest intervals are very wide, and that is a result

With calibration fixed, **all 230 series report `Low` confidence**, and the median
90% interval spans **3.0x the forecast** (Danskvand 11.6x, Energidrikke 5.5x, RTD
2.8x).

This is not a bug to tune away. It is the truthful uncertainty of monthly brand-level
demand forecasting on 29-46 months of history, and the old numbers only looked
respectable because they were calibrated against memorised data.

**It matters for SRQ4.** If System A's headline contribution is "a dedicated model
gives you a number plus a trustworthy interval", the interval being 3x the forecast
is part of the honest answer. It also gives System B a fairer fight: an LLM writing
its own code is not competing against a precision the dedicated model does not have.

Worth stating plainly in the results chapter rather than buried — a reviewer who
finds wide intervals reported openly trusts the rest more, not less.

## F12 — traceability implemented (task 4)

SRQ2 defines traceability as "a recorded mapping from tool call -> forecast value ->
recommendation" and the tool returned none of it. Every `forecast_demand()` response
now carries a `trace` block:

| Field | Question it answers |
|-------|---------------------|
| `model_id`, `model_version` | which artifact do I re-run to reproduce this? |
| `trained_through` | newest month it could have learned from |
| `observed_through` | newest month this brand actually has |
| `calibration_split` | what were the intervals calibrated on? (`val`) |
| `interval_method` | `split_conformal_90` |
| `feature_count` | how many features this category supports |
| `generated_utc` | how stale is this answer? |

Provenance is recorded **per series**, not per service: brands differ in history
depth, so "what did the model see" is a per-brand fact. A service-level answer would
be a comforting average rather than the truth for the brand asked about.

**Terminology, for the write-up** (Brian asked; his colleague's usage was correct):

| Term | Question | Status |
|------|----------|--------|
| **traceability** | where did this number come from? | **now implemented** — SRQ2's actual claim |
| **transparency / interpretability** | *why* this number? | XGBoost is a black box; SHAP approximates it |
| **determinism** | same input -> same output? | already true (fixed seed, temp 0) |

## F13 — serving and training disagreed on the feature list (found by running it)

`build_service` fitted with `available_features()` (13 columns for CSD) but built the
prediction frame from the module-level hardcoded `FEATURES`. XGBoost rejected it:
`feature_names mismatch ... training data did not have the following fields:
promo_intensity`.

The divergence appears precisely where a category lacks a capability — Danskvand and
RTD have no `promo_intensity`, so `available_features()` drops it at fit time while
the hardcoded list still constructs it at predict time.

Also removed a stale `feat["weighted_distribution"] = ...` line: that column does not
exist (it is `weighted_dist`) and was dropped from model inputs on 2026-08-19.

**Serving now mirrors training exactly.** `build_service()` runs end to end: **230
forecasts across 4 categories** (CSD 95, Danskvand 29, Energidrikke 44, RTD 62).

Tasks 3, 4 and 7 are delivered. The remaining blocker is the missing `.env`.

