"""
PreToolUse hook: blocks direct Edit/Write on:
  - .py files anywhere         (CRLF corruption + encoding risk)
  - .env files anywhere        (secret leakage risk)
"""
import sys
import json

data = json.load(sys.stdin)
file_path = data.get("tool_input", {}).get("file_path", "")

block_py = file_path.endswith(".py")
block_env = file_path.endswith(".env")

if block_py:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "BLOCKED: Direct Edit/Write on .py files causes CRLF corruption and encoding errors. "
                "Use the safe patching pattern:\n"
                "  1. Write tool -> C:/Users/brian/AppData/Local/Temp/script.py\n"
                "  2. Bash -> python C:/Users/brian/AppData/Local/Temp/script.py\n"
                "  3. Script: read_bytes() -> CRLF normalize -> patch -> write_bytes()\n"
                "See .claude/rules/tooling-issues-workflow.md for full details."
            )
        }
    }))
elif block_env:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "BLOCKED: Writing to .env files is prohibited to prevent accidental "
                "secret exposure. Edit .env manually outside Claude Code."
            )
        }
    }))
else:
    sys.exit(0)
