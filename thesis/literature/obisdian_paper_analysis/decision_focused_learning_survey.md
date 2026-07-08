---
title: "Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities"
authors: [Mandi, Jayanta, Kotary, James, Berden, Senne, Mulamba, Maxime, Bucarey, Victor, Guns, Tias, Fioretto, Ferdinando]
year: 2024
venue: Journal of Artificial Intelligence Research (JAIR), 81, 1623–1701
url: https://doi.org/10.1613/jair.1.15320
tier: 1 — Core anchor (peer-reviewed survey)
score: 8
srqs: [Main, SRQ4]
tags: [gap-G, forecast-to-decision, peer-reviewed, survey, tight-coupling]
ch2_section: "2.3 From descriptive BI to forecast-informed decision-support"
---

## Core argument
Surveys decision-focused learning (DFL): integrating ML and constrained optimization end-to-end so models are trained for decision quality, not prediction accuracy. Predict-then-optimize is the problem; DFL is the response.

## Method
Bilevel formulation (outer level minimises task loss / regret; inner level solves the constrained-optimization problem). Provides a taxonomy of gradient-based DFL methods — analytical differentiation, analytical smoothing, random-perturbation smoothing, surrogate losses (incl. SPO+) — plus gradient-free methods. Benchmarks 11 methods on 7 problems.

## Key finding
"Zero prediction loss always implies zero task loss" but the converse does not hold; in the benchmark **no single DFL method dominates** across problems; perturbation-based methods offer scalability. Confirms that decision quality, not predictive accuracy alone, is the right objective when predictions feed decisions.

## Key quote
> "zero prediction loss always implies zero task loss" (the converse does not hold).

## Relevance to thesis
- [Main/SRQ4]: Peer-reviewed, field-level confirmation that connecting prediction to downstream decisions is an established paradigm yielding measurable decision-quality gains.
- Provides the survey-level citation legitimising the forecast-to-decision premise.

## Gap / limitation
DFL is tight end-to-end coupling for *formal* optimization problems; it does not cover agent-mediated, natural-language, open-ended decision-support (the thesis's loose-coupling setting). **Do not cite as being about LLM agents.** Full read of §1–7 via arXiv HTML; appendices not inspected.
