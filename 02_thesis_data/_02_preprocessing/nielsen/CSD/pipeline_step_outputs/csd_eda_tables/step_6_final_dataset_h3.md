## Final engineered dataset (CSD, horizon 3 month(s))

- The dataset delivered to the modelling stage. Split boundaries are read back from the labelled data rather than recomputed, so they describe what a model is actually trained and evaluated on.
- Feature counts differ across categories by design: Nielsen reports promotional measures for some categories and not others, and a feature that cannot be measured is omitted rather than filled with a placeholder value. Comparisons across categories must account for this difference in available information.

| quantity                   | value              |
|:---------------------------|:-------------------|
| brands                     | 95                 |
| rows                       | 4370               |
| features                   | 41                 |
| promotional data available | True               |
| train period               | 2022-10 .. 2025-05 |
| validation period          | 2025-06 .. 2025-12 |
| test period                | 2026-01 .. 2026-07 |
| evaluable test origins     | 5                  |
