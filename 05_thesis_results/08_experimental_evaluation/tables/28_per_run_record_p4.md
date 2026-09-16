**Complete record of individual runs - part 4 of 6.** Rows 34 to 44 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |   Actual |   Forecast |   APE (%) | Outcome   |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|---------:|-----------:|----------:|:----------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | 7-UP    | A          |     1 |   13,042 |    170,000 |    1203.5 | ok        |       70.3 |    47194 |      3729 | 3576        | $0.3357      |
| CSD        | 7-UP    | A          |     2 |   13,042 |    140,000 |     973.5 | ok        |       54.7 |    44212 |      2725 | 2558        | $0.2861      |
| CSD        | 7-UP    | B          |     1 |   13,042 |     22,000 |      68.7 | ok        |      127.7 |    29497 |     12674 | 12532       | $0.4990      |
| CSD        | 7-UP    | B          |     2 |   13,042 |     23,000 |      76.4 | ok        |      148.4 |    39498 |     14134 | 14018       | $0.5928      |
| CSD        | 7-UP    | C          |     1 |   13,042 |     14,952 |      14.6 | ok        |        4   |     1030 |       122 | 0           | $0.0088      |
| CSD        | 7-UP    | C          |     2 |   13,042 |     14,952 |      14.6 | ok        |        4.1 |     1030 |       120 | 0           | $0.0088      |
| CSD        | 7-UP    | D          |     1 |   13,042 |     28,500 |     118.5 | ok        |      113.3 |   109663 |      9400 | unknown     | $0.8303      |
| CSD        | 7-UP    | D          |     2 |   13,042 |     20,430 |      56.7 | ok        |      110   |   129355 |      7030 | unknown     | $0.8577      |
| CSD        | 7-UP    | E          |     1 |   13,042 |     14,952 |      14.6 | ok        |       27.4 |    28700 |      1612 | unknown     | $0.1919      |
| CSD        | 7-UP    | E          |     2 |   13,042 |     14,952 |      14.6 | ok        |       31.4 |    21096 |      2020 | unknown     | $0.1661      |
| CSD        | 7-UP    | F          |     1 |   13,042 |     20,000 |      53.4 | ok        |      111.5 |    33340 |     12027 | 11839       | $0.4988      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
