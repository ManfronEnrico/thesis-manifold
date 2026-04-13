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
