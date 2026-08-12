# Archived tests — multi-agent-authored, superseded

Archived 2026-08-11 (P0036). Both files date from the earlier
"multiple agents write everything" approach and neither reflects current code.
Kept rather than deleted because they document what was attempted.

| File | Why archived |
|------|--------------|
| `test_agent_system_comprehensive.py` | **Ran, but asserted a defect was correct.** Reproduced `.ffill().bfill().fillna(0)` on `price_per_unit` (line 292) and asserted the result correct — "forward/backward filled". That `bfill` is the future-leakage bug fixed in `engineer_features.make_calendar` under P0036 task 5 (see F16). The test used its own mock frame and never imported the real module, so it neither broke nor affected any result — but it sat in `tests/` looking authoritative, exactly where someone would copy "how we handle gaps" from. |
| `test_builder_integration.py` | **Could not run at all.** Imports `thesis.thesis_production_system.agents.builder`, a package removed by the P0028 restructure (2026-07-11) when the `thesis/` path segment was flattened. Fails at import before any test executes; `importlib.util.find_spec("thesis")` returns `None`. Has been dead since July. |

## The transferable lesson

The first file is the more instructive failure. A test that *runs and passes* while
encoding a bug as intended behaviour is worse than a test that doesn't run: the
broken one announces itself, the passing one provides false assurance.

This mirrors the root cause of the `bfill` bug itself — `make_calendar`'s docstring
documented the cross-group leak thoroughly and was silent on future leakage, so
reviewers checked the documented risk and stopped. Both cases are the same shape:
**partial coverage reading as full coverage.**

## Related

- `plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/findings.md` — F16 (bfill fix, measurements, why it survived review)
- `02_thesis_data/_02_preprocessing/nielsen/_shared_modules/engineer_features.py` — `make_calendar()`, now ffill-only with both leakage kinds documented
- `.archive/thesis_agents_preintegration/` — the wider pre-integration agent tree these tests belonged to
