# Session Handover — Manifold AI Thesis (2026-06-30)

> Pick-up document for the next session. Branch: `enrico/local-backup` (never pushed).
> Everything below is committed unless flagged. Backup: "thesis meaningful copy" folder exists.

## 0. TL;DR
The thesis empirical core is largely done and written from real results. SRQ1
(forecasting) + SRQ2 (synthesis) are complete and drafted into Ch4/Ch6/Ch7/Ch8/Ch9/Ch10.
SRQ4 (dedicated model vs code-as-action) now has a **working experiment harness**;
the full run was started then **killed** — needs re-launching. The big new development:
we got the **Prometheus / Graph Engine** code (the real production agentic system =
the SRQ4 baseline) + live Nielsen warehouse credentials (secret pending re-send).

## 1. The thesis in one paragraph
CBS master's on extending a **production agentic decision-support system without
native forecasting** (Manifold's "Prometheus") with **lightweight dedicated
forecasting models**, under compute/deployment constraints. Four Nielsen Danish
beverage categories: CSD, danskvand, energidrikke, RTD.
- **SRQ1** — best lightweight forecasting models (accuracy/efficiency/specialisation).
- **SRQ2** — expose forecasts via a structured tool interface (reliability/uncertainty).
- **SRQ3** — integration readiness (assessment; now possibly active via Graph Engine).
- **SRQ4** — dedicated-model integration **vs a code-as-action LLM** (writes+runs its
  own forecasting code), on correctness/consistency/replicability/cost/latency.

## 2. Data state (IMPORTANT — read before using numbers)
- Market scope = **DVH EXCL. HD** (Danish grocery excl. hard discount). Nielsen's
  default AND Prometheus's production default. This is the Path B fix: the inherited
  pipeline summed across ~28 hierarchical market levels → double-counting (CSD ~168B
  vs the true ~27B units, 6.16x). Always dedup the SCD market dim on `market_id`
  before merging (~7x fan-out otherwise).
- Local snapshot: `data/raw/nielsen_<cat>_clean_*.parquet` (frozen extract). CSD
  facts = **2.5M raw rows** (partial).
- **Brian's update (30/06)**: the warehouse CSD fact VIEW was only ~500K rows (<10%
  of the real ~9M-row CSD dataset, 10GB raw); he is fixing it. totalbeer (~16M rows,
  400 brands) is out of scope. He proposes CSD-only for the agentic PoC. → AGREED
  plan: keep the 4-category forecasting study (SRQ1); scope the agentic/SRQ4 demo to
  CSD; request a fresh full-CSD extract for final CSD numbers.
- NOTE the two data LAYERS that cause confusion: raw warehouse facts = millions of
  rows (SKU×market×period); our feature matrices = brand×month, ~3k rows. Not a
  contradiction.

## 3. Feature matrices (built, committed)
- `thesis/data/_03_engineered_dvhexclhd/<cat>/` — brand×month (CSD 77 brands/3077
  rows, danskvand 24/885, energidrikke 27/1007, RTD 42/1543). Builder:
  `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py`.
- `thesis/data/_04_engineered_bychain/<cat>/` — brand×chain×month (~6x rows, 11
  common retail chains). Builder: `..._bychain.py`.
- Decision (Ch6 §6.5.6): **per-category granularity** — CSD/energidrikke/RTD use
  brand×month, danskvand uses brand×chain; XGBoost throughout.

## 4. SRQ1 — forecasting (DONE)
- Scripts: `scripts/srq1_benchmark.py`, `srq1_benchmark_tuned.py` (Optuna),
  `srq1_figures.py`, `srq1_shap.py`, `srq1_baselines_stat.py` (ARIMA/Prophet),
  `srq1_profiling.py` (RAM/latency), `srq1_calibration.py` (conformal).
- Results in `thesis/data/_05_results_srq1/`.
- **Tuned XGBoost best in every category.** Test WMAPE: CSD 16.5, danskvand 22.0,
  energidrikke 11.4, RTD 31.0. Beats ARIMA in 3/4 (SRQ4-trad). All models ≪8GB RAM.
  Conformal coverage CSD 90→90.5%. SHAP: lag_1 + weighted_distribution dominate.
- Metric note: **mean-MAPE is degenerate** on low-volume series → report WMAPE +
  median MAPE + coverage.

## 5. SRQ2 — synthesis (DONE)
- `scripts/srq2_synthesis.py` (deterministic ensemble/agreement/conformal/confidence,
  `_06_results_srq2/`), `scripts/srq2_agent.py` (Claude synthesis + GPT-4o LLM-as-Judge).
- LLM synthesis beats a rule-based baseline on 4/5 judge dimensions (mean 3.81 vs 3.15).

## 6. SRQ4 — dedicated vs code-as-action (HARNESS BUILT, FULL RUN PENDING)
- **System A (thesis = "Oracle")**: agent calls `forecast_demand` tool →
  `scripts/forecast_service.py` (pre-trained XGBoost; `_07_forecast_service/forecasts.csv`).
  Project skeleton: `thesis/thesis_agents/system_a_oracle/` (persona, tool, config, README).
- **System B (baseline)**: agent writes+runs forecasting code in an E2B sandbox
  (Prometheus-style). Both in `scripts/srq4_experiment.py`.
- Demo (HARBOE/CSD, actual 33.16M): A 26.08M (APE 21.3%, 10s, ~1.7k tok) vs B 34.89M
  (APE 5.2%, 32s, ~8.8k tok). Single point. Finding-in-passing: code-as-action is
  env-fragile (statsmodels absent in E2B by default → now pip-installed in the harness).
- `--full` mode added: 15 brands × 3 repeats × 2 systems → aggregates the 5 SRQ4
  metrics to `_08_results_srq4/{runs.csv,summary.md}`. **Was launched then KILLED —
  re-run it** (`.venv/bin/python scripts/srq4_experiment.py --full --repeats 3`).
  Consider scoping to CSD per Brian.

## 7. Prometheus / Graph Engine (the production baseline)
- Working copy: `graph-engine/` (gitignored — confidential Manifold code). Full read
  in `thesis/data/PROMETHEUS_ARCHITECTURE_REPORT.md`.
- Architecture: LangGraph + PydanticAI, two-agent loop (conversational `data_agent`
  gpt-5.5 → delegates via `invoke_prometheus_coder` → coder runs run_sql/execute_code
  in E2B sandbox, read-only, investigate-and-verify ≤40 turns → Nielsen warehouse).
- It is **descriptive only, no forecasting** = exactly the Main-RQ gap. Its
  `warehouse_guide.md` "5 traps" = our Path B double-count bugs (validation).
- To run System A: drop `system_a_oracle/` into `graph-engine/data_agents/projects/oracle/`,
  add `oracle.py` (mirror `prometheus.py`), register in `langgraph.json`. NOT yet wired/run
  (needs engine venv+deps, E2B template id, possibly Qdrant/Redis).

## 8. Chapters (drafts written from real results; pending human review)
Ch1/2/3 prose draft · Ch4 ~78% (numbers fixed, §4.3.6 EDA) · Ch5 ~55% · Ch6 ~65%
(§6.5 full: ML+baselines+SHAP+SRQ4+RAM+calibration, granularity decision) · Ch7 ~65%
(§7.2.3 synthesis, §7.6.1 judge) · Ch8 ~60% (Levels 1/2/3; human baseline REMOVED
from scope) · Ch9 ~55% (§9.1) · Ch10 ~55% (§10.1). All new prose marked/approved
per Enrico 2026-06-24.

## 9. Credentials / keys (in `.env` files, NOT committed)
- Thesis `.env`: ANTHROPIC_API_KEY ✓, OPENAI_API_KEY ✓, E2B_API_KEY ✓ (added).
- `graph-engine/.env`: RU_SERVER_STRING/DATABASE/CLIENT_ID/TENANT_ID ✓ but
  **RU_CLIENT_SECRET is WRONG** (one-time link consumed; photo/hand transcription
  rejected by Azure AADSTS7000215). **Action: ask Nika to re-send the client secret.**
  client_id + tenant_id confirmed valid by Azure.

## 10. Open items / blockers
- ⛔ RU_CLIENT_SECRET re-send (Nika) → needed to run the real Prometheus baseline.
- 🔄 SRQ4 full experiment: re-launch (was killed).
- 🔄 Fresh full-CSD extract from Brian once the view is fixed (~9M rows).
- 🔮 Wire Oracle into the running Graph Engine (infra: venv/deps/E2B template).
- 🔮 Human review/finalisation of Ch4–Ch10 drafts.
- ➖ Prometheus live-data access otherwise NOT needed for the local build.

## 11. Living reports
- `thesis/data/EXECUTION_PROGRESS.md` — status board + chapter %s + experiments ledger.
- `thesis/data/FINAL_EXECUTION_REPORT.md` — zero-context run summary.
- `thesis/data/PROMETHEUS_ARCHITECTURE_REPORT.md` — engine deep-dive.
- Project journal (memory): decisions/pivots/milestones.

## 12. Git
~28 commits this arc on `enrico/local-backup` (d15a1a7 … c622196). Not pushed.
`graph-engine/` gitignored. `.env` never committed.

## 13. Suggested next steps (ranked)
1. Re-launch the SRQ4 full experiment (optionally CSD-only) → the 5-metric table = the SRQ4 answer.
2. Reply to Brian: CSD-only for the agentic PoC; keep 4-cat SRQ1; request fresh full-CSD extract.
3. Get the RU secret from Nika → run the real Prometheus as System B (production validation).
4. Wire Oracle into the engine; run System A there.
5. Human pass on the chapter drafts.
