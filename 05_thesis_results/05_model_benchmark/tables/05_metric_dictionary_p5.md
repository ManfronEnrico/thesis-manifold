**Metric dictionary - part 5 of 5.** Rows 21 to 22 of 22. Definition, unit, direction of improvement and source field for every quantity reported in this appendix.

| Dimension   | Metric       | Unit   | Definition                                                                                                        | Better when   | Source                   |
|:------------|:-------------|:-------|:------------------------------------------------------------------------------------------------------------------|:--------------|:-------------------------|
| Efficiency  | Refit time   | s      | Wall-clock seconds to re-estimate model coefficients on updated data while holding stored hyperparameters fixed.  | lower         | srq1/refit_vs_retune.csv |
| Efficiency  | Re-tune time | s      | Wall-clock seconds to re-run the full hyperparameter search, which repeats a cross-validated fit for every trial. | lower         | srq1/refit_vs_retune.csv |

*Note.* Percentage-valued metrics are given as numbers with the unit in the column heading (for example a weighted MAPE of 19.4 denotes 19.4%), following the convention of the M4 and M5 forecasting competitions.
