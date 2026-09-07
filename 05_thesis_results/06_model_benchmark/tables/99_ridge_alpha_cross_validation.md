**Ridge regularisation strength by rolling-origin cross-validation.** Alpha selected on development data only, with the previously hard-coded value shown for comparison.

| Category     | Arm     | Alpha selected   | WMAPE at fixed alpha=1 (%)   | WMAPE at selected alpha (%)   | Change (pp)   |
|:-------------|:--------|:-----------------|:-----------------------------|:------------------------------|:--------------|
| CSD          | with    | 1.701            | 22.18                        | 22.20                         | +0.02         |
| CSD          | without | 5.878            | 21.06                        | 21.25                         | +0.20         |
| RTD          | with    | 0.001            | 46.87                        | 47.33                         | +0.46         |
| RTD          | without | 0.001            | 55.64                        | 56.30                         | +0.66         |
| danskvand    | with    | 1.125            | 20.95                        | 20.96                         | +0.01         |
| danskvand    | without | 1.701            | 21.49                        | 21.70                         | +0.22         |
| energidrikke | with    | 0.001            | 19.20                        | 19.10                         | -0.09         |
| energidrikke | without | 0.001            | 20.24                        | 20.31                         | +0.07         |

*Note.* Rolling-origin cross-validation trains each fold on months preceding its validation block, so training data always precedes validation data. Ordinary k-fold cross-validation is not valid for this data, since shuffling would place later months in the training fold.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Mean change from selecting alpha rather than fixing it at 1.0: +0.19pp -- i.e. slightly WORSE on test.

The cross-validation curve is flat: the spread between the best alpha and alpha=1 is 0.00-0.44pp, and widening the search grid to 1e-8 changed test WMAPE by less than 0.01pp. Alpha barely matters on this data.

So the hard-coded value was not a defect. Selecting it is worth doing for method, not for accuracy, and the honest reporting is that the correction is negligible. An earlier draft claimed a 13.7pp error for RTD; that figure came from reading a sweep on the TEST split and was wrong.
