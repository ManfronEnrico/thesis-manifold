---
title: "ANAH: Analytical Annotation of Hallucinations in Large Language Models"
authors: Ziwei Ji, Yuzhe Gu, Wenwei Zhang, Chengqi Lyu, Dahua Lin, Kai Chen
year: 2024
venue: Proceedings of ACL 2024 (62nd Annual Meeting of the Association for Computational Linguistics), Long Papers, pp. 8135–8158
url: https://aclanthology.org/2024.acl-long.442/
tier: 2 — Recommended (Scraping Run 2)
score: 8
angles: SRQ2, LLM Reliability, Hallucination Evaluation, Validation Framework
srqs: [SRQ2, SRQ3]
status: CONFIRMED — in corpus (2026-03-15)
---

## Core argument
LLM hallucinations can be systematically quantified at sentence level through a bilingual (Chinese-English) benchmark (ANAH) that combines reference retrieval, hallucination-type classification, and content correction — enabling the training of automated hallucination annotators that approach GPT-4 performance.

## Method
Human-in-the-loop annotation pipeline producing ~12,000 sentence-level annotations for ~4,300 LLM responses across 700+ topics in a knowledge-based QA setting. Each sentence is annotated with: a retrieved reference fragment, a hallucination type label (factual error, fabrication, etc.), and a corrected version. Annotator models trained on ANAH are benchmarked against open-source LLMs, GPT-3.5, and GPT-4.

## Key finding
A generative annotator fine-tuned on ANAH surpasses all open-source LLMs and GPT-3.5, reaches performance competitive with GPT-4, and generalises to unseen question domains — demonstrating that hallucination detection can be automated at scale without closed-model dependence.

## Relevance to thesis
- SRQ2 (Ch.2.1, Ch.5): informs the thesis's treatment of LLM output reliability — hallucination risk is a key constraint on using LLMs for managerial recommendations in business contexts
- SRQ3 (Ch.8 Validation): ANAH's evaluation methodology (sentence-level annotation + type taxonomy) provides a blueprint for the thesis's Level 2 recommendation quality validation
- CBS Compliance: supports the thesis's claims about LLM trustworthiness limitations with empirical evidence

## Gap / limitation
ANAH covers knowledge-based QA; its hallucination taxonomy does not directly address numerical/forecasting errors or the specific failure modes of LLMs reasoning over quantitative business data (e.g. misattributing trend directions).
