---
title: "Smart 'Predict, then Optimize'"
authors: [Elmachtoub, Adam N., Grigas, Paul]
year: 2022
venue: Management Science, 68(1), 9–26
url: https://doi.org/10.1287/mnsc.2020.3922
tier: 1 — Core anchor (peer-reviewed, top-tier venue)
score: 9
srqs: [Main, SRQ4]
tags: [gap-G, forecast-to-decision, peer-reviewed, tight-coupling]
ch2_section: "2.3 From descriptive BI to forecast-informed decision-support"
---

## Core argument
Machine learning minimises prediction error, but practitioners care about decision quality. Standard "predict-then-optimize" trains a predictor independently of how its outputs feed a downstream optimization, so a low-error prediction can still yield a poor decision (and vice versa). Prediction should be trained with respect to the downstream decision cost.

## Method
Defines the SPO loss (true decision regret of the implemented decision) and a tractable convex surrogate, SPO+, derived via duality. Proves SPO+ upper-bounds SPO loss and is Fisher-consistent under mild conditions; for linear models reduces to a linear program per iteration.

## Key finding
SPO+-trained models outperform standard least-squares predict-then-optimize on shortest-path and portfolio problems, sometimes dominating random forests even when the ground truth is nonlinear, because they position decision boundaries correctly rather than minimising residuals.

## Key quote
> "[Most solution systems] do not effectively account for how the predictions will be used in a downstream optimization problem."

## Relevance to thesis
- [Main/SRQ4]: Canonical peer-reviewed evidence that **forecasts create value through their connection to downstream decisions** — the foundation for the thesis's forecast-informed decision-support framing.
- Establishes the *tight-coupling* baseline (predictor trained against the decision objective) against which the thesis's *loose, agent-mediated coupling* is contrasted.

## Gap / limitation
SPO couples prediction and decision tightly via a differentiable optimization objective with a known formal program. It does not address open-ended managerial decision-support, natural-language recommendations, LLM agents, or settings without a single optimization objective — exactly the space the thesis occupies. **Do not cite as being about LLM agents.** No explicit limitations section in the paper.
