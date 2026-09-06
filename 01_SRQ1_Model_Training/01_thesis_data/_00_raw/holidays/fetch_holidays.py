#!/usr/bin/env python
"""
Fetch Danish public holidays from Nager.Date into the raw tier.

WHY THIS EXISTS
---------------
The feature set carries `month`, `quarter` and `peak_month`, all of which are
identical for a given calendar month in every year. They therefore cannot
represent two things that are true of Danish retail:

  - Easter moves. Skaertorsdag/Langfredag/Paaskedag fall in March in some years
    and April in others, so the number of public holidays in "March" is not a
    property of March.
  - Store Bededag was abolished in 2024. The DK holiday count drops 15 -> 14
    permanently, mid-panel. No month-of-year encoding can express a structural
    break that happens once and persists.

Both are visible in the API response and neither is reachable from `month`.

SOURCE
------
Nager.Date v3, the free public tier:

    https://date.nager.at/api/v3/PublicHolidays/{year}/DK

No API key. (The commercial `nagerholidays.com/api/pro/v1/...` paths return
HTTP 401 without one -- if a future maintainer finds empty responses, that host
is why.) DK holidays come back with global=true, types=["Public"] and
counties=null, so there is no regional split to resolve.

TWO ENTRY POINTS, ONE CACHE
---------------------------
    python fetch_holidays.py --years 2019-2027       # standalone, seconds
    python fetch_holidays.py --years 2019-2027 --force

and the same function is called by the Nielsen refetch path so a warehouse
re-pull refreshes holidays in the same motion. Standalone matters because a
Nielsen pull is ~10 minutes at minimum (~2 hours with --download-raw), and
iterating on feature engineering must not cost that.

Per-year caching means a rerun that finds every year present does no network
work at all unless --force is passed.

FAILURE BEHAVIOUR
-----------------
This module fails loudly and never fabricates. If a year cannot be fetched and
is not cached, it is reported as missing and excluded from `years_covered`.
The DECISION about whether to run with or without holiday enrichment is made
downstream in step 3, which records it in the contract -- it is never made
silently here. See the module docstring of step_3_derive_params.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# Repo root on sys.path so `import PATHS` resolves when run as a script.
def _find_repo_root() -> Path:
    """Walk up to the repo root (anchored on .env.example) instead of a fixed
    parents[N] hop, which breaks whenever the file changes folder depth."""
    _start = Path(__file__).resolve().parent
    for _cand in (_start, *_start.parents):
        if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
            return _cand
    raise FileNotFoundError(f"Could not find project root above {_start}")


_REPO_ROOT = _find_repo_root()
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PATHS import THESIS_DATA_RAW_DIR  # noqa: E402

API_BASE = "https://date.nager.at/api/v3/PublicHolidays"
COUNTRY = "DK"
TIMEOUT_S = 20

HOLIDAYS_DIR: Path = THESIS_DATA_RAW_DIR / "holidays"
CACHE_DIR: Path = HOLIDAYS_DIR / "nager_dk"
MANIFEST_PATH: Path = HOLIDAYS_DIR / "nager_dk_manifest.json"


class HolidayFetchError(RuntimeError):
    """A year could not be fetched and was not already cached."""


def _cache_path(year: int) -> Path:
    return CACHE_DIR / f"dk_{year}.json"


def fetch_year(year: int, *, force: bool = False) -> tuple[list[dict], str]:
    """Return (holidays, source) for one year, where source is 'cache' or 'api'.

    Cache-first. A cached year costs nothing; --force re-pulls it. Raises
    HolidayFetchError only when the API fails AND no cache exists, because a
    stale cache is strictly better than no feature -- the staleness is recorded
    in the manifest either way.
    """
    path = _cache_path(year)

    if path.exists() and not force:
        return json.loads(path.read_text(encoding="utf-8")), "cache"

    url = f"{API_BASE}/{year}/{COUNTRY}"
    try:
        resp = requests.get(url, timeout=TIMEOUT_S)
        resp.raise_for_status()
        holidays = resp.json()
    except Exception as exc:
        # Fall back to a stale cache before failing. Refetch -> cached -> fail.
        if path.exists():
            print(f"  {year}: API failed ({exc}); using cached copy")
            return json.loads(path.read_text(encoding="utf-8")), "cache-stale"
        raise HolidayFetchError(
            f"Could not fetch DK holidays for {year} and no cache exists.\n"
            f"  URL: {url}\n"
            f"  Error: {exc}\n"
            f"  The pipeline can still run without holiday enrichment; step 3\n"
            f"  will record holiday_enrichment=false in the contract."
        ) from exc

    if not isinstance(holidays, list) or not holidays:
        raise HolidayFetchError(
            f"DK holidays for {year} came back empty or malformed: {url}"
        )

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(holidays, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return holidays, "api"


def fetch_years(years: list[int], *, force: bool = False) -> dict:
    """Fetch every year, write the manifest, return it.

    The manifest is the provenance record that makes "we pulled DK public
    holidays from Nager.Date on <date>" a methods sentence rather than a claim.
    It carries a content hash per year so a silent upstream revision (exactly
    what the 2024 Store Bededag change was) is detectable on a later re-pull.
    """
    entries: dict[str, dict] = {}
    missing: list[int] = []

    for year in years:
        try:
            holidays, source = fetch_year(year, force=force)
        except HolidayFetchError as exc:
            print(f"  {year}: MISSING -- {exc.args[0].splitlines()[0]}")
            missing.append(year)
            continue

        payload = json.dumps(holidays, sort_keys=True, ensure_ascii=False)
        entries[str(year)] = {
            "n_holidays": len(holidays),
            "source": source,
            "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16],
        }
        print(f"  {year}: {len(holidays):2d} holidays ({source})")

    # The manifest describes THE CACHE, not this invocation. Without this
    # merge, `--years 2023-2025` after a 2018-2027 pull would rewrite
    # years_covered to three years while ten remained on disk -- and step 3,
    # which trusts the manifest, would then refuse enrichment for a panel that
    # is in fact fully covered.
    for path in sorted(CACHE_DIR.glob("dk_*.json")) if CACHE_DIR.exists() else []:
        year = path.stem.removeprefix("dk_")
        if year in entries:
            continue
        holidays = json.loads(path.read_text(encoding="utf-8"))
        payload = json.dumps(holidays, sort_keys=True, ensure_ascii=False)
        entries[year] = {
            "n_holidays": len(holidays),
            "source": "cache",
            "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16],
        }

    # A year that failed this run but is cached from an earlier one is covered,
    # not missing.
    missing = [y for y in missing if str(y) not in entries]

    manifest = {
        "source": "Nager.Date v3",
        "url_template": f"{API_BASE}/{{year}}/{COUNTRY}",
        "country": COUNTRY,
        "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "years_covered": sorted(int(y) for y in entries),
        "years_missing": missing,
        "years": entries,
    }

    HOLIDAYS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def load_manifest() -> dict | None:
    """Read the manifest, or None if holidays have never been fetched.

    Consumers use the None case to mean "no enrichment available" -- it is a
    legitimate state, not an error, and step 3 records it in the contract.
    """
    if not MANIFEST_PATH.exists():
        return None
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_holiday_dates() -> tuple[list[str], list[int]]:
    """Return (ISO date strings, years_covered) for every cached year.

    Returns ([], []) when nothing has been fetched. Callers must treat an empty
    years_covered as "enrichment unavailable" and must NOT interpret a panel
    month outside years_covered as zero holidays -- that would fabricate a
    measurement. See build_holiday_features().
    """
    manifest = load_manifest()
    if manifest is None:
        return [], []

    dates: list[str] = []
    for year in manifest["years_covered"]:
        path = _cache_path(year)
        if not path.exists():
            continue
        for holiday in json.loads(path.read_text(encoding="utf-8")):
            dates.append(holiday["date"])

    return sorted(dates), list(manifest["years_covered"])


def _parse_years(spec: str) -> list[int]:
    """Accept '2019-2027' or '2019,2020,2021'."""
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return list(range(int(lo), int(hi) + 1))
    return [int(part) for part in spec.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch DK public holidays from Nager.Date into the raw tier."
    )
    parser.add_argument(
        "--years",
        default="2018-2027",
        help="Year range '2019-2027' or list '2019,2020'. Default 2018-2027 "
             "covers the Nielsen panel with room either side.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-pull years already cached (use after an upstream revision).",
    )
    args = parser.parse_args()

    years = _parse_years(args.years)
    print(f"Fetching DK public holidays for {years[0]}-{years[-1]} (Nager.Date v3)")

    manifest = fetch_years(years, force=args.force)

    covered = manifest["years_covered"]
    print(f"\nCached {len(covered)} years -> {CACHE_DIR}")
    print(f"Manifest -> {MANIFEST_PATH}")
    if manifest["years_missing"]:
        print(f"MISSING years: {manifest['years_missing']}")
        print("Pipeline can still run; step 3 will record the reduced coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
