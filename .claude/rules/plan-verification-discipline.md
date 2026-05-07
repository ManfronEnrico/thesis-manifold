---
type: feedback
name: Plan Verification Discipline
description: Always verify plan claims against actual code; do not take in-progress plans at face value
---

# Plan Verification Discipline

**Rule:** When referencing claims in a plan document, **always cross-check against the actual implementation** before acting on them. In-progress plans become stale quickly.

**Why:** Plans document intent and design decisions, but code is ground truth. A plan may describe an old approach, a planned refactoring that hasn't shipped, or a decision that was reversed. Taking a plan at face value without checking the code can lead to:
- Implementing outdated logic
- Missing bug fixes that were applied but not documented
- Duplication of work
- Confusion about what's actually implemented vs. intended

**How to apply:**

1. **When a plan claims "feature X is implemented":**
   - Check the actual script/file mentioned
   - Read the code to confirm behavior matches the description
   - If code differs from plan, code is correct; update plan after execution

2. **When a plan says "use flag --foo":**
   - Open the orchestrator/script
   - Check `argparse` or flag handling to confirm `--foo` exists
   - Test the flag behavior if uncertain
   - Don't rely on plan documentation of flags

3. **When a plan describes architecture or structure:**
   - Use `Glob` to verify folder/file layout matches description
   - Check imports and module paths in code
   - Confirm variable names and function signatures

4. **During execution, when something doesn't match plan:**
   - Document the mismatch (in a session note or plan update)
   - Update the plan after discovery (not before)
   - Mark the session where the drift was found

**Examples of drift found:**

- Plan said: "use `--skip-raw` to skip caching"
- Code had: `--run-raw` flag (inverted semantics)
- **Action:** Fixed code to match intent, updated plan

- Plan said: "Step 0 is skipped if cache exists"
- Code had: `else: return False` (skipped when cache MISSING)
- **Action:** Fixed code logic, updated plan with bug note

**When to update the plan:**
- Immediately after discovering code/plan drift during execution
- Use `plan-update-all` skill to sync session context into plan file
- Add timestamp and brief note of what was found/corrected

