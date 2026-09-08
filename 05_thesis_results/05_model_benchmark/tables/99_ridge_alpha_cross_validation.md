**Ridge regularisation strength by rolling-origin cross-validation.** Alpha selected on development data only, with the previously hard-coded value shown for comparison.

| Category   | Arm     | Alpha selected   | WMAPE at fixed alpha=1 (%)   | WMAPE at selected alpha (%)   | Change (pp)   |
|:-----------|:--------|:-----------------|:-----------------------------|:------------------------------|:--------------|
| CSD        | with    | 0.001            | 35.14                        | 34.97                         | -0.16         |
| CSD        | without | 0.001            | 35.34                        | 35.18                         | -0.17         |

*Note.* Rolling-origin cross-validation trains each fold on months preceding its validation block, so training data always precedes validation data. Ordinary k-fold cross-validation is not valid for this data, since shuffling would place later months in the training fold.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Mean change from selecting alpha rather than fixing it at 1.0: -0.17pp -- i.e. slightly WORSE on test.

The cross-validation curve is flat: the spread between the best alpha and alpha=1 is 0.00-0.44pp, and widening the search grid to 1e-8 changed test WMAPE by less than 0.01pp. Alpha barely matters on this data.

So the hard-coded value was not a defect. Selecting it is worth doing for method, not for accuracy, and the honest reporting is that the correction is negligible. An earlier draft claimed a 13.7pp error for RTD; that figure came from reading a sweep on the TEST split and was wrong.
