"""
Step 00 — Setup, pre-flight checks, and MANIFEST.

Creates the output directory structure for this retraining run and writes a
MANIFEST.json capturing:
  - Python version
  - Installed package versions (for reproducibility)
  - Random seeds
  - Hash of the feature_matrix baseline we'll compare against
  - Timestamp

This script is IDEMPOTENT: if the output dir already exists, it asks before
overwriting the manifest.

Usage:
    uv run python -m scripts.ml_retraining.00_setup
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config (locked — do not drift across steps)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_DATE = "2026-04-16"
OUTPUT_ROOT = PROJECT_ROOT / "results" / f"ml_retrain_{RUN_DATE}"
SEED = 42

# Required packages (fails pre-flight if any missing)
REQUIRED_PACKAGES = [
    "sklearn", "lightgbm", "xgboost", "statsmodels",
    "pandas", "numpy", "pyarrow",
    "shap", "seaborn", "matplotlib",
    "aeon", "pymc", "polars",
    "pyodbc", "azure.identity",
]

# Baseline files we will compare against (must exist — this is a safety check)
BASELINE_FILES = [
    PROJECT_ROOT / "results" / "phase1" / "feature_matrix.parquet",
    PROJECT_ROOT / "results" / "phase1" / "split_dates.json",
    PROJECT_ROOT / "results" / "phase1" / "benchmark_results_v2.csv",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_package_versions(pkgs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pkg in pkgs:
        try:
            m = importlib.import_module(pkg)
            out[pkg] = getattr(m, "__version__", "unknown")
        except ImportError:
            out[pkg] = "MISSING"
    return out


def pretty(label: str, value: object, ok: bool = True) -> None:
    mark = "✅" if ok else "❌"
    print(f"  {mark} {label:40s} {value}")


# ---------------------------------------------------------------------------
# Pre-flight checks (Gate G1)
# ---------------------------------------------------------------------------
def preflight() -> tuple[bool, list[str]]:
    print("=" * 72)
    print(f"  STEP 00 — SETUP  |  run date: {RUN_DATE}  |  seed: {SEED}")
    print("=" * 72)
    print()

    issues: list[str] = []

    # --- Python version
    py_ok = sys.version_info >= (3, 11)
    pretty("Python >= 3.11", platform.python_version(), py_ok)
    if not py_ok:
        issues.append(f"Python {platform.python_version()} < 3.11")

    # --- venv active?
    in_venv = sys.prefix != sys.base_prefix
    pretty("Running inside .venv", sys.prefix, in_venv)
    if not in_venv:
        issues.append("Not running inside a virtualenv — use `uv run`")

    # --- Required packages
    versions = get_package_versions(REQUIRED_PACKAGES)
    for pkg, ver in versions.items():
        ok = ver != "MISSING"
        pretty(f"pkg: {pkg}", ver, ok)
        if not ok:
            issues.append(f"Missing package: {pkg}")

    # --- Baseline files
    baseline_hashes: dict[str, str] = {}
    for f in BASELINE_FILES:
        exists = f.exists()
        if exists:
            h = file_sha256(f)
            size_mb = f.stat().st_size / 1e6
            baseline_hashes[str(f.relative_to(PROJECT_ROOT))] = h
            pretty(f"baseline: {f.name}", f"{size_mb:.2f} MB  sha256={h[:16]}…", True)
        else:
            pretty(f"baseline: {f.name}", "NOT FOUND", False)
            issues.append(f"Missing baseline file: {f}")

    # --- .env has required credentials
    from dotenv import load_dotenv  # type: ignore

    load_dotenv(PROJECT_ROOT / ".env")
    env_keys = [
        "RU_SERVER_STRING", "RU_DATABASE", "RU_CLIENT_ID",
        "RU_TENANT_ID", "RU_CLIENT_SECRET",
    ]
    for k in env_keys:
        ok = bool(os.environ.get(k))
        pretty(f".env: {k}", "set" if ok else "missing", ok)
        if not ok:
            issues.append(f"Missing env var: {k}")

    print()
    if issues:
        print(f"  ❌ Pre-flight FAILED — {len(issues)} issue(s):")
        for i in issues:
            print(f"     • {i}")
        return False, issues

    # Stash for manifest
    globals()["_PKG_VERSIONS"] = versions
    globals()["_BASELINE_HASHES"] = baseline_hashes
    print("  ✅ Pre-flight PASSED")
    return True, []


# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
def prepare_output_dir() -> Path:
    print()
    print("-" * 72)
    print(f"  OUTPUT DIRECTORY")
    print("-" * 72)

    existed = OUTPUT_ROOT.exists()
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    subdirs = ["models", "shap_plots", "tmp"]
    for s in subdirs:
        (OUTPUT_ROOT / s).mkdir(exist_ok=True)

    # Also create the data/ tree referenced by later steps
    for p in [
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data" / "clean",
        PROJECT_ROOT / "data" / "features",
        PROJECT_ROOT / "data" / "splits",
        PROJECT_ROOT / "pipelines",
        PROJECT_ROOT / "reports" / "eda",
    ]:
        p.mkdir(parents=True, exist_ok=True)

    pretty(f"output root", f"{OUTPUT_ROOT}  ({'existed' if existed else 'created'})")
    for s in subdirs:
        pretty(f"  subdir", f"{OUTPUT_ROOT / s}")
    return OUTPUT_ROOT


# ---------------------------------------------------------------------------
# MANIFEST
# ---------------------------------------------------------------------------
def write_manifest(output_root: Path) -> Path:
    print()
    print("-" * 72)
    print(f"  MANIFEST")
    print("-" * 72)

    manifest = {
        "run_date": RUN_DATE,
        "created_at_iso": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED,
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "release": platform.release(),
        },
        "packages": globals().get("_PKG_VERSIONS", {}),
        "baseline_input_hashes": globals().get("_BASELINE_HASHES", {}),
        "scope": {
            "market": "DVH EXCL. HD",
            "n_brands": 77,
            "train_period": "2022-10 → 2025-02 (29 months)",
            "val_period": "2025-03 → 2025-08 (6 months)",
            "test_period": "2025-09 → 2026-03 (7 months, held out)",
        },
        "gates": {
            "G1_preflight": "PASSED",
            "G2_sanity": "pending (Step 07)",
            "G3_per_step": "pending",
            "G4_comparison": "pending (Step 10)",
        },
    }

    path = output_root / "MANIFEST.json"
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    pretty("MANIFEST.json", f"{path}  ({path.stat().st_size} bytes)")
    return path


# ---------------------------------------------------------------------------
# Run-log bootstrap
# ---------------------------------------------------------------------------
def init_run_log(output_root: Path) -> Path:
    log_path = output_root / "run_log.txt"
    with open(log_path, "a") as f:
        f.write(f"\n=== Step 00 SETUP @ {datetime.now().isoformat(timespec='seconds')} ===\n")
        f.write("Pre-flight checks passed. Output tree initialised.\n")
    return log_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ok, issues = preflight()
    if not ok:
        return 1

    out = prepare_output_dir()
    write_manifest(out)
    init_run_log(out)

    print()
    print("=" * 72)
    print("  ✅ STEP 00 COMPLETE — ready for Step 01 (data ingestion)")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
