# Comments -- Rationale for model selection

> Objections on **Model Benchmark & Selection > Rationale for model selection**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/01-rationale-for-model-selection.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [235](#c235) | Rationale for model selection | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |

---

<a id="c235"></a>

## [235] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Rationale for model selection
- **Date:** 2026-09-05T15:22:00
- **On:** “Rationale for model selectionFive model families span the inductive-bias spectrum: classical statistical (ARIMA, Prophet), gradient boosting (LightGBM, XGBoost), regularised linear (Ridge), plus four parameter-free benchmarks (mean, naive, seasonal-naive, drift)Selection criteria: (a) established empirical performance on retail/FMCG panels; fit within the ≤8 GB sequential RAM budget; (c) interpretability sufficient for the SRQ4 scenario comparison; (d) diversity of inductive biasThe benchmark rung is required, not decorative. Hyndman & Athanasopoulos (2021, §5.2) define the four simple methods as benchmarks against which “any forecasting methods we develop will be compared … to ensure that the new method is better than these simple alternatives”. A forecasting result reported without them is unbenchmarkedEmpirical weight for that requirement comes from M4: of six pure machine-learning entries, none beat the statistical combination benchmark and only one beat Naïve2 (Makridakis et al., 2018, p. 803)NOT included, and why: deep sequence models (LSTM/N-BEATS) - RAM footprint incompatible with the ≤8 GB constraint, and infeasible under the HPO time budget on ~30 monthly observations per series”

VERIFY, SOURCES, PROSE
