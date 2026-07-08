# Step 1 — Workstream A: preprocessing.py "5-min fix" → 3 hidden problems

**Brian's plan said**: "change `parents[2]` to `parents[3]` in
`thesis/data/preprocessing/combined_scripts/preprocessing.py:24`. 5-min job."

**Reality**: 3 issues stacked on top of each other. None obvious from the
plan's framing.

## Finding 1 — Brian miscounted the parent levels

The file path on either OS:
- Windows (Brian): `C:\dev\thesis-manifold\thesis\data\preprocessing\combined_scripts\preprocessing.py`
- macOS (Enrico): `~/Desktop/Thesis Maniflod/thesis/data/preprocessing/combined_scripts/preprocessing.py`

| `parents[N]` | Resolves to |
|---|---|
| `[2]` | `thesis/data/` ← original (broken) |
| `[3]` | `thesis/` ← Brian's proposed fix (still broken — only contains the package, not the repo) |
| `[4]` | `Thesis Maniflod/` ← actual repo root ← **correct fix** |

Verified by direct `pathlib` introspection. Applied: `parents[2]` → `parents[4]`.

## Finding 2 — macOS case-insensitive filesystem hides the `thesis` package

After fixing Finding 1, `import thesis.data.nielsen.scripts...` still failed
with `ModuleNotFoundError: No module named 'thesis'`.

Root cause:
- Git tracked the directory as `thesis/` (lowercase). Brian's Windows setup
  created it lowercase, committed it, fine.
- On Enrico's macOS, an Obsidian vault `Thesis/` (capitalized) already
  occupied that filesystem slot. APFS is **case-insensitive but
  case-preserving** — both `thesis` and `Thesis` resolve to the same inode
  (verified: `stat -f '%i'` returns the same number for both).
- `os.listdir()` returns the canonical name (`Thesis`), so Python's import
  machinery looks for a `thesis` package, doesn't find one with that exact
  case, and gives up.

**Fix**: rename `Thesis/` → `thesis/` using a 2-step rename trick (required
on case-insensitive filesystems):

```bash
mv Thesis _temp_xyz
mv _temp_xyz thesis
```

This forces the filesystem to update its canonical-name registry. The
underlying inode (and all contents, including the Obsidian `.obsidian/`
config dir) stays untouched. Obsidian must be closed during the rename
otherwise the workspace state may corrupt.

Also created `thesis/__init__.py` (was missing) so Python recognizes the
directory as a regular package, not a namespace package.

## Finding 3 — `tabulate` not in venv

After Findings 1 and 2, `preprocessing.py` ran end-to-end (DB connect → pull
→ calendar → filter → engineer features → split, ~13 sec) but then crashed
on the report generation step:

```
ImportError: Missing optional dependency 'tabulate'.
```

The system Python had `tabulate` installed but the project `.venv/` did not.
The `.venv` doesn't even have `pip` — installed via `uv pip install tabulate`
into the venv directly.

## Verification (success)

```bash
$ python3 thesis/data/preprocessing/combined_scripts/preprocessing.py
Connecting to Nielsen... Connected.
Step 1/5 — Pulling raw data...     Raw rows: 3,789  |  Brands: 136
Step 2/5 — Building calendar...    Rows: 5,712
Step 3/5 — Filtering short...      77 brands kept
Step 4/5 — Engineering features... done
Step 5/5 — Applying split...       done
Done in 13.0s | Peak RAM: 7.9 MB
[markdown report printed]
Outputs written to results/phase1/
```

## Things to tell Brian

1. `parents[3]` was not the right fix — should be `parents[4]`. Likely an
   off-by-one from his manual counting.
2. Cross-platform filesystem case-sensitivity bug — affects any Mac
   contributor. Consider documenting in `tooling-issues.md`.
3. `tabulate` should be added to `pyproject.toml` (or `requirements.lock`)
   so it's deterministically installed by `uv sync`.
