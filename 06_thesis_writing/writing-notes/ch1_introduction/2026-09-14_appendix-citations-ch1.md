---
name: 2026-09-14_appendix-citations-ch1
description: NOTE - Which generated artefacts Chapter 1 can cite, in text or by appendix reference. Chapter 1 owns Figure 1, the research-questions tree, which is currently declared in the front matter but referenced nowhere in the body.
category: workflow
applies-to: [ch1_introduction]
triggers: [ch1 prose pass, figure placement, appendix references, citing results]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written, awaiting a Ch1 pass
---

# Chapter 1 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**Caveat carried from the cross-chapter flow note:** Chapter 1 is one of the two
weak seams. It "promises a thesis the later chapters no longer deliver." Do not
apply anything here until that is resolved — a figure reference added to prose
that is itself being rewritten is wasted work.

---

# What this chapter owns

| Artefact | Type | Status |
|---|---|---|
| `01_introduction/figures/ch1_research_questions_tree_v2.svg` | figure | **already Figure 1**, current |

That is the whole inventory. Chapter 1 introduces; it should not carry evidence.

---

# R1 — Figure 1 is declared but never referenced

**The situation.** The Table of Figures lists *"Figure 1 - Hierarchical Structure
of Research Questions (SRQ1–SRQ4), p19"*. Section 1.3 Research Questions runs
from line 31 and introduces all four sub-questions in prose. **No sentence in the
chapter refers to the figure.**

A reader meets the four SRQs as prose, then encounters a diagram of the same four
with no sentence connecting them.

**Recommendation: in-text, with a callout.** One clause in §1.3, after the four
sub-questions have been stated, is all it needs. Something of the shape
*"…their hierarchical relationship is shown in Figure 1"*.

**Why in-text and not appendix.** The figure's whole job is to show that the four
sub-questions are layered rather than parallel — the substrate, the interface, the
host system, the evidence. That is a structural claim the introduction makes, and
the figure is the clearest statement of it in the document.

**Provenance note.** This figure is fully typed rather than data-driven, which is
correct: it depicts a conceptual hierarchy, not a measurement. It carries no
count that can go stale.

---

# R2 — Do not cite results artefacts here

Chapter 1 should reference no table. Every candidate belongs to the chapter that
derives it, and forward-referencing a result from the introduction invites a
reader to check a number before the method that produced it has been stated.

The one exception worth considering is the **memory envelope**, if §1.2 or §1.4
states it as a constraint. If it does, the measured figure lives in
`05_model_benchmark/tables/05_substrate_resource_profile.md` and is cited
properly in Chapter 6 §6.8. Chapter 1 should state the constraint and let
Chapter 6 carry the evidence.

---

# Open question for Brian and Enrico

**Does Chapter 1 want the methodology figure too?** `ch3_methodology_design_v1.svg`
depicts the DSR activity-to-chapter mapping, which is partly a "how to read this
thesis" device. §1.5 Thesis Structure currently does that job in prose.

My view: **no.** One structural figure in the introduction is enough, and the
methodology figure earns its place in Chapter 3 where the DSR framing is argued.
Recorded here so it is not re-derived.
