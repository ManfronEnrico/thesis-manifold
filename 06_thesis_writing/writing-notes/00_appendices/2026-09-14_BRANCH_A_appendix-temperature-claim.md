---
name: 2026-09-14_BRANCH_A_appendix-temperature-claim
description: DEFECT - A shipping appendix table asserts the scenarios ran at temperature zero. The model does not support temperature at all, and the harness says so explicitly. One string in export_appendix.py, fixed by regeneration.
category: workflow
applies-to: [appendix, 05_thesis_results, submission preparation]
triggers: [appendix regeneration, temperature, decoding settings, export_appendix]
created: 2026_09_14-17_30
updated: 2026_09_14-17_30
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: open - one-line code fix, then regenerate
---

# A shipping appendix claims a decoding setting the model does not have

Found 2026-09-14 while verifying the model pin for the AI Use Declaration.
Verified at `41ecb76`.

---

# The defect

`04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py:389` emits, into a
reader-facing appendix table:

> "vary between identical requests even at temperature zero (Atil et al., 2025)."

**The scenarios did not run at temperature zero. The model does not support
temperature at all.**

The harness is unambiguous about this, at `srq4_experiment.py:178-188`:

```python
# DECODING IS NOT CONTROLLABLE ON THIS MODEL (verified 2026-08-19).
# gpt-5.5 rejects BOTH `temperature` and `top_p` with HTTP 400
# ("Unsupported parameter"). The original protocol specified temperature 0 as
# the decoding control across scenarios; that is not available on a reasoning model.
#
# This does NOT break the comparison -- every scenario is equally uncontrolled,
# so decoding is held constant across scenarios in the only sense the API permits.
# What it changes is the WRITE-UP: run-to-run consistency is a purely measured
# outcome, and cannot be described as "despite temperature 0". Reporting
# temperature 0 in the methodology would be false.
TEMPERATURE = None            # not settable; recorded as such in every trace
DECODING_NOTE = "temperature/top_p unsupported by the model; defaults used"
```

⚠ **The code anticipated exactly this error and warned against it, and the
appendix exporter makes it anyway.** Every run trace records
`"temperature": None` alongside the decoding note, so the artefact contradicts
its own data source.

---

# Why it matters more than a wording slip

**It weakens Chapter 8's strongest finding.** The consistency result — that
tool-backed scenarios return an identical figure on every repeat while
code-writing scenarios do not — is more impressive, not less, when decoding was
*uncontrolled*. Claiming temperature zero implies the variance survived a control
that was never applied, which is both false and a weaker claim.

⚠ It is also **checkable by a reader**: `gpt-5.5` rejecting `temperature` is
documented vendor behaviour, and the appendix elsewhere prints the run
configuration including the decoding note. **The table can be contradicted by the
table two pages away.**

---

# The fix

## One string, then regenerate

**In `export_appendix.py:389`:**

```python
# BEFORE
"vary between identical requests even at temperature zero (Atil et al., 2025)."

# AFTER
"vary between identical requests under identical decoding settings "
"(Atil et al., 2025)."
```

⚠ **The Atıl et al. citation still supports the reworded claim** — their finding
is about run-to-run variation in generated code, not specifically about
temperature zero. The citation is not the problem; the decoding assertion is.

**Then regenerate the appendix.** Do not hand-edit the `.docx` — this table is
generated, and a manual fix would be silently overwritten on the next export
while leaving the document temporarily correct.

---

# Check for siblings while you are in there

⚠ **`TEMPERATURE` is emitted into the run-configuration table** at
`export_appendix.py:1345` as `("Temperature", str(tr.get("temperature", "n/a")))`.

Since `TEMPERATURE = None`, that renders as **"None"**, which reads as a missing
value rather than as a deliberate finding. **Better:**

```python
("Decoding", tr.get("decoding", "n/a")),
```

which prints *"temperature/top_p unsupported by the model; defaults used"* — the
honest and self-explanatory version, already carried in every trace.

**Also grep the generators for other decoding assertions:**

```bash
grep -rn "temperature" --include=*.py 04_SRQ4_Scenario_Experiment/ 05_thesis_results/
```

---

# Where this belongs in the queue

**With the appendix regeneration pass already in flight**, alongside two other
known regeneration items:

| Item | Defect |
|---|---|
| Appendix A2 prompt set | ships `v4-five scenarios+e37111d3daaa`; the funded run is `v6-shared-composition+af04a42a478b` |
| `ch7_scenarios_v2.svg` | draws five scenarios; seven ran |
| **this** | asserts temperature zero; not settable |

**All three are the same class** — generated artefacts predating the 2026-09-12
redesign — and all three are fixed by regeneration rather than editing.

---

# Related

- `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md` — the
  master audit, which found the first two
- `.claude/rules/generated-artefact-provenance.md` — Correctness tier: every
  number in a generated artefact is computed from an input consumed that run.
  ⚠ **This defect is that rule being violated with a string rather than a
  number**, which the rule's own wording covers: a hardcoded claim is true when
  typed and wrong after the next change
