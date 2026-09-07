# `ch5_architecture_v1` — superseded 2026-09-06 by `ch5_layered_architecture_v2`

Hand-drawn SVG with no producer. Its layered framing (substrate → tool interface
→ agentic layer) was sound and is preserved in the replacement; several specific
claims were not.

| Claimed | Verified |
|---|---|
| 5-model substrate: ARIMA, Prophet, LightGBM, XGBoost, Ridge | ARIMA and Prophet are statistical **baselines** (`srq1_baselines_stat.py`). The benchmarked ladder is SeasonalNaive, Ridge, LightGBM, XGBoost |
| "human-in-the-loop checkpoints" | no approval mechanism in any live module |
| "Prometheus Graph Engine · LangGraph deployment" | neither is a dependency; imported nowhere |
| "sandbox (e.g. E2B)" | Scenario B uses Anthropic's **hosted Code Interpreter** container. E2B appears only in `measure_e2b_cost.py`, a separate cost estimate |
| "≤ 8 GB RAM" | measured envelope is 4096 MB |
| "Lightweight Python coordinator" | no coordinator object exists; the stages are separate scripts run in sequence |

Replaced by `ch5_layered_architecture_v2`, which keeps the three-layer story and
reads the ladder, the served model per category, the measured RAM and the
scenario set from artefacts at render time.
