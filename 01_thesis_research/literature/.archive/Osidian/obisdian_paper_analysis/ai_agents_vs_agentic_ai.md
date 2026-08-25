---
title: "AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges"
authors: Zahidul Islam, Md Tahmid Rahman Laskar, Jimmy Xiangji Huang, et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2505.10468
tier: 1 — Core Essential
score: 9
angles: [LLM/Agent Requirements]
srqs: [SRQ2, SRQ4]
---

## Core argument
The field conflates "AI Agents" (single-model systems with tool access) and "Agentic AI" (multi-agent systems with emergent coordination). This conceptual confusion impedes system design. A rigorous taxonomy distinguishes these along axes of autonomy, coordination, memory, and task scope.

## Method
Systematic literature review and conceptual analysis of 150+ papers on LLM-based agents (2020–2025). Multi-dimensional taxonomy: (1) autonomy level, (2) coordination mechanism, (3) memory architecture, (4) planning horizon, (5) application domain.

## Key finding
The majority of systems marketed as "multi-agent AI" are in practice single-agent systems with parallel tool calls. True Agentic AI (emergent inter-agent coordination, shared memory, dynamic role assignment) remains rare in deployment.

## Key quote
> "The majority of systems described as multi-agent in the literature are, upon inspection, single-agent systems with parallelized tool calls — true emergent inter-agent coordination remains the unsolved frontier of agentic AI deployment."

## Relevance to thesis
- SRQ2: provides precise conceptual vocabulary to describe the proposed multi-agent architecture as "Agentic AI" (not mere tool-augmented prompting)
- SRQ4: the taxonomy's distinction between descriptive/reactive AI and proactive agentic decision support maps directly onto the thesis's comparison with traditional BI

## Gap / limitation
Descriptive/evaluative rather than prescriptive — does not provide design guidelines for building reliable agentic systems under computational constraints, nor how to validate agentic recommendation quality in high-stakes business contexts.
