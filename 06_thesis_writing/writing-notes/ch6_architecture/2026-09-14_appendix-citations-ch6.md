---
name: 2026-09-14_appendix-citations-ch6
description: NOTE - Which generated artefacts Chapter 6 can cite. It owns Figure 2, the only architectural figure the document references, and that figure carries a stale scenario block that must be fixed before anything else is added.
category: workflow
applies-to: [ch6_architecture]
triggers: [ch6 prose pass, figure placement, architecture diagram, appendix references]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - one blocking defect, read R1 first
---

# Chapter 6 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

---

# What this chapter owns

| Artefact | Type | Last regenerated | Status |
|---|---|---|---|
| `ch6_layered_architecture_v2.svg` | figure | 2026-09-10 | **Figure 2** — carries a stale block, see R1 |
| `ch6_tool_interface_v1.svg` | figure | 2026-09-10 | current, uncited |

Chapter 6 owns no tables of its own. Several benchmark tables support its
arguments and are noted below.

---

# R1 — Figure 2 must be regenerated before anything else in this chapter

**This is the blocking item.** `ch6_layered_architecture_v2.svg` is the only
architectural figure the document cites, and its scenario block is typed as:

> Plain agent / Agent + data & code / Agent + models

That is the three-scenario vocabulary **retired on 2026-09-11**. The funded
design has seven scenarios, and §6.7 of this very chapter carries the correct
seven-row table with the correct identifiers.

**So Chapter 6 currently contradicts itself**: §6.2's figure shows three rungs,
§6.7's table shows seven, and they are eleven pages apart.

The rest of the figure is sourced live from `profiling()`, `ladder()` and
`served()`, so only this one block is wrong.

**Fix at the producer**, in `generate_architecture_diagrams.py`,
`fig_layered_architecture()`. The scenario names should come from the `SCENARIOS`
tuple in `srq4_experiment.py:1291` rather than being typed.

**Do not paste any new figure reference into this chapter until this is done.**
Adding a second figure while the first contradicts the text makes the chapter
worse, not better.

---

# R2 — The tool-interface figure should be in text in §6.4

**The artefact.** `ch6_tool_interface_v1.svg` — the request-and-response flow
through the structured forecast tool: decision maker, agentic system, request,
model retrieval, feature construction, prediction, structured response, audit
record. It reads the deployed model set live via `served()`.

**Recommendation: in text, §6.4 The Structured Forecast-Tool Interface.**

**Why.** §6.4 argues the single most load-bearing design decision in the thesis —
that feature construction stays server-side and the language model never handles
a feature vector. That is a claim about a boundary, and a boundary is much easier
to show than to describe.

Chapter 7 covers the same interface in more detail and could also use this
figure. **Put it in Chapter 6** where the architecture is set out, and let
Chapter 7 reference it backwards.

This would become **Figure 3** or later depending on what Chapters 1 to 5 add.

---

# R3 — §6.8 needs the measured memory evidence

**§6.8 Memory, Cost, and Latency Budget** is where the 4 GB envelope argument
lives, and it currently carries the numbers in prose alone.

Three artefacts support it:

| Artefact | What it gives §6.8 |
|---|---|
| `05_model_benchmark/tables/05_substrate_resource_profile.md` | peak fit and inference memory per model |
| `05_model_benchmark/figures/ch5_resource_profile_v2.svg` | the same, against the envelope, as a chart |
| `08_experimental_evaluation/tables/07_sandbox_resource_profile.md` | the footprint measured inside the deployment environment |

**Recommendation: appendix for the two tables, cited from §6.8. The figure goes
in one chapter only** — Chapter 5's note recommends Chapter 5, and §6.8 should
reference it.

**Why the sandbox table matters particularly.** It is the measurement taken
*inside* the real deployment environment rather than on a development machine.
The anticipated-assessor-questions file already records Q1.1 — "your budget is
four gigabytes and your system uses 231 megabytes, was the constraint real" —
and this table is part of that answer.

---

# R4 — The retraining-cost and parameter-drift tables belong to this chapter's argument

**The artefacts.** `06_retraining_cost.md` and `08_parameter_drift.md`.

**Recommendation: appendix, cited from §6.8 or §6.10.**

**Why here rather than Chapter 5.** Both are operational rather than evidential.
They answer "what does it cost to keep this running" — a production-readiness
question, which is Chapter 6's subject and SRQ3's territory, not the model
benchmark's.

Chapter 5's note explicitly declines them for this reason.

---

# R5 — §6.7 should reference the scenario figure, once it is correct

`07_decision_synthesis/figures/ch7_scenarios_v2.svg` is the scenario ladder
figure. **It is currently wrong** — it draws five rungs and its caption states
that D and E were not executed, when both ran nine times.

§6.7 is the section that sets out the ladder, and once the figure is fixed it is
the natural place to show it.

**Sequencing:** fix `fig_scenarios()` → regenerate → then decide whether the
figure sits in §6.7 or in Chapter 7. See the Chapter 7 note, which makes the same
observation from the other side. **One chapter, not both.**

My view: **Chapter 6 §6.7**, because that is where the ladder is introduced and
justified. Chapter 7 discusses what the interface does, not how the comparison is
structured.
