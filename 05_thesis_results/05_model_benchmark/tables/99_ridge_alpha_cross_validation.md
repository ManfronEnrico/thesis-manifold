**Ridge regularisation strength by rolling-origin cross-validation.** Alpha selected on development data only, with the previously hard-coded value shown for comparison.

| Category   | Arm     | Alpha selected   | WMAPE at fixed alpha=1 (%)   | WMAPE at selected alpha (%)   | Change (pp)   |
|:-----------|:--------|:-----------------|:-----------------------------|:------------------------------|:--------------|
| CSD        | with    | 0.06236          | 20.34                        | 20.56                         | +0.22         |
| CSD        | without | 0.09427          | 20.34                        | 20.55                         | +0.21         |

*Note.* Rolling-origin cross-validation trains each fold on months preceding its validation block, so training data always precedes validation data. Ordinary k-fold cross-validation is not valid for this data, since shuffling would place later months in the training fold.
