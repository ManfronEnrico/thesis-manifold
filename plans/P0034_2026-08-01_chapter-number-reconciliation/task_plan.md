---
pid: P0034
created: 2026-08-01 00:00:00
updated: 2026-08-19 10:20:00
status: paused
paused_reason: "Deliberately parked by Brian 2026-08-19 until the EDA, model-training and serving pipelines are locked. Chapter numbers cannot be reconciled while the numbers they cite are still moving -- and they moved again on 2026-08-18/19 (H=3 repoint, weighted_dist drop, metric changes)."
focus_detail: "Inventory every hard-coded metric in the chapter drafts that the S01 retrain will invalidate; drop Totalbeer from prose with a documented compute-constraint justification. Prepare-only — no prose lands without Enrico approval."
---

# P0034 — Chapter Number Reconciliation + Totalbeer Removal

> **Independent plan.** The inventory work (phase 1) needs nothing from P0032/P0033 and
> can run today. Phase 3 (applying new numbers) consumes P0032's re-run output.
> This is the harness's T19, scoped down to what Brian can do without Enrico.

## Two distinct workstreams

### A — Numbers that the retrain will invalidate

The V3 leakage fix (P0032) plus the S01 retrain will shift CSD and energidrikke metrics.
Multiple chapters hard-code the current figures. This answers Enrico's handover question
#2 ("does the leakage fix collide with anything that hard-codes old numbers?") — which was
previously unanswered.

### B — Totalbeer removal (4 categories final)

Brian confirmed 2026-08-01: **4 categories final, excluding Totalbeer.** Ch3/Ch4 prose
still says five (beer included).

**Justification to record** (Brian's reason, must appear in the prose, not just a silent
deletion): Totalbeer was excluded on **compute constraints** — the dataset is
significantly larger than any other category (~10M rows). This is a defensible
methodological scoping decision and should be stated as such, likely in Ch3 (scope) with
a pointer from Ch4 and a line in Ch10 limitations.

## Inventory — hard-coded metrics found (grep, 2026-08-01)

**Highest-risk file: `ch6-model-benchmark.md`** — three separate tables repeat the same figures.

| File | Lines | What is hard-coded |
|------|-------|--------------------|
| `sections-drafts/ch6-model-benchmark.md` | 119–122 | Headline WMAPE table: CSD 16.5/20.8/39.9, danskvand 23.8/**22.0**/37.7, energidrikke 11.4/13.9/31.9, RTD 31.0/38.8/58.8 |
| `ch6-model-benchmark.md` | 126 | "Optuna tuning improved WMAPE by roughly 2–4 pp" |
| `ch6-model-benchmark.md` | 137 | "energidrikke reaches **11.4% WMAPE**, near the ≤15% target" |
| `ch6-model-benchmark.md` | 146–147 | ARIMA WMAPE: CSD 24.2, danskvand 33.4, energidrikke 15.7, RTD 48.2 |
| `ch6-model-benchmark.md` | 153–156 | ML-vs-traditional table incl. deltas "+7.7 pp", "+4.3 pp", "+17.2 pp" |
| `ch6-model-benchmark.md` | 161 | Prophet danskvand 16.9% |
| `ch6-model-benchmark.md` | 170–173 | Model sizes (Ridge 1.5, LGB 18.7, XGB 0.2 MB); latency (~1.7 s train, ~16 ms predict, LGB ~7.7 s) |
| `ch6-model-benchmark.md` | 176–178 | Calibration coverage: CSD 90.5%, RTD 88.0%, danskvand 85.8%, energidrikke 81.0% |
| `ch6-model-benchmark.md` | 201–206 | Final selection table (repeats 16.5 / 22.0 / 11.4 / 31.0) |
| `sections-drafts/ch8-evaluation.md` | 45–49 | Repeats all four WMAPE + all four ARIMA + Prophet 16.9% |
| `sections-drafts/ch9-discussion.md` | 17–19 | Repeats 16.5 / 22.0 / 11.4 / 31.0 |
| `ch9-discussion.md` | 67 | Repeats deltas 7.7 / 4.3 / 17.2 pp |
| `sections-drafts/ch10-conclusion.md` | 21 | Range claim "test WMAPE 11.4–31.0%" |

### Severity triage

- **Will change (V3 affects CSD + energidrikke):** every CSD and energidrikke figure above,
  plus the derived deltas (+7.7 pp, +4.3 pp) and the 11.4–31.0% range in Ch10.
- **Should NOT change (promo-zero):** danskvand and RTD figures — but they must be
  *re-verified*, not assumed, since S01 retrains from scratch.
- **At risk from DEC-GRAIN, independent of leakage:** Ch6 lines 119–122 and 201–206 present
  a **brand×chain** column, and danskvand's selected configuration is brand×chain (22.0%).
  DEC-GRAIN drops the chain grain from active results. **This is a structural rewrite of
  those tables, not a number swap** — flag prominently for Enrico.
- **Probably stable:** model sizes and latency (lines 170–173) — but promo feature count
  changes could shift them marginally.

## Approval gate (house rule)

Per `harness/thesis_tasks.json` T19 and the project's bullets-before-prose rule:
**no prose lands without Enrico's approval.** This plan produces *diffs and bullets*.
Applying them is a separate, gated step.

## Phases

| Phase | Goal | Tasks | Depends on |
|-------|------|-------|------------|
| 1 | Complete the inventory + severity triage | 1, 2 | nothing — run today |
| 2 | Draft Totalbeer removal + justification | 3, 4 | nothing |
| 2b | Verify the ≤15% target claim | 8 | nothing — run today |
| 3 | Swap in new numbers | 5, 6 | **gate task 9**, P0032, P0035 |
| 4 | Package for Enrico approval | 7 | phases 1–3 |

## Prose gate (Brian, 2026-08-01)

**No prose or bullets are finalised until the data is streamlined.** Tasks 1–5 and 8
(inventory, triage, Totalbeer draft, structural rewrite, citation check) are *preparation*
and proceed now. Tasks 6–7 (number swap, approval package) wait for P0032 (leakage),
P0033 (all four categories) and P0035 (grain removal) to land. Task 9 records this gate.

## The ≤15% "industry target" — flagged as possibly unsourced

Brian flagged this as likely AI slop. What the grep found:

- `ch6-model-benchmark.md:92` — *"Target MAPE: ≤15% (industry benchmark for retail demand forecasting — cite ML-Based FMCG 2024)"*
- Repeated as fact at `ch6:137`, `ch8:46`, `ch9:18`, `ch10:21`

The cited source is the Springer LNCS / INFUS 2024 chapter *"Machine Learning-Based Demand
Forecasting for an FMCG Retailer"* (`references.md:46-47`). The citation note is still in
draft form ("cite X"), i.e. **it was never verified** — the number propagated into four
chapters on repetition alone.

Task 8 checks whether the paper states any such benchmark. If not, cut it or replace with a
sourced threshold. This matters beyond tidiness: it is the yardstick the thesis's strongest
claim (energidrikke 11.4%) is measured against, and P0032's leakage fix may push
energidrikke past 15% — inverting a sentence that may not have a source in the first place.

## Definition of done

- Every hard-coded metric in the drafts is inventoried with file:line and triaged.
- The chain-grain structural problem in Ch6 is written up as an explicit flag.
- Totalbeer removal drafted with the compute-constraint justification.
- All output is diffs/bullets, ready for approval — nothing applied unilaterally.

## Related

- `harness/thesis_tasks.json` — T19 (`ready`, walled `enrico`)
- P0032 — produces the corrected numbers
- Enrico handover §5 Q2 (leakage vs hard-coded numbers) and Q3 (4 vs 5 categories)

---

## Paused 2026-08-19 — by design, not by blocker

Brian's call: chapter reconciliation waits until EDA, model training and serving are
locked.

That is the right sequencing, and this session proves why. Every headline number this
plan would reconcile **changed again** on 2026-08-18/19:

| Change | Effect on chapter numbers |
|--------|---------------------------|
| Repoint to H=3 matrices | 95 brands, not 58; split 70/15/15, not 57/14/29 |
| `weighted_dist` dropped from models | CSD WMAPE 17.5% -> 17.1%; RTD medMAPE 41.9% -> 28.6% |
| Prophet installed + medMAPE headline | statistical baseline table replaced outright |
| `mean MAPE` dropped | a reported column removed |

Reconciling prose against numbers that move weekly wastes the scarcest resource left.

**Resume when**: SRQ4 has run (P0037) and the SRQ1 results are final. At that point
every figure the chapters cite is fixed, and reconciliation is a single pass rather
than a repeated one.

**Note for whoever resumes**: its task 3 lists P0032 and P0035 as gates. Both were
closed on 2026-08-19 — P0032 cancelled as superseded, P0035 complete — so that
dependency is discharged.
