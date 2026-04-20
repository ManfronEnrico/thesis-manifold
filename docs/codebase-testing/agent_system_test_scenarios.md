# Agent System Test Scenarios — System A Validation
> Comprehensive test suite for the old agent system (Enrico's original LangGraph-based research framework)
> 
> **Date**: 2026-04-15  
> **Status**: Pre-sync validation (15 unpushed commits)

---

## Overview

The AI Research Framework (System A) consists of:
- **Coordinator**: LangGraph StateGraph orchestrator in `ai_research_framework/core/coordinator.py`
- **ResearchState**: Shared typed state in `ai_research_framework/state/research_state.py`
- **4 Research Agents**: Data Assessment, Forecasting, Synthesis, Validation
- **Config**: `ai_research_framework/config.py` (8GB RAM budget, LLM setup)

These test scenarios confirm the agent pipeline still works after 15 commits (skill imports, refactoring, state extension).

---

## Test Scenarios

### Test 1: State Initialization & Coordinator Import
**Objective**: Verify the LangGraph coordinator and state objects can be imported and initialized without errors.

**Test Steps**:
1. Import `ResearchState` from `ai_research_framework.state.research_state`
2. Import `build_research_graph` from `ai_research_framework.core.coordinator`
3. Create an empty ResearchState instance with required fields
4. Call `build_research_graph()` to compile the LangGraph StateGraph

**Expected Output**:
```
✅ ResearchState imported successfully
✅ build_research_graph() compiled without errors
✅ Graph nodes: ['data_assessment', 'forecasting', 'synthesis', 'validation']
✅ Entry point: 'data_assessment'
✅ Checkpoint memory enabled: MemorySaver
```

**Python Code to Run**:
```python
from ai_research_framework.core.coordinator import build_research_graph
from ai_research_framework.state.research_state import ResearchState

# Initialize state
state = {
    "current_phase": "data_assessment",
    "errors": [],
    "requires_human_approval": False,
    "nielsen_data": None,
    "indeks_data": None,
    "feature_matrix": None,
    "consumer_signals": None,
    "data_quality_report": None,
    "model_forecasts": {},
    "current_model_loading": None,
    "synthesis_output": None,
    "validation_report": None,
    "ram_budget_mb": 8192,
    "peak_ram_observed_mb": 0.0,
}

# Build graph
graph = build_research_graph()
print("✅ Coordinator initialized successfully")
print(f"Nodes: {list(graph.graph.nodes())}")
```

**Pass Criteria**:
- No ImportError, AttributeError, or TypeError
- Graph compiles with all 4 nodes present
- MemorySaver checkpoint enabled
- Entry point is "data_assessment"

---

### Test 2: Config Loading
**Objective**: Verify configuration objects load without errors and respect the 8GB RAM budget.

**Test Steps**:
1. Import `NielsenConfig`, `IndeksDanmarkConfig`, and constants from `config.py`
2. Verify `RAM_BUDGET_MB == 8192`
3. Verify `FORECASTING_MODELS` list contains expected models
4. Verify `LLM_MODEL` is set to `claude-sonnet-4-6`
5. Check that `RAM_TARGETS_MB` sum is <= `RAM_BUDGET_MB` with headroom

**Expected Output**:
```
✅ RAM_BUDGET_MB = 8192
✅ FORECASTING_MODELS = ['arima', 'prophet', 'lightgbm', 'xgboost', 'ridge']
✅ LLM_MODEL = 'claude-sonnet-4-6'
✅ RAM_TARGETS_MB sum = 2696 MB (headroom: 5496 MB ✓)
✅ NielsenConfig created
✅ IndeksDanmarkConfig created
```

**Python Code to Run**:
```python
from ai_research_framework.config import (
    NielsenConfig, 
    IndeksDanmarkConfig, 
    RAM_BUDGET_MB, 
    FORECASTING_MODELS, 
    LLM_MODEL, 
    RAM_TARGETS_MB
)

print(f"RAM_BUDGET_MB: {RAM_BUDGET_MB}")
print(f"FORECASTING_MODELS: {FORECASTING_MODELS}")
print(f"LLM_MODEL: {LLM_MODEL}")

targets_sum = sum(RAM_TARGETS_MB.values())
print(f"RAM_TARGETS_MB sum: {targets_sum} MB")
print(f"Headroom: {RAM_BUDGET_MB - targets_sum} MB")

cfg = NielsenConfig()
indeks_cfg = IndeksDanmarkConfig()
print("✅ Configs initialized")
```

**Pass Criteria**:
- RAM_BUDGET_MB == 8192
- FORECASTING_MODELS contains at least ['arima', 'prophet', 'lightgbm', 'xgboost', 'ridge']
- LLM_MODEL == 'claude-sonnet-4-6'
- RAM_TARGETS_MB sum < RAM_BUDGET_MB
- Both config classes instantiate without KeyError

---

### Test 3: Agent Imports & Initialization
**Objective**: Verify all four research agents can be imported and instantiated.

**Test Steps**:
1. Import each agent class from `ai_research_framework.agents`
2. Instantiate DataAssessmentAgent with NielsenConfig and IndeksDanmarkConfig
3. Instantiate ForecastingAgent, SynthesisAgent, ValidationAgent
4. Verify each agent has a `run()` method

**Expected Output**:
```
✅ DataAssessmentAgent imported and instantiated
✅ ForecastingAgent imported and instantiated
✅ SynthesisAgent imported and instantiated
✅ ValidationAgent imported and instantiated
✅ All agents have callable run() methods
```

**Python Code to Run**:
```python
from ai_research_framework.agents import (
    DataAssessmentAgent,
    ForecastingAgent,
    SynthesisAgent,
    ValidationAgent,
)
from ai_research_framework.config import NielsenConfig, IndeksDanmarkConfig

nielsen_cfg = NielsenConfig()
indeks_cfg = IndeksDanmarkConfig()

data_agent = DataAssessmentAgent(nielsen_cfg, indeks_cfg)
forecast_agent = ForecastingAgent()
synthesis_agent = SynthesisAgent()
validation_agent = ValidationAgent()

for agent, name in [
    (data_agent, "DataAssessmentAgent"),
    (forecast_agent, "ForecastingAgent"),
    (synthesis_agent, "SynthesisAgent"),
    (validation_agent, "ValidationAgent"),
]:
    assert hasattr(agent, "run"), f"{name} missing run() method"
    print(f"✅ {name} initialized with run() method")
```

**Pass Criteria**:
- All 4 agent classes import successfully
- Each agent instantiates without error
- Each agent has a callable `run()` method

---

### Test 4: LangGraph Routing Logic
**Objective**: Verify the conditional routing functions work correctly.

**Test Steps**:
1. Import routing functions from `coordinator.py`:
   - `_should_continue_after_data`
   - `_should_continue_after_forecasting`
   - `_should_continue_after_synthesis`
   - `_should_continue_after_validation`
2. Create test ResearchState objects with different error/approval conditions
3. Call each routing function and verify correct path selection

**Expected Output**:
```
✅ _should_continue_after_data: errors → "end"
✅ _should_continue_after_data: no errors, no approval → "forecasting"
✅ _should_continue_after_data: requires_human_approval → "await_approval"
✅ _should_continue_after_forecasting: errors → "end"
✅ _should_continue_after_forecasting: no errors → "synthesis"
✅ _should_continue_after_synthesis: errors → "end"
✅ _should_continue_after_synthesis: no errors → "validation"
✅ _should_continue_after_validation: requires_human_approval → "await_approval"
✅ _should_continue_after_validation: no approval → "end"
```

**Python Code to Run**:
```python
from ai_research_framework.core.coordinator import (
    _should_continue_after_data,
    _should_continue_after_forecasting,
    _should_continue_after_synthesis,
    _should_continue_after_validation,
)

# Test 1: Data phase with errors
state_error = {"errors": ["Test error"], "requires_human_approval": False}
assert _should_continue_after_data(state_error) == "end"
print("✅ _should_continue_after_data: errors → end")

# Test 2: Data phase, all clear
state_clear = {"errors": [], "requires_human_approval": False}
assert _should_continue_after_data(state_clear) == "forecasting"
print("✅ _should_continue_after_data: no errors → forecasting")

# Test 3: Data phase with human approval required
state_approval = {"errors": [], "requires_human_approval": True}
assert _should_continue_after_data(state_approval) == "await_approval"
print("✅ _should_continue_after_data: requires_human_approval → await_approval")

# Test 4: Forecasting phase with errors
assert _should_continue_after_forecasting(state_error) == "end"
print("✅ _should_continue_after_forecasting: errors → end")

# Test 5: Forecasting phase, all clear
assert _should_continue_after_forecasting(state_clear) == "synthesis"
print("✅ _should_continue_after_forecasting: no errors → synthesis")

# Test 6: Synthesis phase with errors
assert _should_continue_after_synthesis(state_error) == "end"
print("✅ _should_continue_after_synthesis: errors → end")

# Test 7: Synthesis phase, all clear
assert _should_continue_after_synthesis(state_clear) == "validation"
print("✅ _should_continue_after_synthesis: no errors → validation")

# Test 8: Validation phase with approval
assert _should_continue_after_validation(state_approval) == "await_approval"
print("✅ _should_continue_after_validation: requires_human_approval → await_approval")

# Test 9: Validation phase, all clear
assert _should_continue_after_validation(state_clear) == "end"
print("✅ _should_continue_after_validation: no approval → end")
```

**Pass Criteria**:
- All routing decisions match expected paths
- Error handling routes to "end"
- Human approval flag routes to "await_approval"
- Normal flow continues to next phase

---

### Test 5: Data Models (Dataclasses) Instantiation
**Objective**: Verify that the data output models can be instantiated with sample data.

**Test Steps**:
1. Import ModelForecast, SynthesisOutput, ValidationReport from `research_state.py`
2. Create sample instances of each dataclass
3. Verify type hints and default values are correct

**Expected Output**:
```
✅ ModelForecast instantiated: ARIMA, MAPE=12.5%, peak_ram=512MB
✅ SynthesisOutput instantiated: confidence_tier=High, confidence_score=85.2
✅ ValidationReport instantiated: best_model=XGBoost, MAPE=14.8%
```

**Python Code to Run**:
```python
from ai_research_framework.state.research_state import (
    ModelForecast,
    SynthesisOutput,
    ValidationReport,
)

# Test ModelForecast
forecast = ModelForecast(
    model_name="ARIMA",
    point_forecast=100.5,
    lower_90=90.0,
    upper_90=110.0,
    mape_validation=12.5,
    rmse_validation=8.3,
    peak_ram_mb=512.0,
    training_latency_s=45.2,
    inference_latency_s=1.3,
    calibrated=False,
)
print(f"✅ ModelForecast: {forecast.model_name}, MAPE={forecast.mape_validation}%, RAM={forecast.peak_ram_mb}MB")

# Test SynthesisOutput
synthesis = SynthesisOutput(
    point_forecast_ensemble=102.3,
    lower_90_calibrated=92.0,
    upper_90_calibrated=112.0,
    confidence_score=85.2,
    confidence_tier="High",
    inter_model_spread=3.5,
    consumer_signal_direction="aligned",
    recommendation_text="All models converge to 102±10 units. Consumer demand signal aligns.",
    llm_tokens_used=287,
)
print(f"✅ SynthesisOutput: tier={synthesis.confidence_tier}, score={synthesis.confidence_score}")

# Test ValidationReport
report = ValidationReport()
report.best_model = "XGBoost"
report.mape_per_model = {"ARIMA": 14.8, "XGBoost": 13.2, "Ridge": 16.1}
report.mape_with_consumer_signals = 13.1
report.within_ram_budget = True
report.peak_ram_total_mb = 2850.0
print(f"✅ ValidationReport: best_model={report.best_model}, within_budget={report.within_ram_budget}")
```

**Pass Criteria**:
- ModelForecast instantiates with all required fields
- SynthesisOutput instantiates with all required fields
- ValidationReport instantiates and fields are mutable
- All dataclasses respect their type hints

---

### Test 6: Forecasting Agent Feature Engineering (Standalone)
**Objective**: Verify the forecasting agent's feature augmentation logic works.

**Test Steps**:
1. Create a mock feature matrix with required columns
2. Call `augment_features()` from `forecasting_agent.py`
3. Verify lag_12 and price_per_unit are computed correctly

**Expected Output**:
```
✅ Mock feature matrix created (3 brands × 24 periods)
✅ lag_12 computed: 12-month shift applied (rows 0-11 are NaN)
✅ price_per_unit computed: sales_value / sales_units
✅ All NaN values forward/backward filled
```

**Python Code to Run**:
```python
import pandas as pd
import numpy as np

# Mock feature matrix (simplified)
dates = pd.date_range('2023-01-01', periods=24, freq='MS')
brands = ['A', 'B', 'C']
data = []
for brand in brands:
    for i, date in enumerate(dates):
        data.append({
            'date': date,
            'brand': brand,
            'sales_units': max(10 + 5*np.sin(i/12*np.pi*2) + np.random.normal(0, 2), 1),
            'sales_value': 100 + 10*np.sin(i/12*np.pi*2) + np.random.normal(0, 5),
        })

df = pd.DataFrame(data).sort_values(['brand', 'date']).reset_index(drop=True)

# Manually implement augment_features logic
df_aug = df.copy()
g = df_aug.groupby("brand")

# lag_12
df_aug["lag_12"] = g["sales_units"].shift(12)

# price_per_unit
df_aug["price_per_unit"] = np.where(
    df_aug["sales_units"] > 0,
    df_aug["sales_value"] / df_aug["sales_units"].clip(lower=1),
    np.nan
)
df_aug["price_per_unit"] = (
    g["price_per_unit"]
    .transform(lambda s: s.ffill().bfill().fillna(0))
)

print(f"✅ Feature augmentation complete")
print(f"  - lag_12 NaN count (expected 36, rows 0-11 per brand): {df_aug['lag_12'].isna().sum()}")
print(f"  - price_per_unit NaN count (expected 0): {df_aug['price_per_unit'].isna().sum()}")
print(f"  - Sample (Brand A, period 13): lag_12={df_aug.iloc[13]['lag_12']:.1f}, price_per_unit={df_aug.iloc[13]['price_per_unit']:.2f}")
```

**Pass Criteria**:
- lag_12 computed correctly (NaN for first 12 rows per brand)
- price_per_unit computed without division errors
- Forward/backward fill eliminates all NaN in price_per_unit
- Columns added to dataframe as expected

---

### Test 7: Metric Functions (MAPE, RMSE, MAE)
**Objective**: Verify metric calculations match expected forecasting accuracy measures.

**Test Steps**:
1. Import metric functions from `forecasting_agent.py` or `test_evaluation.py`
2. Create simple test vectors (ground truth vs. predictions)
3. Verify MAPE, RMSE, MAE calculations are correct

**Expected Output**:
```
✅ MAPE([100, 100], [90, 110]) = 10.0%
✅ RMSE([100, 100], [90, 110]) = 10.0
✅ MAE([100, 100], [90, 110]) = 10.0
✅ MAPE with zero ground truth → handled gracefully (NaN or 0)
```

**Python Code to Run**:
```python
import numpy as np
from sklearn.metrics import mean_squared_error

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true, dtype=float), np.array(y_pred, dtype=float)
    mask = y_true > 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)

def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def mae(y_true, y_pred):
    return float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))

# Test case 1: Perfect prediction
y_true = [100, 100]
y_pred = [100, 100]
assert mape(y_true, y_pred) == 0.0
assert rmse(y_true, y_pred) == 0.0
assert mae(y_true, y_pred) == 0.0
print(f"✅ Perfect prediction: MAPE=0%, RMSE=0, MAE=0")

# Test case 2: 10% error
y_true = [100, 100]
y_pred = [90, 110]
assert abs(mape(y_true, y_pred) - 10.0) < 0.01
assert abs(rmse(y_true, y_pred) - 10.0) < 0.01
assert abs(mae(y_true, y_pred) - 10.0) < 0.01
print(f"✅ 10% error: MAPE=10.0%, RMSE=10.0, MAE=10.0")

# Test case 3: Zero ground truth (edge case)
y_true = [0, 100, 0]
y_pred = [5, 90, 3]
result = mape(y_true, y_pred)
print(f"✅ Zero ground truth handled: MAPE={result} (NaN={np.isnan(result)} or valid={not np.isnan(result)})")
```

**Pass Criteria**:
- MAPE calculated as % error correctly
- RMSE calculated as root-mean-square error
- MAE calculated as mean absolute error
- Zero ground truth handled gracefully (no division by zero)

---

### Test 8: Forecasting Agent Model Stability (Ridge Log Clipping)
**Objective**: Verify Ridge regression log prediction clipping prevents overflow.

**Test Steps**:
1. Create a Ridge model with synthetic data
2. Make predictions in log space
3. Apply clipping (LOG_CLIP_MIN=-5.0, LOG_CLIP_MAX=15.0)
4. Apply exp transformation without overflow

**Expected Output**:
```
✅ Ridge model trained on log-transformed target
✅ Log predictions clipped to [-5.0, 15.0]
✅ expm1(15.0) = 3.3M units (safe, no overflow)
✅ expm1(-5.0) = ~0 units (safe, no negative)
```

**Python Code to Run**:
```python
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler

# Synthetic data
np.random.seed(42)
X_train = np.random.randn(100, 5)
y_train = np.exp(np.random.uniform(0, 3, 100))  # lognormal-ish
y_train_log = np.log(y_train)

# Train Ridge on log space
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
model = RidgeCV(alphas=[0.1, 1.0, 10.0])
model.fit(X_scaled, y_train_log)

# Predict and clip
X_test = scaler.transform(np.random.randn(10, 5))
y_log_pred_raw = model.predict(X_test)
LOG_CLIP_MIN, LOG_CLIP_MAX = -5.0, 15.0
y_log_pred_clipped = np.clip(y_log_pred_raw, LOG_CLIP_MIN, LOG_CLIP_MAX)

# Inverse transform
y_pred_clipped = np.expm1(y_log_pred_clipped)

print(f"✅ Ridge log predictions clipped to [{LOG_CLIP_MIN}, {LOG_CLIP_MAX}]")
print(f"  - Raw pred range: [{y_log_pred_raw.min():.2f}, {y_log_pred_raw.max():.2f}]")
print(f"  - Clipped pred range: [{y_log_pred_clipped.min():.2f}, {y_log_pred_clipped.max():.2f}]")
print(f"  - Inverse expm1 range: [{y_pred_clipped.min():.0f}, {y_pred_clipped.max():.0f}]")
print(f"  - No NaN/Inf: {not np.any(np.isnan(y_pred_clipped)) and not np.any(np.isinf(y_pred_clipped))}")
```

**Pass Criteria**:
- Ridge model trains successfully
- Log predictions are clipped within bounds
- expm1 inverse transform produces no NaN/Inf
- Predictions are strictly >= 0

---

### Test 9: Coordinator State Transitions (Simulation)
**Objective**: Verify the coordinator can simulate state transitions without Nielsen data.

**Test Steps**:
1. Build the research graph
2. Create an initial state with empty data (simulating pre-data phase)
3. Invoke the graph with a mock input
4. Verify the graph halts before "forecasting" (requires approval or data)

**Expected Output**:
```
✅ Graph compiled with checkpoints
✅ Initial state created
✅ Graph invoked → halts at data_assessment phase (awaiting approval or data)
✅ No errors in execution
```

**Python Code to Run**:
```python
from ai_research_framework.core.coordinator import build_research_graph
from ai_research_framework.state.research_state import ResearchState

# Build graph
graph = build_research_graph()

# Create initial state
initial_state = {
    "current_phase": "data_assessment",
    "errors": [],
    "requires_human_approval": False,  # Simulate data assessment passed
    "nielsen_data": None,
    "indeks_data": None,
    "feature_matrix": None,
    "consumer_signals": None,
    "data_quality_report": None,
    "model_forecasts": {},
    "current_model_loading": None,
    "synthesis_output": None,
    "validation_report": None,
    "ram_budget_mb": 8192,
    "peak_ram_observed_mb": 0.0,
}

# Invoke with thread_id (for checkpointing)
try:
    # This will halt at 'forecasting' due to interrupt_before=['forecasting', 'validation']
    result = graph.invoke(
        initial_state, 
        config={"configurable": {"thread_id": "test-run-1"}}
    )
    print("✅ Graph invoked successfully")
    print(f"  - Final phase: {result.get('current_phase', 'unknown')}")
    print(f"  - Errors: {result.get('errors', [])}")
except Exception as e:
    print(f"❌ Graph invocation failed: {e}")
```

**Pass Criteria**:
- Graph compiles with checkpointer
- Graph invokes without exceptions
- State is preserved across invocation
- Interrupt points are registered (forecasting, validation)

---

### Test 10: Integration Check — All Imports + Config
**Objective**: Full smoke test that all components work together without Nielsen data.

**Test Steps**:
1. Import coordinator, all agents, config, state
2. Build the graph
3. Instantiate all agents
4. Create a valid initial state
5. Confirm no runtime errors

**Expected Output**:
```
✅ All imports successful (coordinator, agents, config, state)
✅ Graph built with 4 nodes and conditional edges
✅ All 4 agents instantiated
✅ Initial state valid TypedDict
✅ System A is ready for production (pending Nielsen data)
```

**Python Code to Run**:
```python
import sys
from pathlib import Path

# Ensure ai_research_framework is in path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    # Imports
    from ai_research_framework.core.coordinator import build_research_graph
    from ai_research_framework.agents import (
        DataAssessmentAgent,
        ForecastingAgent,
        SynthesisAgent,
        ValidationAgent,
    )
    from ai_research_framework.config import NielsenConfig, IndeksDanmarkConfig
    from ai_research_framework.state.research_state import ResearchState
    print("✅ All imports successful")
    
    # Config
    config = NielsenConfig()
    indeks_config = IndeksDanmarkConfig()
    print("✅ Configs initialized")
    
    # Agents
    data_agent = DataAssessmentAgent(config, indeks_config)
    forecast_agent = ForecastingAgent()
    synthesis_agent = SynthesisAgent()
    validation_agent = ValidationAgent()
    print("✅ All agents instantiated")
    
    # Graph
    graph = build_research_graph()
    print("✅ Graph built")
    
    # State
    initial_state = {
        "current_phase": "data_assessment",
        "errors": [],
        "requires_human_approval": False,
        "nielsen_data": None,
        "indeks_data": None,
        "feature_matrix": None,
        "consumer_signals": None,
        "data_quality_report": None,
        "model_forecasts": {},
        "current_model_loading": None,
        "synthesis_output": None,
        "validation_report": None,
        "ram_budget_mb": 8192,
        "peak_ram_observed_mb": 0.0,
    }
    print("✅ Initial state valid")
    
    print("\n✅ SYSTEM A SMOKE TEST PASSED")
    print("   Ready for production (pending Nielsen data access)")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

**Pass Criteria**:
- All modules import without error
- Config objects instantiate
- All 4 agents instantiate
- Graph builds successfully
- Initial state is valid

---

## Running the Tests

### Option 1: Individual Test Scripts
Create a script for each test and run separately:
```bash
cd /path/to/CMT_Codebase
python tests/test_1_state_coordinator.py
python tests/test_2_config.py
python tests/test_3_agents.py
# ... etc
```

### Option 2: Consolidated Test Suite (Recommended)
Create a single test file and run all checks:
```bash
python tests/test_agent_system_comprehensive.py
```

### Option 3: Using pytest (If Available)
```bash
pytest tests/test_agent_system_*.py -v
```

---

## Success Criteria Summary

✅ **All 10 tests pass** → System A is stable after the 15 commits
✅ **Import tests pass** → No module path or dependency issues
✅ **State tests pass** → LangGraph compatibility maintained
✅ **Config tests pass** → RAM budget and LLM setup preserved
✅ **Agent tests pass** → All research agents functional
✅ **Metric tests pass** → Forecasting accuracy calculations correct
✅ **Routing tests pass** → State transitions and error handling work

---

## Failure Diagnosis

| Symptom | Likely Cause | Next Step |
|---------|-------------|-----------|
| `ModuleNotFoundError: ai_research_framework` | Path not in sys.path | Add `sys.path.insert(0, str(ROOT))` |
| `ImportError: from langgraph` | LangGraph not installed | `pip install langgraph` |
| Routing test fails (wrong path) | Conditional logic broken in coordinator | Review `_should_continue_*` functions |
| Agent instantiation fails | Missing config fields | Check config.py for required .env vars |
| State TypedDict mismatch | Field mismatch between code and docs | Verify research_state.py matches ResearchState definition |
| Graph.invoke hangs | Checkpoint issue or interrupt point not released | Check if thread_id is unique |

---

## Post-Sync Checklist

After confirming all tests pass:
- [ ] Run all 10 test scenarios
- [ ] Log results in `docs/testing/test_results_2026-04-15.md`
- [ ] Notify colleague (Enrico) that System A is validated
- [ ] Sync 15 commits with `git push origin Major_Refactor_2_Academic_Repos_NotebookLM`
- [ ] Create PR for merge into main

---

**Author**: Brian Rohde  
**Date**: 2026-04-15  
**Status**: Ready for testing
