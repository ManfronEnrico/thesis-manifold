#!/usr/bin/env python
"""Measure peak memory INSIDE the production sandbox, not on the dev machine.

WHY THIS EXISTS
---------------
The thesis claims the forecasting substrate operates within a 4096 MB budget.
That budget is the measured allocation of Manifold's production E2B template
(alias `prometheus`), but every figure supporting the claim was measured
locally, by `srq1_profiling.py`, on a developer workstation.

A budget claim about a deployment, evidenced only on a laptop, is an assertion
about the wrong machine. Local RSS and in-sandbox RSS can differ for reasons
that matter: a different CPU count changes how many threads LightGBM and
XGBoost allocate histogram buffers for, a different BLAS build changes NumPy's
workspace, and the container's own baseline (interpreter, imported libraries)
is charged against the same budget the models must fit inside.

This script closes that gap. It runs the same fit inside the real template and
reports what the container actually charged, against the ceiling the container
actually has -- read from the sandbox rather than assumed.

Cost: one short sandbox lifecycle, billed by E2B at a per-second rate. Not free,
but on the order of a few cents, and it is the measurement that converts the
central resource claim from "our machine can do it" to "the deployment target
can".

Usage
-----
    # against the production template (what the thesis should cite)
    python 03_thesis_modelling/scenario_setup/measure_sandbox_rss.py

    # against E2B's base image, for comparison
    python 03_thesis_modelling/scenario_setup/measure_sandbox_rss.py --template ""

Writes: 04_thesis_results/srq1/sandbox_profiling.csv
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR  # noqa: E402

DEFAULT_TEMPLATE = os.environ.get("PROMETHEUS_TEMPLATE_ID", "prometheus")


def _load_env() -> None:
    """Read .env for the E2B key, matching the harness's own indirection."""
    root = Path(__file__).resolve().parents[2]
    f = root / ".env"
    if f.is_file():
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    for src in ("thesis_manifold_e2b_sandbox", "E2B_API_KEY"):
        if os.environ.get(src) and not os.environ.get("E2B_API_KEY"):
            os.environ["E2B_API_KEY"] = os.environ[src]


# The probe mirrors srq1_profiling.py's method so the two are comparable:
# peak RSS sampled by a poller thread during the fit, in an isolated process,
# because RSS does not return to baseline in-process and a sequential loop would
# charge each model with its predecessors' retained pages.
PROBE = r"""
import json, os, gc, threading, time, sys

def _peak_rss_during(fn):
    import psutil
    proc = psutil.Process()
    gc.collect()
    base = proc.memory_info().rss
    peak = base
    stop = threading.Event()
    def poll():
        nonlocal peak
        while not stop.is_set():
            try:
                r = proc.memory_info().rss
            except Exception:
                return
            if r > peak:
                peak = r
            stop.wait(0.005)
    t = threading.Thread(target=poll, daemon=True)
    t.start()
    t0 = time.perf_counter()
    try:
        out = fn()
    finally:
        stop.set(); t.join(timeout=1)
    return out, time.perf_counter() - t0, (peak - base) / 1e6, base / 1e6

import numpy as np, pandas as pd

# The container ceiling, read rather than assumed. cgroup v2 first, then v1.
def container_limit_mb():
    for p in ("/sys/fs/cgroup/memory.max",
              "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        try:
            v = open(p).read().strip()
            if v and v != "max":
                return int(v) / 1e6
        except Exception:
            pass
    try:
        import psutil
        return psutil.virtual_memory().total / 1e6
    except Exception:
        return None

res = {"limit_mb": container_limit_mb(), "cpus": os.cpu_count(), "models": []}

# Same shape as the CSD brand-by-month matrix: ~2470 rows, 13 features.
rng = np.random.default_rng(42)
n_brand, n_t = 95, 26
df = pd.DataFrame({"brand": np.repeat(np.arange(n_brand), n_t),
                   "t": np.tile(np.arange(n_t), n_brand)})
df["y"] = rng.lognormal(8, 1.2, len(df))
for i in range(1, 12):
    df[f"f{i}"] = rng.normal(0, 1, len(df))
feats = ["t"] + [f"f{i}" for i in range(1, 12)] + ["brand"]
X, y = df[feats].values, df["y"].values
res["n_train"], res["n_features"] = len(X), X.shape[1]

# Baseline: interpreter + libraries already imported, charged against the same
# budget the models must fit inside.
try:
    import psutil
    res["baseline_rss_mb"] = psutil.Process().memory_info().rss / 1e6
except Exception:
    res["baseline_rss_mb"] = None

def bench(name, fn):
    try:
        _, secs, peak, base = _peak_rss_during(fn)
        res["models"].append({"model": name, "fit_s": round(secs, 3),
                              "peak_fit_RSS_MB": round(peak, 1),
                              "process_rss_before_MB": round(base, 1)})
    except Exception as e:
        res["models"].append({"model": name, "error": str(e)[:200]})

try:
    from sklearn.linear_model import Ridge
    bench("Ridge", lambda: Ridge(alpha=1.0).fit(X, y))
except ImportError:
    res["models"].append({"model": "Ridge", "error": "sklearn missing"})

try:
    import lightgbm as lgb
    bench("LightGBM", lambda: lgb.LGBMRegressor(
        n_estimators=374, num_leaves=120, verbose=-1).fit(X, y))
except ImportError:
    res["models"].append({"model": "LightGBM", "error": "lightgbm missing"})

try:
    import xgboost as xgb
    bench("XGBoost", lambda: xgb.XGBRegressor(
        n_estimators=400, max_depth=6, verbosity=0).fit(X, y))
except ImportError:
    res["models"].append({"model": "XGBoost", "error": "xgboost missing"})

print("__RESULT__" + json.dumps(res))
"""


async def run(template: str | None) -> int:
    from e2b_code_interpreter import AsyncSandbox

    label = template or "DEFAULT (E2B base image)"
    print("=" * 72)
    print(f"In-sandbox memory probe -- template: {label}")
    print("=" * 72)

    t0 = time.time()
    sbx = await AsyncSandbox.create(template, timeout=600)
    print(f"\n[1] sandbox created in {time.time()-t0:5.2f}s (id={sbx.sandbox_id})")
    try:
        t1 = time.time()
        ex = await sbx.run_code(PROBE)
        print(f"[2] probe executed in {time.time()-t1:5.2f}s\n")
        if ex.error:
            print(f"    ERROR: {ex.error}")
            return 1
        payload = None
        for log in (ex.logs.stdout or []):
            if log.startswith("__RESULT__"):
                payload = json.loads(log[len("__RESULT__"):])
            else:
                print(f"    | {log.rstrip()}")
    finally:
        await sbx.kill()
        print(f"[3] sandbox killed (lifecycle {time.time()-t0:.2f}s billable)")

    if not payload:
        print("\nNo result payload returned.")
        return 1

    limit = payload.get("limit_mb")
    base = payload.get("baseline_rss_mb")
    print("\n" + "=" * 72)
    print(f"Container limit : {limit:,.0f} MB" if limit else "Container limit : unknown")
    print(f"CPUs            : {payload.get('cpus')}")
    if base:
        print(f"Baseline RSS    : {base:,.1f} MB "
              f"({base/limit*100:.2f}% of limit)" if limit else "")
    print(f"Training rows   : {payload.get('n_train')} x {payload.get('n_features')} features")
    print("-" * 72)
    print(f"{'model':<12}{'fit_s':>10}{'peak RSS MB':>14}{'% of limit':>13}")
    print("-" * 72)

    rows = []
    for m in payload["models"]:
        if "error" in m:
            print(f"{m['model']:<12}{'--':>10}{m['error'][:30]:>28}")
            rows.append({"template": label, "model": m["model"],
                         "error": m["error"], "container_limit_mb": limit})
            continue
        pct = (m["peak_fit_RSS_MB"] / limit * 100) if limit else None
        print(f"{m['model']:<12}{m['fit_s']:>10.3f}{m['peak_fit_RSS_MB']:>14.1f}"
              f"{(f'{pct:.2f}%' if pct else '--'):>13}")
        rows.append({"template": label, "model": m["model"],
                     "fit_s": m["fit_s"], "peak_fit_RSS_MB": m["peak_fit_RSS_MB"],
                     "container_limit_mb": limit,
                     "pct_of_limit": round(pct, 3) if pct else None,
                     "baseline_rss_mb": round(base, 1) if base else None,
                     "cpus": payload.get("cpus"),
                     "n_train": payload.get("n_train"),
                     "n_features": payload.get("n_features")})
    print("=" * 72)

    import pandas as pd
    out = THESIS_RESULTS_SRQ1_DIR / "sandbox_profiling.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8")
    print(f"\nSaved {out}")
    print("\nThis measures the DEPLOYMENT target. Cite it alongside the local "
          "profiling table, not instead of it: the two together show the "
          "footprint is not an artefact of the development machine.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Measure peak RSS inside the production E2B sandbox")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE,
                    help="template alias (default: %(default)s). Pass an empty "
                         "string to probe E2B's base image instead.")
    a = ap.parse_args()

    _load_env()
    if not os.environ.get("E2B_API_KEY"):
        print("E2B_API_KEY not set (checked .env and thesis_manifold_e2b_sandbox).")
        return 2
    return asyncio.run(run(a.template or None))


if __name__ == "__main__":
    raise SystemExit(main())
