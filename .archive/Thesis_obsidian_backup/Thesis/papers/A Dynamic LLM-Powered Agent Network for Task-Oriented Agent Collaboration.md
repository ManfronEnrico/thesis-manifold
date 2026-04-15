---
title: "A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration"
authors: Liu, Z., Zhang, Y., Li, P., Liu, Y., & Yang, D.
year: 2024
venue: COLM 2024 (Conference on Language Modeling)
doi:
apa7: >
  Liu, Z., Zhang, Y., Li, P., Liu, Y., & Yang, D. (2024). A dynamic LLM-powered agent network
  for task-oriented agent collaboration. *Proceedings of COLM 2024*.
read_date: 2026-03-21
read_depth: full
---

## In one sentence

DyLAN shows that dynamically selecting which agents participate in a multi-agent collaboration — based on their measured contribution in a preliminary trial — consistently outperforms fixed-team architectures, improving accuracy by up to 25% on MMLU while reducing unnecessary computational cost.

## Method

Two-stage framework: (1) Team Optimisation — unsupervised Agent Importance Score (forward-backward message passing on a Temporal Feed-Forward Network, inspired by backpropagation) selects top-contributing agents from a candidate pool; (2) Task Solving — selected agents collaborate with dynamic communication structure, LLM-powered ranker deactivates underperforming agents mid-collaboration. Benchmarked on code generation, decision-making, general reasoning, and arithmetic reasoning (MMLU).

## Key findings — cite these

- Agent selection in DyLAN improves accuracy by **up to 25.0%** on specific MMLU subjects vs. fixed-team baselines
- Dynamic agent teams outperform static teams **across all four task types** tested (code generation, decision-making, general reasoning, arithmetic reasoning)
- Agent Importance Score is **unsupervised** — no labelled data required to identify which agents contribute most
- Fixed communication structures and static agent membership are identified as the primary bottleneck in current multi-agent systems
- Dynamic team reformation during task solving (deactivating low-performing agents mid-run) improves both accuracy and efficiency

## Direct quotes — copy verbatim, include page/section

> "Current approaches are constrained by using a fixed number of agents and static communication structures." (Abstract)

> "These approaches generally predefine agents without further validation of the collaboration process, leading to static agent teams or rebuilding teams without principled verification." (Section 1)

> "DyLAN effectively identifies and coordinates a task-oriented team of agents in a principled way." (Section 1)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Multi-agent systems / orchestration)**: Cite as a key reference establishing that static agent team composition is a limitation of current multi-agent architectures — contextualises our fixed four-agent pipeline (A1→A2→A3→A4) as a deliberate resource-constrained design choice, not an oversight
- **Ch.5 (Framework Design / SRQ2)**: DyLAN's Agent Importance Score provides a theoretical precedent for our Validation Agent's role in measuring agent contribution quality — if extended, our framework could adopt dynamic agent routing based on data quality scores
- **Ch.9 (Limitations / Future Work)**: Our fixed sequential pipeline (coordinator → 4 agents) foregoes dynamic team optimisation — cite DyLAN as a future direction for making our coordination layer adaptive to data availability and forecast confidence

## What this paper does NOT cover (gap it leaves)

DyLAN optimises agent team composition for well-defined reasoning tasks with clear correctness signals (MMLU, code generation) — it does not address **how to coordinate agents operating on heterogeneous data modalities** (scanner data + consumer surveys), **resource constraints on agent activation**, or **how agent outputs are synthesised into uncertainty-quantified business recommendations**, which are the core coordination challenges in this thesis.

## My critical assessment

- **Strengths:** Proposes a principled dynamic multi-agent framework (DyLAN) with unsupervised Agent Importance Scoring and adaptive agent selection, showing consistent performance gains (up to 25%) and improved efficiency over static team architectures across multiple reasoning tasks.
- **Weaknesses:** Evaluation is limited to benchmark-style tasks (e.g., MMLU, code generation) with clear correctness signals, lacking validation in real-world, noisy, or data-driven environments; does not consider computational constraints such as memory limits or cost of dynamic orchestration.
- **Relevance to thesis:** Directly informs your multi-agent design by highlighting the limitations of fixed agent pipelines; supports the conceptual role of your Validation/Critic Agent as a mechanism for assessing agent contribution quality, even within a static architecture.
- **Gap addressed by your work:** Does not address **multi-agent coordination over heterogeneous business data (sales + surveys), forecast uncertainty, or synthesis into actionable recommendations under resource constraints**; your thesis applies multi-agent collaboration to **retail decision support**, where correctness is ambiguous and must be inferred from predictive performance and business value.