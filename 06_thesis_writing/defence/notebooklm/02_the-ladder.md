# The seven-scenario ladder — the experiment and why it is shaped that way

> **Source file for NotebookLM.** The single most examinable piece of
> methodology in the thesis. Written for audio-overview and quiz generation.

## The question the experiment answers

Given the same forecasting task, does routing the forecast through a dedicated
model reached by a structured interface produce a better answer than letting a
language model write its own forecasting code — and at what cost?

## Why a two-way comparison could not answer it

A two-arm design confounds two entirely different things:

1. the value of giving an agent access to the firm's data **at all**, and
2. the value of giving it a **trained model** rather than a code sandbox.

The first turns out to be far larger than the second. A two-arm design would
have folded it into the effect the thesis is actually about, and the headline
would have been an artefact of the design rather than a finding.

So the evaluation is built as a **ladder**: each rung adds exactly one capability
to the rung below, so the increments attribute separately.

## The seven rungs

| Rung | Name | What it is given |
|---|---|---|
| A | plain language model | no firm data; web search only |
| B | code-as-action | the brand's history in an execution sandbox, where it writes and runs its own forecasting code |
| C | dedicated model | the same history behind the structured forecast tool; it writes no code |
| D | code-as-action, in production | scenario B, orchestrated by the production platform (Prometheus) |
| E | dedicated model, in production | scenario C, orchestrated by the production platform |
| F | combined | both the execution sandbox and the forecast tool |
| G | combined, in production | scenario F, orchestrated by the production platform |

## How to read the ladder — two directions

**Reading up** from A:
- A → B measures **what access to the firm's own data buys**
- B → C measures **what replacing self-written analysis with a dedicated model
  adds** — *this increment is the thesis contribution*
- C → F measures what returning the code environment on top of the model adds

**Reading across:** D, E and G repeat B, C and F on the production orchestrator,
so an effect observed on the lightweight coordinator can be **checked for
survival** in the deployment environment rather than assumed to transfer.

## Why the two orchestrators matter more than they look

The same intervention — adding the forecasting tool — is applied in **two
independently built agentic systems**. A consistent effect therefore cannot be
attributed to the design of a single evaluation harness.

The two settings also differ in reproducibility, deliberately:

- the general-purpose rungs are **reproducible** from the thesis repository, an
  API key and access to the panel;
- the production rungs are **ecologically valid** but cannot be re-executed by a
  reader, because the production system is proprietary.

Neither property is sufficient on its own. The design is constructed so the two
corroborate one another.

## Scale

- 7 scenarios × 3 brands × 3 repeats = **63 funded runs**
- 60 of 63 produced a usable forecast
- total spend **$19.60**, roughly 31 cents per run

## Why three repeats and not one

Because the within-scenario variation is comparable to the between-scenario
gaps, and a single run of each would have produced a ranking that looked clean
and meant nothing.

The evidence is stark. On the mid-volume brand, scenario A returned errors of
1740, 1204 and 974 per cent across three runs of an **identical** prompt — a
spread of 767 percentage points. The code-writing scenario varied by 23 points
on the same brand. The dedicated-model scenarios varied by **zero**.

**The rule this imposes:** differences between scenarios smaller than the
variation within them cannot be read as an ordering.

## Why three brands, and how they were chosen

Chosen by **volume stratification** from the qualifying population — the
largest, the median and the smallest. They span three orders of magnitude of
monthly sales, from roughly 2,850 units to roughly 6.4 million.

The stratification matters because a comparison run only on data-rich brands
would flatter a trained model, and one run only on thin series would measure
rounding rather than forecasting.

**Never justify the brand selection on "hard to forecast" grounds.** That would
be outcome-based selection. The criteria are volume coverage and a meaningful
error metric, both fixed in advance.

## The three inclusion criteria

All applied before any run, identically to every scenario:

1. at least as many held-out months as the forecast horizon — otherwise there is
   no month to score;
2. no zero months in the held-out window — percentage error divides by the
   actual, and a zero makes the score undefined rather than merely difficult;
3. the scored month must record at least **1,000 units**.

The third is a property of the **measurement**, not of the method. Below roughly
that volume, percentage error is dominated by integer rounding: on a nine-unit
series a single unit of error registers as eleven per cent, which exceeds the
differences the experiment is designed to detect. Fourteen of the seventy-six
brands satisfying the first two criteria sell fewer than a hundred units in the
scored month — so the low end of the category is a cliff rather than a gradient.

## The controls, and the audit that found one had failed

Every scenario receives the **identical user question**. An earlier design gave
each scenario differently worded instructions, so any difference in outcome
would have partly measured the wording rather than the capability under test.

The capability notes that distinguish the scenarios are **composed from shared
blocks** rather than written individually, and an automated check renders all
seven and asserts that paired scenarios are byte-identical wherever they should
be. The full prompt set's identity is recorded as a **hash**, so no prompt can
be altered without the recorded run identity changing with it.

**That control was not assumed to hold.** An audit before the funded run found
the capability notes had drifted: one scenario was instructed to produce a
prediction interval while its paired scenario was not, and both were nonetheless
scored on interval communication. The notes were rebuilt from shared blocks, the
automated check was added in response, and the correction was made **before any
funded run was executed** — so no reported result rests on the defective
instrument.

## Outcomes are classified, never averaged

A scenario that answers six of nine questions is not comparable to one that
answers nine of nine on accuracy alone, and a failure rate says more about
production readiness than a small difference in error.

Scenario A is the only scenario that fails, and it fails on the smallest brand:
asked about a regional Danish producer selling roughly 2,850 units, it answered
120,000, 62,000 and 90,000 across three repeats. Those are not forecasts with
large errors — they are answers of the wrong order of magnitude, and they are
classified as failures rather than scored, because averaging them would let an
arbitrary number determine the scenario's mean.

## What no language model judged

**Nothing.** All measures are computed programmatically against held-out actuals
and recorded execution traces. An LLM-as-judge protocol was considered and
**dropped**, because a model acting as judge introduces non-determinism and with
it a requirement for its own bias controls, into a question that arithmetic
already answers.

## Why an arm that already has the forecast still writes code

In the combined scenarios (F, G) the model's forecast is supplied as **one input
among several** rather than as a starting figure to revise. An agent handed a
number and permitted to keep it will usually keep it, and the design would then
measure **deference** rather than integration.

It worked: all 18 combined-scenario runs carry `deviates_from_model = True`. Not
one adopted the figure it was handed, and several cited the model's own stated
uncertainty as the reason.

## The four threats to validity, each with what was done

| Threat | Type | What was done |
|---|---|---|
| Three brands in one category | External | scope stated wherever a result is claimed; brands stratified by volume, so the range is covered even though the sample is small |
| Within-scenario variation comparable to between-scenario gaps | Internal | three repeats per cell; spread reported beside every mean; no ordering claimed where the gap is smaller than the spread |
| Prompt wording confounded with capability | Construct | identical question; capability notes composed from shared blocks; automated byte-identity check |
| Volume floor on brand inclusion | Construct | a property of the metric's resolution, applied identically and before any run |

**A fifth limitation is a boundary rather than a threat:** the evaluation
measures what each scenario *communicated* and how accurate it was — not whether
a planner receiving that communication decided better. Establishing that would
require an experiment with human participants and ethical approval.

## What the comparison cannot separate

Four explanations compete for any accuracy gap, and the thesis declines to
resolve the attribution rather than choosing:

| | Explanation | What would separate it |
|---|---|---|
| 1 | **Per-series beats per-category** — a category-tuned model is pulled toward brands unlike the one being forecast | fit the pipeline per brand on the same three brands; one training run |
| 2 | **Combination beats a single model** — the code arms fit many models and average; the substrate serves one | add a combination baseline |
| 3 | **Established practice the substrate lacks** — exponential smoothing, a seasonal ARIMA term | close both gaps, re-compare |
| 4 | **Horizon interaction** | only separable if the secondary horizon is run |

Explanation 1 is the largest and the cheapest to test. **Measured** over the 37
data-scenario responses: 36 fitted exponential smoothing, 32 a seasonal ARIMA,
28 used explicit combination language. Those are precisely the techniques the
substrate does not implement — so a material part of the code arms' median
accuracy is plausibly attributable to established practice rather than to code
execution as such.

## The anchoring check — the cheapest attack on the whole result

If the code-writing agent were simply echoing each brand's last observed month,
the comparison would be measuring nothing.

**It was not.** Across the eighteen funded runs whose series is recoverable, not
one forecast fell within five per cent of the brand's last observed month. The
forecasts sat substantially closer to a trailing twelve-month average, with
roughly half the dispersion around it — consistent with the explicit
model-fitting visible in their working.

Quote the **count**, not the ratios: "not one of eighteen within five per cent of
the last value". Per brand the medians are 1.082, 0.991 and 0.825, so only one of
three brands is genuinely centred on its trailing mean; a pooled figure would be
three behaviours averaging into one.

This does not cover scenario A, which receives no history and so cannot anchor.
