<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Composition of the modelling matrix - part 1 of 6

| | |
|---|---|
| Table | `05_thesis_results/04_data_assessment/tables/08_feature_matrix_p1.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-15 12:23 UTC |

---

Read from csd_feature_matrix_h3.parquet and csd_manifest_h3.json at render time; the feature list is the manifest's own, not a copy. Role assignment is BY RULE (_fm_role) and asserts that no column falls through -- a column added upstream fails the export rather than appearing unclassified.
