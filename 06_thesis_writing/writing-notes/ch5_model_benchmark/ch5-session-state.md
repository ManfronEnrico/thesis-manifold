---
name: ch5-session-state
description: NOTE - Where the Chapter 5 prose pass stands as of the 2026-09-11 re-snap, what the four surfaces say, and the four-step order for the rest of it. Written to survive a context compact.
category: workflow
applies-to: [chapter 5]
created: 2026_09_11-13_30
updated: 2026_09_11-13_30
status: live
---

# Chapter 5 prose pass - where we are

**Re-snapped 2026-09-11 13:21.** All four surfaces checked.

| Surface | State |
|---|---|
| remote | **level**, 0 behind 0 ahead. Nothing incoming |
| snapshot | `2026-09-11_13-21_ch5-prose-session`. Document grew 34,441 -> **37,594 words** |
| results | unchanged since the pass was verified at `303f00f` |
| Zotero | re-pulled, **87 items**, unchanged |

## Sections 5.0 to 5.2.1 are already applied

Seven diff hunks, and **three comments closed** (199, 201, 204). Chapter 5's
thread count went 49 -> 46.

| Section | State |
|---|---|
| 5.0 title | ✅ subtitle applied |
| 5.1 Rationale | ✅ prose, and **the RAM figure is settled at 4 GB** |
| 5.2.1 Simple benchmarks | ✅ prose |
| **5.2.2 ARIMA onward** | ⬜ still bullets - **resume here** |

⚠ **The 4 GB question is answered.** Section 5.1 now reads "the 4 GB sequential
memory budget". Section 5.5.6 still says 8 GB, so **5.5.6 is the one to change**
when the pass reaches it. The follow-up's `[4 or 8]` placeholder is resolved.

**Everything from 5.2.2 down in `ch5-prose-pass-followup-01.md` still applies
verbatim** - the prose below that point has not moved, so every anchor holds.

## The book is now local

`C:\Users\brian\Downloads\Hyndman Book (2021)` - 42 PDFs, one per section.
Read from there rather than Google Drive.

⚠ **Quote from where the answer is, not from page 1.** The first pass read six
sections in full but quoted almost entirely from their opening pages, because
that is where a section states its thesis and the reading stopped once a usable
quote appeared. Section 12.2's strongest sentence for this thesis is on its last
page.

## The order for each remaining section

1. **Read what the Word file says**, then its comments, and **verify both against
   the repository**. The follow-up did this at `303f00f`; re-check anything a
   fetch shows has moved.
2. **Check the book PDFs** for a section that supports what we did, and cite it
   in text.
3. **Work around what exists.** We are not re-inventing the training process at
   this stage, so argument and citation adapt to the models as trained. Where the
   literature suggests we should have done something differently, that is a
   limitation to state, not a re-run to schedule.
4. **Record what a re-run would buy**, separately, as an optional note. Insight
   from the book about what we would gain and what we lose by not doing it -
   explicitly optional, and probably not affordable.

## Enrico's handover, validated 2026-09-11

All four items check out. Recorded as **S17 to S20** in
`deferred-structural-decisions.md` - he said S18-S21, but the list only ran to
S16, so they are numbered from 17.

| Item | Verdict |
|---|---|
| calibration fits XGBoost where two categories serve LightGBM | ⚠ **correct** - and subtle, see below |
| profiling / retraining tables pre-date the retraining | ✅ **correct**, `profiling.csv` is dated 2026-09-01, says 13 features |
| the confidence index is dead | ✅ **correct**, and worse than he said |
| Chapter 7 rewritten | ✅ present in the snapshot under the new title |

### The calibration item is right for a non-obvious reason

Selecting on **test WMAPE** gives XGBoost in all four categories, which makes the
claim look wrong. But `train_and_persist.best_model_for()` deliberately selects on
the **cross-validation** score, because selecting on test is selection on the
evaluation set. On CV, energidrikke and RTD pick LightGBM - exactly the two he
named.

**Do not "fix" this by switching selection to test.** The code carries the
reasoning in its own comments.

### The confidence index has two defects, not one

`forecast_tool.py:473`. The relative width reduces to `2·sinh(q90)`, so the
forecast value cancels and **the first term is a per-category constant**. The
second term, `1 - min(q90, 1)`, is **identically zero** for every category, since
implied q90 runs 2.17 to 3.52.

So every forecast scores 2 to 6 and tiers "Low". **Recalibrating the cut-offs
does not fix it** - re-tiering a per-category constant yields four values, one per
category. Recommendation in S18 is to drop the field, and to report that as an
SRQ2 finding rather than an omission.

## What this session must not lose

- **5.5.6 changes to 4 GB**, not the other way round.
- The follow-up's `[4 or 8]` placeholder is **resolved**.
- Resume at **5.2.2**.
- Comment **225** (`OUTDATED` on the validation scheme) is still unexplained and
  still needs Brian.
