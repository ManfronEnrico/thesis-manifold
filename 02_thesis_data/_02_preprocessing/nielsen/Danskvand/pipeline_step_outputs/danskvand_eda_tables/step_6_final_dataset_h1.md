## Final engineered dataset (Danskvand, horizon 1 month(s))

- The dataset delivered to the modelling stage. Split boundaries are read back from the labelled data rather than recomputed, so they describe what a model is actually trained and evaluated on.
- Feature counts differ across categories by design: Nielsen reports promotional measures for some categories and not others, and a feature that cannot be measured is omitted rather than filled with a placeholder value. Comparisons across categories must account for this difference in available information.

| quantity                   | value              |
|:---------------------------|:-------------------|
| brands                     | 30                 |
| rows                       | 1230               |
| features                   | 23                 |
| promotional data available | False              |
| train period               | 2023-03 .. 2025-07 |
| validation period          | 2025-08 .. 2026-01 |
| test period                | 2026-02 .. 2026-07 |
| evaluable test origins     | 6                  |
