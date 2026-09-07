---
name: eod
description: SKILL - End-of-day wrap-up. Documents session state into the active plan files, separates this session's changes from parallel sessions', drafts a commit, optionally writes a handover, then commits and pushes after explicit confirmation. Trigger on "/eod", "end of day", "wrap up the session", "let's close out".
compatibility:
  tools: [Bash, Read, Grep, Write, Edit, AskUserQuestion]
  requires: git repository with plans/ folder
---

# End-of-Day Wrap-Up

Six steps, in order. **Steps 1–4 are analysis and produce no side effects.**
Nothing is staged, committed or pushed before step 5's confirmation.

---

## Step 1 — Establish the git baseline

```bash
git branch --show-current
git log -1 --format="%H %ai %s"
git status --short | awk '{print $1}' | sort | uniq -c
```

**If on `main`**, say so and ask before proceeding — `.claude/rules/trigger-branch-strategy.md`
puts a feature branch per session at Trust tier. The user may still choose main;
that is their call, not a default.

### Verify deletions before anything else

A large `D` count is normal after a restructure and alarming otherwise. Prove
each deleted file still exists somewhere, rather than assuming:

```python
import subprocess, pathlib
out = subprocess.run(['git','status','--short'],capture_output=True,text=True).stdout
deleted = [l[3:].strip() for l in out.splitlines() if l.startswith(' D')]
names = {p.name for p in pathlib.Path('.').rglob('*') if p.is_file()}
missing = [d for d in deleted if pathlib.Path(d).name not in names]
print(f'{len(deleted)} deleted, {len(missing)} not found anywhere')
```

A non-zero `missing` count is a real deletion. Name those files explicitly to
the user before continuing.

---

## Step 2 — Separate this session from the others

**Assume the working tree is mixed.** Parallel sessions and other people commit
into the same repo, and a commit message describing work you did not do cannot
be verified by you or trusted by the reader.

For every modified file, ask: *did I touch this?* When unsure, look:

```bash
git diff --numstat -- <file>          # size of the change
git diff -- <file> | head -40         # is this my edit?
```

A 169-line change to a script you never opened is somebody else's session.

**Some files are genuinely mixed** — shared plan files especially, where you
appended a finding to a file another session also edited. These cannot be split
by path. Include them and **say so in the commit message**; do not pretend the
commit is cleaner than it is.

---

## Step 3 — Re-verify what the session changed

Do not trust that work done hours ago still holds. Two checks have each caught a
real break:

**Every producer still runs.**

```bash
for s in <producer scripts>; do
  python "$s" >/dev/null 2>&1 && echo "OK   $(basename $s)" || echo "FAIL $(basename $s)"
done
python PATHS.py >/dev/null 2>&1 && echo "OK   PATHS.py"
```

**Every path constant resolves.** `Path()` never validates, so a stale constant
fails at read/write time, not at import:

```python
import PATHS as P, pathlib
bad = [n for n in dir(P) if n.endswith('_DIR')
       and isinstance(getattr(P,n), pathlib.Path) and not getattr(P,n).exists()]
print('missing dirs:', bad or 'none')
```

**Every referenced artefact still resolves.** If paths moved this session,
re-resolve them from the file that cites them — a link repointed mid-session can
be repointed to a name that then changed again:

```bash
grep -oh '<results-dir>/[a-z_0-9/]*\.\(svg\|png\|md\|csv\)' <drafts>/*.md \
  | sort -u | while read p; do [ -f "$p" ] && echo "OK  $p" || echo "BROKEN  $p"; done
```

Fix anything broken **now**, before the commit — a broken link committed is a
broken link someone else has to diagnose.

---

## Step 4 — Write the state into the plan files

Plan files are the handover when session history is lost. Update the plan the
work belongs to (`plans/PLANS_INDEX.md` lists the active ones):

| File | What goes in |
|------|--------------|
| `progress.md` | a dated session entry: what was delivered, what was tried and rejected, near-misses |
| `findings.md` | numbered findings — reasoning, not just outcomes |
| `task_plan.md` | tick completed items; update phase status; refresh `focus_detail` |

**Record what failed, not only what worked.** A finding that lists seven
attempts and why each failed prevents the eighth. Findings that only state the
answer get re-derived.

**Update `focus_detail` in the frontmatter.** It is what the next session reads
first — make it say where things stand and what is next.

---

## Step 5 — Draft the commit, then confirm

Present the message as a code block **before staging anything**. Format per
`.claude/rules/trigger-git-commit-workflow.md`:

```
<type>: <imperative subject, ≤60 chars>

- <what changed and why, one line per logical unit>
- <...>
```

Then ask, in one `AskUserQuestion` call:

1. **Branch** — feature branch or the current one (only if on `main`)
2. **Scope** — exclude other sessions' files (default) or include everything
3. **Handover** — write one to `user-docs/handovers/` or rely on the plan files
4. **Handover slug**, if one is being written — offer three: the session title,
   a context-aware slug you propose (recommended — name the *change*, not the
   activity), or a slug the user supplies. Ask this only when a handover was
   chosen; do not burn a question on it otherwise.
5. **Push target** — **always ask, never assume.** The user's stated preference
   is remote `main`, but confirm it every time; a push is outward-facing and not
   easily undone.

---

## Step 6 — Stage, commit, push

**Stage by explicit path. Never `git add -A` or `git add .`** — that is how
another session's untracked files end up in your commit
(`.claude/rules/trigger-git-commit-workflow.md`, and the standing memory note).

```bash
git add <path1> <path2> ...
git status --short          # read it back before committing
git commit -m "$(cat <<'EOF'
<message>
EOF
)"
git push <remote> <branch>  # only the target the user confirmed
```

Report the commit hash and what was deliberately left uncommitted.

---

## Handover documents

Write one when the next reader is a *person* rather than a continuing session —
a collaborator, or yourself after an account switch. Place in
`user-docs/handovers/`, named `YYYY-MM-DD_<topic>-handover-<person>.md`, with the
frontmatter block those files use.

Cover, in this order: **where things are now**, **what to do differently when
adding code**, **what is enforced vs. remembered**, **near-misses**, and **what
is open and not yours to close**. Skip it when the plan files already say
everything and no person needs onboarding.

---

## Lessons this procedure encodes

Each of these came from a real end-of-day pass, not from theory:

- **247 deletions looked catastrophic and were all moves.** Verify before
  alarming the user — and before deleting anything yourself.
- **A folder that reappeared after a move held the *newer* files.** A benchmark
  had run mid-session and written through the old path. Compare timestamps
  before deleting something that "should" be empty.
- **Links repointed earlier in the same session were broken by a later rename.**
  Re-resolve every reference at the end, not when you first repoint it.
- **The working tree contained a parallel session's work**, including a 169-line
  change to a script this session never opened. Assume mixed; verify per file.
- **`git status` alone does not tell you who changed what.** The diff does.

---

## Related

- `.claude/rules/trigger-git-commit-workflow.md` — commit format, selective staging
- `.claude/rules/trigger-branch-strategy.md` — branch-per-session (Trust tier)
- `.claude/rules/workflow-planning-with-files.md` — plan file structure
- `.claude/rules/root-documentation-boundary.md` — where a handover may live
