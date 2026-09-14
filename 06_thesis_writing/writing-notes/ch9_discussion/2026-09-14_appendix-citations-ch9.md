---
name: 2026-09-14_appendix-citations-ch9
description: NOTE - Which generated artefacts Chapter 9 can cite. It owns none, and should reference rather than introduce; the one exception is the residual diagnostics table, which directly supports the limitation §9.1 already states.
category: workflow
applies-to: [ch9_discussion]
triggers: [ch9 prose pass, appendix references, limitations, discussion evidence]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written
---

# Chapter 9 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**Chapter 9 owns no artefacts.** `05_thesis_results/09_discussion/` is empty, and
that is correct — a discussion interprets evidence presented earlier rather than
introducing new evidence.

So the recommendations here are about **referencing backwards**, with one
exception.

---

# R1 — The residual diagnostics table supports a limitation §9.1 already states

**The existing prose.** §9.1 says:

> "…every one of them fitted exponential smoothing and a seasonal ARIMA… Those
> are precisely two techniques the thesis pipeline lacks, since exponential
> smoothing is absent from the benchmark and the pipeline's ARIMA carries no
> seasonal term."

**The artefact.** `05_model_benchmark/tables/residual_diagnostics.md`, written
2026-09-14. Ljung-Box on ARIMA residuals with the degrees-of-freedom correction.
CSD rejects the null for 24 of 95 series, Danskvand for 6 of 29.

**Recommendation: reference it from §9.1, where Chapter 5's appendix entry
carries the table.**

**Why this is worth doing.** §9.1 makes an unusually honest concession — that a
material part of the code-writing scenarios' accuracy is plausibly attributable
to established practice the substrate does not implement. The residual
diagnostics **quantify** that concession: they show the baseline's residuals
still carry structure, which is the measurable form of "no seasonal term".

A conceded limitation with a measurement behind it is much stronger than one
argued in prose. It shows the gap was found by testing rather than noticed in
review.

**Do not duplicate the table here.** Chapter 5's note recommends it as a Chapter 5
appendix entry. Chapter 9 cites that entry.

---

# R2 — §9.4 Limitations should point at the evidence for each limitation it states

Chapter 9 states limitations well. Each one has an artefact behind it, and naming
the artefact converts an assertion into a checkable claim:

| Limitation in §9.4 | Artefact that evidences it | Where it lives |
|---|---|---|
| Narrow experimental scope | `14_per_run_record.md` — 63 runs, 3 brands, 1 category | Ch8 appendix |
| Seed sensitivity | `10_seed_stability.md` | Ch5 |
| Interval coverage below nominal | `calibration.md` | Ch5 body Table 13 |
| Pooled-versus-specialised is a design choice | `pooled_summary.md`, `pooled_perbrand_summary.md` | Ch5 body Table 12 |
| No seasonal ARIMA term | `residual_diagnostics.md` | Ch5 appendix, see R1 |

**Recommendation:** one reference per limitation, pointing at the chapter that
owns it. No new appendix entries.

---

# R3 — Do not introduce figures here

No figure belongs in Chapter 9. The discussion interprets; the figures that
support it are already placed in Chapters 4 through 8, and a reader at Chapter 9
has seen them.

If a point in §9.2 Theoretical contributions needs a diagram, that is a signal the
architecture chapter under-explained it, and the fix belongs there.

---

# R4 — One open question worth recording

**§9.1 rests on a comparison whose figure is currently wrong.** The scenario
ladder figure (`ch7_scenarios_v2.svg`) draws five rungs and states D and E were
not executed. Chapter 9 discusses results from all seven.

Chapter 9 does not cite that figure, so this is not a Chapter 9 defect. But if a
reader reaches §9.1 having seen the figure in Chapter 6 or 7, the discussion will
read as describing an experiment they were told did not happen.

**Recorded here so the dependency is visible.** The fix belongs to the figure
generator; see the Chapter 6 and Chapter 7 notes.
