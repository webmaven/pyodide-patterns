import os
import sys
from unittest.mock import MagicMock

import nest_asyncio

# Add src directory to sys.path to allow importing pyodide_app
# This conftest.py is in tests/patterns/testing/integration/
# We need to go up 4 levels to reach the root.
src_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src")
)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Mock browser-specific modules before any other imports
sys.modules["js"] = MagicMock()
sys.modules["pyodide"] = MagicMock()
sys.modules["pyodide.ffi"] = MagicMock()


def pytest_configure(config):
    nest_asyncio.apply()
