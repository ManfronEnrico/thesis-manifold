<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Computational cost of the forecasting substrate

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/05_substrate_resource_profile.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-11 16:38 UTC |

---

tracemalloc materially understates the native-library models: the serialised model size is the independent witness that RSS, not the Python-heap figure, is what a deployment must provision (P0044 F1-F2). Keep both rows so the correction stays auditable, but RSS is the headline. All three figures are in the table -- do not restate them here.

MERGED from three tables (profile + budget share + retraining) per Brian 2026-09-03: same unit system, same subject, so the comparison belongs in one screenshot. Drift stays separate -- its unit is pp of error, not time or memory.
