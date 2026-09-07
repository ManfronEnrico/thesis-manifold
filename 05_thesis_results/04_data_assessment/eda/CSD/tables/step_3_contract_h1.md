## Feature-engineering parameters (CSD, horizon 1 month(s))

- Parameters governing feature construction and the temporal split. Values are measured from the category's own data where the quantity is measurable, and recorded with their basis where they reflect a modelling decision.
- The minimum series length follows from the feature specification: a brand-month observation is usable only once its lag features are defined, giving warm-up plus horizon plus one. Brands shorter than this cannot be represented under the specification and are excluded on that basis.
- Split boundaries are proportional to the observed period rather than fixed dates, which holds the ratio constant as the panel grows and keeps categories with different start dates comparable.
- Test origins report how many forecasts can be evaluated: an origin counts only when its target month falls within the test window.

| parameter                  | value               |
|:---------------------------|:--------------------|
| forecast_horizon           | 1                   |
| min_periods                | 15                  |
| warmup_periods             | 13                  |
| lags                       | [1, 2, 3, 4, 8, 13] |
| rolling_windows            | [4, 13]             |
| peak_months                | [3, 6, 9, 12]       |
| log_transform_target       | True                |
| train_end                  | (2025, 5)           |
| val_end                    | (2025, 12)          |
| n_test_origins             | 7                   |
| training_row_retention_pct | 100.0               |
