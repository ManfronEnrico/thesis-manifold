<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Effect of holding hyperparameters fixed as data accrues

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/08_parameter_drift.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-11 16:38 UTC |

---

INCONCLUSIVE -- do not fit or cite a per-month drift slope. The origins fall on both sides of zero, the window is a handful of months, and some origins are exactly zero because re-tuning rediscovered the frozen parameters. Recommend refit-per-query + SCHEDULED re-tune, cadence not optimised. F31. The per-origin differences are in the table; the mean is in the note.

Kept SEPARATE from the merged resource table: unit is pp of forecast error across origins, not time/memory.
