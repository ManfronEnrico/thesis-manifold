---
name: srq4-first-results-and-interpretation
description: RULE - First paid SRQ4 results (2026-08-19), the information-ladder increments, how to interpret B vs C, why Scenario B's token cost is structural, and what can and cannot be claimed at n=6. Write-up material for Ch8/Ch9/Ch10.
category: reference
applies-to: [ch8-evaluation, ch9-discussion, ch10-limitations]
triggers: [writing SRQ4 results, interpreting B vs C, defending sample size, explaining token cost, writing the discussion]
created: 2026_08_19-20_30
updated: 2026_08_19-20_30
---

# SRQ4 — First Results and How to Read Them

First paid runs, 2026-08-19. Raw data and per-run logs in
`04_thesis_results/srq4/`. **Every number below is measured**, not projected.

---

## 1. The information ladder — HARBOE (actual 4,778,907 units)

| Scenario | mean forecast | median APE | CV across repeats | latency | cost / 3 runs |
|----------|--------------:|-----------:|------------------:|--------:|--------------:|
| **A** plain LLM | 3,166,667 | 35.1% | 3.65% | 108.7 s | $1.482 |
| **B** data + code | 3,833,333 | 17.3% | 5.27% | 115.4 s | $0.830 |
| **C** trained model | 4,117,982 | **13.8%** | **0.00%** | **5.9 s** | **$0.020** |

**Both increments are positive**, which is the whole reason the design has three
scenarios rather than two:

- **A → B — data access: +17.8pp.** Giving the agent the firm's own history
  halves the error.
- **B → C — model integration: +3.5pp.** Exposing a *trained model* on top of the
  same data adds a further gain. **This is the thesis contribution.**

**Write this honestly**: the second increment is smaller than the first. Most of
the measured value comes from data access. A two-scenario design would have
merged the two and let a reviewer attribute the whole effect to data — which is
precisely why Scenario A earns its place.

---

## 2. B vs C — every observation, both brands

| Brand | Scenario | rep 0 | rep 1 | rep 2 | APE |
|-------|----------|------:|------:|------:|-----|
| COCA COLA | B | 3,427,000 | 3,448,467 | 3,459,436 | 8.7 / 9.4 / 9.7% |
| COCA COLA | **C** | **3,105,464** | **3,105,464** | **3,105,464** | **1.5% ×3** |
| HARBOE | B | 3,600,000 | 3,950,000 | 3,950,000 | 24.7 / 17.3 / 17.3% |
| HARBOE | **C** | **4,117,982** | **4,117,982** | **4,117,982** | **13.8% ×3** |

C wins **every single run of both brands**. C's *worst* run beats B's *best* run
on both. Aggregate median APE: **7.7% (C) vs 13.5% (B)**.

### Consistency is the strongest result

C returned the identical number 6 times out of 6. B produced three distinct
values for Coca Cola and two for HARBOE. On HARBOE, **B's spread (3.60M–3.95M)
is wider than C's entire error.**

This needs no confidence interval: determinism is a *property* of a fixed model,
not a statistical estimate, and one repeat demonstrates it. The repeats exist to
measure B's spread, not C's.

### Accuracy — and a caution about early readings

An earlier single-run comparison had B ahead. That reversed completely at three
repeats. **Report that**: it is direct evidence that single-run LLM comparisons
are unreliable, which strengthens the consistency argument rather than
undermining the result.

### B is not a straw man

Across the six runs B ran **9–16 code blocks each**, ensembling seasonal-naïve,
month-of-year averages and log-trend regressions with expanding-window
backtesting. It is doing serious forecasting work. C beats a genuine effort.

### A shared limitation, not a C advantage

Both B and C under-forecast HARBOE (B −19.8%, C −13.8%) while diverging on
Coca Cola (B +9.3%, C −1.5%). Both missing the same brand in the same direction
suggests a real January uplift neither could see from history. Report it as a
shared limitation; do not credit C for it.

---

## 3. Why Scenario B costs ~40× more — the mechanism, measured

| | prompt sent | input billed | ratio | output | reasoning | code written |
|---|---:|---:|---:|---:|---:|---:|
| B_data | ~547 tok | 11,568 | **21.1×** | 6,547 | 6,314 (**96%**) | 11 blocks, ~2,600 tok |
| C_model | ~97 tok | 576 | 5.9× | 134 | 21 (16%) | none |

**Input: the multiplier is the tool loop, not a long prompt.** B's prompt is sent
once but billed once per *tool round*. Each of its 11 code executions re-sends the
entire conversation — the CSV, every prior code block, every prior execution
output. Input tokens grow roughly quadratically in the number of rounds.

**Output: the model writes the code, but the thinking dominates.** 6,547 output
tokens, of which 6,314 are reasoning — comparing candidate models, backtesting,
weighing ensembles. The ~2,600 tokens of Python are the smaller part.

**Frame this as structural, not as an implementation flaw.** It is what
code-as-action costs: an agent that re-derives a forecasting method on every
query pays for that derivation every time. An agent calling a trained model pays
once, at training time, and amortises it across every query thereafter. That
asymmetry does not shrink with better prompting — it is the treatment.

---

## 4. The defensible claim

**Not** "the trained model is more accurate." That is the weakest version and it
rests on n=6.

> Exposing a trained model as a tool produced **identical answers across repeated
> queries**, at **1/39th the cost** and **1/22nd the latency**, while matching or
> exceeding the accuracy of an agent that wrote its own forecasting code. The
> code-writing agent varied by up to 9% across identical queries and spent 96% of
> its output tokens re-deriving a method it had already used.

This survives B occasionally winning on accuracy at larger n, because
**consistency, cost and latency are structural rather than statistical.**

---

## 5. A methodological defect this run caught — worth reporting

The first run asked *"What will {brand} sell …?"*. **All six Scenario A runs
answered in DKK**, not units: 145,000,000 DKK for Coca Cola against a 3,152,932
*unit* actual, scored as a 4500% error.

The model was not hallucinating — ~145M DKK for monthly Danish Coca-Cola CSD
retail is a plausible *value*. It answered the question that was asked.

Scenarios B and C were immune, because they infer the unit from the data handed
to them. Scenario A has no data, so the ambiguity struck exactly one scenario and
made its measured accuracy an artefact of prompt wording.

Fixed to *"How many units of {brand} will be sold …? Answer in units sold, not
currency."* Re-run confirms it: all runs answered in units and the error fell
from 570% to 35.1%.

**This belongs in the methodology**, not hidden: it is concrete evidence that
prompt equivalence across arms is a real experimental control, not boilerplate.

---

## 6. What can and cannot be claimed

**Established:**

- C is deterministic across repeats; B is not. (Property, n-independent.)
- C costs ~39× less and responds ~22× faster (measured tokens and wall-clock).
- Both ladder increments are positive on HARBOE.

**Not yet established:**

- A confidence interval on the accuracy gap. n=6 per scenario, 2 brands, 1
  category. Sizing (F17): B's CV is 2.67%, so n=10 gives a ±1.9% CI on B's mean
  and detects a 2.65% gap at 80% power. n=10 is the defensible stopping point —
  precision improves as √n, so 10→40 quadruples cost to halve the interval.
- Anything about danskvand, energidrikke or RTD.

---

## 7. Budget arithmetic, from measured per-run cost

| Scenario | mean cost / run | mean latency |
|----------|----------------:|-------------:|
| A_plain | $0.4243 | 100 s |
| B_data | $0.2664 | 114 s |
| C_model | **$0.0068** | **5 s** |
| **one full ladder observation** | **$0.697** | ~220 s |

**$50 buys ~71 full ladder observations (213 API calls).** Practical designs:

| Design | obs / scenario | cost | fits $50? |
|--------|---------------:|-----:|-----------|
| 3 brands × 10 reps | 30 | $20.92 | yes |
| 5 brands × 10 reps | 50 | $34.87 | yes |
| 10 brands × 5 reps | 50 | $34.87 | yes |
| 10 brands × 10 reps | 100 | $69.75 | **no** |
| B+C only, 10 × 10 | 100 | $27.31 | yes |

**Recommended**: 5 brands × 10 repeats × 3 scenarios ≈ **$35**, leaving headroom.
That satisfies the n=10 sizing, widens the brand cross-section from 2 to 5, and
stays inside budget. If money gets tight, dropping Scenario A to 3 repeats saves
~$12 with little loss — A's spread is already small (CV 3.65%) and its role is to
establish the A→B increment, not to be estimated precisely.

---

## Related

- `04_thesis_results/srq4/RESULTS_2026-08-19.md` — the run-level record
- `plans/P0039_.../findings.md` — F12 (B's inconsistency), F17 (sample sizing), F19 (tuning reproducibility), F20 (token breakdown)
- `05_thesis_writing/notes/srq4-experiment-design-rationale.md` — why the design is shaped this way
