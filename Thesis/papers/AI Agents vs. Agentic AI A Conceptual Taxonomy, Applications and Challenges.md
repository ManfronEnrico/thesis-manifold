
authors: (see Information Fusion journal)

year: 2025

venue: Information Fusion (Elsevier)

doi:

apa7: >

  (Authors). (2025). AI agents vs. agentic AI: A conceptual taxonomy,

  applications and challenges. *Information Fusion*.

  https://arxiv.org/abs/2505.10468

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

This review establishes the first formal taxonomy separating AI Agents (single-entity, tool-augmented, task-specific LLM systems) from Agentic AI (multi-agent ecosystems with persistent memory, dynamic task decomposition, and coordinated autonomy), arguing the distinction is necessary to align system design with problem complexity.

  

## Method

  

Structured literature review using a hybrid search across 12 platforms (Google Scholar, IEEE Xplore, ACM, Scopus, arXiv, ChatGPT, Perplexity, DeepSeek, Grok, others). Boolean queries on "AI Agents", "Agentic AI", "LLM Agents", "Multi-Agent AI Systems". Organised as a sequential taxonomy from foundational definitions → architectural evolution → application mapping → challenges → solutions roadmap.

  

## Key findings — cite these

  

- AI Agents = modular, single-entity systems using LLMs for tool-assisted, task-specific automation with constrained autonomy

- Agentic AI = multi-agent systems with distributed cognition, persistent memory, orchestration layers (centralised or decentralised), and emergent coordinated behaviour

- Key architectural differentiators: persistent memory, meta-agent coordination, multi-agent planning loops (ReAct, Chain-of-Thought), semantic communication protocols

- Primary challenges for AI Agents: hallucination, prompt brittleness, shallow reasoning, lack of causal understanding

- Primary challenges for Agentic AI: inter-agent misalignment, error propagation, emergent behaviour unpredictability, explainability deficits

- Google Trends data confirms a step-change in interest in both paradigms post-ChatGPT (November 2022)

  

## Direct quotes — copy verbatim, include page/section

  

> "AI Agents are typically designed as single-entity systems that perform goal-directed tasks by utilizing external tools, applying sequential reasoning, and integrating real-time information to complete well-defined functions." (Section 1)

  

> "Agentic AI systems are composed of multiple, specialized agents that coordinate, communicate, and dynamically allocate sub-tasks within a broader workflow to achieve a common goal." (Section 1)

  

> "Clear taxonomy reduces development inefficiencies by preventing the misapplication of design principles such as assuming inter-agent collaboration in a system designed for single-agent execution." (Section 1)

  

> "The transition from reactive task execution to orchestrated, collaborative workflows marks a significant milestone in the evolution of intelligent systems." (Section 7)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.1**: Primary definitional reference — use to formally position the thesis framework as Agentic AI (not a single AI Agent); the Coordinator + 4 sub-agents with dynamic task allocation maps exactly onto the Agentic AI definition

- **Ch.3 (Methodology)**: Supports the choice of LangGraph as an orchestration layer — the paper explicitly names LangGraph as an example of an agentic orchestration framework

- **Ch.5 (Framework Design)**: The taxonomy's distinction between centralised and decentralised orchestration justifies the thesis's centralised Coordinator design for a resource-constrained environment

- **Ch.9 (Discussion)**: The challenges section (inter-agent misalignment, error propagation) directly informs the thesis's 3-level validation framework rationale

  

## What this paper does NOT cover (gap it leaves)

  

The taxonomy is entirely conceptual and application-agnostic; it does not address resource-constrained deployment (RAM budgets, sequential model execution) nor the synthesis of heterogeneous ML forecasting outputs into calibrated business recommendations. The specific challenge of building Agentic AI under hard computational constraints in a retail analytics context is absent from both the taxonomy and the applications survey.

  

## My critical assessment

while it is highly valuable for design justification, taxonomy, and problem framing, it cannot be used as evidence of system performance or efficiency.

  
**