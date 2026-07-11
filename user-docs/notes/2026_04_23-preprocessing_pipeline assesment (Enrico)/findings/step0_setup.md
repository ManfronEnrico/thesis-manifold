# Step 0 — Setup

**Goal**: import dependencies, set project root on `sys.path`, verify the
Nielsen DB connector loads `.env` correctly.

## Findings

- The `.env` file at the repo root contains all credentials needed for the
  Nielsen Fabric service principal (`RU_*`) plus Anthropic API + Zotero +
  Google Drive service account (added later in the session for completeness).
- `nielsen_connector.get_connection()` automatically loads `.env` via
  python-dotenv at import time.
- `tabulate` is required by `preprocessing.py` (uses `df.to_markdown()`) and
  was missing from the `.venv`. Installed via `uv pip install tabulate`.
- The repo uses `uv` (not pip) for dependency management — `uv.lock` is
  authoritative. To add deps cleanly: `uv add tabulate`.

## Pre-conditions

- Active virtualenv at `.venv/` (Python 3.13).
- DB credentials valid in `.env` (verified by a successful `get_connection()`
  call in step 1).
