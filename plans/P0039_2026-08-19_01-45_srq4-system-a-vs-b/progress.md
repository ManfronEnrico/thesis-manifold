---
pid: P0039
created: 2026-08-19 01:45:00
updated: 2026-08-19 01:45:00
---

# P0039 Progress

## Session 2026-08-19 (01:45) — plan created

Created at the end of the long 2026-08-18/19 session that finished the preprocessing
pipeline (P0038) and the serving interface (P0037 tasks 3, 4, 7). No P0039 task has
been started; this entry records the state the work begins from.

### Why this plan was opened

Every technical dependency of the thesis premise is now discharged except credentials.
The data pipeline is verified, the serving interface produces 230 traced forecasts, and
the horizon is decided. What remains is the experiment itself — and the writing.

### Established before starting (do not re-derive)

- The harness exists and is sound (F1). Read it before assuming anything needs
  building.
- The only blocker is `03_thesis_modelling/.env` (F2).
- E2B is billed by sandbox uptime; the repeated `pip install statsmodels` is the main
  fixed cost per run (F3).
- The vendor choice has **no recorded justification** anywhere in the thesis (F4). This
  is DEC-VENDOR and it blocks task 1.
- "Traceability" is the correct term and is now implemented; transparency and
  determinism are different properties (F5).
- Honest calibration made the intervals wide, which changes what System A should claim
  (F6).

### Decisions carried in

| Decision | Outcome |
|----------|---------|
| DEC-SCOPE-SRQ4 | CSD primary (most brands → most statistical weight), one category as robustness. Settled 2026-08-19. |
| DEC-VENDOR | **OPEN.** Brian favours GPT on ecological-validity grounds; the "cheaper and weaker" argument was rejected as indefensible. |

### Next action

**Task 1**: settle DEC-VENDOR, add `.env`, run `--demo`. That single run tells us
whether the remaining schedule is realistic.

### Standing constraint

Under a month to submission with 120 pages unwritten. Further EDA work is explicitly
out of scope — the pipeline is verified and its one remaining gap is reporting-level,
recorded as a limitation rather than fixed.
