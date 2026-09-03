**Communication of forecast uncertainty by scenario.** Number of answers satisfying each criterion for conveying uncertainty, with the percentage in parentheses, scored against the payload the forecasting tool returned. n denotes the number of answers scored in each scenario.

| Criterion                     | A - no firm data (n=3)   |
|:------------------------------|:-------------------------|
| States a range                | 3 of 3 (100)             |
| Range matches the tool output | 0 of 3 (0)               |
| States confidence             | 3 of 3 (100)             |
| Mean criteria met (of 3)      | 2.00                     |

*Note.* Goodwin, Onkal and Thomson (2010) find that a prediction interval presented as a bare numeric range does not improve decisions and can degrade them, because the step from interval to decision is left to the reader. These criteria record whether that step was supplied: whether a range was stated, whether it corresponds to the one the model produced, and whether the associated confidence was reported. Each is evaluated by direct comparison of the numbers in the answer against the numbers the tool returned, with a five per cent tolerance; no judgement is involved. A scenario with no access to the forecasting tool cannot satisfy the second criterion, which requires a retrieved source against which a stated range can be checked. These measures concern what the system communicated. Whether such communication improves the decisions of human planners is not examined in this thesis and would require a controlled decision experiment with human participants.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Closes the Ch2 sec 2.3 / SRQ4 gap (N9/N10 Option 2). Scored retrospectively from already-logged runs -- NO new API spend. All checks deterministic (regex + numeric comparison vs the tool payload), no judge, consistent with N5b.

DROPPED the 'gives a recommendation' criterion: the shared prompt asks for 'the number, a range, and how confident you are' and never asks for a recommendation, so scoring it measured compliance with an instruction never given. The 33% figure from the first pilot must NOT be cited. If we want it, the prompt has to ask for it -- and that changes the single-variable design, so it is a deliberate decision, not a scorer tweak.

Do NOT claim improved human decisions; needs Goodwin's design + ethics approval (cf. MR-10).
