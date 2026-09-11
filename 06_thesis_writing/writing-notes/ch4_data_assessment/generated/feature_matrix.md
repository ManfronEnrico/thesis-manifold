<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Composition of the modelling matrix

| | |
|---|---|
| Table | `05_thesis_results/04_data_assessment/tables/04_feature_matrix.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-11 16:38 UTC |

---

Read from csd_feature_matrix_h3.parquet and csd_manifest_h3.json at render time; the feature list is the manifest's own, not a copy. Role assignment is BY RULE (_fm_role) and asserts that no column falls through -- a column added upstream fails the export rather than appearing unclassified. Counts here supersede the 13/14/16-feature figures in earlier drafts (P0048 F3, F10): the current matrix carries 34 features after the holiday enrichment. CSD is shown as the worked category; the other three differ in the promotional block, which is absent at source for the promo-zero categories.
