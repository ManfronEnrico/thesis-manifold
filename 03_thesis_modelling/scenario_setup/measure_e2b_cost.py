#!/usr/bin/env python3
"""
Measure what one E2B sandbox actually costs, before scaling D/E.

WHY: E2B bills sandbox *runtime*, which is a different resource from the OpenAI
tokens `srq4_experiment.py` already logs. That harness cannot see E2B spend at
all, so extrapolating the D/E budget from the A/B/C figures would be guesswork --
exactly the "deterministic cost logging and not guesswork" this project rejected.

WHAT IT DOES: creates one sandbox, runs a short workload representative of what
Prometheus's coder writes (pandas + a fit), times each phase, and reports
seconds-per-run. Multiply by E2B's published per-second rate for the sandbox size
to get dollars.

It deliberately uses the DEFAULT sandbox, not the `prometheus` template. Building
that template costs real credit (apt-get + five pip layers on a 4 GB box), and
`PROMETHEUS_TEMPLATE_ID` is optional in the engine's code path
(`AsyncSandbox.create(None, ...)` is legal). So this measures the cheap case
first, and tells us whether the build is even necessary: if the probe reports
pyodbc missing, the template is required for warehouse access; if the workload
runs, per-run cost is known before any build spend.

Usage:
    python 03_thesis_modelling/scenario_setup/measure_e2b_cost.py
    python 03_thesis_modelling/scenario_setup/measure_e2b_cost.py --template prometheus
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))


def _load_env() -> None:
    """Read .env and map this project's key names onto the SDK's expected names.

    The dashboard label is `thesis_manifold_e2b_sandbox`; the SDK reads
    `E2B_API_KEY`. Same indirection the experiment harness uses for OpenAI.
    """
    for env_path in (_root / ".env", _root / "03_thesis_modelling" / ".env"):
        if not env_path.is_file():
            continue
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if v and k.strip() not in os.environ:
                os.environ[k.strip()] = v

    for src in ("thesis_manifold_e2b_sandbox", "E2B_API_KEY"):
        if os.environ.get(src) and not os.environ.get("E2B_API_KEY"):
            os.environ["E2B_API_KEY"] = os.environ[src]


# A workload shaped like what the coder agent actually writes: load a frame,
# aggregate, fit something small. Deliberately NOT a trivial `print()` -- an
# empty sandbox would understate the runtime a real scenario pays for.
PROBE = """
import time, sys
t0 = time.time()
import pandas as pd, numpy as np
print("pandas", pd.__version__)

# Availability probe: these are what prometheus.yaml installs and what a
# warehouse query would need. Their absence is the finding, not an error.
for mod in ("pyodbc", "sqlalchemy", "statsmodels", "xgboost", "prophet"):
    try:
        __import__(mod)
        print(f"HAVE {mod}")
    except ImportError:
        print(f"MISSING {mod}")

# Representative work: a small panel + a fit.
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "brand": np.repeat([f"B{i}" for i in range(20)], 40),
    "t": np.tile(np.arange(40), 20),
})
df["y"] = rng.lognormal(8, 1.2, len(df))
df["lag_1"] = df.groupby("brand").y.shift(1)
d = df.dropna()
coef = np.polyfit(d.lag_1.values, d.y.values, 1)
print(f"rows={len(d)} slope={coef[0]:.4f}")
print(f"ELAPSED_IN_SANDBOX={time.time()-t0:.2f}")
"""


async def main_async(template: str | None, keep_open: float) -> int:
    from e2b_code_interpreter import AsyncSandbox

    print("=" * 70)
    print(f"E2B cost probe -- template: {template or 'DEFAULT (no template)'}")
    print("=" * 70)

    t_create = time.time()
    sbx = await AsyncSandbox.create(template, timeout=600)
    create_s = time.time() - t_create
    print(f"\n[1] sandbox created in {create_s:6.2f}s  (id={sbx.sandbox_id})")

    try:
        t_run = time.time()
        ex = await sbx.run_code(PROBE)
        run_s = time.time() - t_run
        print(f"[2] code executed in  {run_s:6.2f}s\n")

        if ex.error:
            print(f"    ERROR: {ex.error}")
        for log in (ex.logs.stdout or []):
            print(f"    | {log.rstrip()}")

        if keep_open:
            # The engine holds a sandbox for up to `timeout=600` and reuses it
            # across calls, so wall-clock lifetime -- not execution time -- is
            # what bills. This models that.
            print(f"\n[3] holding sandbox open {keep_open:.0f}s to model reuse...")
            import asyncio
            await asyncio.sleep(keep_open)
    finally:
        t_kill = time.time()
        await sbx.kill()
        print(f"\n[4] sandbox killed in  {time.time()-t_kill:6.2f}s")

    total = time.time() - t_create
    print("\n" + "=" * 70)
    print(f"BILLABLE WALL CLOCK: {total:.2f}s for one sandbox lifecycle")
    print("=" * 70)
    print("""
To convert to dollars: multiply by E2B's per-second rate for this sandbox size
(dashboard -> Usage). Then, per D/E run, note that the engine REUSES one sandbox
across a conversation via ctx.deps.state["code_interpreter_id"], so cost tracks
distinct sandbox creations, not tool calls -- but its timeout is 600s, so an
idle-but-open sandbox still bills.

Record the measured figure in
plans/P0040_2026-08-20_prometheus-scenarios-d-e/findings.md (F37) before
choosing a repeat count.""")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure one E2B sandbox lifecycle")
    ap.add_argument("--template", default=None,
                    help="template alias (default: none -- E2B's base image, "
                         "which costs nothing to build)")
    ap.add_argument("--keep-open", type=float, default=0.0,
                    help="seconds to hold the sandbox open, modelling the "
                         "engine's reuse window (default 0)")
    a = ap.parse_args()

    _load_env()
    if not os.environ.get("E2B_API_KEY"):
        print("ERROR: no E2B key. Expected `thesis_manifold_e2b_sandbox` or "
              "`E2B_API_KEY` in .env", file=sys.stderr)
        return 2

    try:
        from e2b_code_interpreter import AsyncSandbox  # noqa: F401
    except ImportError:
        print("ERROR: e2b-code-interpreter not installed.\n"
              "  .venv\\Scripts\\python.exe -m pip install "
              "e2b-code-interpreter e2b", file=sys.stderr)
        return 2

    import asyncio
    return asyncio.run(main_async(a.template, a.keep_open))


if __name__ == "__main__":
    sys.exit(main())
