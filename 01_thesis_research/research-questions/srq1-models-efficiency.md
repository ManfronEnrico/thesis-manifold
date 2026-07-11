---
name: SRQ1 — Predictive Models & Computational Efficiency
description: Sub-research question 1 scope and context for NotebookLM curation
updated: 2026-04-20
---

# SRQ1: Predictive Models & Computational Efficiency

## Research Question

**Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints?**

## Scope

This notebook focuses on understanding:
1. **Predictive modeling approaches**: Traditional statistics, ML, deep learning, ensemble methods
2. **Accuracy metrics**: What makes a model accurate in business forecasting?
3. **Computational efficiency**: Memory usage, training time, inference latency
4. **Cloud constraints**: How computational budgets affect model selection
5. **Trade-offs**: Identifying Pareto frontiers between accuracy and efficiency

## Paper Selection Criteria

Include papers on:
- Classical forecasting methods (ARIMA, exponential smoothing, etc.)
- Machine learning for regression/forecasting (regression trees, SVMs, etc.)
- Deep learning architectures (RNNs, LSTMs, Transformers)
- Ensemble methods and hybrid approaches
- Hyperparameter optimization and AutoML
- Model compression and efficient inference
- Benchmarking studies comparing multiple approaches
- Real-world deployments with computational constraints
- Time series forecasting specifically

Exclude papers on:
- Pure classification problems (not regression/forecasting)
- Generative models (diffusion, GANs) unless applied to forecasting
- Purely theoretical complexity analysis without empirical evaluation

## Key Concepts to Track

When reading papers, look for:
- **Accuracy**: What metrics? (MAE, RMSE, MAPE, etc.)
- **Efficiency**: Training time? Inference time? Memory footprint?
- **Data requirements**: How much historical data needed?
- **Scalability**: How does performance degrade as data grows?
- **Practical insights**: What works in practice vs. theory?

## Writing Roadmap (for main thesis)

These papers will inform Chapter 3 (Methodology) and Chapter 4 (Models):
- Section 3.1: Forecasting problem formulation
- Section 4.1: Model selection approach
- Section 4.2: Candidate models and their characteristics
- Section 4.3: Efficiency analysis and trade-offs

## Next Steps

1. Use NotebookLM to summarize model landscape
2. Ask: "What are the main predictive modeling families and their efficiency characteristics?"
3. Identify papers showing empirical trade-off analysis
4. Extract comparison tables and key findings
