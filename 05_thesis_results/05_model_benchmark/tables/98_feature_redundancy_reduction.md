**Redundancy-based feature reduction, tested and rejected.** Correlated feature groups per category and the size of the reduced set they imply.

| Category     | Features available (n)   | Features after reduction (n)   | Clusters found (n)   |
|:-------------|:-------------------------|:-------------------------------|:---------------------|
| CSD          | 18                       | 9                              | 3                    |
| Danskvand    | 17                       | 9                              | 3                    |
| Energidrikke | 18                       | 10                             | 3                    |
| RTD          | 17                       | 10                             | 3                    |

*Note.* Features were grouped where pairwise absolute Spearman correlation was at least 0.95, keeping the member with the highest permutation importance on the validation split. Across 12 category-by-model cells the reduction was fitted against the full set and rejected: it raised mean test WMAPE from 29.31 to 32.13.
