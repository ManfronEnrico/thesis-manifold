# System A — "Oracle" (thesis forecasting agent)

The thesis artefact: a sibling of Prometheus that **delegates forecasting to a
dedicated model** instead of writing forecasting code at runtime (the SRQ4
contrast). Same Graph Engine, one extra tool.

## Files
- `forecast_demand_tool.py` — the novel tool; wraps `scripts/forecast_service.py`
  (pre-trained tuned XGBoost + conformal interval + confidence tier).
- `docs/persona.md` — forecast-aware analyst; routes predictive→tool,
  descriptive→normal analysis. Default market DVH EXCL. HD.
- `data/data_credentials.json` — `type: file`, local Nielsen snapshot (no live DB).

## To run inside the Graph Engine
1. Copy this folder to `graph-engine/data_agents/projects/oracle/`.
2. Add an `oracle.py` mirroring `prometheus.py`:
   - `ProjectDeps(agent_name="Oracle", company_name="Royal Unibrew", data=…,
     tool_names=[…, "forecast_demand"], conversational_guardrails=persona, …)`
   - import `forecast_demand_tool` (triggers tool registration).
   - `oracle_graph = create_quantitative_research_graph(deps).compile()`.
3. Register `"oracle": "./data_agents/projects/oracle/oracle.py:oracle_graph"` in
   `langgraph.json`.
4. Engine `.env` needs `OPENAI_API_KEY` + `E2B_API_KEY` (both available); no RU
   warehouse credentials required for System A.

## SRQ4 experiment
Run the same ~50 prompts through Oracle (dedicated tool) and Prometheus
(code-as-action) → score correctness, consistency, replicability, cost, latency.
System A runs on local data now; the live warehouse is needed only to run the real
Prometheus baseline.

## Status
Skeleton + working `forecast_service`. Not yet wired into a running engine
(needs `oracle.py` + a local engine run; E2B template id to confirm).
