**Comparison of decision-support scenarios.** Performance of each scenario across the five evaluation dimensions. Covers 6 of an intended 225 runs (15 brands x 5 repeats x 3 scenarios) and one of the three scenarios; the remaining scenarios have not yet been run at the corrected prompt. 

| Measure                              | A - no firm data   |
|:-------------------------------------|:-------------------|
| Runs completed                       | 6                  |
| Usable answers                       | 6                  |
| Median APE (%)                       | 56.4               |
| Mean APE (%)                         | 93.7               |
| Consistency, CV across repeats (%)   | 16.2               |
| Replicability, identical answers (%) | 0                  |
| Top-answer agreement rate            | 0.50               |
| Tokens per answer                    | 83,732             |
| of which reasoning tokens            | 3,816              |
| Cost per answer, estimated (USD)     | $0.5130            |
| Response time (s)                    | 114.6              |

*Note.* The scenarios form an information ladder: A has no access to firm data, B may execute code against it, and C additionally calls the dedicated forecasting model. Correctness, consistency and replicability are the primary dimensions; cost and response time are secondary. The top-answer agreement rate is the share of repeated runs returning the most common answer within a 1% tolerance, where 1.00 denotes complete agreement across repeats.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

'TAR@N' was jargon -- renamed 'top-answer agreement rate' and defined inline + in the dictionary. Cite Atil et al. (2025).
