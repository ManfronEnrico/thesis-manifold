**Holiday-derived features.** Definitions of the three calendar features added to the feature matrix.

| Feature          | Definition                               | Unit   | Source     |
|:-----------------|:-----------------------------------------|:-------|:-----------|
| days_in_month    | Calendar days in the month               | days   | Calendar   |
| n_holidays       | Public holiday-days falling in the month | days   | Nager.Date |
| non_holiday_days | days_in_month minus n_holidays           | days   | Derived    |

*Note.* `non_holiday_days` is named for what it computes and asserts nothing about trading. Danish retail is open at weekends (Lukkeloven liberalised 2012) and many stores open on public holidays with reduced hours, so the column is a proxy for trading exposure, not a measurement of it.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Naming follows the 2026-08-18 holiday_months -> peak_months precedent: a feature name must not assert a cause the computation never established. Earlier drafts of this work used `selling_days` and `trading_days`; both were rejected.

Missing-value rule: a panel month inside the fetched range with no holidays is 0 (a measurement); a month outside it is NaN (unknown), never 0.
