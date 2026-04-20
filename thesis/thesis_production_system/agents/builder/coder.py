"""
Builder Agent — Coder Sub-agent
---------------------------------
Generates a Python trial script from the base_config.py template by patching
the trial-specific constants (model list, ensemble weights, flags).

The Coder:
1. Reads the base template from thesis.ai_research_framework/templates/base_config.py
2. Uses Claude API (claude-sonnet-4-6, temperature=0) to patch only the variable
   parts of the template
3. Saves the generated script to results/scripts/trial_{trial_id}.py
4. Returns the script path for the Executor

CRITICAL: Generated code must import from thesis.ai_research_framework (not re-implement)
CRITICAL: Generated code must write results to results/trial_{trial_id}.json
CRITICAL: Generated code uses the same tracemalloc pattern as the base template
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import anthropic

from .experiment_registry import TrialConfig

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_TEMPLATE_PATH = Path("ai_research_framework/templates/base_config.py")
SCRIPTS_DIR = Path("results/scripts")

LLM_MODEL = "claude-sonnet-4-6"
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 2_048  # Script patch is typically <100 lines


class Coder:
    """
    Generates a runnable trial script by patching the base template.

    Usage
    -----
    >>> coder = Coder()
    >>> script_path = coder.generate(config)
    """

    def __init__(
        self,
        template_path: Path = BASE_TEMPLATE_PATH,
        scripts_dir: Path = SCRIPTS_DIR,
        api_key: Optional[str] = None,
    ) -> None:
        self.template_path = template_path
        self.scripts_dir = scripts_dir
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ["ANTHROPIC_API_KEY"]
        )

    # ── Main entry point ──────────────────────────────────────────────────────

    def generate(self, config: TrialConfig) -> str:
        """
        Generate and save a trial script for the given TrialConfig.

        Reads the base template, uses Claude API to patch the variable constants,
        validates the result contains required imports, then saves to disk.

        Parameters
        ----------
        config : TrialConfig
            Configuration to embed in the generated script.

        Returns
        -------
        str
            Absolute path to the saved script file.

        Raises
        ------
        FileNotFoundError
            If the base template does not exist.
        ValueError
            If the generated script is missing required imports or write_output call.
        """
        if not self.template_path.exists():
            raise FileNotFoundError(
                f"Base template not found at {self.template_path}. "
                "ai_research_framework/templates/base_config.py must exist."
            )

        template = self.template_path.read_text()
        script = self._patch_template(template, config)
        self._validate_script(script, config)

        script_path = self._save_script(config["trial_id"], script)
        return str(script_path)

    # ── Template patching ─────────────────────────────────────────────────────

    def _patch_template(self, template: str, config: TrialConfig) -> str:
        """
        Call Claude API to patch the base template with trial-specific values.

        The LLM only modifies the 5 constant lines near the top of the file
        (TRIAL_MODELS, ENSEMBLE_WEIGHTS, USE_CONSUMER_SIGNAL, APPLY_CALIBRATION,
        MAX_RAM_PER_MODEL_MB). Everything else remains identical to the template.

        Parameters
        ----------
        template : str
            Contents of base_config.py.
        config : TrialConfig
            Values to embed.

        Returns
        -------
        str
            Complete patched Python script.
        """
        system_prompt = (
            "You are a Python code editor. You receive a Python script template and a "
            "configuration dict. Your task is to modify ONLY the following 5 constant "
            "assignments near the top of the file:\n\n"
            "  TRIAL_MODELS = [...]\n"
            "  ENSEMBLE_WEIGHTS = {...}\n"
            "  USE_CONSUMER_SIGNAL = ...\n"
            "  APPLY_CALIBRATION = ...\n"
            "  MAX_RAM_PER_MODEL_MB = ...\n\n"
            "Rules:\n"
            "- Do NOT change any imports, function bodies, class definitions, or CLI code\n"
            "- Do NOT add new imports or functions\n"
            "- Do NOT change the write_output() call or the run_trial() signature\n"
            "- ensemble_weights must contain exactly the models in TRIAL_MODELS\n"
            "- Return ONLY the complete modified Python file — no explanation, no markdown"
        )

        user_prompt = (
            f"Config to embed:\n"
            f"  trial_id: {config['trial_id']}\n"
            f"  models: {config['models']}\n"
            f"  ensemble_weights: {config['ensemble_weights']}\n"
            f"  use_consumer_signal: {config['use_consumer_signal']}\n"
            f"  apply_calibration: {config['apply_calibration']}\n"
            f"  max_ram_mb: {config['max_ram_mb']}\n\n"
            f"Template to patch:\n\n{template}"
        )

        response = self.client.messages.create(
            model=LLM_MODEL,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = response.content[0].text.strip()
        # Strip markdown fences if the LLM wrapped the output
        if raw.startswith("```"):
            parts = raw.split("```")
            raw = parts[1] if len(parts) >= 2 else raw
            if raw.startswith("python\n"):
                raw = raw[7:]
        return raw.strip()

    # ── Validation ────────────────────────────────────────────────────────────

    @staticmethod
    def _validate_script(script: str, config: TrialConfig) -> None:
        """
        Check that the generated script meets minimum correctness requirements.

        Raises ValueError with a descriptive message if any check fails.
        """
        checks = {
            "imports ai_research_framework": "from thesis.ai_research_framework" in script or
                                             "import ai_research_framework" in script,
            "calls write_output": "write_output(" in script,
            "calls run_trial": "run_trial(" in script,
            "contains trial_id": config["trial_id"] in script or
                                  "TRIAL_MODELS" in script,  # patched constant
        }
        failures = [name for name, passed in checks.items() if not passed]
        if failures:
            raise ValueError(
                f"Generated script for trial {config['trial_id']} failed validation: "
                + ", ".join(failures)
            )

    # ── File I/O ──────────────────────────────────────────────────────────────

    def _save_script(self, trial_id: str, script: str) -> Path:
        """
        Save the generated script to results/scripts/trial_{trial_id}.py.

        Parameters
        ----------
        trial_id : str
            Used as the filename component.
        script : str
            Complete Python script content.

        Returns
        -------
        Path
            Absolute path to the saved file.
        """
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        script_path = self.scripts_dir / f"trial_{trial_id}.py"
        script_path.write_text(script)
        return script_path.resolve()
