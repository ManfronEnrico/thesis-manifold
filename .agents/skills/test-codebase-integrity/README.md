# test-codebase-integrity Skill

**Purpose**: Comprehensive integration testing for the entire CMT thesis codebase.

**Trigger phrases**:
- "test codebase integrity"
- "validate system integrity"
- "run full integration tests"
- "check codebase health"
- "test agents" / "test forecasting" / "test coordination" / "test data models"
- "ensure system stability"

## Quick Start

### Full Validation (Before Syncing Commits)

```
User: "Before I push, test codebase integrity"
Skill: Prompts "Which module? (all/agents/forecasting/coordination/data_models)"
User: "all"
Skill: Runs 10 tests, shows results, GO/NO-GO decision
```

### Module-Specific Testing

```
User: "Test agents—I think I broke something in imports"
Skill: Runs tests 1, 3, 10 (agent-specific) + remediation if failures
```

```
User: "Validate forecasting after my feature engineering changes"
Skill: Runs tests 6, 7, 8 (forecasting-specific)
```

## What It Tests

| Test # | Name | Module | Coverage |
|--------|------|--------|----------|
| 1 | State & Coordinator Import | agents | LangGraph imports, 4 nodes |
| 2 | Config Loading | coordination | RAM budget, LLM setup, configs |
| 3 | Agent Imports | agents | All 4 agents instantiate |
| 4 | Routing Logic | coordination | State transition rules |
| 5 | Data Models | data_models | Dataclasses instantiate |
| 6 | Feature Engineering | forecasting | lag_12, price_per_unit |
| 7 | Metric Functions | forecasting | MAPE, RMSE, MAE |
| 8 | Ridge Log Clipping | forecasting | Numerical stability |
| 9 | State Transitions | coordination | End-to-end graph execution |
| 10 | Full Integration | agents | All components together |

## Output Format

**For each test:**
- Test name + pass/fail status
- (If failed) Error type, root cause, remediation steps

**Summary:**
- Pass/fail count
- Execution time
- **GO/NO-GO decision** (safe to sync? yes/no)

## Module Filter Options

- **all** — Run all 10 tests (default, recommended for pre-sync validation)
- **agents** — Tests 1, 3, 10 (import chains, agent instantiation)
- **forecasting** — Tests 6, 7, 8 (feature engineering, metrics, stability)
- **coordination** — Tests 2, 4, 9 (config, routing, state transitions)
- **data_models** — Test 5 (dataclass instantiation)

## Example Output

```
COMPREHENSIVE CODEBASE INTEGRITY VALIDATION
================================================================================

Module Filter: ALL
Tests to run: 10

Test 1: State & Coordinator Import         ... [PASS]
Test 2: Config Loading                     ... [PASS]
Test 3: Agent Imports                      ... [PASS]
Test 4: Routing Logic                      ... [PASS]
Test 5: Data Models                        ... [PASS]
Test 6: Feature Engineering                ... [PASS]
Test 7: Metric Functions                   ... [PASS]
Test 8: Ridge Log Clipping                 ... [PASS]
Test 9: State Transitions                  ... [PASS]
Test 10: Full Integration                  ... [PASS]

================================================================================
SUMMARY
================================================================================
Result: 10/10 PASS
Time: 23.45s

================================================================================
GO FOR SYNC: All tests pass. Ready to merge and sync.
```

## When to Use

- **Before merging a branch**: Validate System A/B agents still work
- **After refactoring agents**: Check import chains
- **After changing forecasting models**: Validate features and metrics
- **After state machine edits**: Check routing and transitions
- **Before pushing commits**: Full suite for safety
- **In CI/CD pipelines**: Automated pre-merge validation

## Files

- `SKILL.md` — Skill definition + detailed documentation
- `scripts/test_runner.py` — Core test execution engine
- `evals/evals.json` — Evaluation test cases for skill validation
- `README.md` — This file

## Implementation Details

The skill bundles a Python test runner (`test_runner.py`) that:
- Imports 10 test functions with module-specific filters
- Captures stdout, stderr, and timing data
- Provides color-coded output with remediation suggestions
- Returns exit codes: 0 = all pass, 1 = some fail

## Known Limitations

- Tests are integration-level, not unit tests
- Some tests require actual file imports (not mocked)
- Feature engineering tests assume standard Nielsen/Indeks data structure
- Numerical stability tests use default Ridge model configuration

## Future Enhancements

- Add unit test runner for specific functions
- Integrate with CI/CD pipelines (GitHub Actions, GitLab CI)
- Add performance benchmarking (track test speed regressions)
- Create side-by-side branch comparison (pre-refactor vs post-refactor)
- Generate test coverage reports
