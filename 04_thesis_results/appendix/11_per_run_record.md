**Complete record of individual runs.** Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. Covers 6 of an intended 225 runs (15 brands x 5 repeats x 3 scenarios) and one of the three scenarios; the remaining scenarios have not yet been run at the corrected prompt.

| Category   | Brand     | Scenario         |   Repeat |   Actual (units) |   Forecast (units) |   APE (%) | Outcome   |   Response time (s) |   Tokens in |   Tokens out |   Reasoning tokens | Cost (USD)   |
|:-----------|:----------|:-----------------|---------:|-----------------:|-------------------:|----------:|:----------|--------------------:|------------:|-------------:|-------------------:|:-------------|
| CSD        | HARBOE    | A - no firm data |        0 |        4,778,907 |          3,100,000 |      35.1 | ok        |               105   |       70341 |         3861 |               3421 | $0.4675      |
| CSD        | HARBOE    | A - no firm data |        1 |        4,778,907 |          3,100,000 |      35.1 | ok        |               109.8 |       81059 |         4051 |               3719 | $0.5147      |
| CSD        | HARBOE    | A - no firm data |        2 |        4,778,907 |          3,300,000 |      30.9 | ok        |               111.4 |       76100 |         4535 |               4110 | $0.4998      |
| CSD        | COCA COLA | A - no firm data |        0 |        3,152,932 |          8,200,000 |     160.1 | ok        |               123   |       80138 |         4417 |               3925 | $0.5211      |
| CSD        | COCA COLA | A - no firm data |        1 |        3,152,932 |         10,200,000 |     223.5 | ok        |                95   |       59653 |         3988 |               3524 | $0.4058      |
| CSD        | COCA COLA | A - no firm data |        2 |        3,152,932 |          5,600,000 |      77.6 | ok        |               143.6 |      109664 |         4585 |               4196 | $0.6692      |

*Note.* The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Currently 6 rows because only a scenario-A pilot has run (CSD, 2 brands, 3 reps). Intended full size is 225 rows: 15 brands x 5 repeats x 3 scenarios. Blocked on API credit (P0042 blocks 1-3, ~$40). NOT the final length.
