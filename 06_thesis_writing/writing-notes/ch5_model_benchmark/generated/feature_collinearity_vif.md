<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Variance inflation factors by feature and category

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/97_feature_collinearity_vif.md` |
| Producer | `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

12 exact dependencies across all categories.

NO THRESHOLD IS ASSERTED IN THE CAPTION, deliberately. The conventional 5 and 10 cut-offs were attributed in an earlier draft to a source not held in the project library; the attribution was removed. See writing-notes/unverified-claims-to-check.md item 1 before putting any numeric threshold in prose.

StandardScaler plus Ridge's L2 penalty absorbs the rank deficiency, so the exact dependency does not move the error materially -- but that is a mechanism argument, not a number measured here. Report the collinearity; do not claim it explains accuracy, and do not cite a pp figure for its removal unless a script computes one.
