<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Redundancy-based feature reduction, tested and rejected

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/98_feature_redundancy_reduction.md` |
| Producer | `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

The negative result is the contribution. Collinearity is a linear-model pathology: ridge cannot apportion credit between correlated predictors, but a gradient-boosted tree splits on whichever is locally most useful and loses real information when the others are removed.

So the correlated lag features ARE information-adding for the tree models, and this measurement is the evidence. A reduction rule adopted without validation would have degraded every reported number while appearing rigorous.

The 0.95 grouping threshold is a reporting parameter with no cited source -- register item 2. Either justify it by sensitivity analysis or describe it as an arbitrary choice.
