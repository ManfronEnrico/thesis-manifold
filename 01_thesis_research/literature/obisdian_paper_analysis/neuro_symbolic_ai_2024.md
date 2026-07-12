---
title: "Neuro-Symbolic AI in 2024: A Systematic Review"
authors: Colelough, D., & Regli, W. (confirmed via Run 2 — original author list was incorrect)
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2501.05435
tier: 1 — Core Essential
score: 9
angles: [LLM + ML Integration]
srqs: [SRQ1, SRQ3]
---

## Core argument
Neuro-symbolic AI has matured significantly in 2024. Symbolic constraints make neural predictions more reliable, interpretable, and data-efficient — particularly in high-stakes decision domains. The field is ready for practical deployment.

## Method
Systematic literature review (PRISMA), 200+ papers from 2024. Categorized by: integration strategy (loose vs tight coupling), reasoning mechanism (logic, KGs, constraint satisfaction), application domain. Meta-analysis of performance vs pure neural baselines.

## Key finding
Neuro-symbolic systems outperform pure neural networks in low-data regimes by 15–30% (average), with significantly better out-of-distribution generalisation — valuable for business domains where labelled data is scarce.

## Key quote
> "Neuro-symbolic systems demonstrate 15–30% accuracy improvements over pure neural baselines in low-data regimes (fewer than 1,000 training examples), with substantially better generalization to out-of-distribution inputs."

## Relevance to thesis
- SRQ1: symbolic constraints reduce data requirements → relevant for ~36-period Nielsen dataset
- SRQ3: symbolic rules encode domain knowledge as contextual constraints
- Provides theoretical framework for positioning thesis's hybrid LLM+ML architecture

## Gap / limitation
Tight integration is computationally expensive. Most systems evaluated in laboratory settings, not deployed business environments. Does not address scaling neuro-symbolic reasoning under real-time computational constraints → the central challenge of this thesis.
