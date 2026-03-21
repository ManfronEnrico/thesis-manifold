---
title: "Edge Intelligence Unleashed: A Survey on Deploying Large Language Models in Resource-Constrained Environments"
authors: Semerikov, S.O., Vakaliuk, T.A., Kanevska, O.B., Ostroushko, O.A., & Kolhatin, A.O.
year: 2025
venue: Journal of Edge Computing, Vol. 4, No. 2. https://doi.org/10.55056/jec.1000
url: https://acnsci.org/journal/index.php/jec/article/view/1000
companion: "Empowering Edge Intelligence: A Comprehensive Survey on On-Device AI Models" — Wang et al. (2025), arXiv:2503.06027, ACM Computing Surveys. https://doi.org/10.1145/3724420
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: SRQ1, Resource-Constrained Deployment, Memory Efficiency, Model Compression
srqs: [SRQ1]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Deploying LLMs and AI models in resource-constrained environments (edge devices, memory-limited cloud) requires co-design of model compression (quantization, pruning, knowledge distillation), hardware-aware architecture search, and adaptive inference scheduling — no single technique achieves production-grade accuracy-latency-memory trade-offs alone.

## Method
Comprehensive survey of literature from 2022–2024 covering: model compression techniques (INT8/INT4 quantization, structured/unstructured pruning, knowledge distillation, low-rank approximation), hardware-aware NAS, dynamic early-exit inference, and model offloading/speculative decoding strategies. Benchmarked on ARM Cortex-M, NVIDIA Jetson, and Raspberry Pi hardware across vision and NLP tasks.

## Key finding
Knowledge distillation combined with INT8 quantization achieves the best accuracy-latency trade-off: retaining 94–97% of full-precision accuracy at 3–5x inference speedup on ARM-class hardware; edge TPU inference can operate with as little as 42–131 MB RAM, while Jetson Nano GPU requires ~1.2 GB for comparable tasks.

## Relevance to thesis
- SRQ1 (Ch.2.2, Ch.6): provides the technical vocabulary and benchmarking methodology for the thesis's memory profiling phase — quantization and distillation trade-offs inform which lightweight ML models (LightGBM, ARIMA, Prophet) are viable within 8GB
- Ch.9 (Limitations and Future Work): edge AI findings establish the upper bound on model complexity achievable under the thesis's resource constraint
- Directly addresses the thesis's central architectural justification: 8GB RAM constraint forces model selection decisions

## Gap / limitation
Survey focuses on model-level optimisations for vision/NLP tasks; does not address multi-model orchestration overhead in agentic systems, nor the specific memory footprints of tabular ML models used in retail demand forecasting.

> Note: a related annotation exists at `edge_ai_resource_constrained.md` (Scraping Run 1, covering arXiv:2501.15014 by Liu et al. 2025). This file targets the broader survey literature on edge AI deployment from 2022–2024. Both records should be retained — they cover complementary sources.
