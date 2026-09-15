**Complete record of individual runs - part 2 of 6.** Rows 12 to 22 of 63. Every run logged, with its forecast, error, outcome class, response time and cost. This is the evidence base from which the aggregate figures are computed. 

| Category   | Brand   | Scenario   |   Rep |    Actual |   Forecast |   APE (%) | Outcome   |   Time (s) |   Tok in |   Tok out | Tok reas.   | Cost (USD)   |
|:-----------|:--------|:-----------|------:|----------:|-----------:|----------:|:----------|-----------:|---------:|----------:|:------------|:-------------|
| CSD        | 7-UP    | F          |     0 |    13,042 |     19,000 |      45.7 | ok        |      139   |    34911 |     12279 | 12129       | $0.5234      |
| CSD        | 7-UP    | G          |     0 |    13,042 |     19,500 |      49.5 | ok        |      101.3 |    88603 |      8064 | unknown     | $0.6849      |
| CSD        | ØRBÆK   | B          |     0 |     2,850 |      2,857 |       0.2 | ok        |      146.2 |    27175 |     11131 | 10987       | $0.4998      |
| CSD        | ØRBÆK   | C          |     0 |     2,850 |      2,769 |       2.8 | ok        |        4   |     1041 |       115 | 0           | $0.0087      |
| CSD        | ØRBÆK   | D          |     0 |     2,850 |      2,856 |       0.2 | ok        |      112.4 |    58436 |     11411 | unknown     | $0.6345      |
| CSD        | ØRBÆK   | E          |     0 |     2,850 |      2,769 |       2.8 | ok        |       34.7 |    29010 |      2121 | unknown     | $0.2087      |
| CSD        | ØRBÆK   | F          |     0 |     2,850 |      2,800 |       1.8 | ok        |      108.2 |    28186 |      9980 | 9817        | $0.4208      |
| CSD        | HARBOE  | A          |     1 | 6,365,900 |  7,200,000 |      13.1 | ok        |       74.8 |    77003 |      3634 | 3438        | $0.4773      |
| CSD        | HARBOE  | A          |     2 | 6,365,900 |  4,400,000 |      30.9 | ok        |       64.7 |    53195 |      3679 | 3475        | $0.3763      |
| CSD        | HARBOE  | B          |     1 | 6,365,900 |  6,850,000 |       7.6 | ok        |      136.7 |    33009 |     14578 | 14453       | $0.5690      |
| CSD        | HARBOE  | B          |     2 | 6,365,900 |  6,550,000 |       2.9 | ok        |       89   |    25825 |      5913 | 5768        | $0.2778      |

*Note.* Actual and Forecast are in units; Rep is the repeat index; Tok in, Tok out and Tok reas. are input, output and reasoning tokens. The full response for each run, including any code generated and the reasoning summary returned by the model, is retained alongside these records. Scenarios are abbreviated to their letter: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model.
