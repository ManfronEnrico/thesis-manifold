---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
authors: Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T.
year: 2023
venue: NeurIPS 2023 (37th Conference on Neural Information Processing Systems)
doi:
apa7: >
  Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L.,
  Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools.
  *Advances in Neural Information Processing Systems*, *36*. (NeurIPS 2023)
read_date: 2026-03-21
read_depth: full
---

## In one sentence

Toolformer demonstrates that LLMs can learn to autonomously decide when, which, and how to call external tool APIs through a self-supervised data generation process — filtered by whether API calls actually reduce perplexity on future tokens — enabling a 6.7B model to outperform the much larger GPT-3 on diverse zero-shot tasks.

## Method

Self-supervised pipeline: (1) sample API call candidates at each token position using few-shot prompts; (2) execute API calls; (3) filter calls that reduce perplexity on subsequent tokens (loss-based selection); (4) fine-tune LM on filtered API-augmented dataset. No large human annotation required — only a handful of demonstrations per API. Tools integrated: calculator, Q&A system, Wikipedia search, translation system, calendar. Base model: GPT-J 6.7B. Benchmarked against GPT-3 and baselines on diverse downstream tasks.

## Key findings — cite these

- Toolformer (6.7B parameters) **outperforms GPT-3** (much larger) on a range of zero-shot downstream tasks after tool learning
- Self-supervised tool learning requires **only a handful of human demonstrations per API** — not large annotated datasets
- LMs autonomously decide **when NOT to call a tool** — tool use is selective, not forced
- Loss-based filtering is the key mechanism: only API calls that help predict future tokens are retained
- Tool use does not degrade core language modelling ability — the model retains generality

## Direct quotes — copy verbatim, include page/section

> "Language models exhibit remarkable abilities to solve new tasks from just a few examples or textual instructions, especially at scale. They also, paradoxically, struggle with basic functionality, such as arithmetic or factual lookup, where much simpler and smaller specialized models excel." (Abstract)

> "The LM should not lose any of its generality and should be able to decide for itself when and how to use which tool." (Section 1)

> "We let a LM annotate a huge language modeling dataset with potential API calls. We then use a self-supervised loss to determine which of these API calls actually help the model in predicting future tokens." (Section 1)

## Where this goes in my thesis

- **Ch.2, Section 2.X (LLM agents / tool use — foundational reference)**: Cite as the seminal paper establishing self-supervised tool use in LLMs — Toolformer is the direct theoretical ancestor of our Forecasting Agent's tool-calling pattern, where the LLM decides which ML model to invoke based on data characteristics
- **Ch.5 (Framework Design / SRQ2)**: Toolformer's principle that "the model decides for itself when and how to use which tool" is the design philosophy underpinning our Synthesis Agent — it selects and weights model outputs rather than always invoking all models uniformly
- **Ch.2 (Related Work — timeline)**: Position Toolformer (2023) → SciAgent (2024) → DyMo (2025) as a progression from self-supervised tool learning → domain-specific tool use → stateful environment tool use, situating our contribution in this lineage

## What this paper does NOT cover (gap it leaves)

Toolformer trains a single LLM to call general-purpose tools (calculator, search) in a text generation context — it does not address **multi-agent coordination where tool outputs feed downstream agents**, **ensemble synthesis of competing probabilistic forecasts under uncertainty**, or **resource-constrained deployment**, which are the architectural and applied challenges this thesis addresses.

## My critical assessment
- **Strengths:** Introduces a scalable, self-supervised approach for learning tool use in LLMs, where API calls are filtered based on their contribution to predictive performance (loss reduction); demonstrates strong empirical gains, with a smaller model outperforming GPT-3 on zero-shot tasks while retaining generality.
- **Weaknesses:** Focuses on single-agent tool use in text-generation settings with well-defined token prediction objectives; does not address multi-step decision pipelines, uncertainty handling, or evaluation beyond language modelling metrics.
- **Relevance to thesis:** Provides the foundational paradigm for tool-augmented LLM behaviour, directly informing your Forecasting and Synthesis Agents where ML models act as tools and are selectively invoked rather than uniformly applied.
- **Gap addressed by your work:** Does not cover **multi-agent orchestration, ensemble synthesis of competing forecasts, or deployment under strict RAM constraints**; your thesis extends tool-use from token-level optimisation to **end-to-end predictive decision support in retail analytics**, where outputs must be aggregated, evaluated, and translated into business actions.
