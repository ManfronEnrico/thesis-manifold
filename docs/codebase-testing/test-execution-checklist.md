# Test Execution Checklist
> Step-by-step checklist to run and validate System A tests before sync

**Date**: 2026-04-15  
**Goal**: Confirm all 10 tests pass before syncing 15 commits  
**Estimated Time**: 5-15 minutes

---

## Pre-Test Verification

- [ ] **Navigate to project root**
  ```bash
  cd /c/Users/brian/OneDrive/Documents/02\ -\ A\ -\ Areas/MSc.\ Data\ Science/2026-03\ -\ CBS\ Master\ Thesis/CMT_Codebase
  ```

- [ ] **Verify test file exists**
  ```bash
  ls -l tests/test_agent_system_comprehensive.py
  ```
  Expected: File should exist and be ~15KB

- [ ] **Verify test documentation exists**
  ```bash
  ls -l docs/testing/agent_system_test_scenarios.md
  ls -l docs/testing/PRE_SYNC_TEST_GUIDE.md
  ```
  Expected: Both files should exist

- [ ] **Check Python version**
  ```bash
  python --version
  ```
  Expected: Python 3.9+ (likely 3.11)

- [ ] **Verify venv is activated** (if using one)
  ```bash
  python -c "import sys; print('venv OK' if 'venv' in sys.prefix.lower() or '.venv' in sys.prefix else 'warning: no venv detected')"
  ```

---

## Run Tests

- [ ] **Execute comprehensive test suite**
  ```bash
  python tests/test_agent_system_comprehensive.py
  ```

- [ ] **Watch for test output**
  - Look for 10 test sections (TEST 1 through TEST 10)
  - Each test should show ✅ PASS or ❌ FAIL
  - At bottom: "Result: X/10 tests passed"

---

## Evaluate Results

### ✅ All Tests Pass (Expected)

If you see:
```
Result: 10/10 tests passed

✅ ALL TESTS PASSED — System A is stable!
   Ready to sync 15 commits and notify colleague.
```

Then proceed to **Post-Test Actions** below.

### ⚠️ Some Tests Fail (Unexpected but Manageable)

If you see:
```
Result: X/10 tests passed

❌ SOME TESTS FAILED — Review errors above.
```

Then:

1. **Read the error messages** — scroll up to find which test failed and why
2. **Note the test number** (Test 1, 2, 3, etc.)
3. **Use debug steps** from `PRE_SYNC_TEST_GUIDE.md` section "If Tests Fail"
4. **Re-run after fixing** (or ask me for help)

---

## Post-Test Actions (If All Pass)

### Documentation

- [ ] **Create test results file**
  ```bash
  cat > docs/testing/test_results_2026-04-15.md << 'EOF'
  # Test Results — 2026-04-15
  
  **Status**: ✅ ALL PASS  
  **Date**: 2026-04-15  
  **Tester**: Brian Rohde  
  
  ## Results
  
  - Test 1 (State & Coordinator): ✅ PASS
  - Test 2 (Config Loading): ✅ PASS
  - Test 3 (Agent Imports): ✅ PASS
  - Test 4 (Routing Logic): ✅ PASS
  - Test 5 (Data Models): ✅ PASS
  - Test 6 (Feature Engineering): ✅ PASS
  - Test 7 (Metric Functions): ✅ PASS
  - Test 8 (Ridge Log Clipping): ✅ PASS
  - Test 9 (State Transitions): ✅ PASS
  - Test 10 (Integration): ✅ PASS
  
  **Total**: 10/10 PASS
  
  ## Conclusion
  
  System A is stable after 15 commits of refactoring, skill imports, and state extensions. Safe to sync.
  EOF
  ```

### Git Operations

- [ ] **Stage test files**
  ```bash
  git add tests/test_agent_system_comprehensive.py
  git add docs/testing/
  ```

- [ ] **Verify staging**
  ```bash
  git status
  ```
  Expected: Files should show under "Changes to be committed"

- [ ] **Commit test infrastructure** (optional, before syncing 15 commits)
  ```bash
  git commit -m "docs(testing): add comprehensive system A validation suite"
  ```

### Sync

- [ ] **Push branch to remote**
  ```bash
  git push origin Major_Refactor_2_Academic_Repos_NotebookLM
  ```
  Expected: No errors, shows branch is pushed

- [ ] **Verify push succeeded**
  ```bash
  git log --oneline -1
  git remote -v show origin
  ```

### Notification

- [ ] **Notify colleague (Enrico)** via email/Slack:

  > **Subject**: System A Validation Complete — Ready to Sync
  > 
  > Hi Enrico,
  > 
  > I've completed comprehensive validation of your original LangGraph agent system (System A) after 15 commits of refactoring and skill imports.
  > 
  > **Test Results**: ✅ 10/10 tests pass
  > - State & coordinator initialization
  > - Config loading (8GB RAM budget, LLM setup)
  > - All 4 agent imports (Data, Forecasting, Synthesis, Validation)
  > - Routing logic and state transitions
  > - Data models and feature engineering
  > - Metric calculations
  > - Ridge model stability
  > - Full integration check
  > 
  > **Conclusion**: Your agent system is stable. Safe to sync 15 commits and merge.
  > 
  > **Next Steps**: Merge `Major_Refactor_2_Academic_Repos_NotebookLM` → `main`, then we can begin Phase 2 planning (ADRs).
  > 
  > Test documentation: [repo]/docs/testing/agent_system_test_scenarios.md
  > 
  > Best,
  > Brian

---

## Failure Diagnosis (If Needed)

### Test 1 Fails (State & Coordinator)

**Symptom**: "ModuleNotFoundError" or "Cannot import ResearchState"

**Fixes** (in order):
1. Check path: `ls ai_research_framework/state/research_state.py`
2. Check imports: `python -c "from ai_research_framework.state.research_state import ResearchState"`
3. Check coordinator: `python -c "from ai_research_framework.core.coordinator import build_research_graph"`

### Test 2 Fails (Config)

**Symptom**: "RAM_BUDGET_MB != 8192" or "KeyError" in config

**Fixes**:
1. Check config file: `cat ai_research_framework/config.py | head -30`
2. Verify RAM constant: `python -c "from ai_research_framework.config import RAM_BUDGET_MB; print(RAM_BUDGET_MB)"`
3. Check .env if needed: `ls -la .env`

### Test 3 Fails (Agent Imports)

**Symptom**: "Cannot import DataAssessmentAgent" or similar

**Fixes**:
1. Check agents exist: `ls ai_research_framework/agents/*.py`
2. Check __init__.py: `cat ai_research_framework/agents/__init__.py`
3. Test each agent individually

### Test 4 Fails (Routing)

**Symptom**: "AssertionError" on routing decision

**Fixes**:
1. Check coordinator logic hasn't changed: `grep -A 5 "_should_continue_after_data" ai_research_framework/core/coordinator.py`
2. Verify routing functions are exported
3. Test state dict structure

### Test 9 Fails (Graph Invoke)

**Symptom**: "Halted before forecasting" error or timeout

**Fixes**:
1. Expected behavior (graph halts at interrupt points)
2. Use unique thread_id in config dict
3. Check if langgraph MemorySaver is working

### Test 10 Fails (Integration)

**Symptom**: Multiple failures or combined error

**Fixes**:
1. Run tests 1-9 individually to isolate issue
2. Check if it's a cascading failure from earlier test
3. Verify all components import independently

---

## Success Verification

- [ ] **All 10 tests show ✅ PASS**
- [ ] **No error messages or warnings** (except expected langgraph logs)
- [ ] **Final summary shows**: "Result: 10/10 tests passed"
- [ ] **Green success message**: "✅ ALL TESTS PASSED"

---

## If Everything Passes

You're ready to:
1. ✅ Sync the 15 commits
2. ✅ Create a PR to main
3. ✅ Notify Enrico that validation is complete
4. ✅ Begin Phase 2 (Architecture decisions)

---

## If Something Breaks

1. **Don't sync yet** — test failures indicate something changed unexpectedly
2. **Review the error** in the test output
3. **Use the diagnosis table above** to identify the root cause
4. **Check which commit introduced it** (if not obvious)
5. **Fix or revert that commit**
6. **Re-run tests**
7. **Then sync**

---

## Reference Files

- **Full test specs**: `docs/testing/agent_system_test_scenarios.md`
- **Quick guide**: `docs/testing/PRE_SYNC_TEST_GUIDE.md`
- **This checklist**: `docs/testing/TEST_EXECUTION_CHECKLIST.md`
- **Summary**: `TEST_SUMMARY_2026-04-15.md` (root of project)

---

**Ready?** Start with the **Pre-Test Verification** section above, then run the tests!

Questions: Check `PRE_SYNC_TEST_GUIDE.md` or ask me.
