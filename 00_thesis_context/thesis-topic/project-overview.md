# Project Overview — Manifold AI Thesis

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
| G2 | No head-to-head benchmark of ARIMA / Prophet / LightGBM / XGBoost / Ridge under an explicit RAM budget in retail FMCG |
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
  code, runnable locally in an E2B sandbox (no Prometheus dependency)
- **SRQ4 metrics** — correctness / consistency / replicability (primary) + cost / latency
  (secondary), ≈50 prompts, judge model with a human-rated subset. Ch8 reports a **pilot**;
  the full run is stated as further work
- **SRQ3** — an integration-readiness *assessment*, not a completed integration (Prometheus
  Graph Engine access pending NDA + dev merge)

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

> **Two open reconciliations with Ch1 §1.4:** Ch1 currently states *five* categories
> (including Totalbeer) and 37–42 periods. Totalbeer was excluded on compute grounds
> (Brian, 2026-08-01 — see P0034), and CSD measures **44** periods at parent market scope
> (measured 2026-08-11 — see P0036 findings F5). Ch1 needs updating on both counts.

→ Pipeline and structure: [`02_thesis_data/`](../../02_thesis_data/)
→ Sample-size rationale, adequacy per SRQ, and tool-call mechanics:
[`sample-size-and-tool-interface-rationale.md`](../../05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md)

---

## 6. System Architecture

→ **Current:** [`user-docs/architecture/architecture.md`](../../user-docs/architecture/architecture.md)
→ Forecast service: `03_thesis_modelling/model_serving/system_a_forecast/`
→ Conversational system: `03_thesis_modelling/model_serving/system_b_conversational/`

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
| Market scope | `DVH EXCL. HD` (id `1256338`) |
| Grain | brand × month |
| Panel depth | 44 monthly periods (CSD, measured 2026-08-11) *(pending re-run for other categories)* |
| RAM hard limit | 8 GB total |
| MAPE target | ≤ 15% |
| Calibration target | ≥ 85% empirical coverage of stated 90% prediction intervals |
| SRQ4 prompt set | ≈ 50 |
| Chapters | 10 + abstract + frontpage |
| CBS methodology | Design Science Research (Hevner 2004 + Peffers 2007) |

> Figures marked *(pending re-run)* change once P0036 and P0033 complete: per-category row
> counts, brand counts, and all model metrics.

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
