---
name: ch6-prose-pass-followup-01
description: NOTE - The F/G smoke completed while the pass was being written. Fix 14's block is now narrower, and the combined arms behaved as designed. Read after ch6-prose-pass.md.
snapshot: 2026-09-11_17-24_ch6-prose-pass
category: workflow
applies-to: [ch6-architecture]
created: 2026_09_11-17_55
updated: 2026_09_11-17_55
status: ready
---

# The F/G smoke completed - what it changes

**`ch6-prose-pass.md` stands in full.** This amends one thing in it: Fix 14 said
the F and G arms had not produced rows. **They completed at 17:31**, while the
pass was being written.

| In the main pass | Status |
|---|---|
| Fix 14, the blocking reason | **narrowed** - see below. The section is still blocked, for a different and smaller reason |
| Everything else | unchanged |

---

# F1 - Both new arms ran clean on the first attempt

Seven scenarios, one brand-month, CSD / HARBOE, held-out actual 6,365,900 units.

| Scenario | Forecast | Error | Latency | Cost |
|---|---|---|---|---|
| F - data, code and the model | 6,200,000 | **2.6%** | 75 s | $0.22 |
| G - the same, on the production orchestrator | 5,604,800 | 12.0% | 81 s | $0.33 |

Both classified `ok`. No failures, no retries, no schema violations.

**This is a pipeline result, not a finding.** One brand, one month, one run per
arm.

---

# F2 - DEC-COMBINED-INPUT held, and that is the thing worth checking

The design decision recorded in `3c37ffd` was that the model's forecast goes in
as **one input among several**, never as a starting point to revise, because an
agent handed a number and told it may keep it will mostly keep it.

**The traces show the decision holding.** Both arms received the model's
forecast of 4,969,049.5 and **neither returned it**:

| Arm | Code executions | Received | Returned |
|---|---|---|---|
| F | 12 | 4,969,050 | 6,200,000 |
| G | 2 | 4,969,050 | 5,604,800 |

Had either arm echoed the model's number, the experiment would have been
measuring deference rather than integration, and the arm would have been worth
nothing. **Neither did.** F ran twelve code executions on top of the forecast it
was handed, and moved 25 per cent away from it.

⚠ **Do not write this into Chapter 6 as a result.** It is a check that the
instrument works, which belongs in Chapter 8's method description if anywhere.

---

# F3 - Fix 14 is still blocked, but the reason has changed

**The old reason is gone:** the arms have now been exercised.

**The reason it stays blocked is S21** - the display labels in
`srq4_experiment.py` map three of seven scenarios and invert the lettering, so
`C_model` prints as "A" and `A_plain` prints as "C", while D through G fall
through to raw internal names.

Section 6.7's job, per your comment asking to *"name each scenario and map it to
the respective set-up"*, is precisely to fix the naming. **Writing that
enumeration against code whose own output contradicts it would bake the
contradiction into the chapter.**

**Recommended order:**

1. Fix the display map in `srq4_experiment.py` - delete it and print the ladder
   letters the thesis uses. Small, and it is a code edit, not a prose one.
2. Then write Section 6.7 against a single consistent set of names.

That is a short task and I can do it on your word. I have not done it
unprompted, because choosing the display order is a presentation decision about
published tables rather than a defect fix, and S21 records both options.

---

# F4 - One thing the pilot flags for Chapter 8, not Chapter 6

Across both repetitions, the code-writing arms beat the model-backed arms on
this brand-month, and the combined arms did too:

| Kind | Arms | Error range |
|---|---|---|
| writes its own code | B, D, F | 1.5 to 21.8 per cent |
| model behind a tool | C, E | 21.9 per cent, identically |
| combined | F, G | 2.6 and 12.0 per cent |

**C and E returned exactly the same number on every run**, to the decimal, which
is the reliability property Section 6.4 claims and now has evidence for. It is
also why their error does not move: the tool returns one forecast, and both
orchestrators relay it faithfully.

⚠ **This does not weaken Section 6.4, and the pass deliberately does not soften
it.** Section 6.4 justifies the interface on reliability, reproducibility and
auditability, and never on accuracy. That restraint is now load-bearing. The
accuracy direction is a Chapter 8 finding and a Chapter 10 limitation.

The one-line reading for Chapter 8, when it comes: the comparison may be
measuring **per-series adaptation** rather than code-versus-model, because the
code-writing arms fit a small model competition per brand while the tool serves
one booster tuned category-wide.
