# Source-Level Verification Report
## Section D: Benchmark Forecasting Methods

This report presents a source-level verification of claims related to **Benchmark Forecasting Methods (BM-01 through BM-05)**, grounded strictly in the provided academic literature: **Hyndman & Athanasopoulos (2021) (*Forecasting: Principles and Practice*, 3rd edition)** and **Makridakis et al. (2018) (*The M4 Competition: Results, findings, conclusion and way forward*)**.

---

### **Claim-by-Claim Verification Register**

| Claim ID | Proposed Thesis Claim | Verdict | Source and Page | Exact Supporting Passage | Safest Thesis-Ready Wording |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BM-01** | Mean, naïve, seasonal-naïve, and drift forecasts are standard simple benchmark methods. | **Supported** | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice* (3rd ed.), Section 5.2 | "Some forecasting methods are extremely simple and surprisingly effective. We will use four simple forecasting methods as benchmarks throughout this book." (Section 5.2) | "Standard baseline forecasting models include the mean method, naïve (random walk) method, seasonal naïve method, and drift method, as formalised by Hyndman and Athanasopoulos (2021). The mean method defines all future forecasts as the historical average: $\hat{y}_{T+h\|T} = \bar{y}$. The naïve method sets all forecasts to the last observed value: $\hat{y}_{T+h\|T} = y_T$. For seasonal naïve forecasts, each prediction equals the last observed value from the corresponding season: $\hat{y}_{T+h\|T} = y_{T+h-m(k+1)}$, where $m$ represents the seasonal period and $k$ is the integer part of $(h-1)/m$. Finally, the drift method extrapolates a linear trend between the first and last observations: $\hat{y}_{T+h\|T} = y_T + h(\frac{y_T - y_1}{T-1})$." |
| **BM-02** | A new forecasting model should be compared with simple benchmarks because simple methods can be surprisingly effective. | **Supported** | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice* (3rd ed.), Section 5.2 | "Sometimes one of these simple methods will be the best forecasting method available; but in many cases, these methods will serve as benchmarks rather than the method of choice. That is, any forecasting methods we develop will be compared to these simple methods to ensure that the new method is better than these simple alternatives." (Section 5.2) | "It is a standard methodological requirement in time-series forecasting to evaluate any newly developed model against simple statistical baselines, such as naïve or seasonal naïve models, to verify that the proposed method delivers a genuine predictive improvement over these simple but often highly effective benchmarks (Hyndman & Athanasopoulos, 2021)." |
| **BM-03** | In the M4 competition, submitted pure machine-learning methods generally failed to outperform established statistical combinations. | **Supported** | Makridakis et al. (2018), J. of Forecasting, 34(4), p. 803 (Abstract & Section 2) | "The six pure ML methods performed poorly, with none of them being more accurate than the combination benchmark and only one being more accurate than Naïve2." (p. 803, Abstract; repeated on p. 804, Section 2) | "In the M4 forecasting competition, pure machine-learning methods performed poorly in point forecasting, with none of the six submitted pure ML methods outperforming the simple statistical combination benchmark (Comb) and only one beating the Naïve2 baseline (Makridakis et al., 2018)." |
| **BM-04** | The strongest M4 results should not be summarized simply as “machine learning failed,” because the winning or leading methods included combinations or hybrids of statistical forecasting and machine learning. | **Supported** | Makridakis et al. (2018), J. of Forecasting, 34(4), p. 803 (Section 2) | "The biggest surprise was a 'hybrid' approach that utilized both statistical and ML features. This method produced both the most accurate forecasts and the most precise PIs, and was submitted by Slawek Smyl, a Data Scientist at Uber Technologies." (p. 803, Section 2) | "Although pure machine-learning models struggled in the M4 competition, the overall winning methods were hybrid or combination frameworks. Specifically, the top-performing method (Smyl, 2020) was a hybrid approach combining exponential smoothing equations with a recurrent neural network (RNN), which achieved a 9.4% improvement over the standard Comb benchmark, while the second-best method combined seven statistical methods with neural network-derived weights (Makridakis et al., 2018)." |
| **BM-05** | M4 proves that seasonal-naïve models generally outperform tuned machine-learning models for retail beverage demand. | **Contradicted** (as a universal claim); **Supported with Qualification** (as a contextual precedent) | Makridakis et al. (2018), J. of Forecasting, 34(4) | *N/A* (The M4 competition consists of 100,000 general time series and does not contain a specific retail beverage demand category where seasonal-naïve is proven to beat ML models universally.) | "While the M4 competition does not specifically evaluate retail beverage demand, its broad empirical finding that pure machine-learning methods often struggle to outperform simple statistical baselines provides strong academic precedent for the empirical results in this thesis, where the simple seasonal naïve baseline outperformed tuned machine-learning models on the highly seasonal Ready-to-Drink (RTD) category (cf. Makridakis et al., 2018)." |

---

### **Detailed Verification Analysis & Mathematical Definitions**

#### **1. Procedural Definitions of simple benchmarks (BM-01)**
Section 5.2 of Hyndman & Athanasopoulos (2021) defines the four benchmark methods as follows:

*   **Mean Method:** The forecast of all future values is equal to the sample mean of the historical data ($y_1, \dots, y_T$):
    $$\hat{y}_{T+h\|T} = \bar{y} = \frac{1}{T}\sum_{t=1}^T y_t$$
*   **Naïve Method:** The forecast is simply set to the last observed value:
    $$\hat{y}_{T+h\|T} = y_T$$
    This is also referred to as a **random walk forecast** and is modeled using the `RW()` function in R.
*   **Seasonal Naïve Method:** For highly seasonal data, the forecast is set to the last observed value from the same season of the previous year (or cycle):
    $$\hat{y}_{T+h\|T} = y_{T+h-m(k+1)}$$
    where $m$ is the seasonal period, and $k$ is the integer part of $(h-1)/m$ (the number of complete seasonal cycles in the forecast period prior to time $T+h$).
*   **Drift Method:** A variation on the naïve method that allows forecasts to increase or decrease over time according to the average historical change (the "drift"):
    $$\hat{y}_{T+h\|T} = y_T + \frac{h}{T-1}\sum_{t=2}^T (y_t - y_{t-1}) = y_T + h\left(\frac{y_T - y_1}{T-1}\right)$$
    This is geometrically equivalent to drawing a straight line between the first ($y_1$) and last ($y_T$) historical observations and extrapolating it.

#### **2. Methodological Precedent of simple benchmarks (BM-02)**
Hyndman and Athanasopoulos (2021) outline that automatic forecasting models must always be evaluated against these simple benchmarks. The underlying rationale is that simple benchmarks are surprisingly robust and effective; if a sophisticated machine learning or statistical model cannot beat a simple benchmark, it should not be utilized.

#### **3. Performance of Pure Machine Learning in the M4 (BM-03 & BM-04)**
The M4 competition (Makridakis et al., 2018) evaluated 61 forecasting methods across 100,000 time series. A core finding was the distinct performance gap between **pure machine learning (ML)** methods and **hybrid/combination** approaches:
*   **Poor Pure ML Performance:** The six submitted pure ML methods performed poorly. None of them outperformed the simple statistical combination benchmark (**Comb**, which is the simple average of Single, Holt, and Damped exponential smoothing models), and only one managed to beat the simple **Naïve2** baseline (which is a naïve model adjusted for seasonality).
*   **The Power of Hybrids and Combinations:** The winning method, submitted by Slawek Smyl, was a **hybrid** approach combining exponential smoothing formulas with a recurrent neural network (RNN) engine. It outperformed the Comb benchmark by 9.4% in sMAPE and achieved highly accurate 95% prediction intervals (actual coverage of 94.8% vs. 95% target). The second-best method (Montero-Manso, Talagala, Hyndman & Athanasopoulos) was a combination of seven statistical methods, where the averaging weights were dynamically calculated by a meta-learning neural network trained to minimize forecasting error.

#### **4. Thesis Contextual Adaptation (BM-05)**
A critical distinction must be maintained between **the general conclusions of the M4** and the **specific empirical findings of your thesis**:
*   The M4 did *not* prove that seasonal naïve models outperform machine learning models *specifically for retail beverage demand*. The M4 dataset is a massive, heterogeneous database of 100,000 series across micro, macro, finance, industry, and demographic domains.
*   However, your finding that seasonal naïve (SNAIVE) outperformed tuned machine learning models on the Ready-to-Drink (RTD) category is heavily supported by the *spirit* of the M4's findings. Highly seasonal categories with relatively short histories (like RTD) are notoriously difficult for complex ML models to learn without overfitting. In such regimes, the simple seasonal naïve baseline (27.3% WMAPE) serves as an exceptionally tough benchmark, echoing the M4's core lesson that complex models are not universally superior.

---

### **Thesis Correction Register**

#### **A. Overstatements and Misattributions requiring correction**
1.  **Do not write:** *"The M4 competition proved that seasonal-naïve models generally outperform tuned machine-learning models for retail beverage demand."*
    *   **Correction:** Rephrase to emphasize that the M4 competition established a general precedent regarding the difficulty pure ML models face when competing with simple statistical baselines, which contextualizes and supports your specific empirical finding in the RTD category.

#### **B. Missing citations or parameters**
1.  When defining simple benchmarks, ensure that the formal mathematical equations are explicitly written (as detailed in the section above) and refer directly to **Section 5.2 of Hyndman & Athanasopoulos (2021)**.
2.  When citing the performance of pure ML models in M4, cite the exact statistics: *"none of the six pure ML models outperformed the Comb benchmark, and only one outperformed the Naïve2 baseline (Makridakis et al., 2018)."*
