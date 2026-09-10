---
name: re-snap
description: SKILL - Refresh every surface a prose pass verifies against, in one command - git fetch, thesis snapshot, Zotero re-pull, and a diff of what the author applied since last time. Run BEFORE writing any prose pass or follow-up note. Triggers - /re-snap, re-snap, refresh the snapshot, before the next prose pass.
category: workflow
applies-to: [thesis prose, writing-notes, chapter passes, follow-up notes]
triggers: [/re-snap, starting a chapter pass, writing a follow-up note, verifying a claim against the repo]
created: 2026_09_10-17_30
updated: 2026_09_10-17_30
---

# /re-snap — refresh every surface before writing

A prose pass verifies claims against **four moving surfaces**. All four can
change between one pass and the next, and each has produced a documented
failure when skipped.

| Surface | Moves when | Failure when stale |
|---|---|---|
| the `.docx` | the author applies fixes or adds comments | anchors quote text that no longer exists |
| the repository | the VPS or HPC pushes | a verified number changed hours ago |
| results artefacts | a re-run regenerates a table | a table pairing fresh structure with a stale number |
| the Zotero library | either author adds a source | a citation reported missing that exists |

**Run this before writing a pass or a follow-up. Every time. No exceptions for
"nothing has changed" — that is the assumption the check exists to test.**

---

## The four steps

### 1. Fetch, and read what landed

```bash
git fetch origin
git rev-list --left-right --count origin/main...HEAD   # behind / ahead
git log HEAD..origin/main --oneline
```

If anything is incoming, **read the commit messages before merging**. A commit
titled *"holiday + intermittency columns now reach the model"* tells you which
chapter it invalidates. Merge, then note the commit you verified against — "at
`3f8b0a9`", not "against the repository".

### 2. Snapshot the document

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<chapter>-<purpose>"
```

### 3. Diff against the previous snapshot

**This is the step that saves the most time**, and the one most often skipped:

```bash
cd 06_thesis_writing/docx-exported-snapshots
PREV=$(ls -1dt 2026-* | sed -n 2p); NEW=$(ls -1dt 2026-* | sed -n 1p)
diff <(sed 's/[[:space:]]\+/ /g' $PREV/chapters/<ch>.md) \
     <(sed 's/[[:space:]]\+/ /g' $NEW/chapters/<ch>.md) | cut -c1-220
```

Read it as three questions: **which fixes landed** (do not re-propose them),
**which were applied differently** (the author made a decision — respect it), and
**what did the author add that no note proposed** (new prose needs the same
verification as yours; an added citation needs a register row).

Also compare comment counts. A drop means threads were resolved; a rise means
new ones, and those carry the author's freshest thinking.

### 4. Re-pull Zotero, and query the API when a source is missing

```bash
python utility_scripts/scripts/zotero_client.py     # writes bibtex.bib, derives citations.json
```

⚠ **`citations.json` is filtered, not a mirror of the library.**
`zotero_client.py` keeps only `_SCHOLARLY_TYPES` — journalArticle, preprint,
book, bookSection, conferencePaper, report, document, thesis, magazineArticle,
newspaperArticle, webpage. **A `computerProgram`, `dataset`, `software`,
`blogPost` or `manuscript` entry is silently dropped.**

Measured 2026-09-10: a Nager.Date entry was added to Zotero as
`computerProgram`. The re-pull ran correctly, the export excluded it by type,
and the pass reported the citation as missing when it was there.

**So never conclude "not in the library" from `citations.json` alone.** Query the
API unfiltered:

```python
import sys; sys.path.insert(0, "utility_scripts/scripts")
from zotero_client import _load_env
from pyzotero import Zotero
env = _load_env()
z = Zotero(library_id=env["group_id"], library_type="group", api_key=env["api_key"])
for it in z.everything(z.top()):
    d = it.get("data", {})
    blob = f"{d.get('title','')}{d.get('creators','')}{d.get('url','')}".lower()
    if "<search term>" in blob:
        print(d.get("itemType"), "|", d.get("title"), "|", d.get("date"))
```

Search **whole words**. A substring match on a short term returns "management"
and "Manager" for "nager", which is noise that hides a real miss.

---

## What to write down

The note's frontmatter and opening name what was checked, so a reader can tell
what the verification was worth:

```yaml
snapshot: 2026-09-10_15-09_ch4-final
```

```markdown
Regenerated against `2026-09-10_15-09_ch4-final`. Zotero re-pulled the same
minute: 87 items. Repository at `5137ed4`, fetch clean.

## What you applied
<the diff, as a table: fix -> section -> state>
```

**"Verified against the repository" does not survive. "Verified at `5137ed4`,
87 items, snapshot 15-09" does.**

---

## Why this is a skill and not a checklist

It was written as four separate rules first — *Remote currency*, *Snapshot
currency*, *Library currency*, *Results currency* — and the steps were still
skipped, because each reads as advice at the moment you are about to write and
feel current.

A single command removes the judgement call. **There is no "is it worth
re-snapping?" decision to get wrong.**

---

## Related

- `.claude/rules/prose-insertion-discipline.md` — the four currency sections,
  and what an anchor must carry
- `.claude/rules/generated-artefact-provenance.md` — why a results number must
  be computed rather than transcribed (Correctness tier)
- `.claude/skills/write-prose-from-bullets/SKILL.md` — the pass itself, which
  this precedes
