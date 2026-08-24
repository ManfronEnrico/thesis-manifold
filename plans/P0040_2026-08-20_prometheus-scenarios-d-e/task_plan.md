---
pid: P0040
created: 2026-08-20 00:00:00
updated: 2026-08-20 12:00:00
status: focus
focus_detail: "Extend the SRQ4 ladder from three scenarios to five by adding the real Prometheus Graph Engine: D_prometheus (as it ships, code-as-action) and E_prometheus_model (same engine, plus the forecast_demand tool). D->E is the thesis contribution measured inside the production system, and it independently replicates B->C. Tasks 1-3 DONE 2026-08-20: the archived blueprint's API is correct (F13), the engine runs gpt-5.5 like scenarios A-C, RU warehouse credentials verified live (F35), and E2B cost measured at ~$0.0001/run -- negligible (F38). Nothing external is blocked: E2B key is Brian's own, and PROMETHEUS_TEMPLATE_ID is a build artifact of a recipe that ships with the engine. Next: build the template (REQUIRED -- base image lacks statsmodels/prophet, so D would be silently handicapped), then run the engine locally."
---

# P0040 — Prometheus scenarios D and E

## Goal

Measure the thesis contribution **inside the production agent**, not only in a
GPT-based stand-in.

> Does adding a dedicated forecasting model as a tool improve Prometheus's
> answers, versus Prometheus writing its own forecasting code?

## The five-scenario ladder

| Scenario | Engine | Forecast access | Reproducible by an examiner |
|----------|--------|-----------------|------------------------------|
| `A_plain` | GPT-5.5 | none | yes |
| `B_data` | GPT-5.5 | Code Interpreter | yes |
| `C_model` | GPT-5.5 | `forecast_demand` tool | yes |
| `D_prometheus` | Prometheus Graph Engine | none (code-as-action, as shipped) | **no** — NDA/proprietary |
| `E_prometheus_model` | Prometheus Graph Engine | `forecast_demand` tool | **no** — NDA/proprietary |

**Naming convention (Brian, 2026-08-20): `{LETTER}_{suffix}`.** The suffix names
the capability so every log line and results table stays legible once letters stop
carrying meaning on their own. Applies to D and E exactly as to A-C.

### Why two Prometheus scenarios rather than one

A single Prometheus scenario would move **two variables at once** (engine *and*
tool), so a C-to-D difference could not isolate the contribution. Splitting gives:

- **D -> E** — same engine, same prompts, one variable: the tool. This is the
  comparison the thesis has claimed since the outset.
- **B -> C and D -> E** — the *same intervention on two different orchestrators*.
  Agreement between them is a materially stronger claim than either alone.

### What this does to B_data's role

B_data was built as a stand-in for Prometheus while access was pending. Once D
exists, B is no longer a proxy — it becomes "generic LLM with code execution."
**State this explicitly in the methodology** rather than leaving a reviewer to
notice the reframing.

### Reproducibility is a design feature, not a concession

A-C is the reproducible core (repo + an API key). D-E is ecological validation
that no third party can rerun. Presenting them as two tiers that *agree* is
stronger than pretending the whole ladder is reproducible.

## Decisions

### DEC-SCENARIO-SPLIT — five scenarios, D plain and E tooled

**Status: SETTLED (Brian, 2026-08-20).** Superseded the earlier single-scenario-D
proposal for the confound reason above.

### DEC-PROMETHEUS-VENDORING — the engine never enters the repo

**Status: SETTLED (Brian, 2026-08-20).**

The Graph Engine is Manifold AI proprietary (~500 MB extracted). It stays a
**sibling of the repo**, located via `.env`:

```
PROMETHEUS_ROOT=Z:/_dev-ssd/prometheus
```

The repo holds only a thin, committable, auditable adapter under
`03_thesis_modelling/scenario_setup/`. Rationale is IP and thesis-repository
publication, not file size. `.gitignore` already covers `.env`, `.env.*` and
`*.7z`; add a defensive `prometheus/` entry in case the tree ever lands inside
the repo.

### DEC-PROMETHEUS-DATA — same snapshot across all five scenarios

**Status: SETTLED in principle (Brian, 2026-08-20); verify in task 3.**

Initial concern was that D/E reading the live Royal Unibrew warehouse while A-C
read the local Nielsen snapshot would break comparability and risk leaking the
target month.

**Brian's correction, which resolves it:** the warehouse is **not** updated daily.
It is refreshed roughly monthly, and a re-poll on 2026-08-19 returned data through
**July 2026 — identical to the local snapshot.** So within August the two sources
*are* the same snapshot, and the concern is largely theoretical.

Decision: prefer pointing Prometheus at the **local snapshot** where supported
(the archived `data_credentials.json` uses `type: file`, suggesting it is), because
it makes identical-input an *enforced property* rather than a timing coincidence.
Fall back to the live connection if the engine requires it, and record which was
used in every run trace. **If the run slips past August, re-verify** — the
coincidence expires when the warehouse next refreshes.

## Inherited context (do not re-derive)

| Fact | Source |
|------|--------|
| A/B/C ladder runs, 18 paid runs logged | P0039, `04_thesis_results/srq4/` |
| C beat B on every run: 7.7% vs 13.5% median APE | P0039 results |
| C is also ~28x cheaper and ~22x faster than B | P0039 results |
| `forecast_tool.py` loads persisted models, never fits | P0037 task 3 |
| Every forecast carries a `trace` block | P0037 F12 |
| Conformal calibration uses val residuals, not test | P0037 task 7 |
| Chain grain deleted; brand x month is locked | DEC-GRAIN |
| Enrico has funding for the D/E API spend | Brian, 2026-08-20 |

## The archived integration blueprint — read critically

`.archive/thesis_agents_preintegration/system_a_oracle/` contains a
`forecast_demand_tool.py`, README and persona doc describing how to register the
tool with the Graph Engine.

**Provenance caveat (Brian, 2026-08-20):** this is most likely Enrico's work from
*before* the team had Prometheus access. Its own README concedes *"Not yet wired
into a running engine (needs `oracle.py` + a local engine run; E2B template id to
confirm)."*

**Treat it as a hypothesis about the engine's API, not a description of it.** It is
specific in ways that suggest real knowledge — `@data_agent.tool`, imports from
`data_agents.agents.base_agents`, `ProjectDeps.tool_names`, pydantic_ai, LangGraph,
registration in `langgraph.json` — but none of that is verified against what
shipped. Task 1 is exactly that verification.

Known-stale regardless of whether the API matches:

| Reference | Current state |
|-----------|---------------|
| `scripts/forecast_service.py` via `parents[3]` | moved in the P0028 restructure; path resolves to nothing |
| `chain` parameter, `_07_forecast_service/` | chain grain deleted per DEC-GRAIN |
| "~50 prompts", "System A / System B" | superseded: 1 prompt x N repeats, scenarios, reversed lettering |

## Tasks

| # | Task | Phase | Blocked by | Status |
|---|------|-------|-----------|--------|
| 1 | Verify the engine's real tool API against the archived blueprint | 1 | -- | **done** (F13) |
| 2 | Locate `prometheus.py`, `langgraph.json`, and the tool-registration path | 1 | -- | **done** (F13) |
| 3 | Determine how data access is configured; confirm local-snapshot support | 1 | -- | **done** (F18, F35) |
| 3b | Build the `prometheus` E2B template -- **required**, base image is bare (F38) | 1 | -- | **done** (F42) |
| 4 | Get the engine running locally on the shipped Prometheus project | 2 | 3b | **in_progress** -- env built + verified (F46); per-call timeout ruled out (F45); engine not yet launched |
| 5 | Run `D_prometheus` on the SRQ4 prompt with logging + cost capture | 2 | 4 | pending |
| 6 | Port `forecast_demand` to the verified API; drop `chain`; repoint via PATHS | 3 | 1, 4 | pending |
| 7 | Register the tooled project and run `E_prometheus_model` | 3 | 6 | pending |
| 8 | Analyse D->E against B->C; check the two agree in direction | 4 | 5, 7 | pending |
| 9 | Measure the engine's real RAM footprint (see below) | 4 | 4 | pending |
| 10 | Write up; fold into the SRQ4 results section | 4 | 8, 9 | pending |
| 11 | Seed sweep on the per-brand pooled analysis -- is LightGBM's null stable? | 5 | -- | pending |
| 12 | Build `F_ensemble` -- pooled + specialised served together, C->F measures whether disagreement helps | 5 | 11 | **decided** (F55) |
| 13 | Add both metrics (WMAPE + medMAPE) for model and benchmark to the payload | 2 | -- | **done** (F56) |
| 14 | Add brand volume tercile + within-tercile model accuracy to the payload | 3 | 13 | pending -- now part of task 18 |
| 18 | Context-and-predictions factorial: 5 cells, PILOT FIRST | 5 | 13, 15 | **designed** -- see `context_experiment_design.md` |
| 19 | Serve "n/a" instead of implausible error rates in the payload | 2 | -- | **done** (F64) |
| 20 | Ch6: regenerate all accuracy numbers; add benchmarks, pooled, Ridge, CV protocol | 1 | 15 | pending (F66) |
| 21 | Fix `fig4_ram_budget` -- hardcoded 512 MB vs measured 3-4 MB | 1 | -- | pending (F66) |
| 22 | Ch3: remove the judge protocol where it is SPECIFIED, not just referenced | 2 | -- | pending (F66) |
| 23 | Ch8 rewrite -- structure assumes a two-arm judge-scored design | 4 | 5, 7 | pending (F66) |
| 24 | Ch9/Ch10: SRQ3 integration framing + inherited vocabulary | 4 | 23 | pending (F66) |
| 25 | Add NUMBER-level rules to check_chapter_facts.py | 3 | 20 | pending (F66) |
| 15 | Re-tune with expanding-window CV, 100 trials, dual objective | 2 | -- | **done** (F65, F67) |
| 16 | Ridge reporting: publish clipped + unclipped both | 3 | -- | **done** -- DEC-RIDGE-BOTH; refuted F57, see F63 |
| 17 | Verify every citation in the writing notes against the actual sources | 5 | -- | pending (F59) |

### Task 15 -- CV re-tune (running 2026-08-22)

`srq1_benchmark_cv.py --trials 100 --folds 4`. 16 studies x 100 trials x 4 folds
~= 6,400 fits. Outputs `cv_metrics.csv`, `cv_convergence.csv`, `cv_params.json`,
`cv_summary.md`.

**When it finishes, check three things:**
1. `plateau_trial` -- if most studies plateau well before 100, the budget is
   justified empirically and that is what the write-up should say (there is no
   citable convention for trial count; see F59).
2. Whether tuning for medMAPE selects a different model than tuning for WMAPE. If
   not, the objective choice was immaterial and that is reportable.
3. Whether CV-tuned test scores differ materially from the single-split scores in
   `tuned_metrics.csv`. A large gap means the single split was lucky or unlucky and
   the old numbers should be superseded rather than reported alongside.

### Task 17 -- citation verification (BLOCKING for submission)

Brian requires an academic source at every best-practice decision. F59 lists what is
safely citable and, importantly, **what is not**: the "50-200 trials" convention
(folklore, no source), the 3x extrapolation bound (invented here), and the
`confidence` index (arbitrary weights).

Every reference in the writing notes is a LEAD TO VERIFY. Page numbers, exact titles
and whether the claim appears where stated must be checked against the real sources.
Do not submit with an unverified citation.

### Task 11 -- seed sweep (no API spend)

F51 found the brand-level "pooling helps small brands" mechanism holds for XGBoost
(win-rate 68/59/54 across volume terciles) and is flat for LightGBM (46/45/46,
corr = -0.014 against training rows). Single seed, single split, so the null could
be stable or a one-seed artifact.

Run `srq1_pooled_perbrand.py` across ~5 seeds and check whether LightGBM's flat
win-rate persists. Cheap, no API spend. **Only worth doing if the brand-level
mechanism becomes load-bearing in the prose** -- the category-level result (F49),
which is the actual SRQ1 deliverable, does not depend on it.

A hypothesis worth testing at the same time: LightGBM grows trees leaf-wise and its
`min_child_samples` may let a POOLED model carve brand-specific leaves, which would
blur the pooled/specialised distinction that XGBoost's depth-wise growth preserves.
If true, the tuned `num_leaves`/`min_child_samples` for the pooled LightGBM should
be markedly different from the per-category ones -- checkable from
`pooled_params.json` without refitting anything.

### Task 12 -- `F_ensemble` as a sixth scenario (DECIDED 2026-08-22)

Brian's proposal (2026-08-22): have `forecast_demand` return BOTH the pooled and
the per-category prediction, with accuracy context, so the agent has more than one
model datapoint. **Explicitly not a model-selection choice** -- both values are
returned unconditionally, so the agent is not asked to pick.

**In favour.** It does not break the SRQ4 ladder as a selection choice would: the
agent makes no additional decision, it receives a richer observation, so `B->C`
still measures "what does trained-model access buy?". Disagreement between the two
models is itself an uncertainty signal that neither model's own conformal interval
captures -- the same logic `srq2_synthesis.py` already applies to inter-model
agreement. Under SRQ2 this is a defensible interface-design contribution: a single
point estimate understates model risk.

**Against.** It changes what `C_model` and `E_prometheus_model` ARE. Today C is
"the artefact this thesis built, served"; with two model families plus agreement
signals it becomes a stronger but different artefact, and the SRQ4 methodology text
describing C needs rewriting. With ~1 month to submission, every payload field added
is a field whose effect on the B->C and D->E deltas is unmeasured -- if C improves,
attribution across the added fields is not possible.

**Constraint if adopted:** it must land BEFORE any scored run, never between runs,
and as one deliberate documented change rather than incremental additions.

**RESOLVED (Brian, 2026-08-22): make it a separate scenario, not a change to C.**

That removes the objection above entirely -- `C_model` stays exactly as specified,
and the ensemble becomes its own rung with its own measurement:

| Scenario | Serves |
|----------|--------|
| `C_model` | specialised model: prediction + interval + accuracy context |
| `F_ensemble` | pooled AND specialised, each with WMAPE + medMAPE, plus agreement |

`C -> F` isolates one variable: does exposing model disagreement improve the agent's
forecast? Publishable either way -- a null says one well-calibrated estimate
suffices.

Brian's structural argument: the thesis already runs specialised-vs-pooled at the
data/model layer (F49); running it again at the serving layer asks the same question
one level up, making it a through-line across two RQs rather than a bolt-on.

**Scope:** one orchestrator only -- the question is about the interface, not the
engine, so no Prometheus twin.

**Cost:** ~$8-10 at 5 repeats. **Sequence LAST**, after B/C/D/E lock and A_plain
runs. An un-started scenario drops for free; a half-integrated ensemble inside C
would contaminate the cleanest comparison in the thesis.

See F55 for the full rationale, F56 for what the payload should and should not
carry (statistics yes, extra point predictions no).

### Task 13 -- both metrics in the payload (F56)

Add medMAPE alongside WMAPE for the served model AND the benchmark, and consider
reporting both baselines rather than one. Rationale: `_track_record` currently picks
the best baseline by medMAPE, which for RTD selects Naive (44.1%) and reports
+7.4pp improvement; selecting by WMAPE would pick SeasonalNaive (27.3%) and show the
model **losing by 6.3pp**. Same data, opposite story. Disclose the choice rather
than letting it read as neutral.

Must land BEFORE any scored run.

Tasks 1-3 are **read-only and free** and decide the entire cost estimate.

## The RAM budget — a real finding replaces a fabricated one

`04_thesis_results/generate_figures.py::fig4_ram_budget` is currently **hardcoded
and invented** (a literal 500 MB Python runtime, 512 MB "active ML model"). The
measured reality is that the served model needs **3-4 MB**.

Prometheus does not invalidate the compute-constraint argument — it **rescues** it.
The defensible claim was never "ML models are heavy"; it is:

> The model is the cheap part. The agent runtime is where the budget goes.

Task 9 measures the engine's actual footprint and regenerates the figure from
measurement. This converts the thesis's weakest figure into a genuine result.

## Out of scope

- Retraining or model reselection (SRQ1 settled)
- The A-C scale-up run (P0039; deliberately lower priority than D/E — the
  scale-up strengthens a result already established in direction, whereas D/E is
  the only result nobody else could produce)
- The ensemble iteration (deferred; see findings)
- Reframing SRQ3 from "assessment" to "integration" — a scope decision for Brian
  and Enrico, **not** settled by access alone

## Related

- `plans/P0039_2026-08-19_01-45_srq4-system-a-vs-b/` — the A/B/C ladder this extends
- `plans/P0037_2026-08-12_15-28_serving-interface-refinement/` — its out-of-scope
  line ("Prometheus/Graph Engine integration ... pending NDA") is what expired
- `00_thesis_context/prometheus-integration/` — April architecture docs
- `01_thesis_research/research-questions/srq3-integration-readiness.md`
- `.archive/thesis_agents_preintegration/system_a_oracle/` — the unverified blueprint
