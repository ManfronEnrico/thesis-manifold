# Cheatsheet — Manifold AI Thesis

Quick reference for common commands, workflows, and conventions.

---

## Environment Setup

```bash
# Set Anthropic API key (required for all LLM calls)
export ANTHROPIC_API_KEY=sk-ant-...

# Persist across sessions (add to ~/.zshrc or ~/.bashrc)
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
source ~/.zshrc

# Verify key is set
echo $ANTHROPIC_API_KEY
```

---

## Claude Code

```bash
# Start a Claude Code session (always run from project root)
cd "Thesis Maniflod"
claude

# Useful slash commands inside Claude Code
/clear          # Clear context — use at every task change
/compact        # Compress context — use when >50% full
/help           # Show all available commands
/REV            # Activate REV agent (academic paper → Obsidian note)

# REV agent (inline activation)
# Start your message with _REV followed by paper content
_REV
[paste abstract + intro + conclusion here]
```

---

## Git & GitHub

### The Golden Rule
Always `git pull` before you start working. Always `git push` when you're done.
Never work directly on `main` — use your own branch.

---

### Everyday Workflow

```bash
# 1. Check what branch you are on and what has changed
git status
git branch                        # * marks your current branch

# 2. Get the latest changes from GitHub before starting work
git fetch --all                   # see what's changed remotely (safe, no edits applied)
git pull                          # apply those changes to your current branch

# 3. Stage your changes (choose what to include in the commit)
git add Thesis/papers/my_note.md  # add a specific file
git add Thesis/papers/            # add an entire folder
git add -p                        # interactive — review each change before staging

# 4. Commit (save a snapshot locally)
git commit -m "Add annotated note: Schick et al. (2023) Toolformer"

# 5. Push (upload to GitHub so your colleague can see it)
git push
```

---

### Branching — Working Without Stepping on Each Other

```bash
# See all branches (local + remote)
git branch -a

# Switch to an existing branch
git checkout main
git checkout brian/rev-brian-command

# Create a new branch and switch to it
git checkout -b brian/new-feature

# Push a new branch to GitHub for the first time
git push -u origin brian/new-feature   # only needed once; plain `git push` works after
```

---

### Merging Your Branch into Main

```bash
# Step 1 — switch to main and get the latest version
git checkout main
git pull

# Step 2 — merge your branch in
git merge brian/rev-brian-command

# Step 3 — push the updated main to GitHub
git push
```

---

### Keeping Your Branch Up to Date with Main

Run this when your colleague has pushed changes to `main` that you want in your branch:

```bash
git checkout brian/rev-brian-command   # make sure you're on your branch
git fetch --all                        # get latest remote state
git merge origin/main                  # bring main's changes into your branch
```

---

### Checking What Has Changed

```bash
git log --oneline -10             # last 10 commits, compact view
git diff                          # unstaged changes (what you've edited but not staged)
git diff --staged                 # staged changes (what will go into the next commit)
git diff main..brian/rev-brian-command  # compare two branches
```

---

### Undoing Mistakes

```bash
# Undo the last commit but KEEP your file changes (safest option)
git reset --soft HEAD~1

# Discard changes to a specific file (revert to last committed version)
git checkout -- Thesis/papers/my_note.md

# See what's different between local and remote before pushing
git diff origin/main..HEAD
```

---

### Conflict Resolution (when two people edited the same file)

Git will mark conflicts inside the file like this:

```
<<<<<<< HEAD
your version of the line
=======
your colleague's version of the line
>>>>>>> origin/main
```

1. Open the file, delete the conflict markers, and keep the correct version.
2. Then:

```bash
git add the_conflicted_file.md
git commit -m "Resolve merge conflict in [filename]"
git push
```

---

### Quick Reference Card

| Task | Command |
|---|---|
| What branch am I on? | `git branch` |
| What files have changed? | `git status` |
| Get latest from GitHub | `git fetch --all` then `git pull` |
| Stage a file | `git add path/to/file` |
| Commit staged changes | `git commit -m "message"` |
| Upload to GitHub | `git push` |
| Switch branch | `git checkout branch-name` |
| Create new branch | `git checkout -b branch-name` |
| Merge branch into main | `git checkout main` → `git merge branch-name` → `git push` |
| Undo last commit (keep files) | `git reset --soft HEAD~1` |

---

## Dependencies

```bash
# Install System A dependencies (research framework)
pip install -r ai_research_framework/requirements.txt

# Install System B dependencies (thesis production)
pip install -r thesis_production_system/requirements.txt

# Install figure generation tools
pip install graphviz matplotlib
brew install graphviz   # macOS — required for graphviz Python package

# Install Prophet on Apple Silicon (if install fails)
brew install cmake
pip install prophet

# Check installed packages
pip list | grep -E "langgraph|pydantic|anthropic|lightgbm|prophet"
```

---

## Generate Figures

```bash
# Generate all 6 architecture diagrams (SVG + PNG)
python generate_figures.py

# Output location
ls docs/thesis/figures/
# system_architecture_v1.svg/.png
# agent_workflow_v1.svg/.png
# data_flow_v1.svg/.png
# ram_budget_v1.svg/.png
# confidence_score_v1.svg/.png
# project_overview_v1.svg/.png
```

---

## Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run Builder Agent integration tests only
python -m pytest tests/test_builder_integration.py -v

# Run with output (see print statements)
python -m pytest tests/ -v -s

# Run a specific test class
python -m pytest tests/test_builder_integration.py::BuilderGraphTests -v
```

---

## System A — Research Framework

```python
# Run the full research pipeline (requires data access)
from ai_research_framework.core.coordinator import build_coordinator
from ai_research_framework.state.research_state import ResearchState

coordinator = build_coordinator()
initial_state: ResearchState = {
    "current_phase": "data_assessment",
    "ram_budget_mb": 8192,
    "errors": [],
    "requires_human_approval": False,
}
result = coordinator.invoke(initial_state)

# Check RAM budget configuration
from ai_research_framework.config import RAM_BUDGET_MB, MODEL_RAM_BUDGET
print(f"Total budget: {RAM_BUDGET_MB} MB")
print(MODEL_RAM_BUDGET)

# Run a single agent (e.g. DataAssessmentAgent)
from ai_research_framework.agents.data_assessment_agent import DataAssessmentAgent
agent = DataAssessmentAgent()
result = agent.run(state)
```

---

## System B — Thesis Production

```python
# Run the thesis production coordinator
from pathlib import Path
from thesis_production_system.core.coordinator import ThesisCoordinator
from thesis_production_system.state.thesis_state import ThesisState

coordinator = ThesisCoordinator(project_root=Path("."))
state = ThesisState.load("docs/tasks/thesis_state.json")
coordinator.run(state)

# Load and inspect thesis state
import json
with open("docs/tasks/thesis_state.json") as f:
    state = json.load(f)
print(state.keys())

# Check section status
for section, data in state.get("sections", {}).items():
    print(f"{section}: {data.get('status')}")
```

---

## Literature Management

```bash
# View confirmed papers
ls docs/literature/papers/

# Count confirmed papers
ls docs/literature/papers/ | wc -l

# Search across all paper notes
grep -r "LightGBM" docs/literature/papers/
grep -r "SRQ1" docs/literature/papers/

# View gap analysis
cat docs/literature/gap_analysis.md

# View RQ evolution history
cat docs/literature/rq_evolution.md

# View scraping log
cat docs/literature/scraping_log.md
```

---

## Thesis Sections

```bash
# View all chapter bullet skeletons
ls docs/thesis/sections/

# Read a specific chapter
cat docs/thesis/sections/ch5_framework_design.md
cat docs/thesis/sections/ch2_literature_review.md

# Check compliance report
cat docs/compliance/compliance_checks/compliance_report_20260315.md

# Check CBS guidelines notes
cat docs/compliance/cbs_guidelines_notes.md

# View thesis outline
cat docs/thesis/outline.md
```

---

## Experiment Tracking

```bash
# View experiment registry
cat docs/experiments/experiment_registry.json | python -m json.tool

# View experiment summary
cat docs/experiments/experiment_summary.md

# Count experiments run
cat docs/experiments/experiment_registry.json | python -c "
import json, sys
data = json.load(sys.stdin)
print(f'Total experiments: {len(data.get(\"experiments\", []))}')
"
```

---

## Memory Profiling (for SRQ1)

```python
# Profile RAM usage of a function
from memory_profiler import memory_usage
import tracemalloc

# Method 1 — memory_profiler
mem_usage = memory_usage((my_function, (args,)), interval=0.1)
print(f"Peak RAM: {max(mem_usage):.1f} MB")

# Method 2 — tracemalloc (built-in)
tracemalloc.start()
my_function()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Peak RAM: {peak / 1024 / 1024:.1f} MB")

# Check if within budget
from ai_research_framework.config import RAM_BUDGET_MB
assert peak_mb < RAM_BUDGET_MB, f"RAM exceeded: {peak_mb} MB > {RAM_BUDGET_MB} MB"
```

---

## Key File Locations

| What | Path |
|---|---|
| Master project instructions | `CLAUDE.md` |
| Session log | `docs/context.md` |
| Research state definition | `ai_research_framework/state/research_state.py` |
| RAM budget config | `ai_research_framework/config.py` |
| System A coordinator | `ai_research_framework/core/coordinator.py` |
| System B coordinator | `thesis_production_system/core/coordinator.py` |
| Thesis state (JSON) | `docs/tasks/thesis_state.json` |
| Architecture report | `docs/system_architecture_report.md` |
| Gap analysis | `docs/literature/gap_analysis.md` |
| Thesis outline | `docs/thesis/outline.md` |
| Chapter skeletons | `docs/thesis/sections/` |
| Compliance notes | `docs/compliance/cbs_guidelines_notes.md` |
| Experiment registry | `docs/experiments/experiment_registry.json` |

---

## Workflow Rules (Important)

```
1. Every phase transition requires explicit human approval — never proceed autonomously
2. WritingAgent produces ONLY bullet points — prose requires human sign-off
3. Use /clear at every task change
4. Use /compact when context exceeds 50% of window
5. Use Opus for architecture, literature, and complex decisions
6. Use Sonnet for standard development and bullet point writing
7. Never commit .env files or actual data (Nielsen / Indeks Danmark)
8. Document every new package installation in docs/context.md
9. System B never modifies System A logic
10. Coordinator is the sole decision-maker on task order
```

---

## CBS Compliance Quick Reference

| Rule | Value |
|---|---|
| Total pages (group thesis) | 120 standard pages |
| Standard page | 2,275 characters (incl. spaces) |
| Appendices / bibliography | Excluded from count |
| Citation format | APA 7th edition |
| Abstract | Counts toward page limit |
| AI usage declaration | Mandatory |

---

## Common Troubleshooting

```bash
# API key not found
echo $ANTHROPIC_API_KEY        # should print your key
export ANTHROPIC_API_KEY=...   # re-set if empty

# Prophet install fails on macOS
brew install cmake
pip install prophet

# Graphviz import error
brew install graphviz
pip install graphviz

# LangGraph version conflict
pip install "langgraph>=0.2.0" --upgrade

# Check Python version (requires 3.11+)
python --version

# Kill a runaway process (e.g. stuck Builder trial)
# Find PID:
ps aux | grep python
# Kill:
kill -9 [PID]
```
