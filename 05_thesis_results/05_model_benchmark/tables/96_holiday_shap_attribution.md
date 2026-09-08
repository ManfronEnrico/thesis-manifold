**SHAP attribution of calendar features, before and after enrichment.** Mean absolute SHAP value as a percentage of total attribution (LightGBM, test split).

| Category     | Feature          | Attribution without (%)   | Attribution with (%)   | Change (pp)   |
|:-------------|:-----------------|:--------------------------|:-----------------------|:--------------|
| CSD          | days_in_month    |                           | 0.35                   |               |
| CSD          | month            | 2.17                      | 1.69                   | -0.48         |
| CSD          | n_holidays       |                           | 0.89                   |               |
| CSD          | non_holiday_days |                           | 1.13                   |               |
| CSD          | peak_month       | 1.41                      | 1.38                   | -0.04         |
| CSD          | quarter          | 0.16                      | 0.07                   | -0.08         |
| RTD          | days_in_month    |                           | 0.44                   |               |
| RTD          | month            | 2.22                      | 1.78                   | -0.44         |
| RTD          | n_holidays       |                           | 0.77                   |               |
| RTD          | non_holiday_days |                           | 1.10                   |               |
| RTD          | peak_month       | 2.58                      | 1.96                   | -0.62         |
| RTD          | quarter          | 0.11                      | 0.17                   | +0.06         |
| danskvand    | days_in_month    |                           | 0.24                   |               |
| danskvand    | month            | 1.06                      | 0.90                   | -0.16         |
| danskvand    | n_holidays       |                           | 0.49                   |               |
| danskvand    | non_holiday_days |                           | 0.48                   |               |
| danskvand    | peak_month       | 3.70                      | 3.57                   | -0.14         |
| danskvand    | quarter          | 0.07                      | 0.11                   | +0.04         |
| energidrikke | days_in_month    |                           | 0.57                   |               |
| energidrikke | month            | 1.47                      | 2.01                   | +0.55         |
| energidrikke | n_holidays       |                           | 0.79                   |               |
| energidrikke | non_holiday_days |                           | 0.52                   |               |
| energidrikke | peak_month       | 0.54                      | 0.69                   | +0.15         |
| energidrikke | quarter          | 0.51                      | 0.17                   | -0.34         |

*Note.* An empty 'without' cell marks a feature absent from that arm. If the holiday features merely re-encoded month-of-year, their attribution would be offset by an equal fall in month and peak_month. The existing calendar features lose substantially less than the holiday features gain, so the calendar carries information those features do not.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

This is the empirical half of the anti-collinearity argument; appendix table 92 is the structural half. Cite both when the enrichment is challenged as month re-encoded.

Note the tension worth stating plainly in the text: the features earn attribution in every category, yet improve accuracy in only some. Attribution is not accuracy.
