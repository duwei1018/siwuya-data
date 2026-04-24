"""Make `from integrity_framework.src import ...` resolvable in tests.

The repo is a flat data + library hybrid, not a pip-installable package
(yet). conftest.py prepends the parent directory so tests can import
without `pip install -e .` ceremony.
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
