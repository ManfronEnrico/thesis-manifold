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

---

## Issue 5: LangGraph venv installation corruption — missing RECORD, version None

**Symptom**: Tests fail with `ImportError: cannot import name 'StateGraph' from 'langgraph.graph'`. Running `pip list` shows `langgraph` with version `None`. Attempting to upgrade/reinstall fails with `error: uninstall-no-record-file — Cannot uninstall langgraph None`.

**Cause**: The LangGraph package in the venv became corrupted — the dist-info RECORD file was deleted or never written. Pip cannot uninstall packages without a RECORD, preventing reinstallation. This can happen after interrupted installs, forced deletions, or OneDrive sync conflicts.

**Solution**: 
1. Manually delete the broken installation: `rm -rf .venv/Lib/site-packages/langgraph*`
2. Reinstall all dependencies: `.venv/Scripts/python.exe -m pip install pyzotero python-dotenv pydantic langgraph langchain`
3. Verify the import: `.venv/Scripts/python.exe -c "from langgraph.graph import StateGraph, END"`
4. Run tests to confirm: `python test_runner.py --module all`

**Key lesson**: Never try to force-reinstall or --no-deps a package in a broken venv state. Always manually delete the corrupted directory first, then reinstall with full dependencies. The `pip install --force-reinstall --no-deps` pattern fails on corrupted installations — it needs the full dependency chain to work.

**Prevention**: When seeing pip RECORD errors, immediately delete the package directory and do a clean install. Don't waste time with pip flags that won't work on already-broken metadata.

---

## Issue 6: Unicode encoding errors when writing text to Windows console/files

**Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character '\u2713' in position 0: character maps to <undefined>` when Python prints special characters (checkmarks, arrows, etc.) or writes UTF-8 text to disk on Windows. The error appears during print statements or `.write_text()` file writes.

**Cause**: Windows console defaults to `cp1252` (Latin-1) encoding, which cannot represent Unicode characters outside the Western European range. When Python tries to encode special characters (✓, →, ✅, etc.) to `cp1252`, it fails.

**Solution**: Use UTF-8 encoding explicitly in all file writes and avoid special characters in print statements:
1. For file writes: `Path().write_bytes(content.encode('utf-8'))` instead of `.write_text()`
2. For print statements: Use ASCII equivalents in f-strings (avoid ✓, use OK instead; avoid →, use `->`; avoid ✅, use [OK])
3. When generating script files: Write to `/tmp/` first with explicit UTF-8, then use Bash to read/normalize/write to target
4. Set environment variable if needed: `export PYTHONIOENCODING=utf-8` (though this is not a guaranteed fix on Windows)

**Key lesson**: Never assume UTF-8 on Windows. Always use `.write_bytes(...encode('utf-8'))` for file I/O. For print output to console, test with the actual Python interpreter first before committing the code.

**Impact on scripts**: The test_group.py and zotero_sync_*.py scripts all use `.write_bytes(text.encode('utf-8'))` to avoid this issue. Copy this pattern for any future scripts that generate reports or documentation files.

---

## Issue 7: PowerShell `<<` redirection operator incompatible with bash heredoc syntax

**Symptom**: When running Python code from PowerShell using `python << 'EOF'`, PowerShell throws parser errors: `Missing file specification after redirection operator` and `The '<' operator is reserved for future use`. The `<<` heredoc syntax that works in bash/sh does not work in PowerShell.

**Cause**: PowerShell uses different syntax for input redirection. The `<` and `<<` operators are not supported for heredoc-style multi-line input. PowerShell expects `@' ... '@` (here-string) syntax instead.

**Solution**: Use one of these approaches:
1. **In bash environment** (recommended): Switch to bash shell and use `python << 'EOF'` normally
2. **In PowerShell**: Use here-string syntax: `@" ... "@ | python` or create a temp `.py` file and run it
3. **Portable pattern**: Always create a temp Python file instead of inline heredoc. The pattern is:
   - Write script to `/tmp/script.py`
   - Run `python /tmp/script.py`
   - Clean up if needed
4. **From PowerShell specifically**:
   ```powershell
   $script = @"
   import os
   print('hello')
   "@
   $script | python
   ```

**Key lesson**: For cross-platform compatibility (Windows PowerShell + bash), avoid heredoc syntax. Always use temp files instead: write to `/tmp/`, execute via Bash, let Bash handle I/O. This avoids shell syntax incompatibilities entirely.

**Prevention**: When user is in PowerShell and needs to run Python code, guide them to create a `.py` file instead of using inline heredoc. Check their shell (`echo $SHELL` in bash, `$PROFILE` in PowerShell) before suggesting syntax.
