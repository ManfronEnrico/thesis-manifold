---
title: "Neuro-Symbolic AI in 2024: A Systematic Review"
authors: Colelough, B. C., & Regli, W.
year: 2025
venue: arXiv preprint (arXiv:2501.05435v2) / CEUR Workshop Proceedings
doi:
apa7: >
  Colelough, B. C., & Regli, W. (2025). Neuro-Symbolic AI in 2024: A systematic review.
  *arXiv preprint arXiv:2501.05435*.
read_date: 2026-03-21
read_depth: full
---

## In one sentence

A PRISMA-based systematic review of 158 Neuro-Symbolic AI papers (2020–2024) finds that research is concentrated in learning/inference and logic/reasoning while explainability, trustworthiness, and meta-cognition — the capacities most critical for reliable real-world deployment — remain significantly underrepresented.

## Method

PRISMA systematic review methodology. Five databases: IEEE Xplore, Google Scholar, arXiv, ACM, SpringerLink. Initial pool: 1,428 papers; final corpus: 158 papers (filtered for relevance, peer review, and public codebase availability). Five-category taxonomy: Knowledge Representation, Learning & Inference, Explainability & Trustworthiness, Logic & Reasoning, Meta-Cognition. Coverage period: 2020–2024.

## Key findings — cite these

- **63%** of papers focus on Learning & Inference; **44%** on Knowledge Representation; **35%** on Logic & Reasoning
- **Only 28%** address Explainability & Trustworthiness — critical gap given real-world deployment requirements
- **Only 5% (n=8)** address Meta-Cognition — the most underrepresented area in the field
- Neuro-Symbolic AI publications grew exponentially from 53 (2020) to 236 (2023 peak)
- Only **one paper** (AlphaGeometry, Google) sits at the intersection of all four main research areas
- Meta-Cognition defined as: the system's capacity to monitor, evaluate, and adjust its own reasoning — directly analogous to agent self-monitoring and critic loops

## Direct quotes — copy verbatim, include page/section

> "Neuro-Symbolic AI is a composite AI framework that seeks to merge the domains of Symbolic AI and Neural Networks to create a superior hybrid AI model possessing reasoning capabilities." (Section 1.3, citing Garcez & Lamb, 2023)

> "Neglecting Meta-Cognition in Neuro-Symbolic AI research limits system autonomy, adaptability, and reliability, hindering error correction and reducing trustworthiness in dynamic environments." (Section 2.2)

> "There remains a relative sparseness of research focused on explainability and trustworthiness. This gap is particularly concerning given the increasing deployment of AI systems in real-world applications, where transparency and reliability are paramount." (Section 6)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Hybrid AI / theoretical framing)**: Cite as the state-of-the-art survey positioning our framework within the Neuro-Symbolic AI landscape — our system combines sub-symbolic ML forecasting (LightGBM, Prophet) with symbolic LLM reasoning (Synthesis Agent), making it a practical Neuro-Symbolic application
- **Ch.5 (Framework Design)**: The Learning & Inference + Knowledge Representation intersection maps directly to our architecture — ML models (sub-symbolic) + LLM synthesis with structured state (symbolic)
- **Ch.5 / Ch.8**: The Meta-Cognition definition (monitor, evaluate, adjust own reasoning) is the theoretical grounding for our Critic Agent and 3-level Validation Agent — cite when justifying self-monitoring agent design
- **Ch.9 (Limitations / Future Work)**: The explainability gap identified in this review directly motivates a future work item — our system currently lacks a formal explainability layer; cite to position this as a known field-wide gap, not just our limitation

## What this paper does NOT cover (gap it leaves)

This review surveys Neuro-Symbolic AI at the algorithmic and architectural level but does not address **resource-constrained deployment** or **domain-specific business applications** — it provides no guidance on how to implement a Neuro-Symbolic pipeline under a fixed RAM budget for retail analytics, which is the applied design challenge at the core of this thesis.

## My critical assessment

- **Strengths:** Provides a comprehensive, PRISMA-based systematic review of 158 Neuro-Symbolic AI papers, clearly categorising research across Learning & Inference, Knowledge Representation, Logic & Reasoning, Explainability & Trustworthiness, and Meta-Cognition; identifies key gaps in real-world deployment readiness.
- **Weaknesses:** Survey focuses on algorithmic and architectural literature without addressing practical deployment constraints, such as limited RAM, large-scale tabular datasets, or retail-specific business use cases; does not provide implementation guidance for multi-agent orchestration or hybrid predictive pipelines.
- **Relevance to thesis:** Positions your framework within the Neuro-Symbolic AI landscape, justifying the combination of sub-symbolic ML forecasting (ARIMA, LightGBM, Prophet, etc.) with symbolic LLM synthesis (Synthesis Agent); the meta-cognition discussion supports your Critic Agent design for self-monitoring and adaptive evaluation.
- **Gap addressed by your work:** The review does not cover **resource-constrained, domain-specific predictive decision-support systems**; your thesis operationalises a Neuro-Symbolic-inspired architecture under ≤8 GB RAM, applied to Danish FMCG retail sales and survey data, directly filling this practical gap.