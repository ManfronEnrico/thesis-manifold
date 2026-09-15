**Metric dictionary - part 3 of 5.** Rows 11 to 15 of 22. Definition, unit, direction of improvement and source field for every quantity reported in this appendix.

| Dimension   | Metric                      | Unit   | Definition                                                                                                                                              | Better when   | Source                          |
|:------------|:----------------------------|:-------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------|:--------------------------------|
| Cost        | Tokens per answer           | tokens | Input plus output tokens for one run.                                                                                                                   | lower         | runs.csv: tokens                |
| Cost        | Reasoning tokens            | tokens | Tokens the model spends on internal reasoning. Billed at the output rate but absent from the visible answer, so they are reported separately.           | lower         | runs.csv: tokens_reasoning      |
| Cost        | Cost per answer (estimated) | USD    | Token counts at published rates. Excludes the code-execution container charge, which the API does not report per call.                                  | lower         | runs.csv: cost_usd_est          |
| Cost        | Cost billed (actual)        | USD    | Billed total from the provider's organisation-costs endpoint over the run window, including container charges. This is the figure reported in the text. | lower         | summary.md: cost reconciliation |
| Latency     | Response time               | s      | Wall-clock seconds per run, including tool round-trips.                                                                                                 | lower         | runs.csv: latency_s             |

*Note.* Percentage-valued metrics are given as numbers with the unit in the column heading (for example a weighted MAPE of 19.4 denotes 19.4%), following the convention of the M4 and M5 forecasting competitions.
