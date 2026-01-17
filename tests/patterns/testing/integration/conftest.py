import sys
from unittest.mock import MagicMock
import nest_asyncio

# Mock browser-specific modules before any other imports
sys.modules["js"] = MagicMock()
sys.modules["pyodide"] = MagicMock()
sys.modules["pyodide.ffi"] = MagicMock()

def pytest_configure(config):
    nest_asyncio.apply()
