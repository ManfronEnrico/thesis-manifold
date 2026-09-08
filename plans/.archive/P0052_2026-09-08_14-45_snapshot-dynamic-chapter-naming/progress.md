---
pid: P0052
created: 2026-09-08 14:45:00
updated: 2026-09-08 15:20:00
---

# P0052 — Progress log

## 2026-09-08 14:45 — Plan created (investigation only, no code changed)

**Trigger:** the Ch5/Ch6 swap landed in Word earlier the same day (P0048 F14). While
staging the 37 prose cross-reference repairs, the exporter was found to have silently
mispaired the two chapters.

**Done in this session:**

- Reproduced `_slug()`'s resolution against the four live heading forms (F2)
- Traced all four `CHAPTER_MAP` consumers (F3)
- Confirmed the drift table is actively reporting the mispairing as data (F1)
- Found the pre-existing ch7/ch8 drift absence and its cause (F5)
- Identified `PATHS.py` as the already-correct implementation to port (F4)
- Wrote the six-phase plan

**NOT done — deliberately.** No code was changed. The exporter is working "well
enough to mislead", which is a reason to fix it carefully in a session that owns it,
not to patch it mid-way through a prose pass.

**State of the world right now:**

| | status |
|---|---|
| Word `.docx` | swapped, correct |
| Snapshot filenames | **inverted** — documented in the snapshot README |
| Prose cross-references | 37 repairs staged, verified, not yet pasted |
| `PATHS.py` / results folders / diagram stems | **not done** — P0050 |
| Exporter naming | **not done** — this plan |

## Next session — start here

1. Read `task_plan.md`'s **Open question** and decide it first. It determines every
   filename in the snapshot, and deciding it late means renaming twice.
2. Write the phase 1 assertions before touching `_slug()`.
3. Grep `CHAPTER_MAP` (F3) — four consumers, and the comments-tree one is the one that
   fails silently.

**Do not** fold in P0050's half (folder renames, diagram stems) — different plan, and
the two do not interact.

---

## 2026-09-08 15:20 — Implemented, all six phases

**Decision taken first** (the open question at the foot of the plan): Brian chose to **keep
the chapter number in the filename but derive it**, rather than dropping it. Both halves are
read from the heading Word rendered, so a reorder renames the files by itself.

That decision forced one design change the plan had not anticipated: the drift table had to
pair on **subject alone**, or `sections-drafts/` would still churn on every reorder. See F9.

**Delivered**

- `thesis_snapshot.py`: `CHAPTER_MAP` -> `CHAPTER_SUBJECTS` + `_CH_PREFIX` + `_subject()`;
  `_slug()` returns `ch{N}-{subject}`; all four consumers updated
- `MANIFEST.md` gained a *Chapter order as the document reports it* table, so a future
  reorder is a one-line diff instead of an inference
- `sections-drafts/`: 11 files renamed to subject-only names; two stale H1 numbers dropped
- `.gitignore`: snapshot tracking inverted to opt-in via `shared_snapshot/`
- `docx-exported-snapshots/README.md`: tracking model, publish procedure and four
  troubleshooting rows rewritten

**Verified** (not assumed)

- 13 slug assertions pass, including the acceptance test — *if Ch7 and Ch8 were swapped
  tomorrow, would anything need editing?* No.
- Live export: 17/17 headings resolved, **zero warnings**, mirror pair gone, ch7/ch8 now
  present (F8)
- Comments tree: **zero orphaned paths** against the chapters tree — the slug-equality
  guarantee the README advertises still holds (this was F3's main risk)
- All three guard rails still fire (F11)
- `git add -n` on `shared_snapshot/`: 325 files, 0 `.docx` (F12)

**Near-miss.** Content was checked *before* renaming the drafts, not after.
`ch5-framework-design.md` -> `architecture.md` was only correct because that file really did
hold architecture material; renaming on the filename's own claim would have re-created the
exact bug being fixed.

**Left for Brian**

- `shared_snapshot/` is populated but **not committed** — publishing is his call, and the
  branch question is open (currently on `main`).
- Two live docs still point at renamed drafts:
  `06_thesis_writing/writing-notes/ch5-ch6-swap-reference-repair.md:222` and
  `plans/P0048_.../findings.md:305` both say `sections-drafts/ch5-framework-design.md`, now
  `architecture.md`. **Both belong to the parallel session's swap-repair work**, so they were
  flagged rather than edited. Dated handovers and research-question files mentioning the old
  names were deliberately left alone — they are historical records.
