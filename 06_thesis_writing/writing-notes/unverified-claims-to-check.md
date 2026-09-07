---
name: unverified-claims-to-check
description: RULE - Running list of claims and citations that entered the project WITHOUT verification against the Zotero library. Brian must verify or remove each before it reaches thesis prose.
category: governance
applies-to: [all chapters, all methodology claims, all code comments citing literature]
triggers: [citing a source from memory, stating a numeric threshold, quoting a convention, writing a methods sentence, reviewing before submission]
created: 2026_09_06-16_10
updated: 2026_09_07-10_45
---

# Unverified claims to check

Every row here entered the project **without being checked against the Zotero
library**. Each is either wrong, unverifiable, or true-but-uncited. None may
reach thesis prose until it is verified or removed.

## Why this file exists

On 2026-09-06 Claude wrote `Hair et al. (2019) Multivariate Data Analysis` into
a code comment as the source of the VIF > 10 threshold. The attribution was made
**from memory**. The source is not in the Zotero library, was never read, and
could not be checked — but the comment read as though it had been.

That is the same defect the project has already corrected twice in its own data
pipeline: the old `holiday_months` feature asserted a cause the computation never
established, and `DEFAULT_HOLIDAY_MONTHS` was an inherited constant that looked
measured. A citation invented to justify a threshold is that failure in the
literature layer, and it is more dangerous there because a reader cannot inspect
it against the data.

**Rule: if a source is not in the library, it is not a source.** Write the claim
here instead, and let Brian decide.

## Open items

| # | claim | where it entered | status |
|---|---|---|---|
| 1 | VIF > 10 = "serious" multicollinearity, > 5 = stricter cut-off | `srq1_feature_diagnostics.py` (constants) | **Attribution removed.** The bands remain as *reporting* bands only, and nothing is dropped because of them. If prose ever states a numeric VIF threshold, a verified source is required first. |
| 2 | Spearman \|rho\| >= 0.95 defines a redundancy cluster | `srq1_feature_diagnostics.py::REDUNDANCY_RHO` | **Never had a source.** It is a chosen reporting parameter, not a convention. Either justify it by sensitivity analysis (does the cluster structure change at 0.90 / 0.99?) or describe it as an arbitrary reporting choice. Do not imply it is standard. |
| 3 | "Lukkeloven was liberalised in 2012", Danish stores open Sundays | Claude, in conversation; now in `engineer_features.py::add_holiday_features` docstring and in the enrichment writing note | Brian confirmed the *substance* (Danish retail trades weekends) from domain knowledge, which is what the feature design rests on. The **year and the statute name** came from Claude and are uncited. Either cite Danish retail-hours legislation or drop the specifics and keep the plain statement. |
| 4 | Store Bededag abolished effective 2024 (L 13, adopted 2023-02-28) | `export_holiday_appendix.py`, appendix table 91 review note | The *effect* is verified in data — the Nager API returns 15 holidays through 2023 and 14 from 2024. The **bill number and adoption date** were written from memory and are not verified. Verify against Danish legislation or cite only the observed change. |

## How to use this file

- **Adding**: any time a source is named from memory rather than from the
  library, or a numeric convention is stated without one, add a row here in the
  same edit that introduces it. Do not wait for a review pass.
- **Clearing**: verify against the library (or add the source to Zotero and
  re-export `citations.json`), then either cite it properly or delete the claim.
  Move the row to "Resolved" with what was done.
- **Before submission**: this file must be empty of open items, or every
  remaining item must have been deliberately removed from the prose.

## Related

- `06_thesis_writing/citations/citations.json` — the library, 86 entries; the
  only acceptable source of a citation
- `utility_scripts/scripts/zotero_client.py` — re-export after adding to Zotero
- `.claude/rules/writing-surface-authority.md` — prose lives in the `.docx`;
  this file is a planning surface
- `plans/P0046_..._exogenous-enrichment-decision/findings.md` F12, F14 — the
  measured corrections of Claude's own claims in the same session

| 5 | XGBoost's histogram builder reduces per-thread gradient sums in completion order, so thread count changes the result | `srq1_benchmark.py::XGB_N_JOBS` comment and P0047 F18 | **MEASURED IN-PROJECT, mechanism NOT cited.** The *effect* is directly measured and reproducible in this repo (n_jobs 1/2/4/8 -> WMAPE 34.65/34.95/35.40/37.30, seed and data fixed) — that evidence stands on its own and needs no citation. The *explanation* (non-associative float reduction over threads) is Claude's, from general knowledge, and is not backed by an XGBoost reference. **In prose: report the measurement, and either cite XGBoost documentation for the mechanism or state the cause as the most likely explanation rather than established fact.** |


---

## Verification workflow (added 2026-09-07)

These five claims now have a NotebookLM briefing pack at
`06_thesis_writing/notebookLM/04-Claims_Verification/`, where they are numbered
**CV-01 … CV-05** in the same order as the table above.

| Register # | Brief ID | Claim |
|---|---|---|
| 1 | CV-01 | VIF 5 / 10 |
| 2 | CV-02 | Spearman >= 0.95 |
| 3 | CV-03 | Lukkeloven 2012 |
| 4 | CV-05 | Store Bededag abolition |
| 5 | CV-04 | XGBoost thread determinism |

**This file stays the source of truth for what is open.** The brief is the instrument;
this register records the outcome. When a verdict comes back, update the status column
here — do not delete a row. A resolved row showing how it was resolved is more useful
than an absent one, because it evidences that the claim was checked.

**Run it in two notebooks, not one** (see the HOW-TO-RUN): CV-01/CV-02 need a body of
statistical literature, CV-03/CV-04/CV-05 need specific documents. A single mixed
notebook answers a statistics question with a shop-hours law in its retrieval pool.

**Already handled in the prose.** The task-12 write-up
(`srq1-holiday-enrichment-result-and-limitations.md`) was written so that no unverified
claim is asserted: the statute name and year are omitted, the XGBoost cause is described
without a mechanism citation, and Store Bededag is cited as observed in the fetched data
rather than as a legislative fact. Those paragraphs are safe to paste **now**; verifying
these five would let them be sharpened, not corrected.
