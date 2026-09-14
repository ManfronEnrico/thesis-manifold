---
name: 2026-09-14_appendix-citations-ch7
description: NOTE - Which generated artefacts Chapter 7 can cite. It already makes three unnumbered appendix promises in prose, and owns the interval-communication table plus the stale scenario figure.
category: workflow
applies-to: [ch7_synthesis]
triggers: [ch7 prose pass, appendix references, interval communication, traceability, figure placement]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - three existing promises need numbers
---

# Chapter 7 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**Chapter 7 is the chapter that already promises appendices.** Three sentences
say "in the appendix" without a number. Those promises are the highest-value work
here, because an unnumbered promise is a promise an assessor cannot follow.

---

# What this chapter owns

| Artefact | Type | Last regenerated | Status |
|---|---|---|---|
| `07_decision_synthesis/tables/13_interval_communication.md` | table | 2026-09-13 | indexed, **two naming systems in its header** |
| `07_decision_synthesis/figures/ch7_scenarios_v2.svg` | figure | 2026-09-10 | **wrong — see R4** |

---

# R1 — Three existing promises, three specific artefacts

## §7.2 The contract

> "…its fields fall into four groups, summarised in Table 17 and listed in full
> in the appendix."

**What fulfils it.** The full response schema from `forecast_tool.py`. There is
no generated table for this today.

**Recommendation:** either generate one — a small exporter reading the response
model's fields, types and descriptions — or reword the promise to point at the
tool module. My view is **generate it**: a typed interface that documents itself
is exactly the SRQ2 contribution, and a hand-copied field list would go stale.

**This is the one gap in the whole audit where the artefact does not yet exist.**

## §7.3 Preserving reliability

> "The full set, together with the capability note that distinguishes each
> scenario, is given in the appendix."

**What fulfils it.** Appendix A2 already exists in the document and carries the
prompts with the schema hash. **This promise is already kept** — it just needs
the number.

## §7.5 Preserving traceability

> "…the check that the agent queried the correct series is reported in the
> appendix, while the check that the payload arrived complete is recorded on
> every call and reported nowhere."

**What fulfils it.** `08_experimental_evaluation/tables/14_per_run_record.md`
carries the per-run trace. The traceability table the exporter would have written
was skipped — the export log says *"skip traceability: no dedicated-model tool
calls logged yet."*

**Recommendation:** check whether that table now generates against the funded
run. If it does, it fulfils the promise directly. If it does not, the sentence
should point at the per-run record instead.

**Note the honesty already in that sentence** — it concedes that half the
capability is unmeasured. Keep that. It is the kind of concession that earns
trust, and the anticipated-assessor-questions file treats unmeasured claims as
the more useful half of the document.

---

# R2 — The interval-communication table is this chapter's best evidence, and it has a defect

**The artefact.** `13_interval_communication.md`, regenerated 2026-09-13 against
the funded set. Four criteria for conveying uncertainty, scored per scenario
against what the tool actually returned.

**Recommendation: in text, in §7.4 Preserving uncertainty.**

**Why in text.** It carries the cleanest result in the thesis. Every scenario
states a range; only the two with tool access state a range that **matches** the
model's output — 9 of 9 for C and E, 0 of 9 for everyone else. That is the SRQ2
contribution in a single row, and burying it in an appendix wastes it.

**The defect to fix first — FIXED 2026-09-14.** Its column headers mixed two
naming systems: `A - no firm data`, `B - code execution`, `C - dedicated model`,
then `D_prometheus_data`, `E_prometheus_model`, `F_llm_data_model`,
`G_prometheus_data_model`.

**The cause was not where I first reported it.** An earlier draft of this note
blamed `export_appendix.py:902`. That is wrong — `HDR` there is an empty dict and
every use is `HDR.get(s, s)`, which falls through to the raw identifier, so the
exporter rendered faithfully what it was handed.

The real source was a three-entry relabel map at
`score_interval_communication.py:113`, which rewrote A, B and C into descriptive
glosses **when writing the CSV** and left D through G untouched. Removed
2026-09-14; the scenario identifier is now written through unchanged.

**Re-run `score_interval_communication.py` before pasting**, since the fix is in
the file that produces the CSV, not in the exporter that reads it.

---

# R3 — The scenario-comparison table supports §7.4 but belongs to Chapter 8

`11_scenario_comparison.md` carries replicability at 100% for the two
tool-mediated scenarios and 0% elsewhere, which is a §7.4 argument.

**Recommendation: let Chapter 8 own the table; Chapter 7 quotes the one row it
needs.** Duplicating an eleven-row table across two chapters invites them to
disagree.

---

# R4 — The scenario figure is wrong, and Chapter 6 should probably own it

`ch7_scenarios_v2.svg` draws five rungs and its caption says D and E are
*"specified but not executed here, since the engine is proprietary."* Both ran
nine times each in the funded set.

It is the only one of the twelve architecture diagrams that reads no data at all.

**Fix:** `fig_scenarios()` should read the `SCENARIOS` tuple from
`srq4_experiment.py:1291`.

**Placement:** the Chapter 6 note recommends §6.7, where the ladder is introduced
and justified. I agree — Chapter 7 describes what the interface does, not how the
comparison is structured. **Recorded in both notes so the decision is made once.**

---

# Summary of what I would apply

| # | Item | Action | Confidence |
|---|---|---|---|
| R1a | §7.2 schema promise | **generate the artefact** | high — the only missing one |
| R1b | §7.3 prompt promise | add the number, A2 exists | high |
| R1c | §7.5 traceability promise | check, then point | medium |
| R2 | interval communication | fix producer, then **in text §7.4** | high |
| R3 | scenario comparison | quote one row, Ch8 owns it | medium |
| R4 | scenario figure | fix, then Ch6 §6.7 owns it | high |
