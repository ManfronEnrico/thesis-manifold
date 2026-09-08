---
pid: P0052
created: 2026-09-08 14:45:00
updated: 2026-09-08 15:20:00
status: complete
completed: 2026-09-08 15:20:00
outcome_summary: "Chapter identity now derives from the document. CHAPTER_MAP (which encoded
  identity twice, by number and by title, and contradicted itself after the Ch5/Ch6 swap) is
  replaced by CHAPTER_SUBJECTS plus a Chapter-N prefix stripper; _slug() returns
  ch{N}-{subject} with both halves read from the heading. Drift pairs on subject alone, so
  sections-drafts/ never renames on a reorder. Verified against the live .docx: 17/17 headings
  resolved, zero warnings, the fictitious +/-1,8xx mirror pair gone, ch7 and ch8 present in the
  drift table for the first time, zero orphaned comment paths, all three guard rails still
  firing. Snapshot tracking also inverted to opt-in via shared_snapshot/. Acceptance test
  passes: a future chapter swap needs no code edit."
---

# P0052 — Snapshot export: dynamic chapter naming

> **Prerequisite reading:** `utility_scripts/scripts/thesis_snapshot.py` lines 87–120
> (`CHAPTER_MAP`) and 477–494 (`_slug`), then `PATHS.py` lines 160–210
> (`CHAPTER_SLUGS` / `CHAPTER_ORDER` / `_chapter_folder`) — which is the same
> problem, already solved correctly. **Copy that design, do not invent a new one.**

## The problem, in one measurement

Chapters 5 and 6 were swapped in Word on 2026-09-08. The exporter has not noticed,
and it fails **silently and in a way that looks like real data**:

| snapshot file | actually contains |
|---|---|
| `chapters/ch5-framework-design.md` | **Chapter 5 — Model Benchmark & Selection** |
| `chapters/ch6-model-benchmark.md` | **Chapter 6 — Predictive-Extension Architecture** |

Both filenames now name the *opposite* chapter's subject.

**The visible damage is in `MANIFEST.md`'s drift table**, which pairs each snapshot
chapter with a `sections-drafts/*.md` of the same slug:

```
| ch5-framework-design  | 2,923 | 4,738 | +1,815 |
| ch6-model-benchmark   | 3,991 | 2,153 | -1,838 |
```

Near-mirror deltas. That is not drift — it is the benchmark chapter being diffed
against the architecture draft and vice versa. The code's own comment says an
explicit map was chosen because *"a wrong pairing would report drift between two
unrelated chapters, which is worse than reporting none."* That is exactly what is
now happening.

## Root cause

`CHAPTER_MAP` encodes chapter identity **twice, in two incompatible ways**:

```python
"chapter 5": "ch5-framework-design",                    # by NUMBER
...
"predictive-extension architecture": "ch5-framework-design",  # by TITLE
```

Before the swap both agreed. After it they contradict, and `_slug()` resolves
longest-key-first, so **the number wins and the title loses**. Verified:

| heading in the document | `_slug()` returns | correct? |
|---|---|---|
| `Chapter 5 \| Model Benchmark & Selection` | `ch5-framework-design` | ✗ |
| `Chapter 6 \| Predictive-Extension Architecture` | `ch6-model-benchmark` | ✗ |
| `Model Benchmark & Selection` *(no prefix)* | `ch6-model-benchmark` | ✓ |
| `Predictive-Extension Architecture` *(no prefix)* | `ch5-framework-design` | ✓ |

Note the last two rows: **the title keys are still right.** Only the number keys are
wrong, and they are wrong *because* they encode a position that moved. The number is
not identity — it is a sort key that the document owns.

## The design to copy

`PATHS.py` already states the principle, and states it well:

> *"The slug names the SUBJECT and survives a renumbering; the prefix is only a sort
> key. Nothing in the codebase references a chapter number to build a path, so
> reordering `CHAPTER_SLUGS` is the whole edit."*

`CHAPTER_ORDER` is `{slug: i+1 for i, slug in enumerate(CHAPTER_SLUGS)}` — derived,
never typed. **The exporter must do the same, except that its order comes from the
document rather than a tuple**, because the document is what actually moved.

## Target behaviour

1. **Identity comes from the title**, never the number. `"Model Benchmark & Selection"`
   is a stable fact about a chapter; `"Chapter 5"` is a fact about its current position.
2. **Order comes from document position** — the sequence Heading 1s appear in.
3. **The `Chapter N` prefix is stripped before matching**, so both prefixed and bare
   headings resolve identically. (Ch1–6 have already dropped and regained the prefix
   once — seen 2026-09-05 — so both forms must keep working.)
4. **A reorder requires no code edit at all.** That is the acceptance test.
5. **A genuinely new or renamed chapter still warns**, loudly. The current
   `not in CHAPTER_MAP` warning is the only thing standing between a renamed heading
   and a silently-unpaired chapter; it must survive, not be traded away for flexibility.

## Phases

| # | Phase | Scope | Status |
|---|---|---|---|
| 1 | Reproduce and pin | failing test for the mispairing, before any fix | **done** |
| 2 | Title-keyed resolution | strip `Chapter N`, match on subject, derive order from position | **done** |
| 3 | Fix the four stale drafts | `ch7-synthesis` → `ch7-decision-synthesis`, +3 more | **done** |
| 4 | Renumber the sections tree | `09-ch5-…`/`10-ch6-…` prefixes follow document order | **done** |
| 5 | Guard rails | warn on unknown title; abort on two chapters claiming one slug | **done** |
| 6 | Re-export and verify | drift deltas plausible; filenames match contents | **done** |

---

## Phase 1 — Reproduce before fixing

Write the failing case first; it is three lines and it is what proves the fix.

```python
# the four headings currently in the document
assert _slug("Chapter 5 | Model Benchmark & Selection")      == "ch5-model-benchmark"
assert _slug("Chapter 6 | Predictive-Extension Architecture") == "ch6-architecture"
```

**Decide the naming convention here, once, and write it down** — see the open
question at the bottom, because it changes every filename in the snapshot.

## Phase 2 — Resolve by title, order by position

Replace the number keys with a **subject map** plus a prefix stripper:

```python
# Subject -> stable slug. NO chapter numbers: a number is a position, and
# positions move (Ch5/Ch6 swapped 2026-09-08). Keys match the lowercased
# heading with any "Chapter N" prefix and separator already removed.
CHAPTER_SUBJECTS = {
    "introduction":                       "introduction",
    "literature review":                  "literature-review",
    "methodology":                        "methodology",
    "data assessment":                    "data-assessment",
    "model benchmark":                    "model-benchmark",
    "predictive-extension architecture":  "architecture",
    "context-aware decision synthesis":   "decision-synthesis",
    "experimental evaluation":            "experimental-evaluation",
    "discussion":                         "discussion",
    "conclusion":                         "conclusion",
}

_CH_PREFIX = re.compile(r"^chapter\s+\d+\s*[|:\u2013\u2014-]?\s*", re.I)
```

Then `_slug()` strips the prefix and matches on what remains. **Keep the existing
longest-key-first ordering** — `"discussion"` is a substring of nothing here, but
`"conclusion"` and `"introduction"` share a suffix and future subjects may not be so
lucky.

**Order comes from the parse, not the map.** The chapter list is already built in
document order (`for ci, ch in enumerate(d["chapters"], 1)` at line 999), so the
position is in hand — it simply must not be baked into the identity.

⚠ **`CHAPTER_MAP` is consumed in four places**, not one. Grep before editing:
`_slug()` (line 486), the drift pairing, the unmapped-chapters warning (line 1329),
and `_write_comments`'s `slug_by_thread` (line ~1245). The comments tree pairs with
the chapters tree **by slug**, so a change in one and not the other silently
decouples `comments/sections/…` from `chapters/sections/…` — the exact pairing the
README advertises as the reason the section trees exist.

## Phase 3 — Four drafts whose names never matched

Independent of the swap, and it is why **ch7 and ch8 have never once appeared in a
drift table**:

| draft on disk | map expects |
|---|---|
| `ch7-synthesis.md` | `ch7-decision-synthesis` |
| `ch8-evaluation.md` | `ch8-experimental-evaluation` |
| `ai-declaration.md` | `ai-use-declaration` |
| `frontpage.md` | *(nothing — front matter, expected)* |

The README already flags this as a known trap: *"A chapter is missing from the drift
table → there is no matching `sections-drafts/<slug>.md`. **Ch7 and Ch8 currently
have none** — absence reads like agreement but isn't."*

**Rename the drafts to match** (they are the odd ones out; every other draft already
uses the long form). If phase 1 renames slugs wholesale, fold this in rather than
renaming twice.

## Phase 4 — The sections tree carries numbers too

`chapters/sections/09-ch5-framework-design/` — a **two-digit position prefix over a
slug that also contains a chapter number**. Same defect, second location: the `09-`
is correct (position 9 counting front matter) while `ch5` inside it is now wrong.

Derive the prefix from enumeration and let the slug carry only the subject:

```
09-model-benchmark/     (was 09-ch5-framework-design)
10-architecture/        (was 10-ch6-model-benchmark)
```

The numeric prefix already re-derives on every run, so **this folder tree
self-corrects once the slug stops carrying a number.**

## Phase 5 — Guard rails, so the next reorder is loud

Three, in ascending severity:

1. **WARN** — a Heading 1 whose subject is not in `CHAPTER_SUBJECTS`. Exists today
   (line 1329); keep it, retargeted at subjects. This is what catches a *renamed*
   chapter, which is the one case a title-keyed scheme genuinely cannot self-heal.
2. **ABORT** — two chapters resolving to the same slug. Already exists for filename
   collisions (*"two chapters share a filename"*); confirm it still fires.
3. **ABORT** — the existing 40 %-of-document guard. Untouched, but re-verify it fires
   after the refactor; it is what caught the 2026-09-05 restyle that merged six
   chapters into the Abstract.

**Record the order the document reported** in `MANIFEST.md`, so a future reorder is
visible in a diff rather than inferred:

```markdown
| # | subject | heading as written |
|---|---|---|
| 5 | model-benchmark | Chapter 5 \| Model Benchmark & Selection |
| 6 | architecture    | Chapter 6 \| Predictive-Extension Architecture |
```

## Phase 6 — Verify

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "dynamic-naming-check"
```

| check | expected |
|---|---|
| filename vs. content | every `chapters/<slug>.md` names its own subject |
| drift deltas | ch5/ch6 deltas plausible; **the ±1,8xx mirror pair is gone** |
| ch7 / ch8 | now **present** in the drift table (phase 3) |
| comments pairing | `comments/sections/<path>` mirrors `chapters/sections/<path>` |
| warnings | no `not in CHAPTER_MAP` for the ten real chapters |

**The real acceptance test is a hypothetical, and it should be written down as one:**
*if Ch7 and Ch8 were swapped tomorrow, would anything need editing?* The answer must
be no.

---

## Open question — decide before phase 1

**Do snapshot filenames keep a chapter number at all?**

| | `ch5-model-benchmark.md` | `model-benchmark.md` |
|---|---|---|
| reading order visible in `ls` | ✅ | ❌ (front matter interleaves) |
| survives a reorder | ❌ **still renames on every swap** | ✅ |
| matches `PATHS.py` | ❌ | ✅ (`CHAPTER_SLUGS` holds no numbers) |
| churn now | every draft + every doc link | same |

**Recommendation: drop the number from the slug and keep it in the sections-tree
prefix** (`09-model-benchmark/`), which is exactly `PATHS.py`'s `_chapter_folder()`
split — subject in the name, position in the prefix, number derived and never typed.

It also removes the trap this whole plan exists to fix, permanently: a filename
containing `ch5` is a claim about position that a file cannot keep.

**Cost is one-time and real**: `sections-drafts/*.md` all rename, and every internal
doc link to `ch5-framework-design.md` needs updating. Grep first —
`06_thesis_writing/writing-notes/` and `user-docs/` both reference these paths.

## Related

- `utility_scripts/scripts/thesis_snapshot.py` — `CHAPTER_MAP` (87), `_slug` (477),
  unmapped warning (1329), `_write_comments` slug pairing (~1245)
- `PATHS.py` lines 160–210 — **the design to copy**
- `06_thesis_writing/docx-exported-snapshots/README.md` — documents the inverted-filename
  trap and the ch7/ch8 drift absence
- `plans/P0048_…/findings.md` **F14** — the swap, and the 37 prose references it stranded
- `06_thesis_writing/writing-notes/ch5-ch6-swap-reference-repair.md` — the prose half,
  already staged; **independent of this plan**
- P0050 owns the *other* repo-side half of the swap (`PATHS.py` `CHAPTER_SLUGS` order,
  two results-folder renames, six diagram stems). **Do not do those here** — this plan
  is the exporter only.


---

## Outcome (2026-09-08 15:20)

All six phases complete. See `findings.md` F8-F12 and the progress log.

**The open question was decided by Brian**: keep the number in the filename, but derive it
from the document rather than typing it. That differs from this plan's own recommendation
(drop the number), and it required one design change the plan had not foreseen — the drift
table pairs on **subject alone**, so `sections-drafts/` holds `model-benchmark.md` and never
needs renaming when a chapter moves. Filename mirrors the document; pairing key does not.
See F9.

**Acceptance test passes.** `_slug("Chapter 8 | Context-Aware Decision Synthesis")` returns
`ch8-decision-synthesis` with no code change — a future swap renames the files by itself.

**Two follow-ups belong to other work, not here:**

- `writing-notes/ch5-ch6-swap-reference-repair.md:222` and `P0048/findings.md:305` still point
  at `sections-drafts/ch5-framework-design.md`, now `architecture.md`. Both are the parallel
  session's files.
- ~~`shared_snapshot/` is populated but uncommitted~~ **Superseded (F16):** all
  snapshots are gitignored outright; 326 files untracked. `shared_snapshot/` is
  obsolete and can be deleted.
