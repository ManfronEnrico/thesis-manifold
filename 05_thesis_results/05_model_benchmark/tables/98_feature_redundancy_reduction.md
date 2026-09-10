**Redundancy-based feature reduction, tested and rejected.** Correlated feature groups per category and the size of the reduced set they imply.

| Category     | Features available (n)   | Features after reduction (n)   | Clusters found (n)   |
|:-------------|:-------------------------|:-------------------------------|:---------------------|
| CSD          | 18                       | 9                              | 3                    |
| Danskvand    | 17                       | 9                              | 3                    |
| Energidrikke | 18                       | 10                             | 3                    |
| RTD          | 17                       | 10                             | 3                    |

*Note.* Features were grouped where pairwise absolute Spearman correlation was at least 0.95, keeping the member with the highest permutation importance on the validation split. Across 12 category-by-model cells the reduction was fitted against the full set and rejected: it raised mean test WMAPE from 29.31 to 32.13.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

The negative result is the contribution. Collinearity is a linear-model pathology: ridge cannot apportion credit between correlated predictors, but a gradient-boosted tree splits on whichever is locally most useful and loses real information when the others are removed.

So the correlated lag features ARE information-adding for the tree models, and this measurement is the evidence. A reduction rule adopted without validation would have degraded every reported number while appearing rigorous.

The 0.95 grouping threshold is a reporting parameter with no cited source -- register item 2. Either justify it by sensitivity analysis or describe it as an arbitrary choice.
