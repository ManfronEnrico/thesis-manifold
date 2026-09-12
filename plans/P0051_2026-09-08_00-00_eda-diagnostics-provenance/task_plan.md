---
pid: P0051
created: 2026-09-08 00:00:00
updated: 2026-09-08 00:00:00
status: pending
focus_detail: "READ THIS BEFORE P0055 — it is the evidentiary base that plan builds on, not a subset of it (an earlier 2026-09-12 edit wrongly marked it folded; that is retracted). F2 is the strongest fact in the area: 27 of 79 brands test as ALREADY STATIONARY in raw form, so the blanket d=1 OVER-DIFFERENCES them. F7 re-verified live 2026-09-12 at step_2_eda_descriptive.py:543-553 — p_diff is computed and never used in the decision rule. NOT STARTED. Two EDA diagnostics (per-feature skewness, per-brand ADF) are computed and reported but never consumed by the pipeline. The modelling is defensible; the Ch4 prose implies an evidentiary link that does not exist. Read findings.md F1-F2 first, then the Ch4 anchors in F5."
---

# P0051 — EDA diagnostics: computed, reported, never consumed

> **NOT superseded. Read this BEFORE P0055.** An edit earlier on 2026-09-12 marked
> this plan as folded into P0055; **that is retracted.** A closer reading found this
> plan is the better-evidenced statement of the defect — seven findings with line
> numbers, verified by exhaustive grep across three pipeline generations. P0055
> inherits these findings as its evidentiary base and adds the forecasting-literature
> layer on top. Work the repairs from P0055 Phase 2.A; the evidence is here.

> Split out of the P0050 figures/tables session on 2026-09-08 at Brian's request,
> so it can be worked with its own context. **Nothing here has been executed.**

## Objective

Two diagnostics in the category EDA produce per-brand / per-feature
recommendations that **no code reads**. Decide, per diagnostic, whether to:

- **(a)** leave the pipeline as-is and correct the thesis prose to describe what
  actually happens (recommended — see F3), or
- **(b)** wire the recommendation into the pipeline, or
- **(c)** stop computing it.

This is primarily a **writing and honesty** task, not a modelling fix.

## The finding in one line

The per-brand ADF `recommendation` column and the per-feature skewness
interpretation are **decorative with respect to the pipeline**. A single global
`log1p` is applied to every brand from a hardcoded constant, and ARIMA uses a
hardcoded `d=1`.

## Why this is not (mainly) a modelling defect

Per-brand transform selection on n=46 monthly series would be **worse** than what
is done now: ADF has low power at that length (the artefact's own header says
so), selection would be fitting noise, and per-brand transforms make feature
semantics inconsistent across the panel. The pipeline's own console note says
*"apply log1p universally for stability."*

**The decision was deliberate and is defensible. The prose is what misstates it.**

## Phases

| # | Phase | Scope | Status |
|---|-------|-------|--------|
| 1 | Confirm findings still hold | re-run greps after any pipeline change | pending |
| 2 | Ch4 prose corrections | Table 2 basis row, §4.2.2 blanket claim, RTD contradiction | pending |
| 3 | Fix the false code comment | `pipeline_config.py:218` states the opposite of the truth | pending |
| 4 | Decide the ARIMA `d=1` framing | fixed spec vs ADF-selected — prose or code | pending |
| 5 | Optional: fix or retire the `p_diff` defect | recommendation ignores its own diff test | pending |

## Sequencing

- **Phase 2 depends on P0048 phase 3** (the horizon re-run) only where it cites
  *numbers*. The structural claims (what drives the transform) are stable and can
  be written now.
- **Phase 3 is a one-line code change** and is independent of everything else.
- Phases 4 and 5 are judgement calls, not blockers.

## Related

- `.claude/rules/prose-insertion-discipline.md` — anchored blocks, `writing-notes/`
- `.claude/rules/writing-surface-authority.md` — the `.docx` is authoritative
- P0048 — owns the Ch4 prose pass; coordinate so the same paragraph is not
  rewritten twice
- P0050 — owns the EDA figures/tables these diagnostics produce
