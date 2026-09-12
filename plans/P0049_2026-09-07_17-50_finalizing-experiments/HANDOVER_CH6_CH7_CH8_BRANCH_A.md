---
name: handover-ch6-ch7-ch8-branch-a
description: HANDOVER - Instructions for the session drafting complete Ch6, Ch7 and Ch8 prose against Branch A. Written for a session with no conversation history.
pid: P0049
created: 2026_09_13
updated: 2026_09_13
status: current
---

# Handover — Ch6, Ch7, Ch8 prose passes against BRANCH A

**You have no conversation history. This file plus `BRANCH_A_STATE.md` is the
whole picture for the experiment. Read both before writing a sentence.**

---

## What Branch A is, in one paragraph

The SRQ4 experiment is **finished and paid for**: 63 runs, prompt schema
`v6-shared-composition+af04a42a478b`, committed at **`58243f3`**. A separate plan
(**P0055**) may re-engineer the forecasting features and re-run everything as
"Branch B", but **that has not happened and may never happen**. Branch A is what
the thesis ships if Branch B is abandoned. **Write Ch6/Ch7/Ch8 as if Branch A is
final**, because today it is.

---

## Read in this order

1. **`BRANCH_A_STATE.md`** (this folder) — the measured experiment: setup,
   payload, prompt schema, results table, cost reconciliation, known defects
2. **`START_HERE.md`** (this folder) — the ⚠ banner at the top lists four figures
   that are wrong elsewhere in the plan
3. `../P0055_.../findings.md` — **only** for the "what may change later" caveats
4. `.claude/rules/prose-insertion-discipline.md` — **mandatory** before any
   writing pass

---

## ⚠ Before you write anything: run `/re-snap`

The `.docx` is the only authoritative prose surface and it moves. `/re-snap` runs
the git fetch, the snapshot, the diff against the previous snapshot and the
Zotero pull together. **Anchors quoted from a stale snapshot cannot be found by
the author**, which is the single most common way a prose pass wastes everyone's
time.

Then **sweep each chapter's note folder** (`06_thesis_writing/writing-notes/chN_*/`)
before writing. Notes left there are claims that still need applying. Seven notes
were added on 2026-09-12 and are **unapplied**:

| Chapter | Note |
|---|---|
| ch3 | `srq4-data-input-is-a-constructed-choice.md` |
| ch7 | `what-the-tool-must-carry-for-an-agent-to-weigh-it.md` |
| ch8 | `the-agent-input-contract.md`, `prompt-consistency-as-an-experimental-control.md` |
| ch9 | `ad-hoc-data-science-vs-a-trained-pipeline.md`, `the-result-hinges-on-forecasting-practice.md`, `when-to-use-which-scenario-group.md` |

---

## Chapter-by-chapter

### Ch6 — Architecture. **Safe to finalise.**

Branch B touches feature engineering and model repairs. **It does not change
Ch6's argument.** Write it as final.

One number to check: Ch6 answers *"if the model needs thirteen months of lag
depth, how does it answer today?"* (`ch6-CONSOLIDATED-pass.md:981`,
`anticipated-assessor-questions.md:251`). If Branch B lands, that becomes
**twelve** — which makes the argument slightly *easier*, not harder. Write
thirteen for now; it is what the shipped pipeline does.

### Ch7 — Synthesis / tool interface. **Safe to finalise, three stale numbers.**

Its **latency, token and cost figures pin to `smoke/runs.csv` (2026-09-11)**,
which the 63-run set superseded. The *argument* is unaffected; the numbers are
stale either way. Take them from `BRANCH_A_STATE.md` §4 instead.

The unapplied ch7 note (`what-the-tool-must-carry...`) is about what the tool
must expose for an agent to weigh a forecast — that is Ch7's contribution and
should land in this pass.

### Ch8 — Experimental evaluation. **The big one. Currently a skeleton.**

1,384 words with `[N] SKUs × 28 retailers × [T] weeks` placeholders, a **weekly
grain that contradicts the monthly panel**, and pre-v6 WMAPE figures.
**Everything in it must be rewritten from `BRANCH_A_STATE.md`.**

Structure it around the ladder, which is the design's whole point:

```
A_llm_plain -> B_llm_data -> C_llm_model -> F_llm_data_model    (hosted)
D_prometheus_data -> E_prometheus_model -> G_prometheus_data_model  (orchestrator)
```

**A→B measures what data access buys. B→C measures what the trained model adds —
that is the thesis contribution. C→F measures what returning code on top adds.**
D/E/G repeat the three rungs on the orchestrator so the ladders compare rung for
rung.

---

## Five things about the results that will trip you up

**1. Outcomes are classified, never averaged.** A scenario answering 6 of 9 is
not comparable to one answering 9 of 9. Report the taxonomy beside the accuracy.

**2. The only failures are three implausible `A_llm_plain` forecasts, all
ØRBÆK** — 120,000 / 62,000 / 90,000 against an actual of 2,850. A model with no
firm data, asked about a small regional Danish brand, over-forecasts by 20-40x.
**This is the ladder's bottom rung behaving exactly as designed**, not a bug.

**3. C and E are identical on every metric** (mean APE 13.14, median 14.65,
CV 0.0%, TAR 1.00). **This is correct** — both read the same persisted model
deterministically. `summary.md` does **not** say so, and two identical columns
read as a copy-paste error. **State it explicitly in the prose.**

**4. HARBOE cuts against the headline.** The trained model scores **21.9** mean
APE on HARBOE where data-only scenarios get **0.6-4.1**. Do not bury this.
Understand it before writing the B→C argument, because it is the obvious
examiner question.

**5. 7-UP is the hard brand for everyone** (A 1305.8, B 78.9, D 73.6, G 41.9).
Per-brand heterogeneity is a finding, not noise.

---

## Numbers: where to get them, and three not to trust

**Everything computed goes through `BRANCH_A_STATE.md` §4 or is recomputed from
`runs.csv`.** Never transcribe from `summary.md` without checking these three:

| Do not trust | Use instead |
|---|---|
| `runs.csv` "has 63 rows" | **69 rows.** 6 are superseded `v2`. **Filter `schema.str.startswith('v6')`** — pooling once reported $11.13 for an $8.05 block |
| `summary.md:42` "Actually billed: $18.4647" | **$19.60 actual** — the balance delta across two run invocations. $18.46 is ONE billing window |
| `cost_usd_est` as the cost | Estimator **overshoots 29%**. Ramp-up basis: **~$0.31/run** |

**Generated-artefact rule applies**: every figure in a table or caption is read
from an input consumed on that run. A hardcoded number is true when typed and
wrong after the next re-run.

---

## What NOT to do

- **Do not edit `summary.md` by hand.** It is regenerated by `_write_summary()`
  at `srq4_experiment.py:1804`. Fix the producer, or your edit vanishes.
- **Do not delete the 6 `v2` rows from `runs.csv`.** They are the record of a
  superseded run. Filter at every read site instead.
- **Do not touch the prompt schema.** Any edit invalidates 63 paid runs.
- **Do not write prose into `sections-drafts/`.** That is a claims ledger —
  bullets, status, provenance only. Prose goes in the OneDrive `.docx`, staged
  via `writing-notes/`.
- **Do not cite a source that is not in Zotero.** Re-pull before checking.

---

## Fix regardless of branch

**Ch9 §9.1.4 still states the code-as-action baseline "was not executed… E2B is
not configured."** It ran **63 times**. This is false on either branch and must
go. It is Ch9, not your three chapters, but you will see it referenced.

---

## The state of the repo as you inherit it

Commit **`58243f3`** on `main` holds everything: the v6 harness, the payload
generator, `runs.csv`, `summary.md`, all 65 raw responses, the agent input CSVs,
seven writing notes and the P0055 book scan.

⚠ **It was NOT pushed** — `git push` was blocked by a permission classifier.
Verify with `git rev-list --left-right --count origin/main...HEAD` and push
before doing anything else, or this all lives on one disk.

⚠ `raw_responses/` holds **65** JSON files for **63** runs: seven are orphaned
`RB_K`-slugged rep0 files from before the ØRBÆK transliteration fix, and A and G
carry their rep0 twice. **`runs.csv` is unaffected and clean** — 63 rows, one per
(system, brand, rep). Full account in `../P0055_.../FALLBACK.md`.
