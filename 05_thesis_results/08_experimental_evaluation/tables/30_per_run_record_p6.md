**Complete record of individual runs - part 6 of 6.** Rows 56 to 63 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |   Actual |   Forecast |   APE (%) | Outcome   |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|---------:|-----------:|----------:|:----------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | ØRBÆK   | D          |     2 |    2,850 |      2,824 |       0.9 | ok        |      102   |    92156 |      8111 | unknown     | $0.7041      |
| CSD        | ØRBÆK   | E          |     1 |    2,850 |      2,769 |       2.8 | ok        |       26.3 |    28951 |      1373 | unknown     | $0.1859      |
| CSD        | ØRBÆK   | E          |     2 |    2,850 |      2,769 |       2.8 | ok        |       35   |    29346 |      2240 | unknown     | $0.2139      |
| CSD        | ØRBÆK   | F          |     1 |    2,850 |      2,850 |       0   | ok        |       93.1 |    25255 |      9820 | 9673        | $0.4013      |
| CSD        | ØRBÆK   | F          |     2 |    2,850 |      2,850 |       0   | ok        |       46.4 |    18100 |      3746 | 3600        | $0.1833      |
| CSD        | ØRBÆK   | G          |     0 |    2,850 |      2,822 |       1   | ok        |      109.8 |   108394 |      7971 | unknown     | $0.7811      |
| CSD        | ØRBÆK   | G          |     1 |    2,850 |      2,800 |       1.8 | ok        |       76.7 |    81587 |      5690 | unknown     | $0.5786      |
| CSD        | ØRBÆK   | G          |     2 |    2,850 |      2,820 |       1.1 | ok        |       64.4 |    61142 |      4241 | unknown     | $0.4329      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
