---
title: "SciAgent: Tool-augmented Language Models for Scientific Reasoning"
authors: [Ma, Minghao, et al.]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2402.11451
tier: 1 — Core Essential
score: 8
srqs: [SRQ2]
---

## Core argument
SciAgent proposes a tool-augmented LLM framework for scientific reasoning that equips language models with a curated toolset covering mathematical computation, knowledge retrieval, and domain-specific APIs. The system demonstrates that LLMs acting as reasoning orchestrators — delegating subtasks to specialised tools — substantially outperform pure LLM approaches on complex, multi-step scientific problems. The paper argues that effective tool selection and invocation is a learnable, trainable capability rather than a prompt-engineering artefact.

## Method
The authors construct a scientific reasoning benchmark (SciToolBench) spanning mathematics, physics, chemistry, and biology, then fine-tune and evaluate LLMs on tool-augmented versus tool-free settings. Tool invocation sequences are derived from curated demonstrations and evaluated on correctness and tool-use efficiency.

## Key finding
SciAgent achieves up to 13.4 percentage-point improvements over GPT-4 in tool-free mode on multi-step scientific tasks, demonstrating that structured tool augmentation systematically closes the gap between LLM reasoning and domain-expert accuracy.

## Key quote
> "We propose SciAgent, a framework that equips language models with scientific tools to enhance their scientific reasoning abilities, bridging the gap between language model capabilities and the demands of expert-level scientific tasks."

## Relevance to thesis
- [SRQ2]: Directly informs the Synthesis Agent design — the pattern of an LLM orchestrator invoking specialised tools (ML models, data APIs) mirrors how the thesis framework routes analytical subtasks to forecasting sub-agents and data retrieval tools.
- [SRQ2]: The tool-selection and invocation logic studied in SciAgent is analogous to the Coordinator's decision to dispatch tasks to the Forecasting Agent or Data Assessment Agent.

## Gap / limitation
SciAgent operates in a scientific reasoning benchmark context with no resource (RAM/compute) constraints and no real-time business data pipelines. It does not address FMCG retail demand forecasting, multi-agent coordination across heterogeneous ML outputs, or the synthesis of probabilistic forecasts into managerial natural-language recommendations. There is no evaluation of tool-use under memory-constrained cloud deployment.
