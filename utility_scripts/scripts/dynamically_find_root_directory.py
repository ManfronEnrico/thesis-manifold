# Import the config file from the project root to centralize all directories
from pathlib import Path   
import importlib

# Find project root by locating CLAUDE.md -> helps dynamically finding the project root regardless of where the script is run from                                                                                                                                                                                                                                                          
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        ROOT_DIR_FINDER = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

import sys
print(f"Project root found at: {ROOT_DIR_FINDER}")
sys.path.insert(0, str(ROOT_DIR_FINDER))


import PATHS
importlib.reload(PATHS)  # Reload the config module to ensure we have the latest changes

from PATHS import *