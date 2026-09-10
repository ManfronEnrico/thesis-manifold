<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Holiday enrichment: test WMAPE with and without

| | |
|---|---|
| Table | `05_thesis_results/05_model_benchmark/tables/94_holiday_ablation_tuned.md` |
| Producer | `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

Do NOT quote the mean of this column. It averages over model families that respond differently, and that difference is itself the finding: Ridge benefits in 1 of 1 categories while the tree models benefit in 5 of 8 cells.

RTD XGBoost is the least stable cell in the study (it swings 2.95pp between the untuned and tuned runs, table 95).
