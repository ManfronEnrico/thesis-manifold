---
pid: P0034
created: 2026-08-01 00:00:00
updated: 2026-08-01 17:00:00
---

# P0034 — Progress Log

## 2026-08-01 — Plan created

- Ran metric grep across `05_thesis_writing/` — 13 hard-coded locations in 4 chapters
- Answered Enrico handover Q2: yes, extensive collision
- Surfaced F2: chain-grain removal is a structural rewrite of Ch6 tables, and danskvand's
  headline number worsens 22.0% → 23.8% from the grain decision alone
- Surfaced F3: derived deltas/ranges and the "≤15% target" qualitative claim are the
  easy-to-miss stale items
- Confirmed V2 already reflected in Ch6 §6.5.1 prose
- Tasks 1–7 decomposed; no prose changed

## Session log

### 2026-08-01 (session: P0034 — chapter numbers + Totalbeer)

**Setup**
- Created isolated worktree `worktrees/p0034-chapter-numbers` on branch
  `thesis/p0034-chapter-numbers-totalbeer`. Main repo left on `main`.
- Worktree creation hit repeated Windows friction (checkout timeout → stale
  `index.lock` → missing `.git` link → transient file lock). Resolved; see tooling
  note below. Worth logging via `/errors-log` before commit.

**Task 1 — inventory: COMPLETE**
- All 13 locations in the task_plan table verified accurate at stated file:line.
- Found 6 additional locations the plan missed — recorded as F8. Most consequential:
  `ch1-introduction.md:64` and `:88`, and `ch3-methodology.md:45`/`:47` carry the
  five-category framing (the plan only anticipated Ch3/Ch4).

**Totalbeer premise CORRECTED — see F7**
- Plan said "excluded on compute constraints (~10M rows)".
- `ch4-data-assessment.md:11` said the opposite: "absent from the source data … not a
  size or memory constraint".
- Brian confirmed 2026-08-01: *"not true, it does exist, just too large."*
- Verified on disk: `totalbeer_clean_facts_v.jsonl` = **20.31 GB** (vs CSD 11.39,
  energidrikke 3.64, danskvand 0.63). Totalbeer is 1.78× the largest worked category.
- ⇒ Ch4:11 is a **factual error to correct**, not just a count to trim. The "~10M rows"
  figure from the plan is unverified and must not be quoted; use measured file sizes.

**Dispatched to sub-agent (isolated worktree)**
- Tasks 2 (severity triage), 3+4 (Totalbeer removal + Ch4 correction), 5 (Ch6
  chain-grain structural rewrite), 8 (≤15% target verification).
- Output → `2026-08-01_DOC-prep-output.md`; new findings appended as F9+.
- Gate respected: no file under `05_thesis_writing/` is edited. Tasks 6/7 remain
  blocked behind task 9 pending P0032/P0033/P0035.

**Tooling note (for `/errors-log`)**
- Symptom: `git worktree add` on this repo exceeds the 2-minute Bash default and is
  killed mid-checkout, leaving a worktree that is registered but has no `.git` link
  file and cannot be repaired (`git worktree repair` → "not a valid path").
- Cause: ~1700-file checkout on the Z: drive; timeout kill leaves `index.lock` and a
  partial tree. Windows then intermittently reports "directory not empty" /
  "used by another process" on cleanup even with no process holding a handle.
- Fix: raise the Bash timeout for worktree creation; on failure remove the directory
  with `cmd /c rmdir /s /q` (PowerShell `Remove-Item -Recurse -Force` was less
  reliable), then `git worktree prune`, then recreate. Retry transient lock errors
  once before hunting for a holding process.

**Sub-agent returned — output verified by me, not taken on trust**

The completion notice warned the safety classifier was unavailable during the
sub-agent's review, so its claims were independently re-checked before being
recorded here. Verification performed:

| Check | Result |
|---|---|
| Gate held — any file under `05_thesis_writing/` modified? | **No.** `git status` shows only plan-folder files touched. |
| `2026-08-01_DOC-prep-output.md` exists and is substantive | Yes, 40 KB |
| Findings F9/F10/F11 appended | Yes |
| Task JSONs 2/3/4/5/8 → `completed`; 6/7/9 still `pending` | Confirmed |
| F10 quote from `ml_fmcg_demand_forecasting.md:21` | **Verbatim match** — "15–25% MAPE reduction over ARIMA baselines" |
| F10 `WARNING-CH6-02` in `compliance_report_20260315.md:254` | **Verbatim match** |
| F11 pre-registration wording at `ch3-methodology.md:39` | **Verbatim match** — "locked design decisions … prevent retroactive revision based on observed model performance" |
| F9 find-replace trap at `ch3-methodology.md:55` | **Confirmed** — "Five forecasting models … across the five Nielsen beverage categories" |

All spot-checked claims hold. F9/F10/F11 are treated as verified, not provisional.

**State at session end**

| Task | Status | Note |
|---|---|---|
| 1 — inventory | complete | +6 locations (F8) |
| 2 — severity triage | complete | in DOC-prep-output |
| 3 — Totalbeer removal diff | complete | drafted, not applied |
| 4 — Totalbeer justification | complete | must use measured GB, never "~10M rows" |
| 5 — Ch6 chain-grain rewrite | complete | drafted, not applied |
| 8 — ≤15% target verification | complete | **verdict: NOT FOUND — cut it** |
| 6 — swap in post-retrain numbers | **pending** | blocked by task 9 |
| 7 — package for Enrico | **pending** | blocked by task 9 |
| 9 — GATE | **pending** | holds until P0032 + P0033 + P0035 land |

Nothing has been applied to any chapter. All output is draft-only, inside the
plan folder, on branch `thesis/p0034-chapter-numbers-totalbeer`. Uncommitted.

**Three things that changed the shape of the plan**

1. **The ≤15% target has no source and cannot be re-sourced into validity** (F10).
   Two independent defects: the cited paper says "15–25% MAPE *reduction*"
   (relative), not "≤15% MAPE" (absolute); and separately the threshold is stated
   on MAPE while every figure compared to it is WMAPE. The second defect survives
   any re-sourcing, so the recommendation is to cut from all five sites rather
   than hunt for a citation. Open as `WARNING-CH6-02` since 2026-03-15.
2. **DEC-GRAIN contradicts a pre-registration claim** (F11). `ch3:39` promises no
   "retroactive revision based on observed model performance"; dropping the chain
   grain because it helped in only 1 of 4 categories is exactly that. Not fixable
   by quietly editing `ch3:39` — needs an openly reported protocol deviation.
   Highest examiner exposure in the plan.
3. **Ch4:11's beer-exclusion reason is factually wrong** (F7), confirmed by Brian
   and by measured file size (20.31 GB). "Absent at source" → "too large to
   compute" is a change from an external limitation to an owned scoping choice.

**Two risks carried forward, not yet actioned**

- **SeasonalNaive must be recomputed, not re-worded** (F10 in DOC-prep-output):
  the Ch6 baseline column is labelled "(chain)". A brand×month SeasonalNaive is a
  P0032/P0035 compute task, not a prose fix.
- **Sleeper**: energidrikke's +4.3 pp ML-vs-ARIMA delta is the thinnest margin in
  the table. If the leakage fix erodes it, the SRQ4 verdict could flip. Watch on
  P0032 completion.

**Open for Brian — Q1–Q7 in `2026-08-01_DOC-prep-output.md`**, none answered this
session. The two that block the most downstream work are the F11 handling choice
(open deviation vs. narrowed pre-registration) and whether Ch1:64's brand-count
range moves to an in-scope basis.

**Next session starts here**: answer Q1–Q7, then hold. Tasks 6/7 cannot start
until P0032/P0033/P0035 land.

<!-- append: date, what ran, results, errors -->
