---
title: "On Accelerating Edge AI: Optimizing Resource-Constrained Environments"
authors: Sicong Liu, Bin Guo, Zhiwen Yu, et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2501.15014
tier: 1 — Core Essential
score: 9
angles: [Cloud/Resource-Constrained AI]
srqs: [SRQ1]
---

## Core argument
Achieving production-grade AI on edge/resource-constrained hardware requires co-design across model compression (quantization, pruning, knowledge distillation), hardware-aware architecture search, and adaptive inference scheduling — no single technique is sufficient.

## Method
Comprehensive survey + empirical benchmarks. Tests combinations of: INT8/INT4 quantization, structured/unstructured pruning, knowledge distillation, NAS with hardware-in-the-loop, dynamic early-exit inference. Hardware: ARM Cortex-M, NVIDIA Jetson, Raspberry Pi 4. Tasks: vision and NLP.

## Key finding
Knowledge distillation + INT8 quantization achieves best accuracy-latency trade-off: retains 94–97% of full-precision accuracy at 3–5× inference speedup on ARM-class hardware.

## Key quote
> "Knowledge distillation with INT8 quantization retains 94–97% of full-precision model accuracy while achieving 3–5x inference speedup on ARM-class edge hardware."

## Relevance to thesis
- SRQ1: technical toolkit for the lightweight ML benchmark — quantifies acceptable accuracy loss vs. latency/memory savings
- Provides the methodology for the thesis's memory profiling at Phase 4

## Gap / limitation
Focuses on model-level optimisations only — does not address multi-model orchestration overhead, data pipeline latency, or trade-off between model accuracy and downstream decision quality. Does not consider contextual inputs (SRQ3) reducing computational burden through selective inference.
