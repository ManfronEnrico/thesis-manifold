---
name: 2026-09-14_appendix-citations-ch3
description: NOTE - Which generated artefacts Chapter 3 can cite. It owns the methodology design figure, which is generated from the chapter's own prose and is currently uncited.
category: workflow
applies-to: [ch3_methodology]
triggers: [ch3 prose pass, figure placement, DSR diagram, appendix references]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - blocked on the Ch3 rewrite, read the caveat
---

# Chapter 3 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

> ⚠ **Blocked, and this matters more than the recommendation.** The cross-chapter
> flow note finds Chapter 3 to be one of two weak seams: it *"specifies methods
> the experiment did not use."* §3.5 still names MAPE and RMSE as the accuracy
> metrics and lists five models including Prophet and ARIMA, while Chapter 5
> reports WMAPE and medMAPE and Chapter 8 runs seven scenarios.
>
> **Do not add a figure reference to prose that is being rewritten.** Settle the
> chapter first; this note will still apply afterwards.

---

# What this chapter owns

| Artefact | Type | Last regenerated | Status |
|---|---|---|---|
| `03_methodology/figures/ch3_methodology_design_v1.svg` | figure | 2026-09-10 | current, uncited |

---

# R1 — The methodology figure is generated from this chapter and should be cited by it

**What it is.** The chapter's own section structure, the four sub-question
subjects, and the six DSR activities mapped to the chapters that realise them —
all parsed from the methodology chapter text at render time, grouped into three
phases by a curated grouping in the generator.

**Recommendation: in-text, early, as a numbered figure.**

**Why.** This figure does something no other figure in the thesis does: it shows
how the Design Science Research frame maps onto the document the assessor is
holding. The DSR contribution is assessed, and this is the single clearest
statement that the artefact and the method-level contribution are both delivered.

**Where.** §3.2 Research Design: Design Science Research is the natural home. The
figure restates §3.2's argument in one view.

**The caveat that makes this interesting.** The figure is **parsed from the
chapter prose**. If Chapter 3 is rewritten — which it needs to be — the figure
must be regenerated afterwards, and it carries three guards that will fail loudly
if the rewrite breaks the parse: an unmapped section, a sub-question count other
than four, and a blank DSR activity.

**So the sequence is:** rewrite Chapter 3 → run
`thesis_snapshot.py` → run `generate_methodology_diagram.py` → then add the
figure reference. Doing it in any other order produces a figure of the old
chapter.

---

# R2 — §3.5 should reference the metric dictionary rather than restate metrics

**The artefact.** `05_model_benchmark/tables/01_metric_dictionary.md` defines
every metric used in the thesis, with its formula and the reason it was chosen.

**Recommendation: appendix reference from §3.5 Analytical Approach.**

**Why this solves a real problem.** §3.5 currently names metrics in prose, and it
names the wrong ones. Pointing at a generated dictionary instead of restating
definitions means the methodology chapter cannot drift from the benchmark chapter
again — the dictionary is written by the same run that computes the numbers.

This is the cheapest available fix for part of the Chapter 3 staleness, and it is
structural rather than cosmetic: it removes a place where the same fact is stated
twice.

---

# R3 — Consider referencing the run configuration

**The artefact.** `08_experimental_evaluation/tables/15_run_configuration.md` —
the complete experimental configuration, including the prompt-schema hash.

**Recommendation: appendix reference, optional, from §3.6 Validity and
Reliability.**

Reproducibility is a validity claim. A reader who wants to know whether the study
could be repeated wants the configuration, and §3.6 is where that question is
raised. Chapter 8 also has a claim on this table; if only one chapter cites it,
Chapter 8 is the better home and §3.6 can point forward.
