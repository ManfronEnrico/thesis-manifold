**Complete record of individual runs - part 5 of 6.** Rows 45 to 55 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |   Actual |   Forecast |   APE (%) | Outcome     |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|---------:|-----------:|----------:|:------------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | 7-UP    | F          |     2 |   13,042 |     18,500 |      41.9 | ok          |       64.3 |    16518 |      3288 | 3113        | $0.1525      |
| CSD        | 7-UP    | G          |     1 |   13,042 |     18,000 |      38   | ok          |       62.2 |    61269 |      4183 | unknown     | $0.4318      |
| CSD        | 7-UP    | G          |     2 |   13,042 |     18,000 |      38   | ok          |       80.6 |    62224 |      5733 | unknown     | $0.4831      |
| CSD        | ØRBÆK   | A          |     0 |    2,850 |    120,000 |           | implausible |       63.8 |    54821 |      3126 | 2927        | $0.3512      |
| CSD        | ØRBÆK   | A          |     1 |    2,850 |     62,000 |           | implausible |       90.8 |    75215 |      4120 | 3955        | $0.4830      |
| CSD        | ØRBÆK   | A          |     2 |    2,850 |     90,000 |           | implausible |       84.9 |    67365 |      4395 | 4227        | $0.4520      |
| CSD        | ØRBÆK   | B          |     1 |    2,850 |      2,900 |       1.7 | ok          |      160   |    25341 |     11306 | 11182       | $0.4959      |
| CSD        | ØRBÆK   | B          |     2 |    2,850 |      2,840 |       0.4 | ok          |       83   |    23526 |      9835 | 9712        | $0.3931      |
| CSD        | ØRBÆK   | C          |     1 |    2,850 |      2,769 |       2.8 | ok          |        3.3 |     1041 |       113 | 0           | $0.0086      |
| CSD        | ØRBÆK   | C          |     2 |    2,850 |      2,769 |       2.8 | ok          |        3.2 |     1041 |       111 | 0           | $0.0085      |
| CSD        | ØRBÆK   | D          |     1 |    2,850 |      2,872 |       0.8 | ok          |      101.8 |   107313 |      9003 | unknown     | $0.8067      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
