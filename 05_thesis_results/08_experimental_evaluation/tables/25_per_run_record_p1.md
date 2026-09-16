**Complete record of individual runs - part 1 of 6.** Rows 1 to 11 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |    Actual |   Forecast |   APE (%) | Outcome   |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|----------:|-----------:|----------:|:----------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | HARBOE  | A          |     0 | 6,365,900 |  7,100,000 |      11.5 | ok        |       71.6 |    59259 |      3816 | 3590        | $0.4108      |
| CSD        | HARBOE  | B          |     0 | 6,365,900 |  6,250,000 |       1.8 | ok        |       87.9 |    21672 |      4447 | 4320        | $0.2718      |
| CSD        | HARBOE  | C          |     0 | 6,365,900 |  4,969,050 |      21.9 | ok        |       12.9 |     1033 |       136 | 0           | $0.0092      |
| CSD        | HARBOE  | D          |     0 | 6,365,900 |  6,300,000 |       1   | ok        |      155.3 |   103662 |     14740 | unknown     | $0.9605      |
| CSD        | HARBOE  | E          |     0 | 6,365,900 |  4,969,050 |      21.9 | ok        |       33.7 |    29292 |      2040 | unknown     | $0.2077      |
| CSD        | HARBOE  | F          |     0 | 6,365,900 |  5,900,000 |       7.3 | ok        |      118.1 |    32766 |     13554 | 13365       | $0.5417      |
| CSD        | HARBOE  | G          |     0 | 6,365,900 |  6,300,000 |       1   | ok        |       83.7 |    66088 |      5898 | unknown     | $0.5074      |
| CSD        | 7-UP    | B          |     0 |    13,042 |     25,000 |      91.7 | ok        |      134.9 |    31404 |     13818 | 13692       | $0.6016      |
| CSD        | 7-UP    | C          |     0 |    13,042 |     14,952 |      14.6 | ok        |        6.5 |     1030 |       122 | 0           | $0.0088      |
| CSD        | 7-UP    | D          |     0 |    13,042 |     19,000 |      45.7 | ok        |       80.1 |    62911 |      4991 | unknown     | $0.4643      |
| CSD        | 7-UP    | E          |     0 |    13,042 |     14,952 |      14.6 | ok        |       33.2 |    29301 |      1985 | unknown     | $0.2061      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
