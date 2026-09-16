# Thesis in brief — forecasting for agentic decision-support

> **Source file for NotebookLM.** Written for audio-overview and quiz generation.
> It is a *restatement* of a submitted thesis, written from its results artefacts,
> not an excerpt of its prose.
>
> ⚠ **Do not also upload the thesis chapters.** NotebookLM will return our own
> wording as a "source", which reads as independent confirmation and is not.

## The one-paragraph version

A Danish company, Manifold AI, ships a conversational assistant to retailers and
consumer-goods manufacturers. It explains what has already happened — volumes,
market share, weighted distribution — and cannot forecast. This thesis extends
that deployed system with forecasting light enough for a small provider's cloud
budget of about four gigabytes of RAM, and then asks a question that could have
sunk the whole project: is a dedicated forecasting model actually better than
letting a language model write and run its own forecasting code?

The answer is a qualified yes, and the qualification is the contribution.

## Why the framing matters

This is a capability gap in a live product, not a prototype built for a thesis.
The deployed system is the empirical anchor and is **extended, not replaced**.
That single constraint rules out the greenfield architecture most of the
literature assumes, and it is the reason the memory ceiling is treated as a
formal design criterion rather than a convenience.

## The main research question

How can production-oriented agentic decision-support systems without native
predictive capabilities be extended with lightweight forecasting models to
support reliable, forecast-informed, and cost-justified decision-making under
computational and deployment constraints?

## Four sub-questions, one per layer

| | Layer | The question |
|---|---|---|
| SRQ1 | the substrate | Which lightweight forecasting models give the best trade-off between accuracy, memory efficiency, and category specialisation? |
| SRQ2 | the interface | How can a forecast reach an agent with reliability, uncertainty and traceability preserved? |
| SRQ3 | the host system | What must a production agentic system already do before forecasting can attach? |
| SRQ4 | the evidence | Do dedicated models beat an agent writing its own forecasting code, at justified cost? |

## Method

Design Science Research. The thesis produces two things and both are assessed:
an **instantiation** (a working artefact) and a **method-level contribution**
(design knowledge stated separately from the artefact). This is why SRQ2 and
SRQ3 are framed as principles and criteria rather than as descriptions of what
was built.

One design cycle was completed. The design principles are therefore **derived,
not validated across contexts** — the thesis says so.

## The data

A commercial Nielsen scanner panel covering four Danish beverage categories:
carbonated soft drinks, still and sparkling water, energy drinks, and
ready-to-drink. Brand-by-month grain, up to 44 monthly periods. A fifth
category, beer, was dropped on compute grounds — at 455 brands it would have
dominated both preprocessing and the memory budget the thesis exists to respect.

The panel is commercial data under licence and a non-disclosure agreement. It
never leaves the local environment.

## The artefact, in three layers

1. **Forecasting substrate.** Five lightweight model families — ARIMA and
   Prophet as classical methods, LightGBM and XGBoost as gradient-boosted
   ensembles, Ridge as a regularised linear baseline. Five are benchmarked; one
   is served per category, selected on cross-validated rather than test
   accuracy.
2. **Typed tool interface.** JSON function calling with a closed schema taking
   two arguments, category and brand. It returns a point forecast, a
   split-conformal prediction interval, the serving model's measured
   out-of-sample error, and the provenance needed to reconstruct the call.
3. **Bounded tool-using agent.** An orchestrator that calls the tool, validates
   the answer, and communicates it. It advises; it never acts.

**The load-bearing design decision:** the language model never handles a feature
vector. Feature construction stays server-side, where it is versioned and
identical on every call. That is what makes the forecast auditable rather than
merely available, and it is most of the SRQ2 contribution.

## Four findings

1. **Gradient boosting wins, but not decisively between the two families.** Both
   boosters beat Ridge and ARIMA in all four categories. But a five-seed sweep
   changes which one is selected in *every* category, so the two are
   statistically indistinguishable on this data — a weaker headline than naming
   a winner and a more useful one, because a practitioner can choose on training
   time or tooling maturity instead.

2. **The memory constraint bound the selection, not the runtime.** Fitting peaks
   at about 34.5 megabytes against a 4096-megabyte ceiling; serving costs under
   half a megabyte. The budget did its work by excluding transformer and locally
   hosted options before any of them was fitted.

3. **Reliability and traceability hold; uncertainty is a negative result.** Every
   figure the agent reported matched the figure the tool returned. But the
   90 per cent interval spans roughly eight to thirty-four times the quantity
   being forecast — truthful, and too wide for a planner to act on.

4. **Data access is worth far more than the artefact on top of it.** Median error
   falls from 502 per cent to under 3 per cent when the agent is given the
   firm's own history. Above that rung, the dedicated model does *not* win on
   accuracy — it wins on cost, speed and reproducibility.

## The conclusion, stated honestly

A language model given data and an execution environment is a stronger
forecaster than the literature generally grants it. A dedicated predictive layer
must therefore be justified on **reproducibility, cost and auditability** rather
than on error alone.

The closing claim: a forecast becomes usable not when it is accompanied by an
interval, but when it is accompanied by evidence of how far the model producing
it has been right before.

## Scope boundary

One organisation, one national market, four categories — and the scenario
comparison rests on three brands within one of those categories.
