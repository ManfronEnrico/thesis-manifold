---
pid: P0040
created: 2026-08-20 00:00:00
updated: 2026-08-20 00:00:00
---

# P0040 — Progress log

## Session 1 — 2026-08-20 (planning only, no code)

**Trigger.** Brian had a call with Enrico. Priority shifted: Prometheus access
landed and the engine zip was sent (~182 MB compressed, ~500 MB extracted, still
extracting at end of session after one unzip tool errored). Enrico also confirmed
funding for the D/E API spend, ideally spent on Prometheus runs rather than more
GPT runs.

**Decided.**

- Five scenarios, not four. `D_prometheus` plain + `E_prometheus_model` tooled
  (DEC-SCENARIO-SPLIT). Brian's improvement on the single-D proposal; avoids
  confounding engine with tool.
- `{LETTER}_{suffix}` naming confirmed for D and E.
- Engine stays outside the repo, located via `PROMETHEUS_ROOT` in `.env`
  (DEC-PROMETHEUS-VENDORING). IP, not size, is the reason.
- Same data snapshot across all five; prefer local-snapshot mode where supported
  (DEC-PROMETHEUS-DATA).

**Learned.** See findings F1-F8. Most consequential:

- An integration blueprint already exists in `.archive/` but predates engine
  access — a hypothesis to verify, not a spec (F1, F2).
- The warehouse/snapshot leakage worry was overstated: monthly refresh means both
  sources sit at July 2026 right now (F4). Brian's correction.
- The RAM figure is currently fabricated; Prometheus supplies the real numbers
  that make the argument work (F5).

**Corrected myself.** F7 — access does not by itself reconvert SRQ3 from
"assessment" to "integration"; that framing is by design and the change would be a
scope decision.

**Not done / next.** Tasks 1-3 (read-only API and data-access verification) as soon
as extraction finishes. These are free and determine whether D/E is days or weeks.

**Open, needs Brian.**

- Whether pooled-vs-per-brand is a genuine RQ commitment (F8) — decides if the
  ensemble is deferrable.
- Whether to reframe SRQ3 (F7).
- 12 commits remain unpushed; Brian must run `git push` (assistant is
  classifier-blocked).

## Session 2 — 2026-08-20 (engine extracted; tasks 1-3 closed)

**Verified, not assumed.** The archived blueprint's API predictions all held
(F13): `langgraph.json` registry, `ProjectDeps`, `@data_agent.tool`,
`RunContext[CodeExecutorDeps]`, `create_quantitative_research_graph`. The engine is
LangGraph + pydantic_ai and already runs **gpt-5.5** for both main and coder agents
— so D/E will not differ from A-C by base model, a comparability win nobody planned.

**Blockers dissolved rather than resolved.** `PROMETHEUS_TEMPLATE_ID` was never a
secret to obtain from Manifold — `data_agents/sandboxes/templates/prometheus.yaml`
ships the full recipe, and the alias registers per-account (F31, F39). The E2B key
is self-serve; Brian holds his own with $5 loaded. RU warehouse credentials
**verified live** by running `nielsen_connector.test_connection()` — connected and
returned rows from all four views (F35). That is also free evidence the
service-principal flow the engine's token swap depends on works.

**Measured before spending.** One default-sandbox probe (F38): 3.08s per lifecycle,
~$0.0001 per run — E2B is not a budget constraint. More important, the probe found
the base image is bare (`MISSING pyodbc sqlalchemy statsmodels xgboost prophet`),
so the template **is** required: without `statsmodels`/`prophet`, `D_prometheus`
could not fit a real forecasting model and the D->E gap would be inflated in the
thesis's own favour. Cheap-first sequencing caught a self-flattering confound for a
fraction of a cent.

**Corrections I made to my own earlier claims.**

- F33 said no repo warehouse code exists — **wrong**, Brian pointed at
  `02_thesis_data/_00_raw/nielsen/scripts/nielsen_connector.py`. My search excluded
  the path. Recorded as F35.
- F11 blamed CSD-heavy runs on the brand selector — **wrong**, the default is
  already 4/4/4/3 across all categories; the skew came from `--categories CSD`
  during testing. Recorded as F15.
- F16 recommended checking SHAP importance — **it already existed** and Brian was
  right that it belongs to model evaluation. It was 40 days stale because `shap`
  was missing from `requirements.txt` entirely.
- F27 called E2B a hard blocker — **too pessimistic** (F29, then F38).

**Work landed.**

- `srq4_experiment.py`: `--brand-strategy stratified` (F25). Verified all 12 picks
  have zero-free test windows, spanning 237M down to 439 units.
- SHAP regenerated (F23). `promo_intensity` halved to 0.041 — intersection
  **confirmed** safe. Caught that `weighted_distribution`, ranked #2 in the stale
  artifact, no longer exists as a model input.
- `measure_e2b_cost.py` written — the harness could not see E2B spend at all.
- Five shadow scripts in `utility_scripts/scripts/` verified stale and archived
  with a per-file README (F36). `README.md:128` repointed.
- `requirements.txt`: added `shap==0.52.0` (root cause of the stale artifact) and
  `e2b`; consolidated the stale "System A/B" block and flagged the 2.9.1-vs-2.0.0
  pin conflict rather than silently changing it.
- Cross-category checks (F24): no sign inversions, log scale comparable. Nothing
  blocks pooling.

**Open, needs Brian.**

- Task 3b: build the template (command in F39). **Not yet run** — tomorrow.
- Task 4 needs an environment decision (F40): the engine wants python 3.11,
  `e2b_code_interpreter==2.0.0` and `pydantic-ai`; its shipped `.venv` is a broken
  Linux venv. Recommend a separate `uv sync` environment, not installing engine
  pins into the thesis venv.
- SRQ1 pooled-vs-per-category remains an unclosed RQ commitment (F8) — a named gap,
  not an optional extra.
- 12+ commits unpushed; Brian runs `git push`.
