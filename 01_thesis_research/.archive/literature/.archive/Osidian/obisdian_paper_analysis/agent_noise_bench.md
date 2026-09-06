---
title: "AgentNoiseBench: Benchmarking Robustness of Tool-Using LLM Agents Under Noisy Conditions"
authors: Ruipeng Wang, Yuxin Chen, Yukai Wang, Chang Wu, Junfeng Fang, Xiaodong Cai, Qi Gu, Hui Su, An Zhang, Xiang Wang, Xunliang Cai, Tat-Seng Chua
year: 2026
venue: arXiv preprint (arXiv:2602.11348)
url: https://arxiv.org/abs/2602.11348
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: SRQ2, Agent Robustness, Tool Use Evaluation, Validation Framework
srqs: [SRQ2, SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
Current tool-using LLM agents are evaluated under idealized assumptions that ignore real-world noise; AgentNoiseBench introduces a systematic framework for injecting controllable noise (user-noise and tool-noise) into agent benchmarks while preserving task solvability, revealing consistent and significant performance degradation across all tested models.

## Method
Noise taxonomy: two primary noise categories — user-noise (ambiguous or corrupted instructions) and tool-noise (noisy, incomplete, or erroneous tool outputs). Automated noise injection pipeline applied to existing agent-centric benchmarks. Evaluated across a wide range of LLMs with diverse architectures and parameter scales. Results compare performance under clean vs. noisy conditions across multiple noise intensity levels.

## Key finding
All evaluated agentic models show consistent and substantial performance degradation under realistic noise conditions, with larger models not consistently more robust than smaller ones — demonstrating that noise robustness is not an emergent property of scale and must be explicitly addressed in agent design and evaluation.

## Relevance to thesis
- SRQ2 (Ch.2.1, Ch.5): directly informs the thesis's agent architecture design — noisy retail data (missing values, promotional anomalies, reporting delays in Nielsen data) constitutes real-world tool-noise that the thesis framework must handle
- SRQ3 (Ch.8 Validation, Level 2): AgentNoiseBench's noise taxonomy provides a methodological blueprint for the thesis's agent behaviour monitoring (Level 3 validation)
- Strengthens the novelty argument: existing agent frameworks do not systematically address noise robustness in business data environments

## Gap / limitation
Published February 2026 — very recent, not yet peer-reviewed; focuses on general agent benchmarks rather than business/forecasting-specific task structures. Noise types may not fully capture the structured missingness patterns in retail scanner data.
