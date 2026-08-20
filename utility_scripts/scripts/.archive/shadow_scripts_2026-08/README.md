# Shadow scripts retired 2026-08-20

These five files duplicated scripts that also live under `03_thesis_modelling/`
and `04_thesis_results/`. P0035 F6 established `03_thesis_modelling/` as the
canonical tree and flagged these as stale; they were left in place then.

They were retired here after **verifying each one is genuinely superseded** — the
check P0040 required before archiving, so nothing unique was discarded.

## Verification, per file

| File | Canonical counterpart | Verdict |
|------|----------------------|---------|
| `srq1_shap.py` | `03_thesis_modelling/model_training/srq1/srq1_shap.py` | stale (67 vs 119 lines) |
| `srq1_calibration.py` | `03_thesis_modelling/model_training/srq1/srq1_calibration.py` | stale (72 vs 124) |
| `srq1_baselines_stat.py` | `03_thesis_modelling/model_training/srq1/srq1_baselines_stat.py` | stale (112 vs 129) |
| `generate_figures.py` | `04_thesis_results/generate_figures.py` | **byte-identical** |
| `srq2_agent.py` | *(none)* — already archived at `03_thesis_modelling/.archive/superseded_scripts_2026-08/` | superseded |

## Why the three `srq1_*` files are stale, not merely older

Every line unique to these copies is a **superseded pattern**, not unique work:

- `sys.path.insert(0, str(Path(__file__).resolve().parents[2]))` — the fixed-index
  root lookup that P0035 replaced with an upward search for `PATHS.py`. This broke
  in the 2026-08-19 reorganisation.
- `"holiday_month"` in the FEATURES list — renamed `peak_month`; the old name
  implied a holiday calendar that was never consulted.
- `"weighted_distribution"` in FEATURES — dropped from model inputs in `f4779a7`
  (worse accuracy in 3 of 4 categories).
- `{slug}_feature_matrix.parquet` — pre-H=3 filename; current matrices are
  `_feature_matrix_h3.parquet` per DEC-HORIZON.
- `np.log(...)` fitted against `np.expm1(...)` inversion in
  `srq1_baselines_stat.py` — the mismatched pair fixed in `5f2e9b7`.

Running any of them would have produced results against dropped features, a renamed
column and superseded matrices — or crashed on the path lookup.

## Why `generate_figures.py` was archived despite being identical

Byte-identical to `04_thesis_results/generate_figures.py`, so nothing is lost. It is
archived rather than kept because the canonical copy needs a **correction**: its
`fig4_ram_budget` is entirely hardcoded (a literal 512 MB "active ML model") against
a measured 3–4 MB. Leaving a second copy in place would let a future session fix one
and cite the other.

## Why `srq2_agent.py` was archived

No counterpart in the canonical tree: it was already archived to
`03_thesis_modelling/.archive/superseded_scripts_2026-08/srq2_agent.py`. It builds
on **LLM-as-Judge**, dropped by B-DEC-2 (all SRQ4 metrics are programmatic), and
targets `claude-sonnet-4-6`, superseded by `gpt-5.5-2026-04-23` per DEC-LLM. This
copy was simply a duplicate of an already-retired file.

## If you need these

Prefer the canonical versions. Recover from git history if genuinely required:

```bash
git log --follow -- utility_scripts/scripts/srq1_shap.py
```

## Related

- `.claude/rules/repo-tier-structure.md` — `utility_scripts/` is tooling-only,
  never thesis content
- `plans/P0035_2026-08-01_grain-artifact-removal/findings.md` F6 — canonical tree
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md` F34, F36
