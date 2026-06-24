# EXECUTION PROGRESS — Autonomous Thesis Run

> Living report. Updated every loop iteration. Branch: `enrico/local-backup`.
> External blockers: **PROMETHEUS** = live Nielsen data platform · **NIKA** = access/credentials gatekeeper.

## TL;DR (latest)
Autonomous loop started 2026-06-23. Phase: SRQ1 forecasting benchmark on the
corrected brand×chain matrices (`_04`). Everything here runs on the LOCAL Nielsen
snapshot — no Prometheus/Nika needed.

---

## STATUS BOARD

| Item | Status | Notes |
|------|--------|-------|
| DVH EXCL. HD market-scope fix (Path B) | ✅ COMPLETED | committed a9de949…b57b503 |
| brand×month matrices `_03` | ✅ COMPLETED | 77/24/27/42 brands |
| brand×chain matrices `_04` | ✅ COMPLETED | 15606/4570/6006/7684 rows, d15a1a7 |
| SRQ1 benchmark (baselines+LGB+XGB, WMAPE) | ✅ COMPLETED | untuned 1st pass, both datasets (E1/E2) |
| SRQ1 Optuna tuning (LGB+XGB, 30 trials) | ✅ COMPLETED | 59f331c; XGB best 8/8; tuned WMAPE in _05 |
| Ch4 §4.3.6 per-category EDA | ✅ COMPLETED | a928525, [PENDING APPROVAL] prose |
| Publication figures (ladder/granularity/overlay) | ✅ COMPLETED | 4c7a98b, _05/figures/ |
| Ch6 §6.5 results drafted | ✅ COMPLETED | 665210a, [PENDING APPROVAL] |
| SHAP feature importance | ✅ COMPLETED | ffa1836; lag_1 + weighted_distribution top |
| ARIMA/Prophet baselines (SRQ4) | ✅ COMPLETED | 907b135; ARIMA stable, Prophet unstable 2/4 |
| Ch6 §6.5.3 SRQ4 comparison | ✅ COMPLETED | ML beats ARIMA 3/4 categories |
| RAM/latency profiling | ✅ COMPLETED | 2cfcc38; all models ≪8GB |
| Calibration / prediction intervals (SRQ2) | ✅ COMPLETED | 07803f4; CSD 90→90.5% coverage |
| Ch4 §4.3.6 + Ch6 §6.5 prose | ✅ APPROVED | Enrico 2026-06-24; markers removed |
| Per-category granularity decision | ✅ DECIDED | Ch6 §6.5.6: CSD/energi/RTD brand×month, danskvand brand×chain |
| Prometheus access | ➖ OUT OF SCOPE | not needed (local snapshot canonical); not available |
| SRQ2 synthesis engine (deterministic) | ✅ COMPLETED | scripts/srq2_synthesis.py → _06_results_srq2; coverage 80-98% |
| Ch7 §7.2.3 synthesis results | ✅ WRITTEN | 886559e; from real outputs |
| Ch8 §8.2.5 (Level 1) + §8.4.4 (Level 3) | ✅ WRITTEN | 886559e; from real runs |
| LLM rec-text / LLM-as-Judge / SRQ4 code-as-action | ⛔ BLOCKED | needs LLM API (NOT Prometheus) — the real remaining blocker |
| Agentic harness (System A/B) | 🔮 FUTURE | local + LLM API; consumes _05/_06 outputs |
| Ch4 absolute-volume number fix (27.4B etc.) | ✅ COMPLETED | cb2e718, docx regenerated |
| Ch4 §4.3 EDA for danskvand/energi/RTD | 🔄 IN PROGRESS | numbers ready in eda_findings |
| Ch6/Ch7/Ch8 from regenerated results | 🔮 FUTURE | after benchmark |
| Agentic System A/B code (local-runnable) | 🔮 FUTURE | stub Prometheus data layer |
| `_03` vs `_04` canonical reconciliation | 🧯 TECH DEBT | `_04` is primary |
| Modular `_02` files runnable | 🧯 TECH DEBT | reference-only for now |
| Fresh/expanded Nielsen pulls (weekly, more cats) | ⛔ BLOCKED | PROMETHEUS (creds via NIKA) |

## CHAPTER COMPLETION %
(basis: skeleton 10 / bullets 30 / drafted 60 / numbers-verified 80 / approved 100)

| Ch | % | Basis |
|----|---|-------|
| 1 Introduction | 60 | prose draft, RQs v3/v4 realigned |
| 2 Literature | 60 | prose draft |
| 3 Methodology | 60 | prose draft, RQs v4 |
| 4 Data assessment | 78 | abs-numbers fixed; 3-cat §4.3 EDA prose pending |
| 5 Framework design | 55 | prose draft, prototype rebuilding |
| 6 Model benchmark | 65 | §6.5 fully drafted [PENDING APPROVAL]: ML+baselines+SHAP+SRQ4+RAM+calibration. §6.6/6.7 interpretive prose pending approval |
| 7 Synthesis | 45 | §7.2.3 deterministic synthesis results written; LLM parts need API |
| 8 Evaluation | 45 | Level 1 + Level 3 written from real runs; Level 2 needs API |
| 9 Discussion | 10 | skeleton |
| 10 Conclusion | 10 | skeleton |

## EXPERIMENTS LEDGER
| # | Dataset | Models | Headline (best WMAPE, test) | Script | Output |
|---|---------|--------|-----------------------------|--------|--------|
| E1 | _04 bychain | Naive/Ridge/LGB/XGB (untuned, seed42) | CSD 23.3 / dansk 22.9 / energi 16.0 / RTD 41.2 (XGB) | scripts/srq1_benchmark.py | _05_results_srq1/ |
| E2 | _03 brand | same | CSD 19.0 / dansk 31.8 / energi 15.6 / RTD 36.4 | same | same |

| E3 | _04 + _03 | Optuna-tuned LGB+XGB (30 trials, seed42) | tuned XGB WMAPE: CSD 16.5(brand)/20.8(chain), dansk 22.0(chain), energi 11.4(brand), RTD 31.0(brand) | scripts/srq1_benchmark_tuned.py | _05/tuned_*, tuned_params.json |
| E4 | corrected results | 3 publication figures | model-ladder / granularity / forecast-overlay | scripts/srq1_figures.py | _05/figures/*.png |

**Key finding:** "more rows = better" is NOT confirmed — granularity gain is
category-dependent (brand×month wins CSD/energi/RTD, chain wins danskvand). XGBoost
best in all 8; every model beats SeasonalNaive; tuning gained ~2–4 pp WMAPE.
energidrikke 11.4% WMAPE ≈ the ≤15% industry target. METRIC NOTE: mean-MAPE is
degenerate on low-volume series (tiny denominator → billions %); WMAPE + median
MAPE are the reported robust metrics.

## ASSUMPTIONS LOG
- A1: WMAPE (volume-weighted) is the primary business metric; plain mean-MAPE
  reported alongside for comparability with the old pipeline / literature target.
- A2: `_04` brand×chain is the canonical dataset; `_03` brand×month kept as
  robustness comparison.

## BLOCKERS LEDGER
- B1 ⛔ PROMETHEUS: any new Nielsen pull (weekly granularity, extra categories,
  fields absent from `data/raw`). Unblock = Prometheus access. Gated by NIKA (Azure
  client secret regeneration). Work routed around via the local snapshot + stubs.

## FILES TOUCHED (this run)
- + `thesis/data/EXECUTION_PROGRESS.md` (this report)
