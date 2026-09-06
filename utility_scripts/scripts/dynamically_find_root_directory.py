"""
Dynamic project-root finder + PATHS re-export.

Import this from any script that needs the project paths without knowing where
it sits in the tree:

    from utility_scripts.scripts.dynamically_find_root_directory import *

ANCHOR (changed 2026-09-06): the root is located by walking up from this file
until a directory containing ".env.example" (or ".env") is found.

Previously the anchor was "CLAUDE.md". That was replaced because the repository
is shared with assessors, and a filename that advertises the assistant used to
write it is not something to ship. ".env.example" is an equally reliable
root marker -- it exists only at the repo root, in this project and by
near-universal convention -- and it carries no such signal.

Note ".env.example" is force-included in .gitignore (which otherwise excludes
".env.*"), because an anchor that is not committed cannot anchor a fresh clone.

Walking up from __file__ rather than Path.cwd() is deliberate: cwd depends on
where the user happened to invoke python from, so the old cwd-based version
failed whenever a script was run from outside the repo.
"""

from pathlib import Path
import importlib
import sys

ANCHORS = (".env.example", ".env", "PATHS.py")


def find_project_root(start: Path | None = None) -> Path:
    """
    Walk upward from `start` (default: this file) until a directory containing
    one of ANCHORS is found.

    Returns:
        Path to the project root.

    Raises:
        FileNotFoundError: if no anchor is found in any ancestor directory.
    """
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if any((candidate / a).exists() for a in ANCHORS):
            return candidate
    raise FileNotFoundError(
        f"Could not find project root: no {' / '.join(ANCHORS)} in any parent "
        f"of {current}"
    )


ROOT_DIR_FINDER = find_project_root()

if str(ROOT_DIR_FINDER) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR_FINDER))

import PATHS
importlib.reload(PATHS)  # pick up edits without restarting a long-lived session

from PATHS import *  # noqa: F401,F403,E402
