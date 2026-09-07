---
name: p0049-inherited-context
description: STATE - Everything absorbed from P0039, P0040, P0042 and P0044 before those plans were archived. Decisions, delivered evidence, and design rationale that must survive the account switch. Do NOT re-derive any of this.
pid: P0049
created: 2026_09_07-18_30
updated: 2026_09_07-18_30
---

# Inherited context (P0039 · P0040 · P0042 · P0044)

Those four plans are archived. **Everything still live from them is here.** Read this
rather than the archive; the archive is kept for provenance, not for working from.

---

## 1. The experiment the thesis actually rests on

> Does having a trained forecasting model **available as a tool** improve an LLM's
> answers, compared with giving it the raw data and letting it write its own
> forecasting code?

**One variable under test: how the agent produces a forecast.** Model, prompts,
temperature, brand and horizon are held constant.

### The five-scenario ladder

| Scenario | Engine | Forecast access | Examiner can reproduce |
|---|---|---|---|
| `A_plain` | GPT-5.5 | none | yes |
| `B_data` | GPT-5.5 | code execution | yes |
| `C_model` | GPT-5.5 | `forecast_demand` tool | yes |
| `D_prometheus` | Prometheus Graph Engine | none (code-as-action, as shipped) | **no** — proprietary |
| `E_prometheus_model` | Prometheus Graph Engine | `forecast_demand` tool | **no** — proprietary |

**Naming is `{LETTER}_{suffix}`** (Brian, 2026-08-20) — the suffix names the capability
so logs stay legible once letters stop carrying meaning alone.

**Why two Prometheus scenarios, not one.** A single one would move *engine* and *tool*
together, so a C→D difference could not isolate the contribution. Splitting gives
**D→E**: same engine, same prompts, one variable. And because **B→C and D→E are the same
intervention on two different orchestrators**, agreement between them is a materially
stronger claim than either alone.

**Reproducibility is a design feature, not a concession.** A–C is the reproducible core
(repo + an API key); D–E is ecological validation nobody outside can rerun. Two tiers
that *agree* beats pretending the whole ladder is reproducible.

**B_data's role was reframed.** It began as a stand-in for Prometheus while access was
pending. Once D exists, B is "generic LLM with code execution". **Say this explicitly in
the methodology** rather than letting a reviewer notice the reframing.

---

## 2. DELIVERED EVIDENCE — the A/B/C ladder (2026-08-19, $4.92)

`05_thesis_results/srq4_scenario_experiments/RESULTS_2026-08-19.md` (the path P0042 gives
is stale). Verified against source. On HARBOE:

| Scenario | median APE | CV across repeats | latency | cost (3 runs) |
|---|---:|---:|---:|---:|
| A_plain | 35.1 % | 3.65 % | 108.7 s | $1.482 |
| B_data | 17.3 % | 5.27 % | 115.4 s | $0.830 |
| **C_model** | **13.8 %** | **0.00 %** | **5.9 s** | **$0.020** |

**`C_model` beat `B_data` on every run of both brands — C's worst run beat B's best.**
Across both brands the aggregate is **median APE 7.7 % (C) against 13.5 % (B)**.

Note what C wins on beyond accuracy: **zero variance across repeats**, ~20× faster, and
~40× cheaper. That is the tool-interface argument in one table.

⚠ **These were produced against the H1-mislabelled-as-H3 track record (F22).** The
comparison is sound — every scenario saw the same tool — but the horizon label needs
correcting wherever these are reported.

---

## 3. Decisions — settled, do not reopen

| ID | Decision | Source |
|---|---|---|
| **DEC-SCENARIO-SPLIT** | Five scenarios; D plain and E tooled | P0040, Brian 2026-08-20 |
| **DEC-HORIZON** | H=3 primary; implement + benchmark both horizons | P0039 / P0048 |
| **DEC-RSS** | Measure process **RSS**, not `tracemalloc` | P0044 |
| **DEC-SUBPROCESS** | Profile each model in a **fresh subprocess** | P0044 |
| **DEC-REFIT-NOT-RETUNE** | Retrain-per-query refits on stored hyperparameters; it does **not** re-run Optuna | P0044 |
| **DEC-ARMS-LOW-N** | Retrain arms at n=3 | P0044 |
| **DEC-ARCHIVE-NOT-DELETE-PROSE** | Superseded prose is archived, never deleted | P0044 |
| **DEC-GRAIN** | brand × month | earlier |
| **DEC-DETERMINISM** | Accuracy `n_jobs=1`; resource profiling `-1` | P0047 F18 |

### Still OPEN

**DEC-VENDOR** — which LLM is primary. The harness hardcoded `claude-sonnet-4-6` with
**no justification recorded anywhere in the thesis**, and an unargued default is exactly
what a reviewer probes. Brian favours GPT. ~$7 (Claude) vs ~$4 (GPT) for 50 runs, so
**cost is not the deciding factor at this scale — decide on ecological validity.**

> The harness now pins `gpt-5.5-2026-04-23`, a dated snapshot, and `verify_setup.py`
> confirms it is reachable and that temperature is not settable (recorded honestly as
> "temperature/top_p unsupported by the model; defaults used"). So the *de facto* choice
> is GPT; what is missing is the **written justification**.

---

## 4. Why the RAM claim needed rebuilding (P0044)

Brian's Word comments [18] [19] [20] [22] [25] challenged the thesis's central RAM
premise. The investigation found the code **half-supported and half-refuted** him:

- [25] "memory efficiency is not tracked" was **wrong** — it was measured and published.
- But **the instrument was broken**, which is what he actually suspected. It used
  `tracemalloc`, which sees only Python-level allocations. LightGBM and XGBoost allocate
  trees in **C++**. XGBoost reported **0.1 MB peak** — less than Ridge, which is
  impossible at `n_estimators=1040, max_depth=10`.

So the published table understated tree models by an unknown factor, and the ≤8 GB claim
rested on it. Hence DEC-RSS and DEC-SUBPROCESS: **fix the instrument before rewriting the
framing**, or the new promise sits on the same sand.

**The binding figure is the MEASURED 4096 MB Prometheus E2B template — not the assumed
8 GB SME envelope. Those are different budgets; do not conflate them.**

### Measured, keep

- **Refit 2.93 s vs re-tune 417 s — 142×.** This is what makes the retrain-per-query
  architecture affordable and the argument defensible.
- **7-month parameter drift: inconclusive.** Report as inconclusive; do not round it into
  a claim.

---

## 5. Facts inherited from earlier plans — do not re-derive

| Fact | Origin |
|---|---|
| Feature matrices, 4 categories × 2 horizons, verified 8/8 | P0038 |
| `forecast_service.build_service()` produces 230 forecasts across 4 categories | P0037 F13 |
| Every forecast carries a `trace` block (model, cutoff, calibration split) | P0037 F12 |
| Intervals are honestly calibrated and **wide** — median 3× the forecast | P0037 F10/F11 |
| Prophet diverges on individual series → report **medMAPE, not WMAPE** | P0038 F72 |
| E2B cost ≈ **$0.0001/run** — negligible | P0040 F38 |
| RU warehouse credentials verified live | P0040 F35 |
| Archived Prometheus blueprint's API is correct | P0040 F13 |

---

## 6. Sequencing rules carried from P0042

**Two workstreams that are genuinely independent — do not serialise them:**

| | A — Review rounds | B — Scenario runs |
|---|---|---|
| Where | NotebookLM browser | cloud session |
| Cost | none | API spend |
| Owner | Brian, interactively | separate session |

**The one coupling:** B produces the numbers Ch7/Ch8 report, so A's Ch7/Ch8 review
cannot run until those numbers exist. Everything else is parallel.

**Frozen sampling design** (`2026-09-01_DOC-srq4-sampling-design.md`): **111 runs,
~$40 realistic**, allocated *inversely to per-run cost* — A n=3, B/C n=10 stratified,
C-only cross-category.

**The E2B template build is REQUIRED before D/E**, not optional: the base image lacks
`statsmodels`/`prophet`, so scenario D would be silently handicapped and D→E would
measure the missing library rather than the tool.

---

## 7. Stale claims in those plans — corrected here

| Plan said | Reality |
|---|---|
| P0039: "blocked on `03_thesis_modelling/.env`" | That path does not exist. `.env` is at repo root (11 keys); `verify_setup.py` passes **10/10**. |
| P0042: "gate 1 discharged, A/B/C unblocked" | True then. **Now gated on the horizon fix** (F22). |
| P0044: "profiling publishes to `04_thesis_results/srq1/`" | Results moved to `05_thesis_results/srq1_model_performance/tables/`. |
| P0042: results at `04_thesis_results/srq4/` | Now `05_thesis_results/srq4_scenario_experiments/`. |

**The lesson:** a stated blocker is a claim with a timestamp. Check it before acting on
it — two of the four were stale.
