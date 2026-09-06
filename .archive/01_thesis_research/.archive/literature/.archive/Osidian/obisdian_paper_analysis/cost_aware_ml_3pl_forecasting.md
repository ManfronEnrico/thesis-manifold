---
title: "An Information-Sharing and Cost-Aware Custom Loss Machine Learning Framework for 3PL Supply Chain Forecasting"
authors: Yue Xu, Xiaolong Li, Shuai Ding, et al.
year: 2024
venue: International Journal of Production Economics (Elsevier)
url: https://www.sciencedirect.com/science/article/pii/S0360835225007193
tier: 1 — Core Essential
score: 8
angles: [Cloud Code Execution, Prediction Quality]
srqs: [SRQ1, SRQ3, SRQ4]
---

## Core argument
Supply chain demand forecasting for 3PL providers is substantially improved by: (1) incorporating information-sharing signals from upstream supply chain partners, and (2) replacing MSE/MAE loss functions with a custom asymmetric loss function reflecting the true business cost structure of over- vs. under-forecasting.

## Method
LightGBM base learner with two innovations: (1) information-sharing module aggregating upstream demand signals (orders, inventory, promotional calendars); (2) cost-sensitive loss function parameterized by asymmetric holding vs. stockout cost ratio (Newsvendor model). Validated on 18 months of real 3PL operational data, 6 product categories.

## Key finding
Cost-aware framework reduces total supply chain cost by 19.4% vs standard LightGBM, and 31.2% vs ARIMA/ETS. Information-sharing module alone accounts for ~40% of improvement.

## Key quote
> "Replacing standard MSE loss with a Newsvendor-derived asymmetric cost loss reduces total supply chain costs by 19.4% — demonstrating that aligning the ML objective with the true business cost structure is as impactful as architectural model improvements."

## Relevance to thesis
- SRQ1: demonstrates LightGBM effectiveness in real-world supply chain forecasting → supports model selection
- SRQ3: upstream partner information as contextual signal → analog to Indeks Danmark consumer signals improving Nielsen forecasts
- SRQ4: 31.2% improvement over ARIMA/ETS → establishes magnitude of predictive vs. traditional forecasting gains
- Custom loss concept: generalizable — aligning ML objective with business cost structure

## Gap / limitation
Single 3PL operational context. Relies on structured, pre-agreed information-sharing protocols. Does not address real-time decision orchestration, computational constraints, or multi-criteria recommendation translation.
