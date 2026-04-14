# Tooling Issues — CMT_Codebase

Living registry of solved Windows / OneDrive / tooling problems. Claude must read this **before** any plan or multi-step task.

Updated per `.claude/rules/tooling-issues-workflow.md`.

---

## Issue 1: Direct Edit/Write on OneDrive .py files causes corruption

**Symptom**: After using Claude Code's Edit or Write tool to modify a `.py` file on an OneDrive path, the file becomes corrupted with `\x08` (backspace) bytes where backslash-b sequences existed. Python then fails to import the file with a `SyntaxError` or `EEXIST` error.

**Cause**: OneDrive's file sync on Windows introduces CRLF line ending conflicts. The Edit/Write tool writes in a way that interacts badly with OneDrive's file locking and line-ending normalization, turning `\b` (backspace escape in Python strings) into literal `\x08` bytes.

**Solution**: Never use Edit or Write directly on `.py` files located on an OneDrive path. Use the safe patching pattern instead:
1. Write the new script to a temp location: `Write → C:/Users/brian/AppData/Local/Temp/patch_script.py`
2. Execute the patch via Bash: `python C:/Users/brian/AppData/Local/Temp/patch_script.py`
3. The patch script reads the target file with `read_bytes()`, normalizes CRLF, patches the content, and writes back with `write_bytes()`

The PreToolUse hook (`.claude/hooks/check_file_edit.py`) blocks direct Edit/Write attempts on OneDrive `.py` files automatically. If the hook fires, follow the safe patching pattern above.

**Key lesson**: All `.py` files in this repo are on an OneDrive path — always use the temp-script pattern.

---

## Issue 2: .env file must never be written by Claude

**Symptom**: Accidental write to `.env` would expose API keys and secrets to the conversation context.

**Cause**: `.env` contains live credentials (API keys for Anthropic, etc.).

**Solution**: The PreToolUse hook blocks all writes to `.env` files. Edit `.env` manually in a text editor outside Claude Code. Use `.env.example` as the template for documenting required variables.

**Key lesson**: `.env` is Brian-only. `.env.example` is the safe reference for Claude.

---

## Issue 3: Python 3.14 installed — check compatibility

**Symptom**: The `__pycache__` directories show `.cpython-314.pyc` files, indicating Python 3.14 is in use. Some packages may not yet support 3.14.

**Cause**: Cutting-edge Python version on this machine.

**Solution**: Before installing any new package, check PyPI for 3.14 compatibility. If a package fails to install, try the latest pre-release or pin to 3.12 using a virtual environment.

**Key lesson**: Verify package 3.14 compatibility before `pip install`.

---

## Issue 4: Enrico's SRQ1 model selection reports validation metrics as if they were test metrics

**Symptom**: CLAUDE.md and `global_v2_summary.md` claim "Global LightGBM v2 (Tweedie) achieves 22.5% median MAPE" — but when cross-checked against `test_summary.md`, the test set MAPE is **46.7%** (LightGBM) / **45.5%** (XGBoost). The 22.5% figure is from the validation set, not the held-out test set.

**Cause**: Two separate evaluation runs produced different narratives:
1. `global_model_v2.py` reports validation metrics (22.5%, 23.8%, 26.2%) in `global_v2_summary.md`
2. `test_evaluation.py` reports test metrics (46.7%, 45.5%, 48.4%) in `test_summary.md`
3. CLAUDE.md was updated with v2 validation results but not re-checked against test results after `test_evaluation.py` ran
4. Tweedie loss was tested on validation but **never evaluated on the test set** — only MSE/log and Ensemble were tested on test

**Solution**: When reporting SRQ1 results in the thesis, always report **test set metrics** as the ground truth:
- Best test model: XGBoost 45.5% median MAPE (or LightGBM 46.7%)
- Baseline (SeasonalNaive): 66.9% median MAPE
- Note: All models degrade 12–18pp from val → test due to short training window (29 periods)
- Acknowledge: Tweedie loss was tested on validation (23.8%) but not on test; recommend test validation before claiming superiority
- Update CLAUDE.md to reflect test numbers, not validation numbers

Do NOT use 22.5% as the final model MAPE in any thesis section. Do NOT claim Tweedie as "best model" without test validation.

**Key lesson**: Validation metrics are for hyperparameter selection only. Test metrics are what you report in the thesis. When an agent runs multiple evaluation scripts, always harmonize the narrative to use the same evaluation set for all claims in CLAUDE.md.

**Impact on SRQ2/SRQ3/SRQ4**: The synthesis module (SRQ2) will be benchmarked against the test baseline (45–47% MAPE), not the inflated validation baseline (22–26%). Budget Phase 5 accordingly.
