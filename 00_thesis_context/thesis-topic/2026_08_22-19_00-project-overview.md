# Project Overview — Manifold AI Thesis

> **Updated 2026-08-22.** Corrections applied: SRQ4 scenario ladder, LLM-as-judge
> dropped, Prometheus access landed, benchmark set widened to 8 model families,
> accuracy targets restated with the metric named, `model_serving_interface/` rename.

> *Extending Production Agentic Decision-Support with Lightweight Forecasting for FMCG Retail*
> CBS Master's Thesis · Business Administration & Data Science · Deadline 15 May 2026

> **Navigation document.** Canonical detail lives in the linked files — this page states the
> problem and points at the sources of truth. Do not embed copies of research questions,
> literature, or architecture here; they drift.

---

## 1. The Problem

**Manifold AI** builds "AI Colleagues" — production-deployed conversational AI assistants
embedded in BI workflows for Danish retailers and consumer goods manufacturers. The current
system operates at a **descriptive analytics level**: it retrieves and explains historical
data, but has no native predictive capability. It cannot forecast future demand, issue
confidence-qualified recommendations, or communicate uncertainty to the user.

This is not a prototype gap — it is a capability gap in a live, deployed product. The thesis
treats Manifold AI's existing agentic system as the empirical anchor: a production-oriented
agentic decision-support system to be **extended, not replaced**.

The extension requires solving three coupled problems:

1. **A predictive substrate** — lightweight forecasting models that fit realistic SME cloud
   deployment budgets (≤ 8 GB RAM) and perform reliably on FMCG retail demand data
2. **A reliable interface** — a structured tool/action interface exposing forecasting outputs
   to the agent layer with uncertainty, confidence bounds and traceability intact
3. **Integration readiness** — the architectural and operational conditions under which an
   existing agentic system can absorb forecast-informed decision-support without redesign

Core constraint: SME cloud deployments realistically budget **≤ 8 GB RAM**, ruling out
LSTM-class deep learning and large language models used as direct forecasters.

---

## 2. The Research Gap

Five gaps, whose intersection has not been addressed:

| # | Gap |
|---|---|
| G1 | No framework for extending an existing production agentic system with forecasting under ≤ 8 GB RAM |
| G2 | No head-to-head benchmark of naive / seasonal-naive / drift / Ridge / ARIMA / Prophet / LightGBM / XGBoost under an explicit RAM budget in retail FMCG |
| G3 | No structured tool/action interface design for exposing ML forecasts — with uncertainty and traceability — to LLM-based agents |
| G4 | Integration readiness criteria for agentic systems adopting predictive capabilities have not been empirically derived or validated |
| G5 | No replicable RAM profiling methodology for multi-component AI pipelines combining ML forecasting + LLM synthesis |

**Closest paper:** Bürger & Pauli (2024, EAAI) — *Hybrid AI and LLM-Enabled Agent for Industrial
Batch Processes*, an architecturally analogous system applied to dairy CIP process control. The
thesis is the retail FMCG transposition of this blueprint, under explicit RAM constraints and
with a production-extension rather than greenfield framing.

→ Full gap analysis, novelty statement and corpus mapping:
[`gap_analysis_v4.md`](../../01_thesis_research/literature/gap_analysis_v4.md)

---

## 3. Research Questions

→ **Canonical:** [`research-questions.md`](../../01_thesis_research/research-questions/research-questions.md)
— Main RQ + SRQ1–4, mirroring Ch1 §1.3, with per-SRQ scope files alongside.

Deliberately not restated here. Ch1 is the editing surface; a copy in this file would drift.

**Operative scope decisions** (detail in the canonical file):

- **SRQ4 comparator** — a code-as-action LLM that writes and self-corrects its own forecasting
  code, runnable locally in an E2B sandbox. **Extended 2026-08-22 to a five-scenario ladder**
  (A_plain / B_data / C_model / D_prometheus / E_prometheus_model) after Prometheus access
  landed; `B→C` and `D→E` apply the same intervention to two different orchestrators
- **SRQ4 metrics** — correctness / consistency / replicability (primary) + cost / latency
  (secondary). **All metrics are programmatic; LLM-as-judge was dropped (B-DEC-2).**
  **Prompt set is 1 prompt × N repeats**, not ≈50 varied prompts — repeats are what measure
  consistency. Ch8 reports a **pilot**; the full run is stated as further work
- **SRQ3** — an integration-readiness *assessment*, not a completed integration. **Prometheus
  Graph Engine access LANDED 2026-08-20** and the engine runs locally, so this framing is now
  an **open scope decision** for Brian and Enrico rather than a constraint

---

## 4. Methodology

**Design Science Research** (Hevner et al., 2004; Peffers et al., 2007), with Saunders, Lewis &
Thornhill (2023) as the research-design scaffold. Philosophy: pragmatism.

The thesis produces both an **instantiation** (a working extension of a production agentic
system) and a **method-level contribution** (generalised integration readiness criteria and
interface design principles reusable beyond this retail context).

→ [`00_thesis_context/methodology/`](../methodology/)

---

## 5. Data

- **Primary** — Nielsen / Prometheus star schema, Danish grocery at market scope
  `DVH EXCL. HD` (id `1256338`), grain brand × month. **Four categories**: CSD, Danskvand,
  Energidrikke, RTD.
- **Empirical reference case** — Manifold AI's production agentic system, for SRQ3
- **SRQ4 comparator** — code-as-action LLM baseline in an E2B sandbox

> **Two open reconciliations with Ch1 §1.4 — STILL OPEN, verified 2026-08-22.** Ch1 line 64
> states *five* categories (including totalbeer) and 37–42 periods; line 88 repeats "five
> categories". Totalbeer was excluded on compute grounds (Brian, 2026-08-01 — see P0034), and
> CSD measures **44** periods at parent market scope (measured 2026-08-11 — see P0036 F5).
> **Ch1 line 54 additionally still describes the dropped LLM-as-judge protocol.** All three
> need correcting before submission.

→ Pipeline and structure: [`02_thesis_data/`](../../02_thesis_data/)
→ Sample-size rationale, adequacy per SRQ, and tool-call mechanics:
[`sample-size-and-tool-interface-rationale.md`](../../05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md)

---

## 6. System Architecture

→ **Current:** [`user-docs/architecture/architecture.md`](../../user-docs/architecture/architecture.md)
→ Forecast service: `03_thesis_modelling/model_serving_interface/scenario_c_forecast/`
→ Scenario harness: `03_thesis_modelling/scenario_setup/`
> `model_serving/` was renamed `model_serving_interface/` on 2026-08-19, to name
> SRQ2's "Structured Tool Interface" explicitly.

The original v2-era multi-agent design (System A's 5 agents, System B's 10 writing agents) is
**frozen, not current** — see
[`system-a-and-b-agent-design-FROZEN.md`](../../05_thesis_writing/writing_agents/system-a-and-b-agent-design-FROZEN.md).
Two commitments from it remain live: the **≤ 8 GB RAM budget** and the **typed tool/action
interface** (the SRQ2 contribution).

---

## 7. Literature

→ **Canonical:** [`gap_analysis_v4.md`](../../01_thesis_research/literature/gap_analysis_v4.md)
— 58 annotated paper notes; supersedes the 26-paper March 2026 snapshot this file used to embed.

→ Annotations: `01_thesis_research/literature/obisdian_paper_analysis/`
→ References: [`references.md`](../../05_thesis_writing/references.md)
→ RQ version history: [`rq_evolution.md`](../../01_thesis_research/literature/rq_evolution.md)

---

## 8. Quick Reference

| Item | Value |
|---|---|
| Thesis deadline | 15 May 2026 |
| Page limit | 120 standard pages (2 students; 2,275 chars incl. spaces / page) |
| Categories | 4 — CSD, Danskvand, Energidrikke, RTD (Totalbeer excluded, compute grounds) |
| Model families benchmarked | 8 — naive, seasonal-naive, drift, Ridge, ARIMA, Prophet, LightGBM, XGBoost |
| Market scope | `DVH EXCL. HD` (id `1256338`) |
| Grain | brand × month |
| Panel depth | 44 monthly periods (CSD, measured 2026-08-11) *(pending re-run for other categories)* |
| RAM hard limit | 8 GB total |
| MAPE target | ≤ 15% **WMAPE** — met on 3 of 4 categories (14.5–20.9%); RTD is ~32% |
| Calibration target | ≥ 85% empirical coverage of stated 90% prediction intervals |
| SRQ4 design | 5 scenarios × 12 stratified brands × N repeats (1 prompt) |
| Chapters | 10 + abstract + frontpage |
| CBS methodology | Design Science Research (Hevner 2004 + Peffers 2007) |

> Figures marked *(pending re-run)* change once P0036 and P0033 complete: per-category row
> counts, brand counts, and all model metrics.

> **Accuracy figures updated 2026-08-22.** Models are now tuned with expanding-window
> time-series CV over 100 Optuna trials (`04_thesis_results/srq1/cv_metrics.csv`), superseding
> the earlier single-split results in `tuned_metrics.csv`.
>
> **A caveat that applies to every accuracy claim in this thesis:** WMAPE (volume-weighted)
> and median MAPE (per-series) disagree repeatedly — three separate analyses found the same
> split. Median MAPE sits at 29–39% where WMAPE sits at 14–32%. **Always name the metric.**

> **The RAM budget figure is not yet defensible.** `04_thesis_results/generate_figures.py::fig4_ram_budget`
> is entirely hardcoded, including a literal 512 MB "active ML model" against a **measured
> 3–4 MB**. The honest version is stronger: the trained model is the cheap part, and the agent
> runtime is where the budget goes — measurable now that the Prometheus engine runs locally.

> **Thesis title unresolved against `frontpage.md`.** The title above is Brian's choice
> (2026-08-11). `05_thesis_writing/sections-drafts/frontpage.md` is a 2026-03-14 template
> carrying v2-era candidates, and Ch1 states no title. Reconcile against the thesis contract
> and update `frontpage.md` to match.

---

## Related

| Topic | Location |
|---|---|
| Research questions (canonical) | `01_thesis_research/research-questions/` |
| Gap analysis + literature | `01_thesis_research/literature/gap_analysis_v4.md` |
| RQ version history | `01_thesis_research/literature/rq_evolution.md` |
| Architecture (current) | `user-docs/architecture/architecture.md` |
| Frozen agent design | `05_thesis_writing/writing_agents/system-a-and-b-agent-design-FROZEN.md` |
| CBS compliance | `00_thesis_context/formal-requirements/` |
| Thesis outline | `05_thesis_writing/outline.md` |
| Active plans | `plans/PLANS_INDEX.md` |
