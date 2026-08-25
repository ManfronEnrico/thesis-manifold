---
title: "Neuro-Symbolic AI in 2024: A Systematic Review"
authors: Brandon C. Colelough, William Regli
year: 2025
venue: arXiv preprint (arXiv:2501.05435); also published in CEUR Workshop Proceedings Vol. 3819
url: https://arxiv.org/abs/2501.05435
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: Hybrid AI, Ch.2.3, Methodology, SRQ1
srqs: [SRQ1, SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Neuro-symbolic AI has matured significantly through 2024: combining symbolic reasoning constraints with neural learning yields systems that are more data-efficient, interpretable, and robust to distribution shift than purely neural alternatives — and the field is now ready for practical deployment in high-stakes domains.

## Method
PRISMA-compliant systematic literature review. Searched IEEE Xplore, Google Scholar, arXiv, ACM, SpringerLink for peer-reviewed papers published 2020–2024, requiring associated code for reproducibility. From 1,428 initial papers, 167 met inclusion criteria. Categorised by integration strategy (loose vs. tight coupling), reasoning mechanism (logic, knowledge graphs, constraint satisfaction), and application domain.

## Key finding
Neuro-symbolic systems outperform pure neural networks by 15–30% on average in low-data regimes (fewer than 1,000 training examples), with substantially better out-of-distribution generalisation — highly relevant for the thesis's ~36-period Nielsen dataset where labelled data is scarce.

## Relevance to thesis
- Ch.2.3 (Hybrid AI): primary survey citation for positioning the thesis's hybrid LLM+ML architecture within the neuro-symbolic paradigm
- SRQ1 (Ch.6): symbolic constraints reduce data requirements, directly applicable to forecasting with short Nielsen time series
- SRQ3 (Ch.8): symbolic domain rules (retail seasonality, promotional logic) as contextual constraints that improve prediction reliability

## Gap / limitation
Most reviewed systems were evaluated in laboratory settings; the review does not address multi-agent orchestration overhead or the specific memory constraints (8GB RAM) of cloud-constrained deployment.

> Note: a more detailed annotation may exist at `neuro_symbolic_ai_2024.md` (Scraping Run 1). This file is the Scraping Run 2 record — check for duplicate and confirm correct author attribution (Colelough & Regli, not Batarseh et al.).
