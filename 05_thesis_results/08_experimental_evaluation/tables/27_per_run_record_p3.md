**Complete record of individual runs - part 3 of 6.** Rows 23 to 33 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |    Actual |   Forecast |   APE (%) | Outcome   |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|----------:|-----------:|----------:|:----------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | HARBOE  | C          |     1 | 6,365,900 |  4,969,050 |      21.9 | ok        |       10.8 |     1034 |       129 | 0           | $0.0090      |
| CSD        | HARBOE  | C          |     2 | 6,365,900 |  4,969,050 |      21.9 | ok        |        4.8 |     1034 |       201 | 88          | $0.0112      |
| CSD        | HARBOE  | D          |     1 | 6,365,900 |  6,412,572 |       0.7 | ok        |       89.4 |    65319 |      5237 | unknown     | $0.4837      |
| CSD        | HARBOE  | D          |     2 | 6,365,900 |  6,367,620 |       0   | ok        |      137.5 |   174942 |      9376 | unknown     | $1.1560      |
| CSD        | HARBOE  | E          |     1 | 6,365,900 |  4,969,050 |      21.9 | ok        |       28.6 |    28938 |      1705 | unknown     | $0.1958      |
| CSD        | HARBOE  | E          |     2 | 6,365,900 |  4,969,050 |      21.9 | ok        |       35.1 |    29397 |      2383 | unknown     | $0.2185      |
| CSD        | HARBOE  | F          |     1 | 6,365,900 |  5,900,000 |       7.3 | ok        |      132.4 |    32425 |     14893 | 14735       | $0.5756      |
| CSD        | HARBOE  | F          |     2 | 6,365,900 |  5,900,000 |       7.3 | ok        |      121.5 |    31450 |     13394 | 13216       | $0.5303      |
| CSD        | HARBOE  | G          |     1 | 6,365,900 |  6,300,000 |       1   | ok        |       68.5 |    65226 |      4526 | unknown     | $0.4619      |
| CSD        | HARBOE  | G          |     2 | 6,365,900 |  5,800,000 |       8.9 | ok        |      112   |    89908 |      5694 | unknown     | $0.6204      |
| CSD        | 7-UP    | A          |     0 |    13,042 |    240,000 |    1740.3 | ok        |       49.7 |    34638 |      2966 | 2773        | $0.2455      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
