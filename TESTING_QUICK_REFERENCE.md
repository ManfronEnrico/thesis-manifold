# Testing Quick Reference Card
> One-page cheat sheet for System A validation

---

## The One-Command Test

```bash
python tests/test_agent_system_comprehensive.py
```

**Expected time**: ~30 seconds  
**Expected result**: ✅ ALL TESTS PASSED

---

## What Gets Tested (10 Tests)

| # | Test | What It Checks | Status |
|---|------|---|---|
| 1 | State & Coordinator | LangGraph imports, 4 nodes present | ✅ Ready |
| 2 | Config Loading | RAM budget (8GB), LLM model, forecasting models | ✅ Ready |
| 3 | Agent Imports | All 4 agents (Data, Forecast, Synthesis, Validation) | ✅ Ready |
| 4 | Routing Logic | State transitions (error → end, normal → next) | ✅ Ready |
| 5 | Data Models | ModelForecast, SynthesisOutput, ValidationReport | ✅ Ready |
| 6 | Feature Engineering | lag_12 and price_per_unit computation | ✅ Ready |
| 7 | Metrics | MAPE, RMSE, MAE calculations | ✅ Ready |
| 8 | Ridge Stability | Log clipping prevents overflow | ✅ Ready |
| 9 | Graph Invoke | State transitions work end-to-end | ✅ Ready |
| 10 | Integration | All components work together | ✅ Ready |

---

## Success Path

```
Run Tests
   ↓
All 10 pass?
   ├─ YES → Sync 15 commits → Create PR → Notify Enrico → Phase 2
   └─ NO  → Debug → Fix → Re-run → Then sync
```

---

## Failure Path (Unlikely)

| If Test # Fails | Likely Cause | Fix |
|---|---|---|
| 1-3 | Import/path issue | Check ai_research_framework/ exists |
| 2 | Config values | Check config.py RAM_BUDGET_MB = 8192 |
| 4 | Routing changed | Check _should_continue_* functions |
| 6-7 | Math logic | Check forecasting_agent.py |
| 9 | Graph execution | Check coordinator.py compile() |

**Verdict**: All 15 commits are structural (skills, docs, refactoring) — **low risk of breakage**.

---

## Files to Know

| File | Purpose | Read When |
|------|---------|---|
| `PRE_SYNC_TEST_GUIDE.md` | 5-min overview | Before running tests |
| `TEST_EXECUTION_CHECKLIST.md` | Step-by-step | If you want structure |
| `agent_system_test_scenarios.md` | Detailed specs | If test fails, need details |
| `TEST_SUMMARY_2026-04-15.md` | Executive summary | For overview + risk |

---

## System A Structure (What's Being Tested)

```
ai_research_framework/
├── core/coordinator.py         ← LangGraph StateGraph
├── state/research_state.py      ← Shared state (TypedDict)
├── agents/
│   ├── data_assessment_agent.py
│   ├── forecasting_agent.py     ← 7 models (ARIMA, Prophet, Ridge, LGB, XGB, Ensemble)
│   ├── synthesis_agent.py       ← Ensemble + confidence
│   └── validation_agent.py      ← Final eval
└── config.py                    ← 8GB RAM budget, Claude Sonnet 4.6
```

**None of these were modified in 15 commits.** ✅ Safe to test.

---

## Pre-Test Checklist (30 seconds)

- [ ] In project root: `cd /c/Users/brian/OneDrive/Documents/02\ -\ A\ -\ Areas/MSc.\ Data\ Science/2026-03\ -\ CBS\ Master\ Thesis/CMT_Codebase`
- [ ] Test file exists: `ls tests/test_agent_system_comprehensive.py`
- [ ] Python works: `python --version` (3.9+)

---

## Command Cheat Sheet

```bash
# Run all tests
python tests/test_agent_system_comprehensive.py

# Test imports only
python -c "from ai_research_framework.core.coordinator import build_research_graph; print('✅ OK')"

# Check config
python -c "from ai_research_framework.config import RAM_BUDGET_MB; print(f'RAM={RAM_BUDGET_MB}')"

# Test agent creation
python -c "from ai_research_framework.agents import ForecastingAgent; ForecastingAgent(); print('✅ OK')"

# After tests pass, sync
git push origin Major_Refactor_2_Academic_Repos_NotebookLM
```

---

## Expected Test Output (Excerpt)

```
================================================================================
COMPREHENSIVE AGENT SYSTEM TEST SUITE (System A)
================================================================================

━━ TEST 1: State Initialization & Coordinator Import ━━
✅ ResearchState and build_research_graph imported
✅ ResearchState instance created
✅ build_research_graph() compiled successfully
✅ All expected nodes present: ['data_assessment', 'forecasting', 'synthesis', 'validation']

[... tests 2-10 ...]

================================================================================
TEST SUMMARY
================================================================================

  Test 1: ✅ PASS
  Test 2: ✅ PASS
  ... (all pass)
  
Result: 10/10 tests passed

✅ ALL TESTS PASSED — System A is stable!
   Ready to sync 15 commits and notify colleague.
```

---

## Timeline

| Step | Time |
|------|------|
| Pre-test checks | 1 min |
| Run test suite | 1-2 min |
| Evaluate results | 1 min |
| Git sync (if pass) | 1-2 min |
| Notify colleague | 2 min |
| **Total** | **~5 min** (if pass) |

If any test fails, add 5-10 min for debugging.

---

## Decision Tree

```
┌─ Run tests
│  └─ All 10 pass?
│     ├─ YES → Great! Proceed to sync
│     │        └─ git push origin Major_Refactor_2_Academic_Repos_NotebookLM
│     │        └─ Email Enrico: "Validation complete, ready to merge"
│     │
│     └─ NO → See failure diagnosis table
│            └─ Likely cause: import/config issue
│            └─ Debug with commands above
│            └─ Re-run tests after fix
│            └─ Then sync
```

---

## Key Fact

✨ **None of the 15 commits modify core agent logic.**

- ✅ Skills imported (isolated in .claude/skills/)
- ✅ Docs updated (docs/ only)
- ✅ Folders reorganized (no logic changes)
- ✅ State extended (ResearchState untouched)

**Confidence Level**: Very high that tests will pass.

---

## Questions?

- **What to test?** → See this card (you're reading it)
- **How to test?** → Run `python tests/test_agent_system_comprehensive.py`
- **What if it breaks?** → See failure table above
- **Details?** → See `agent_system_test_scenarios.md`

---

**Ready?** 

```bash
python tests/test_agent_system_comprehensive.py
```

**Good luck! 🚀**
