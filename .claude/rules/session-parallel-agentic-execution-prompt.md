---
name: session-parallel-agentic-execution-prompt
description: RULE - Task isolation prompt for parallel execution; governs how Claude offers worktree/sub-agent isolation at task kickoff
category: workflow
applies-to: [task kickoff, worktree selection]
triggers: [task initialization, medium-high-epic scope tasks]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Parallel Execution Prompt

**Auto-loads** every session. Governs how Claude offers isolation at task kickoff.

## Rule

Before starting any task classified **MEDIUM, HIGH, or EPIC** scope (per scope table below), prompt the user with three options. Do NOT silently start work on main without the prompt unless the task is TRIVIAL or LOW scope.

## The Prompt

> This task is **[parallelizable with X / sequential]** and scoped **[MEDIUM/HIGH/EPIC]**. How would you like to run it?
>
> - **[A] Auto-isolate via sub-agent** *(recommended default for scoped work)*
>   I spawn a sub-agent with `isolation: "worktree"`. The harness creates + cleans up a temporary worktree automatically. Best for parallel work across multiple independent tasks.
>
> - **[B] Manual worktree**
>   I create `worktrees/<slug>/` + a feature branch. **You** then open a new Claude Code window at that path to drive the work interactively. Use this when you want turn-by-turn control.
>
> - **[C] Run here on current branch** *(no isolation)*
>   Fine for tiny, reversible edits. Risks cross-session staging collisions if another session is active.

## Scope → Prompt Matrix

| Scope | Definition | Prompt? | Default suggestion |
|-------|-----------|---------|-------------------|
| TRIVIAL | 1 file, <50 lines | No | Run here (C) |
| LOW | 1 component | No | Run here (C) |
| MEDIUM | Multiple components, same domain | Yes | A (sub-agent) |
| HIGH | 5+ files, cross-domain | Yes | A or B |
| EPIC | Multi-session | Yes | B (manual — needs interactive steering) |

## Parallelizability Check

Before showing the prompt, assess: does this task have **independent sub-tasks that could run simultaneously**? If yes, state that in the prompt and bias toward A. If no, say "sequential."

**Signals of parallelizability**:
- Multiple files in different modules with no shared state
- Independent plan phases
- Batch operations (N regex fixes, N doc updates)

**Signals of sequential-only**:
- Later step depends on earlier step's output
- Single file with multiple coupled edits
- Debugging / investigation workflows

## If User Picks B — Required Follow-Up

After running the `/git-using-worktrees` flow, tell the user:

> Worktree ready at `worktrees/<slug>/`.
> Branch: `cc/<timestamp>/<slug>`.
>
> **This current Claude Code session CANNOT follow into the worktree.** To work there:
> 1. Open a new terminal OR a new VS Code window at `worktrees/<slug>/`.
> 2. Start a fresh Claude Code session in that window.
> 3. That session is isolated — all its commits land on the feature branch.
>
> When done, merge with `/git-worktree-merge` from the main repo folder.

## Opt-Out

User can disable the prompt per-session by saying "skip worktree prompts" or "just run it." Respect that for the rest of the session. Do not persist opt-out across sessions.

## Related

- `.claude/skills/git-using-worktrees/SKILL.md` — Pattern B mechanics
- `.claude/skills/git-worktree-merge/SKILL.md` — Merge-back workflow
- `.claude/rules/workflow-planning-with-files.md` — Plan creation before starting work
