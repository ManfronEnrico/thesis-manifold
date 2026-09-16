**Composition of the scenario prompts.** Prompt components by scenario. Only the blocks below the rule differ between arms; those are the treatment.

|                           | A   | B   | C   | D   | E   | F   | G   |
|:--------------------------|:----|:----|:----|:----|:----|:----|:----|
| The question              | •   | •   | •   | •   | •   | •   | •   |
| Output exemplar           | •   | •   | •   | •   | •   | •   | •   |
| Sentinel instruction      | •   | •   | •   | •   | •   | •   | •   |
| No firm data              | •   |     |     |     |     |     |     |
| Sales history + schema    |     | •   |     | c   |     | •   | c   |
| Model forecast payload    |     |     |     |     | c   | •   | c   |
| Forecast tool             |     |     | •   |     |     |     |     |
| Analysis task             |     | •   |     | c   |     |     |     |
| Analysis task, with model |     |     |     |     |     | •   | c   |
| Do not query warehouse    |     |     |     | c   | c   |     | c   |
| Route to analysis engine  |     |     |     | c   | c   |     | c   |

*Note.* • the arm receives this component; c reaches only the nested coder, not the conversational agent. Membership is computed from the assembled prompts, so an arm cannot appear to share a component it does not. Schema v6-shared-composition+af04a42a478b.
