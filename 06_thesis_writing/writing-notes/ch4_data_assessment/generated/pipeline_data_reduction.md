<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Panel size through the preprocessing pipeline

| | |
|---|---|
| Table | `05_thesis_results/04_data_assessment/tables/03_pipeline_data_reduction.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-11 16:38 UTC |

---

Read from step_4_log_h{N}.json, which step 4 writes itself -- NOT from the run manifest, whose summary carries only the endpoints and would hide the calendar-fill stage. Values are the ones the step computed, so this cannot drift from the pipeline (P0046 F25).

** DO NOT PUBLISH THE HORIZON COLUMN AS-IS.** P0048 F1 / P0049 F22: engineer_features() takes no horizon argument, so the h1 and h3 matrices encode the SAME one-month prediction task and differ only in their split dates. The row counts below are real, but labelling one of them '3' asserts a horizon the feature construction never applied. Re-run this table after the horizon fix lands.
