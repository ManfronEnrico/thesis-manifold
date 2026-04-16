---
name: Skills Demo Examples
description: 10 concrete demonstrations with expected outputs showing how to use imported skills
version: 1.0
date: 2026-04-16
---

# Skills Demo Examples — 10 Concrete Use Cases

Each demo shows:
- **What skill to use**: The `/skill-name` command
- **What to ask**: Exact prompt to try
- **Expected output**: What you should see
- **Chapter alignment**: Which thesis chapter benefits
- **Time to run**: How long it takes

Try these in order, 5 minutes each.

---

## DEMO 1: Exploratory Data Analysis (Chapter 4)

### What to Use
```
/exploratory-data-analysis
```

### What to Ask
```
"Profile the Nielsen demand data for me. Check:
- Missing values per SKU
- Outliers in daily demand
- Seasonal patterns
- Distribution of demand across product categories"
```

### Expected Output
```
=== Nielsen Data Profile ===

Dataset: 120,000 rows × 5 columns (17.5 MB)
- Columns: date, sku_id, demand, category, store_id
- Date range: 2020-01-01 to 2023-03-31 (1185 days)

Missing Values:
- demand: 2.3% (2,760 rows)
- sku_id: 0%
- category: 0%

Demand Distribution:
- Mean: 127.4 units/day
- Median: 89.2 units/day
- Std Dev: 185.6 units/day
- Min: 0 | Max: 2,847 | IQR: [34, 198]

Outliers (>Q3 + 1.5*IQR):
- Count: 1,247 outliers (1.04% of data)
- Potential causes: promotions, holidays, supply constraints

Seasonal Patterns:
- Strong weekly seasonality (Fri/Sat peak)
- Monthly trend: higher in months 11-12, lower in 8-9
- ACF lag-1 autocorrelation: 0.67 (strong)

Category Breakdown:
- Beverages: 42% of records
- Snacks: 31% of records
- Frozen: 27% of records

Recommendation: Handle 2.3% missing values via
forward-fill (seasonal patterns present)
```

### Chapter Alignment
**Chapter 4 — Data Characteristics**
- Data quality metrics
- Seasonal structure
- Outlier identification

### Time to Run
⏱️ 5 minutes

---

## DEMO 2: Aeon Time Series Forecasting (Chapter 6, SRQ1)

### What to Use
```
/aeon
```

### What to Ask
```
"Compare 3 ensemble forecasting methods on Nielsen demand data:
1. AutoEnsemble with voting
2. ARIMA ensemble
3. Neural network (LSTM) ensemble

Train on 2022 data, test on first 100 days of 2023.
Show RMSE, MAE, and ensemble voting breakdown."
```

### Expected Output
```
=== Aeon Ensemble Forecasting Results ===

Training Period: 2022-01-01 to 2022-12-31 (365 days)
Test Period: 2023-01-01 to 2023-04-10 (100 days)
SKUs evaluated: Top 20 by volume

Method 1: AutoEnsemble (Voting)
├─ Components: RandomForest, GradientBoosting, ExtraTrees
├─ Voting rule: Weighted average (weights optimized on validation)
├─ Test RMSE: 42.3 units
├─ Test MAE: 28.7 units
└─ Component weights: RF(0.40), GB(0.35), ET(0.25)

Method 2: ARIMA Ensemble
├─ Components: 5 ARIMA configs (1,1,1), (0,1,2), (2,1,0), etc.
├─ Voting: Median ensemble
├─ Test RMSE: 45.8 units
├─ Test MAE: 31.2 units
└─ Improvement over single ARIMA: -6.2% RMSE

Method 3: Neural Network Ensemble (LSTM)
├─ Components: 3 LSTMs (64, 128, 256 hidden units)
├─ Window size: 28-day lookback
├─ Test RMSE: 38.9 units (BEST)
├─ Test MAE: 25.4 units (BEST)
└─ Training time: 3.2 minutes

Winner: Method 3 (LSTM Ensemble)
├─ RMSE improvement vs. baseline: 14.2%
├─ MAE improvement vs. baseline: 16.8%
└─ Stability: High (low variance across SKUs)
```

### Chapter Alignment
**Chapter 6 — Forecasting Performance**
- SRQ1: Multi-method comparison
- System A vs. baseline comparison
- Ensemble effectiveness

### Time to Run
⏱️ 5-7 minutes

---

## DEMO 3: Scikit-Learn Classical Baselines (Chapter 6-7, SRQ4)

### What to Use
```
/scikit-learn
```

### What to Ask
```
"Train 3 classical ML baselines on Nielsen data:
1. Logistic Regression (next-day demand high/low)
2. Random Forest (quantile regression for 25th/50th/75th percentiles)
3. SVM (next-week average demand)

Features: last-7-day rolling mean, day-of-week, category, store.
Show performance metrics (R² for regression, accuracy for classification).
Compare to System A results if available."
```

### Expected Output
```
=== Scikit-Learn Classical Baselines ===

Baseline 1: Logistic Regression (Demand High/Low Classification)
├─ Threshold: median demand (89.2 units)
├─ Accuracy: 72.3%
├─ Precision (High): 0.74 | Recall (High): 0.68
├─ AUC-ROC: 0.804
└─ Top 3 features: day_of_week(0.42), last_7day_mean(0.38), category(0.20)

Baseline 2: Random Forest (Quantile Regression)
├─ Trees: 100, max_depth: 15
├─ Q25 (low demand) R²: 0.58
├─ Q50 (median demand) R²: 0.67
├─ Q75 (high demand) R²: 0.61
├─ Average R²: 0.62
└─ Feature importance: last_7day_mean(0.48), lag_1(0.22), seasonality(0.18)

Baseline 3: SVM (Next-Week Average Demand)
├─ Kernel: RBF, C=1.0, epsilon=0.1
├─ Test R²: 0.53
├─ RMSE: 67.4 units
├─ Training time: 18.3 seconds
└─ Notable: SVM ignores short-term volatility, captures trend

Comparison: Scikit-Learn vs. System A
├─ Best scikit-learn (RF Q50): R² = 0.67, RMSE = 51.2
├─ System A result: R² = 0.79, RMSE = 38.9 (SRQ4 improvement: +18%)
├─ Statistical significance: p < 0.001 (Wilcoxon signed-rank)
└─ Conclusion: System A outperforms classical ML by 18% RMSE
```

### Chapter Alignment
**Chapter 6-7 — Baseline Comparison**
- SRQ4: "How does System A compare to traditional ML?"
- Quantitative baseline metrics
- Feature importance analysis

### Time to Run
⏱️ 5-6 minutes

---

## DEMO 4: PyMC Bayesian Uncertainty (Chapter 6-8)

### What to Use
```
/pymc
```

### What to Ask
```
"Build a Bayesian hierarchical model for Nielsen demand across categories:

Model structure:
- Global intercept + global trend
- Category-specific offsets (pooled)
- Store-specific noise

Estimate posterior for:
1. Overall trend coefficient (with uncertainty interval)
2. Category effects (ranked)
3. Posterior predictive for next week

Show credible intervals (94% and 66%)."
```

### Expected Output
```
=== PyMC Bayesian Hierarchical Model ===

Model Structure:
├─ Global intercept: μ ~ Normal(mean=100, sd=50)
├─ Global trend: β ~ Normal(mean=0, sd=5)
├─ Category offsets: α_cat ~ Normal(μ=0, σ=τ_cat) [pooled]
└─ Likelihood: demand ~ Normal(μ + β*t + α_cat, σ_obs)

Sampling: MCMC (NUTS) 2000 draws, 1000 warmup
├─ Chains: 4
├─ Divergences: 0
├─ Energy transition: 0.93 (excellent)
└─ Time: 42 seconds

Posterior Estimates:

1. Global Trend Coefficient (β)
   ├─ Mean: 0.18 units/day
   ├─ 94% Credible Interval: [0.03, 0.34]
   └─ Interpretation: ~6.5% annual growth in demand

2. Category-Specific Offsets
   ├─ Beverages: +12.4 [94% CI: +2.1, +23.1]
   ├─ Snacks: -3.7 [94% CI: -14.2, +6.8]
   └─ Frozen: +1.3 [94% CI: -8.4, +10.9]

3. Posterior Predictive (Next 7 Days)
   ├─ Day 1: 145.2 (66% CI: [124, 167], 94% CI: [89, 201])
   ├─ Day 2: 146.1 (66% CI: [125, 168], 94% CI: [88, 206])
   ├─ ...
   └─ Day 7: 151.8 (66% CI: [130, 174], 94% CI: [93, 211])

Model Quality Metrics:
├─ R²: 0.64
├─ LOO-IC (cross-validation): -2,847 (lower is better)
└─ Rank-normalized Pareto k: all < 0.5 (reliable predictions)
```

### Chapter Alignment
**Chapter 6-8 — Uncertainty Quantification**
- SRQ2: Multi-agent coordination under uncertainty
- Posterior distributions for decision-making
- Credible intervals for predictions

### Time to Run
⏱️ 6-8 minutes

---

## DEMO 5: SHAP Model Explainability (Chapter 8, SRQ2)

### What to Use
```
/shap
```

### What to Ask
```
"Explain System A's forecast for a specific day:
- SKU: Top-selling beverages on Friday, Dec 15, 2023
- System A prediction: 280 units (vs. actual 295)
- Baseline demand: ~130 units

Show:
1. SHAP force plot (which features drove the +150 unit increase?)
2. Feature importance (top 5)
3. Interaction effects (which feature pairs matter most?)"
```

### Expected Output
```
=== SHAP Model Explanation ===

Case: Beverages (top SKU) on Friday, Dec 15, 2023
- Prediction: 280 units
- Baseline: 130 units
- Delta explained: +150 units

SHAP Force Plot:
Base value: 130.0 ───────────────────── Prediction: 280.0
                  [forces to watch]

↑ POSITIVE (increases demand):
├─ last_7day_mean (avg=185): +48.2 units ████████
├─ day_of_week (Friday): +32.4 units █████
├─ holiday_promo (True): +28.7 units ████
├─ seasonality_winter (winter sales): +21.5 units ███
└─ store_shelf_stock (high): +19.2 units ███
                                      ─────────── Sum: +150.0

↓ NEGATIVE (decreases demand):
├─ competitor_discount (active): -5.1 units ▌
└─ [all others near zero]

SHAP Feature Importance (Global):
  1. last_7day_mean: 87.3 (std: 42.1)
  2. day_of_week: 34.2 (std: 18.7)
  3. seasonality: 28.9 (std: 15.4)
  4. holiday_promo: 24.1 (std: 12.6)
  5. store_stock: 15.3 (std: 8.2)

Interaction Effects (SHAP):
├─ last_7day_mean × day_of_week: +18.4 (Friday peaks are higher)
├─ seasonality × holiday_promo: +14.2 (winter holidays are strongest)
└─ last_7day_mean × store_stock: +9.3 (well-stocked stores capture more)

Prediction Confidence:
├─ Model RMSE on test set: 38.9 units
├─ 66% confidence interval: [241, 319]
├─ 94% confidence interval: [206, 354]
└─ Actual value: 295 (within 66% CI ✓)
```

### Chapter Alignment
**Chapter 8 — Explainability & Decision Support**
- SRQ2: How do multi-agent systems explain decisions?
- Prediction drivers (what matters most?)
- Feature interactions

### Time to Run
⏱️ 5-7 minutes

---

## DEMO 6: Seaborn Exploratory Plots (Chapter 4)

### What to Use
```
/seaborn
```

### What to Ask
```
"Create 4 exploratory plots of Nielsen data:
1. Distribution of daily demand (histogram + KDE overlay)
2. Demand by category (violin plot)
3. Correlation heatmap (top 10 variables)
4. Pairplot for key variables (demand, last_7day_mean, seasonality)

Color palette: 'husl', use category colors."
```

### Expected Output
```
=== Seaborn Exploratory Visualization ===

Plot 1: Demand Distribution
┌──────────────────────────────────────┐
│ histogram + KDE                      │
│         ╭╯╲  ╭─╮                     │
│    ╭────╯  ╲╱  ╲╮                    │
│   ╱  ║ ║ ║ ║    ║╲                   │
│  ║   ║ ║ ║ ║    ║ ║                  │
│  ║ ║ ║ ║ ║ ║ ║  ║ ║                  │
│  ║_║_║_║_║_║_║__║_║                  │
│  0   50  100  150  200  250 300      │
│            Demand (units)            │
│ Mean: 127.4, Median: 89.2, Skew: 1.8│
└──────────────────────────────────────┘

Plot 2: Demand by Category (Violin Plot)
┌──────────────────────────────────────┐
│ Beverages │ Snacks │ Frozen          │
│     ╱╲        ╱╲       ╱╲            │
│    ╱  ╲      ╱  ╲     ╱  ╲           │
│   │ ● │     │ ● │    │ ● │          │
│    ╲  ╱      ╲  ╱     ╲  ╱           │
│     ╲╱        ╲╱       ╲╱            │
│  [142.3]   [108.6]  [113.2]          │
│   (median)                           │
└──────────────────────────────────────┘

Plot 3: Correlation Heatmap
┌──────────────────────────────────────┐
│         Variables Correlation        │
│  ┌─────┬─────┬──────┬─────┬──────┐   │
│  │1.00 │0.67 │ 0.34 │0.18 │-0.12 │   │
│  ├─────┼─────┼──────┼─────┼──────┤   │
│  │0.67 │1.00 │ 0.41 │0.22 │ 0.05 │   │
│  ├─────┼─────┼──────┼─────┼──────┤   │
│  │0.34 │0.41 │ 1.00 │0.68 │ 0.12 │   │
│  ├─────┼─────┼──────┼─────┼──────┤   │
│  │0.18 │0.22 │ 0.68 │1.00 │ 0.45 │   │
│  ├─────┼─────┼──────┼─────┼──────┤   │
│  │-0.12│ 0.05│ 0.12 │0.45 │ 1.00 │   │
│  └─────┴─────┴──────┴─────┴──────┘   │
│  Strongest: demand ↔ last_7day (0.67)│
└──────────────────────────────────────┘

Plot 4: Pairplot
┌──────────────────────────────────────┐
│  Demand    last_7day   Seasonality   │
│    ...        ...           ...      │
│   ⋰ ⋱        ⋰ ⋱          ⋰ ⋱       │
│  ⋰ ⋱ ⋰     ⋰ ⋱ ⋰        ⋰ ⋱ ⋰     │
│    ...        ...           ...      │
└──────────────────────────────────────┘
| Strong diagonal (univariate) and
| linear relationships visible
```

### Chapter Alignment
**Chapter 4 — Data Exploration**
- Data distribution characteristics
- Category-wise comparisons
- Correlation structure
- Feature relationships

### Time to Run
⏱️ 5-6 minutes

---

## DEMO 7: Matplotlib Publication Figures (All Chapters)

### What to Use
```
/matplotlib
```

### What to Ask
```
"Create a 2×2 subplot figure for Chapter 6:
- Top-left: System A forecast vs. baseline (line plot)
- Top-right: Residual distribution (histogram)
- Bottom-left: Autocorrelation of errors (ACF plot)
- Bottom-right: Forecast error by category (box plot)

Style: publication-ready (12pt font, tight layout)
Export to: figure_ch6_validation.pdf (300 dpi)"
```

### Expected Output
```
=== Matplotlib Publication Figure ===

[Figure exported as figure_ch6_validation.pdf]

Subplot layout:
┌────────────────────┬────────────────────┐
│  System A vs Actual│  Residual Distrib  │
│  ────────────────  │  ────────────────  │
│      ╱╲            │        │││         │
│     ╱  ╲           │      ││││││        │
│    ╱    ╲──        │    │││││││││      │
│   ╱      ╲──       │  ││││││││││││    │
│  ╱        ╲────    │ │││││││││││││││  │
│  0  50  100  150   │ -50  0  +50  +100│
│        Days        │      Error       │
├────────────────────┼────────────────────┤
│   ACF Plot         │  Error by Category │
│      ╭──           │  ┌────┐            │
│     ╱  ╲           │  │ ··· │ Beverages │
│    ╱    ╲          │  ├────┤            │
│   ╱      ╲         │  │ ··· │ Snacks    │
│  ╱        ╲───     │  ├────┤            │
│ 0  5  10  15  20   │  │ ··· │ Frozen    │
│     Lags           │  └────┘            │
└────────────────────┴────────────────────┘

Figure Properties:
├─ Size: 10" × 8" (standard journal size)
├─ DPI: 300 (publication quality)
├─ Font: 12pt serif (matching thesis)
├─ Colors: colorblind-friendly palette
└─ File: 2.3 MB PDF (vector, no pixelation)
```

### Chapter Alignment
**All Chapters — Publication Figures**
- Multi-panel layouts
- Validation plots
- Figure formatting standards

### Time to Run
⏱️ 5-7 minutes

---

## DEMO 8: NetworkX Agent Architecture Graph (Chapter 5)

### What to Use
```
/networkx
```

### What to Ask
```
"Visualize System A's multi-agent architecture:

Nodes: 6 agents (Planner, Coordinator, Forecaster-A, Forecaster-B, Evaluator, Optimizer)
Edges: Communication flow (data dependencies)

Show:
1. Network graph (spring layout)
2. Node centrality (which agent is most critical?)
3. Critical path (Planner → ... → Optimizer)
4. Communication bottlenecks

Color nodes by agent type, size by centrality."
```

### Expected Output
```
=== NetworkX Agent Architecture ===

Network Graph:
         ╔═══════════════════════╗
         ║      Planner          ║ (hub: centrality 0.89)
         ╚═════╤═════════════╤═══╝
               │             │
       ╔═══════╩══╗    ╔════╩════════╗
       ║Coordinator║    ║ Evaluator   ║
       ╚═══╤═══╤══╝    ╚════╤════════╝
           │   │             │
      ╔════╩╗ ╔╩═════╗      │
      ║F-A  ║ ║F-B   ║      │
      ╚═╤══╤╝ ╚╤═════╝      │
        │  └────┴──────┬────┘
        │              │
        └──────┬───────┘
               │
         ╔═════╩══════╗
         ║ Optimizer  ║
         ╚════════════╝

Node Centrality Ranking:
  1. Planner:     0.89 (controls workflow)
  2. Coordinator: 0.73 (routes data)
  3. Evaluator:   0.62 (feedback loop)
  4. F-A:         0.58 (parallel forecasting)
  5. F-B:         0.58 (parallel forecasting)
  6. Optimizer:   0.44 (final decision)

Critical Path (Planner → Optimizer):
  [Planner] → [Coordinator] → [F-A + F-B] → [Evaluator] → [Optimizer]
  └─────────────────────────────────────────────────────────────────┘
  Path length: 5 hops
  Bottleneck: Evaluator (must process both F-A & F-B outputs)

Communication Load:
├─ Planner → Coordinator: 1200 msgs/hour (high)
├─ Coordinator → F-A/B: 2400 msgs/hour (highest)
├─ F-A → Evaluator: 600 msgs/hour
└─ Evaluator → Optimizer: 400 msgs/hour (low)

Recommendation: Parallelize Evaluator if forecast latency critical
```

### Chapter Alignment
**Chapter 5 — System A Architecture**
- Multi-agent coordination structure
- Communication flow
- Bottleneck identification
- System design justification

### Time to Run
⏱️ 5-6 minutes

---

## DEMO 9: Hypothesis Generation from Data (Chapter 5-7)

### What to Use
```
/hypothesis-generation
```

### What to Ask
```
"Generate research hypotheses from Nielsen demand data analysis:

Observations:
1. Demand peaks on Friday (35% higher)
2. Winter demand 2.3x summer demand
3. High-stock SKUs have 18% lower stockouts
4. Competitor discounts reduce demand by 12% next day

Generate 5 novel, testable hypotheses that:
- Explain these patterns
- Could be unique contributions to the thesis
- Are falsifiable (can be tested)"
```

### Expected Output
```
=== Data-Driven Hypothesis Generation ===

Generated Hypotheses (ranked by novelty & testability):

H1: Social Coordination Effect
├─ Statement: Weekend demand peaks are driven by household shopping
│  coordination (couples shop together on Friday evening)
├─ Evidence: Peak occurs Fri 5-8pm, not Fri 9am-12pm
├─ Prediction: Mixed-gender household SKUs show stronger Fri peaks
├─ Test method: Segment by product type, run ANOVA on day-of-week
└─ Novelty score: 0.82 (high)

H2: Demand Elasticity Asymmetry
├─ Statement: Consumer demand is less elastic to competitor discounts
│  than to own price increases (loss aversion)
├─ Evidence: Competitor discounts → -12% demand, own discount → +18%
├─ Prediction: Price elasticity is asymmetric (higher for price up)
├─ Test method: Logistic regression with price_direction interaction term
└─ Novelty score: 0.78

H3: Capacity Constraint Feedback Loop
├─ Statement: High shelf stock increases demand not through visibility,
│  but through social proof (abundance signals quality/freshness)
├─ Evidence: +18% lower stockouts in high-stock SKUs
├─ Prediction: Effect disappears if controlling for actual visibility
├─ Test method: Collect store photo data, tag visible shelf height
└─ Novelty score: 0.71

H4: Seasonal Demand Amplification
├─ Statement: Winter demand spike is multiplicative, not additive,
│  due to holiday party hosting behavior
├─ Evidence: 2.3x multiplier (summer 100 → winter 230, not 130)
├─ Prediction: Effect is stronger in alcohol/snacks than frozen foods
├─ Test method: Fit hierarchical model with multiplicative seasonality
└─ Novelty score: 0.68

H5: Forecast Error Autocorrelation
├─ Statement: System A's forecast errors have positive autocorrelation,
│  meaning a single shock causes multi-day demand waves
├─ Evidence: Residual ACF lag-1 = +0.34 (unexpected)
├─ Prediction: Multi-step forecast error compounds faster than theory predicts
├─ Test method: Error accumulation analysis, compare actual vs. theoretical
└─ Novelty score: 0.65

Testability & Feasibility:
✓ H1: Medium cost (data segmentation)
✓ H2: Low cost (already have price data)
✗ H3: High cost (requires store photos)
✓ H4: Low cost (hierarchical modeling)
✓ H5: Low cost (error analysis)

Recommendation for Thesis:
Test H2 (Demand Elasticity Asymmetry) - High novelty, low cost, high impact
```

### Chapter Alignment
**Chapter 5-7 — System A Insights**
- Data-driven research questions
- Novel contribution identification
- Testable hypotheses
- Unexpected findings

### Time to Run
⏱️ 5-8 minutes

---

## DEMO 10: Scholar Evaluation Literature Quality (Chapter 2)

### What to Use
```
/scholar-evaluation
```

### What to Ask
```
"Evaluate the quality of my current 37 literature papers using ScholarEval:

Rank by:
1. Relevance to thesis (forecasting + retail + constraints)
2. Citation impact (how influential is this paper?)
3. Methodology quality (are methods sound?)
4. Recency bias (balance old seminal + new cutting-edge)

Show:
- Top 10 essential papers (must keep)
- 10 good supporting papers
- 5 weak papers (could cut if space limited)
- Overall literature quality score"
```

### Expected Output
```
=== Scholar Evaluation (Ch. 2 Literature Review) ===

Total Papers Evaluated: 37
Average Citation Count: 89.2
Date Range: 2015-2024
Coverage: 5 sub-topics

TIER 1: Essential Papers (Top 10)
┌─────┬──────────────────────────────────┬────────┬───────┐
│Rank │ Paper                            │ Score  │Reason │
├─────┼──────────────────────────────────┼────────┼───────┤
│ 1   │ Makridakis et al. (2022)         │ 0.96   │ Recent│
│     │ "Forecasting with machine..."   │        │ seminal
├─────┼──────────────────────────────────┼────────┼───────┤
│ 2   │ Box & Jenkins (1970)             │ 0.91   │Ancient│
│     │ "Time Series Analysis..."       │        │ gold  
├─────┼──────────────────────────────────┼────────┼───────┤
│ 3   │ Goodfellow et al. (2016)         │ 0.88   │ Deep  │
│     │ "Deep Learning" (foundational)  │        │ learning
├─────┼──────────────────────────────────┼────────┼───────┤
│ 4   │ Taieb et al. (2012)              │ 0.85   │ Vector│
│     │ "A robust and accurate..."      │        │ models
├─────┼──────────────────────────────────┼────────┼───────┤
│ 5   │ Ke et al. (2017)                 │ 0.84   │ GBM   │
│     │ "LightGBM: A fast..."           │        │ intro 
├─────┼──────────────────────────────────┼────────┼───────┤
│ 6-10│ [Other high-impact papers]       │0.78-0.82 │Solid │
└─────┴──────────────────────────────────┴────────┴───────┘

TIER 2: Good Supporting Papers (10 papers)
├─ Relevant methods: 0.65-0.77 (adequate detail)
├─ Adequate citation counts: 30-80 citations
└─ Recent enough: 2018 or later

TIER 3: Weak / Marginal Papers (5 papers)
├─ Off-topic or tangentially relevant: score < 0.50
├─ Rarely cited (< 10 citations): credibility questionable
├─ Old without seminal status: superseded by newer work
├─ Recommendation: CUT these to save space (need 10-15 pages)

Literature Coverage Assessment:
├─ Forecasting methods: 7/10 papers (strong)
├─ Retail/FMCG domain: 5/10 papers (moderate - could add)
├─ Constrained optimization: 3/10 papers (weak - needs reinforcement)
├─ Multi-agent systems: 4/10 papers (moderate)
└─ Overall coverage quality: 68/100 (good, some gaps)

Recommendations:
1. KEEP: All Tier 1 (10 papers)
2. EVALUATE: Tier 2 papers against space budget
3. CUT: All Tier 3 papers
4. ADD: 2-3 papers on constrained optimization
5. Final literature count target: 35-40 papers (current 37 is good)

Quality Score: 7.2/10
├─ Depth: 7/10 (methodology well-covered)
├─ Recency: 7/10 (balanced old & new)
├─ Relevance: 7/10 (some domain gaps)
└─ Coherence: 7/10 (good narrative flow)
```

### Chapter Alignment
**Chapter 2 — Literature Review**
- Paper ranking and selection
- Literature quality assessment
- Coverage evaluation
- Gap identification
- Space optimization (120-page limit)

### Time to Run
⏱️ 6-8 minutes

---

## How to Run All 10 Demos

### Option A: Quick Pass (50 minutes total)
```
Session 1 (10 min):
  - DEMO 1: Exploratory Data Analysis
  - DEMO 6: Seaborn Plots

Session 2 (15 min):
  - DEMO 2: Aeon Forecasting
  - DEMO 3: Scikit-learn Baselines

Session 3 (15 min):
  - DEMO 5: SHAP Explainability
  - DEMO 7: Matplotlib Figures

Session 4 (10 min):
  - DEMO 8: NetworkX Graph
  - DEMO 10: Scholar Evaluation
```

### Option B: Deep Dive (120 minutes total)
Run all 10 demos in sequence, taking detailed notes on outputs.

---

## Next Steps After Demos

1. **Choose primary skills** for your workflow (e.g., `/aeon`, `/matplotlib`)
2. **Create reusable scripts** from demos
3. **Integrate into Ch. 4-8** analysis pipeline
4. **Run quality checks** as you go (don't wait until end)

---

**Status**: All 10 demos ready to execute  
**Expected time**: 5-8 minutes per demo  
**Skills demonstrated**: 8 out of 35 (most critical ones)
