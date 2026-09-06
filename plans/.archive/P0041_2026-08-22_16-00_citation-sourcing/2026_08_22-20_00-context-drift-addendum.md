---
name: context-drift-addendum
description: Corrections to the project-overview and research-question files as of 2026-08-22. Read ALONGSIDE those files; where they conflict, this file is newer.
created: 2026_08_22-18_00
updated: 2026_08_22-20_00
supersedes_as_of: 2026-08-22
---

# Context drift addendum — read with the RQ and overview files

**Purpose.** This recorded nine points where the project-overview and research-question
files had fallen behind the work.

> **UPDATE 2026-08-22 20:00 — SEVEN OF NINE ARE NOW FIXED AT SOURCE.** The RQ files,
> the project overview, and Ch1 §1.3 were corrected directly, so the files you are
> reading no longer carry those errors. Two items were *decisions* rather than errors
> and were resolved (§2, §4).
>
> **This file is now a change log, not a set of live corrections.** It is kept because
> it explains *why* several things read the way they do, and because it names what a
> literature researcher should and should not spend effort on (see the closing
> summary, which remains current).

---

## 1. The two corrections that most affect literature search

### 1.1 LLM-as-Judge has been DROPPED — ✅ fixed at source

The overview and the SRQ4 file both specify *"a separate judge model with bias
awareness + a human-rated subset"*. **This is no longer the design** (decision
B-DEC-2).

All SRQ4 metrics are now **programmatic**: forecast error against held-out actuals,
run-to-run variance, token cost, wall-clock latency. No model judges another model's
output.

**Consequence for research:** LLM-as-judge methodology, judge bias, and human-rating
protocols are **no longer needed**. Do not spend effort there.

### 1.2 Prometheus access has LANDED — ✅ fixed at source

Three files state that Prometheus Graph Engine access is *"pending NDA + dev merge"*
and that SRQ4 was deliberately designed to avoid depending on it.

**The engine was delivered on 2026-08-20.** It is inspected, its environment is
built, and it runs locally. SRQ4 now includes two scenarios that use it directly.

**Consequence:** SRQ3's framing as an *assessment rather than a completed integration*
is now a **scope decision under active review**, not a constraint imposed by lack of
access. See §4.

---

## 2. SRQ4 is now a five-scenario ladder — ✅ fixed, and the RQ WORDING was changed

The RQ files describe SRQ4 as ML integration **vs** a code-as-action LLM baseline —
two arms. The implemented design has **five**, with a sixth under consideration:

| Scenario | Engine | Forecast access |
|----------|--------|-----------------|
| `A_plain` | GPT-5.5 | none |
| `B_data` | GPT-5.5 | code execution (E2B sandbox) |
| `C_model` | GPT-5.5 | `forecast_demand` tool |
| `D_prometheus` | **Prometheus Graph Engine** | none (code-as-action, as shipped) |
| `E_prometheus_model` | **Prometheus Graph Engine** | `forecast_demand` tool |
| `F_ensemble` *(proposed)* | GPT-5.5 | pooled + specialised, with accuracy context |

The design logic is one variable per rung. **`B->C` and `D->E` are the same
intervention applied to two different orchestrators** — an intentional replication,
and the strongest structural feature of the design.

**Consequence for research:** the SRQ4 file's exclusion of "traditional BI as a
baseline" still holds, but the *comparator set* is wider than described. Literature on
tool-augmented LLMs, and on whether LLMs can forecast directly, is more relevant than
the two-arm framing suggests.

---

## 3. Categories: FOUR, not five — ✅ fixed at source

`srq1-models-efficiency.md` §Scope item 5 says *"per-category vs pooled modelling
across the five categories"*. This contradicts the same file's own "what changed"
section and the overview's quick-reference table.

**Correct: four categories** — CSD, Danskvand, Energidrikke, RTD. Totalbeer was
excluded on compute grounds (2026-08-01).

---

## 4. SRQ3's scope — ✅ RESOLVED (middle position)

Both the overview and the SRQ3 file present the assessment framing as partly forced by
pending access. Access has landed, so the question is live:

**Resolved 2026-08-22:** readiness criteria are **derived from a working integration**,
without claiming a completed production deployment.

The deciding observation was that the integration happens regardless — scenario
`E_prometheus_model` *is* `forecast_demand` running inside the Prometheus engine, so
SRQ4 cannot run without it. The only question was whether SRQ3 claims that work as
evidence. Grounding the criteria in what the integration actually depended on is
stronger than architectural analysis alone and costs no extra work.

Explicitly **not** claimed: operational hardening, monitoring at scale, organisational
adoption.

**Research on both integration-readiness models and completed ML-into-production
integrations remains useful** — the middle position draws on both literatures.

---

## 5. SRQ1's answer set has grown

### 5.1 The model ladder is six benchmarks, not two families

The overview's gap G2 names *"ARIMA / Prophet / LightGBM / XGBoost / Ridge"*. As of
2026-08-22 the comparison also includes **naive, seasonal-naive and drift** — the
standard benchmark set (Hyndman & Athanasopoulos; M-competitions).

This matters for the gap claim: a benchmark study that omits the standard floor is
conventionally treated as unbenchmarked, so their addition **strengthens** G2 rather
than diluting it.

### 5.2 The pooled-vs-per-category question now has an answer

SRQ1's third leg (*"does a per-category model beat a single pooled model?"*) was
unanswered until 2026-08-21 — the results file had no pooled row. It now does:

> Neither strategy dominates. Specialisation pays only where a category has enough
> history; below that a pooled model borrowing cross-category structure is more
> accurate. On this dataset the crossover sits between roughly 750 and 1000
> brand-month training observations. The sign flips once, at the same place, for both
> model families.

**This is the finding most in need of literature support** — see citation register
entry C4 (global vs local forecasting models). It is currently presented as if novel.

### 5.3 A benchmark beats the tuned models on one category

On RTD, **seasonal-naive (27.3% WMAPE) beats every tuned model** (35.1-37.0%). This
is the M4 finding reproduced on this data and will be reported, not buried.

---

## 6. Accuracy targets in the overview are not met as stated

The quick-reference table gives **MAPE target ≤ 15%** and **≥ 85% empirical coverage**
of 90% intervals.

Measured: best tuned models reach **12-17% WMAPE** on three categories and **~35% on
RTD**. Median MAPE is considerably higher throughout (30-50%).

The ≤15% target is met only on some categories and only on the volume-weighted metric.
**The targets need restating with the metric named**, or they will read as unmet.

**A recurring finding worth knowing:** WMAPE (volume-weighted) and median MAPE
(per-series) **disagree repeatedly** in this project — three separate analyses found
the same split. Any accuracy claim must name its metric.

---

## 7. The RAM budget figure is not yet defensible

The overview states a **≤ 8 GB RAM** constraint, and `generate_figures.py::fig4_ram_budget`
is **entirely hardcoded**, including a literal 512 MB "active ML model".

**Measured footprint of the served model: 3-4 MB.** The figure cannot ship as-is.

The honest version is stronger than the invented one: *the trained model is the cheap
part; the agent runtime is where the budget goes.* This supports rather than weakens
the deployment argument, and it becomes measurable now that the Prometheus engine runs
locally.

---

## 8. The SRQ2 interface has grown since it was specified

The SRQ2 file describes the artefact as *"point forecast, calibrated 90% interval,
confidence score, source attribution and traceability metadata"*. Still true, plus:

- **Both accuracy metrics** (WMAPE and median MAPE) for the served model
- **Both baselines** — best-by-WMAPE and best-by-medMAPE, which can be different
  models pointing in opposite directions
- A **`metrics_disagree`** flag when the two comparisons contradict
- **`"n/a"` substitution** for implausible values, so a failed model's error rate
  cannot reach the agent as a number

**An interface principle emerged that belongs in SRQ2's contribution:** *an interface
should not serve a number it cannot vouch for, however much caveat text accompanies
it.*

**A caution for the write-up:** the `confidence` score is a **heuristic index** with
hand-chosen weights and tier cutoffs. It is not a calibrated probability and has no
literature definition. See citation register Group 5.

---

## 9. Path renamed — ✅ fixed at source

`03_thesis_modelling/model_serving/` was renamed **`model_serving_interface/`** on
2026-08-19, to name SRQ2's "Structured Tool Interface" explicitly. The overview §6
still uses the old path.

---

## Summary for a literature researcher

**Do not research:** LLM-as-judge methodology (dropped).

**Research with higher priority than the RQ files imply:**
- Global vs local (pooled vs per-series) forecasting models — §5.2
- Conformal prediction, especially for time series — §8
- Tool-augmented LLMs for quantitative tasks — §2
- Whether LLMs can forecast time series directly — §2
- Context length and LLM performance degradation — relevant to the proposed
  `F_ensemble` and context-depth experiments
- Forecast accuracy metrics: WMAPE, MAPE failure modes, robust alternatives — §6
