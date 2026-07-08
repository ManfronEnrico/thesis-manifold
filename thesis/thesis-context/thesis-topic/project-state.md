---
name: Project State & Frozen Decisions
description: Deliberate choices, open questions, known constraints, and TODOs for the thesis
updated: 2026-04-15
---

# Project State & Known Constraints

## Frozen Decisions (Do Not Modify Without Explicit Approval)

- **Measurement model**: DSR (Design Science Research) methodology confirmed — do not suggest alternatives
- **RAM constraint**: 8GB hard limit on all System A models — no exceptions, no suggestions to "just use more RAM"
- **Writing Agent**: produces ONLY bullet points — never full prose. Prose requires human sign-off
- **Phase transitions**: every phase requires explicit human approval before proceeding
- **RQs v4**: canonical version, synced 2026-06-17 to ch1-introduction.md §1.3. Manifold-aligned reframe ADOPTED (17/06): Main RQ gains "cost-justified"; **SRQ4 baseline = code-as-action LLM** (not non-agentic template); metrics = correctness/consistency/replicability (primary) + cost/latency (secondary); code-as-action is now the central SRQ4 comparator, not future work. SRQ1/SRQ2/SRQ3 unchanged; SRQ3 stays readiness assessment (Prometheus access pending), Graph Engine = integration target. Ch1 + figure done; Ch2/Ch3/Ch10 propagation pending. Ch1 is editing surface; research-questions.md mirrors it. Do not modify without flagging a phase transition.
- **System A vs System B**: these are separate systems. Never modify System A logic from System B agents
- **ADR-001/002/003**: open decisions — do not implement Phase 3 before these are resolved
- **SRQ1 baseline models**: XGBoost 45.5% median MAPE (test), LightGBM 46.7% median MAPE (test) — see `docs/tasks/srq1_verification_report.md` for validation metrics and test/val discrepancy analysis
- **No em dashes in prose**: rewrite using commas, semicolons, colons, or subordinate clauses (hyphens in compound adjectives permitted)

## Critical Constraints

- **Hard deadline**: 15 May 2026 — 120-page thesis (group, 2 students)
- **Hard memory limit**: ≤ 8 GB RAM. Every architectural decision must be justified against this constraint
- **Data security**: Nielsen dataset must not leave the local environment (Indeks Danmark dropped from scope 2026-06-19)
- **No package installs without logging**: install freely but always document in `docs/context.md`

## Open Questions & Uncertainty

- **Methodology framework PENDING** — Saunders et al. (2023) "research onion" schematised and mapped to Ch3 in [saunders-research-onion-framework.md](../methodology/saunders-research-onion-framework.md). To DECIDE (multi-method quantitative vs mixed methods) then APPLY when we write/finalise Ch3. Not yet applied to prose.
- RQs still evolving — Literature Review Agent has an explicit mandate to propose refinements
- Novelty to be finalised — gap analysis in progress
- ~~Indeks Danmark integration for SRQ3~~ **DROPPED 2026-06-19** — Indeks / consumer-survey enrichment removed entirely from all chapters; thesis uses one data source (Nielsen). SRQ3 = integration readiness only.
- Manifold AI feedback on framework design pending
- Plan file location rules not yet finalized

## Risk Flags

- 🔴 **High complexity**: 7-agent architecture, multi-indicator synthesis module, 3-level validation framework
- 🔴 **Tight timeline**: 15 May — ~1 month remaining for SRQ2–4 implementation + thesis writing
- 🟡 **High uncertainty**: RQs still evolving, novelty to be finalised, Indeks Danmark integration for SRQ3 not yet implemented
- 🟡 **External dependency**: Manifold AI feedback on framework design pending
- 🔒 **Security critical**: Nielsen dataset must not leave the local environment; Indeks Danmark contains survey weights
- 💥 **Context overflow risk**: Literature Review Agent over many papers, Thesis Writing Agent over 120 pages — use `/compact` aggressively

## TODO

- [ ] Phase 5 Synthesis Module (SRQ2) — can begin (Phase 4 benchmark complete)
- [ ] Phase 6 Evaluation (SRQ3/SRQ4) — requires Phase 5 complete
- [ ] Indeks Danmark integration as external consumer signal (SRQ3)
- [ ] NotebookLM Phase 1: create 6 chapter notebooks, populate with 16+ confirmed papers
- [ ] NotebookLM verification of 25 Ch.2 citations (pending)
- [ ] CBS compliance checks on chapter skeletons
- [ ] Chapter prose review (Ch.1–3 written, pending review)
- [ ] DSR supervisor confirmation (OI-03) — required for Ch.3 compliance sign-off
