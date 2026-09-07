# Pre-fix stability baseline (2026-08-24)

Snapshot taken 2026-09-07, **before** `srq1_stability.py` was re-run under the F18
determinism fix (`XGB_N_JOBS = 1`).

These files were produced with `n_jobs=-1`, so their XGBoost rows carry
**seed variation AND thread-count variation combined**. That matters more here than
in any other table: stability's entire purpose is to quantify seed sensitivity, and
it has been attributing thread noise to seeds.

Kept as the comparison point for whether the stability *verdict* changes, not merely
its digits. A narrowed XGBoost spread after the fix would mean the previously reported
seed sensitivity was partly an artefact — a finding, not a correction.

Superseded for all reporting purposes by the regenerated tables.
