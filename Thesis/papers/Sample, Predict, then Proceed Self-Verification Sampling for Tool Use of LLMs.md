
---
title: "Sample, Predict, then Proceed: Self-Verification Sampling for Tool Use of LLMs"
authors: Anonymous
year: 2025
venue: Submitted to 39th Conference on Neural Information Processing Systems (NeurIPS 2025)
doi:
apa7: >
  Anonymous. (2025). Sample, predict, then proceed: Self-verification sampling for tool use of LLMs.
  *Submitted to NeurIPS 2025*.
read_date: 2026-03-21
read_depth: full
---

## In one sentence

LLMs can be fine-tuned to predict the future state of their own tool calls (DyMo), enabling a self-verification sampling strategy (SVS) that selects the most reliable trajectory at test time without querying the live environment — reducing hallucinations and allowing the model to refuse uncertain outputs.

## Method

Post-training augmentation (SFT + RL) on an 8B model to generate both function calls and predicted resulting states. SVS at inference: sample k candidate tool calls, predict resulting states for each, select the best via scoring function. Evaluated on Berkeley Function Calling Leaderboard V2 (BFCL-V2). Compared against GPT-4o.

## Key findings — cite these

- DyMo reduces hallucinations in SFT models and improves success rates in RL-trained models on BFCL-V2
- An **8B model with DyMo matches and occasionally surpasses GPT-4o** on BFCL-V2
- Correct tool calls are retrievable for **over 93% of prompts** using Best-of-N decoding
- SVS enables models to **refuse uncertain completions**, improving output reliability without oracle access
- RL models consistently outperform SFT models in hallucination mitigation

## Direct quotes — copy verbatim, include page/section

> "Many real-world applications may not rely on a verifier to improve test-time sampling, especially when the LLM interacts with the world as in Agentic scenarios." (Section 1, p. 1)

> "The environment status states after executing an action and cannot be easily reverted — the bank account is reduced after a payment!" (Section 1, p. 2)

> "By allowing the model to refuse uncertain completions, our approach produces more reliable outputs in scenarios where correctness is essential." (Section 6, p. 12)

## Where this goes in my thesis

- **Ch.2, Section 2.X (LLM agents / tool use)**: Cite DyMo as a state-of-the-art method for reliable tool-calling in stateful environments — directly relevant to how our agents interact with data pipelines and forecasting tools
- **Ch.5 (Framework Design)**: SVS's "refuse if uncertain" mechanism is a design precedent for our Validation Agent's confidence thresholding — agents should withhold low-confidence recommendations rather than hallucinate
- **Ch.8 (Evaluation / SRQ3–SRQ4)**: The reliability metric (proportion of outputs verified correct) is a citable evaluation protocol analogous to our confidence-scored recommendation quality
- **Ch.9 (Limitations / Related Work)**: Acknowledge that our system does not implement internal state prediction — DyMo represents a more sophisticated future direction

## What this paper does NOT cover (gap it leaves)

DyMo/SVS focuses on single-agent tool-call reliability in general-purpose benchmarks; it does not address how reliability and uncertainty propagate across a **multi-agent pipeline** where one agent's noisy tool output becomes the input to a downstream synthesis or recommendation agent — the exact setting of our thesis.

## My critical assessment



**My critical assessment**

- Introduces a **novel and powerful reliability mechanism** by enabling LLMs to predict the outcomes of their own tool calls, reducing dependence on external verification
- Demonstrates that **self-verification at inference time (SVS)** can significantly improve reliability and reduce hallucinations without requiring interaction with the live environment
- Key contribution: the ability to **refuse uncertain outputs**, which is highly aligned with the thesis’s emphasis on reliability and controlled decision-making
- Shows that relatively small models (8B) can achieve **near state-of-the-art performance** through improved reasoning and verification strategies rather than scale alone
- However, the approach is limited to **single-agent settings** and does not address error propagation across multi-agent pipelines
- Assumes the model can accurately predict future states, which may not hold in **data-driven, stochastic environments** such as retail forecasting
- Does not consider **resource constraints** or the overhead introduced by sampling multiple trajectories at inference time
- Focuses on tool-call correctness rather than **end-to-end decision quality** or synthesis of heterogeneous model outputs
- Therefore, highly relevant as a **state-of-the-art approach to reliability and uncertainty handling in LLM agents**, but limited in addressing the complexities of multi-agent orchestration and domain-specific decision pipelines central to the thesis