# Pre-Sync Test Guide — System A Validation
> Quick start guide for testing the old agent system before syncing 15 commits

**Status**: Ready to test  
**Date**: 2026-04-15  
**Target**: Validate System A (Enrico's LangGraph research framework) still works after refactoring

---

## Summary

You have **15 unpushed commits** that include:
- Skill imports (30 academic research skills)
- State extension (Phase 1 integration)
- Refactoring and folder reorganization
- Documentation updates

Before syncing, we need to **confirm the old agent system (System A) still works** using these test scenarios.

---

## Quick Start

### Run the Comprehensive Test Suite

```bash
cd /c/Users/brian/OneDrive/Documents/02\ -\ A\ -\ Areas/MSc.\ Data\ Science/2026-03\ -\ CBS\ Master\ Thesis/CMT_Codebase

python tests/test_agent_system_comprehensive.py
```

**Expected Output**:
```
✅ Test 1: PASS
✅ Test 2: PASS
✅ Test 3: PASS
✅ Test 4: PASS
✅ Test 5: PASS
✅ Test 6: PASS
✅ Test 7: PASS
✅ Test 8: PASS
✅ Test 9: PASS
✅ Test 10: PASS

Result: 10/10 tests passed
✅ ALL TESTS PASSED — System A is stable!
   Ready to sync 15 commits and notify colleague.
```

---

## What the Tests Validate

| Test | What It Checks | Pass Criteria |
|------|---|---|
| **Test 1** | State & Coordinator import | Can build LangGraph coordinator without errors |
| **Test 2** | Config loading | RAM budget, LLM model, forecasting models all set correctly |
| **Test 3** | Agent instantiation | All 4 agents (Data, Forecasting, Synthesis, Validation) can be created |
| **Test 4** | Routing logic | State transitions follow correct paths (error → end, normal → next phase) |
| **Test 5** | Data models | Output dataclasses (ModelForecast, SynthesisOutput, ValidationReport) instantiate |
| **Test 6** | Feature engineering | lag_12 and price_per_unit computed correctly for forecasting |
| **Test 7** | Metric calculations | MAPE, RMSE, MAE computed accurately |
| **Test 8** | Ridge stability | Log prediction clipping prevents overflow/underflow |
| **Test 9** | State transitions | Graph invokes and halts at expected interrupt points |
| **Test 10** | Full integration | All components work together without Nielsen data |

---

## If Tests Fail

### Common Issues & Fixes

| Error | Likely Cause | Fix |
|-------|---|---|
| `ModuleNotFoundError: ai_research_framework` | Path not in sys.path | Already handled in test script (auto-adds ROOT to path) |
| `ImportError: from langgraph` | LangGraph dependency missing | `pip install langgraph` |
| Test 2 fails (config mismatch) | .env file missing or incomplete | Add .env with Nielsen credentials (or skip if testing without data) |
| Test 3 fails (agent instantiation) | Config issue (missing .env vars) | Check config.py for required environment variables |
| Test 4 fails (routing returns wrong path) | Coordinator logic changed | Review `_should_continue_*` functions in coordinator.py |
| Test 9 fails (graph invoke hangs) | Checkpoint/interrupt issue | Try unique `thread_id` in config dict |

### Debug Steps

1. **Check imports first**:
   ```bash
   python -c "from ai_research_framework.core.coordinator import build_research_graph; print('✅ Imports OK')"
   ```

2. **Test config separately**:
   ```bash
   python -c "from ai_research_framework.config import RAM_BUDGET_MB; print(f'RAM_BUDGET_MB = {RAM_BUDGET_MB}')"
   ```

3. **Test agent instantiation**:
   ```bash
   python -c "from ai_research_framework.agents import ForecastingAgent; fa = ForecastingAgent(); print('✅ ForecastingAgent OK')"
   ```

4. **Run individual test**:
   ```bash
   python -c "from tests.test_agent_system_comprehensive import test_1_state_coordinator_import; test_1_state_coordinator_import()"
   ```

---

## Detailed Test Scenarios

For step-by-step test details, see: **[agent_system_test_scenarios.md](agent_system_test_scenarios.md)**

This file contains:
- Full test descriptions
- Expected outputs
- Code snippets you can run individually
- Pass/fail criteria for each test

---

## Post-Test Checklist

After **all 10 tests pass**:

- [ ] Run: `python tests/test_agent_system_comprehensive.py`
- [ ] Verify: All tests show ✅ PASS
- [ ] Log results: Document test results in `docs/testing/test_results_2026-04-15.md`
- [ ] Commit: `git add tests/test_agent_system_comprehensive.py docs/testing/`
- [ ] Push: `git push origin Major_Refactor_2_Academic_Repos_NotebookLM`
- [ ] Notify: Tell colleague (Enrico) System A is validated and sync is safe

---

## System A Overview (What We're Testing)

**File**: `ai_research_framework/`

```
ai_research_framework/
├── core/coordinator.py          ← LangGraph StateGraph orchestrator
├── state/research_state.py       ← Shared typed state (ResearchState)
├── agents/
│   ├── data_assessment_agent.py  ← Phase 1: Data quality check
│   ├── forecasting_agent.py      ← Phase 2: Model benchmarking (7 models)
│   ├── synthesis_agent.py        ← Phase 3: Ensemble + confidence scoring
│   ├── validation_agent.py       ← Phase 4: Final evaluation
│   └── test_evaluation.py        ← Test set evaluation
├── config.py                     ← 8GB RAM budget, LLM setup, Nielsen config
└── templates/                    ← Base configuration
```

**Key Constraints**:
- 8GB RAM budget (hard constraint for SRQ1 evaluation)
- Sequential model loading (one model in RAM at a time)
- Human-in-the-loop checkpointing at forecasting/validation phases
- Claude Sonnet 4.6 for synthesis recommendations

---

## Next Steps (After Tests Pass)

1. **Create PR**: Merge `Major_Refactor_2_Academic_Repos_NotebookLM` → `main`
2. **Notify Enrico**: "System A validation complete. 15 commits synced. Ready to integrate your changes."
3. **Phase 2 Planning**: Once merged, begin Phase 2 (architecture decisions / ADRs)

---

**Questions?** See CLAUDE.md or repository_map.md for full project context.
