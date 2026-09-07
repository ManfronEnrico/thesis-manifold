"""
Horizon selection for the SRQ1 scripts.
=======================================

One place that answers two questions every SRQ1 script has to ask:

  * which feature matrix do I read?
  * where do my results go?

Both come from ONE value, so they cannot drift apart. That drift is exactly the
defect this module was written to close (P0049 F22/F23/F24): `--horizon` used to
reach filenames and contracts but not the features themselves, and the thesis
reported one-month accuracy while describing three-month.

WHY H=3 KEEPS THE UNSUFFIXED PATHS
----------------------------------
H=3 is the primary reported horizon -- a quarter is the period in which marketing
budgets are authorised, so it is the first horizon at which a campaign decision is
actually taken. It therefore writes where it always has:

    05_thesis_results/model_benchmark/{tables,figures,models}/

H=1 writes to a parallel subtree:

    05_thesis_results/model_benchmark/h1/{tables,figures,models}/

This asymmetry is deliberate. `forecast_tool.py`, the SRQ4 harness, the appendix
exporter and the figure generators all read the unsuffixed paths; moving the
primary horizon would break every one of them to gain nothing. The secondary
horizon is the one that needs somewhere new to live.

The consequence that matters: **an H=1 run can never overwrite an H=3 result.**
Before this module, every SRQ1 script hardcoded `_h3` as its input while writing
to a single shared output directory, so pointing one at h1 data would have
silently replaced the published H=3 tables with H=1 numbers under H=3 filenames.

HOW A SCRIPT USES IT
--------------------
    from _horizon import HORIZON, matrix_path, results_root

    OUT = _SRQ1Out(results_root())          # instead of THESIS_RESULTS_SRQ1_DIR
    fm  = pd.read_parquet(matrix_path(cat, slug))

The horizon comes from the SRQ1_HORIZON environment variable, defaulting to 3.
An env var rather than a flag because these scripts already have heterogeneous
argparse setups (several have none at all), and a run must not depend on whether
a given script remembered to define `--horizon`. `run_both_horizons.py` sets it.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").exists()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from PATHS import (  # noqa: E402
    THESIS_DATA_ENGINEERED_BYMONTH_DIR,
    THESIS_RESULTS_SRQ1_DIR,
)

# Horizons this project reports. Adding one means generating its matrices in
# preprocessing first -- the list is not a promise that the data exists.
SUPPORTED = (1, 3)

# The primary reported horizon, and the one that owns the unsuffixed paths.
PRIMARY = 3

_ENV = "SRQ1_HORIZON"


def _resolve() -> int:
    raw = os.environ.get(_ENV)
    if raw is None or str(raw).strip() == "":
        return PRIMARY
    try:
        h = int(str(raw).strip())
    except ValueError:
        raise SystemExit(
            f"{_ENV}={raw!r} is not an integer. Supported: {SUPPORTED}.")
    if h not in SUPPORTED:
        raise SystemExit(
            f"{_ENV}={h} is not a supported horizon. Supported: {SUPPORTED}.\n"
            f"A horizon needs its feature matrices built by preprocessing "
            f"step 4 before any SRQ1 script can read them.")
    return h


HORIZON: int = _resolve()


def matrix_path(category: str, slug: str, base: Path | None = None) -> Path:
    """The engineered feature matrix for `category` at the active horizon.

    `base` overrides the engineered root for the scripts that select among
    several dataset roots (`DATASETS[ds]`); everything else takes the default.
    """
    sub = "CSD" if category == "CSD" else category
    root = THESIS_DATA_ENGINEERED_BYMONTH_DIR if base is None else base
    return root / sub / f"{slug}_feature_matrix_h{HORIZON}.parquet"


def results_root() -> Path:
    """Where results for the active horizon go.

    The primary horizon keeps the unsuffixed tier root so every existing
    consumer keeps working; a secondary horizon gets its own subtree.
    """
    if HORIZON == PRIMARY:
        return THESIS_RESULTS_SRQ1_DIR
    d = THESIS_RESULTS_SRQ1_DIR / f"h{HORIZON}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def label() -> str:
    """Short human label for console banners and table captions."""
    return f"H={HORIZON}" + (" (primary)" if HORIZON == PRIMARY else " (secondary)")


def banner() -> str:
    """One line naming the horizon and where its output lands.

    Printed by every script that runs at a horizon, because a results directory
    that silently depends on an environment variable is a directory someone will
    eventually misread.
    """
    return f"[horizon] {label()}  ->  {results_root()}"
