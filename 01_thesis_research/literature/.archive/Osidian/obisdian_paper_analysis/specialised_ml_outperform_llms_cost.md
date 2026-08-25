---
title: "Faster, Cheaper, More Accurate: Specialised Knowledge Tracing Models Outperform LLMs"
authors: Pragya Bhattacharyya, Joshua Mitton, Ralph Abboud, Simon Woodhead
year: 2026
venue: arXiv preprint (arXiv:2603.02830)
url: https://arxiv.org/abs/2603.02830
tier: 2 — Supporting
score: 7
angles: [Cost/Latency, Specialised ML vs LLM]
srqs: [SRQ4]
peer_reviewed: false
preprint: true
---

## Core argument
For a specialised predictive task, a small dedicated ML model beats a general-purpose LLM on
accuracy **and** is orders of magnitude cheaper and faster to deploy — i.e. the LLM's generality
is not cost-justified when a specialised model exists.

## Method
Head-to-head comparison between specialised classical ML (knowledge-tracing) models and LLMs on a
domain-specific prediction task, reporting a three-way accuracy / latency / deployment-cost
comparison.

## Key finding
The specialised models win on accuracy (F1) while the LLMs are "orders of magnitude slower and
more expensive to deploy." The cost/latency gap, not just accuracy, is the decisive factor.

## Relevance to thesis
- SRQ4 (secondary metrics — cost, latency): the cleanest external analogue of our core SRQ4
  claim — **dedicated lightweight ML beats a general LLM on cost, latency, and correctness for a
  specialised predictive task.** Grounds the v4 "cost-justified" dimension of the Main RQ and
  supports the external-validity argument in the Discussion (different domain, same conclusion
  shape).
- Complements [[infiagent_dabench]] / [[airepr_reproducibility]] (which cover the primary metrics)
  by supplying the cost/latency evidence.

## Gap / limitation
**PREPRINT — not peer-reviewed** (flag in Ch.2; confirm acceptability with supervisor). Domain is
educational knowledge tracing, not FMCG demand forecasting, so it is an analogue rather than a
direct precedent. Does not address the agentic-orchestration layer — only the model-vs-LLM
comparison.
