**Comparison of decision-support scenarios.** Performance of each scenario across the five evaluation dimensions. 

| Measure                              | A       | B       | C       | D       | E       | F       | G       |
|:-------------------------------------|:--------|:--------|:--------|:--------|:--------|:--------|:--------|
| Runs completed                       | 9       | 9       | 9       | 9       | 9       | 9       | 9       |
| Usable answers                       | 6       | 9       | 9       | 9       | 9       | 9       | 9       |
| Median APE (%)                       | 502.2   | 2.9     | 14.6    | 0.9     | 14.6    | 7.3     | 1.8     |
| Mean APE (%)                         | 662.1   | 27.9    | 13.1    | 25.0    | 13.1    | 18.3    | 15.6    |
| Consistency, CV across repeats (%)   | 26.7    | 4.1     | 0.0     | 8.1     | 0.0     | 1.7     | 3.3     |
| Replicability, identical answers (%) | 0       | 0       | 100     | 0       | 100     | 33      | 33      |
| Top-answer agreement rate            | 0.33    | 0.44    | 1.00    | 0.56    | 1.00    | 0.67    | 0.78    |
| Tokens per answer                    | 60,566  | 39,420  | 1,165   | 109,228 | 30,168  | 38,437  | 81,827  |
| of which reasoning tokens            | 3,391   | 10,740  | 10      | unknown | unknown | 10,165  | unknown |
| Cost per answer, estimated (USD)     | $0.3798 | $0.4667 | $0.0091 | $0.7664 | $0.1994 | $0.4253 | $0.5536 |
| Response time (s)                    | 69.5    | 123.8   | 6.0     | 111.3   | 31.7    | 103.9   | 84.4    |

*Note.* Scenarios: A = A_llm_plain; B = B_llm_data; C = C_llm_model; D = D_prometheus_data; E = E_prometheus_model; F = F_llm_data_model; G = G_prometheus_data_model. Correctness, consistency and replicability are primary; cost and response time secondary. Top-answer agreement is the share of repeats returning the most common answer within 1%. Reasoning tokens show as unknown for D, E, G: the production orchestrator does not report them, so this is an absent figure rather than a measured zero.
