<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->
<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 carry only what a thesis reader should see, which is why this lives here and not beside the artefact it describes. -->

# Communication of forecast uncertainty by scenario

| | |
|---|---|
| Table | `05_thesis_results/07_decision_synthesis/tables/13_interval_communication.md` |
| Producer | `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` |
| Written | 2026-09-13 10:40 UTC |

---

Closes the Ch2 sec 2.3 / SRQ4 gap (N9/N10 Option 2). Scored retrospectively from already-logged runs -- NO new API spend. All checks deterministic (regex + numeric comparison vs the tool payload), no judge, consistent with N5b.

The 'gives a recommendation' criterion was dropped while the shared question did not ask for one, and RESTORED on 2026-09-13: prompts.py v3 (2026-09-03) added the request and all seven arms receive it identically, so the criterion now measures compliance with an instruction that was given. The 33% figure from the FIRST pilot still must not be cited -- it predates the prompt change.

Criterion 2 is scored against a RECOMPUTED payload. The v6 harness logs payload_complete as a boolean and discards the payload, so the interval the agent was given is not in the trace; the scorer recalls the tool and verifies the recomputed point forecast against the logged one before using its interval. If the models are retrained the check fails and the criterion goes unscored rather than silently wrong.

Do NOT claim improved human decisions; needs Goodwin's design + ethics approval (cf. MR-10).
