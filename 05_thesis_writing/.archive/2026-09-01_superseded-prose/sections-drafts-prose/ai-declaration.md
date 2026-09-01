# AI Use Declaration
> CBS requirement: Autumn 2025 rules — must declare use of AI when required by course/programme
> Placement: confirm with supervisor — likely in front matter (before abstract) or as a mandatory appendix
> Status: DRAFT — requires supervisor confirmation on required format
> Last updated: 2026-03-15

---

## Draft text (bullet form — NOT prose yet)

### Heading
"Use of Artificial Intelligence in This Thesis"

### What AI was used for (declaration bullets)
- **Claude claude-sonnet-4-6 (Anthropic)** was used as a research component:
  - As the Synthesis Agent's natural language generation engine — integrated into the multi-agent framework as an API call (see Chapter 7). This is NOT an assistive use; it is the research object/artefact itself.
  - Temperature: 0 (deterministic outputs); all prompts and outputs logged for reproducibility
- **Claude Code (Anthropic CLI)** was used as a software development assistant during implementation:
  - Assisted with Python code scaffolding for System A (LangGraph, forecasting agents, synthesis pipeline)
  - Assisted with System B thesis production scaffolding (diagram generation scripts, compliance checks)
  - All code reviewed and verified by the authors; final implementation decisions are the authors' own
- **No AI tools were used to generate thesis prose**: all written text (arguments, analysis, discussion) was written by the authors

### What AI was NOT used for
- Literature search and evaluation — done manually by the authors using CBS library resources
- Data analysis interpretation — conducted by the authors based on empirical results
- Thesis argumentation, conclusions, or theoretical contributions — authored independently

### Transparency note
- The use of Claude API as a system component (Synthesis Agent) is the thesis's primary research contribution — its behaviour, limitations, and evaluation are central to the thesis
- Source code for all AI integrations is included in Appendix [X] and the project repository

---

## Placement options (confirm with supervisor)

| Option | Placement | Pros | Cons |
|---|---|---|---|
| A | Front matter (before abstract) | Maximum visibility; signals transparency | May be unusual format for CBS programme |
| B | End of Chapter 3 (Methodology) | Contextually appropriate; fits research design | Buried; examiners may miss it |
| C | Mandatory appendix | Doesn't use page budget | CBS may require it in main text |

**Recommended**: Option A — place in front matter, before abstract, clearly labelled.

---

## Outstanding
- [ ] Confirm with supervisor: required format and placement per programme rules
- [ ] Confirm whether Anthropic/Claude must be cited as a tool (APA 7 software citation format)
- [ ] Confirm scope: does declaration need to cover ALL AI use or only AI in the research object?
