<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Communication of forecast uncertainty by scenario

| | |
|---|---|
| Table | `05_thesis_results/07_decision_synthesis/tables/13_interval_communication.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-10 17:27 UTC |

---

Closes the Ch2 sec 2.3 / SRQ4 gap (N9/N10 Option 2). Scored retrospectively from already-logged runs -- NO new API spend. All checks deterministic (regex + numeric comparison vs the tool payload), no judge, consistent with N5b.

DROPPED the 'gives a recommendation' criterion: the shared prompt asks for 'the number, a range, and how confident you are' and never asks for a recommendation, so scoring it measured compliance with an instruction never given. The 33% figure from the first pilot must NOT be cited. If we want it, the prompt has to ask for it -- and that changes the single-variable design, so it is a deliberate decision, not a scorer tweak.

Do NOT claim improved human decisions; needs Goodwin's design + ethics approval (cf. MR-10).
