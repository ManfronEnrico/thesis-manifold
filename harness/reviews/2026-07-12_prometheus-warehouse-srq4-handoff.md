# Handoff brief — Prometheus, the Nielsen warehouse, and the SRQ4 comparison
> Written 2026-07-12 for a fresh Claude Code session. Read this first, then
> `harness/thesis_tasks.json` (single source of truth). This session did NO figure/code
> changes worth keeping beyond harness updates — it was a discovery + decisions session.

## TL;DR
The SRQ4 comparison was conceptually muddled (wrong "System A/System B" labels, a fake E2B
proxy in the experiment code, and a false belief that we can't run Prometheus). This session
cleared that up: **we CAN reach the real Nielsen warehouse ourselves**, and the comparison is
**one system (Prometheus) with vs without a dedicated forecasting tool** — not two separate systems.

## What Prometheus actually is (verified from code)
- A **read-only conversational data analyst** for Royal Unibrew's Nielsen data. Code lives in
  `graph-engine/data_agents/projects/prometheus/` (agent `prometheus.py`, coder `prometheus_coder.py`).
- Framework: **PydanticAI agents on a LangGraph graph**. Model: **gpt-5.5 (OpenAI)**, NOT Claude.
- Sandbox: **E2B** (`graph-engine/data_agents/tools/code_executor.py`; template
  `graph-engine/data_agents/sandboxes/templates/prometheus.yaml` — installs statsmodels/prophet/
  lightgbm/xgboost/optuna/shap + ODBC).
- **It has NO forecasting ability today.** grep `forecast|predict|fit` over the prometheus tree = 0.
  It only does descriptive Nielsen measures (value/volume/share/price/distribution/promo) and
  declines out-of-scope asks (`docs/persona.md`). The ML libs are installed in its sandbox but
  nothing directs it to model.
- Its coder writes **T-SQL against the live warehouse** and runs it in E2B (`prometheus_coder.py:107-136`).

## The Nielsen warehouse = our data source (BIG finding)
- The warehouse `Nielsen_clean` (Azure SQL / Microsoft Fabric, T-SQL read-only) is the **live source**
  of the Nielsen data. Our local `data/raw/nielsen_<cat>_clean_*.parquet` are a **frozen April download**
  of the same `{cat}_clean_facts_v` / `_dim_*_v` views.
- **We can connect to it ourselves.** The `.env` has the RU Azure **service principal**
  (`RU_CLIENT_ID/SECRET/TENANT`) + `RU_SERVER_STRING` + `RU_DATABASE=Nielsen_clean`.
  `graph-engine/security/token_swap.py:125-153` mints an `AZURE_SQL_ACCESS_TOKEN` from those via
  OAuth2 client-credentials; then connect exactly as `prometheus_coder.py:107-129` (ODBC Driver 18 —
  installed; `.venv` has pyodbc 5.3.0; pass the token via `attrs_before={1256: token_struct}`).
- **VERIFIED read-only this session:** connection OK; `SELECT COUNT(*) FROM dbo.csd_clean_facts_v`
  → **9,824,601 rows**. (Earlier "we can't run it / need Nika" was from the April planning docs and
  was WRONG for the current repo.)
- ⚠️ Our local CSD snapshot = **2,535,464 rows = only 25.8%** of the warehouse (≈74% missing).
  This is the "partial CSD" behind B01. Other categories may be more complete (unverified).

## The SRQ4 comparison — correct framing
Drop the labels "System A / System B" (overloaded: `ai-declaration.md` uses "System B" for the
thesis-production tooling). Use descriptive names. The comparison is the **same Prometheus, two modes**:
1. **Dedicated-model agent** (the artefact / thesis contribution): Prometheus **delegates** to our
   pre-trained forecasting model exposed as a **callable tool** (Nika's integration plan:
   `00_thesis_context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md`).
2. **Code-as-action baseline**: Prometheus (as-is) **writes & runs its own forecasting code** on the
   warehouse in E2B — no pre-built model. Ch5 §5.7 / Ch8 §8.3.3 define this as the SRQ4 baseline.

Note: Nika's docs actually frame a "50/50/50" (Prometheus alone / + untuned tool / + tuned tool), and
"Prometheus alone" is undefined because it can't forecast. Whether the baseline = "writes own code"
is the **thesis's** construct, not explicitly Nika's — a real open question (can't reach Nika now).

## Decisions made this session (in harness)
- **DEC-DATA**: use the **frozen April snapshots** for the reproducible comparison (reproducibility +
  independence from RU creds/uptime), NOT the live warehouse for results.
- **B01 unblocked**: refetch-via-RU-secret is proven; no longer needs Brian.
- Consequence recorded: for a fair same-data comparison the code-as-action arm must read the snapshot,
  not live SQL → feeds OPEN-BASELINE.

## Open decisions (do NOT decide for Enrico — these are his)
- **OPEN-CSD**: keep the 26% partial CSD snapshot, or one-time full fetch (9.8M) + freeze. STEP 1 first:
  understand *what* the partial slice excludes (periods? markets? products?). Enrico has NOT decided.
- **OPEN-BASELINE**: real Prometheus (needs E2B template + gpt-5.5 + graph-engine runnable) vs a faithful
  code-as-action agent we build; how it reads the snapshot; which base LLM (same for both arms, Ch5).
- Then: sandbox, comparative tools (tuned-only vs the 50/50/50 tiers), metrics/scope.

## Known-broken things to fix once the above is decided
- `03_thesis_modelling/model_training/srq4_experiment.py` is a **stand-in, not real Prometheus**: it uses
  a bespoke E2B agent, hands the LLM a pre-made `df` (not warehouse/snapshot access), and uses Claude
  (not gpt-5.5). Rework after OPEN-BASELINE.
- The two figures `05_thesis_writing/figures/fig_system{A,B}_thesis_v2.svg` were drawn on the wrong
  "System A/B" framing — **redo** as "Prometheus + dedicated tool" vs "Prometheus code-as-action" once
  the baseline is defined. (Visual language + swimlane style are fine to reuse.)
- Harness task file paths (R1–R6 etc.) still point at pre-restructure `scripts/`, `thesis/` — stale after
  Brian's P0028 flatten; remap to the numbered tiers when convenient.

## Reconnect recipe (for a fresh session)
`.venv/bin/python`, `requests` for the token (certifi), then pyodbc:
1. POST `https://login.microsoftonline.com/{RU_TENANT_ID}/oauth2/v2.0/token` with
   grant_type=client_credentials, client_id=RU_CLIENT_ID, client_secret=RU_CLIENT_SECRET,
   scope=`https://database.windows.net/.default` → `access_token`.
2. `conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=<RU_SERVER_STRING>;DATABASE=Nielsen_clean;Encrypt=yes;TrustServerCertificate=yes;"`
3. `token_struct = struct.pack("<I"+str(len(raw))+"s", len(raw), raw)` where `raw = token.encode("UTF-16-LE")`;
   `pyodbc.connect(conn_str, attrs_before={1256: token_struct})`. Read-only only.
Run outside the Bash sandbox (needs network). `.venv` Python is 3.13 and lacks system CA certs — use
`requests` (certifi) for the token, not stdlib urllib.
