<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Cost of retraining a model on request

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/06_retraining_cost.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-11 16:38 UTC |

---

Do NOT claim re-tuning is less accurate. Optuna seed alone moves test WMAPE by more than the gap between the two strategies (F21), and the accuracy figures sit inside the seed-variance band. The case for refit-not-retune is elapsed time alone: re-tuning multiplies one fit by trials and folds (F28), while peak memory stays a small fraction of budget in every row above. The time and memory numbers are in the table -- do not restate them here.
