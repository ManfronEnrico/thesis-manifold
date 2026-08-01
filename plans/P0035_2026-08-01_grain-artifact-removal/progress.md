---
pid: P0035
created: 2026-08-01 00:00:00
updated: 2026-08-01 00:00:00
---

# P0035 — Progress Log

## 2026-08-01 — Plan created

- Verified `_03_engineered/bychain/` already deleted from disk; only `bymonth/` remains
- Found ~20 live files still referencing chain/region grain (paths, FEATURES, results, docs)
- Verified P0027's groupby leakage bug is already fixed (`group_keys` threaded throughout)
- Decided `group_keys` parameter stays — grain-capable, not grain-committed
- Flagged `utility_scripts/scripts/` vs `03_thesis_modelling/` duplication as a
  determine-canonical-first hazard
- Tasks 1–8 decomposed; nothing removed yet

## Session log

<!-- append: date, what ran, results, errors -->
