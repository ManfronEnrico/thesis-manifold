"""
Builder Agent — System B sub-package
---------------------------------------
Exposes the public API for the Builder Agent loop.

Primary entry point:
    from thesis_production_system.agents.builder import run_builder

    final_state = run_builder(
        goal="find best 3-model ensemble under 512MB RAM",
        max_trials=30,
    )

Individual sub-agents (for testing or extension):
    from thesis_production_system.agents.builder import (
        Architect, Coder, Executor, Evaluator, BuilderRegistry
    )
"""

from .architect import Architect
from .builder_graph import build_graph, run_builder
from .coder import Coder
from .evaluator import Evaluator
from .executor import Executor
from .experiment_registry import (
    BuilderRegistry,
    BuilderState,
    TrialConfig,
    TrialResult,
)

__all__ = [
    "Architect",
    "Coder",
    "Executor",
    "Evaluator",
    "BuilderRegistry",
    "BuilderState",
    "TrialConfig",
    "TrialResult",
    "build_graph",
    "run_builder",
]
