**Distribution of run outcomes by scenario.** Counts and percentages of runs falling into each outcome class.

| Outcome              | A_llm_plain   | B_llm_data   | C_llm_model   | D_prometheus_data   | E_prometheus_model   | F_llm_data_model   | G_prometheus_data_model   |
|:---------------------|:--------------|:-------------|:--------------|:--------------------|:---------------------|:-------------------|:--------------------------|
| Usable answer        | 6 (67%)       | 9 (100%)     | 9 (100%)      | 9 (100%)            | 9 (100%)             | 9 (100%)           | 9 (100%)                  |
| Execution error      | 0 (0%)        | 0 (0%)       | 0 (0%)        | 0 (0%)              | 0 (0%)               | 0 (0%)             | 0 (0%)                    |
| No forecast returned | 0 (0%)        | 0 (0%)       | 0 (0%)        | 0 (0%)              | 0 (0%)               | 0 (0%)             | 0 (0%)                    |
| Timed out            | 0 (0%)        | 0 (0%)       | 0 (0%)        | 0 (0%)              | 0 (0%)               | 0 (0%)             | 0 (0%)                    |
| Implausible value    | 3 (33%)       | 0 (0%)       | 0 (0%)        | 0 (0%)              | 0 (0%)               | 0 (0%)             | 0 (0%)                    |

*Note.* Failures are reported as classes rather than averaged into the accuracy figures. A scenario that returns a usable answer in a fraction of runs is not directly comparable to one that always answers, and a single implausible value distorts a mean without bound; classifying such runs preserves both facts.
