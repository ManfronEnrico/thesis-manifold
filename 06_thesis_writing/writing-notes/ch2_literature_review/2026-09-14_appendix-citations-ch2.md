---
name: 2026-09-14_appendix-citations-ch2
description: NOTE - Which generated artefacts Chapter 2 can cite. It owns the literature-design map table and the gap diagram, and currently references neither.
category: workflow
applies-to: [ch2_literature_review]
triggers: [ch2 prose pass, figure placement, appendix references, literature table]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written
---

# Chapter 2 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

Chapter 2 reads well and was cleared by the cross-chapter flow note as part of
the continuous run of Chapters 2 and 4 to 8. These are additions, not repairs.

---

# What this chapter owns

| Artefact | Type | Last regenerated | Status |
|---|---|---|---|
| `02_literature_review/tables/89_literature_design_map.md` | table | 2026-09-10 | current, **unindexed and uncited** |
| `02_literature_review/figures/ch2_gap_diagram_v2.svg` | figure | 2026-09-10 | current, uncited |

---

# R1 — The literature-to-design map is the strongest unused artefact in the chapter

**What it is.** A generated table mapping each of the chapter's sections to the
research question it informs and the design consequence it produces. Section 2.5
maps to SRQ2 and SRQ4, section 2.6 to SRQ3, section 2.8 to all four, and so on.

**Recommendation: appendix, cited from §2.7.**

**Why.** §2.7 is the research-gap section — the point where the chapter stops
surveying and starts arguing that the gap is real. A reader who wants to check
that the literature review actually earns its conclusions wants exactly this
table, and that reader is an assessor.

But it is eight rows of cross-reference machinery. In the body it interrupts the
argument; in the appendix it is available to the reader who asks the question.

**Suggested reference.** One sentence at the close of §2.7, of the shape
*"The mapping from each strand to the design decision it informs is given in
Appendix [N]."*

**Note on the producer.** `generate_literature_table.py` reads section numbers
and titles from the chapter itself, so a section renumber updates the table.
Re-run it after any Chapter 2 restructure.

---

# R2 — The gap diagram should be in-text

**What it is.** Four literature strands drawn as overlapping regions with the
research gap at their intersection, and the memory envelope interpolated from
`RAM_BUDGET_MB`.

**Recommendation: in-text in §2.7, as a numbered figure.**

**Why.** The gap argument is the chapter's conclusion and the thesis's
justification. It is currently made in prose alone. A diagram that shows four
literatures failing to overlap at one point is a stronger statement of "this is
unaddressed" than a paragraph, and it is the kind of figure an examiner
remembers.

This would become **Figure 3** under the current numbering, or Figure 2 if the
architectural overview moves.

**Provenance caveat.** This figure is fully typed apart from the RAM envelope.
That is legitimate — the four strands are an editorial grouping, not a
measurement — but it means the strand names must be kept in step by hand if the
chapter's section titles change.

---

# R3 — Nothing else from the results tree belongs here

Chapter 2 surveys literature. No benchmark table, EDA plot or experimental result
should be cited before the methodology has been stated.

---

# Renumbering warning

Adding a figure to Chapter 2 renumbers every later figure. The document currently
declares only two figures, so the cost is small **now** and grows with each one
added. If several of these recommendations are accepted across chapters, insert
them in document order in one pass rather than one at a time.

Word's caption fields renumber automatically; plain-text callouts in prose do
not. Check both.
