
---
aliases:
learning_text_title: "SLM-Bench: A Comprehensive Benchmark of Small Language Models on Environmental Impacts"
learning_text_venue: Findings of the Association for Computational Linguistics: EMNLP 2025
learning_text_doi:
learning_text_apa7: "Pham, N. T., Kieu, T., Nguyen, D.-M., Xuan, S. H., Duong-Trung, N., & Le-Phuoc, D. (2025). SLM-Bench: A comprehensive benchmark of small language models on environmental impacts. In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 21369–21392). Association for Computational Linguistics."
learning_list_authors:
  - Pham, N. T.
  - Kieu, T.
  - Nguyen, D.-M.
  - Xuan, S. H.
  - Duong-Trung, N.
  - Le-Phuoc, D.
learning_list_topic:
  - Small Language Models
  - Benchmarking
  - Resource-Constrained AI
  - Computational Efficiency
  - Energy Consumption
  - Environmental Impact
  - Multi-Dimensional Evaluation
learning_list_srq:
  - SRQ1
  - SRQ2
learning_list_chapter:
  - Ch.3
  - Ch.5
  - Ch.6
learning_number_release_year: 2025
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: High
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-22
cssclasses:
---

# AI Assessment
---
## In one sentence

SLM-Bench establishes the first systematic benchmarking framework for small language models that simultaneously quantifies task accuracy, computational cost (#params, FLOP, runtime), and environmental consumption (energy, CO2, cost) across 15 models, 9 tasks, and 4 hardware configurations — demonstrating that no single SLM dominates all dimensions and that deployment decisions require explicit multi-criteria trade-off analysis.

## Core Ideas
- No existing benchmark evaluates SLMs on correctness, computation, AND consumption simultaneously — the absence of a multi-dimensional evaluation standard forces practitioners into implicit trade-off decisions without empirical grounding, particularly in resource-constrained deployments
- Trade-offs among SLMs are task- and hardware-dependent: models that excel in accuracy often carry disproportionate energy or runtime costs; optimal model selection requires specifying a deployment constraint profile (accuracy floor, memory ceiling, energy budget) rather than a single ranked list
- Hardware configuration is a confounding variable that prior benchmarks ignore — the same model can vary substantially in energy consumption, runtime, and even accuracy across CPU/GPU configurations; controlled hardware evaluation is a methodological requirement for fair comparison
- The 11-metric evaluation framework (correctness: F1/BLEU/ROUGE/METEOR/perplexity; computation: #params/FLOP/runtime; consumption: energy/CO2/cost) provides a replicable protocol for multi-criteria model selection that is directly extensible to non-NLP model benchmarking

## Methods
- 15 SLMs evaluated: 1.1B–7B parameter range including TinyLlama-1.1B, Phi-1.5B/3-3.8B, Gemma-2B/3-1B, Mistral-7B, LLaMA-2-7B, LLaMA-3.2-1B, Zephyr-7B, and others
- 9 NLP task types: classification, reading comprehension, reasoning, text generation, question answering, common sense, problem solving, topic extraction, sentiment analysis
- 23 datasets across 14 domains including healthcare, legal, finance, education, news
- 4 hardware configurations for controlled cross-hardware comparison
- 11 evaluation metrics: accuracy metrics (F1, BLEU, ROUGE, METEOR, perplexity), computational metrics (#params, FLOP, runtime), consumption metrics (energy kWh, CO2 kg, cost USD)
- Open-source pipeline published at github.com/HiveIntel/SLM-Bench

## Key findings — cite these
- Trade-off between accuracy and efficiency is not monotonic — some SLMs achieve high accuracy with acceptable energy cost, while others sacrifice accuracy without proportional efficiency gains
- No single SLM dominates across all 11 metrics — model selection must be anchored to a specific deployment constraint profile
- Hardware configuration significantly affects both accuracy and energy metrics — benchmarks conducted on uncontrolled hardware are not directly comparable
- Smaller parameter count does not guarantee energy efficiency — architectural choices (attention mechanism, tokeniser, quantisation) interact with hardware in ways that decouple parameter count from runtime energy consumption

## Direct quotes — copy verbatim, include page/section
> "Unlike prior benchmarks, SLM-Bench quantifies 11 metrics across correctness, computation, and consumption, enabling a holistic assessment of efficiency trade-offs." (Abstract)

> "Our findings highlight the diverse trade-offs among SLMs, where some models excel in accuracy while others achieve superior energy efficiency." (Abstract)

> "This lack of standardized evaluation hinders a deeper understanding of their practical implications, particularly in resource-constrained environments where efficiency and sustainability are paramount." (Section 1)

> "SLM-Bench sets a new standard for SLM evaluation, bridging the gap between resource efficiency and real-world applicability." (Abstract)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): Directly relevant — the 11-metric multi-dimensional benchmarking methodology (accuracy + computation + consumption) is the methodological precedent for the thesis's ML model benchmark table in Ch.6; specifically legitimises memory profiling and runtime measurement alongside MAPE/RMSE as evaluation dimensions, not merely accuracy metrics
- **SRQ2** (multi-agent coordination and recommendations): Relevant for LLM/SLM selection — the SLM benchmark data (which models fit within constrained RAM budgets and retain acceptable task performance) directly informs which model is viable as the orchestration layer within the thesis's ≤8GB constraint after ML models are loaded
- **SRQ3** (contextual information improving AI capabilities): N/A
- **SRQ4** (predictive AI vs. descriptive BI): N/A

## Where this goes in our thesis
- **Ch.3, Section 3.X (Benchmarking Methodology)**: Cite as methodological precedent for multi-criteria model evaluation — the correctness/computation/consumption framework justifies why the thesis benchmark table includes memory footprint and runtime alongside forecasting accuracy metrics
- **Ch.5, Section 5.X (LLM/SLM Selection)**: Cite when justifying the choice of orchestration model within the ≤8GB RAM constraint — the SLM-Bench results provide empirical grounding for selecting a sub-7B model as the synthesis layer LLM without requiring cloud-scale compute
- **Ch.6 (Model Benchmark & Selection)**: Cite in the benchmark design section to frame the thesis's multi-metric evaluation as consistent with emerging best practice in resource-constrained AI benchmarking

## What this paper does NOT cover (gap it leaves)

SLM-Bench evaluates SLMs exclusively on standard NLP task accuracy — it does not address time series forecasting, multi-model ensemble synthesis, or the specific challenge of integrating an SLM orchestrator within a constrained pipeline that simultaneously runs ML forecasting models, which is the architectural constraint that makes the thesis's benchmarking problem distinct.

## Strength
- EMNLP 2025 Findings — top-tier ACL venue; multi-institutional authorship (TU Berlin, Aalborg, DFKI) with open-source replication pipeline adds credibility and reproducibility
- The 11-metric framework is directly actionable — provides a citable, structured evaluation template that the thesis can adapt for its own benchmark table
- Hardware-controlled evaluation methodology is a replicable protocol contribution applicable beyond NLP

## Weaknesses
- NLP task domain (classification, QA, reasoning) is entirely separate from time series forecasting — accuracy metrics (BLEU, ROUGE, F1) are not transferable to the thesis's forecasting evaluation (MAPE, RMSE, hit rate)
- No RAM profiling at the pipeline level — individual model memory footprint is reported via #params but not peak RAM under concurrent multi-model deployment, which is the specific constraint the thesis faces
- Benchmark does not include quantised models or GGUF/GGML inference formats that are most relevant for sub-8GB deployment

## My critical assessment

- **Strengths:** Proposes a comprehensive, multi-dimensional benchmarking framework (accuracy, computation, and environmental consumption), highlighting that model selection in resource-constrained settings requires explicit trade-off analysis rather than single-metric optimisation; strong methodological contribution with controlled hardware evaluation.
    
- **Weaknesses:** Focuses exclusively on NLP tasks and SLM performance, limiting direct applicability to time series forecasting; lacks pipeline-level evaluation (e.g., combined memory usage across multiple models) and does not consider integration with downstream decision-support systems.
    
- **Relevance to thesis:** Provides a direct methodological precedent for your **multi-criteria benchmarking approach** (accuracy, runtime, memory), and supports the need to select an LLM/SLM that fits within the ≤8 GB RAM constraint while maintaining acceptable performance.
    
- **Gap addressed by your work:** Does not address **forecasting models, ensemble synthesis, or joint optimisation of ML + LLM pipelines under shared resource constraints**; your thesis extends this by applying multi-dimensional benchmarking to a **hybrid retail forecasting system**, where both predictive models and orchestration agents compete for limited computational resources.

# Manual Assessment
---


---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
-
## Link References
- https://github.com/HiveIntel/SLM-Bench
- https://swarm.hiveintel.ai/leaderboard/
## Physical References
+
## Other References
-
