---
name: 2026-09-14_appendix-citations-ch8
description: NOTE - Which generated artefacts Chapter 8 can cite. All five of its tables regenerated against the funded run and its prose numbers reconcile exactly; the work here is giving them numbers and fixing one generated note that stops at scenario C.
category: workflow
applies-to: [ch8_experiment]
triggers: [ch8 prose pass, appendix references, scenario tables, per-run record, funded run]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written
---

# Chapter 8 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**This chapter's evidence is in the best state of any in the thesis.** All five
tables regenerated on 2026-09-13 against the funded run, and the chapter's own
numbers reconcile against them exactly — 502.2, 662.1, 26.7, 69.5 and the rest
all check out. Nothing here is stale.

The work is **reach**, not repair.

---

# What this chapter owns

| Artefact | Last regenerated | Status |
|---|---|---|
| `11_scenario_comparison.md` | 2026-09-13 | indexed, **note stops at C** |
| `12_outcome_taxonomy.md` | 2026-09-13 | indexed, uncited |
| `14_per_run_record.md` | 2026-09-13 | indexed, uncited |
| `15_run_configuration.md` | 2026-09-13 | indexed, uncited |
| `07_sandbox_resource_profile.md` | 2026-09-11 | indexed, claimed by Ch6 §6.8 |

Plus the raw evidence base: 65 raw response files and `runs.csv`, 69 rows of
which 63 are the funded `v6-shared-composition+af04a42a478b` set and 6 are
retired `v2` rows.

---

# R1 — The per-run record is the single most defensible appendix in the thesis

**The artefact.** Every run logged individually: category, brand, scenario,
repeat, actual, forecast, APE, outcome class, response time, tokens in and out,
reasoning tokens, cost.

**Recommendation: appendix, cited from §8.3 Results.**

**Why this is the strongest candidate anywhere.** Chapter 8's headline numbers
are aggregates over nine runs per scenario. An assessor who doubts an aggregate
wants the rows. This table is that, completely, and it is the thing that makes
the experiment auditable rather than merely reported.

It is also what makes the repository-driven claim concrete: the appendix says
"here is every run", the repository holds the raw responses behind them, and the
two agree.

**One sentence in §8.3 does it.** Something of the shape *"The complete record of
all 63 runs is given in Appendix [N]."*

---

# R2 — The outcome taxonomy should be in text, not appendix

**The artefact.** Counts and percentages by outcome class per scenario — usable
answer, execution error, no forecast, timed out, implausible value.

**Recommendation: in text, §8.3.**

**Why.** The design decision that outcomes are **classified rather than averaged**
is a methodological commitment the thesis makes repeatedly, and this table is the
only place it is visible. Scenario A returns 6 usable answers of 9 with 3
implausible values; every other scenario returns 9 of 9. That failure rate says
more about production readiness than the accuracy gap does, which is precisely
the argument the chapter makes.

Five rows by seven columns. Small enough for the body.

---

# R3 — The scenario comparison table needs its note fixed before it is cited

**The artefact.** Eleven measures across all seven scenarios. The chapter's
numbers already come from it.

**Recommendation: in text — it likely already is — but fix the generated note
first.**

**The defect.** `export_appendix.py:980` types:

> "The scenarios form an information ladder: A has no access to firm data, B may
> execute code against it, and C additionally calls the dedicated forecasting
> model."

Seven columns of data under a sentence explaining three. D, E, F and G appear and
go unexplained.

**FIXED 2026-09-14.** The note is now built from the scenarios actually present
in the run log, with a guard that raises if a scenario appears in the data and
has no description — so the table cannot silently explain a subset again.

**Related correction.** The sibling defect in `13_interval_communication.md`
(two naming systems in one header) was **not** caused by `export_appendix.py` as
this note first reported. It came from a relabel map in
`score_interval_communication.py:113`, one stage upstream. See the Chapter 7 note.

---

# R4 — The run configuration is the reproducibility appendix

**The artefact.** Complete experimental configuration including the prompt-schema
hash `v6-shared-composition+af04a42a478b`.

**Recommendation: appendix, cited from §8.2 Experimental Design.**

**Why.** §8.2 already makes a strong claim about prompt control:

> "an automated check renders all seven and asserts that paired scenarios are
> byte-identical wherever they should be… its identity is recorded as a hash, so
> that no prompt can be altered without the recorded run identity changing with
> it."

That claim is verifiable only if the reader can see the hash. The configuration
table carries it.

**Chapter 3 §3.6 also has a claim on this table.** Chapter 8 is the better owner;
§3.6 can point forward.

---

# R5 — §8.2's prompt promise already has its appendix

> "The full prompt set is given in the appendix and its identity is recorded as a
> hash."

**Appendix A2 already exists** and carries the prompts with the schema id.
**This promise is kept** — it needs the number, not new content.

**One check before applying.** A2's text names the set as
`v4-five scenarios+e37111d3daaa`. The funded run used
`v6-shared-composition+af04a42a478b`. **A2 documents a superseded prompt set.**

That is a real defect and it belongs in this chapter's next pass. The appendix
must carry the prompts the funded runs actually used, or the hash argument
collapses.

---

# R6 — The sandbox resource profile: let Chapter 6 own it

`07_sandbox_resource_profile.md` measures the footprint inside the deployment
environment. §8.4 Operating cost of the substrate could use it, and so could
Chapter 6 §6.8.

**Recommendation: Chapter 6 owns it**, because it is evidence for the
production-readiness argument rather than an experimental result. §8.4 references
it.

---

# Summary of what I would apply

| # | Artefact | Placement | Confidence |
|---|---|---|---|
| R1 | per-run record | appendix | **highest in the thesis** |
| R2 | outcome taxonomy | in text §8.3 | high |
| R3 | scenario comparison | fix note, then in text | high |
| R4 | run configuration | appendix, §8.2 | high |
| R5 | A2 prompt set | **fix — documents a superseded schema** | high |
| R6 | sandbox profile | Ch6 owns, §8.4 references | medium |
