%%FILE NAME: Schick et al. (2023) - Toolformer Language Models Can Teach Themselves to Use Tools%%

---
aliases:
learning_text_title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
learning_text_venue: NeurIPS 2023
learning_text_doi: 10.48550/arXiv.2302.04761
learning_text_apa7: "Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. *Advances in Neural Information Processing Systems*, *36*."
learning_list_authors:
  - Schick, T.
  - Dwivedi-Yu, J.
  - Dessì, R.
  - Raileanu, R.
  - Lomeli, M.
  - Zettlemoyer, L.
  - Cancedda, N.
  - Scialom, T.
learning_list_topic:
  - tool-augmented LLMs
  - self-supervised fine-tuning
  - API call generation
  - LLM agents
  - zero-shot task performance
learning_list_srq:
  - SRQ2
  - SRQ3
learning_list_chapter:
  - Ch.2
  - Ch.3
learning_number_release_year: 2023
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: Medium
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-21
cssclasses:
---

# AI Assessment
---
## In one sentence

Toolformer demonstrates that a generalist language model can learn, through self-supervised perplexity-based filtering of its own API call candidates, when and how to invoke external tools — without task-specific supervision or sacrificing general language modelling capability.

## Core Ideas

- **Self-supervised tool annotation**: Given only a handful of human-written examples showing how an API works, the model generates thousands of candidate API calls inserted into plain text, executes them, and keeps only those where having the tool's answer actually reduces prediction error on the surrounding tokens — no human labelling of when to use tools is needed beyond the initial few-shot prompt.
- **Perplexity-based filtering criterion**: An API call is retained only if `L⁻ᵢ − L⁺ᵢ ≥ τf` — i.e., receiving both the call and its result must reduce the model's cross-entropy loss over future tokens compared to receiving no call or a call with no result. This ensures only genuinely informative tool uses survive into the fine-tuning corpus.
- **Generalised, task-agnostic tool routing**: The model learns to decide at inference time which tool (if any) to invoke and what to ask, rather than being hard-wired to a specific task; tool selection emerges from fine-tuning on the filtered corpus without any explicit routing supervision.

### Business-level takeaway
Think of it like training a new analyst: instead of writing a manual for every possible situation, you show them a few examples of when to use a calculator, when to look something up, and when to ask a colleague — then let them figure out the rest themselves by trial and error. Toolformer does the same thing automatically: it reads millions of documents, experiments with inserting tool calls, checks whether the tool's answer actually helped it understand the text, and keeps only the useful habits. The result is an AI that knows when to reach for the right tool on its own, without a human specifying it for every new task.

## Methods
- Base model: GPT-J (6.7B); ablation on GPT-2 family (124M–1.6B) for scaling analysis.
- Dataset: Subset of CCNet used for both pretraining and API-call augmentation (C → C*).
- Tools: QA system (Atlas, retrieval-augmented), BM25 Wikipedia search, four-operation calculator, calendar (returns current date), NLLB machine translation (200 languages).
- Filtering thresholds τf and τs tuned per tool; up to k=10 candidate API positions and m samples per position.
- Evaluation: Zero-shot prompted inference on LAMA (SQuAD, Google-RE, T-REx), ASDiv/SVAMP/MAWPS (math), WebQS/NQ/TriviaQA (open-domain QA), MLQA (multilingual), TEMPLAMA/DATESET (temporal reasoning); greedy decoding with top-k=10 disposition for API token.

## Key findings — cite these

- Toolformer (6.7B) outperforms GPT-3 (175B, ~25× larger) on LAMA T-REx (53.5 vs. 39.8) and all three math benchmarks (ASDiv: 40.4 vs. 14.0; SVAMP: 29.4 vs. 10.0; MAWPS: 44.0 vs. 19.8) in zero-shot settings.
- Tool-use ability only emerges reliably at ≥775M parameters; smaller models gain no measurable benefit from API calls.
- Fine-tuning on the augmented corpus C* does not degrade core LM perplexity relative to fine-tuning on the original corpus C (10.5 vs. 10.5 on CCNet), confirming that tool-use learning does not trade off against general language ability.
- The model learns near-perfect tool routing without explicit supervision: calculator used in 97.9% of math examples; QA tool in 98.1% of LAMA examples.
- Sample inefficiency is severe: >1M documents yield only ~1,000 useful calculator examples at τf=1.0, limiting practical replication.

### Business-level takeaway
The headline result is that a much smaller, cheaper model beat a model 25× its size — because it knew when to pick up the phone and call a specialist (the calculator, the search engine) instead of trying to answer from memory. For a resource-constrained retail AI system, this is a directly relevant signal: you do not need a massive model if you can equip a leaner one with the right external tools and teach it when to use them. The trade-off is data preparation cost — training on tool calls requires processing millions of documents to get enough useful examples, which has compute implications.

## Direct quotes — copy verbatim, include page/section

> "Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction." (Abstract)

> "An API call is helpful to M if providing it with both the input and the output of this call makes it easier for the model to predict future tokens, compared to not receiving the API call at all, or receiving only its input." (p. 3, Section 2 – Filtering API Calls)

> "The ability to leverage the provided tools only emerges at around 775M parameters: smaller models achieve similar performance both with and without tools." (p. 8, Section 4.4)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Tangentially relevant — the finding that a smaller tool-augmented model can outperform much larger models supports the thesis argument that computational efficiency can be achieved by routing to specialised modules rather than scaling model size.
- **SRQ2** (multi-agent coordination and recommendations): Directly relevant — Toolformer's self-directed tool selection is a foundational mechanism for agent-tool coordination; illustrates how a single LLM agent can autonomously route to specialised external modules, analogous to coordinator-to-specialist delegation in a multi-agent system.
- **SRQ3** (contextual information improving AI capabilities): Directly relevant — the paper's central thesis is that external tool outputs (retrieved facts, computed values, translated text, current date) improve prediction and task accuracy; maps to enriching a retail AI agent with contextual signals such as consumer surveys or promotional calendars.
- **SRQ4** (predictive AI vs. descriptive BI): N/A

## Where this goes in our thesis
- **Ch.2, Section on LLM Agent Architecture**: Cite as the foundational mechanism for tool-augmented agents; establishes the self-supervised paradigm for tool routing without human annotation overhead.
- **Ch.3 (System Design)**: Reference the API-call interleaving and filtering pattern as precedent for our coordinator agent invoking forecasting and data-retrieval modules during inference.

## What this paper does NOT cover (gap it leaves)

Toolformer addresses factual and arithmetic tool use in a general NLP setting but does not consider structured tabular data retrieval, time-series forecasting tools, or resource-constrained deployment budgets — the thesis extends tool-augmented agency into a retail analytics context with explicit computational efficiency constraints (≤8 GB RAM) and domain-specific heterogeneous data signals.

## Strength
- Rigorous self-supervised filtering criterion (perplexity reduction) provides a principled, annotation-free method for identifying when tool use is genuinely beneficial — directly citable as methodological precedent for agent tool-routing design.
- Zero-shot evaluation across diverse task types (factual, mathematical, multilingual, temporal) provides strong evidence of generality, not task-specific overfitting.

## Weaknesses
- No chained tool calls: each API is invoked independently, preventing multi-step reasoning (e.g., retrieve date → query QA with that date); a notable gap relative to a multi-agent design requiring sequential tool orchestration.
- Severe sample inefficiency (millions of documents → hundreds of useful calculator examples at τf=1.0) limits direct adoption of the training pipeline under resource constraints.

## My critical assessment


# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
-
## Physical References
+
## Other References
-
