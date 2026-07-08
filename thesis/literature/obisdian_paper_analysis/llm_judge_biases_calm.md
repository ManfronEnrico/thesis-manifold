---
title: "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge"
authors: [Ye, Jiayi, Wang, Yanbo, Huang, Yue, Chen, Dongping, Zhang, Qihui, Moniz, Nuno, Gao, Tian, Geyer, Werner, Huang, Chao, Chen, Pin-Yu, Chawla, Nitesh V., Zhang, Xiangliang]
year: 2024
venue: "arXiv:2410.02736 [PREPRINT — OpenReview/ICLR submission; acceptance UNCERTAIN — verify before final]"
url: https://arxiv.org/abs/2410.02736
tier: 2 — High relevance (preprint; peer-review uncertain)
score: 6
srqs: [SRQ4]
tags: [gap-H, llm-as-judge, evaluation-validity, preprint]
ch2_section: "2.5 Reliability/uncertainty & evaluation of agentic outputs"
---

## Core argument
LLM-as-a-judge is widely used for evaluation but exhibits systematic biases that undermine reliability; comprehensive automated bias assessment was previously lacking.

## Method
CALM framework: an "attack-and-detect" approach injecting 12 bias types via principle-guided perturbations, measuring Robustness Rate and Consistency Rate across fact-related, refinement-aware, and alignment datasets.

## Key finding
Position bias intensifies with more answer candidates; self-enhancement bias is widespread; biases are more pronounced on alignment than fact tasks; Claude-3.5 most resilient overall. Recommends separate models for generation vs evaluation and explicit bias-detection mechanisms.

## Key quote
> "significant biases persist in certain specific tasks" despite strong overall judge performance.

## Relevance to thesis
- [SRQ4]: Direct **threat-to-validity** basis for the thesis's LLM-as-judge evaluation — justifies using a separate judge model and explicitly acknowledging judge bias as a limitation.

## Gap / limitation
Preprint (peer-review uncertain). Supports judge-design caution; does **not** validate the thesis's specific pilot as bias-free (CALM was not run on our outputs).
