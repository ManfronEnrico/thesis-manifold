<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Abstract

> **P0044 OPEN (2026-09-01): RAM figure needs reconciling.** This file states an
> 8 GB budget. That number is a project assumption, not a sourced one -- Ng (2017)
> argues memory is the binding design variable, not that SMEs get 8 GB. Manifold's
> production Prometheus E2B template is provisioned at a **measured 4096 MB**
> (`fxe7gzkqjupdhbx4uvpr`, verified live 2026-09-01). Prefer the measured figure.
> All results hold under the tighter bound (serving 36.8 MB, refit ~37 MB).
> See `plans/P0044_2026-09-01_17-10_resource-measurement-and-retrain-arms/findings.md` F22-F23.

> CBS requirement: max 1 standard page (≤2,275 characters including spaces)
> Counts toward total page limit AND character count
> Must appear BEFORE Chapter 1
> Language: English (confirm programme language with supervisor)
> Status: BULLET SKELETON — requires empirical results to complete
> Last updated: 2026-03-15

---

## Purpose

---

## Bullet skeleton (to be converted to prose after empirical results available)

### Problem
- Business Intelligence systems in SME retail contexts operate primarily at a descriptive analytics level, producing retrospective reports rather than forward-looking recommendations
- Transitioning to predictive decision-support requires ML forecasting infrastructure that is typically resource-intensive and economically inaccessible at enterprise cloud scale for SME AI providers
- Gap: no validated framework exists for resource-constrained (≤8GB RAM) multi-agent AI decision-support integrating heterogeneous data signals in a retail CPG context

### Method
- Design Science Research (Hevner et al., 2004; Peffers et al., 2007): design, implementation, and evaluation of a multi-agent AI framework
- Artefact: a multi-agent system (LangGraph orchestration + 5 lightweight ML models + LLM synthesis via Claude API) deployed on Danish CSD retail data (Nielsen CSD panel + Indeks Danmark consumer survey)
- 3-level evaluation framework: ML accuracy (Level 1), recommendation quality / LLM-as-Judge (Level 2), RAM and latency profiling (Level 3)

### Key findings (TBD — fill after empirical results)
- SRQ1: [Best model family, MAPE achieved, RAM within/near 8GB constraint]
- SRQ2: [Calibration coverage, LLM-as-Judge score, vs. baseline]
- SRQ3: [MAPE improvement from consumer signal enrichment — X%]
- SRQ4: [AI system vs. descriptive BI — on which dimensions and by how much]

### Contribution
- Validated proof-of-concept for AI-augmented demand forecasting within ≤8GB RAM
- 5 generalised design principles for resource-constrained multi-agent AI deployment
- Memory profiling methodology for multi-component AI pipelines (replicable protocol)
- Demonstrated feasibility of LLM synthesis layer for calibrated, contextualised demand recommendations

### Scope note
- Single empirical context: Danish CSD retail, Manifold AI / Nielsen CSD panel, Indeks Danmark consumer survey
- Findings are indicative for the SME AI decision-support domain; generalisation requires further validation

---

## Character count target
- Maximum: 2,275 characters including spaces
- Equivalent to approximately 350–380 words
- When writing prose: use Word → Review → Word Count → Characters (with spaces) to verify

---

## Outstanding
- [ ] Fill SRQ1–SRQ4 findings once empirical results are available (Phase 4–6)
- [ ] Confirm language of abstract with supervisor (English if English programme)
- [ ] Final character count check before submission
