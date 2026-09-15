---
name: 2026-09-15_BRANCH_A_final-eight-threads
description: PASS - The last eight open comment threads, each with a verdict and a paste-ready fix where one is needed. Three close on verification alone, three are the appendix regeneration, one is a one-place reword, one is Enrico's and already settled.
category: workflow
applies-to: [ch1_introduction, ch4_data_assessment, ch7_synthesis, ch8_experiment, reference-list, appendix]
triggers: [comment threads, closing comments, final sweep, submission]
created: 2026_09_15-11_05
updated: 2026_09_15-11_05
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# The last eight threads

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`
— **46,465 words, 8 comments in 8 threads.** Zotero re-pulled: **92 items, clean
run** (no crash this time).

**Every thread below has a verdict.** Four need an edit from you; three are the
appendix regeneration already in flight; one is Enrico's and is settled.

| Thread | Surface | Verdict | Work |
|---|---|---|---|
| **23** | Ch1 §1.3.4 | **FIX F1** | one reword, **one place only** |
| **26** | Ch1 §1.3.4 | appendix pass | regenerate Figure 1 |
| **78** | Ch4 §4.2.2 | **FIX F2** | fill one placeholder |
| **80** | Ch4 §4.2.3 | ✅ **VERIFIED-OK** | resolve, no edit |
| **226** | Ch7 §7.4 | ✅ **ADDRESSED** | resolve, no edit |
| **239** | Ch8 §8.3 | appendix pass | regenerate Table 23 |
| **277** | References | **SEQUENCED** | after in-text fields |
| **284** | Appendix A2 | appendix pass | regenerate, v4 → v6 |

---

# F1 — Thread 23, shorten SRQ4

## ⚠ I was wrong about the scope, and it makes this much cheaper

**My earlier note said shortening SRQ4 "means four other chapters must match" and
recommended leaving it alone. That caution was wrong.**

Measured against this snapshot: the full question text appears in **exactly one
place**.

| Location | Carries |
|---|---|
| **Ch1 §1.3.4** | ⚠ the full quoted question — **the only verbatim copy** |
| Ch3 §3.5.4 | a paraphrase: *"SRQ4 concerns whether integrating dedicated lightweight forecasting models into the agentic system is warranted at all..."* |
| Ch9 §9.1.4 | a heading only |
| Ch10 §10.1 | a findings paraphrase |
| Ch2, Ch5, Ch6, Ch7, Ch8 | the label "SRQ4", never the text |

✅ **None of the paraphrases quotes the question, so none of them breaks.** This
is a single-paragraph edit.

### Anchor

**Chapter 1, Section 1.3.4 SRQ4 – Dedicated Models vs. Code Execution.** The
italicised, bolded block quote immediately under that heading. Searchable,
verbatim:

> "To what extent does giving an agentic decision-support system access to
> dedicated lightweight forecasting models improve the correctness, consistency,
> and replicability of forecast-informed decision-support outputs, at justified
> cost and latency, relative to the same system with only data access and code
> execution (a code-as-action baseline), and does that improvement hold in a
> production agentic system as well as in a general-purpose one?"

**64 words, one sentence, four subordinate clauses.**

### Action

REWORD — the quoted question only. The heading and the prose around it stand.

**After:**

> "To what extent does access to dedicated lightweight forecasting models improve
> the correctness, consistency and replicability of an agentic system's
> forecast-informed outputs, at justified cost and latency, relative to the same
> system with only data access and code execution — and does that improvement hold
> in a production agentic system as well as in a general-purpose one?"

**51 words. Thirteen shorter, and nothing lost.**

### Note — what was cut, and why each was safe

| Cut | Why it survives |
|---|---|
| *"giving an agentic decision-support system"* → *"an agentic system's"* | the possessive carries the same relation in four fewer words |
| *"of forecast-informed decision-support outputs"* → *"forecast-informed outputs"* | "decision-support" already qualifies the system; repeating it on the outputs is redundant |
| *"(a code-as-action baseline)"* | ⚠ **the one judgement call.** The term is defined in Ch2 and used throughout Ch8, so it is not lost — but if you want it kept, restore the parenthesis and the question is 55 words, still nine shorter |
| the comma before *"and does that improvement hold"* → an em dash | signals the second clause as a distinct question rather than a trailing afterthought |

✅ **Both halves of the question survive** — the primary comparison and the
production-orchestrator replication. That second clause is what the Prometheus
arms exist to answer, so it could not be cut.

⚠ **Check §1.3's preamble and §1.5's chapter map** after pasting, in case either
paraphrases the long form. Neither did in this snapshot, but both sit within a
page of the edit.

---

# F2 — Thread 78, the ADF appendix placeholder

**The thread says only:** *"Table: step_2_05_adf_per_brand"* — it is telling you
which table fills the placeholder.

### Anchor

**Chapter 4, Section 4.2.2 Stationarity.** The final sentence of the paragraph
beginning *"That treatment is applied uniformly across brands rather than selected
per series..."*. Searchable, verbatim:

> "The cost is accepted deliberately, and the per-brand results are reported in full in Appendix [N]  rather than summarised away."

⚠ **Note the double space before "rather"** — it is in the document, and it is
what makes the string findable.

### Action

REWORD — that sentence.

**After:**

> "The cost is accepted deliberately, and the per-brand results are reported in
> full in Appendix A3 rather than summarised away."

### ⚠ NEEDS-BRIAN — the appendix letter

**The Table of Appendices currently lists only `Appendix A1 – Star Schema
Diagram`.** A2 is the prompt set (thread 284). So the ADF table is **A3 if it is
next in sequence** — but the appendix is mid-regeneration and its final ordering
is yours.

→ **Set the letter when the appendix is rebuilt, and use the same letter here.**
This is the last `Appendix [N]` placeholder in the document — I grepped every
chapter; there are no others.

---

# Thread 80 — VERIFIED-OK, resolve without editing

**Tagged `VERIFY & PROSE & METADATA` on the whole of §4.2.3 Seasonality.** Every
figure checks out against the EDA artefact.

| Prose claim | Artefact | Match |
|---|---|---|
| December 11.5 per cent | `step_2_08_monthly_distribution.md` — Dec, 110,216,851 units, **11.5%**, PEAK | ✅ |
| June 11.1 | Jun, 106,319,098, **11.1%**, PEAK | ✅ |
| March 9.9 | Mar, 94,458,943, **9.9%**, Normal | ✅ |
| May 8.9 | May, 84,943,304, **8.9%**, Normal | ✅ |
| peak set = March, June, September, December | the ten-per-cent-above-mean rule, not these shares | ✅ **the prose says exactly this** |

✅ **The paragraph's most important sentence is the one that distinguishes the two
measures:** *"The peak-month indicator is not taken from these shares directly."*
That is correct and it is the reason March and September appear in the indicator
set while ranking third and seventh by share.

✅ **The renaming rationale is also sound** — the measure detects quarter-end trade
loading, not holidays, and the prose says so without citing the rename as an
editing event.

→ **Resolve as VERIFIED-OK. No edit.**

---

# Thread 226 — Enrico's held table, ADDRESSED

**The longest comment in the document, and it is superseded.** Enrico held §7.4's
calibration table on 10 September pending three things:

| Held on | Status |
|---|---|
| calibration fitted XGBoost for all four categories, but Energidrikke and RTD serve LightGBM | ⚠ **still true** — recorded as **S17** |
| `calibration.csv`'s `mean_rel_width` column holds a median | ⚠ **still true**, cosmetic, recorded |
| the confidence index is degenerate | ✅ **settled** — §7.4 takes the "declare it degenerate" option, which is what shipped |

✅ **The table question itself is resolved by S28:** Chapter 7 carries **no**
calibration table and cites Chapter 5's Table 13 instead. **The held table does
not need unholding — it needs removing from the plan.**

⚠ **The underlying defect is real and remains recorded as S17**, now affecting
Ch5's Table 13, which is the thesis's only copy. It is a known limitation, stated
in the document.

→ **Resolve as ADDRESSED**, pointing at S28 and S17. No prose change.

---

# Threads 26, 239, 284 — the appendix regeneration

**All three are the same pass, already in flight. None is a prose edit.**

| Thread | Target | Defect |
|---|---|---|
| **26** | Ch1 Figure 1, *Hierarchical Structure of Research Questions* | `APPENDIX PASS: RE-GENEREATE` |
| **239** | Ch8 **Table 23**, *The seven scenarios on sixty-three runs* | `Re-generate & Replace` |
| **284** | Appendix A2, prompt set | ships **`v4-five scenarios+e37111d3daaa`**; the funded run is **`v6-shared-composition+af04a42a478b`**, and it describes five scenarios where seven ran |

⚠ **Do not hand-edit any of the three in Word.** All are generated. A manual fix
is overwritten on the next export while leaving the document temporarily correct
— the worst of both.

✅ **Your `37a04f0` commit (the SVG table renderer) is the machinery for 239.**

⚠ **One thing to check while regenerating:** that commit created
`06_substrate_resource_profile` beside the existing `05_substrate_resource_profile`,
and `09_parameter_drift` beside `08_parameter_drift`. If those were renumberings
rather than additions, **the old slugs are now stale duplicates** and the
generator's delete-by-identity step did not catch the rename. Two `ls` calls
during the pass.

✅ **The temperature defect is fixed in code** — see below. Thread 284's
regeneration will pick it up.

→ **Resolve all three when the appendix pass lands.**

---

# Thread 277 — the reference list

**`MUST BE TURNED INTO DYNAMIC ZOTERO REFERENCE LIST.`** Mechanical, and the
sequencing is the whole point:

> ⚠ **Every in-text citation must be a Zotero field before the list is
> generated.** A bibliography built first will not match the text.

**Zotero stands at 92 items and pulled cleanly this run.** ⚠ **Three duplicate
*Elements of Statistical Learning* records** (keys `4TVC5APJ`, `SPW7NXHT`,
`Q4IIBE2Z`, all `webpage`, all missing a year) **plus one missing year on *Smart
"Predict, then Optimize"*** (`HVAURH2K`). **Fix those in Zotero before generating**
— duplicates will render as three separate entries, and a missing year renders as
"n.d.".

→ **Resolve when the dynamic list is generated.**

---

# Done in code this session — the temperature defect

✅ **Both edits applied to `export_appendix.py`**, so the note
`00_appendices/2026-09-14_BRANCH_A_appendix-temperature-claim.md` is now closed.

**Line 446** — the false claim, in a reader-facing table:

```python
# BEFORE
"vary between identical requests even at temperature zero (Atil et al., 2025)."
# AFTER
"vary between identical requests under identical decoding settings "
"(Atil et al., 2025)."
```

**Line 1431** — a redundant row that rendered as "None":

```python
# REMOVED
("Temperature", str(tr.get("temperature", "n/a"))),
# KEPT (your 37a04f0 added this)
("Decoding", tr.get("decoding", "n/a")),
```

⚠ **`gpt-5.5` rejects `temperature` and `top_p` with HTTP 400**, so `TEMPERATURE
= None` and the row printed the string "None" — which reads as a missing value
rather than as a deliberate finding. The `Decoding` row prints
*"temperature/top_p unsupported by the model; defaults used"*, which is the honest
version and is carried in every trace.

✅ **This strengthens Chapter 8.** The consistency finding is more impressive when
decoding was *uncontrolled*: claiming temperature zero implied the variance
survived a control that was never applied.

→ **Takes effect on the next appendix regeneration.** No Word edit.

---

# What closes when

| | Threads |
|---|---|
| **Paste F1 and F2** | 23, 78 |
| **Resolve on verification, no edit** | 80, 226 |
| **Appendix regeneration** | 26, 239, 284 |
| **Citations → fields, then the list** | 277 |

**After F1, F2 and the two verifications: 8 → 4 open, all mechanical.**
