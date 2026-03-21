---
title: "Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents"
authors: [Putta, Pranav, et al.]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2408.07199
tier: 2 — High Relevance
score: 8
srqs: [SRQ2]
---

## Core argument
Agent Q introduces a framework for training autonomous AI agents to perform multi-step reasoning and decision-making through a combination of Monte Carlo Tree Search (MCTS) and Direct Preference Optimisation (DPO). The paper argues that agents must be capable of iterative self-improvement via feedback loops — not just prompted reasoning — to handle complex, long-horizon tasks reliably. The framework couples search-based planning with preference learning to fine-tune agent behaviour on task-relevant trajectories.

## Method
MCTS is used to explore multi-step action trajectories on web navigation and agentic benchmarks; successful and failed trajectories are used as preference pairs to fine-tune the underlying LLM via DPO. Evaluation is conducted on WebShop and real-world web agent tasks, measuring task completion rate and step efficiency.

## Key finding
Agent Q achieves a 50.5% success rate on real-world web-based agent tasks compared to 18.6% for baseline LLM-only agents, demonstrating that iterative, search-guided self-improvement significantly lifts autonomous agent performance.

## Key quote
> "We introduce Agent Q, a framework that combines Monte Carlo Tree Search with AI feedback and Direct Preference Optimization to enable agents to learn from both successful and failed reasoning trajectories."

## Relevance to thesis
- [SRQ2]: The MCTS + DPO loop is conceptually relevant to how the Coordinator agent might iteratively refine sub-agent task assignments based on quality feedback from the Validation Agent.
- [SRQ2]: Agent Q's treatment of long-horizon multi-step decision-making under uncertainty parallels the thesis framework's need to coordinate sequential phases (data assessment → forecasting → synthesis) with feedback between agents.

## Gap / limitation
Agent Q is evaluated on web navigation and general agentic benchmarks, with no application to business analytics, forecasting, or FMCG retail. There is no treatment of RAM or computational constraints, no integration of ML forecasting outputs, and no evaluation in a decision-support context where outputs must be interpretable to business analysts. The self-improvement loop requires iterative LLM fine-tuning, which is infeasible under an 8GB RAM constraint.
