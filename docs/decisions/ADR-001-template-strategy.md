# ADR-001: CBS Thesis LaTeX Template Strategy

**Status**: OPEN — decision pending
**Date**: 2026-04-13
**Deciders**: Brian + thesis partner

---

## Context

The thesis must be submitted in a format compliant with CBS (Copenhagen Business School) requirements. The final deliverable is a PDF. Current state: thesis sections exist as Markdown files in `docs/thesis/sections/`. No rendering pipeline exists yet.

Two options for the LaTeX template:

1. **CBS Official Overleaf template** — if CBS provides one, extract formatting specs directly
2. **Custom `cbs_thesis.cls`** — create a LaTeX document class from scratch based on CBS guidelines

Key specs to extract from `Thesis/Thesis Guidelines/` PDFs and `docs/compliance/cbs_guidelines_notes.md`:
- Page size (A4 confirmed)
- Font family and size
- Margin widths
- Line spacing
- Header/footer format
- Page numbering style
- Title page / frontpage requirements
- Chapter heading style
- Citation format (APA7 per CBS guidelines)

---

## Decision Options

### Option A: CBS Overleaf Template (if available)
- **Pro**: Officially compliant; no guesswork
- **Con**: May not be freely available; Overleaf dependency; may need adaptation for Pandoc

### Option B: Custom cbs_thesis.cls based on guidelines
- **Pro**: Full control; works with local Pandoc pipeline; no Overleaf dependency
- **Con**: Risk of formatting errors; more upfront work

### Option C: Hybrid — Overleaf for final submission, Pandoc for drafts
- **Pro**: Best of both worlds for supervisor review workflow
- **Con**: Two pipelines to maintain; formatting drift risk

---

## Decision

[PENDING — complete this section after extracting CBS specs from Thesis Guidelines PDFs]

**Chosen option**: [A / B / C]
**Rationale**: [why]

---

## Consequences

[Complete after decision]

---

## References

- `docs/compliance/cbs_guidelines_notes.md` — extracted CBS requirements
- `Thesis/Thesis Guidelines/` — source PDF guidelines (gitignored)
- ADR-002 (build pipeline) depends on this decision
