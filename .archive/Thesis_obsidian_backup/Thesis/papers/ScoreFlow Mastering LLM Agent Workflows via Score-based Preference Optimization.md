---
title: "ScoreFlow: Mastering LLM Agent Workflows via Score-based Preference Optimization"
authors: Wang, Y., Yang, L., Li, G., Wang, M., & Aragam, B.
year: 2025
venue: arXiv preprint (arXiv:2502.04306v1)
doi:
apa7: >
  Wang, Y., Yang, L., Li, G., Wang, M., & Aragam, B. (2025). ScoreFlow: Mastering LLM agent
  workflows via score-based preference optimization. *arXiv preprint arXiv:2502.04306*.
read_date: 2026-03-21
read_depth: full
---

## In one sentence

ScoreFlow replaces discrete workflow optimisation (Monte Carlo Tree Search, RL) with continuous gradient-based optimisation via Score-DPO — a DPO variant that incorporates quantitative evaluation scores rather than binary preference pairs — achieving 8.2% improvement over baselines while enabling smaller models to outperform larger ones at lower cost.

## Method

Automated multi-agent workflow generation using code as workflow representation. Score-DPO: collects preference pairs from evaluation scores, integrates quantitative score information directly into DPO loss (rather than binary win/lose pairs) to reduce variance and improve convergence. Open-source LLM as workflow generator (minimises API costs). Evaluated on six benchmarks across question answering, coding, and mathematical reasoning. Compared against DyLAN, GPTSwarm, AFlow, ADAS.

## Key findings — cite these

- ScoreFlow achieves **8.2% average improvement** over existing baselines across six benchmarks
- Score-DPO consistently outperforms standard DPO and other preference optimisation methods
- Gradient-based continuous optimisation is **more flexible and scalable** than discrete methods (MCTS, RL) — avoids premature convergence on suboptimal workflow structures
- Smaller models fine-tuned with ScoreFlow can **outperform larger models** at lower inference cost
- Existing methods (AFlow, ADAS) fail to adapt workflows per task instance — ScoreFlow addresses this with per-task adaptive generation

## Direct quotes — copy verbatim, include page/section

> "Existing methods remain inflexible due to representational limitations, a lack of adaptability, and poor scalability when relying on discrete optimization techniques." (Abstract)

> "By replacing traditional discrete optimization algorithms with loss-gradient-based optimization, we enhance the framework's flexibility and scalability." (Section 5)

> "Our method enables smaller models to outperform larger models while incurring lower API costs." (Section 5)

## Where this goes in my thesis

- **Ch.2, Section 2.X (Multi-agent systems / workflow optimisation)**: Cite alongside AutoFlow and DyLAN as the state-of-the-art in automated multi-agent workflow optimisation — establishes that our manually designed LangGraph workflow is a deliberate resource-constrained design choice, not a limitation of the field
- **Ch.5 (Framework Design)**: Score-DPO's use of quantitative scores as optimisation signal is a methodological precedent for our confidence scoring approach — the Synthesis Agent assigns numerical confidence scores (0–100) rather than binary pass/fail, which aligns with ScoreFlow's quantitative feedback philosophy
- **Ch.9 (Limitations / Future Work)**: Our fixed coordinator workflow (sequential A1→A2→A3→A4) could be replaced by a ScoreFlow-style automated optimiser — cite as a concrete future direction for making the coordination layer adaptive

## What this paper does NOT cover (gap it leaves)

ScoreFlow optimises workflows for well-defined benchmark tasks with deterministic correctness signals (QA, coding, maths) — it does not address workflow optimisation where the reward signal is a business outcome metric (forecast accuracy + decision quality), **heterogeneous multi-modal data inputs** (scanner data + consumer surveys), or **resource-constrained deployment under a RAM budget**, which are the applied constraints defining this thesis's design space.

## My critical assessment

- **Strengths:** Introduces a novel continuous optimisation approach (Score-DPO) for multi-agent workflows, effectively leveraging quantitative evaluation scores rather than binary preferences; demonstrates improved performance (8.2%) and efficiency, including enabling smaller models to outperform larger ones.
- **Weaknesses:** Evaluation is limited to structured benchmark tasks (QA, coding, maths) with clear correctness signals; lacks validation in real-world decision-support settings with noisy data, ambiguous objectives, and multi-criteria evaluation.
- **Relevance to thesis:** Provides a strong methodological precedent for using **quantitative scoring signals** (rather than binary evaluation) to guide system behaviour, aligning with your Synthesis Agent’s confidence scoring and evaluation framework; also contextualises your fixed LangGraph workflow as a design choice under constraints.
- **Gap addressed by your work:** Does not address **workflow optimisation under business-oriented objectives (forecast accuracy + decision quality), heterogeneous retail data (scanner + survey), or strict RAM constraints**; your thesis applies similar principles in a **practical, resource-constrained retail analytics setting**, where optimisation targets are less well-defined and more context-dependent.