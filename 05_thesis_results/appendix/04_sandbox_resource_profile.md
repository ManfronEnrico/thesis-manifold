**Resource footprint measured inside the deployment environment.** Memory required to fit each model within the production sandbox, measured in the deployment environment itself rather than on a development machine. The container reports a memory limit of 4,122 MB and provides 1 processor core; the interpreter and its libraries occupy 156.4 MB, or 3.79% of that limit, before any model is fitted. The lowest value in each row is shown in bold italic.

| Measure                      | Ridge       |   LightGBM |   XGBoost |
|:-----------------------------|:------------|-----------:|----------:|
| Fit time (s)                 | ***0.524*** |      2.092 |     1.426 |
| Peak fit memory, RSS (MB)    | ***1.4***   |     28.2   |     6.5   |
| Share of container limit (%) | ***0.03***  |      0.68  |     0.16  |

*Note.* The limit is read from the container at run time, and so corroborates the provisioned budget independently of the deployment configuration. Absolute figures are lower than those measured on the development machine because the container provides a single processor core, so the tree-based learners allocate fewer parallel working buffers. That the interpreter and its libraries occupy more memory than any model fit is the expected profile for lightweight models, and confirms that the constraint operates on the choice of model class rather than on the footprint of the models finally selected.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

MEASURED 2026-09-03, template `prometheus`. Container limit 4122 MB independently corroborates 4 GB -- cite ALONGSIDE local profiling, not instead. cpus=1 explains lower-than-local RSS; state the reason or it reads as a contradiction. Closes N6.
