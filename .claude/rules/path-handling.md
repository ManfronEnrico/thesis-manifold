---
name: path-handling
description: RULE - Every filesystem path resolves through PATHS.py. Never hardcode a directory-name segment, never index Path(__file__).parents[N], never build a path from string literals of folder names.
category: governance
applies-to: [any .py that opens, writes, globs or imports by path]
triggers: [adding a file read/write, a script cannot find its input, a path broke after a folder rename, importing a sibling module by path]
created: 2026_09_10-14_40
updated: 2026_09_10-14_40
---

# Path handling — one source of truth is `PATHS.py`

The repo has been reorganised at least four times (P0028 tiers, the 2026-08-19
modelling split, the 2026-09-06 SRQ rename). Every reorganisation broke a path
that was written as a literal or as `parents[N]`, and each break was silent —
the script ran, `is_file()` returned False, and a stage "degraded" instead of
failing. `PATHS.py` exists so a rename is one edit, in one file.

## Quick Reference

| Situation | Wrong | Right |
|---|---|---|
| Repo root | `Path(__file__).parents[3]` | the root-finder already in the file, or `from PATHS import ROOT_DIR` |
| A tier / SRQ folder | `root / "04_SRQ4_Scenario_Experiment" / "scenario_setup"` | `from PATHS import SRQ4_SCENARIO_SETUP_DIR` |
| A results dir | `THESIS_RESULTS_DIR / "05_model_benchmark"` | `from PATHS import THESIS_RESULTS_SRQ1_DIR` (or `get_srq_tables_dir(...)`) |
| A per-category data dir | `engineered / "bymonth" / cat` | `from PATHS import get_category_engineered_bymonth_dir` |
| Path segment not in `PATHS.py` | invent a literal here | **add the constant/helper to `PATHS.py`**, then import it |

## The three banned patterns

1. **`Path(__file__).resolve().parents[N]`** for anything above the script's own
   directory. `N` is a distance that changes the moment the script moves a level
   deeper — which is exactly what the 2026-08-19 reorganisation did
   (`ModuleNotFoundError: No module named 'PATHS'`). If you need the repo root,
   use the upward-search-for-an-anchor pattern (`.env.example` / `PATHS.py`) that
   the well-behaved scripts already carry, or import `ROOT_DIR`.

2. **A directory-name string literal in a path expression** —
   `"04_SRQ4_Scenario_Experiment"`, `"05_model_benchmark"`, `"scenario_setup"`,
   `"bymonth"`, a lowercase category folder name. The literal encodes a fact
   (`where does SRQ4's harness live`) that `PATHS.py` already owns. When the fact
   changes, `PATHS.py` changes once; a literal has to be hunted for.

3. **A hardcoded category key that is really a folder name.** Category folders on
   disk are `CSD`, `Danskvand`, `Energidrikke`, `RTD` — capitalised. A dict
   `{"danskvand": ...}` used to build a path resolves to nothing on a
   case-sensitive filesystem and silently drops the category (F1, and its
   re-occurrences F6/F9 in P0053). Category → path always goes through a
   `get_category_*_dir()` helper; if you must keep a local dict, its keys match
   the on-disk casing exactly.

## When `PATHS.py` is missing what you need

Add it. `PATHS.py` is the correct place for a new path constant or
`get_*_dir()` helper — that is its entire job. A one-line addition there is
cheaper than every future rename hunting for your literal, and it means the next
script that needs the same path finds it instead of re-deriving it.

Deprecated aliases stay (see `THESIS_MODELLING_SCENARIO_DIR` →
`SRQ4_SCENARIO_SETUP_DIR`) so old imports keep working; new code uses the
current name.

## How to apply

- **Before writing any `open()`, `read_parquet()`, `glob()`, `write_text()`, or
  path-based `import`:** the path's parent comes from a `PATHS` import, not from
  `__file__` arithmetic or a folder-name literal.
- **When a script cannot find its input:** check whether it built the path by
  hand before assuming the input is missing. A `parents[N]` or a stale literal
  is the more common cause.
- **In review:** a `/` operator with a quoted folder name on its right-hand side
  is a finding. So is `parents[` followed by a digit `> 0`.

## See Also

- `PATHS.py` — the constants and `get_*_dir()` helpers; top-of-file docstring
  mirrors the tier map
- `.claude/rules/repo-tier-structure.md` — what each tier holds
- `.claude/rules/generated-artefact-provenance.md` — the sibling rule for the
  *values* in generated output (same "compute, don't hardcode" principle)
- `plans/P0053_2026-09-08_15-40_vps-hpc-model-training/findings.md` — F1, F6, F9
  are all this rule being violated
