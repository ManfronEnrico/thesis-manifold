# ADR-002: Thesis Build Pipeline (Markdown → PDF)

**Status**: OPEN — decision pending
**Date**: 2026-04-13
**Deciders**: Brian + thesis partner
**Depends on**: ADR-001 (template strategy)

---

## Context

Thesis sections are written as Markdown files in `docs/thesis/sections/`. The final deliverable must be a PDF. A build pipeline is needed to convert Markdown → LaTeX → PDF.

Two primary approaches:

1. **Local Pandoc pipeline** — Concatenate sections → Pandoc → LaTeX (using `cbs_thesis.cls`) → `pdflatex` → PDF
2. **Overleaf** — Upload Markdown or LaTeX to Overleaf; use web-based LaTeX compiler

---

## Decision Options

### Option A: Local Pandoc Pipeline
Components:
- `pandoc/thesis.yaml` — metadata (author, title, supervisor, institution, date)
- `pandoc/thesis_build.sh` — concatenation + pandoc invocation
- `Makefile` — `make pdf`, `make check`, `make figures` targets
- `build/` — gitignored output directory for generated PDFs

**Pro**: Fully local; reproducible; no internet dependency; integrates with `make check` integrity gates
**Con**: Requires `pandoc` + `pdflatex` (texlive) to be installed; more setup

### Option B: Overleaf
**Pro**: No local LaTeX install required; easy supervisor review via share link
**Con**: Manual upload step; not integrated with local `make` workflow; less reproducible

### Option C: Hybrid — Local Pandoc for drafts, Overleaf for final + supervisor review
- Generate PDF locally during writing
- Upload final LaTeX output to Overleaf for supervisor review and final submission

**Pro**: Best of both; supervisor gets live Overleaf link for comments
**Con**: Two-step process; must keep Overleaf in sync

---

## Decision

[PENDING — complete after ADR-001 and confirmation of Overleaf preference]

**Chosen option**: [A / B / C]
**Rationale**: [why]

---

## Consequences

[Complete after decision]

**If Option A or C:** Create these files in Phase 3:
- `pandoc/thesis.yaml`
- `pandoc/thesis_build.sh`
- `Makefile` with `make pdf` / `make check` / `make figures`
- `build/.gitkeep`
- `templates/cbs_thesis.cls`

---

## References

- ADR-001 (template strategy) — must be resolved first
- `docs/compliance/cbs_guidelines_notes.md` — formatting requirements
- Master plan Phase 3: "Core Pipeline Build"
