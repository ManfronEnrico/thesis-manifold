---
name: project-overview
description: REFERENCE - What this thesis is about and why. Navigation only; every number, path and result lives elsewhere.
category: reference
applies-to: [thesis]
triggers: [what is this thesis about, project scope, onboarding, thesis topic]
created: 2026_09_10-16_50
updated: 2026_09_10-16_50
---

# Project Overview — Manifold AI Thesis

> *Extending Production Agentic Decision-Support with Lightweight Forecasting for FMCG Retail*
> CBS Master's Thesis · Business Administration & Data Science · Deadline 15 May 2026

---

## What this file is, and is not

This states **the problem, the questions and the reasoning**. It is the answer to
"what is this thesis about?" for someone who has never seen the repository.

**It deliberately contains no results, no measurements, no file paths and no
status.** Every one of those has a home that is kept current by something other
than a person remembering to edit this page, and a copy here would be a second
version that silently disagrees with the first.

| If you want | Read |
|---|---|
| the research questions, verbatim | `THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR` |
| any number, table or figure | `THESIS_RESULTS_DIR`, by chapter |
| the thesis prose itself | the OneDrive `.docx`, mirrored read-only under `THESIS_WRITING_SNAPSHOTS_DIR` |
| where anything lives on disk | `PATHS.py` |
| what is decided, open or blocked | `plans/PLANS_INDEX.md` and the registers in `THESIS_WRITING_DIR / "writing-notes"` |
| CBS formal requirements | `THESIS_CONTEXT_REQUIREMENTS_DIR` |

Path names above are `PATHS.py` constants, not directories to type. The
repository has been reorganised four times; every literal path written into a
document broke silently, which is why this file names constants instead.

---

## 1. The problem

**Manifold AI** builds "AI Colleagues": production-deployed conversational
assistants embedded in the business-intelligence workflows of Danish retailers
and consumer-goods manufacturers.

The system operates at a **descriptive** level. It retrieves and explains what
has already happened, and it does that well. It cannot forecast demand, qualify a
recommendation with a confidence bound, or tell a user how much to trust what it
just said.

**This is a capability gap in a live product, not a prototype.** That framing
does most of the work in this thesis. It means the deployed system is the
empirical anchor and is to be **extended rather than replaced**, which rules out
the greenfield architecture most of the literature assumes and imposes the
constraints a running product actually has.

Three coupled problems follow, and the coupling is the point — solving any one
alone leaves the capability unusable:

1. **A predictive substrate.** Forecasting models light enough to run inside a
   realistic small-business cloud budget, and accurate enough on fast-moving
   consumer-goods demand to be worth consulting.
2. **A reliable interface.** A structured tool interface that carries a forecast
   to the agent layer with its uncertainty, its provenance and its confidence
   intact, rather than as a bare number the agent may present as certain.
3. **Integration readiness.** The architectural and operational conditions under
   which an existing agentic system can absorb forecast-informed decision-support
   without being redesigned around it.

### The constraint that shapes everything

Small and medium-sized deployments budget memory in **single-digit gigabytes**,
not tens. That one fact rules out deep sequence models and rules out using a
large language model as the forecaster itself, and it is why the thesis is about
*lightweight* forecasting rather than *best-available* forecasting.

**The exact budget figure lives in the results tables**, which report every
model's memory as a measured share of it. Do not restate it here; it is a
deployment parameter, and it has already moved once.

---

## 2. The research gap

The individual pieces are not novel. **The intersection is**, and the argument
rests on five gaps that have not been addressed together:

| # | Gap |
|---|---|
| G1 | No framework for extending an *existing production* agentic system with forecasting under an explicit memory budget |
| G2 | No head-to-head benchmark of the lightweight model families against parameter-free baselines under a stated memory budget, on retail fast-moving consumer goods |
| G3 | No structured tool-interface design for exposing machine-learning forecasts, with uncertainty and traceability, to language-model agents |
| G4 | Integration-readiness criteria for agentic systems adopting predictive capability have not been empirically derived or validated |
| G5 | No replicable memory-profiling methodology for pipelines combining forecasting with language-model synthesis |

The literature that comes closest works on **industrial process control** rather
than retail, and assumes a system built for the purpose. This thesis is the
retail transposition of that architecture, under an explicit resource budget and
with a production-extension framing.

Which papers those are, and how each gap maps onto the corpus, belongs to the
literature review and its notes — not here, because the corpus grows and a list
copied into this file would be wrong within a fortnight.

---

## 3. Research questions

**Canonical text lives in `THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR`**, mirroring
the introduction chapter, with one scope file per sub-question.

Not restated here, deliberately. The introduction is the editing surface, and a
copy in this file would drift from it. What follows is only the shape of the
argument, so a reader knows why there are four sub-questions and not three.

The main question asks **how a production agentic system without predictive
capability can be extended with lightweight forecasting** so that its
decision-support becomes reliable, forecast-informed and cost-justified under
deployment constraints.

The four sub-questions decompose that into one question per layer of the
extension, which is also the order in which they have to be answered:

| | Layer | Asks |
|---|---|---|
| **SRQ1** | the substrate | which lightweight models trade accuracy against memory and category specialisation best |
| **SRQ2** | the interface | how a forecast reaches the agent with reliability, uncertainty and traceability preserved |
| **SRQ3** | the host system | what a production agentic system must already be able to do before forecasting can be attached |
| **SRQ4** | the evidence | whether dedicated models actually beat an agent that writes its own forecasting code, at justified cost |

SRQ4's comparator is a language model given the firm's data and the ability to
write, run and correct its own analysis code. The comparison is therefore
between two ways of obtaining a forecast, not between a forecasting system and
an absence of one.

---

## 4. Methodology

**Design Science Research** (Hevner et al., 2004; Peffers et al., 2007), with
Saunders, Lewis and Thornhill as the research-design scaffold. Philosophy:
pragmatism.

Design Science is the right frame because the thesis produces **an artefact and a
claim about artefacts of its kind**, and both are assessed:

- an **instantiation** — a working extension of a production agentic system,
  which is the thing that either runs or does not
- a **method-level contribution** — integration-readiness criteria and interface
  design principles intended to hold beyond this one retail context

The second is what makes it a thesis rather than a consulting deliverable, and
it is why SRQ3 and SRQ2 are framed as *criteria* and *principles* rather than as
descriptions of what was built.

Detail lives in `THESIS_CONTEXT_METHODOLOGY_DIR`.

---

## 5. Data

**A commercial retail-measurement panel of Danish grocery**, at a single market
scope, with the modelling grain fixed at **brand by month**.

Three properties of it drive design decisions throughout, and each is a stated
limitation as much as a feature:

- **Monthly, not daily.** Annual seasonality is estimated from a small number of
  cycles, and weekly effects do not exist. This is what puts the more elaborate
  seasonal methods outside their design regime.
- **Panel, not census.** Brands enter and leave, and series lengths differ, so
  any model must tolerate short and interrupted histories rather than assume a
  rectangle.
- **Several categories, deliberately unlike each other.** They differ in
  volatility, in seasonality and in whether promotional measurement exists at
  all. That heterogeneity is what makes the category-specialisation question in
  SRQ1 answerable rather than rhetorical.

**Which categories, how many periods and how many brands: read the data-assessment
chapter's tables.** Those counts change when the pipeline re-runs, and they are
generated from the data each time.

Two further sources support the other questions: **the production agentic system
itself**, as the reference case for integration readiness, and **a code-writing
language-model baseline** in a sandbox, as SRQ4's comparator.

Pipeline structure: `THESIS_DATA_DIR`. Access terms are governed by the data
provider's licence and the non-disclosure agreement, which is why no raw data is
committed to this repository.

---

## 6. What is being built

Three artefacts, one per layer, each addressing one sub-question:

| Artefact | Where the code lives | Answers |
|---|---|---|
| Trained forecasting models and their benchmark | `SRQ1_DIR` | SRQ1 |
| The typed forecast tool interface | `SRQ2_DIR` | SRQ2 |
| The scenario experiment comparing capability levels | `SRQ4_DIR` | SRQ4 |

SRQ3 produces criteria rather than code, and is argued from the integration
work the other three make possible.

**The design commitment worth knowing** is that feature construction stays
server-side. The language model never handles a feature vector; it calls a tool
and receives a forecast, an interval, a confidence signal and the provenance
needed to trace it. That single decision is most of SRQ2's contribution, and it
is what makes the forecast auditable rather than merely available.

Current architecture: `user-docs/architecture/architecture.md`.

---

## 7. Scope boundaries

Stated because each was a real decision, and each gets re-litigated otherwise:

- **Extension, not replacement.** The host system's architecture is a given. A
  recommendation requiring it to be rebuilt is out of scope by construction.
- **Lightweight, not best-available.** Deep sequence models and language models
  as direct forecasters are excluded by the memory budget, not by preference.
  Saying so is part of the contribution.
- **One grain.** Brand by month. Finer grains were evaluated during development
  and are reported as limitation and future work.
- **Assessment where a deployment is not possible.** Where the thesis cannot
  ship something into production, it derives criteria from a working integration
  rather than claiming a deployment it did not do.
- **Pilot where a full run is not affordable.** Where an experiment's full
  version exceeds the budget or the calendar, the thesis reports a pilot and says
  so, rather than reporting a partial run as complete.

---

## Related

| Topic | Location |
|---|---|
| Research questions and per-SRQ scope | `THESIS_CONTEXT_RESEARCH_QUESTIONS_DIR` |
| Methodology | `THESIS_CONTEXT_METHODOLOGY_DIR` |
| CBS formal requirements | `THESIS_CONTEXT_REQUIREMENTS_DIR` |
| Results, by chapter | `THESIS_RESULTS_DIR` |
| Thesis prose (authoritative) | the OneDrive `.docx` |
| Read-only prose mirror | `THESIS_WRITING_SNAPSHOTS_DIR` |
| Writing notes and registers | `THESIS_WRITING_DIR / "writing-notes"` |
| Architecture | `user-docs/architecture/architecture.md` |
| Every path constant | `PATHS.py` |
| Plans and decisions | `plans/PLANS_INDEX.md` |
