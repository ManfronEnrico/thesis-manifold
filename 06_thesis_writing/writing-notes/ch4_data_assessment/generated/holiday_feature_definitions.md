<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Holiday-derived features

| | |
|---|---|
| Table | `05_thesis_results/04_data_assessment/tables/93_holiday_feature_definitions.md` |
| Producer | `01_SRQ1_Model_Training/01_thesis_data/_00_raw/holidays/export_holiday_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

Naming follows the 2026-08-18 holiday_months -> peak_months precedent: a feature name must not assert a cause the computation never established. Earlier drafts of this work used `selling_days` and `trading_days`; both were rejected.

Missing-value rule: a panel month inside the fetched range with no holidays is 0 (a measurement); a month outside it is NaN (unknown), never 0.
