<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Effect of hyperparameter tuning on the ablation

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/95_holiday_ablation_tuning_sensitivity.md` |
| Producer | `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

This table is why the fixed-configuration ablation was not reported. Danskvand's trees were mis-specified by ~12pp, and that category flips from harmful to helpful once the model can fit. An ablation is only interpretable against a properly specified model.

Methodological point worth a sentence in the text: the direction of a feature effect can invert under tuning.
