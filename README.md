# Manifold AI Thesis — Predictive Analytics Framework

> **Master's Thesis** — Business Administration & Data Science
> Copenhagen Business School (CBS), in collaboration with Manifold AI
> **Group thesis** — 2 students — 120 pages — Deadline: 15 May 2026

---

## Research Question

> *How can AI systems be designed to provide reliable, cost-justified predictive decision-support in real-world business environments under computational constraints?*

**Sub-questions:**
- **SRQ1** — Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints (≤8 GB RAM)?
- **SRQ2** — How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?
- **SRQ3** — To what extent does additional contextual information (Prometheus integration) improve the predictive and decision-support capabilities of AI systems? (Currently scoped as an integration-readiness assessment — Prometheus access pending.)
- **SRQ4** — How does the proposed predictive AI system compare to a code-as-action LLM baseline, on correctness/consistency/replicability (primary) and cost/latency (secondary)?

See [00_thesis_context/thesis-topic/project-state.md](00_thesis_context/thesis-topic/project-state.md) for the full list of frozen decisions and open questions, and [01_thesis_research/research-questions/](01_thesis_research/research-questions/) for the canonical RQ text.

---

## Repo Structure

**As of 2026-07-11**, the repo root is organized into six numbered thesis tiers plus supporting tooling/docs folders. Full authoritative reference: [.claude/rules/repo-tier-structure.md](.claude/rules/repo-tier-structure.md).

| Tier | Purpose |
|------|---------|
| [00_thesis_context/](00_thesis_context/) | Thesis topic, scope, frozen decisions, CBS compliance |
| [01_thesis_research/](01_thesis_research/) | Research questions, literature corpus |
| [02_thesis_data/](02_thesis_data/) | Data pipeline: raw → converted → preprocessed → engineered |
| [03_thesis_modelling/](03_thesis_modelling/) | Model training scripts + serving code (System A/B) |
| [04_thesis_results/](04_thesis_results/) | Final SRQ1/SRQ2/SRQ4 results |
| [05_thesis_writing/](05_thesis_writing/) | Thesis chapter drafts, final sections, figures |

| Other folder | Purpose |
|---|---|
| `utility_scripts/` | Tooling-only helper scripts (not thesis content) |
| `user-docs/` | Architecture, integration guides, handovers, reference docs |
| `plans/` | Dated P-ID session plan folders |
| `.claude/` | Claude Code rules, skills, agents, commands |

---

## What This Repository Contains

Two systems that must not be confused:

| System | Location | Purpose | In Thesis? |
|---|---|---|---|
| **System A** — Research Framework | `03_thesis_modelling/model_serving/system_a_forecast/` + `model_training/` | The multi-agent forecasting system being studied and evaluated (SRQ1/SRQ2) | ✅ Yes |
| **System B** — Thesis Production | `03_thesis_modelling/model_serving/system_b_conversational/` + `.claude/` agents/skills | Internal tooling for writing and managing the thesis | ❌ No — invisible to reader |

> ⚠️ **System B never modifies System A logic.** System A is the research object; System B supports the writing process.

### System A — AI Research Framework

**Hard constraint: ≤ 8 GB RAM total** — every architectural decision is justified against this.

Models benchmarked (SRQ1): AutoARIMA, Prophet, LightGBM, XGBoost, Ridge — run **sequentially**, never in parallel, to stay within budget. Current baselines: XGBoost 45.5% median MAPE (test), LightGBM 46.7% median MAPE (test) — see `02_thesis_data/preprocessing/` and `03_thesis_modelling/model_training/` for the benchmark scripts.

### Data Sources

| Dataset | Format | Status |
|---|---|---|
| Nielsen/Prometheus CSD | Power BI/Fabric API exports (JSONL → Parquet → engineered) | ✅ Active — see [02_thesis_data/nielsen/](02_thesis_data/nielsen/) |
| Indeks Danmark | Consumer-survey CSV | ❌ Dropped from scope (2026-06-19) — not used |

---

## Setup

### Prerequisites

- Python 3.11+
- An **Anthropic API key** (required for all LLM agent calls)

### 1. Clone the repository

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold
```

### 2. Configure credentials

Copy the `.env` template and fill in values (ask your co-author for the Nielsen credentials):

```bash
cp .env.example .env   # then open .env and fill in all values
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or, if using uv:
uv sync
```

### 4. Install Claude Code and GitHub CLI (for AI-assisted development)

```bash
npm install -g @anthropic-ai/claude-code
claude  # run from project root
```

**GitHub CLI** (`gh`) is required for creating draft PRs at the end of each session:

```powershell
# Windows (PowerShell) — run once, then restart your terminal
winget install --id GitHub.cli
```

After restarting, authenticate with your own GitHub account (one-time setup per machine):

```powershell
gh auth login
# Choose: GitHub.com → HTTPS → Yes → Login with web browser
```

> Each collaborator runs this independently with their own account. `gh` is a system tool, not a Python package.

### 5. Generate architecture figures

```bash
pip install graphviz matplotlib
python utility_scripts/scripts/generate_figures.py
# Output: 05_thesis_writing/figures/*.svg and *.png
```

---

## Running Tests

```bash
python -m pytest utility_scripts/ -v
```

---

## Workflow Phases

Every phase transition requires **explicit human approval** before proceeding.

```
Phase 0 — Setup & pre-start checklist                         [Complete]
Phase 1 — Literature Review & Gap Analysis                    [Complete]
Phase 2 — Data Assessment & Preprocessing                     [Complete]
Phase 3 — SRQ1: Model Selection & Benchmark                   [Complete]
Phase 4 — SRQ2: Synthesis Module                              [In progress]
Phase 5 — SRQ3/SRQ4: Evaluation & Validation                  [In progress]
Phase 6 — Thesis Writing            [bullets only → human approval → prose]
```

See [00_thesis_context/thesis-topic/project-state.md](00_thesis_context/thesis-topic/project-state.md) for the current TODO list and risk flags.

---

## Key Documents

| Document | Location | Purpose |
|---|---|---|
| Master instructions | `CLAUDE.md` | Read by Claude Code at every session |
| Agent instructions | `AGENTS.md` | Same navigation hub, for non-Claude-Code agents |
| Repo tier structure | `.claude/rules/repo-tier-structure.md` | Authoritative folder-layout reference |
| Repository map | `user-docs/contributing/repository_map.md` | File-to-purpose mapping |
| Project state | `00_thesis_context/thesis-topic/project-state.md` | Frozen decisions, open questions, TODOs |
| Formal requirements | `00_thesis_context/formal-requirements/` | CBS compliance checks |
| Research questions | `01_thesis_research/research-questions/` | Canonical RQ text (v4) |

---

## CBS Compliance Notes

- **Page limit**: 120 standard pages (group thesis, 2 students)
- **Standard page**: 2,275 characters including spaces
- **Excluded from count**: appendices, bibliography
- **Citation format**: APA 7th edition
- All sections checked against CBS guideline PDFs — see `00_thesis_context/formal-requirements/`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph (System A) + custom coordinator (System B) |
| LLM | Claude API |
| ML / Forecasting | pmdarima, Prophet, LightGBM, XGBoost, scikit-learn |
| Data | Nielsen/Prometheus SQL star schema (JSONL → Parquet pipeline) |
| Figures | Graphviz + Matplotlib |
| Runtime | Local Python 3.11 |

---

## Security Notes

- **Never commit** actual Nielsen data — `.gitignore` enforces this
- `ANTHROPIC_API_KEY` must be set as an environment variable — never hardcoded
- Nielsen dataset must not leave the local environment (confidentiality agreement)
