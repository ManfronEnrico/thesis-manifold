---
name: 2026-08-20-prometheus-integration-handover-enrico
description: HANDOVER - Prometheus Graph Engine integration; the SRQ4 ladder extends from three scenarios to five, plus SRQ1 findings from the same session.
category: reference
applies-to: [srq4, srq1, prometheus, scenario-design]
triggers: [picking up the Prometheus integration, reviewing the five-scenario design]
created: 2026_08_20-18_00
updated: 2026_08_21-15_00
---

# Handover — Prometheus integration and the five-scenario ladder

**From:** Brian · **To:** Enrico · **Date:** 2026-08-20
**Plan:** `plans/P0040_2026-08-20_prometheus-scenarios-d-e/`

Thanks for sending the engine. It arrived, it is fully inspected, and the picture
is better than expected: **nothing external is blocking us.** Details below,
including the two credentials I asked you about — it turns out we never needed
them from you.

---

## 1. What changed: three scenarios became five

SRQ4 previously compared three scenarios, all on GPT-5.5, because Prometheus access
was pending:

| Scenario | Engine | Forecast access |
|----------|--------|-----------------|
| `A_plain` | GPT-5.5 | none |
| `B_data` | GPT-5.5 | Code Interpreter |
| `C_model` | GPT-5.5 | `forecast_demand` tool |

With the engine in hand we are adding two more:

| Scenario | Engine | Forecast access |
|----------|--------|-----------------|
| `D_prometheus` | **Prometheus Graph Engine** | none (code-as-action, as shipped) |
| `E_prometheus_model` | **Prometheus Graph Engine** | **`forecast_demand` tool** |

### Why two rather than one

A single "Prometheus + tool" scenario would move **two variables at once** (engine
*and* tool) relative to `C_model`, so any difference would be uninterpretable.
Splitting them gives:

- **D → E** — same engine, same prompts, one variable: the tool. This is the
  comparison the thesis has claimed from the start, now measured in the production
  system rather than a stand-in.
- **B → C and D → E** — the *same intervention on two different orchestrators*. If
  both move the same direction, the finding is not an artifact of one harness. This
  is the strongest structural feature of the design.

### What this does to B_data

`B_data` was built as a proxy for Prometheus while access was pending. Once D
exists it stops being a proxy and becomes "generic LLM with code execution." We
will say that explicitly in the methodology — stated openly it reads as a plan that
improved when a dependency unblocked; noticed unprompted it reads as drift.

### On reproducibility

D and E cannot be re-run by an examiner (proprietary, NDA). Rather than apologise
for that, we present two tiers that corroborate each other: **A–C** reproducible
from the repo plus an API key, **D–E** ecological validation nobody outside the
collaboration could produce. Neither alone covers both internal and external
validity.

---

## 2. The credentials question — resolved, and we did not need you

I asked you for `E2B_API_KEY` and `PROMETHEUS_TEMPLATE_ID`, and you mentioned you
had hit the same problem and worked around it but could not recall how. Reading the
code answered it:

**`PROMETHEUS_TEMPLATE_ID` was never a secret.** The engine ships its own template
builder and recipe:

- `data_agents/sandboxes/build_template.py`
- `data_agents/sandboxes/templates/prometheus.yaml` ← the full recipe
- `data_agents/sandboxes/README.md`

Building it registers the alias **under your own E2B account**. So the value is a
build artifact, per-account, not a shared credential. That is very likely what your
workaround was.

Also relevant: `template_id` defaults to `None` in
`data_types.py::extract_all_env_vars`, and `AsyncSandbox.create(None, ...)` is
legal — it yields E2B's default image. So omitting the template does not crash. See
§3 for why we are building it anyway.

**`E2B_API_KEY` is self-serve.** E2B is an ordinary SaaS vendor (e2b.dev), free tier
available. I signed up and loaded $5 on my own key, so **no cost lands on you for
the sandbox side.**

**RU warehouse credentials work.** Verified live by running
`02_thesis_data/_00_raw/nielsen/scripts/nielsen_connector.py` — it connected and
returned rows from all four views. That also gives free evidence that the
service-principal flow the engine's `security/token_swap.py` depends on succeeds
with our credentials.

---

## 3. A confound we nearly walked into

Before building the template I ran one probe on E2B's **default** sandbox to
measure cost cheaply. It reported:

```
pandas 2.2.3
MISSING pyodbc
MISSING sqlalchemy
MISSING statsmodels
MISSING xgboost
MISSING prophet
```

The base image is bare. This matters more than warehouse access:

**`D_prometheus` is the code-as-action scenario — its entire measurement is whether
the LLM can write working forecasting code.** With no `statsmodels` and no
`prophet`, it cannot fit a real forecasting model at all. Running D on the default
sandbox would **silently handicap it and inflate the D → E gap in our own
favour** — the worst class of confound, one that flatters our contribution.

So the template build is mandatory before any D run is scored. Cost of learning
this: a fraction of a cent, versus a full build cycle.

**E2B cost is otherwise a non-issue**, though the figure moved once the template
existed. Measured on the built `prometheus` template: **36.3s per sandbox
lifecycle**, against 3.08s on the bare image -- ~12x, on an identical workload. That
is import cost, not compute (`prophet`/`statsmodels` pull in `cmdstanpy` and
`scipy`), and it is paid **once per sandbox**, which the engine reuses across a
conversation. 60 D-runs is ~36 sandbox-minutes, still under a dollar of my $5. The
OpenAI side (~$42 for the full design) remains the only cost that matters.

**One risk this introduces, worth flagging before any scored run:** a 28-second
first import is long enough to collide with a *per-execution* timeout, which is a
different limit from `AsyncSandbox.create(..., timeout=600)`. If the executor caps
single calls below ~30s, D's first tool call fails on cold start and the trace reads
as "the LLM wrote bad code" when it is really a startup timeout -- depressing D and
inflating D -> E in our favour. I am checking `code_executor.py` for this before
running anything scored.

---

## 4. What the archived blueprint got right

`.archive/thesis_agents_preintegration/system_a_oracle/` — your pre-access work —
predicted the integration surface accurately. Verified against the shipped engine:

| Blueprint claim | Shipped |
|-----------------|---------|
| `langgraph.json` graph registry | ✓ 21 agents |
| `projects/<name>/<name>.py:<name>_graph` | ✓ exact |
| `ProjectDeps(agent_name, tool_names, …)` | ✓ exact |
| `@data_agent.tool` + `RunContext[CodeExecutorDeps]` | ✓ exact |
| `create_quantitative_research_graph(deps)` | ✓ exact |

One correction: import `data_agent` from
`data_agents.graphs.quantitative_research_graph`, not `agents.base_agents` — follow
the shipped `projects/prometheus/tools/weekly_report_tool.py`, which is a live
working example.

Three things in the blueprint are stale and will be fixed on port: the
`parents[3]` path to `forecast_service.py` (moved in P0028), the `chain` parameter
(chain grain deleted per DEC-GRAIN), and the "~50 prompts / System A vs B" framing
(now 1 prompt × N repeats).

**An unplanned win:** `prometheus.py` sets `main_agent_model="gpt-5.5"` and
`coder_model="gpt-5.5"` — the same family as A–C. D/E will not differ from the GPT
scenarios by base model.

---

## 5. SRQ1 findings from the same session

### The SHAP artifact was 40 days stale — and `shap` was not in requirements

`shap_importance.csv` dated 2026-07-10 against `tuned_metrics.csv` at 2026-08-19.
**Root cause: `shap` was absent from `requirements.txt` entirely** and not installed
— the script could not run in a clean environment. Same failure class as the
`optuna`/`joblib` gaps. Added and regenerated.

What changed after regeneration:

| Feature | Old | New |
|---------|-----|-----|
| CSD `promo_intensity` | 0.100 (7th) | 0.041 (11th) |
| CSD `weighted_distribution` | **1.146 (2nd)** | **absent** |

**Anything in the drafts citing `weighted_distribution` as a leading predictor is
now wrong** — it was dropped from model inputs in `f4779a7`.

### Feature importance is not feature selection — we have a measured instance

Worth a methodology paragraph. `weighted_dist` ranked **#2 by SHAP** yet dropping it
**improved** accuracy in 3 of 4 categories. The obvious explanation — redundancy
with the lags — does not hold: partial correlation with the target controlling for
`lag_1` is **0.594** against a raw 0.673, so it carries genuinely independent
information.

The resolution is that SHAP measures how much a fitted model *used* a feature,
while held-out error measures whether that reliance *generalised*.
`weighted_dist` is nearly static (corr(t, t−1) = 0.976), close to a brand
fingerprint — a tree can use it to recognise which brand it is looking at and recall
that brand's level, which works until distribution shifts. Had it been merely
redundant, removing it would have been neutral; that removing it *helped* indicates
active harm.

Also note for the write-up: this was an **accuracy decision, not a leakage fix.**
The feature was tested for leakage and cleared. Conflating the two would
misrepresent the process.

### SRQ4 brand selection is now stratified

Top-N-by-volume evaluated every scenario on the largest, most stable series. Now
`--brand-strategy stratified` takes highest/median/lowest **among brands with a
fully non-zero test window** — 12 pairs spanning 237,169,352 down to 439 units.

The zero filter is not cosmetic: **40% of nominally eligible brands would have
produced undefined APE** (danskvand's and energidrikke's lowest-volume brands have
*all-zero* test windows, so APE is a divide-by-zero, not a number).

### An open SRQ1 gap worth your attention

SRQ1's headline question names a **three-way** trade-off — accuracy, memory
efficiency, and **category specialization**, glossed in
`srq1-models-efficiency.md:32` as *"does a per-category model beat a single pooled
model?"* `tuned_metrics.csv` reports the first two and has **no pooled row**; grep
finds no pooled code path.

The thesis currently asks a question in its own SRQ1 heading that its results do not
answer. Pre-run checks are done and encouraging: **33 of 51 feature columns are
common to all four categories**, **no correlation sign inversions**, and the log
target makes scale comparable. The 18 non-shared columns are one family
(`baseline_*`, `promo_*`) absent because danskvand and RTD have no promo signal —
which is a finding about the Danish market, not an arbitrary restriction.

---

## 6. Where it stands, and what is next

**Done:** engine inspected, tool API verified, data access understood, credentials
confirmed, E2B cost measured, **template built and verified**, **engine environment
built**.

The `prometheus` template is live and the alias resolves, so nothing in the engine
config needs rewiring. All five packages confirmed present (`pyodbc`, `sqlalchemy`,
`statsmodels`, `xgboost`, `prophet`) against all five missing on the base image.
Template id `fxe7gzkqjupdhbx4uvpr`, and I set `skip_cache: false` in
`prometheus.yaml` so future rebuilds reuse layers.

Worth knowing if you ever rebuild: the first attempt died with a `CancelledError` in
its log poller, and **the build did not survive the disconnect** -- probing the id
returned `404: tag 'default' does not exist`, i.e. the template record existed with
no completed build. Re-running under python 3.13 rather than 3.14 worked first time.

**Next (Brian):**

1. Get the engine running locally on the shipped Prometheus project.
2. Check `code_executor.py` for a per-call timeout (see the cold-start risk above).
3. Port `forecast_demand` to the verified tool API.

**The environment question is settled.** The engine now has its **own** venv, built
with `uv sync --frozen --python 3.13` against the shipped `uv.lock`. Both hard pins
are satisfied -- `e2b_code_interpreter==2.0.0`, `pydantic-ai==1.73.0` -- and the
thesis venv keeps 2.9.1, which `B_data` imports. Downgrading the shared venv would
have meant breaking a working scenario to enable an unbuilt one.

Two corrections to what I said earlier: the engine requires **`>=3.12`**, not 3.11
(that came from the archived blueprint), so the python version was never the blocker
-- the `==` pins are. And I picked 3.13 specifically because your shipped `.venv`
records `version_info = 3.13.2`, so it is the version the engine is known to run on
at your end.

Your shipped `.venv` was replaced: it was a Linux venv pointing at
`/home/niks/miniconda3/bin`, unusable on Windows and fully reconstructible from
`uv.lock`.

**Budget.** Full stratified design at 5 repeats is **$41.85** on the OpenAI side, of
which `A_plain` alone is $25.46 (61%) — it is the most expensive scenario despite
having no tools, because reasoning tokens bill at the output rate. Plan is to run
B/C/D/E first, lock the design, and re-run A **last**, so a configuration change
never wastes the expensive arm. Thanks for the 2,000 DKK — it takes the budget from
binding to comfortable.

---

## 7. Questions for you

1. **SRQ3 scope.** `srq3-integration-readiness.md` frames SRQ3 as an *assessment* by
   design, not merely because access was blocked. Now that we have the engine, do we
   reframe it as a completed integration, or leave it? That is a scope call for the
   two of us, not something access settles by itself.
2. **Pooled vs per-category** (§5) — do you agree it is a real gap to close before
   submission? It is one training run on a 33-column intersection, no API spend.
3. **Anything you remember about the engine's local run** — the README's known
   unknown was the E2B template id, which is now answered, but if you hit anything
   else when you ran it, that would save time.

---

## Related

- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/` — full findings F1–F41
- `05_thesis_writing/notes/prometheus-scenarios-design-rationale.md` — write-up notes
- `user-docs/handovers/2026-08-19_srq4-experiment-handover-enrico.md` — the A/B/C ladder
