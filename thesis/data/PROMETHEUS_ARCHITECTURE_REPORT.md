# Prometheus / Graph Engine — Specific Architecture Report

_Read of the real code at `graph-engine/` (working copy, secrets excluded), 2026-06-25.
For: deciding what System A (the thesis artefact) must reuse, change, and implement._

## 1. What Prometheus actually is
A **descriptive data analyst agent for Royal Unibrew**, built on the shared
"Graph Engine" framework (LangGraph + PydanticAI). It turns the Nielsen retail
warehouse into plain-language commercial insight. Scope is deliberately narrow
(`persona.md`): Royal Unibrew's Nielsen categories, brands, markets, measures, and
**how they move over time** — i.e. *what happened*. It explicitly declines coding,
general knowledge, other datasets. **It has no forecasting capability.**

The framework is multi-tenant: `langgraph.json` registers ~20 sibling agents
(prometheus, zenda, hamilton, aiana, dario, …). Each is the same engine + a project
folder. So building "System A" = adding one more project folder.

## 2. The architecture (two brains in a loop)
LangGraph state machine (`quantitative_research_graph.py`), one cycle per turn:
```
dependency_injection → data_agent → image_inserter → human → (loop)
```
- **dependency_injection** loads `ProjectDeps` (agent_name, company, data sources,
  tool_names, guardrails, models).
- **data_agent** — the conversational brain. PydanticAI `Agent`, model
  `OpenAIModels().standard.balanced` (project sets `main_agent_model="gpt-5.5"`).
  System prompt = `quantitative_research_prompt` + persona + memory + proactive.
  It NEVER queries data itself; it picks a tool.
- **image_inserter / human** format charts and wait for the next message.

**Two-agent delegation (the key pattern):**
- Main agent's tools: `invoke_prometheus_coder`, knowledge base (Qdrant), memory,
  proactive.
- `invoke_prometheus_coder` (`prometheus_coder.py`) hands a **structured brief**
  (objective, dataset, market, period, comparison, rows_and_metrics, notes) to the
  **coder agent** (model `.powerful`), which runs an investigate-and-verify loop
  (request_limit=40).

## 3. The code-as-action engine (this is the SRQ4 baseline)
The coder's tools, all sandbox-backed:
- `run_sql` (one read-only SELECT/WITH), `inspect_schema`, `distinct_values`,
  `sample_rows`, `execute_code` (pandas/matplotlib).
- A **read-only guard** (`assert_read_only`) rejects anything but SELECT/WITH, in
  Python AND re-enforced inside the sandbox kernel bootstrap.
- Execution happens in an **E2B sandbox** (`code_executor.py` → `e2b_code_interpreter`).
- **Token swap** (`security/token_swap.py`): permanent RU client secret →
  short-lived (1h) Azure AD token (`https://database.windows.net/.default`), so the
  sandbox never holds the real secret.
- Output is scanned (`security/output_gate.py`); charts uploaded → image URLs.

For a forecasting question Prometheus has no model — its coder would **write
forecasting code on the fly** in the sandbox. That is exactly the v4 SRQ4
"code-as-action LLM baseline".

## 4. The data layer
- Source: `Nielsen_clean` database, schema `dbo`, on **Microsoft Fabric SQL**
  (read-only). Star schema per category: `<p>_clean_facts_v` + `_dim_market_v` /
  `_dim_period_v` / `_dim_product_v`, plus RAW tables (no `_v`) with the hierarchy +
  SCD2 versioning. Prefixes: `csd, danskvand, energidrikke, rtd, totalbeer` (5 —
  Prometheus keeps totalbeer; our local snapshot has 4, totalbeer facts absent).
- Config: `data/data_credentials.json` (`type: database`, maps RU_* + E2B +
  TEMPLATE_ID env vars), described to the coder via `data_model.md`,
  `warehouse_guide.md`, `business_reference.md`.

## 5. ⭐ Direct validations for the thesis (found in the code)
1. **DVH EXCL. HD is Prometheus's production default market** (`data_summary.md`:
   "Default market when the user doesn't specify: DVH EXCL. HD"). Our Path B market
   choice matches the production system exactly — strong external validation.
2. **The "five traps" in `warehouse_guide.md` are our Path B bugs**, encoded as
   prompt warnings the LLM must remember at runtime:
   - Trap 1/2: fact view holds pre-aggregated grains; the raw product hierarchy is
     multi-level/multi-dimensional — "NEVER SUM ACROSS LEVELS"; magnitude sanity:
     "billions/trillions for a single month → you are multi-counting grains — stop
     and fix." This is precisely the 168B→27B double-count we fixed.
   - `weighted_distribution` is NON-ADDITIVE ("never sum or average") — matches our
     mean-not-sum handling.
   - No YTD/quarter rows (months only); YoY, share, growth, price/L all derived by
     hand.
   → **Thesis argument**: a dedicated model bakes the correct scope/aggregation in
   *by construction*; the code-as-action agent must re-derive it correctly every
   run from prompt "tribal knowledge" — a replicability/consistency gap to measure.
3. **Descriptive-only** = the precise gap in the Main RQ ("agentic systems without
   native predictive capabilities").

## 6. What System A needs (reuse / change / implement)
**Reuse unchanged:** the whole engine — graph, two-agent loop, E2B sandbox, token
swap, security gates, image handling.

**Change (a new project folder, sibling of prometheus):**
- `data/data_credentials.json` — point at our data (either the same warehouse, or
  `type: file` over the local parquet snapshot to run without the live DB).
- `persona.md` / `operating_rules.md` — a forecasting-aware analyst that knows
  *when to delegate to the dedicated model* vs descriptive query.
- `<project>.py` — wire `create_quantitative_research_graph` with our `ProjectDeps`.

**Implement (the novel bit):**
- A custom tool `forecast_demand(category, brand[, chain], horizon)` that returns
  our pre-trained XGBoost forecast + conformal interval + confidence tier (from
  `_05_results_srq1` / `_06_results_srq2`), instead of letting the LLM write
  forecasting code.

**SRQ4 experiment:** same prompt set through System A (dedicated tool) vs System B
(Prometheus code-as-action) → correctness, consistency, replicability, cost, latency.
Runnable on local data with OPENAI + E2B keys; the live warehouse (RU creds) is
needed only to run the *real* production Prometheus as final validation.

## 7. Open dependencies
- RU warehouse client secret: re-send needed (one-time link consumed; hand-typed
  copy rejected by Azure). NOT blocking the local build.
- `PROMETHEUS_TEMPLATE_ID` / a custom E2B template may be required for the exact
  sandbox image; verify when wiring.
