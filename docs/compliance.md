---
name: Compliance & Architectural Decisions
description: CBS thesis guidelines, integrity gates, and open ADRs (template, pipeline, builder agent)
updated: 2026-04-15
---

# Compliance & Architectural Decisions

## CBS Guidelines & Requirements

The CBS thesis guidelines PDF files are in `Thesis/Thesis Guidelines/`.

All thesis work must comply with:
- **Citation format**: APA 7 / CBS standard
- **Chapter and section structure**: As defined in `docs/thesis/outline.md`
- **Methodological requirements**: Documented in `docs/compliance/cbs_guidelines_notes.md`
- **Word count and formatting**: 120-page thesis (group, 2 students)
- **Mandatory declarations**: Plagiarism statement, AI disclosure, research ethics compliance

See `docs/compliance/cbs_guidelines_notes.md` for full CBS requirements extracted from guidelines.

## Integrity Gates

| Gate | When | Checks |
|------|------|--------|
| **Gate 1** (Pre-Draft) | Before prose expansion | Section completeness, page budget (120p), skeleton approved |
| **Gate 2** (Post-Draft) | After first full draft | APA7 citations, figure references, NotebookLM cross-check |
| **Gate 3** (Pre-Submission) | Before final PDF | 7-mode AI failure checklist, CBS compliance, AI disclosure, 49-citation validation |

Gate 3 checklist in `docs/compliance/integrity_checklist.md` (Phase 4, TODO).

## Open Architectural Decisions (ADRs)

All ADRs are open decisions requiring explicit approval before Phase 3 implementation.

### ADR-001: LaTeX Template Strategy

**Status**: OPEN  
**File**: [docs/decisions/ADR-001-template-strategy.md](decisions/ADR-001-template-strategy.md)

**Summary**: Choosing between:
1. Pandoc + custom LaTeX template (control, complexity, maintenance)
2. Existing thesis template (Overleaf, quarto, reproducible-research)
3. Hybrid (Markdown source + templated LaTeX output)

**Decision pending**: User approval on template approach before Phase 3 begins.

### ADR-002: Build Pipeline Strategy

**Status**: OPEN  
**File**: [docs/decisions/ADR-002-build-pipeline.md](decisions/ADR-002-build-pipeline.md)

**Summary**: Designing Markdown → LaTeX → PDF pipeline with reproducibility gates.

**Decision pending**: Approval of pipeline architecture and CI/CD approach.

### ADR-003: Builder Agent Fate

**Status**: OPEN  
**File**: [docs/decisions/ADR-003-builder-agent-fate.md](decisions/ADR-003-builder-agent-fate.md)

**Summary**: Whether to implement System B "Builder Agent" for automated thesis assembly or rely on manual compilation.

**Decision pending**: Approval on automation vs. manual control trade-off.

## Definition of Done

| Task | Completion Criterion |
|---|---|
| Data Assessment | Written report: Nielsen data quality, missing values, forecasting suitability, recommendation on additional data needs |
| Literature Review | Finalised RQs + identified academic gap + novelty documented in `docs/literature/gap_analysis.md` |
| Framework Design | Architecture approved with written brief, agent diagram, justification of choices against 8GB constraint |
| SRQ1 — Model Selection | Benchmark of ≥3 lightweight models with memory profiling, comparative table of accuracy vs memory footprint |
| SRQ2 — Synthesis Module | Working module aggregating outputs from multiple models into a confidence-scored recommendation in natural language |
| SRQ3 — Evaluation | Comparative report: framework vs descriptive baseline on defined metrics (MAPE, decision quality score) |
| Validation Framework | All 3 levels covered: ML accuracy metrics, recommendation quality (LLM-as-judge or human eval), agent behaviour monitoring |
| Thesis Writing | Approved bullet points for every paragraph of every section, before any prose is written |

## Related Documents

- **Guidelines**: [docs/compliance/cbs_guidelines_notes.md](compliance/cbs_guidelines_notes.md)
- **Compliance checks**: [docs/compliance/compliance_checks/](compliance/compliance_checks/)
- **Integrity checklist**: [docs/compliance/integrity_checklist.md](compliance/integrity_checklist.md) (Phase 4, TODO)
- **Decisions**: [docs/decisions/](decisions/) (ADR-001, ADR-002, ADR-003)
