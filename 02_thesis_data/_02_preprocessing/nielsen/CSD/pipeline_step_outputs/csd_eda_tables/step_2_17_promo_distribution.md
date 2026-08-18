## Promo Intensity Distribution Summary

- Promo intensity = promo_units / max(sales_units, 1). The clip avoids zero-division without the +1 bias that would inflate the ratio for low-volume brands.
- promo_units is a subset of sales_units in Nielsen's model, so an intensity above 1 is a delivery defect: 1 such row(s) here, reported and left uncorrected (F42).
- The boxplot compares the target's level between promoted and unpromoted brand-months. A visible shift motivates promo features; overlapping boxes argue they add little.
- Descriptive, not causal: promotions are placed on brands already expected to sell, so this gap is confounded by selection and cannot be read as promotional uplift.
- Complements 3.13, which ranks brands by intensity; this section characterises the distribution's shape.

| metric                        |      value |
|:------------------------------|-----------:|
| mean intensity                |     0.3007 |
| median intensity              |     0.2567 |
| skewness                      |     0.3986 |
| rows with promo               |  2972.0000 |
| rows without promo            |  1237.0000 |
| median sales_units (promo)    | 10443.2606 |
| median sales_units (no promo) |    36.4786 |
| rows with intensity > 1       |     1.0000 |
