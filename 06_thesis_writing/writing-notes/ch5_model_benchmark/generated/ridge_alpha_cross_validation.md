<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Ridge regularisation strength by rolling-origin cross-validation

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/99_ridge_alpha_cross_validation.md` |
| Producer | `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

Covers 2 category-arm cell(s): CSD.

Mean change from selecting alpha rather than fixing it at 1.0: +0.21pp -- i.e. slightly WORSE on test.

The cross-validation curve is flat: the spread between the selected alpha and alpha=1 is 0.21-0.22pp. Alpha barely matters on this data.

So the hard-coded value was not a defect. Selecting it is worth doing for method, not for accuracy, and the honest reporting is that the correction is negligible.
