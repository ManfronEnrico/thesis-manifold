---
pid: P0052
created: 2026-09-08 14:45:00
updated: 2026-09-08 15:20:00
---

# P0052 — Findings

Everything below was **measured on 2026-09-08** against snapshot
`2026-09-08_14-05_chapter-reorder`. None of it needs re-deriving.

---

## F1 — The mispairing is already in production, and it looks like data

The drift table in the current `MANIFEST.md`:

```
| ch5-framework-design  | 2,923 | 4,738 | +1,815 |
| ch6-model-benchmark   | 3,991 | 2,153 | -1,838 |
```

Two near-mirror deltas. A reader scanning for "which chapter drifted most" is handed
the two most alarming numbers in the table, and **both are artefacts**. The benchmark
chapter is being diffed against the architecture draft and vice versa.

Every other row is plausible, which is what makes this dangerous: the table is not
obviously broken.

## F2 — `_slug()` resolution reproduced exactly

Ran the resolution order standalone (the script has import side effects, so this was
replicated rather than imported):

| heading | `_slug()` | correct |
|---|---|---|
| `Chapter 5 \| Model Benchmark & Selection` | `ch5-framework-design` | ✗ |
| `Chapter 6 \| Predictive-Extension Architecture` | `ch6-model-benchmark` | ✗ |
| `Model Benchmark & Selection` | `ch6-model-benchmark` | ✓ |
| `Predictive-Extension Architecture` | `ch5-framework-design` | ✓ |

**The title keys are still correct. Only the number keys are wrong.** `_slug()` sorts
keys longest-first, and `"chapter 5"` (9 chars) beats `"model benchmark"` (15)? No —
it does *not*, and that is worth stating precisely, because it explains why the bug
is subtle:

`_slug()` matches with `low.startswith(key)`. The heading begins `"chapter 5 | ..."`,
so **only the number key can match at position 0**. The title key never gets a chance,
regardless of length. Length ordering resolves ties among keys that *could* match, and
here there is only one.

**Consequence for the fix:** stripping the `Chapter N` prefix before matching is not a
convenience — it is the whole mechanism. Once stripped, the (correct) title keys match
and the (positional) number keys become unnecessary.

## F3 — `CHAPTER_MAP` has four consumers, not one

A fix touching only `_slug()` leaves three silent inconsistencies:

| line | consumer | what breaks if missed |
|---|---|---|
| 486 | `_slug()` | chapter filenames |
| ~1245 | `_write_comments` → `slug_by_thread` | **`comments/` decouples from `chapters/`** |
| 1329 | unmapped-chapter warning | the only alarm for a *renamed* chapter goes quiet |
| — | drift pairing (via slug) | the F1 mispairing |

The comments one matters most. The README advertises that
`comments/sections/<path>` and `chapters/sections/<path>` share a relative path so a
section and its objections pair exactly. That guarantee is **slug equality**, and
nothing enforces it structurally — it holds only because both call `_slug()`.

## F4 — PATHS.py already solved this, and says so

```python
# The slug names the SUBJECT and survives a renumbering; the prefix is only a
# sort key. Nothing in the codebase references a chapter number to build a path,
# so reordering CHAPTER_SLUGS is the whole edit.
CHAPTER_ORDER: dict = {slug: i + 1 for i, slug in enumerate(CHAPTER_SLUGS)}
```

`CHAPTER_SLUGS` contains **no numbers**: `"architecture"`, `"model_benchmark"`. The
number is derived from tuple position by `_chapter_folder()` and never written twice.

So the repo holds two solutions to one problem — a correct one in `PATHS.py` and a
broken one in `thesis_snapshot.py`. **This plan is a port, not a design exercise.**

The one difference to respect: `PATHS.py` gets order from a hand-maintained tuple,
because *it* defines the canonical order. The exporter must get order from the
**document**, because the document is the thing that moved.

## F5 — Four drafts have never matched, and ch7/ch8 have never been diffed

| draft on disk | `CHAPTER_MAP` expects | in drift table? |
|---|---|---|
| `ch7-synthesis.md` | `ch7-decision-synthesis` | **no** |
| `ch8-evaluation.md` | `ch8-experimental-evaluation` | **no** |
| `ai-declaration.md` | `ai-use-declaration` | no (front matter) |
| `frontpage.md` | — | no (expected) |

Confirmed: the drift table has 9 rows and contains **no ch7 or ch8 line at all**.

This predates the swap and is independent of it. The README already names the trap —
*"absence reads like agreement but isn't"* — which means it was known and not fixed.
Cheap to fix while the naming is being touched anyway.

## F6 — The sections tree encodes position twice

```
chapters/sections/09-ch5-framework-design/
                  ^^                ^^^
                  position          ALSO a position, now wrong
```

The `09-` prefix is derived per run and is **correct**. The `ch5` inside the slug is
typed and is **wrong**. Same defect as F2, second location.

Good news: because the prefix re-derives every run, this tree **self-corrects the
moment the slug stops carrying a number**. No migration logic needed.

## F7 — Both heading forms must keep working

`CHAPTER_MAP` carries title keys only because of an incident:

> *"Ch1-6 headings dropped their 'Chapter N -' prefix (seen 2026-09-05) and read as a
> bare title, so match on the title too."*

They have since regained it — the current document reads `Chapter 5 | Model Benchmark
& Selection`. So the prefix has been present, absent, and present again inside four
days. **A prefix-stripping matcher handles all three states with one code path**,
which is a second, independent argument for the phase 2 design.

Note the separator is a pipe (`|`) in the current document and was a hyphen before.
The stripper must accept `|`, `:`, `-`, en-dash and em-dash.

---

## F8 — Implemented. The measured before/after

Ran the real exporter against the live `.docx` after the fix
(`2026-09-08_15-09_dynamic-naming-verified`).

| | before | after |
|---|---|---|
| ch5 delta | **+1,815** | +712 |
| ch6 delta | **-1,838** | -805 |
| ch7 / ch8 | *absent from the table* | +115 / +281 |
| drift rows | 9 | **12** |
| warnings | — | none; all 17 headings resolved |

The mirror pair is gone, which is the signature the fix was aimed at. Filenames now name
their own subject: `ch5-model-benchmark.md` holds *Model Benchmark & Selection*.

## F9 — The drift pairing key had to change too, or the fix was half a fix

Naming by `ch{N}-{subject}` (Brian's decision: keep the number, derive it) would still have
renamed `sections-drafts/*.md` on every reorder — trading a wrong-content bug for a churn
bug.

So the two keys were deliberately split:

| surface | keyed on | why |
|---|---|---|
| snapshot filename | `ch{N}-{subject}` | mirrors the document, including its order |
| drift pairing | **subject alone** | a draft names a subject; subjects do not move |

`sections-drafts/` therefore holds `model-benchmark.md`, never `ch5-model-benchmark.md`.
This is the same subject/position split `PATHS.py` uses, applied to the pairing rather than
to the filename.

## F10 — Two draft H1s carried the pre-swap number, invisibly

`architecture.md` (ex-`ch5-framework-design.md`) opened `# Chapter 5 — Predictive-Extension
Architecture` while the document had moved it to 6. The filename was renamed by this plan;
the heading inside would have stayed wrong.

Fixed by **dropping the number** from those two headings rather than retyping it. A typed
number in a planning file is the same trap this plan exists to remove, and the document owns
the number now.

Content was verified before renaming — `architecture.md` genuinely holds architecture
material and `model-benchmark.md` genuinely holds benchmark material — so the rename was a
correction, not a second mispairing.

## F11 — Guard rails re-verified, not assumed

A refactor that silences an alarm is worse than the bug it fixed. All three were exercised
against the patched module:

| guard | fires |
|---|---|
| WARN on a subject absent from `CHAPTER_SUBJECTS` (a **rename**) | yes |
| ABORT on two chapters resolving to one slug | yes |
| ABORT on one chapter holding >40 % of the document | yes |

The rename warning matters most: title-keying self-heals a reorder but **cannot** self-heal a
rename, so it is now the only thing standing between a retitled chapter and a silently
unpaired one.

## F12 — Tracking inverted to opt-in

The `.gitignore` did the opposite of the intended model: `.archive/` was ignored while the
loose current snapshot was tracked. Now the whole folder is ignored except `shared_snapshot/`
and `README.md`, which Brian populates by hand.

Verified rather than assumed — `git add -n` on the populated `shared_snapshot/` reports
**325 files, 0 of them `.docx`**. The negation re-includes the folder, so the binary exclusion
must come *after* it in the file to win; it does.

The previously-tracked `2026-09-08_14-05_chapter-reorder` was `git rm --cached`-ed. It is the
snapshot carrying the mispaired filenames, so dropping it from the index also removes the
wrong artefact from view.

## F13 — Publishing copies the FOLDER, not its contents (a mistake made and corrected)

First attempt at populating `shared_snapshot/` ran `cp -r <snap>/* shared_snapshot/`,
which flattened the snapshot: `shared_snapshot/chapters/`, `shared_snapshot/MANIFEST.md`,
and no slug anywhere. Brian caught it.

What the slug carries is the snapshot's whole identity -- which `.docx`, exported when,
under what label -- and flattening discards all three. It also makes a *second* published
snapshot impossible, since the next one's loose `chapters/` would overwrite the first's.

Correct shape, verified:

```
shared_snapshot/
`-- 2026-09-08_15-43_dynamic-naming-verified/
    |-- MANIFEST.md
    `-- chapters/
```

The `.docx` exclusion already used `**/`, so it kept working at the deeper path
(confirmed with `git check-ignore`): 325 files staged, 0 binaries. But the README had the
flattening baked into its publish command as `Copy-Item -Recurse "$snap\*"` -- the
trailing `\*` is precisely the bug -- so the docs would have reproduced it. Both the
command and the tree diagram are corrected, with a note saying why not to flatten.

## F14 — Comment index tables now carry the anchored text

Brian (2026-09-08): every comment index must show the **first 5 and last 5 words of the
selected text**, so a thread can be found in Word by Ctrl-F.

The two index tables previously showed only `opens with` / `gist` -- the reviewer's own
words. That says what the objection *was*, not where in the thesis it *is*, and Word's
comment pane does not make the anchored passage greppable. Added `_anchor_locator()` and
an **on (first 5 … last 5 words)** column to both:

| table | file |
|---|---|
| per-chapter and per-section index | `comments/<slug>.md`, `comments/sections/**.md` |
| global thread index | `comments/INDEX.md` |

Head **and** tail, because a selection's boundaries identify it while the middle of a long
one is least distinguishing -- the same reasoning as `_anchor_excerpt`, at table scale.

**Short anchors return whole.** Head+tail on a 7-word anchor would print 5 words, an
ellipsis, then 5 words overlapping the first 5 -- longer than the original and lying about
what was selected. Below 2n words the text is returned unchanged.

## F15 — The index tables were already broken by unescaped pipes

Found by reading the rendered output rather than trusting the run: the *section* cell
holds a heading, and the headings read `Chapter 5 | Model Benchmark & Selection`. That
literal pipe closed the cell early, so the row silently gained a column and shifted tags,
replies and every later value one place right.

Pre-existing -- it arrived when the heading separator became a pipe -- and invisible until
the new anchor column made the misalignment obvious. A row that gains a column still
renders; nothing errors.

Fixed with `_md_cell()` on **every** text cell in both tables (chapter, section, tags
roll-up, gist), not only the ones added here. Two ordering details that matter:

1. **Truncate, then escape.** Escaping first lets a `[:28]` cut land inside `\|`, leaving
   a dangling backslash that escapes the cell-closing pipe -- reproduced at exactly 27
   characters of heading before the pipe.
2. Newlines are flattened too: a newline ends the *row*, not just the cell.

Verified structurally, not by eye: a column-count checker over the snapshot's
`comments/` tree confirms **153 tables, every row matching its header**.

## F16 — Superseded: snapshots are now gitignored outright

**F12 and F13 describe a tracking model that no longer exists.** Brian, 2026-09-08:
snapshots bloat source control and none should be committed.

The whole of `06_thesis_writing/docx-exported-snapshots/` is now ignored, except
`README.md` -- which is kept because it documents how to *run* the exporter and is the only
place that does. It is documentation that happens to live in the folder, not a snapshot.

326 files were untracked with `git rm -r --cached`; nothing on disk was touched. Verified:
`git add -n` on the whole folder now stages **0 files**.

Tracking was attempted twice and abandoned twice -- first every snapshot (1,306 files),
then one published folder under `shared_snapshot/`. The argument that ended it is the one
that was always true of both: a snapshot is regenerable output, and the prose's real
history is the `.docx`'s OneDrive version history.

**Consequence to keep in view:** a drift check now needs two exports kept **on disk**,
because git holds none. `.archive/` already serves this -- 7 snapshots at time of writing.
`shared_snapshot/` no longer has a purpose.

The naming work in F1-F11 and the anchor-locator work in F14-F15 are unaffected: both are
exporter behaviour, independent of whether output is committed.
