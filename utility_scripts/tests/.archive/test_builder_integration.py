"""
Builder Agent — Integration Tests
------------------------------------
Three tests covering the core Builder Agent contract:

Test 1: Registry append + deduplication
    - Append two trials with the same config → second entry flagged as duplicate
    - get_best_trial(metric="MAPE") returns the lower-MAPE entry
    - get_all_results_as_dataframe() returns correct shape

Test 2: Executor handles subprocess failure gracefully
    - A script that exits with returncode != 0 → TrialResult with error set
    - A non-existent script path → TrialResult with error set
    - A script that times out → TrialResult with error set (mocked timeout)

Test 3: Evaluator correctly identifies convergence
    - 5 consecutive successful trials with < 0.5% MAPE improvement → converged=True
    - Fewer than 5 trials → converged=False
    - Budget exhausted (trials_run >= max_trials) → stop_reason="budget_exhausted"

Run with:
    python -m pytest tests/test_builder_integration.py -v
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

import pytest

# ── Add project root to path ──────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent.parent))

from thesis.thesis_production_system.agents.builder.experiment_registry import (
    BuilderRegistry,
    BuilderState,
    TrialConfig,
    TrialResult,
)
from thesis.thesis_production_system.agents.builder.executor import Executor
from thesis.thesis_production_system.agents.builder.evaluator import Evaluator


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_config(trial_id: str = "t_test", models: List[str] = None) -> TrialConfig:
    models = models or ["ridge", "lightgbm"]
    n = len(models)
    return {
        "trial_id": trial_id,
        "models": models,
        "ensemble_weights": {m: round(1.0 / n, 4) for m in models},
        "use_consumer_signal": False,
        "apply_calibration": True,
        "max_ram_mb": 512,
    }


def _make_result(trial_id: str, mape: float, error: str = None) -> TrialResult:
    return {
        "trial_id": trial_id,
        "MAPE": mape,
        "RMSE": mape * 100,
        "peak_RAM_MB": 350.0,
        "latency_sec": 12.0,
        "confidence_score": max(0.0, 80.0 - mape),
        "error": error,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TEST 1: Registry append + deduplication
# ─────────────────────────────────────────────────────────────────────────────

class TestRegistryAppendAndDeduplication:
    """Test 1: BuilderRegistry core behaviour."""

    def test_append_and_retrieve(self, tmp_path):
        """Appended entry can be retrieved by trial_id."""
        reg = BuilderRegistry(tmp_path / "registry.json")
        config = _make_config("t_001")
        result = _make_result("t_001", mape=12.5)

        entry = reg.append("test goal", config, result, "looks good")

        assert entry["trial_id"] == "t_001"
        assert reg.count() == 1
        retrieved = reg.get_by_id("t_001")
        assert retrieved is not None
        assert retrieved["result"]["MAPE"] == 12.5

    def test_duplicate_config_flagged(self, tmp_path):
        """Second append with identical config gets DUPLICATE flag in evaluator_judgment."""
        reg = BuilderRegistry(tmp_path / "registry.json")
        config_a = _make_config("t_001")
        config_b = _make_config("t_002")  # different trial_id, same hash

        reg.append("goal", config_a, _make_result("t_001", 12.5), "first")
        entry_b = reg.append("goal", config_b, _make_result("t_002", 11.0), "second")

        assert "DUPLICATE CONFIG" in entry_b["evaluator_judgment"]
        assert reg.count() == 2

    def test_get_best_trial_mape(self, tmp_path):
        """get_best_trial('MAPE') returns the entry with the lowest MAPE."""
        reg = BuilderRegistry(tmp_path / "registry.json")
        reg.append("g", _make_config("t_001", ["ridge"]), _make_result("t_001", 15.0), "j1")
        reg.append("g", _make_config("t_002", ["lightgbm"]), _make_result("t_002", 9.5), "j2")
        reg.append("g", _make_config("t_003", ["arima"]), _make_result("t_003", 12.0), "j3")

        best = reg.get_best_trial("MAPE")
        assert best is not None
        assert best["trial_id"] == "t_002"

    def test_get_best_trial_excludes_failures(self, tmp_path):
        """get_best_trial ignores trials with errors even if they have low MAPE."""
        reg = BuilderRegistry(tmp_path / "registry.json")
        # A failed trial with unrealistically low MAPE (0.0)
        reg.append("g", _make_config("t_001", ["ridge"]), _make_result("t_001", 0.0, error="timeout"), "fail")
        reg.append("g", _make_config("t_002", ["lightgbm"]), _make_result("t_002", 11.0), "ok")

        best = reg.get_best_trial("MAPE")
        assert best is not None
        assert best["trial_id"] == "t_002"

    def test_dataframe_shape(self, tmp_path):
        """get_all_results_as_dataframe returns one row per trial with expected columns."""
        pytest.importorskip("pandas")
        reg = BuilderRegistry(tmp_path / "registry.json")
        for i in range(3):
            reg.append(
                "goal",
                _make_config(f"t_00{i}", ["ridge"]),
                _make_result(f"t_00{i}", 10.0 + i),
                "judgment",
            )

        df = reg.get_all_results_as_dataframe()
        assert len(df) == 3
        assert "MAPE" in df.columns
        assert "trial_id" in df.columns

    def test_append_only_no_overwrite(self, tmp_path):
        """Appending a new trial never modifies existing entries."""
        reg = BuilderRegistry(tmp_path / "registry.json")
        reg.append("g", _make_config("t_001", ["ridge"]), _make_result("t_001", 12.0), "j")

        original_entry = reg.get_by_id("t_001")
        reg.append("g", _make_config("t_002", ["arima"]), _make_result("t_002", 9.0), "j2")

        assert reg.get_by_id("t_001") == original_entry  # unchanged


# ─────────────────────────────────────────────────────────────────────────────
# TEST 2: Executor handles subprocess failure gracefully
# ─────────────────────────────────────────────────────────────────────────────

class TestExecutorSubprocessFailures:
    """Test 2: Executor robustness to script failures."""

    def test_nonexistent_script_returns_error(self, tmp_path):
        """Executor returns TrialResult with error when script path does not exist."""
        executor = Executor(results_dir=tmp_path, timeout=10)
        config = _make_config("t_fail_01")

        result = executor.run(script_path="/nonexistent/path/script.py", config=config)

        assert result["error"] is not None
        error_lower = result["error"].lower()
        assert (
            "not found" in error_lower
            or "no such file" in error_lower
            or "Script not found" in result["error"]
        )
        assert result["MAPE"] == 0.0

    def test_script_with_nonzero_exit_returns_error(self, tmp_path):
        """Executor captures stderr when the subprocess exits with returncode != 0."""
        # Write a script that immediately raises an exception
        script = tmp_path / "fail_script.py"
        script.write_text("raise RuntimeError('intentional failure')\n")

        executor = Executor(results_dir=tmp_path, timeout=10)
        config = _make_config("t_fail_02")

        result = executor.run(script_path=str(script), config=config)

        assert result["error"] is not None
        assert result["MAPE"] == 0.0

    def test_script_writes_output_json_read_correctly(self, tmp_path):
        """Executor reads the output JSON written by a successful script."""
        trial_id = "t_ok_01"
        output_json = {
            "trial_id": trial_id,
            "MAPE": 11.3,
            "RMSE": 1130.0,
            "peak_RAM_MB": 280.0,
            "latency_sec": 8.5,
            "confidence_score": 72.0,
            "error": None,
        }

        # Write a script that writes the expected JSON and exits 0
        script = tmp_path / f"trial_{trial_id}.py"
        script.write_text(
            textwrap.dedent(f"""\
                import json
                from pathlib import Path
                Path("{tmp_path}").mkdir(parents=True, exist_ok=True)
                Path("{tmp_path}/trial_{trial_id}.json").write_text(json.dumps({output_json}))
            """)
        )

        executor = Executor(results_dir=tmp_path, timeout=30)
        config = _make_config(trial_id)

        result = executor.run(script_path=str(script), config=config)

        assert result["error"] is None
        assert result["MAPE"] == pytest.approx(11.3)
        assert result["peak_RAM_MB"] == pytest.approx(280.0)

    def test_timeout_returns_error(self, tmp_path):
        """Executor returns error when subprocess exceeds timeout."""
        # Write a script that sleeps indefinitely
        script = tmp_path / "sleep_script.py"
        script.write_text("import time; time.sleep(9999)\n")

        executor = Executor(results_dir=tmp_path, timeout=1)  # 1-second timeout
        config = _make_config("t_timeout")

        result = executor.run(script_path=str(script), config=config)

        assert result["error"] is not None
        assert "timed out" in result["error"].lower()

    def test_nielsen_not_found_message(self, tmp_path):
        """Executor propagates clear Nielsen-missing message."""
        script = tmp_path / "nielsen_script.py"
        script.write_text(
            "import sys\n"
            "print('Nielsen data not found at data/nielsen/', file=sys.stderr)\n"
            "sys.exit(1)\n"
        )

        executor = Executor(results_dir=tmp_path, timeout=10)
        config = _make_config("t_nielsen")

        result = executor.run(script_path=str(script), config=config)

        assert result["error"] is not None
        assert "Nielsen data not found" in result["error"]

    def test_validate_ram_flags_violation(self, tmp_path):
        """validate_ram returns an error message when peak RAM exceeds limit."""
        executor = Executor(results_dir=tmp_path)
        result = _make_result("t_ram", mape=10.0)
        result["peak_RAM_MB"] = 8_000.0  # Over 7,680 MB limit

        error_msg = executor.validate_ram(result, limit_mb=7_680.0)

        assert error_msg is not None
        assert "exceeded RAM limit" in error_msg

    def test_validate_ram_passes_within_budget(self, tmp_path):
        """validate_ram returns None when peak RAM is within budget."""
        executor = Executor(results_dir=tmp_path)
        result = _make_result("t_ram_ok", mape=10.0)
        result["peak_RAM_MB"] = 3_000.0

        assert executor.validate_ram(result) is None


# ─────────────────────────────────────────────────────────────────────────────
# TEST 3: Evaluator stopping conditions
# ─────────────────────────────────────────────────────────────────────────────

class TestEvaluatorStoppingConditions:
    """Test 3: Evaluator correctly identifies stopping conditions."""

    def _make_state(
        self,
        results: List[TrialResult],
        max_trials: int = 30,
    ) -> BuilderState:
        configs = [_make_config(f"t_{i:03d}") for i in range(len(results))]
        return {
            "goal": "find best ensemble",
            "max_trials": max_trials,
            "trials_run": configs,
            "results": results,
            "best_trial_id": None,
            "stop_reason": None,
            "generated_code": None,
            "evaluator_judgment": None,
        }

    def test_budget_exhausted(self):
        """stop_reason='budget_exhausted' when trials_run >= max_trials."""
        results = [_make_result(f"t_{i:03d}", 10.0 + i) for i in range(5)]
        state = self._make_state(results, max_trials=5)

        # Mock Claude API call so the test doesn't require ANTHROPIC_API_KEY
        with patch.object(Evaluator, "_get_judgment", return_value="budget reached"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, stop_reason, _ = evaluator.evaluate(state)

        assert should_stop is True
        assert stop_reason == "budget_exhausted"

    def test_ram_violation_triggers_stop(self):
        """stop_reason='ram_violation' when any trial exceeds 7.5 GB."""
        results = [
            _make_result("t_000", 12.0),
            _make_result("t_001", 10.0),
        ]
        results[1]["peak_RAM_MB"] = 8_500.0  # Over limit

        state = self._make_state(results, max_trials=30)

        with patch.object(Evaluator, "_get_judgment", return_value="ram exceeded"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, stop_reason, _ = evaluator.evaluate(state)

        assert should_stop is True
        assert stop_reason == "ram_violation"

    def test_convergence_detected_after_5_stable_trials(self):
        """stop_reason='converged' when last 5 successful trials show < 0.5% improvement."""
        # Best: 10.0% MAPE; last 5 all within 0.005 of each other (no improvement)
        results = [
            _make_result("t_000", 14.0),
            _make_result("t_001", 12.0),
            _make_result("t_002", 10.0),   # best so far
            _make_result("t_003", 10.003), # < 0.005 improvement
            _make_result("t_004", 10.001),
            _make_result("t_005", 9.999),
            _make_result("t_006", 10.002),
        ]
        state = self._make_state(results, max_trials=30)

        with patch.object(Evaluator, "_get_judgment", return_value="converged"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, stop_reason, _ = evaluator.evaluate(state)

        assert should_stop is True
        assert stop_reason == "converged"

    def test_no_convergence_with_fewer_than_5_trials(self):
        """Convergence is not triggered with fewer than CONVERGENCE_WINDOW trials."""
        results = [
            _make_result("t_000", 10.001),
            _make_result("t_001", 10.002),
            _make_result("t_002", 10.000),
        ]
        state = self._make_state(results, max_trials=30)

        with patch.object(Evaluator, "_get_judgment", return_value="continuing"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, stop_reason, _ = evaluator.evaluate(state)

        assert should_stop is False
        assert stop_reason is None

    def test_improving_trials_do_not_trigger_convergence(self):
        """Consistent MAPE improvement does not trigger convergence."""
        results = [
            _make_result(f"t_{i:03d}", 15.0 - i)  # MAPE drops 1% each trial
            for i in range(10)
        ]
        state = self._make_state(results, max_trials=30)

        with patch.object(Evaluator, "_get_judgment", return_value="improving"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, _, _ = evaluator.evaluate(state)

        assert should_stop is False

    def test_failed_trials_excluded_from_convergence_check(self):
        """Trials with errors are excluded from the convergence window."""
        # 3 good trials, then 5 failed trials — should NOT trigger convergence
        results = (
            [_make_result(f"t_{i:03d}", 10.0 + i) for i in range(3)]
            + [_make_result(f"t_{i+3:03d}", 0.0, error="script failed") for i in range(5)]
        )
        state = self._make_state(results, max_trials=30)

        with patch.object(Evaluator, "_get_judgment", return_value="continuing"):
            evaluator = Evaluator.__new__(Evaluator)
            evaluator.client = MagicMock()

            should_stop, _, _ = evaluator.evaluate(state)

        # Only 3 successful trials — insufficient for convergence window of 5
        assert should_stop is False
